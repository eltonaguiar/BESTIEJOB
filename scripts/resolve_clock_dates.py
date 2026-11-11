#!/usr/bin/env python3
"""resolve_clock_dates.py — end the rows whose `postedDate` is the scan clock.

`tools/normalize_exa_rounds.py` wrote `posted = r.get("publishedDate") or stamp`,
and `scripts/merge_bucket_jobs.py` wrote `datetime.now()` when a bucket row had no
date. Both put the moment of the scan into a field the README defines as "the date
shown by the source" — the one thing the board promises never to do. The README
row for those URLs carries the same day, because it was written by that same scan,
so re-dating from the board is laundering, not repair. That was tried on
2026-11-11 and reverted: 103 of 105 "fixed" rows kept the identical calendar day.

This script asks the posting instead:

  1. `scripts/ats_date_resolve.py` for Workday / SmartRecruiters (their own JSON)
  2. the page's JSON-LD `datePosted`, then `article:published_time`, then an
     `itemprop="datePosted"` value

A date is accepted only when it is absolute, in the past, and inside the board's
window. Anything else leaves the row **undated**: `postedDate: null` plus
`dateSource: "missing"` in the feed, and no dated table row in the README (the
board's rule is "no date, no row"). The removed README rows are archived next to
it, so a posting is never silently lost.

Usage
    python3 scripts/resolve_clock_dates.py                 # report only
    python3 scripts/resolve_clock_dates.py --apply
    python3 scripts/resolve_clock_dates.py --apply --workers 8
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import ats_date_resolve                                     # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
CLOCK_TOLERANCE = 120        # seconds; postedDate this close to scrapedAt is the clock
MAX_AGE_DAYS = 45
TODAY = datetime.now(timezone.utc).date()

JSONLD = re.compile(r'"datePosted"\s*:\s*"([^"]{4,40})"')
META = re.compile(r'<meta[^>]+(?:property|name)=["\']article:published_time["\']'
                  r'[^>]+content=["\']([^"\']{4,40})', re.I)
ITEMPROP = re.compile(r'itemprop=["\']datePosted["\'][^>]*content=["\']([^"\']{4,40})', re.I)
DATE_CELL = re.compile(r"^(\|\s*)(\d{4}-\d{2}-\d{2})(\s*\|)")


def parse_dt(value) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def clock_rows(jobs: list[dict]) -> list[dict]:
    out = []
    for j in jobs:
        posted, scraped = parse_dt(j.get("postedDate")), parse_dt(j.get("scrapedAt"))
        if posted and scraped and abs((posted - scraped).total_seconds()) <= CLOCK_TOLERANCE:
            out.append(j)
    return out


def plausible(iso: str) -> str | None:
    try:
        d = date.fromisoformat(iso[:10])
    except ValueError:
        return None
    if TODAY + timedelta(days=1) < d or d < TODAY - timedelta(days=MAX_AGE_DAYS):
        return None
    return d.isoformat()


def from_page(url: str) -> tuple[str, str] | None:
    """(date, which-field) from the posting's own markup, or None."""
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-CA,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status != 200:
                return None
            html = resp.read(900_000).decode("utf-8", "replace")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None
    for pattern, label in ((JSONLD, "json-ld"), (META, "meta"), (ITEMPROP, "microdata")):
        m = pattern.search(html)
        if not m:
            continue
        iso = plausible(m.group(1).strip())
        if iso:
            return iso, label
    return None


def resolve(url: str) -> tuple[str, str] | None:
    try:
        ats = ats_date_resolve.resolve(url)
    except Exception:                                    # noqa: BLE001
        ats = None
    if ats:
        iso = plausible(ats)
        if iso:
            return iso, "ats-json"
    return from_page(url)


def rewrite_readme(path: Path, dates: dict[str, str], undated: set[str],
                   archive: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    kept, removed, relabelled = [], [], 0
    for line in lines:
        if not line.startswith("| 20"):
            kept.append(line)
            continue
        m = re.search(r"\((https?://[^)\s]+)\)", line)
        if not m:
            kept.append(line)
            continue
        url = m.group(1)
        iso = dates.get(url)
        if iso:
            new, n = DATE_CELL.subn(lambda c: f"{c.group(1)}{iso}{c.group(3)}", line, count=1)
            relabelled += n
            kept.append(new)
        elif url in undated:
            removed.append(line)
        else:
            kept.append(line)
    if removed:
        archive.write_text("# Rows removed: postedDate was the scan clock and the posting "
                           "states no date\n# rule: no date, no row in a dated table\n\n"
                           + "\n".join(removed) + "\n", encoding="utf-8")
    path.write_text("\n".join(kept) + "\n", encoding="utf-8")
    return {"relabelled": relabelled, "removed": len(removed)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="only the first N rows (debug)")
    args = ap.parse_args()

    root = Path(args.repo)
    feed_path = root / "jobs.json"
    payload = json.loads(feed_path.read_text(encoding="utf-8"))
    jobs = payload["jobs"] if isinstance(payload, dict) else payload
    targets = clock_rows(jobs)
    if args.limit:
        targets = targets[: args.limit]

    urls = sorted({j.get("url", "") for j in targets if j.get("url")})
    print(f"clock-date rows: {len(targets)}  unique URLs: {len(urls)}")
    with futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        got = dict(zip(urls, ex.map(resolve, urls)))

    dates = {u: v[0] for u, v in got.items() if v}
    undated = {u for u in urls if not got.get(u)}
    by_field: dict[str, int] = {}
    for res in got.values():
        if res:
            by_field[res[1]] = by_field.get(res[1], 0) + 1
    print(f"resolved from the posting: {len(dates)}  {by_field}")
    print(f"posting states no date:    {len(undated)}")
    for u in urls[:8]:
        print(f"  {got.get(u, ('-', ''))[0] if got.get(u) else '—':12} "
              f"{(got.get(u) or ('','none'))[1]:10} {u[:88]}")

    if not args.apply:
        print("\ndry run — pass --apply to write")
        return 0

    changed = 0
    for j in jobs:
        u = j.get("url", "")
        if u in dates:
            j["postedDate"] = f"{dates[u]}T12:00:00.000Z"
            j["dateSource"] = f"posting:{got[u][1]}"
            changed += 1
        elif u in undated:
            j["postedDate"] = None
            j["dateSource"] = "missing"
            changed += 1
    if isinstance(payload, dict) and "meta" in payload:
        payload["meta"]["undated"] = sum(1 for j in jobs if not j.get("postedDate"))
    feed_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
                         encoding="utf-8")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive = root / f"README.UNDATED_{stamp}.md"
    readme_stats = rewrite_readme(root / "README.md", dates, undated, archive)
    report = {"generatedAt": datetime.now(timezone.utc).isoformat(),
              "clockRows": len(targets), "resolved": len(dates),
              "byResolver": by_field, "undated": len(undated),
              "feedRowsChanged": changed, **readme_stats,
              "resolvedMap": dates, "undatedUrls": sorted(undated)}
    out = root / "reports" / f"clock_dates_{TODAY.isoformat()}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"feed rows changed: {changed}  README relabelled: {readme_stats['relabelled']}"
          f"  README rows removed: {readme_stats['removed']}")
    print(f"archive: {archive.name if readme_stats['removed'] else '(nothing removed)'}")
    print(f"report:  {out.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""audit_today.py — check the rows the board publishes for one day.

Three questions, one pass over the rows dated `--date`:

1. **Dead links** — does the URL still answer?  401/403/429 prove the posting
   exists behind a wall, so only 404/410, other 4xx/5xx and network failures
   count as dead.
2. **Wrong dates** — two shapes.  (a) *clock*: `postedDate` equals `scrapedAt`
   to the second, so the feed is showing when we scanned the posting, not when
   it was posted.  (b) *mismatch*: the posting's own page or ATS JSON states a
   different date than the feed row claims.
3. **Off-title** — the row does not name ServiceNow, Salesforce, or one of their
   modules/certs anywhere in title, tags or excerpt (e.g. a generic backend
   role pulled in by an Adzuna keyword match).

The audit never edits the board.  It writes a report plus an optional JSON list
of rows that should be dropped or re-dated, so the decision stays reviewable.

Usage
    python3 scripts/audit_today.py
    python3 scripts/audit_today.py --date 2026-11-09 --workers 8
    python3 scripts/audit_today.py --local jobs.json --out reports/audit.md
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

try:
    from ats_date_resolve import resolve as ats_date  # noqa: E402
except Exception:                                     # pragma: no cover - optional
    def ats_date(_url: str) -> str | None:            # type: ignore[misc]
        return None

LIVE_FEED = "https://eltonaguiar.github.io/BESTIEJOB/jobs.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

SN = re.compile(r"service\s?now|\bcsdm\b|\bcmdb\b|\bitsm\b|\bitam\b|\bitom\b|"
                r"\bhrsd\b|\bsecops\b|\bcsa\b|\bcad\b|\bcis\b|\bnow assist\b|"
                r"\bflow designer\b|\bservice catalog\b|\bglide\b", re.I)
SF = re.compile(r"salesforce|\bapex\b|\bsoql\b|\blwc\b|lightning|visualforce|"
                r"agentforce|\bcpq\b|mulesoft|\bsfdc\b|experience cloud|"
                r"platform (?:developer|administrator|admin)", re.I)

PAGE_DATE = [
    re.compile(r'"datePosted"\s*:\s*"([^"]{8,40})"'),
    re.compile(r'property=["\']article:published_time["\']\s+content=["\']([^"\']+)'),
    re.compile(r'itemprop=["\']datePosted["\']\s+content=["\']([^"\']+)'),
    re.compile(r'(?:date\s+posted|posted\s+on|posted)\s*:?\s*(\d{1,2}/\d{1,2}/\d{4})', re.I),
    re.compile(r'(?:date\s+posted|posted\s+on|posted)\s*:?\s*'
               r'([A-Z][a-z]{2,8}\.?\s+\d{1,2},\s*\d{4})'),
]


def as_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def page_date(url: str, timeout: int) -> tuple[str | None, str]:
    """(ISO date the posting itself states, verdict about the link)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                              "Accept": "text/html,application/json,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            body = resp.read(300_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 429):
            return None, "walled"
        return None, f"dead:http-{exc.code}"
    except Exception as exc:                          # noqa: BLE001
        return None, f"dead:{type(exc).__name__}"
    if status >= 400:
        return None, f"dead:http-{status}"
    for pattern in PAGE_DATE:
        m = pattern.search(body)
        if not m:
            continue
        raw = m.group(1).strip()
        for parse in (lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")),
                      lambda s: datetime.strptime(s[:10], "%Y-%m-%d"),
                      lambda s: datetime.strptime(s, "%m/%d/%Y"),
                      lambda s: datetime.strptime(s, "%B %d, %Y"),
                      lambda s: datetime.strptime(s, "%b %d, %Y"),
                      lambda s: datetime.strptime(s, "%b. %d, %Y")):
            try:
                return parse(raw).date().isoformat(), "live"
            except (ValueError, TypeError):
                continue
    return None, "live"          # page answered; it just states no date


def check(job: dict, day: str, timeout: int) -> dict:
    url = job.get("url") or ""
    posted = (job.get("postedDate") or "")[:10]
    scraped = as_dt(job.get("scrapedAt"))
    posted_dt = as_dt(job.get("postedDate"))
    flags: list[str] = []

    hay = " ".join(str(job.get(k) or "") for k in ("title", "company", "excerpt", "tags"))
    if not (SN.search(hay) or SF.search(hay)):
        flags.append("off-title")

    # (a) the feed is reporting the scan clock as the posting date
    if scraped and posted_dt and abs((posted_dt - scraped).total_seconds()) <= 120:
        flags.append("clock-date")

    stated, verdict = (None, "skipped")
    if url.startswith("http"):
        stated, verdict = page_date(url, timeout)
        if verdict.startswith("dead"):
            flags.append(verdict)
        elif stated is None:
            stated = ats_date(url)
    if stated and posted and stated != posted:
        flags.append(f"date-mismatch(page={stated})")

    return {"title": job.get("title") or "", "company": job.get("company") or "",
            "location": job.get("location") or "", "url": url,
            "source": job.get("source") or "", "posted": posted,
            "scraped": (job.get("scrapedAt") or "")[:19], "stated": stated or "—",
            "flags": flags}


def render(rows: list[dict], day: str, total: int) -> str:
    dead = [r for r in rows if any(f.startswith("dead:") for f in r["flags"])]
    clock = [r for r in rows if "clock-date" in r["flags"]]
    off = [r for r in rows if "off-title" in r["flags"]]
    mism = [r for r in rows if any(f.startswith("date-mismatch") for f in r["flags"])]
    walled = [r for r in rows if "walled" in r["flags"]]
    clean = [r for r in rows if not r["flags"]]
    lines = [f"# Board audit — rows dated {day}", "",
             f"Checked {total} rows from the live feed at "
             f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.", "",
             "| Finding | Rows |", "|---|---|",
             f"| clean | {len(clean)} |",
             f"| dead link | {len(dead)} |",
             f"| date is the scan clock | {len(clock)} |",
             f"| date disagrees with the posting | {len(mism)} |",
             f"| does not name ServiceNow/Salesforce | {len(off)} |",
             f"| behind a login wall (counts as live) | {len(walled)} |", ""]

    def table(title: str, subset: list[dict], note: str) -> None:
        lines.append(f"## {title} ({len(subset)})")
        if note:
            lines.append(note)
        if not subset:
            lines.append("_none_")
            lines.append("")
            return
        lines.append("")
        lines.append("| Role | Company | Feed date | Posting states | Flags | URL |")
        lines.append("|---|---|---|---|---|---|")
        for r in subset:
            t = r["title"][:70].replace("|", "/")
            lines.append(f"| {t} | {r['company'][:32].replace('|', '/')} | {r['posted']} "
                         f"| {r['stated']} | {', '.join(r['flags'])} | {r['url']} |")
        lines.append("")

    table("Dead links", dead, "The URL no longer answers — drop or replace.")
    table("Dates that are the scan clock",
          clock, "`postedDate` equals `scrapedAt`, so the board is showing when we "
                 "scanned it. Re-date from the source or drop.")
    table("Dates that disagree with the posting", mism, "")
    table("Off-title rows", off, "No ServiceNow/Salesforce term in title, tags or excerpt.")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    ap.add_argument("--feed", default=LIVE_FEED)
    ap.add_argument("--local", help="read jobs.json from disk instead of the feed")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="")
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    if args.local:
        payload = json.loads(Path(args.local).read_text(encoding="utf-8"))
    else:
        with urllib.request.urlopen(args.feed, timeout=60) as resp:
            payload = json.loads(resp.read())
    jobs = payload.get("jobs", payload) if isinstance(payload, dict) else payload
    todays = [j for j in jobs if (j.get("postedDate") or "")[:10] == args.date]
    if args.limit:
        todays = todays[: args.limit]
    print(f"[audit] {args.date}: {len(todays)} rows in the feed")

    with futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(lambda j: check(j, args.date, args.timeout), todays))

    out = Path(args.out) if args.out else ROOT / "reports" / f"audit_{args.date}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rows, args.date, len(todays)), encoding="utf-8")
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(rows, indent=2), encoding="utf-8")

    from collections import Counter
    counts = Counter(f.split("(")[0] for r in rows for f in r["flags"])
    print(f"[audit] flagged: {dict(counts) or 'none'} | clean "
          f"{sum(1 for r in rows if not r['flags'])}/{len(rows)}")
    print(f"[audit] report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

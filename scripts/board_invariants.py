#!/usr/bin/env python3
"""Audit the board against the rules it publishes about itself.

The README makes four promises, and each one has already been broken at least
once by a scrape that looked fine:

  * "`Posted` is the date shown by the source, not a board's relative days ago."
    — so a future date is fabricated, a row older than the 30-day window does
    not belong in a dated table, and a `postedDate` that equals `scrapedAt` is
    the scan clock wearing a date's clothes.
  * "deduplicated by URL" — so one URL may appear once, with one date.
  * the location comes from the posting, so it must name a province or country
    when the posting does.
  * vendor sales titles and "a job *at* the product vendor" are excluded.

`check_inbox.py` guards rows on the way *in*; `readme_job_row_guard.py` guards
against mass deletion. Nothing audited the rows already published, which is how
663 explicit-US postings and a duplicated Built In date sat on a Toronto board.
This checker reads the published files and reports. It never edits.

Severity: `error` fails the run (a promise broken by the file as it stands),
`warning` is counted and listed for triage but does not fail. Pass
`--fail-on warning` to make CI strict.

Usage
    python3 scripts/board_invariants.py
    python3 scripts/board_invariants.py --repo /path/to/clone
    python3 scripts/board_invariants.py --fail-on warning --json-out reports/invariants.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from locscope import region_of                                  # noqa: E402

SCAN_START, SCAN_END = "<!-- DAILY-SCAN:START -->", "<!-- DAILY-SCAN:END -->"

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
DATE_RE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*$")
SEPARATOR_RE = re.compile(r"^:?-{2,}:?$")
COUNT_RE = re.compile(r"\*\*(\d[\d,]*)\s+live postings\*\*")

# An explicit country is decided by tools/locscope.py so this audit and
# enforce_canada_scope.py cannot disagree about the same row.
CA_RE = re.compile(
    r"\b(Canada|Ontario|Quebec|Québec|British Columbia|Alberta|Manitoba|Saskatchewan|"
    r"Nova Scotia|New Brunswick|Newfoundland|Prince Edward Island|Yukon|Nunavut|"
    r"Northwest Territories|ON|BC|QC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b")

# "vendor sales titles" — the exclusion the registry's rules name explicitly.
VENDOR_CO = re.compile(r"\bservice\s?now\b|\bsalesforce\b", re.I)
SALES_TITLE = re.compile(
    r"\b(account executive|account manager|sales director|sales representative|"
    r"sales executive|sales development|partner sales|pre-?sales|enterprise sales|"
    r"commercial account|sales manager|business development)\b", re.I)
# A row can name a sales motion and still be an engineering role.
ENG_TITLE = re.compile(
    r"\b(developer|engineer|architect|administrator|admin|analyst|consultant|"
    r"technical|qa|integration|implementation|specialist)\b", re.I)

# A Company/Title cell a scraper filled with its own bookkeeping instead of data.
PLACEHOLDER = re.compile(
    r"^(apparent duplicate|official\b|unknown\s*/|not specified|remote canada position at)",
    re.I)


def strip_scan_echo(text: str) -> str:
    """Drop the verbatim scanner echo block, which repeats rows by design."""
    if SCAN_START in text and SCAN_END in text:
        start = text.index(SCAN_START)
        end = text.index(SCAN_END) + len(SCAN_END)
        return text[:start] + text[end:]
    return text


# A markdown table escapes a pipe inside a cell as \| — splitting on the raw
# character turns `[Staff Security Engineer \| Enterprise Security](url)` into
# two cells whose first half has no link at all.
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


def split_row(line: str):
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells = [c.strip() for c in CELL_SPLIT_RE.split(s)]
    return cells if len(cells) >= 3 else None


def is_separator(cells) -> bool:
    return all(SEPARATOR_RE.match(c) for c in cells if c)


def parse_readme(path: Path) -> tuple[list[dict], int | None]:
    text = path.read_text(encoding="utf-8")
    claimed = None
    m = COUNT_RE.search(text)
    if m:
        claimed = int(m.group(1).replace(",", ""))
    rows = []
    for lineno, line in enumerate(strip_scan_echo(text).splitlines(), 1):
        cells = split_row(line)
        if not cells or is_separator(cells):
            continue
        dm = DATE_RE.match(cells[0].strip().strip("*"))
        if not dm:
            continue
        lk = LINK_RE.search(line)
        if not lk:
            continue
        rows.append({
            "line": lineno,
            "posted": dm.group(1),
            "title": lk.group(1),
            "url": lk.group(2),
            "company": cells[2] if len(cells) > 2 else "",
            "location": cells[3] if len(cells) > 3 else "",
        })
    return rows, claimed


def normalise_url(url: str) -> str:
    """Match the merger/guard: keep the query string, drop scheme and trailing slash."""
    u = (url or "").strip().lower()
    u = re.sub(r"^https?://(www\.)?", "", u)
    return u.rstrip("/")


def identity(row: dict) -> str:
    squash = lambda s: " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).split())
    return f"{squash(row['company'])}|{squash(row['title'])}"


def audit_readme(rows: list[dict], claimed: int | None, today: date) -> list[dict]:
    findings: list[dict] = []

    def add(kind, severity, row, note):
        findings.append({"kind": kind, "severity": severity, "note": note,
                         "line": row.get("line"), "posted": row.get("posted"),
                         "title": row.get("title", ""), "company": row.get("company", ""),
                         "location": row.get("location", ""), "url": row.get("url", "")})

    horizon = today - timedelta(days=30)
    for r in rows:
        try:
            posted = date.fromisoformat(r["posted"])
        except ValueError:
            add("bad-date", "error", r, f"{r['posted']} is not a calendar date")
            continue
        if posted > today:
            add("future-date", "error", r, f"posted {r['posted']} is after today {today}")
        if posted < horizon:
            add("outside-window", "error", r,
                f"posted {r['posted']} precedes the 30-day window ({horizon})")

        company, title = r["company"], r["title"]
        if PLACEHOLDER.match(company) or PLACEHOLDER.match(title):
            add("placeholder-cell", "error", r, "Company or Role cell holds scraper bookkeeping, not data")
        if "](" in company or "](" in r["location"]:
            add("split-row", "error", r, "a link leaked into the Company/Location cell — the row's pipes are wrong")

        loc = r["location"]
        if loc and region_of(loc) and region_of(loc) != "ca":
            add("non-canada", "error", r, f"location is explicitly outside Canada: {loc}")
        elif loc and not CA_RE.search(loc) and "remote" not in loc.lower():
            add("location-ambiguous", "warning", r, f"location names no province or country: {loc}")

        if VENDOR_CO.search(company) and SALES_TITLE.search(title) and not ENG_TITLE.search(title):
            add("vendor-sales", "error", r, "sales/exec role at the product vendor — excluded by the board's rules")

    if claimed is not None and claimed != len(rows):
        findings.append({"kind": "count-disagreement", "severity": "warning",
                         "note": f"header claims {claimed} live postings, tables hold {len(rows)}",
                         "line": None, "posted": "", "title": "", "company": "",
                         "location": "", "url": ""})

    by_url: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_url[normalise_url(r["url"])].append(r)
    for key, group in by_url.items():
        dates = {g["posted"] for g in group}
        if len(group) > 1 and len(dates) > 1:
            findings.append({"kind": "url-date-conflict", "severity": "error",
                             "note": f"one URL, {len(dates)} different dates: {sorted(dates)}",
                             "line": group[0]["line"], "posted": group[0]["posted"],
                             "title": group[0]["title"], "company": group[0]["company"],
                             "location": group[0]["location"], "url": group[0]["url"]})
        elif len(group) > 1:
            findings.append({"kind": "duplicate-url", "severity": "warning",
                             "note": f"same URL appears {len(group)} times",
                             "line": group[0]["line"], "posted": group[0]["posted"],
                             "title": group[0]["title"], "company": group[0]["company"],
                             "location": group[0]["location"], "url": group[0]["url"]})

    by_ident: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_ident[identity(r)].append(r)
    for key, group in by_ident.items():
        if len({g["posted"] for g in group}) > 1:
            findings.append({"kind": "identity-date-conflict", "severity": "warning",
                             "note": f"{len(group)} rows, {len({g['posted'] for g in group})} dates, "
                                     f"{len({normalise_url(g['url']) for g in group})} URLs",
                             "line": group[0]["line"], "posted": group[0]["posted"],
                             "title": group[0]["title"], "company": group[0]["company"],
                             "location": group[0]["location"], "url": group[0]["url"]})
    return findings


def audit_jobs_json(path: Path) -> tuple[list[dict], int]:
    """The feed's own date rule: postedDate must come from the posting."""
    if not path.exists():
        return [], 0
    payload = json.loads(path.read_text(encoding="utf-8"))
    jobs = payload.get("jobs", []) if isinstance(payload, dict) else payload
    findings = []

    def parse(value):
        if not value:
            return None
        try:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return None
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)

    for j in jobs:
        posted, scraped = parse(j.get("postedDate")), parse(j.get("scrapedAt"))
        if posted and scraped and abs((posted - scraped).total_seconds()) <= 120:
            findings.append({"kind": "clock-date", "severity": "error",
                             "note": f"postedDate {j.get('postedDate')} equals scrapedAt — this is the scan clock",
                             "line": None, "posted": (j.get("postedDate") or "")[:19],
                             "title": j.get("title") or "", "company": j.get("company") or "",
                             "location": j.get("location") or "", "url": j.get("url") or ""})
        # A date the writer could not source must never reach the feed at all.
        if j.get("postedDate") and j.get("dateSource") == "missing":
            findings.append({"kind": "date-without-source", "severity": "error",
                             "note": "postedDate is set but dateSource says the posting has no date",
                             "line": None, "posted": (j.get("postedDate") or "")[:19],
                             "title": j.get("title") or "", "company": j.get("company") or "",
                             "location": j.get("location") or "", "url": j.get("url") or ""})
    return findings, len(jobs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=str(ROOT), help="clone to audit (default: this repo)")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD; default is the system date")
    ap.add_argument("--fail-on", choices=("error", "warning"), default="error")
    ap.add_argument("--samples", type=int, default=6, help="examples printed per finding kind")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--baseline", default="reports/board_invariants_baseline.json",
                    help="recorded per-kind counts that may not grow (ratchet)")
    ap.add_argument("--write-baseline", action="store_true",
                    help="record the current counts as the new baseline")
    ap.add_argument("--no-baseline", action="store_true", help="ignore any recorded baseline")
    args = ap.parse_args()

    root = Path(args.repo)
    today = date.fromisoformat(args.today) if args.today else datetime.now(timezone.utc).date()

    rows, claimed = parse_readme(root / "README.md")
    findings = audit_readme(rows, claimed, today)
    feed_findings, feed_rows = audit_jobs_json(root / "jobs.json")
    findings.extend(feed_findings)

    by_kind = Counter(f["kind"] for f in findings)
    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] == "warning"]

    print(f"README: {len(rows)} posting rows (header claims {claimed if claimed is not None else '—'})")
    print(f"jobs.json: {feed_rows} rows")
    print(f"{'kind':26s} {'severity':9s} count")
    print("-" * 48)
    for kind, count in sorted(by_kind.items(), key=lambda kv: (-kv[1], kv[0])):
        sev = "error" if any(f["kind"] == kind and f["severity"] == "error" for f in findings) else "warning"
        print(f"{kind:26s} {sev:9s} {count}")

    for kind, _ in sorted(by_kind.items(), key=lambda kv: (-kv[1], kv[0])):
        sample = [f for f in findings if f["kind"] == kind][: args.samples]
        print(f"\n--- {kind} ---")
        for f in sample:
            where = f"line {f['line']}" if f["line"] else "jobs.json"
            print(f"  [{where}] {f['posted']} | {f['title'][:52]} | {f['company'][:26]} "
                  f"| {f['location'][:24]} | {f['url'][:64]}")
            print(f"      {f['note']}")

    print(f"\nerrors={len(errors)} warnings={len(warnings)}")

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"today": today.isoformat(), "readmeRows": len(rows),
                                   "claimed": claimed, "jobsJsonRows": feed_rows,
                                   "counts": dict(by_kind), "findings": findings},
                                  indent=1), encoding="utf-8")
        print(f"report: {out}")

    bl = Path(args.baseline)
    bl = bl if bl.is_absolute() else root / bl
    recorded: dict[str, int] = {}
    if not args.no_baseline and bl.exists():
        recorded = json.loads(bl.read_text(encoding="utf-8")).get("counts", {})
    if args.write_baseline:
        bl.parent.mkdir(parents=True, exist_ok=True)
        bl.write_text(json.dumps({
            "recordedAt": today.isoformat(),
            "why": "per-kind counts as published on this date. Each kind is a ratchet: a later run "
                   "fails when a kind grows past the count here, so legacy debt cannot expand.",
            "counts": dict(by_kind),
        }, indent=1), encoding="utf-8")
        print(f"baseline written: {bl}")
        recorded = dict(by_kind)

    considered = errors if args.fail_on == "error" else errors + warnings
    growing = {k: (c, recorded.get(k, 0)) for k, c in by_kind.items()
               if c > recorded.get(k, 0)}
    failing = [f for f in considered if not recorded or f["kind"] in growing]

    if recorded:
        detail = ", ".join(f"{k} {c}>{was}" for k, (c, was) in growing.items()) or "no kind grew"
        print(f"\nratchet against {bl.name}: {detail}")

    if failing:
        print(f"\nFAIL: {len(failing)} finding(s) violate the board's published rules "
              f"(threshold: {args.fail_on}).", file=sys.stderr)
        return 1
    print("\nPASS: the published board satisfies its own rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

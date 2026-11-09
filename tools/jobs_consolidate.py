#!/usr/bin/env python3
"""
Consolidate README.md into a single low-noise layout.

Result:
  * one "Current jobs" section with exactly three tables — ServiceNow, Salesforce, Other
  * only postings whose posted date is within --days (default 30) of --today
  * everything else (every older row and every legacy prose section) is moved to
    README.BAK_<UTC timestamp>.md, which is kept in the repo

The daily scanner's <!-- DAILY-SCAN --> block is preserved verbatim and moved to the
bottom, because scripts/daily_job_scan.mjs rewrites whatever sits between those markers.

Usage:
  python3 tools/jobs_consolidate.py                 # rewrite README.md
  python3 tools/jobs_consolidate.py --dry-run       # report only
  python3 tools/jobs_consolidate.py --today 2026-11-02 --days 30
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
SCAN_START = "<!-- DAILY-SCAN:START -->"
SCAN_END = "<!-- DAILY-SCAN:END -->"

DATE_RE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*$")
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
ID_RE = re.compile(r"\[([A-Za-z]{0,4})\s*(\d{4,})\]")


def parse_date(cell: str) -> str | None:
    cell = cell.strip().strip("*").strip()
    m = DATE_RE.match(cell)
    return m.group(1) if m else None


def split_row(line: str) -> list[str] | None:
    """Return table cells for a markdown table row, or None if it is not one."""
    if not line.strip().startswith("|"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells if len(cells) >= 3 else None


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def classify(title: str, url: str, location: str = "") -> str:
    hay = f"{title} {url} {location}".lower()
    if re.search(r"service\s?now|\bsn\b|itsm|itam|cmdb|itom", hay):
        return "servicenow"
    if re.search(r"salesforce|apex|visualforce|soql|marketing cloud|sfdc|ncino|vlocity|omnistudio", hay):
        return "salesforce"
    return "other"


# Aggregator result pages masquerading as postings. Evidence: of 367 rows the
# websearch harvesters carried that were absent from the board, the ones with no
# posting id were Exa's answer to "data analyst toronto" — a category or search
# URL, not a role. Each host below has a stable search/category shape, so the URL
# alone identifies it; a real posting on the same host carries an id and does not
# match. Checked against the 39 listing pages in that set (all caught) and every
# URL on the board (only the 7 search pages already listed there matched).
LISTING_RULES = (
    # /jobs/<keywords>-jobs[-<city>] is a search page; /jobs/view/<id> is a posting.
    (r"(^|\.)linkedin\.com$", r"^/jobs/(?!view/)[a-z0-9%-]*-jobs"),
    # Glassdoor marks result pages with -jobs-SRCH_ keys.
    (r"(^|\.)glassdoor\.[a-z.]+$", r"(?i)-jobs-srch_|srch_|/job/jobs\.htm"),
    (r"(^|\.)wellfound\.com$", r"^/role/"),
    # Robert Half category pages: /ca/en/jobs/<city>[/<keyword>]; a posting is
    # /ca/en/jobs/detail/<id>/<slug>, so "detail/" is the exclusion.
    (r"(^|\.)roberthalf\.[a-z.]+$",
     r"^/[a-z]{2}/[a-z]{2}/jobs/(?!detail/)[a-z][a-z0-9-]*(?:/[a-z0-9-]+)?/?$"),
    (r"(^|\.)randstad\.[a-z.]+$", r"^/jobs/q-"),
    (r"(^|\.)eluta\.ca$", r"(?i)-jobs-in-"),
    (r"(^|\.)jobbank\.gc\.ca$", r"^/marketreport/"),
    (r"(^|\.)ziprecruiter\.com$", r"^/Jobs/"),
    (r"(^|\.)whatjobs\.com$", r"^/jobs/[a-z0-9-]+/[a-z0-9-]+/?$"),
    (r"(^|\.)adzuna\.[a-z.]+$", r"^/[a-z0-9-]+/?$"),
    (r"(^|\.)indeed\.[a-z.]+$", r"^/q-"),
    # jobs.ca company hub: /<company> (no /jobs/ segment) is a company landing
    # page, not a posting. A real posting is /<company>/jobs/<slug>-<hash>.
    # Without this, jobs.ca/accenture rendered as a ServiceNow Technical
    # Architect posting (2026-11-09).
    (r"(^|\.)jobs\.ca$", r"^/[a-z0-9-]+/?$"),
)
LISTING_QUERY = re.compile(r"(?i)[?&](q|query|search|keywords?|k|ss|term|what|jobtitle)=")
# Slash-delimited only: "/jobsearch/jobposting/<id>" (Job Bank) and
# "/jobsearch/viewjob/<token>" (Workopolis) are postings, not searches.
LISTING_PATH = re.compile(r"(?i)/(jobs?|careers?)/(search|results|browse)(/|$)")


def is_listing_url(url: str) -> bool:
    """True for an aggregator search/category page, which is not a posting."""
    m = re.match(r"https?://([^/?#]+)([^?#]*)(\?[^#]*)?", url or "")
    if not m:
        return False
    host = m.group(1).lower().removeprefix("www.")
    path = m.group(2) or "/"
    query = m.group(3) or ""
    if LISTING_QUERY.search(query) or LISTING_PATH.search(path):
        return True
    return any(re.search(h, host) and re.search(p, path) for h, p in LISTING_RULES)


# Tracking/session parameters that never identify a posting. LinkedIn adds
# `position`, `pageNum`, `refId`, `trackingId` to the same job link, so without
# these the 2026-11-09 backlog merge kept 123 duplicate postings (guard growth
# 0 -> 123) that the guard — which drops the whole query — counted as repeats.
URL_TRACKING = re.compile(
    r"[?&](utm_[^&]+|se|v|utm_medium|utm_source|refId|trackingId|trk|position|"
    r"pageNum|originalSubdomain|eBP|savedSearchId)=[^&]*",
    re.I,
)


def normalise_url(url: str) -> str:
    url = url.split("#")[0]
    url = URL_TRACKING.sub("", url)
    # A LinkedIn posting is identified by the numeric id in the path; everything
    # after it is search-session noise.
    if re.search(r"linkedin\.com/jobs/view/", url, re.I):
        url = re.split(r"[?#]", url, maxsplit=1)[0]
    return url.rstrip("/?").lower()


def extract_rows(text: str) -> tuple[list[dict], list[str]]:
    """Pull every posting row out of the README, in file order."""
    rows: list[dict] = []
    unmatched: list[str] = []
    for line in text.splitlines():
        cells = split_row(line)
        if not cells or is_separator(cells):
            continue
        posted = parse_date(cells[0])
        link = LINK_RE.search(line)
        if not posted or not link:
            if "http" in line and "|" in line:
                unmatched.append(line.strip()[:160])
            continue
        title, url = link.group(1), link.group(2)
        company = cells[2] if len(cells) > 2 else ""
        location = cells[3] if len(cells) > 3 else ""
        source = ""
        if len(cells) > 4:
            source = " ".join(c for c in cells[4:] if c)
        rows.append(
            {
                "posted": posted,
                "title": title.replace("|", "/").strip(),
                "url": url,
                "company": company.replace("|", "/").strip(),
                "location": location.replace("|", "/").strip(),
                "note": source.replace("|", "/").strip()[:120],
                "family": classify(title, url),
            }
        )
    return rows, unmatched


def dedupe(rows: list[dict]) -> tuple[list[dict], int]:
    seen: dict[str, dict] = {}
    dropped = 0
    for row in rows:
        key = normalise_url(row["url"])
        if key in seen:
            dropped += 1
            # prefer the row that carries a company name
            if not seen[key]["company"] and row["company"]:
                seen[key] = row
            continue
        seen[key] = row
    return list(seen.values()), dropped


def extract_scan_block(text: str) -> str | None:
    if SCAN_START not in text or SCAN_END not in text:
        return None
    start = text.index(SCAN_START)
    end = text.index(SCAN_END) + len(SCAN_END)
    return text[start:end]


def render(jobs: list[dict], today: date, days: int, cutoff: date, archive_name: str) -> str:
    families = [
        ("servicenow", "ServiceNow jobs", "developer / administrator / architect / analyst roles"),
        ("salesforce", "Salesforce jobs", "developer / administrator / architect / consultant roles"),
        ("other", "Other jobs", "ITSM, ITAM, CMDB, SQL, BI, automation and integration roles that match the profile"),
    ]
    counts = {key: sum(1 for j in jobs if j["family"] == key) for key, _, _ in families}
    out: list[str] = []
    out.append("# BESTIEJOB")
    out.append("")
    # Lives in render() rather than in README.md directly: every merge rewrites
    # this file, so a hand-edited banner would vanish on the next run.
    out.append(
        '<h2 align="center"><a href="https://eltonaguiar.github.io/BESTIEJOB/">'
        "▶ Open the live job board — eltonaguiar.github.io/BESTIEJOB</a></h2>"
    )
    out.append("")
    out.append(
        "**[Search, filter and sort every live posting on the web version →]"
        "(https://eltonaguiar.github.io/BESTIEJOB/)**"
    )
    out.append("")
    out.append(
        "Toronto-first ServiceNow / Salesforce / IT-platform job list. "
        "**Three tables, newest first, nothing older than "
        f"{days} days.** Older postings and every legacy section live in `{archive_name}`."
    )
    out.append("")
    out.append("## Contents")
    out.append("")
    out.append(f"- [Current jobs — as of {today.isoformat()}](#current-jobs--as-of-{today.isoformat()})")
    out.append(f"  - [ServiceNow jobs ({counts['servicenow']})](#servicenow-jobs-{counts['servicenow']})")
    out.append(f"  - [Salesforce jobs ({counts['salesforce']})](#salesforce-jobs-{counts['salesforce']})")
    out.append(f"  - [Other jobs ({counts['other']})](#other-jobs-{counts['other']})")
    out.append("- [User / AI agent guide](#user--ai-agent-guide)")
    out.append("- [How to add jobs](#how-to-add-jobs-to-this-file)")
    out.append("- [Archive](#archive)")
    out.append("")
    out.append(f"## Current jobs — as of {today.isoformat()}")
    out.append("")
    out.append(
        f"Window: {cutoff.isoformat()} → {today.isoformat()} · "
        f"**{len(jobs)} live postings** · deduplicated by URL · "
        "`Posted` is the date shown by the source, not a board's relative \"days ago\"."
    )
    out.append("")
    for key, heading, blurb in families:
        group = sorted(
            (j for j in jobs if j["family"] == key), key=lambda j: (j["posted"], j["title"]), reverse=True
        )
        out.append(f"### {heading} ({len(group)})")
        out.append("")
        if not group:
            out.append(f"_No {heading.lower()} in the {days}-day window._")
            out.append("")
            continue
        out.append(f"_{blurb}_")
        out.append("")
        out.append(f"<details><summary><strong>Show {len(group)} postings</strong></summary>")
        out.append("")
        out.append("| Posted | Role | Company | Location | Source / note |")
        out.append("|---|---|---|---|---|")
        for j in group:
            note = j["note"] or ""
            # a square bracket in the title ("[Hiring] ServiceNow Developer") closes the
            # markdown link early, so LINK_RE cannot parse the row back out and the
            # posting silently disappears from the board on the next read
            title = j["title"].replace("[", "(").replace("]", ")")
            out.append(
                f"| {j['posted']} | [{title}]({j['url']}) | {j['company']} | {j['location']} | {note} |"
            )
        out.append("")
        out.append("</details>")
        out.append("")
    out.append("## User / AI agent guide")
    out.append("")
    out.append("<details><summary><strong>If you are a person job-hunting</strong></summary>")
    out.append("")
    out.append(
        "Open the table that matches the platform you work on. Every row links straight to the\n"
        "posting, and `Posted` is the date the source published it — not a board's \"days ago\" label.\n"
        "Rows are newest first, so whatever sits at the top of a table is the freshest. Aggregator\n"
        "mirrors (Adzuna, LinkedIn, Talent.com) can lag or expire without notice: open the link\n"
        "before applying. If a row says `date relative — unverified`, treat the date as a hint only."
    )
    out.append("")
    out.append("</details>")
    out.append("")
    out.append("<details><summary><strong>If you are an AI agent adding jobs</strong></summary>")
    out.append("")
    out.append("1. **Never edit the three tables directly.** Concurrent agents will collide on them.")
    out.append("2. Drop a file in `inbox/` named `<model-slug>--<YYYY-MM-DD>--v<N>.md`.")
    out.append("3. One row per job, with an **absolute** `YYYY-MM-DD` date and a URL:")
    out.append("")
    out.append("```markdown")
    out.append("| Posted | Role | Company | Location | URL |")
    out.append("|---|---|---|---|---|")
    out.append("| 2026-11-02 | ServiceNow Developer | Acme Corp | Toronto, ON | https://example.com/job/1 |")
    out.append("```")
    out.append("")
    out.append("4. Same model, same day, more rows? Rename `v1` → `v2` and edit that file. Do not open a second one.")
    out.append(
        "5. Run `python3 tools/jobs_merge_inbox.py --dry-run`, then without the flag. A hand\n"
        "run never rewrites `inbox/`; add `--bump-inbox` if you want your file version-stamped."
    )
    out.append("6. Or open a PR that touches **only** your `inbox/` file.")
    out.append("")
    out.append("</details>")
    out.append("")
    out.append("<details><summary><strong>Rules the merger enforces</strong></summary>")
    out.append("")
    out.append("| Rule | Behaviour |")
    out.append("|---|---|")
    out.append("| Absolute date only | `2 days ago`, `New!` or a blank cell is rejected |")
    out.append("| URL required | rows without `http(s)://` are rejected |")
    out.append("| Duplicate URL | skipped, counted, never re-added (query strings and `utm_*` ignored) |")
    out.append(f"| Older than {days} days | moved to `README.BAK_*.md`, not into the tables |")
    out.append(f"| Table size | newest first; everything inside the 30-day window stays visible |")
    out.append(
        "| Listing page, not a posting | rejected — LinkedIn `/jobs/<keywords>-jobs`, Robert Half\n"
        "`/ca/en/jobs/<city>`, Wellfound `/role/`, and aggregator search/category URLs never enter\n"
        "the tables or `jobs.json` |"
    )
    out.append(
        "| Sales/marketing role | rejected by title, except platform and analytics work:\n"
        "Marketing Cloud, and growth/data analyst roles, are accepted |"
    )
    out.append("")
    out.append("</details>")
    out.append("")
    out.append("<details><summary><strong>Troubleshooting</strong></summary>")
    out.append("")
    out.append("- `inbox/ is empty` — your file does not match `<model>--<YYYY-MM-DD>--v<N>.md`.")
    out.append("- Row missing after a merge — it was a duplicate URL or it failed the date rule; the merge report says which.")
    out.append("- Scanner block reappeared — `scripts/daily_job_scan.mjs` must be run with `--no-readme` (the workflow already does).")
    out.append("")
    out.append("</details>")
    out.append("")
    out.append("## How to add jobs to this file")
    out.append("")
    out.append(
        "Do **not** hand-edit the three tables above. Drop a submission file in `inbox/` and run the\n"
        "merger, or open a PR that only touches `inbox/`. Full rules, file naming, dedupe and version\n"
        "bumping are in [`docs/JOB_SUBMISSION_METHODOLOGY.md`](docs/JOB_SUBMISSION_METHODOLOGY.md)."
    )
    out.append("")
    out.append("```bash")
    out.append("python3 tools/jobs_merge_inbox.py --dry-run   # preview")
    out.append("python3 tools/jobs_merge_inbox.py            # merge + archive expired rows")
    out.append("```")
    out.append("")
    out.append("Every row must carry an absolute `Posted` date and a URL that resolves. Relative ages\n"
               "(\"2 days ago\") are rejected — the merger refuses rows without a `YYYY-MM-DD` date.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=None, help="YYYY-MM-DD, defaults to today (UTC)")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--max-per-table", type=int, default=150, help="newest N rows kept per table")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--drop-scan-block", action="store_true", help="omit the scanner block entirely")
    ap.add_argument("--keep-scan-block", action="store_true", default=True)
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=args.days)

    text = README.read_text(encoding="utf-8")
    rows, unmatched = extract_rows(text)
    unique, dropped = dedupe(rows)
    current = [r for r in unique if cutoff.isoformat() <= r["posted"] <= today.isoformat()]
    archived = [r for r in unique if r["posted"] < cutoff.isoformat()]

    # keep each table readable: newest N per family, overflow stays in the backup
    kept: list[dict] = []
    overflow = 0
    for key in ("servicenow", "salesforce", "other"):
        group = sorted((r for r in current if r["family"] == key), key=lambda r: r["posted"], reverse=True)
        kept.extend(group[: args.max_per_table])
        overflow += max(0, len(group) - args.max_per_table)
    current = sorted(kept, key=lambda r: r["posted"], reverse=True)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    archive_name = f"README.BAK_{stamp}.md"

    counts = {k: sum(1 for r in current if r["family"] == k) for k in ("servicenow", "salesforce", "other")}
    print(f"parsed rows      : {len(rows)}")
    print(f"duplicates merged: {dropped}")
    print(f"rows in window   : {len(current)}  {counts}")
    print(f"rows archived    : {len(archived)} (+{overflow} beyond the per-table cap)")
    if unmatched:
        print(f"unparsed link rows kept out of tables: {len(unmatched)} (preserved in {archive_name})")

    if args.dry_run:
        for key in ("servicenow", "salesforce", "other"):
            newest = sorted((r for r in current if r["family"] == key), key=lambda r: r["posted"])[-3:]
            for r in newest:
                print(f"  [{key}] {r['posted']} {r['title'][:60]} — {r['company'][:30]}")
        return 0

    shutil.copyfile(README, ROOT / archive_name)
    new_readme = render(current, today, args.days, cutoff, archive_name)

    scan_block = extract_scan_block(text)
    if scan_block and args.keep_scan_block and not args.drop_scan_block:
        new_readme += (
            "## Automated feed (rewritten daily)\n\n"
            "Below is the raw output of `npm run scan:daily`. It may repeat rows from the tables above;\n"
            "the three tables are the curated view. The scanner only rewrites between these markers.\n\n"
            + scan_block
            + "\n"
        )
    new_readme += (
        f"\n## Archive\n\n`{archive_name}` holds the previous README in full — every older table, "
        "the peer-branch reconciliation notes, per-source method write-ups and anything removed from "
        "this file on "
        f"{today.isoformat()}.\n"
    )

    README.write_text(new_readme, encoding="utf-8")
    print(f"wrote {README.relative_to(ROOT)} ({len(new_readme.splitlines())} lines)")
    print(f"backup {archive_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

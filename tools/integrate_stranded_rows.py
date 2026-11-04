#!/usr/bin/env python3
"""Bring live job rows stranded on unmerged branches into the published feed.

Agents scan on their own branches (`publish-90-rounds-*`, `kilo-deep-scan-*`,
`restore-truncated-board-*`, ...). When those branches never merge, their rows
never reach the board: `jobs.json` on `main` is the only input the page reads.

This tool reads `<branch>:jobs.json` from the remote for every unmerged branch,
keeps only rows that would be legitimate on the board, collapses duplicates
across branches, and appends the survivors to the local `jobs.json`. Run
`scripts/sync_readme_to_jobs.mjs` and `tools/build_site.py` afterwards.

A row is kept when it:
  * has a URL, a title and a `postedDate` inside the board's window (45 days),
  * looks like an IT / platform role (the board's "Other" family),
  * is not a search/listing page ("339 Servicenow Jobs in Toronto"),
  * is not already in the feed, either as a row, as an `alternates` mirror, or
    under the same company + title + city key.

Usage:
  python3 tools/integrate_stranded_rows.py                    # report only
  python3 tools/integrate_stranded_rows.py --apply            # append to jobs.json
  python3 tools/integrate_stranded_rows.py --branches a,b --apply
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
JOBS = ROOT / "jobs.json"

# IT / platform roles, matching the remit of the board's "Other" family.
IN_REMIT = re.compile(
    r"service\s?now|salesforce|apex|visualforce|soql|workday|mulesoft|boomi|sap\b|oracle"
    r"|peoplesoft|itsm|itam|cmdb|asset management|invoice|data|cloud|devops|sre\b|sql"
    r"|python|java\b|javascript|typescript|\.net|architect|analyst|developer|engineer"
    r"|administrator|admin\b|consultant|integration|platform|crm\b|erp\b|security"
    r"|grc\b|qa\b|tester|test automation|support|service desk|infrastructure|network"
    r"|database|dba\b|business intelligence|power ?bi|tableau|splunk|dynatrace|dynamics"
    r"|atlassian|jira|servicenow|kafka|kubernetes|docker|aws|azure|gcp|machine learning"
    r"|data scientist|technolog|informatique|syst[eè]mes|analyste|d[ée]veloppeur",
    re.I,
)

# Roles outside the board's remit that the IT regex above still catches.
OUT_OF_REMIT = re.compile(
    r"tracks? engineering|civil|mechanical|structural|construction|\bbim\b|litigation"
    r"|payroll|nurse|clinical|driver|warehouse|receptionist|sales representative"
    r"|account executive|recruiter|talent acquisition|marketing coordinator",
    re.I,
)

# Bad extractions: the company cell holds a location, or the title is the
# aggregator's page title rather than the role.
BAD_COMPANY = re.compile(
    r"^(toronto|vancouver|montreal|ottawa|calgary|edmonton|remote|hybrid|on|qc)\b"
    r"|,\s*(on|qc|bc|ab|canada)\b|\bcanada\b",
    re.I,
)
BAD_TITLE = re.compile(r"job details|\|\s*jobs?$|^jobs?$|\bjob posting\b", re.I)

# Aggregator search-result pages, not postings.
LISTING_TITLE = re.compile(
    r"^\d[\d,]*\s.*\bjobs\b|\bjobs in\b|\bjobs\s*$|^jobs\b|job search|^careers?$"
    r"|^job openings$|^open positions$",
    re.I,
)
LISTING_URL = re.compile(r"/jobs/[a-z0-9-]*jobs-[a-z0-9-]*$|/jobs/search", re.I)


def clean_url(raw: str) -> str:
    """Strip tracking query strings and session ids so mirrors compare equal."""
    parts = urlsplit(raw)
    path = re.sub(r";jsessionid=[^/?#]*", "", parts.path)
    return urlunsplit((parts.scheme, parts.netloc.lower(), path, "", ""))


def city_of(location: str) -> str:
    first = re.split(r"[,·|]", location or "")[0]
    return first.strip().lower()


def key_of(row: dict) -> tuple[str, str, str]:
    return (
        (row.get("company") or "").strip().lower(),
        re.sub(r"\s+", " ", (row.get("title") or "").strip().lower()),
        city_of(row.get("location") or ""),
    )


def candidate_branches() -> list[str]:
    """Every branch that may hold rows: local heads plus origin's remote heads.

    Local-only branches matter here — agents scan on their own machine and often
    commit the results without pushing, so `refs/remotes/origin` alone misses
    them (`job-hunt-2026-11-03` held 17 in-remit postings nobody could see).
    """
    out = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes/origin"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    skip = {"origin", "origin/main", "origin/HEAD", "main", "master"}
    return [b for b in out if b.strip() not in skip]


def branch_rows(branch: str) -> list[dict]:
    r = subprocess.run(["git", "show", f"{branch}:jobs.json"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode:
        return []
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else data.get("jobs") or []


def parse_date(value: str) -> date | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except (TypeError, ValueError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="append survivors to jobs.json")
    ap.add_argument("--branches", help="comma-separated branches (default: every remote branch)")
    ap.add_argument("--max-age-days", type=int, default=45)
    ap.add_argument("--today", help="override today (YYYY-MM-DD), for reproducible runs")
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()
    cutoff = today - timedelta(days=args.max_age_days)

    payload = json.loads(JOBS.read_text())
    feed = payload["jobs"] if isinstance(payload, dict) else payload
    seen_urls: set[str] = set()
    seen_keys: set[str] = set()
    for row in feed:
        if row.get("url"):
            seen_urls.add(clean_url(row["url"]))
        seen_keys.add(key_of(row))
        for alt in row.get("alternates") or []:
            alt_url = alt if isinstance(alt, str) else alt.get("url")
            if alt_url:
                seen_urls.add(clean_url(alt_url))

    branches = args.branches.split(",") if args.branches else remote_branches()
    per_branch = Counter()
    candidates: dict[str, dict] = {}
    for branch in branches:
        for row in branch_rows(branch.strip()):
            url, title = row.get("url"), (row.get("title") or "").strip()
            posted = parse_date(row.get("postedDate"))
            if not url or not title or not posted:
                continue
            if posted < cutoff or posted > today + timedelta(days=1):
                continue
            if LISTING_TITLE.search(title) or LISTING_URL.search(urlsplit(url).path):
                continue
            if not IN_REMIT.search(title) or OUT_OF_REMIT.search(title):
                continue
            if BAD_TITLE.search(title) or BAD_COMPANY.search(row.get("company") or ""):
                continue
            curl = clean_url(url)
            if curl in seen_urls or key_of(row) in seen_keys:
                continue
            existing = candidates.get(curl)
            if existing and str(existing.get("postedDate")) >= str(row.get("postedDate")):
                continue
            row = dict(row, url=curl)
            row.setdefault("id", f"{row.get('source', 'branch')}:{curl}")
            candidates[curl] = row
            per_branch[branch.strip()] += 1

    added = list(candidates.values())
    print(f"branches scanned: {len(branches)}")
    for branch, n in per_branch.most_common():
        if n:
            print(f"  {n:>4}  {branch}")
    print(f"new rows: {len(added)}")
    src = Counter(r.get("source") for r in added)
    print(f"  by source: {dict(src)}")

    if not args.apply:
        print("(report only — pass --apply to append to jobs.json)")
        return 0
    if not added:
        print("nothing to add")
        return 0

    feed.extend(added)
    if isinstance(payload, dict):
        payload["jobs"] = feed
        payload.setdefault("meta", {})
        if isinstance(payload["meta"], dict):
            payload["meta"]["strandedBranchesImportedAt"] = datetime.now().astimezone().isoformat()
            payload["meta"]["strandedBranchesImportedRows"] = len(added)
    JOBS.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {JOBS.relative_to(ROOT)} → {len(feed)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())

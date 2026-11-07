#!/usr/bin/env python3
"""
autonomous_scan.py — Fully autonomous job discovery pipeline for gx10 device.

Runs headlessly (no Playwright, no browser, no Windows PC needed).
Discovers ServiceNow/Salesforce/IT jobs via Adzuna API, creates inbox/
submission files, merges into README.md, and pushes to GitHub.

Usage:
    python3 scripts/autonomous_scan.py              # full pipeline
    python3 scripts/autonomous_scan.py --dry-run     # preview only
    python3 scripts/autonomous_scan.py --search-only # just search, no merge

Env vars:
    ADZUNA_APP_ID        Adzuna app id (default: 54ce986e)
    ADZUNA_API_KEY       Adzuna API key (default: db851f299e966c0a2a72af525dce6199)
    GITHUB_REPO          GitHub repo URL (default: https://github.com/eltonaguiar/BESTIEJOB.git)
    GITHUB_BRANCH        Git branch (default: restore-truncated-board-2026-11-03)
    AUTONOMOUS_COMMIT    Set to "1" to auto-commit and push (default: 0)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
INBOX = ROOT / "inbox"

ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID", "54ce986e")
ADZUNA_API_KEY = os.environ.get("ADZUNA_API_KEY", "db851f299e966c0a2a72af525dce6199")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "https://github.com/eltonaguiar/BESTIEJOB.git")
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "restore-truncated-board-2026-11-03")
AUTO_COMMIT = os.environ.get("AUTONOMOUS_COMMIT", "0") == "1"

# Fresh keyword angles — rotated to find new postings not already indexed
SEARCH_QUERIES = [
    ("servicenow developer", "canada"),
    ("servicenow administrator", "canada"),
    ("servicenow architect", "canada"),
    ("servicenow technical consultant", "canada"),
    ("servicenow implementation consultant", "canada"),
    ("servicenow solution architect", "canada"),
    ("servicenow ITOM", "canada"),
    ("servicenow ITAM", "canada"),
    ("servicenow HRSD", "canada"),
    ("servicenow CSM", "canada"),
    ("salesforce developer", "canada"),
    ("salesforce administrator", "canada"),
    ("salesforce architect", "canada"),
    ("salesforce technical architect", "canada"),
    ("salesforce platform developer", "canada"),
    ("salesforce platform administrator", "canada"),
    ("salesforce marketing cloud", "canada"),
    ("salesforce commerce cloud", "canada"),
    ("salesforce financial services cloud", "canada"),
    ("salesforce health cloud", "canada"),
    ("salesforce consultant", "canada"),
    ("salesforce implementation consultant", "canada"),
    ("salesforce solution architect", "canada"),
    ("salesforce CPQ", "canada"),
    ("IT project manager", "canada"),
    ("business analyst", "canada"),
    ("data analyst", "canada"),
    ("IT director", "canada"),
    ("IT manager", "canada"),
    ("IT operations manager", "canada"),
]

# Job function exclusion — sales/marketing roles are out of scope
EXCL = re.compile(
    r"\b(account executive|account manager|sales representative|sales manager|"
    r"business development|recruiter|talent acquisition|pre-?sales|"
    r"customer success|product marketing|demand gen|content marketing|"
    r"email marketing|social media|brand manager|growth hacker|"
    r"marketing (?:manager|specialist|coordinator|director|associate|"
    r"intern|consultant|executive|ops|operations))\b",
    re.I,
)

# Classification
SN = re.compile(r"service\s?now|itsm|itam|cmdb|csdm|hrsd|servicenow", re.I)
SF = re.compile(r"salesforce|apex|soql|lwc|visualforce|marketing cloud|sfdc|agentforce|cpq|platform developer|platform administrator", re.I)


def classify(title: str, url: str) -> str:
    hay = f"{title} {url}".lower()
    if SN.search(hay):
        return "servicenow"
    if SF.search(hay):
        return "salesforce"
    return "other"


def norm_url(u: str) -> str:
    u = u.strip().rstrip("/")
    u = re.sub(r"^\w+://", "", u, flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    return u.lower()


def fetch_adzuna(what: str, where: str, page: int = 1, results_per_page: int = 50, max_days_old: int = 14) -> dict:
    url = (
        f"https://api.adzuna.com/v1/api/jobs/ca/search/{page}"
        f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_API_KEY}"
        f"&results_per_page={results_per_page}"
        f"&what={urllib.parse.quote(what)}"
        f"&where={urllib.parse.quote(where)}"
        f"&content-type=application/json"
        f"&max_days_old={max_days_old}"
        f"&sort_by=date"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def discover_jobs(dry_run: bool = False) -> list[dict]:
    """Run Adzuna searches across all keyword angles."""
    all_results: list[dict] = []
    seen_urls: set[str] = set()

    for what, where in SEARCH_QUERIES:
        try:
            payload = fetch_adzuna(what, where)
        except Exception as exc:
            print(f"  ADZUNA ERR {what} @ {where}: {exc}")
            continue

        results = payload.get("results", [])
        count = payload.get("count", 0)
        print(f"[adzuna] '{what}' @ {where} -> count={count} returned={len(results)}")

        for j in results:
            url = (j.get("redirect_url") or "").strip()
            if not url:
                continue
            key = norm_url(url)
            if key in seen_urls:
                continue
            seen_urls.add(key)

            title = (j.get("title") or "").strip()
            company = (j.get("company", {}).get("display_name") or "").strip()
            location = (j.get("location", {}).get("display_name") or "").strip()
            posted = (j.get("created") or "")[:10]

            if EXCL.search(title):
                continue

            family = classify(title, url)
            all_results.append({
                "posted": posted,
                "title": title.replace("|", "/").strip(),
                "company": company.replace("|", "/").strip(),
                "location": location.replace("|", "/").strip(),
                "url": url,
                "note": f"via adzuna autonomous · {what}",
                "family": family,
            })

        time.sleep(0.5)  # be polite to the API

    return all_results


def load_existing_urls() -> set[str]:
    """Load URLs already in README.md for dedupe."""
    if not README.exists():
        return set()
    text = README.read_text(encoding="utf-8", errors="replace")
    urls = set()
    for m in re.finditer(r"\((https?://[^\s)]+)\)", text):
        u = m.group(1).strip().rstrip("/")
        u = re.sub(r"^\w+://", "", u, flags=re.I)
        u = re.sub(r"^www\.", "", u, flags=re.I)
        urls.add(u.lower())
    return urls


def write_inbox(new_rows: list[dict]) -> Path:
    """Write an inbox/ submission file following the established pattern."""
    today = date.today().isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = INBOX / f"adzuna-autonomous--{today}--v1.md"

    # Find next version if file exists
    ver = 1
    while fname.exists():
        ver += 1
        fname = INBOX / f"adzuna-autonomous--{today}--v{ver}.md"

    lines = [
        "---",
        "model: adzuna-autonomous",
        f"scanned_at: {datetime.now(timezone.utc).isoformat()}Z",
        "task: adzuna-autonomous-scan",
        "---",
        "",
        "| Posted | Role | Company | Location | URL | Note |",
        "|---|---|---|---|---|---|",
    ]
    for r in new_rows:
        lines.append(
            f"| {r['posted']} | [{r['title']}]({r['url']}) | {r['company']} | "
            f"{r['location']} | {r['url']} | {r['note']} |"
        )
    lines.append("")
    fname.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {fname} with {len(new_rows)} rows")
    return fname


def run_merger(dry_run: bool = False) -> None:
    """Run jobs_merge_inbox.py to merge inbox/ into README.md."""
    cmd = ["python3", "tools/jobs_merge_inbox.py", "--bump-inbox"]
    if dry_run:
        cmd.append("--dry-run")
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"Merger failed with code {result.returncode}", file=sys.stderr)


def git_commit_push() -> None:
    """Commit and push changes to GitHub."""
    if not AUTO_COMMIT:
        print("AUTONOMOUS_COMMIT not set — skipping commit/push")
        return

    cmds = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", "Autonomous scan: adzuna job discovery (gx10)"],
        ["git", "push", "origin", GITHUB_BRANCH],
    ]
    for cmd in cmds:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode != 0:
            print(f"Git command failed: {' '.join(cmd)}", file=sys.stderr)
            break


def main() -> int:
    ap = argparse.ArgumentParser(description="Autonomous job discovery for gx10")
    ap.add_argument("--dry-run", action="store_true", help="preview only, no writes")
    ap.add_argument("--search-only", action="store_true", help="just search, no merge")
    args = ap.parse_args()

    print(f"=== Autonomous Job Discovery (gx10) ===")
    print(f"Root: {ROOT}")
    print(f"Dry run: {args.dry_run}")
    print(f"Auto-commit: {AUTO_COMMIT}")
    print()

    # Step 1: Discover jobs via Adzuna
    print("--- Step 1: Adzuna discovery ---")
    all_results = discover_jobs(dry_run=args.dry_run)
    print(f"Total raw results: {len(all_results)}")

    # Step 2: Dedupe against existing README
    existing_urls = load_existing_urls()
    today = date.today().isoformat()
    cutoff = (date.today() - timedelta(days=30)).isoformat()

    new_rows = []
    skipped = 0
    for r in all_results:
        key = norm_url(r["url"])
        if key in existing_urls:
            skipped += 1
            continue
        if r["posted"] < cutoff:
            skipped += 1
            continue
        new_rows.append(r)

    print(f"New unique jobs: {len(new_rows)}")
    print(f"Skipped (dup/old): {skipped}")
    sn = sum(1 for r in new_rows if r["family"] == "servicenow")
    sf = sum(1 for r in new_rows if r["family"] == "salesforce")
    ot = sum(1 for r in new_rows if r["family"] == "other")
    print(f"ServiceNow: {sn}, Salesforce: {sf}, Other: {ot}")

    if not new_rows:
        print("No new jobs to add — pipeline complete")
        return 0

    # Step 3: Write inbox/ submission
    if not args.dry_run:
        inbox_file = write_inbox(new_rows)
        print(f"Inbox file: {inbox_file}")

    # Step 4: Run merger
    if not args.search_only and not args.dry_run:
        print("\n--- Step 2: Merge into README ---")
        run_merger(dry_run=args.dry_run)

        # Step 5: Commit and push
        print("\n--- Step 3: Git commit/push ---")
        git_commit_push()
    elif args.search_only:
        print("\nSearch-only mode — skipping merge and git")

    print("\n=== Autonomous scan complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Convert job rows held on unmerged remote branches into inbox/ submissions.

Why: branches like zoo/2026-10-30, auto/2026-10-30 and kilo/2026-10-30 carry
hundreds of rows that never reached README.md. Rather than hand-merging them,
this turns each branch into a normal inbox file and lets the merger dedupe,
date-filter and archive them like any other agent submission.

    python3 tools/migrate_peer_branches.py --dry-run
    python3 tools/migrate_peer_branches.py
    python3 tools/jobs_merge_inbox.py

Each branch becomes inbox/<branch-slug>--<today>--v1.md. Rows without an
absolute YYYY-MM-DD date or without a URL are skipped and counted.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from jobs_consolidate import classify, dedupe, extract_rows  # noqa: E402

INBOX = ROOT / "inbox"


def sh(cmd: str) -> str:
    return subprocess.run(
        cmd, cwd=ROOT, shell=True, capture_output=True, text=True, check=True
    ).stdout


def slugify(branch: str) -> str:
    name = branch.replace("origin/", "")
    name = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return f"peer-{name}"


def md_files(branch: str) -> list[str]:
    try:
        listing = sh(f"git ls-tree -r --name-only {branch}")
    except subprocess.CalledProcessError:
        return []
    return [f for f in listing.splitlines() if re.search(r"\.md$", f, re.I)]


DATE_ANY = re.compile(r"\d{4}-\d{2}-\d{2}")
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BAD_TITLE = re.compile(
    r"^(apply( now| here)?|view|details?|read more|see more|learn more|click here|\d+|n/?a|-+)$",
    re.I,
)
BAD_URL = re.compile(r"(/jobsearch|/search\?|/jobs\?|\?q=|/land/ad/|/spl/$|/careers/$)", re.I)
BAD_TITLE_SUBSTR = re.compile(r"(search results?|job search|ziprecruiter search|indeed search|^search\b)", re.I)


def is_joblike(row: dict) -> bool:
    """Peer files mix real postings with index-page links; keep only the former."""
    title = (row.get("title") or "").strip()
    company = (row.get("company") or "").strip()
    if len(title) < 8 or BAD_TITLE.match(title) or BAD_TITLE_SUBSTR.search(title):
        return False
    if len(company) < 2 or BAD_TITLE.match(company):
        return False
    if BAD_URL.search(row.get("url") or ""):
        return False
    return True


def relaxed_rows(body: str) -> list[dict]:
    """Fallback for peer files that do not put the date in the first column."""
    rows: list[dict] = []
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        link = LINK.search(line)
        date = DATE_ANY.search(line)
        if not link or not date:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        title, url = link.group(1), link.group(2)
        rest = [
            c
            for c in cells
            if c and c != title and url not in c and not DATE_ANY.search(c) and not c.startswith("[")
        ]
        rows.append(
            {
                "posted": date.group(0),
                "title": title.replace("|", "/"),
                "url": url,
                "company": (rest[0] if rest else "").replace("|", "/"),
                "location": (rest[1] if len(rest) > 1 else "").replace("|", "/"),
                "note": "peer migration",
            }
        )
    return rows


def branch_rows(branch: str) -> list[dict]:
    rows: list[dict] = []
    for path in md_files(branch):
        try:
            body = sh(f"git show {branch}:{path}")
        except subprocess.CalledProcessError:
            continue
        parsed, _ = extract_rows(body)
        if not parsed:
            parsed = relaxed_rows(body)
        for row in parsed:
            if not is_joblike(row):
                continue
            row["origin"] = path
            row["family"] = row.get("family") or classify(row["title"], row["url"])
            rows.append(row)
    unique, _ = dedupe(rows)
    return unique


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--branch", action="append", help="limit to a branch (repeatable)")
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else datetime.now(timezone.utc).date()
    INBOX.mkdir(exist_ok=True)

    branches = args.branch or [
        b.strip()
        for b in sh("git branch -r --no-merged origin/main").splitlines()
        if b.strip() and "HEAD" not in b
    ]

    total_written = 0
    for branch in branches:
        rows = branch_rows(branch)
        if not rows:
            print(f"{branch}: 0 rows — skipped")
            continue
        rows.sort(key=lambda r: (r["posted"], r["title"]), reverse=True)
        name = f"{slugify(branch)}--{today.isoformat()}--v1.md"
        out = INBOX / name
        lines = [
            "---",
            f"source: {branch}",
            f"migrated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
            f"rows: {len(rows)}",
            "---",
            "",
            "| Posted | Role | Company | Location | URL |",
            "|---|---|---|---|---|",
        ]
        for r in rows:
            lines.append(
                f"| {r['posted']} | {r['title']} | {r['company']} | {r['location']} | {r['url']} |"
            )
        text = "\n".join(lines) + "\n"
        total_written += len(rows)
        print(f"{branch}: {len(rows)} rows -> inbox/{name}")
        if not args.dry_run:
            out.write_text(text, encoding="utf-8")

    print(f"\n{'would write' if args.dry_run else 'wrote'} {total_written} rows across "
          f"{len(branches)} branches")
    return 0


if __name__ == "__main__":
    sys.exit(main())

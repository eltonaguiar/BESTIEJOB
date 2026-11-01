#!/usr/bin/env python3
"""Guard against destructive edits to the bestiejob README job tables.

Motivated by two real incidents on this repo:

  * commit 8c25626 - titled "README: add ... rows", diffed +6/-508, and deleted
    210 posting rows plus five documentation sections.
  * an earlier peer commit that took the README from 583 lines to 85.

Both looked like ordinary edits and both removed postings nobody noticed for days.
This script compares a base and a head README and fails when posting rows disappear.

Rules
-----
1. Net loss: fail when (rows in base missing from head) - (rows in head not in base)
   exceeds --max-net-loss. Deleting a row *and* replacing it with the same posting
   under a different URL is not a loss, so the check is set-based rather than
   line-based.
2. Duplicate growth: fail when the number of repeated posting URLs grows by more
   than --max-dup-growth. The README already carries a known set of mirror
   duplicates, so only growth is treated as a regression.
3. Override: put [allow-readme-removals] in the commit message (or pass
   --allow-removals) when a deletion is genuinely intended.

Usage
-----
    python3 .github/scripts/readme_job_row_guard.py --base <sha> --head <sha>
    python3 .github/scripts/readme_job_row_guard.py --base origin/main~1
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

URL_RE = re.compile(r"https?://[^\s)\|<>\"']+", re.I)
JOB_RE = re.compile(r"servicenow|salesforce|sfdc|now platform", re.I)
SKIP_PATH = "README.md"


def git_show(rev: str, path: str = SKIP_PATH) -> str:
    proc = subprocess.run(
        ["git", "show", f"{rev}:{path}"], capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise SystemExit(f"cannot read {path} at {rev}: {proc.stderr.strip()}")
    return proc.stdout


def normalize(url: str) -> str:
    url = url.strip().lower()
    url = re.sub(r"^https?://(www\.)?", "", url)
    url = re.sub(r"[?#].*$", "", url)
    return url.rstrip("/.,;)")


def job_rows(text: str) -> tuple[dict[str, str], int, list[str]]:
    """Return (unique postings by URL, total row count, duplicated URLs)."""
    seen: dict[str, str] = {}
    dups: list[str] = []
    total = 0
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        if not JOB_RE.search(line):
            continue
        urls = URL_RE.findall(line)
        if not urls:
            continue
        total += 1
        key = normalize(urls[0])
        if key in seen:
            dups.append(key)
        else:
            seen[key] = line.strip()
    return seen, total, dups


def render(line: str, width: int = 150) -> str:
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    return plain[:width]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", required=True, help="base revision (pre-change)")
    ap.add_argument("--head", default="HEAD", help="head revision (default HEAD)")
    ap.add_argument("--max-net-loss", type=int, default=3)
    ap.add_argument("--max-dup-growth", type=int, default=5)
    ap.add_argument("--allow-removals", action="store_true")
    ap.add_argument("--list-removed", type=int, default=25)
    args = ap.parse_args()

    base_rows, base_total, base_dups = job_rows(git_show(args.base))
    head_rows, head_total, head_dups = job_rows(git_show(args.head))

    removed = [u for u in base_rows if u not in head_rows]
    added = [u for u in head_rows if u not in base_rows]
    net_loss = len(removed) - len(added)
    dup_growth = len(head_dups) - len(base_dups)

    print(f"base {args.base}: {base_total} rows / {len(base_rows)} unique postings")
    print(f"head {args.head}: {head_total} rows / {len(head_rows)} unique postings")
    print(f"removed: {len(removed)}   added: {len(added)}   net loss: {net_loss}")
    print(f"duplicate URLs: {len(base_dups)} -> {len(head_dups)} (growth {dup_growth})")

    failed = False

    if net_loss > args.max_net_loss and not args.allow_removals:
        failed = True
        print(
            f"\nFAIL: net loss of {net_loss} posting rows (limit {args.max_net_loss}).",
            file=sys.stderr,
        )
        print("Postings dropped:", file=sys.stderr)
        for url in removed[: args.list_removed]:
            print(f"  - {url}", file=sys.stderr)
            print(f"    {render(base_rows[url])}", file=sys.stderr)
        if len(removed) > args.list_removed:
            print(f"  ... and {len(removed) - args.list_removed} more", file=sys.stderr)
        print(
            "\nIf this deletion is intended, put [allow-readme-removals] in the commit "
            "message.",
            file=sys.stderr,
        )

    if dup_growth > args.max_dup_growth and not args.allow_removals:
        failed = True
        print(
            f"\nFAIL: duplicate posting URLs grew by {dup_growth} "
            f"(limit {args.max_dup_growth}).",
            file=sys.stderr,
        )
        for url in sorted(set(head_dups))[: args.list_removed]:
            print(f"  + {url}", file=sys.stderr)

    if not failed:
        print("\nPASS: no posting rows lost.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

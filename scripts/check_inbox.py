#!/usr/bin/env python3
"""Validate inbox/ job submissions before the merger rewrites README.md.

Why this exists: `tools/jobs_merge_inbox.py` accepts a row only when its first
cell is an absolute ``YYYY-MM-DD``. Anything else — a relative date ("2 days
ago"), an empty Posted cell, a badly split row — is dropped without a word, so
an agent could believe it submitted rows that never appeared anywhere. On
2026-11-02 the inbox held 80 submissions and nothing checked any of them.

Rules enforced here (violations exit 1):

  * filename is ``<model-slug>--<YYYY-MM-DD>--v<N>.md``
  * every table row has at least 5 cells: Posted | Role | Company | Location | URL
  * Posted is either a real calendar date or an explicit undated marker
    (``—``, ``-``, ``?``, ``n/a``, ``unknown``, ``tbd``, empty). Undated rows are
    legal — the merger skips them on purpose — but a *relative* date is an error
    because it silently means "no date".
  * a dated row carries an absolute http(s) URL somewhere in the row

Usage:
  python3 scripts/check_inbox.py
  python3 scripts/check_inbox.py --file inbox/grok-4--2026-11-02--v1.md
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"

NAME_RE = re.compile(r"^(?P<slug>[a-z0-9._-]+)--(?P<date>\d{4}-\d{2}-\d{2})--v(?P<ver>\d+)\.md$", re.I)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEPARATOR_RE = re.compile(r"^:?-{2,}:?$")
URL_RE = re.compile(r"https?://[^\s|)\]]+")
# Markers that mean "no posted date published". The merger skips these rows.
UNDATED_MARKERS = {"", "—", "–", "-", "?", "n/a", "na", "unknown", "tbd", "none"}

IGNORED_PREFIXES = ("_", "TEMPLATE", "README")


def cells_of(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def check_file(path: Path) -> tuple[list[str], dict[str, int]]:
    """Return (errors, stats). Stats are informational only."""
    errors: list[str] = []
    stats = {"dated": 0, "undated": 0, "rows": 0}

    m = NAME_RE.match(path.name)
    if not m:
        errors.append(f"{path.name}: filename must be <model-slug>--<YYYY-MM-DD>--v<N>.md")
    else:
        try:
            submit_date = date.fromisoformat(m.group("date"))
        except ValueError:
            submit_date = None
            errors.append(f"{path.name}: {m.group('date')} is not a real calendar date")

    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = cells_of(stripped)
        if not cells or all(SEPARATOR_RE.match(c) for c in cells if c):
            continue  # |---|---| separator
        if cells[0].lower() in {"posted", "date"}:
            continue  # header row

        stats["rows"] += 1
        where = f"{path.name}:{lineno}"

        if len(cells) < 5:
            errors.append(
                f"{where}: needs at least 5 cells (Posted | Role | Company | Location | URL), got {len(cells)}"
            )
            continue

        posted = cells[0]
        if DATE_RE.match(posted):
            try:
                date.fromisoformat(posted)
            except ValueError:
                errors.append(f"{where}: '{posted}' is not a real calendar date")
                continue
            if not URL_RE.search(stripped):
                errors.append(f"{where}: dated row has no absolute http(s) URL")
                continue
            stats["dated"] += 1
        elif posted.lower() in UNDATED_MARKERS:
            stats["undated"] += 1
        else:
            errors.append(
                f"{where}: Posted cell '{posted[:40]}' is neither YYYY-MM-DD nor an undated marker "
                f"({', '.join(sorted(m for m in UNDATED_MARKERS if m))}) — use the date the source shows, "
                "or an em dash if the page publishes none"
            )

    return errors, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", action="append", default=None, help="check only this file (repeatable)")
    args = ap.parse_args()

    if args.file:
        files = [Path(f) for f in args.file]
    else:
        if not INBOX.exists():
            print("no inbox/ directory — nothing to check")
            return 0
        files = sorted(
            p
            for p in INBOX.glob("*.md")
            if not p.name.startswith(IGNORED_PREFIXES)
        )

    if not files:
        print("inbox/ has no submissions — nothing to check")
        return 0

    all_errors: list[str] = []
    totals = {"files": len(files), "rows": 0, "dated": 0, "undated": 0}
    for path in files:
        errors, stats = check_file(path)
        all_errors.extend(errors)
        for k in ("rows", "dated", "undated"):
            totals[k] += stats[k]

    print(
        f"inbox: {totals['files']} files, {totals['rows']} rows "
        f"({totals['dated']} dated, {totals['undated']} undated)"
    )
    if all_errors:
        print(f"\n{len(all_errors)} violation(s):", file=sys.stderr)
        for err in all_errors[:40]:
            print(f"  x {err}", file=sys.stderr)
        if len(all_errors) > 40:
            print(f"  … {len(all_errors) - 40} more", file=sys.stderr)
        return 1

    print("OK: every submission is well-formed (undated rows are allowed and are skipped by the merger)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

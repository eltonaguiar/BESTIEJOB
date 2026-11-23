#!/usr/bin/env python3
"""Keep the README's "**N live postings**" claim equal to what the tables hold.

`scripts/board_invariants.py` reports `count-disagreement` when the header claim
and its own parsed row count differ. On 2026-11-18 the header claimed **7588**
while the tables held **7856** — the claim was last written by two one-off round
scripts (`apply_round8.py`, `fix_counts_r8.py`) and nothing has maintained it
since, so it drifts every time rows age out, are purged, or a sweep adds more.

This recomputes the claim with board_invariants' *own* parser and rewrites it, so
the gate and the header cannot disagree by construction.

Usage:  python3 scripts/sync_readme_counts.py [--check]
        --check exits 1 if the header is stale (CI-friendly, writes nothing)
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from board_invariants import COUNT_RE, parse_readme  # noqa: E402

README = ROOT / "README.md"


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    rows, claimed = parse_readme(README)
    actual = len(rows)
    if claimed == actual:
        print(f"header already correct: {actual} live postings")
        return 0
    if check_only:
        print(
            f"header is stale: claims {claimed}, tables hold {actual} "
            f"(run scripts/sync_readme_counts.py)",
            file=sys.stderr,
        )
        return 1
    text = README.read_text(encoding="utf-8")
    new_text = COUNT_RE.sub(f"**{actual} live postings**", text, count=1)
    if new_text == text:
        # The README's auto-scan block no longer carries a standalone
        # "**N live postings**" claim (it now reads "**Scan: ... · N live
        # postings from ...**"), so there is nothing for this script to
        # rewrite. Return 0 so normalize_board.py and hourly-scan.yml do not
        # fail on a header that is absent by design; board_invariants treats a
        # missing claim as no claim.
        print("header count line not found — nothing rewritten", file=sys.stderr)
        return 0
    README.write_text(new_text, encoding="utf-8")
    print(f"header count {claimed} -> {actual} live postings")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

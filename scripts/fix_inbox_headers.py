#!/usr/bin/env python3
"""Fix header rows that were accidentally converted in the focused inbox files."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"

files = [
    "focused-sn-all--20261104T005721Z.md",
    "focused-sf-all--20261104T005721Z.md",
    "focused-other-all--20261104T005721Z.md",
    "focused-older-good--20261104T005721Z.md",
]

for name in files:
    f = INBOX / name
    if not f.exists():
        print(f"Skip {name}: not found")
        continue
    lines = f.read_text(encoding="utf-8").splitlines()
    fixed = []
    for line in lines:
        # Fix header row that was accidentally given a date
        if "| 2026-11-04 | Role | Company | Location | Score/10 via Source |" in line:
            fixed.append("| Posted | Role | Company | Location | Source |")
        else:
            fixed.append(line)
    f.write_text("\n".join(fixed) + "\n", encoding="utf-8")
    print(f"Fixed {name}")

print("Done.")

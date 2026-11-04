#!/usr/bin/env python3
"""
Convert finalize_rounds.py output inbox files to merger format:
| Score | Round | Role | Company | Location | Source |
-> | Posted | Role | Company | Location | Source |
Also rename to match <model>--<YYYY-MM-DD>--v<N>.md convention.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"

# Files created by finalize_rounds.py
files = [
    "focused-sn-all--20261104T063418Z.md",
    "focused-sf-all--20261104T063418Z.md",
    "focused-other-all--20261104T063418Z.md",
    "focused-older-good--20261104T063418Z.md",
]

new_names = {
    "focused-sn-all--20261104T063418Z.md": "focused-sn-all--2026-11-04--v3.md",
    "focused-sf-all--20261104T063418Z.md": "focused-sf-all--2026-11-04--v3.md",
    "focused-other-all--20261104T063418Z.md": "focused-other-all--2026-11-04--v3.md",
    "focused-older-good--20261104T063418Z.md": "focused-older-good--2026-11-04--v3.md",
}

for old_name, new_name in new_names.items():
    f = INBOX / old_name
    if not f.exists():
        print(f"Skip {old_name}: not found")
        continue
    lines = f.read_text(encoding="utf-8").splitlines()
    out = []
    converted = 0
    for line in lines:
        if not line.strip().startswith("|"):
            out.append(line)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            out.append(line)
            continue
        # Skip separator row
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            out.append(line)
            continue
        # Skip header row
        if cells[0].lower() in ("score", "posted"):
            out.append(line)
            continue
        # Old format: | Score | Round | [title](url) | Company | Location | Source |
        score = cells[0]
        rnd = cells[1]
        role_cell = cells[2] if len(cells) > 2 else ""
        company = cells[3] if len(cells) > 3 else ""
        location = cells[4] if len(cells) > 4 else ""
        source = cells[5] if len(cells) > 5 else ""

        # Extract posted date from source filename
        m = re.search(r"(\d{4}-\d{2}-\d{2})", source)
        posted = m.group(1) if m else "2026-11-04"

        # Ensure role cell is a markdown link
        link_m = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", role_cell)
        if not link_m and role_cell:
            # Bare title, no link
            pass

        new_line = f"| {posted} | {role_cell} | {company} | {location} | {score}/10 via {source} |"
        out.append(new_line)
        converted += 1

    # Fix header row
    fixed = []
    for line in out:
        if "| Posted | Role | Company | Location | Score/10 via Source |" in line:
            fixed.append("| Posted | Role | Company | Location | Source |")
        else:
            fixed.append(line)

    # Write to new name
    new_f = INBOX / new_name
    new_f.write_text("\n".join(fixed) + "\n", encoding="utf-8")
    print(f"Converted {old_name} -> {new_name}: {converted} rows")

    # Delete old file
    f.unlink()
    print(f"Deleted {old_name}")

print("Done.")

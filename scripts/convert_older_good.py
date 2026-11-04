#!/usr/bin/env python3
"""Convert the older-good inbox file to merger format."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
f = INBOX / "focused-older-good--20261104T005721Z.md"

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
    # Old format: | Score | Platform | [title](url) | Company | Location |
    score = cells[0]
    platform = cells[1]
    role_cell = cells[2] if len(cells) > 2 else ""
    company = cells[3] if len(cells) > 3 else ""
    location = cells[4] if len(cells) > 4 else ""

    link_m = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", role_cell)
    if link_m:
        title, url = link_m.group(1), link_m.group(2)
        role_cell = f"[{title}]({url})"

    new_line = f"| 2026-11-04 | {role_cell} | {company} | {location} | {score}/10 ({platform}) via older-good |"
    out.append(new_line)
    converted += 1

f.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Converted focused-older-good: {converted} rows")

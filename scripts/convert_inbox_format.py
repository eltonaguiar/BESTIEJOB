#!/usr/bin/env python3
"""
Convert focused-*.md inbox files to the format jobs_merge_inbox.py expects:
| Posted | Role(url) | Company | Location | Source/note |
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"

# Match our focused inbox files
files = sorted(INBOX.glob("focused-*-all--*.md")) + sorted(INBOX.glob("focused-older-good--*.md"))
if not files:
    print("No focused inbox files found.")
    sys.exit(0)

for f in files:
    lines = f.read_text(encoding="utf-8").splitlines()
    out = []
    converted = 0
    for line in lines:
        if not line.strip().startswith("|"):
            out.append(line)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            out.append(line)
            continue
        # Skip separator row
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            out.append(line)
            continue
        # Old format: | Score | Round | [title](url) | Company | Location | Source |
        score = cells[0] if len(cells) > 0 else ""
        rnd = cells[1] if len(cells) > 1 else ""
        role_cell = cells[2] if len(cells) > 2 else ""
        company = cells[3] if len(cells) > 3 else ""
        location = cells[4] if len(cells) > 4 else ""
        source = cells[5] if len(cells) > 5 else ""
        # Extract posted date from source filename like 2026-11-04_sn_round1_raw_....json
        m = re.search(r"(\d{4}-\d{2}-\d{2})", source)
        posted = m.group(1) if m else "2026-11-04"
        # Role cell should be [title](url)
        link_m = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", role_cell)
        if link_m:
            title, url = link_m.group(1), link_m.group(2)
            role_cell = f"[{title}]({url})"
        new_line = f"| {posted} | {role_cell} | {company} | {location} | {score}/10 via {source} |"
        out.append(new_line)
        converted += 1

    f.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Converted {f.name}: {converted} rows")

print("Done.")

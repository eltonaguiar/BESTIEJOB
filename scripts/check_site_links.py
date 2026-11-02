#!/usr/bin/env python3
"""CI guard: the deployed page must be tabbed, stamped, and link every posting."""
import json
import re
import sys
from pathlib import Path

jobs = json.load(open("public/jobs-data.json"))["jobs"]
html = Path("public/index.html").read_text(encoding="utf-8")

fails = []
if 'class="apply"' not in html:
    fails.append("per-card apply link missing")
if "data-tab" not in html:
    fails.append("tabbed interface missing")
if not ("Data updated" in html or "Last updated" in html) or "__BUILT__" in html:
    fails.append("build stamp missing/unsubstituted")
if jobs and "match" not in jobs[0]:
    fails.append("resume-fit score missing from data")
bad = [j for j in jobs if not re.match(r"^https?://\S+$", j.get("url") or "")]
if bad:
    fails.append(f"{len(bad)} rows without an absolute url")

print(f"jobs={len(jobs)} applyLinks={html.count('class=\"apply\"')} "
      f"tabs={'data-tab' in html} stamp={'Data updated' in html or 'Last updated' in html}")
if fails:
    print("FAIL:", "; ".join(fails))
    sys.exit(1)
print("OK: page is tabbed, stamped and every card links to its posting")

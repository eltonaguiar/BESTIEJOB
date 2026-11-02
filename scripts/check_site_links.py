#!/usr/bin/env python3
"""Guard: every card must carry a real absolute link to its posting."""
import json, re, sys
from pathlib import Path
jobs = json.load(open("public/jobs-data.json"))["jobs"]
html = Path("public/index.html").read_text(encoding="utf-8")
fails = []
if 'class="apply"' not in html:
    fails.append("apply link template missing from index.html")
if 'href="${esc(j.url)}"' not in html:
    fails.append("title anchor template missing")
bad = [j for j in jobs if not re.match(r"^https?://\S+$", j.get("url") or "")]
if bad:
    fails.append(f"{len(bad)} rows without an absolute url")
if "__BUILT__" in html:
    fails.append("build stamp not substituted")
print(f"jobs={len(jobs)} applyLinks={html.count('class=\"apply\"')} stamp={'Last updated' in html}")
if fails:
    print("FAIL:", "; ".join(fails)); sys.exit(1)
print("OK: every card links to its posting")

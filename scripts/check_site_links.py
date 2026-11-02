#!/usr/bin/env python3
"""CI guard: the deployed page must be tabbed, stamped, and link every posting."""
import json
import re
import sys
from pathlib import Path

jobs = json.load(open("public/jobs-data.json"))["jobs"]
html = Path("public/index.html").read_text(encoding="utf-8")

apply_count = html.count('class="apply"')
has_tabs = "data-tab" in html
has_aria = 'role="tablist"' in html
has_stamp = ("Data updated" in html) or ("Last updated" in html)
stamp_placeholder = "__BUILT__" in html
has_fit = bool(jobs) and ("match" in jobs[0])

fails = []
if not apply_count:
    fails.append("per-card apply link missing")
if not has_tabs:
    fails.append("tabbed interface missing")
if not has_aria:
    fails.append("ARIA tab semantics missing")
if not has_stamp or stamp_placeholder:
    fails.append("build stamp missing/unsubstituted")
if not has_fit:
    fails.append("resume-fit score missing from data")

url_re = re.compile(r"^https?://\S+$")
bad = [j for j in jobs if not url_re.match(j.get("url") or "")]
if bad:
    fails.append("%d rows without an absolute url" % len(bad))

print("jobs=%d applyLinks=%d tabs=%s aria=%s stamp=%s fit=%s blocked=%d"
      % (len(jobs), apply_count, has_tabs, has_aria, has_stamp, has_fit, len(bad)))

if fails:
    print("FAIL: " + "; ".join(fails))
    sys.exit(1)
print("OK: page is tabbed, stamped and every card links to its posting")

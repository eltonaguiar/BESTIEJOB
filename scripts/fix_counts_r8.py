#!/usr/bin/env python3
"""Fix README count locations (Round 8). Uses explicit flags= to avoid the
re.sub positional-arg trap where re.M lands in `count` instead of `flags`."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

text = README.read_text(encoding="utf-8")


def count_section(name, nxt):
    a = re.search(rf"^### {name} jobs \(\d+\)$", text, re.M | re.S).end()
    b = (re.search(rf"^### {nxt} jobs \(\d+\)$", text, re.M | re.S).start()
         if nxt else re.search(r"^## User / AI agent guide$", text, re.M | re.S).start())
    return sum(1 for l in text[a:b].split("\n")
               if l.startswith("| 20") and l.count("|") >= 5)


n_snow = count_section("ServiceNow", "Salesforce")
n_sf = count_section("Salesforce", "Other")
n_other = count_section("Other", None)
total = n_snow + n_sf + n_other
print(f"actual: ServiceNow={n_snow} Salesforce={n_sf} Other={n_other} total={total}")

# section headers
text = re.sub(r"^### ServiceNow jobs \(\d+\)$",
              f"### ServiceNow jobs ({n_snow})", text, flags=re.M)
text = re.sub(r"^### Salesforce jobs \(\d+\)$",
              f"### Salesforce jobs ({n_sf})", text, flags=re.M)
text = re.sub(r"^### Other jobs \(\d+\)$",
              f"### Other jobs ({n_other})", text, flags=re.M)

# TOC entries (label + anchor fragment must both change)
text = re.sub(r"^(\s*- )\[ServiceNow jobs \(\d+\)\]\(#servicenow-jobs-\d+\)$",
              rf"\g<1>[ServiceNow jobs ({n_snow})](#servicenow-jobs-{n_snow})",
              text, flags=re.M)
text = re.sub(r"^(\s*- )\[Salesforce jobs \(\d+\)\]\(#salesforce-jobs-\d+\)$",
              rf"\g<1>[Salesforce jobs ({n_sf})](#salesforce-jobs-{n_sf})",
              text, flags=re.M)
text = re.sub(r"^(\s*- )\[Other jobs \(\d+\)\]\(#other-jobs-\d+\)$",
              rf"\g<1>[Other jobs ({n_other})](#other-jobs-{n_other})",
              text, flags=re.M)

# headline
text = re.sub(r"\*\*\d+ live postings\*\*", f"**{total} live postings**", text)

# per-section "Show N postings" — do it by positional slicing per section
for name, n in (("ServiceNow", n_snow), ("Salesforce", n_sf), ("Other", n_other)):
    a = re.search(rf"^### {name} jobs \(\d+\)$", text, re.M | re.S).end()
    nxt = {"ServiceNow": "Salesforce", "Salesforce": "Other"}.get(name)
    b = (re.search(rf"^### {nxt} jobs \(\d+\)$", text, re.M | re.S).start()
         if nxt else re.search(r"^## User / AI agent guide$", text, re.M | re.S).start())
    seg = re.sub(r"<summary><strong>Show \d+ postings</strong></summary>",
                 f"<summary><strong>Show {n} postings</strong></summary>", seg_dummy := text[a:b])
    text = text[:a] + seg + text[b:]

README.write_text(text, encoding="utf-8")

# --- verify
t = README.read_text(encoding="utf-8")
hdrs = [int(x) for x in re.findall(r"^### \w+ jobs \((\d+)\)$", t, flags=re.M)]
toc = [(m[0], int(m[1])) for m in re.findall(
    r"^  - \[(\w+) jobs \((\d+)\)\]\(#[\w-]+\)$", t, flags=re.M)]
show = [int(x) for x in re.findall(r"<summary><strong>Show (\d+) postings", t)]
head = int(re.search(r"\*\*(\d+) live postings\*\*", t).group(1))
ok = (sum(hdrs) == head == total
      and [n for _, n in toc] == hdrs
      and show == hdrs)
print(f"headers={hdrs} sum={sum(hdrs)}")
print(f"toc    ={toc}")
print(f"show   ={show}")
print(f"headline={head}")
print(f"CONSISTENT: {ok}")
sys.exit(0 if ok else 1)

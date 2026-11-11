import json, re, sys
REMOVE = sys.argv[1] if len(sys.argv) > 1 else ""
ROWS = sys.argv[2] if len(sys.argv) > 2 else ""
SN = re.compile(r"service\s*now|servicenow|\bitsm\b|\bitam\b|\bitom\b|\bcmdb\b", re.I)
SF = re.compile(r"salesforce|\bapex\b|\bmulesoft\b|\bagentforce\b|\bcpq\b|omnistudio|vlocity|ncino|\blwc\b", re.I)
def section_for(t):
    return "ServiceNow" if SN.search(t) else ("Salesforce" if SF.search(t) else "Other")
def sections(lines):
    return [(i, m.group(1), int(m.group(2))) for i, l in enumerate(lines)
            if (m := re.match(r"### (\w+) jobs \((\d+)\)", l))]
def bump(lines, start, delta):
    lines[start] = re.sub(r"(### \w+ jobs \()(\d+)(\))",
                          lambda m: f"{m.group(1)}{int(m.group(2))+delta}{m.group(3)}", lines[start], 1)
    for j in range(start, min(start + 12, len(lines))):
        if re.search(r"<details><summary><strong>Show \d+ postings", lines[j]):
            lines[j] = re.sub(r"(Show )(\d+)( postings)",
                              lambda m: f"{m.group(1)}{int(m.group(2))+delta}{m.group(3)}", lines[j], 1)
            break

lines = open("README.md").read().splitlines(True)
removed = 0
if REMOVE:
    drop = json.load(open(REMOVE))
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("| 20") and any(u in lines[i] for u in drop):
            sec = max([s for s, _, _ in sections(lines) if s < i], default=None)
            del lines[i]; removed += 1
            if sec is not None: bump(lines, sec, -1)
    print("removed weak rows:", removed)

added = 0
if ROWS:
    rows = json.load(open(ROWS))
    for r in sorted(rows, key=lambda x: x["date"], reverse=True):
        secs = sections(lines)
        sec = section_for(r["title"])
        start = next(i for i, n, _ in secs if n == sec)
        end = min([i for i, _, _ in secs if i > start] + [len(lines)])
        idx = [i for i in range(start, end) if lines[i].startswith("| 20")]
        if not idx: continue
        pos = next((i for i in idx if lines[i][2:12] < r["date"]), idx[-1] + 1)
        esc = lambda s: re.sub(r"\s+", " ", (s or "").replace("|", "/")).strip()
        lines.insert(pos, f"| {r['date']} | [{esc(r['title'])}]({r['url']}) | {esc(r['company'])} "
                          f"| {esc(r['loc'])} | via {r['channel']} |\n")
        bump(lines, start, +1); added += 1
    print("inserted rows:", added)
open("README.md", "w").writelines(lines)

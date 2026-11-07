#!/usr/bin/env python3
"""Regenerate FRESH_JOBS.md from jobs.json"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
JOBS_JSON = ROOT / "jobs.json"
FRESH_JOBS = ROOT / "FRESH_JOBS.md"

SN = re.compile(r'service\s?now|itsm|itam|cmdb|csdm|hrsd|servicenow', re.I)
SF = re.compile(r'salesforce|apex|soql|lwc|visualforce|marketing cloud|sfdc|agentforce|cpq|platform developer|platform administrator|financial services cloud|health cloud|experience cloud|data cloud', re.I)

def classify(title, url):
    hay = f"{title} {url}".lower()
    if SN.search(hay): return 'servicenow'
    if SF.search(hay): return 'salesforce'
    return 'other'

def main():
    d = json.load(open(JOBS_JSON))
    jobs = d.get("jobs", [])

    sn = [j for j in jobs if classify(j.get('title',''), j.get('url','')) == 'servicenow']
    sf = [j for j in jobs if classify(j.get('title',''), j.get('url','')) == 'salesforce']
    other = [j for j in jobs if classify(j.get('title',''), j.get('url','')) == 'other']

    for group in [sn, sf, other]:
        group.sort(key=lambda j: j.get('posted',''), reverse=True)

    lines = []
    lines.append("# Fresh job scan")
    lines.append("")
    lines.append(f"Auto-generated from jobs.json on {datetime.now(timezone.utc).isoformat()}. Total {len(jobs)} jobs.")
    lines.append("")
    lines.append("| Posted | Role | Company | Location | Type | Source |")
    lines.append(f"|---|---|---|---|---|---|")

    for j in sn + sf + other:
        title = j.get('title','')
        company = j.get('company','')
        location = j.get('location','')
        posted = j.get('posted','')
        employment_type = j.get('employmentType','')
        source = j.get('source','')
        url = j.get('url','')
        lines.append(f"| {posted} | [{title}]({url}) | {company} | {location} | {employment_type} | {source} |")

    lines.append("")
    FRESH_JOBS.write_text("\n".join(lines))
    print(f"FRESH_JOBS.md regenerated: {len(sn)} SN, {len(sf)} SF, {len(other)} Other, {len(jobs)} total")

if __name__ == "__main__":
    main()

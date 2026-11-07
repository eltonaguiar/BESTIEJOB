import json, re
from pathlib import Path
from datetime import date, timedelta, datetime, timezone

README = Path('README.md')
text = README.read_text(encoding='utf-8', errors='replace')
existing_urls = set()
for m in re.finditer(r'\((https?://[^\s)]+)\)', text):
    u = m.group(1).strip().rstrip('/')
    u = re.sub(r'^\w+://', '', u, flags=re.I)
    u = re.sub(r'^www\.', '', u, flags=re.I)
    existing_urls.add(u.lower())

print(f'Existing URLs in README: {len(existing_urls)}')

SN = re.compile(r'service\s?now|itsm|itam|cmdb|csdm|hrsd|servicenow', re.I)
SF = re.compile(r'salesforce|apex|soql|lwc|visualforce|marketing cloud|sfdc|agentforce|cpq|platform developer|platform administrator', re.I)
EXCL = re.compile(r'\b(account executive|account manager|sales representative|sales manager|business development|recruiter|talent acquisition|pre-?sales|customer success|product marketing)\b', re.I)

def classify(title, url):
    hay = f'{title} {url}'.lower()
    if SN.search(hay):
        return 'servicenow'
    if SF.search(hay):
        return 'salesforce'
    return 'other'

def norm_url(u):
    u = u.strip().rstrip('/')
    u = re.sub(r'^\w+://', '', u, flags=re.I)
    u = re.sub(r'^www\.', '', u, flags=re.I)
    return u.lower()

today = date.today().isoformat()
cutoff = (date.today() - timedelta(days=30)).isoformat()

all_new = []
sn_count = sf_count = ot_count = 0

# Process agent_new_jobs.json
with open('/tmp/agent_new_jobs.json') as f:
    data = json.load(f)
print(f'agent_new_jobs.json: {len(data)} items')
for j in data:
    u = norm_url(j.get('url', ''))
    if not u or u in existing_urls:
        continue
    title = (j.get('title') or '').strip()
    if EXCL.search(title):
        continue
    posted = (j.get('postedDate') or '')[:10]
    if posted < cutoff:
        continue
    company = (j.get('company') or '').strip()
    location = (j.get('location') or '').strip()
    family = classify(title, j.get('url', ''))
    if family == 'servicenow':
        sn_count += 1
    elif family == 'salesforce':
        sf_count += 1
    else:
        ot_count += 1
    all_new.append({
        'posted': posted,
        'title': title.replace('|', '/').strip(),
        'company': company.replace('|', '/').strip(),
        'location': location.replace('|', '/').strip(),
        'url': j.get('url', ''),
        'note': 'via cached agent_new_jobs.json',
        'family': family,
    })

# Process agent_real_verified.json
with open('/tmp/agent_real_verified.json') as f:
    data = json.load(f)
print(f'agent_real_verified.json: {len(data)} items')
for j in data:
    u = norm_url(j.get('url', ''))
    if not u or u in existing_urls:
        continue
    title = (j.get('title') or '').strip()
    if EXCL.search(title):
        continue
    posted = (j.get('posted') or '')[:10]
    if posted < cutoff:
        continue
    company = (j.get('company') or '').strip()
    location = (j.get('location') or '').strip()
    family = classify(title, j.get('url', ''))
    if family == 'servicenow':
        sn_count += 1
    elif family == 'salesforce':
        sf_count += 1
    else:
        ot_count += 1
    all_new.append({
        'posted': posted,
        'title': title.replace('|', '/').strip(),
        'company': company.replace('|', '/').strip(),
        'location': location.replace('|', '/').strip(),
        'url': j.get('url', ''),
        'note': 'via cached agent_real_verified.json',
        'family': family,
    })

# Process adzuna_servicenow.json
with open('/tmp/adzuna_servicenow.json') as f:
    data = json.load(f)
print(f'adzuna_servicenow.json: {len(data.get("results", []))} results')
for j in data.get('results', []):
    u = norm_url(j.get('redirect_url', ''))
    if not u or u in existing_urls:
        continue
    title = (j.get('title') or '').strip()
    if EXCL.search(title):
        continue
    posted = (j.get('created') or '')[:10]
    if posted < cutoff:
        continue
    company = (j.get('company', {}).get('display_name') or '').strip()
    location = (j.get('location', {}).get('display_name') or '').strip()
    family = classify(title, j.get('redirect_url', ''))
    if family == 'servicenow':
        sn_count += 1
    elif family == 'salesforce':
        sf_count += 1
    else:
        ot_count += 1
    all_new.append({
        'posted': posted,
        'title': title.replace('|', '/').strip(),
        'company': company.replace('|', '/').strip(),
        'location': location.replace('|', '/').strip(),
        'url': j.get('redirect_url', ''),
        'note': 'via cached adzuna_servicenow.json',
        'family': family,
    })

# Process adzuna_salesforce.json
with open('/tmp/adzuna_salesforce.json') as f:
    data = json.load(f)
print(f'adzuna_salesforce.json: {len(data.get("results", []))} results')
for j in data.get('results', []):
    u = norm_url(j.get('redirect_url', ''))
    if not u or u in existing_urls:
        continue
    title = (j.get('title') or '').strip()
    if EXCL.search(title):
        continue
    posted = (j.get('created') or '')[:10]
    if posted < cutoff:
        continue
    company = (j.get('company', {}).get('display_name') or '').strip()
    location = (j.get('location', {}).get('display_name') or '').strip()
    family = classify(title, j.get('redirect_url', ''))
    if family == 'servicenow':
        sn_count += 1
    elif family == 'salesforce':
        sf_count += 1
    else:
        ot_count += 1
    all_new.append({
        'posted': posted,
        'title': title.replace('|', '/').strip(),
        'company': company.replace('|', '/').strip(),
        'location': location.replace('|', '/').strip(),
        'url': j.get('redirect_url', ''),
        'note': 'via cached adzuna_salesforce.json',
        'family': family,
    })

# Deduplicate within all_new
seen = set()
unique_new = []
for r in all_new:
    k = norm_url(r['url'])
    if k in seen:
        continue
    seen.add(k)
    unique_new.append(r)

print(f'\nTotal new jobs: {len(unique_new)} (SN={sn_count}, SF={sf_count}, Other={ot_count})')

# Write inbox file
fname = Path(f'inbox/round11-cached--{date.today().isoformat()}--v1.md')
lines = [
    '---',
    'model: adzuna-round10-cached',
    f'scanned_at: {datetime.now(timezone.utc).isoformat()}Z',
    'task: adzuna-round10-cached-service-now-salesforce',
    '---',
    '',
    '| Posted | Role | Company | Location | URL | Note |',
    '|---|---|---|---|---|---|',
]
for r in unique_new:
    lines.append(f'| {r["posted"]} | [{r["title"]}]({r["url"]}) | {r["company"]} | {r["location"]} | {r["url"]} | {r["note"]} |')
lines.append('')
fname.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {fname} with {len(unique_new)} rows')

# Save for merge
with open('/tmp/round11_jobs.json', 'w') as f:
    json.dump(unique_new, f, indent=1)
print('Saved to /tmp/round11_jobs.json')

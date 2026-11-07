#!/usr/bin/env python3
"""
Creative job hunt scans using Tavily and Firecrawl search APIs.
Adzuna is rate-limited (HTTP 429), so we use alternative search APIs.
"""
import urllib.request
import urllib.parse
import json
import sys
import time
import re
from pathlib import Path
from datetime import date, timedelta, datetime, timezone

sys.path.insert(0, 'tools')
from ai_panel import get_key

TAVILY_KEY = get_key('TAVILY_API_KEY')
FIRECRAWL_KEY = get_key('FIRECRAWL_API_KEY')
EXA_KEY = get_key('EXA_API_KEY')

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / 'inbox'

SN = re.compile(r'service\s?now|itsm|itam|cmdb|csdm|hrsd|servicenow', re.I)
SF = re.compile(r'salesforce|apex|soql|lwc|visualforce|marketing cloud|sfdc|agentforce|cpq|platform developer|platform administrator', re.I)
EXCL = re.compile(r'\b(account executive|account manager|sales representative|sales manager|business development|recruiter|talent acquisition|pre-?sales|customer success|product marketing)\b', re.I)

def classify(title, url):
    hay = f'{title} {url}'.lower()
    if SN.search(hay): return 'servicenow'
    if SF.search(hay): return 'salesforce'
    return 'other'

def norm_url(u):
    u = u.strip().rstrip('/')
    u = re.sub(r'^\w+://', '', u, flags=re.I)
    u = re.sub(r'^www\.', '', u, flags=re.I)
    return u.lower()

def tavily_search(query, max_results=10):
    url = "https://api.tavily.com/search"
    data = {
        "api_key": TAVILY_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": "advanced",
        "include_answer": False
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  Tavily error for '{query}': {e}")
        return None

def firecrawl_search(query, limit=10):
    url = "https://api.firecrawl.dev/v2/search"
    data = {
        "query": query,
        "limit": limit,
        "scrapeOptions": {"formats": ["markdown"]}
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {FIRECRAWL_KEY}'
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  Firecrawl error for '{query}': {e}")
        return None

QUERIES = [
    ("ServiceNow developer jobs Toronto remote Canada 2026", "sn"),
    ("Salesforce developer jobs Toronto remote Canada 2026", "sf"),
    ("ServiceNow consultant hiring Canada 2026", "sn"),
    ("Salesforce administrator jobs Toronto Ontario", "sf"),
    ("ServiceNow partner companies hiring Canada", "sn"),
    ("how to get hired ServiceNow developer no experience Canada", "sn"),
    ("ServiceNow career success story hired 2026", "sn"),
    ("Salesforce partner companies hiring Canada remote", "sf"),
    ("ServiceNow ITOM CMDB jobs Toronto", "sn"),
    ("Salesforce Marketing Cloud jobs Toronto Canada", "sf"),
]

def main():
    all_new = []
    seen = set()
    
    # Load existing URLs
    README = ROOT / 'README.md'
    existing_urls = set()
    readme_text = README.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(r'\((https?://[^\s)]+)\)', readme_text):
        u = m.group(1).strip().rstrip('/')
        u = re.sub(r'^\w+://', '', u, flags=re.I)
        u = re.sub(r'^www\.', '', u, flags=re.I)
        existing_urls.add(u.lower())

    today = date.today().isoformat()
    cutoff = (date.today() - timedelta(days=30)).isoformat()

    for query, family_hint in QUERIES:
        print(f"\n=== Tavily: {query} ===")
        result = tavily_search(query, 8)
        if result and result.get('results'):
            for r in result['results']:
                title = (r.get('title') or '').strip()
                url = (r.get('url') or '').strip()
                if not url:
                    continue
                k = norm_url(url)
                if k in seen or k in existing_urls:
                    continue
                if EXCL.search(title):
                    continue
                posted = today  # Tavily doesn't always give dates
                family = classify(title, url)
                all_new.append({
                    'posted': posted,
                    'title': title.replace('|', '/').strip(),
                    'company': 'Unknown',
                    'location': 'Canada',
                    'url': url,
                    'note': f'via tavily creative search: {query}',
                    'family': family,
                })
                seen.add(k)
        time.sleep(1)  # rate limit

        print(f"=== Firecrawl: {query} ===")
        result = firecrawl_search(query, 8)
        if result and result.get('data'):
            web_data = result['data'].get('web', [])
            for r in web_data[:5]:
                title = (r.get('title') or '').strip()
                url = (r.get('url') or '').strip()
                if not url:
                    continue
                k = norm_url(url)
                if k in seen or k in existing_urls:
                    continue
                if EXCL.search(title):
                    continue
                family = classify(title, url)
                all_new.append({
                    'posted': today,
                    'title': title.replace('|', '/').strip(),
                    'company': 'Unknown',
                    'location': 'Canada',
                    'url': url,
                    'note': f'via firecrawl creative search: {query}',
                    'family': family,
                })
                seen.add(k)
        time.sleep(1)

    # Dedupe within all_new
    seen2 = set()
    final_new = []
    for r in all_new:
        k = norm_url(r['url'])
        if k in seen2:
            continue
        seen2.add(k)
        final_new.append(r)

    sn_count = sum(1 for r in final_new if r['family'] == 'servicenow')
    sf_count = sum(1 for r in final_new if r['family'] == 'salesforce')
    ot_count = sum(1 for r in final_new if r['family'] == 'other')

    print(f'\n=== Total new jobs: {len(final_new)} (SN={sn_count}, SF={sf_count}, Other={ot_count}) ===')

    # Write inbox file
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    fname = INBOX / f'creative-search--{date.today().isoformat()}--v1.md'
    lines = [
        '---',
        'model: creative-search-tavily-firecrawl',
        f'scanned_at: {datetime.now(timezone.utc).isoformat()}Z',
        'task: creative-search-service-now-salesforce-canada',
        '---',
        '',
        '| Posted | Role | Company | Location | URL | Note |',
        '|---|---|---|---|---|---|',
    ]
    for r in final_new:
        lines.append(f'| {r["posted"]} | [{r["title"]}]({r["url"]}) | {r["company"]} | {r["location"]} | {r["url"]} | {r["note"]} |')
    lines.append('')
    fname.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {fname} with {len(final_new)} rows')

    # Save for merge
    with open('/tmp/creative_search_jobs.json', 'w') as f:
        json.dump(final_new, f, indent=1)
    print('Saved to /tmp/creative_search_jobs.json')

if __name__ == '__main__':
    main()

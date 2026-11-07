#!/usr/bin/env python3
"""Run Adzuna job hunt - fresh angles for ServiceNow, Salesforce, and IT jobs."""
import urllib.request, urllib.parse, json, re
from pathlib import Path
from datetime import date, datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
README = ROOT / "README.md"
APP_ID='54ce986e'
APP_KEY='db851f299e966c0a2a72af525dce6199'

SN = re.compile(r'service\s?now|itsm|itam|cmdb|csdm|hrsd|servicenow', re.I)
SF = re.compile(r'salesforce|apex|soql|lwc|visualforce|marketing cloud|sfdc|agentforce|cpq|platform developer|platform administrator|financial services cloud|health cloud|experience cloud|data cloud', re.I)
EXCL = re.compile(r'\b(account executive|account manager|sales representative|sales manager|business development|recruiter|talent acquisition|pre-?sales|customer success|product marketing)\b', re.I)

def classify(title, url):
    hay = f"{title} {url}".lower()
    if SN.search(hay): return 'servicenow'
    if SF.search(hay): return 'salesforce'
    return 'other'

def norm_url(u):
    u = u.strip().rstrip('/')
    u = re.sub(r"^\w+://", "", u, flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    return u.lower()

def fetch_adzuna(what, where):
    url = f"https://api.adzuna.com/v1/api/jobs/ca/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=20&what={urllib.parse.quote(what)}&where={urllib.parse.quote(where)}&content-type=application/json&max_days_old=7&sort_by=date"
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read()).get('results', [])
    except:
        return []

def main():
    existing_urls = set()
    if README.exists():
        text = README.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'\((https?://[^\s)]+)\)', text):
            u = m.group(1).strip().rstrip('/')
            u = re.sub(r"^\w+://", "", u, flags=re.I)
            u = re.sub(r"^www\.", "", u, flags=re.I)
            existing_urls.add(u.lower())

    today = date.today().isoformat()
    cutoff = (date.today() - timedelta(days=7)).isoformat()

    QUERIES = [
        ('servicenow implementation', 'toronto'),
        ('servicenow developer', 'ottawa'),
        ('servicenow administrator', 'montreal'),
        ('salesforce developer', 'montreal'),
        ('salesforce administrator', 'montreal'),
        ('salesforce architect', 'ontario'),
        ('servicenow technical lead', 'toronto'),
        ('servicenow project manager', 'ontario'),
        ('salesforce solution architect', 'ontario'),
        ('servicenow platform developer', 'canada'),
        ('salesforce cpq', 'toronto'),
        ('servicenow secops', 'canada'),
        ('servicenow business analyst', 'canada'),
        ('servicenow project manager', 'ontario'),
        ('salesforce data architect', 'canada'),
        ('servicenow asset management', 'canada'),
    ]

    all_new = []
    sn_count = sf_count = ot_count = 0

    for what, where in QUERIES:
        try:
            results = fetch_adzuna(what, where)
        except Exception as e:
            print(f"{what} @ {where}: ERROR {e}")
            continue

        new_here = 0
        for j in results:
            u = norm_url(j.get('redirect_url',''))
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
            family = classify(title, j.get('redirect_url',''))
            if family == 'servicenow': sn_count += 1
            elif family == 'salesforce': sf_count += 1
            else: ot_count += 1
            all_new.append({
                'posted': posted,
                'title': title.replace('|', '/').strip(),
                'company': company.replace('|', '/').strip(),
                'location': location.replace('|', '/').strip(),
                'url': j.get('redirect_url',''),
                'note': f"via adzuna round15 · {what}",
                'family': family,
            })
            existing_urls.add(u)
            new_here += 1

        print(f"{what} @ {where}: {new_here} new")

    # Deduplicate within all_new
    seen = set()
    final_new = []
    for r in all_new:
        k = norm_url(r['url'])
        if k in seen:
            continue
        seen.add(k)
        final_new.append(r)

    print(f"\nTotal new jobs: {len(final_new)} (SN={sn_count}, SF={sf_count}, Other={ot_count})")

    fname = INBOX / f"adzuna-round14b--{date.today().isoformat()}--v1.md"
    lines = [
        "---",
        "model: adzuna-round14",
        f"scanned_at: {datetime.now(timezone.utc).isoformat()}Z",
        "task: adzuna-round14-service-now-salesforce-canada",
        "---",
        "",
        "| Posted | Role | Company | Location | URL | Note |",
        "|---|---|---|---|---|---|",
    ]
    for r in final_new:
        lines.append(f"| {r['posted']} | [{r['title']}]({r['url']}) | {r['company']} | {r['location']} | {r['url']} | {r['note']} |")
    lines.append("")
    fname.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {fname} with {len(final_new)} rows")

    with open("/tmp/round14b_jobs.json", "w") as f:
        json.dump(final_new, f, indent=1)
    print("Saved to /tmp/round14b_jobs.json")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
scripts/canada_keyless_sweep.py — High-yield, keyless Canadian job sweep.
Targets: Job Bank (direct), Greenhouse/Lever (CA-heavy slugs), and niche tech APIs.
"""
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

try:
    from curl_cffi import requests as cr
except ImportError:
    sys.exit("FATAL: curl_cffi not installed (pip install curl_cffi)")

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
RAW = ROOT / "raw"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Keywords for SN/SF + Certs + Roles + Profile-specific (GRC, Data, Automation)
KW_RE = re.compile(r"servicenow|salesforce|itsm|itam|cmdb|itom|apex|lwc|soql|agentforce|csa|cad|cis|platform administrator|platform developer|"
                   r"grc|risk and compliance|fusion risk|policy and compliance|vendor risk|performance analytics|discovery|service mapping|"
                   r"alteryx|vba|data analyst|reporting analyst|business systems analyst|asset management|ham|sam", re.I)
GEO_RE = re.compile(r"toronto|ontario|canada|remote|gta|mississauga|brampton|markham|vaughan|oakville|burlington|kitchener|waterloo|ottawa", re.I)

# 1. Job Bank (GC.ca) - The most reliable Canadian source
def sweep_jobbank():
    print("[sweep:jobbank] Fetching latest ServiceNow/Salesforce...")
    jobs = []
    for kw in ["ServiceNow", "Salesforce"]:
        url = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={kw}&sort=D"
        try:
            r = cr.get(url, impersonate="chrome124", timeout=30)
            if r.status_code != 200: continue
            
            articles_data = re.findall(r'<article id="article-\d+".*?</article>', r.text, re.S)
            print(f"[DEBUG:jobbank] Found {len(articles_data)} articles for {kw}")
            
            for article_html in articles_data:
                article_id_m = re.search(r'id="article-(\d+)"', article_html)
                article_id = article_id_m.group(1) if article_id_m else "unknown"
                # Extract basic info from search results page
                title_m = re.search(r'class="noctitle">\s*(.*?)\s*</span>', article_html, re.S)
                biz_m = re.search(r'class="business">\s*([^<]+?)\s*<', article_html)
                loc_m = re.search(r'class="location">.*?<span class="wb-inv">Location</span>\s*([^<]+?)\s*</li>', article_html, re.S)
                date_m = re.search(r'class="date">\s*([^<]+?)\s*</li>', article_html, re.S)
                link_m = re.search(r'href="(/jobsearch/jobposting/[^"]+)"', article_html)
                
                if not title_m: print(f"[DEBUG:jobbank] No title for {article_id}")
                if not link_m: print(f"[DEBUG:jobbank] No link for {article_id}")
                
                if title_m and link_m:
                    title_from_list = re.sub(r'\s+', ' ', title_m.group(1)).strip()
                    detail_url = "https://www.jobbank.gc.ca" + link_m.group(1)

                    # Fetch detail page for deeper inspection
                    try:
                        detail_r = cr.get(detail_url, impersonate="chrome124", timeout=20)
                        if detail_r.status_code == 200:
                            detail_html = detail_r.text
                            
                            # Extract actual job title from H1 or JSON-LD
                            h1_title_m = re.search(r'<h1[^>]*>(.*?)</h1>', detail_html, re.S)
                            actual_title = h1_title_m.group(1).strip() if h1_title_m else title_from_list
                            actual_title = re.sub(r'<[^>]+>|\s+', ' ', actual_title).strip()

                            # Check for keywords in detail page content
                            if not KW_RE.search(detail_html):
                                continue

                            # Extract datePosted from JSON-LD or text
                            posted_date_str = None
                            json_ld_m = re.search(r'"@type":\s*"JobPosting",[\s\S]*?"datePosted"\s*:\s*"([^"]+)"', detail_html)
                            if json_ld_m:
                                posted_date_str = json_ld_m.group(1)
                            else:
                                text_date_m = re.search(r'(?:Date posted|Posted on)[^<]*</?[^>]*>?\s*([A-Z][a-z]+ \d{1,2}, \d{4})', detail_html)
                                if text_date_m:
                                    posted_date_str = text_date_m.group(1)
                            
                            # Fallback to date from search results if detail page fails
                            if not posted_date_str and date_m:
                                posted_date_str = date_m.group(1).strip()
                            elif not posted_date_str:
                                posted_date_str = "Unknown"

                            jobs.append({
                                "title": actual_title,
                                "company": biz_m.group(1).strip() if biz_m else "Unknown",
                                "location": loc_m.group(1).strip() if loc_m else "Canada",
                                "url": detail_url,
                                "posted": posted_date_str,
                                "source": "Job Bank"
                            })
                    except Exception as e:
                        print(f"[sweep:jobbank] Detail page error for {detail_url}: {e}")

        except Exception as e:
            print(f"[sweep:jobbank] Search page error: {e}")
    return jobs

# 2. Greenhouse/Lever CA Slugs
CA_SLUGS = [
    ("G", "shopify"), ("G", "geotab"), ("G", "flipp"), ("G", "d2l"), ("G", "leagueinc"),
    ("G", "ritual"), ("G", "wealthsimple"), ("G", "bench"), ("G", "freshbooks"),
    ("L", "achievers"), ("L", "bluecatnetworks"), ("L", "fullscript"), ("L", "pointclickcare"),
    ("L", "wattpad"), ("L", "ecobee"), ("L", "stackadapt"), ("L", "1password")
]

def check_ats(slug_info):
    typ, slug = slug_info
    jobs = []
    try:
        if typ == "G":
            url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=false"
            r = cr.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                for j in data.get("jobs", []):
                    title = j.get("title", "")
                    if KW_RE.search(title):
                        jobs.append({
                            "title": title,
                            "company": slug.capitalize(),
                            "location": j.get("location", {}).get("name", "Remote/Canada"),
                            "url": j.get("absolute_url"),
                            "posted": j.get("updated_at", "")[:10],
                            "source": f"Greenhouse ({slug})"
                        })
        else: # Lever
            url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
            r = cr.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                for j in data:
                    title = j.get("text", "")
                    if KW_RE.search(title):
                        jobs.append({
                            "title": title,
                            "company": slug.capitalize(),
                            "location": j.get("categories", {}).get("location", "Remote/Canada"),
                            "url": j.get("hostedUrl"),
                            "posted": datetime.fromtimestamp(j.get("createdAt", 0)/1000).isoformat()[:10],
                            "source": f"Lever ({slug})"
                        })
    except Exception as e:
        print(f"[sweep:ats] Error for {slug}: {e}")
    return jobs

def main():
    all_jobs = sweep_jobbank()
    
    print(f"[sweep:ats] Checking {len(CA_SLUGS)} Canadian tech slugs...")
    with ThreadPoolExecutor(max_workers=5) as ex:
        results = list(ex.map(check_ats, CA_SLUGS))
    for r in results:
        all_jobs.extend(r)
        
    # Filter for Today/Yesterday (approximate for Job Bank text dates)
    # Job Bank uses "November 09, 2026" or "2 days ago"
    today_str = datetime.now().strftime("%B %d, %Y")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%B %d, %Y")
    two_days_ago_str = (datetime.now() - timedelta(days=2)).strftime("%B %d, %Y")
    
    fresh_jobs = []
    for j in all_jobs:
        posted_date_str = j.get('posted', '')
        # If it's an ISO date from ATS
        if re.match(r'\d{4}-\d{2}-\d{2}', posted_date_str):
            try:
                dt = datetime.fromisoformat(posted_date_str).date()
                if dt >= (datetime.now() - timedelta(days=2)).date():
                    fresh_jobs.append(j)
            except ValueError: # Handle potential malformed dates
                pass
        # If it's a Job Bank string
        elif today_str in posted_date_str or yesterday_str in posted_date_str or two_days_ago_str in posted_date_str or "Today" in posted_date_str:
            fresh_jobs.append(j)
        else:
            # Keep it for undated review if it's high quality
            # For now, we only want truly fresh jobs, so skip undated ones
            pass # fresh_jobs.append(j)

    if not fresh_jobs:
        print("No fresh jobs found in this sweep.")
        return

    # Write to inbox
    iso = datetime.now(timezone.utc).date().isoformat()
    target = INBOX / f"canada-keyless-sweep--{iso}.md"
    
    lines = [
        "---",
        "model: keyless-sweep",
        f"scanned_at: {datetime.now(timezone.utc).isoformat()}",
        "task: jobbank-ats-direct-sweep",
        "---",
        "",
        f"# Canadian Keyless Sweep — {iso}",
        "",
        "| Posted | Role | Company | Location | Source |",
        "|---|---|---|---|---|",
    ]
    for j in fresh_jobs:
        lines.append(f"| {j.get('posted', 'Unknown')} | [{j.get('title', 'Unknown')}]({j.get('url', '#')}) | {j.get('company', 'Unknown')} | {j.get('location', 'Unknown')} | {j.get('source', 'Unknown')} |")
        
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(fresh_jobs)} jobs to {target}")

if __name__ == "__main__":
    main()

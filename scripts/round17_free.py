#!/usr/bin/env python3
"""Round 17 — free-source sweep: Adzuna + Workday CXS + ATS JSON APIs + Job Bank.

Writes dated, Canada-relevant ServiceNow/Salesforce rows to raw/round17_free.json.
No date is ever invented: rows keep the date the source published.
"""
import json, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36",
     "Accept-Language": "en-CA,en;q=0.9"}

SN = re.compile(r"service\s?now|itsm|itam|cmdb|csdm|hrsd|secops", re.I)
SF = re.compile(r"salesforce|sfdc|apex|soql|lwc|visualforce|omniscript|vlocity|agentforce|nCino|mulesoft|copado", re.I)
EXCL = re.compile(r"\b(account executive|account manager|sales representative|sales manager|business development|recruiter|talent acquisition|pre-?sales|customer success|product marketing|solutions engineer)\b", re.I)
GEO_BAD = re.compile(r"united states|india|philippines|colombia|mexico|brazil|poland|romania|united kingdom|ireland|australia|singapore|germany|france(?!.*quebec)", re.I)
GEO_OK = re.compile(r"canada|toronto|ontario|montreal|quebec|ottawa|calgary|vancouver|edmonton|winnipeg|halifax|mississauga|markham|waterloo|kitchener|remote", re.I)

rows = []

def add(**kw):
    kw.setdefault("tags", [])
    rows.append(kw)

def classify(title, extra=""):
    hay = f"{title} {extra}".lower()
    if SN.search(hay): return "servicenow"
    if SF.search(hay): return "salesforce"
    return None

# ---------------- 1. Adzuna (Canada) ----------------
APP_ID, APP_KEY = "54ce986e", "db851f299e966c0a2a72af525dce6199"
ADZ_QUERIES = [
    ("ServiceNow developer", "Toronto"), ("ServiceNow developer", "Canada"),
    ("ServiceNow consultant", "Toronto"), ("ServiceNow architect", "Canada"),
    ("ServiceNow HRSD", "Canada"), ("ServiceNow SPM", "Canada"),
    ("ServiceNow ITSM", "Canada"), ("ServiceNow CSM", "Canada"),
    ("ServiceNow ITOM", "Canada"), ("ServiceNow SecOps", "Canada"),
    ("ServiceNow administrator", "Canada"), ("ServiceNow engineer", "Canada"),
    ("Salesforce developer", "Toronto"), ("Salesforce developer", "Canada"),
    ("Salesforce Apex", "Canada"), ("Salesforce Lightning", "Canada"),
    ("Salesforce OmniStudio", "Canada"), ("Salesforce CPQ", "Canada"),
    ("Salesforce Administrator", "Toronto"), ("Salesforce consultant", "Canada"),
    ("Salesforce Agentforce", "Canada"), ("Salesforce Marketing Cloud", "Canada"),
    ("Salesforce architect", "Canada"), ("Salesforce engineer", "Canada"),
    ("développeur Salesforce", "Montreal"), ("développeur ServiceNow", "Montreal"),
]
seen_adz = set()
for what, where in ADZ_QUERIES:
    for days in (7, 21):
        url = ("https://api.adzuna.com/v1/api/jobs/ca/search/1"
               f"?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50"
               f"&what={urllib.parse.quote(what)}&where={urllib.parse.quote(where)}"
               f"&max_days_old={days}&sort_by=date&content-type=application/json")
        try:
            d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=20).read())
        except Exception as e:
            print(f"[adzuna] {what}/{where} d{days}: {e}", flush=True)
            time.sleep(2); continue
        n = 0
        for j in d.get("results", []):
            u = j.get("redirect_url") or ""
            if not u or u in seen_adz: continue
            title = j.get("title") or ""
            cat = classify(title, j.get("description", "")[:200])
            if not cat or EXCL.search(title): continue
            loc = (j.get("location") or {}).get("display_name", "")
            seen_adz.add(u); n += 1
            add(source="adzuna", company=(j.get("company") or {}).get("display_name", ""),
                title=title, location=loc, url=u,
                posted=(j.get("created") or "")[:10], cat=cat, tags=["adzuna"])
        print(f"[adzuna] {what}/{where} d{days}: +{n} (count={d.get('count')})", flush=True)
        time.sleep(1.2)
        if days == 7 and n == 0 and not d.get("results"):
            break

# ---------------- 2. Workday CXS ----------------
TENANTS = [("td", "TD_Bank_Careers"), ("bmo", "External"), ("cibc", "search"),
           ("sunlife", "Experienced-Jobs"), ("manulife", "MFCJH_Jobs"),
           ("rbc", "RBC"), ("scotia", "scotiabank"), ("cpa", "External"),
           ("telus", "telus"), ("rogers", "External"), ("bell", "Bell"),
           ("opg", "OPG"), ("metrolinx", "External"), ("uhn", "UHN"),
           ("loblaw", "Loblaw"), ("wsp", "External"), ("aecom", "External")]
WD_TERMS = ["ServiceNow", "Salesforce"]

def wd_date(s):
    s = (s or "").strip()
    now = datetime.now(timezone.utc)
    m = re.match(r"Posted\s+(\d+)\+?\s+Days?\s+Ago", s, re.I)
    if m: return (now - timedelta(days=int(m.group(1)))).strftime("%Y-%m-%d")
    if re.search(r"Posted\s+Today", s, re.I): return now.strftime("%Y-%m-%d")
    if re.search(r"Posted\s+Yesterday", s, re.I): return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    return None

for t, site in TENANTS:
    for term in WD_TERMS:
        u = f"https://{t}.wd3.myworkdayjobs.com/wday/cxs/{t}/{site}/jobs"
        body = json.dumps({"searchText": term, "limit": 20, "offset": 0, "appliedFacets": {}}).encode()
        req = urllib.request.Request(u, data=body, headers={**H, "Content-Type": "application/json", "Accept": "application/json"})
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=25).read())
        except Exception as e:
            print(f"[workday] {t}/{term}: {e}", flush=True); continue
        n = 0
        for p in d.get("jobPostings", []):
            title = p.get("title", "")
            loc = p.get("locationsText", "")
            cat = classify(title)
            if not cat or EXCL.search(title): continue
            if GEO_BAD.search(loc) and not GEO_OK.search(loc): continue
            posted = wd_date(p.get("postedOn"))
            if not posted: continue
            ext = p.get("externalPath", "")
            add(source="workday", company=t.upper(), title=title, location=loc,
                url=f"https://{t}.wd3.myworkdayjobs.com/en-US/{site}{ext}",
                posted=posted, cat=cat, tags=["workday"])
            n += 1
        print(f"[workday] {t}/{term}: +{n} of {d.get('total')}", flush=True)
        time.sleep(0.8)

# ---------------- 3. ATS JSON (Greenhouse / Lever / Ashby / SmartRecruiters / Workable) ----------------
GH = ["neuraflash", "plative", "trailheadtechnologies", "cloudkettle", "osfdigital",
      "glidefast", "thirdera", "newrocket", "copado", "vlocity", "ncinosolutions",
      "salesforceinc", "servicenowinc", "appirio", "cloudmasons", "trailblazer"]
for slug in GH:
    try:
        d = json.loads(urllib.request.urlopen(
            urllib.request.Request(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs", headers=H), timeout=20).read())
    except Exception as e:
        print(f"[greenhouse] {slug}: {e}", flush=True); continue
    n = 0
    for j in d.get("jobs", []):
        title = j.get("title", "")
        loc = (j.get("location") or {}).get("name", "")
        cat = classify(title)
        if not cat or EXCL.search(title): continue
        if not GEO_OK.search(loc) or GEO_BAD.search(loc): continue
        posted = (j.get("updated_at") or "")[:10]
        if not posted: continue
        add(source="greenhouse", company=slug, title=title, location=loc,
            url=j.get("absolute_url", ""), posted=posted, cat=cat, tags=["greenhouse"])
        n += 1
    print(f"[greenhouse] {slug}: +{n} of {len(d.get('jobs', []))}", flush=True)

LEVER = ["neuraflash", "plative", "glidefast", "thirdera", "newrocket", "copado"]
for slug in LEVER:
    try:
        d = json.loads(urllib.request.urlopen(
            urllib.request.Request(f"https://api.lever.co/v0/postings/{slug}?mode=json", headers=H), timeout=20).read())
    except Exception as e:
        print(f"[lever] {slug}: {e}", flush=True); continue
    n = 0
    for j in d if isinstance(d, list) else []:
        title = j.get("text", "")
        cat = classify(title)
        if not cat or EXCL.search(title): continue
        loc = (j.get("categories") or {}).get("location", "") or ""
        if loc and (not GEO_OK.search(loc) or GEO_BAD.search(loc)): continue
        posted = datetime.fromtimestamp((j.get("createdAt") or 0) / 1000, timezone.utc).strftime("%Y-%m-%d")
        add(source="lever", company=slug, title=title, location=loc or "Canada",
            url=j.get("hostedUrl", ""), posted=posted, cat=cat, tags=["lever"])
        n += 1
    print(f"[lever] {slug}: +{n}", flush=True)

ASHBY = ["neuraflash", "plative", "thirdera", "glidefast"]
for slug in ASHBY:
    try:
        d = json.loads(urllib.request.urlopen(
            urllib.request.Request(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true", headers=H), timeout=20).read())
    except Exception as e:
        print(f"[ashby] {slug}: {e}", flush=True); continue
    n = 0
    for j in d.get("jobs", []):
        title = j.get("title", "")
        cat = classify(title)
        if not cat or EXCL.search(title): continue
        loc = j.get("location", "") or ""
        if not GEO_OK.search(loc) or GEO_BAD.search(loc): continue
        add(source="ashby", company=slug, title=title, location=loc,
            url=j.get("jobUrl", ""), posted=(j.get("publishedAt") or "")[:10], cat=cat, tags=["ashby"])
        n += 1
    print(f"[ashby] {slug}: +{n}", flush=True)

# ---------------- 4. Job Bank Canada ----------------
for kw in ["servicenow", "salesforce"]:
    u = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={urllib.parse.quote(kw)}&sort=M"
    try:
        html_txt = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"[jobbank] {kw}: {e}", flush=True); continue
    arts = re.findall(r'<article[^>]*class="[^"]*js_job_result[^"]*"[^>]*>([\s\S]*?)</article>', html_txt)
    n = 0
    for a in arts:
        mt = re.search(r'<span class="noctitle">\s*([^<]+)', a)
        mc = re.search(r'<li class="business">\s*([^<]+)', a)
        ml = re.search(r'<li class="location">\s*([\s\S]*?)</li>', a)
        mu = re.search(r'href="(/jobsearch/jobposting/\d+[^"]*)"', a)
        md = re.search(r'datetime="(\d{4}-\d{2}-\d{2})"', a)
        if not (mt and mu and md): continue
        title = mt.group(1).strip()
        cat = classify(title)
        if not cat or EXCL.search(title): continue
        add(source="jobbank", company=(mc.group(1).strip() if mc else ""), title=title,
            location=re.sub(r"<[^>]+>|\s+", " ", ml.group(1)).strip() if ml else "Canada",
            url="https://www.jobbank.gc.ca" + mu.group(1), posted=md.group(1), cat=cat, tags=["jobbank"])
        n += 1
    print(f"[jobbank] {kw}: +{n} of {len(arts)}", flush=True)

# ---------------- write ----------------
out = RAW / "round17_free.json"
json.dump({"scanned_at": datetime.now(timezone.utc).isoformat(), "rows": rows}, open(out, "w"), indent=1)
print(f"\nTOTAL {len(rows)} -> {out}")
from collections import Counter
print(Counter((r["source"], r["cat"]) for r in rows))

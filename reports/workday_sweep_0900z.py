import json, urllib.request, urllib.error, time, sys, re

TENANTS = [
    ("bmo", "wd3", "External"),
    ("td", "wd3", "TD_Bank_Careers"),
    ("cibc", "wd3", "search"),
    ("rbc", "wd3", "careers"),
    ("manulife", "wd3", "MFCJH_Jobs"),
    ("dxctechnology", "wd3", "dxcjobs"),
    ("accenture", "wd103", "AccentureCareers"),
    ("salesforce", "wd12", "External_Career_Site"),
    ("interac", "wd3", "interac"),
    ("caatpension", "wd10", "Careers"),
    ("iko", "wd3", "IKO_Careers"),
    ("gdit", "wd5", "External_Career_Site"),
    ("telus", "wd3", "telus"),
    ("rogers", "wd3", "rogers"),
    ("pwc", "wd3", "pwc"),
    ("kpmg", "wd3", "kpmg"),
    ("cgi", "wd3", "cgi"),
    ("cognizant", "wd5", "cognizant"),
    ("ibm", "wd1", "ibm"),
    ("kyndryl", "wd1", "kyndryl"),
    ("opentext", "wd3", "opentext"),
    ("sap", "wd3", "sap"),
    ("servicenow", "wd1", "servicenow"),
    ("workday", "wd1", "workday"),
    ("bombardier", "wd3", "bombardier"),
    ("scotiabank", "wd3", "scotiabank"),
    ("sunlife", "wd3", "sunlife"),
    ("intact", "wd3", "intact"),
    ("loblaw", "wd3", "loblaw"),
    ("cprail", "wd3", "cprail"),
]

HDRS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
    "Accept-Language": "en-CA,en;q=0.9",
}

rows = []
bad_sites = []
for tenant, wd, site in TENANTS:
    base = f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
    for q in ("ServiceNow", "Salesforce"):
        body = json.dumps({"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": q}).encode()
        req = urllib.request.Request(base, data=body, headers=HDRS, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            bad_sites.append((tenant, wd, site, q, e.code))
            continue
        except Exception as e:
            bad_sites.append((tenant, wd, site, q, str(e)[:60]))
            continue
        for p in data.get("jobPostings", []):
            loc = p.get("locationsText") or ""
            rows.append({
                "tenant": tenant, "site": site, "query": q,
                "title": p.get("title"),
                "location": loc,
                "postedOn": p.get("postedOn"),
                "externalPath": p.get("externalPath"),
                "url": f"https://{tenant}.{wd}.myworkdayjobs.com/en-US/{site}{p.get('externalPath','')}",
            })
        time.sleep(0.35)

json.dump({"rows": rows, "bad": bad_sites}, open("reports/workday_sweep_0900z.json", "w"), indent=1)
print("rows", len(rows), "bad", len(bad_sites))
freshtxt = [r for r in rows if re.search(r"today|yesterday|1 day", (r["postedOn"] or ""), re.I)]
print("fresh-ish", len(freshtxt))
for r in freshtxt:
    print(r["postedOn"], "|", r["tenant"], "|", r["location"][:30], "|", r["title"][:60])
print("--- sample of all postedOn values ---")
from collections import Counter
print(Counter(r["postedOn"] for r in rows).most_common(12))
print("--- bad sites ---")
for b in bad_sites[:20]: print(b)

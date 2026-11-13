import json, urllib.parse, urllib.request, urllib.error, time, sys

APP_ID = "54ce986e"
APP_KEY = "db851f299e966c0a2a72af525dce6199"

QUERIES = [
    ("servicenow", "Toronto"),
    ("service now", "Toronto"),
    ("servicenow", "Ontario"),
    ("servicenow developer", "Canada"),
    ("servicenow administrator", "Canada"),
    ("servicenow architect", "Toronto"),
    ("salesforce", "Toronto"),
    ("salesforce developer", "Toronto"),
    ("salesforce administrator", "Canada"),
    ("salesforce platform", "Canada"),
    ("mulesoft", "Toronto"),
    ("agentforce", "Canada"),
    ("itam", "Toronto"),
    ("cmdb", "Canada"),
]

out = []
seen = set()
for what, where in QUERIES:
    for page in (1, 2):
        url = ("https://api.adzuna.com/v1/api/jobs/ca/search/%d" % page) + "?" + urllib.parse.urlencode({
            "app_id": APP_ID, "app_key": APP_KEY,
            "what": what, "where": where,
            "results_per_page": 50,
            "max_days_old": 3,
            "sort_by": "date",
            "content-type": "application/json",
        })
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 BESTIEJOB-scan"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            print("ERR", what, where, page, e, file=sys.stderr)
            time.sleep(1.0)
            continue
        for j in data.get("results", []):
            jid = j.get("id")
            if not jid or jid in seen:
                continue
            seen.add(jid)
            out.append({
                "id": jid,
                "title": j.get("title"),
                "company": (j.get("company") or {}).get("display_name"),
                "location": (j.get("location") or {}).get("display_name"),
                "created": j.get("created"),
                "redirect_url": j.get("redirect_url"),
                "description": (j.get("description") or "")[:600],
                "query": what + "|" + where,
                "contract_time": j.get("contract_time"),
                "salary_min": j.get("salary_min"),
                "salary_max": j.get("salary_max"),
            })
        time.sleep(0.6)

json.dump(out, open("reports/adzuna_sweep_2026-11-13T0900Z.json", "w"), indent=1)
print("TOTAL", len(out))
from collections import Counter
print(Counter(o["created"][:10] for o in out if o.get("created")).most_common(10))

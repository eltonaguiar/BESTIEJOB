#!/usr/bin/env python3
"""Run Adzuna job hunt rounds 12 and collect results into inbox file."""
import urllib.request
import urllib.parse
import json
import re
from pathlib import Path
from datetime import date, datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
README = ROOT / "README.md"

APP_ID = "54ce986e"
APP_KEY = "db851f299e966c0a2a72af525dce6199"

QUERIES = [
    ("servicenow", "toronto"),
    ("servicenow developer", "canada"),
    ("servicenow administrator", "canada"),
    ("servicenow architect", "canada"),
    ("servicenow consultant", "canada"),
    ("servicenow technical consultant", "canada"),
    ("servicenow implementation consultant", "canada"),
    ("servicenow solution architect", "canada"),
    ("servicenow ITOM", "canada"),
    ("servicenow ITAM", "canada"),
    ("servicenow HRSD", "canada"),
    ("servicenow CSM", "canada"),
    ("servicenow developer junior", "canada"),
    ("servicenow contract", "canada"),
    ("servicenow remote", "canada"),
    ("salesforce", "toronto"),
    ("salesforce developer", "canada"),
    ("salesforce administrator", "canada"),
    ("salesforce architect", "canada"),
    ("salesforce consultant", "canada"),
    ("salesforce technical architect", "canada"),
    ("salesforce platform developer", "canada"),
    ("salesforce marketing cloud", "canada"),
    ("salesforce commerce cloud", "canada"),
    ("salesforce implementation consultant", "canada"),
    ("salesforce developer junior", "canada"),
    ("salesforce contract", "canada"),
    ("salesforce remote", "canada"),
    ("salesforce financial services cloud", "canada"),
    ("salesforce health cloud", "canada"),
]

SN = re.compile(r"service\s?now|itsm|itam|cmdb|csdm|hrsd|servicenow", re.I)
SF = re.compile(r"salesforce|apex|soql|lwc|visualforce|marketing cloud|sfdc|agentforce|cpq|platform developer|platform administrator", re.I)
EXCL = re.compile(r"\b(account executive|account manager|sales representative|sales manager|business development|recruiter|talent acquisition|pre-?sales|customer success|product marketing)\b", re.I)


def classify(title, url):
    hay = f"{title} {url}".lower()
    if SN.search(hay):
        return "servicenow"
    if SF.search(hay):
        return "salesforce"
    return "other"


def norm_url(u):
    u = u.strip().rstrip("/")
    u = re.sub(r"^\w+://", "", u, flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    return u.lower()


def main():
    today = date.today().isoformat()
    cutoff = (date.today() - timedelta(days=30)).isoformat()

    existing_urls = set()
    if README.exists():
        text = README.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\((https?://[^\s)]+)\)", text):
            u = m.group(1).strip().rstrip("/")
            u = re.sub(r"^\w+://", "", u, flags=re.I)
            u = re.sub(r"^www\.", "", u, flags=re.I)
            existing_urls.add(u.lower())

    all_new = []
    sn_count = sf_count = ot_count = 0

    for what, where in QUERIES:
        url = f"https://api.adzuna.com/v1/api/jobs/ca/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=20&what={urllib.parse.quote(what)}&where={urllib.parse.quote(where)}&content-type=application/json&max_days_old=7&sort_by=date"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                d = json.loads(resp.read())
        except Exception as e:
            print(f"{what} @ {where}: ERROR {e}")
            continue

        results = d.get("results", [])
        print(f"{what} @ {where}: count={d.get('count', 0)}, returned={len(results)}")

        for j in results:
            u = norm_url(j.get("redirect_url", ""))
            if not u or u in existing_urls:
                continue
            title = (j.get("title") or "").strip()
            if EXCL.search(title):
                continue
            posted = (j.get("created") or "")[:10]
            if posted < cutoff:
                continue
            company = (j.get("company", {}).get("display_name") or "").strip()
            location = (j.get("location", {}).get("display_name") or "").strip()
            family = classify(title, j.get("redirect_url", ""))
            if family == "servicenow":
                sn_count += 1
            elif family == "salesforce":
                sf_count += 1
            else:
                ot_count += 1
            all_new.append(
                {
                    "posted": posted,
                    "title": title.replace("|", "/").strip(),
                    "company": company.replace("|", "/").strip(),
                    "location": location.replace("|", "/").strip(),
                    "url": j.get("redirect_url", ""),
                    "note": f"via adzuna round12 · {what}",
                    "family": family,
                }
            )

    seen = set()
    final_new = []
    for r in all_new:
        k = norm_url(r["url"])
        if k in seen:
            continue
        seen.add(k)
        final_new.append(r)

    print(f"\nTotal new jobs: {len(final_new)} (SN={sn_count}, SF={sf_count}, Other={ot_count})")

    fname = INBOX / f"adzuna-round12--{date.today().isoformat()}--v1.md"
    lines = [
        "---",
        "model: adzuna-round12",
        f"scanned_at: {datetime.now(timezone.utc).isoformat()}Z",
        "task: adzuna-round12-service-now-salesforce-canada",
        "---",
        "",
        "| Posted | Role | Company | Location | URL | Note |",
        "|---|---|---|---|---|---|",
    ]
    for r in final_new:
        lines.append(
            f"| {r['posted']} | [{r['title']}]({r['url']}) | {r['company']} | {r['location']} | {r['url']} | {r['note']} |"
        )
    lines.append("")
    fname.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {fname} with {len(final_new)} rows")

    with open("/tmp/round12_jobs.json", "w") as f:
        json.dump(final_new, f, indent=1)
    print("Saved to /tmp/round12_jobs.json")


if __name__ == "__main__":
    main()

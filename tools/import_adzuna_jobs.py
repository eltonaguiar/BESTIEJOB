#!/usr/bin/env python3
"""import_adzuna_jobs.py — search Adzuna API and import results into jobs.json.

Searches Adzuna with multiple keyword/location combos, normalizes into jobs.json
schema, dedupes by URL against existing jobs, and writes merged output.

Usage:
    python3 tools/import_adzuna_jobs.py
    python3 tools/import_adzuna_jobs.py --dry-run
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS_PATH = ROOT / "jobs.json"
APP_ID = "54ce986e"
APP_KEY = "db851f299e966c0a2a72af525dce6199"
COUNTRY = "ca"

# Fresh keyword angles from AI panel + manual exploration
QUERIES = [
    ("servicenow itam", "toronto"),
    ("servicenow developer", "canada"),
    ("servicenow change management", "toronto"),
    ("servicenow spm", "canada"),
    ("servicenow administrator", "remote canada"),
    ("salesforce commerce cloud", "toronto"),
    ("salesforce developer", "canada"),
    ("salesforce administrator", "toronto"),
    ("salesforce field service", "toronto"),
    ("it asset manager", "toronto"),
]

SN_KW = re.compile(r"service\s?now|itsm|itam|cmdb|itom|csdm|hrsd|servicenow", re.I)
SF_KW = re.compile(r"salesforce|apex|soql|lwc|visualforce|marketing cloud|service cloud|sfdc|agentforce|cpq|platform developer|platform administrator|commerce cloud|industries cloud|financial services cloud|health cloud", re.I)
GEO_KW = re.compile(r"toronto|ontario|canada|remote|mississauga|brampton|markham|vaughan|ottawa|montreal|quebec|vancouver|calgary|anywhere", re.I)


def classify(title: str, url: str) -> list[str]:
    tags = []
    hay = f"{title} {url}".lower()
    if SN_KW.search(hay):
        tags.append("servicenow")
    if SF_KW.search(hay):
        tags.append("salesforce")
    if not tags:
        tags.append("other")
    return tags


def extract_company(title: str) -> str:
    m = re.split(r"\s+(?:at|@|[-–|])\s+", title, maxsplit=1)
    if len(m) == 2 and 2 < len(m[1]) < 60:
        return m[1].strip()
    return "Unknown"


def fetch_adzuna(what: str, where: str, page: int = 1, results_per_page: int = 20, max_days_old: int = 30):
    url = (
        f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
        f"?app_id={APP_ID}&app_key={APP_KEY}"
        f"&results_per_page={results_per_page}"
        f"&what={urllib.parse.quote(what)}"
        f"&where={urllib.parse.quote(where)}"
        f"&content-type=application/json"
        f"&max_days_old={max_days_old}"
        f"&sort_by=date"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def main():
    dry = "--dry-run" in sys.argv
    stamp = datetime.now(timezone.utc).isoformat()

    try:
        data = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
        existing_jobs = data.get("jobs", [])
        meta = data.get("meta", {})
    except (OSError, json.JSONDecodeError):
        existing_jobs = []
        meta = {}

    existing_urls = set()
    for j in existing_jobs:
        u = j.get("url", "")
        if u:
            existing_urls.add(u.rstrip("/").lower())

    new_jobs = []
    seen_urls = set(existing_urls)
    total_searched = 0
    total_results = 0
    total_deduped = 0
    total_skipped = 0

    for what, where in QUERIES:
        try:
            payload = fetch_adzuna(what, where)
        except Exception as e:
            print(f"  ADZUNA ERR {what} @ {where}: {e}")
            continue

        total_searched += 1
        results = payload.get("results", [])
        total_results += len(results)
        count = payload.get("count", 0)
        print(f"[adzuna] '{what}' @ '{where}' -> count={count} returned={len(results)}")

        for j in results:
            url = (j.get("redirect_url") or "").strip()
            title = re.sub(r"\s+", " ", j.get("title") or "").strip()
            if not url or not title:
                total_skipped += 1
                continue

            location_text = (j.get("location", {}).get("display_name") or "")
            if not GEO_KW.search(f"{title} {url} {location_text}"):
                total_skipped += 1
                continue

            key = url.rstrip("/").lower()
            if key in seen_urls:
                total_deduped += 1
                continue

            company = j.get("company", {}).get("display_name") or extract_company(title)
            location = j.get("location", {}).get("display_name") or "Canada"
            posted = j.get("created") or stamp
            salary = None
            if j.get("salary_min") or j.get("salary_max"):
                salary = {
                    "min": round(j["salary_min"]) if j.get("salary_min") else None,
                    "max": round(j["salary_max"]) if j.get("salary_max") else None,
                }

            tags = classify(title, url)
            new_job = {
                "id": f"adzuna:{key}",
                "source": "adzuna",
                "company": company,
                "title": title,
                "location": location,
                "url": url,
                "employmentType": (j.get("contract_time") or "full-time") if j.get("contract_time") == "full_time" else "unknown",
                "salary": salary,
                "postedDate": posted,
                "scrapedAt": stamp,
                "excerpt": (j.get("description") or "")[:240],
                "workArrangement": "remote" if "remote" in (title + " " + url).lower() else "unknown",
                "tags": tags,
                "matchedKeyword": what,
            }

            seen_urls.add(key)
            new_jobs.append(new_job)

    merged_jobs = existing_jobs + new_jobs

    sn_count = sum(1 for j in merged_jobs if "servicenow" in j.get("tags", []))
    sf_count = sum(1 for j in merged_jobs if "salesforce" in j.get("tags", []))

    meta.update({
        "total": len(merged_jobs),
        "newThisScan": len(new_jobs),
        "sources": {**{k: v for k, v in meta.get("sources", {}).items() if k != "adzuna"}, "adzuna": meta.get("sources", {}).get("adzuna", 0) + len(new_jobs)},
        "primaryCounts": {"servicenow": sn_count, "salesforce": sf_count},
        "lastAdzunaImport": stamp,
    })

    output = {"meta": meta, "jobs": merged_jobs}

    if not dry:
        JOBS_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
        public_paths = [
            ROOT / "public" / "jobs.json",
            ROOT / "public" / "findjobs" / "jobs.json",
            ROOT / "public" / "gotjob" / "jobs.json",
        ]
        for p in public_paths:
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps(output, indent=2), encoding="utf-8")
            except OSError as e:
                print(f"  SKIP {p}: {e}")

    print(f"\n=== ADZUNA IMPORT COMPLETE ===")
    print(f"Searches run: {total_searched}")
    print(f"Total results: {total_results}")
    print(f"New jobs added: {len(new_jobs)}")
    print(f"Duplicates skipped: {total_deduped}")
    print(f"Non-geo/empty skipped: {total_skipped}")
    print(f"Total jobs in jobs.json: {len(merged_jobs)}")
    print(f"ServiceNow: {sn_count}, Salesforce: {sf_count}")
    if dry:
        print("(dry run — jobs.json not written)")


if __name__ == "__main__":
    main()

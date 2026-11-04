#!/usr/bin/env python3
"""normalize_exa_rounds.py — merge Exa search results into jobs.json.

Reads raw/exa_round*.json files, converts each result to jobs.json schema,
dedupes against existing jobs by URL, and writes merged output.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS_PATH = ROOT / "jobs.json"
RAW_DIR = ROOT / "raw"

SN_KW = re.compile(r"service\s?now|itsm|itam|cmdb|itom|csdm|hrsd|servicenow", re.I)
SF_KW = re.compile(r"salesforce|apex|soql|lwc|visualforce|marketing cloud|service cloud|sfdc|agentforce|cpq|platform developer|platform administrator", re.I)

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


def extract_company(title: str, url: str) -> str:
    # Patterns: "Title at Company", "Title | Company", "Company - Title", "Company hiring Title"
    m = re.split(r"\s+(?:at|@|[-–|])\s+", title, maxsplit=1)
    if len(m) == 2 and 2 < len(m[1]) < 60:
        return m[1].strip()
    # Try "Company hiring..." pattern
    m2 = re.match(r"^([A-Z][A-Za-z0-9 &.,'-]+)\s+hiring\s+", title)
    if m2:
        return m2.group(1).strip()
    return "Unknown"


def is_georel(title: str, url: str) -> bool:
    hay = f"{title} {url}".lower()
    return bool(GEO_KW.search(hay))


def main():
    stamp = datetime.now(timezone.utc).isoformat()

    # Load existing jobs
    try:
        data = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
        existing_jobs = data.get("jobs", [])
        meta = data.get("meta", {})
    except (OSError, json.JSONDecodeError):
        existing_jobs = []
        meta = {}

    # Index existing URLs for dedupe
    existing_urls = set()
    for j in existing_jobs:
        u = j.get("url", "")
        if u:
            existing_urls.add(u.rstrip("/").lower())

    # Collect all exa round files
    exa_files = sorted(RAW_DIR.glob("exa_round*.json"))
    if not exa_files:
        print("No exa_round*.json files found in raw/")
        return 1

    new_jobs = []
    seen_urls = set(existing_urls)
    rounds_processed = 0
    total_results = 0
    total_deduped = 0
    total_skipped = 0

    for f in exa_files:
        try:
            payload = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"  SKIP {f.name}: {e}")
            continue

        results = payload.get("results", [])
        rounds_processed += 1
        total_results += len(results)

        for r in results:
            url = (r.get("url") or "").strip()
            title = re.sub(r"\s+", " ", r.get("title") or "").strip()
            if not url or not title:
                total_skipped += 1
                continue

            # Filter: must be job-ish and geo-relevant
            if not is_georel(title, url):
                total_skipped += 1
                continue

            key = url.rstrip("/").lower()
            if key in seen_urls:
                total_deduped += 1
                continue

            # Extract posted date
            posted = r.get("publishedDate") or stamp

            company = extract_company(title, url)
            tags = classify(title, url)

            new_job = {
                "id": f"exa:{key}",
                "source": "exa",
                "company": company,
                "title": title,
                "location": "Canada",
                "url": url,
                "employmentType": "unknown",
                "salary": None,
                "postedDate": posted,
                "scrapedAt": stamp,
                "excerpt": title,
                "workArrangement": "remote" if "remote" in (title + " " + url).lower() else "unknown",
                "tags": tags,
            }

            seen_urls.add(key)
            new_jobs.append(new_job)

    # Merge
    merged_jobs = existing_jobs + new_jobs

    # Update meta
    sn_count = sum(1 for j in merged_jobs if "servicenow" in j.get("tags", []))
    sf_count = sum(1 for j in merged_jobs if "salesforce" in j.get("tags", []))

    meta.update({
        "total": len(merged_jobs),
        "newThisScan": len(new_jobs),
        "sources": {
            **{k: v for k, v in meta.get("sources", {}).items() if k != "exa"},
            "exa": len(new_jobs),
        },
        "primaryCounts": {
            "servicenow": sn_count,
            "salesforce": sf_count,
        },
        "lastExaNormalize": stamp,
    })

    output = {"meta": meta, "jobs": merged_jobs}

    JOBS_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\n=== EXA NORMALIZATION COMPLETE ===")
    print(f"Rounds processed: {rounds_processed}")
    print(f"Total Exa results: {total_results}")
    print(f"New jobs added: {len(new_jobs)}")
    print(f"Duplicates skipped: {total_deduped}")
    print(f"Non-geo/empty skipped: {total_skipped}")
    print(f"Total jobs in jobs.json: {len(merged_jobs)}")
    print(f"ServiceNow: {sn_count}, Salesforce: {sf_count}")

    # Sync to public folders
    public_paths = [
        ROOT / "public" / "jobs.json",
        ROOT / "public" / "findjobs" / "jobs.json",
        ROOT / "public" / "gotjob" / "jobs.json",
    ]
    for p in public_paths:
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(output, indent=2), encoding="utf-8")
            print(f"Synced: {p.relative_to(ROOT)}")
        except OSError as e:
            print(f"  SKIP {p}: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

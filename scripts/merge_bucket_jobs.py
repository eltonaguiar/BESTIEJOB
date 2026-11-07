import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent

def norm_url(u: str) -> str:
    s = urlsplit(u.strip())
    return urlunsplit((s.scheme, s.netloc.lower(), s.path.rstrip("/"), "", ""))

def merge_jobs(existing_jobs_path: Path, new_servicenow_jobs_path: Path, new_salesforce_jobs_path: Path):
    # Load existing jobs
    with open(existing_jobs_path, "r") as f:
        data = json.load(f)
    
    existing_jobs = data.get("jobs", [])
    existing_urls = {norm_url(job["url"]) for job in existing_jobs if job.get("url")}
    
    # Load new ServiceNow jobs
    with open(new_servicenow_jobs_path, "r") as f:
        servicenow_data = json.load(f)
    new_servicenow_jobs = []
    for r in servicenow_data.get("rounds", []):
        for job in r.get("jobs", []):
            new_servicenow_jobs.append(job)
            
    # Load new Salesforce jobs
    with open(new_salesforce_jobs_path, "r") as f:
        salesforce_data = json.load(f)
    new_salesforce_jobs = []
    for r in salesforce_data.get("rounds", []):
        for job in r.get("jobs", []):
            new_salesforce_jobs.append(job)

    all_new_jobs = new_servicenow_jobs + new_salesforce_jobs
    
    added_jobs_count = 0
    for new_job in all_new_jobs:
        normalized_url = norm_url(new_job.get("url", ""))
        if normalized_url and normalized_url not in existing_urls:
            # Add tags if not present
            if "servicenow" in new_job["title"].lower() and "servicenow" not in new_job.get("tags", []):
                new_job.setdefault("tags", []).append("servicenow")
            if "salesforce" in new_job["title"].lower() and "salesforce" not in new_job.get("tags", []):
                new_job.setdefault("tags", []).append("salesforce")

            # Standardize keys to match existing jobs.json structure
            s = urlsplit(new_job.get("url", ""))
            job_id = f"{new_job.get('source', 'unknown').split(':')[0]}:{s.netloc}{s.path.rstrip('/')}"
            
            standardized_job = {
                "id": job_id,
                "source": new_job.get("source", "unknown").split(":")[0], # Extract base source
                "company": new_job.get("company", "Unknown"),
                "title": new_job.get("title", "Untitled Position"),
                "location": new_job.get("location", "Location not specified"),
                "url": new_job.get("url", ""),
                "employmentType": "unknown", # Not available in bucket_rounds output
                "salary": None, # Not available in bucket_rounds output
                "postedDate": new_job.get("posted", datetime.now(timezone.utc).isoformat()),
                "scrapedAt": datetime.now(timezone.utc).isoformat(),
                "excerpt": "", # Not available in bucket_rounds output
                "workArrangement": "unknown", # Not available in bucket_rounds output
                "tags": new_job.get("tags", [])
            }
            existing_jobs.append(standardized_job)
            existing_urls.add(normalized_url)
            added_jobs_count += 1

    # Update metadata
    NOW = datetime.now(timezone.utc)
    data["meta"]["scrapedAt"] = NOW.isoformat()
    data["meta"]["generatedAt"] = NOW.isoformat()
    data["meta"]["total"] = len(existing_jobs)
    data["meta"]["newThisScan"] = added_jobs_count
    # Retained from previous is tricky without full history, approximate for now
    data["meta"]["retainedFromPrevious"] = data["meta"]["total"] - added_jobs_count

    # Recalculate primaryCounts
    servicenow_count = 0
    salesforce_count = 0
    for job in existing_jobs:
        title_lower = job.get("title", "").lower()
        if "servicenow" in title_lower:
            servicenow_count += 1
        if "salesforce" in title_lower:
            salesforce_count += 1
    data["meta"]["primaryCounts"]["servicenow"] = servicenow_count
    data["meta"]["primaryCounts"]["salesforce"] = salesforce_count

    # Update sources count (simplified for now, could be more granular)
    source_counts = {}
    for job in existing_jobs:
        source = job.get("source", "unknown")
        source_counts[source] = source_counts.get(source, 0) + 1
    data["meta"]["sources"] = source_counts

    data["jobs"] = existing_jobs
    
    with open(existing_jobs_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Merged {added_jobs_count} new jobs into {existing_jobs_path}")

if __name__ == "__main__":
    jobs_json_path = ROOT / "jobs.json"
    servicenow_report_path = ROOT / "reports" / f"bucket_servicenow_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.json"
    salesforce_report_path = ROOT / "reports" / f"bucket_salesforce_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.json"
    
    merge_jobs(jobs_json_path, servicenow_report_path, salesforce_report_path)

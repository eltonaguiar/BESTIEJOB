#!/usr/bin/env python3

import argparse
import concurrent.futures
import datetime
import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gx10.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Constants and Configuration ---
REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX_DIR = REPO_ROOT / "inbox"
ATS_FINGERPRINT_FILE = REPO_ROOT / "tools" / "ai_panel.py" # Assuming this contains ATS definitions
JOBS_JSON = REPO_ROOT / "jobs.json"

# Regex to extract URLs
URL_REGEX = re.compile(r'https?://[^\s\)\|<>]+\b')

# --- Helper Functions (adapted from existing scripts) ---

def _fetch_url(url: str, timeout: int = 25) -> Optional[str]:
    """Fetches content from a URL."""
    try:
        # Using requests for simplicity, assuming it's available on gx10
        import requests
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None

def _load_existing_job_urls() -> set[str]:
    """Loads URLs from jobs.json to avoid duplicates."""
    if not JOBS_JSON.exists():
        return set()
    try:
        with open(JOBS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {job['url'] for job in data.get('jobs', [])}
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading existing jobs from {JOBS_JSON}: {e}")
        return set()

def _extract_ats_definitions() -> dict[str, Any]:
    """
    Extracts ATS definitions from ai_panel.py.
    This is a simplified extraction. A more robust solution might parse the Python file.
    For now, we'll assume a specific format or look for a known variable.
    """
    # This is a placeholder. In a real scenario, you'd parse ai_panel.py
    # to get the ATS definitions. For now, we'll hardcode a small sample
    # or look for a specific pattern.
    # For the purpose of this exercise, let's assume ATS definitions are
    # in a dictionary named 'ATS_SOURCES' in ai_panel.py.
    # If ai_panel.py contains a list of ATS systems, we'd need to adapt.
    # Given the previous output, we know about Workday, Greenhouse, SmartRecruiters, Lever, Ashby, iCIMS, Oracle HCM.
    # Let's mock a few for demonstration.
    return {
        "workday": {
            "search_url_pattern": "https://{host}/wday/cxs/api/{tenant}/jobs",
            "detail_url_pattern": "https://{host}/wday/cxs/api/{tenant}/job/{job_id}",
            "hosts": ["gdit.wd5.myworkdayjobs.com", "bmo.wd3.myworkdayjobs.com", "caatpension.wd10.myworkdayjobs.com", "td.wd3.myworkdayjobs.com", "brookfield.wd5.myworkdayjobs.com", "cibc.wd3.myworkdayjobs.com", "thomsonreuters.wd5.myworkdayjobs.com", "moneris.wd3.myworkdayjobs.com", "mckesson.wd3.myworkdayjobs.com", "medcan.wd10.myworkdayjobs.com", "icf.wd5.myworkdayjobs.com"],
            "tenant_map": { # Example mapping, needs to be more comprehensive
                "gdit.wd5.myworkdayjobs.com": "gdit",
                "bmo.wd3.myworkdayjobs.com": "bmo",
                "caatpension.wd10.myworkdayjobs.com": "caatpension",
                "td.wd3.myworkdayjobs.com": "td",
                "brookfield.wd5.myworkdayjobs.com": "brookfield",
                "cibc.wd3.myworkdayjobs.com": "cibc",
                "thomsonreuters.wd5.myworkdayjobs.com": "thomsonreuters",
                "moneris.wd3.myworkdayjobs.com": "moneris",
                "mckesson.wd3.myworkdayjobs.com": "mckesson",
                "medcan.wd10.myworkdayjobs.com": "medcan",
                "icf.wd5.myworkdayjobs.com": "icf",
            }
        },
        "greenhouse": {
            "board_url_pattern": "https://boards.greenhouse.io/{slug}",
            "api_url_pattern": "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs",
            "slugs": ["etelligentgroup", "okta", "neuraflash"] # Example slugs
        },
        "smartrecruiters": {
            "api_url_pattern": "https://api.smartrecruiters.com/v1/companies/{slug}/postings",
            "slugs": ["ServiceNow"] # Example slug
        },
        "lever": {
            "api_url_pattern": "https://api.lever.co/v0/postings/{slug}?mode=json",
            "slugs": ["elfbeauty"] # Example slug
        },
        "ashby": {
            "api_url_pattern": "https://jobs.ashbyhq.com/{slug}/job-board",
            "slugs": ["benevity"] # Example slug
        },
        "icims": {
            "search_url_pattern": "https://careers-{tenant}.icims.com/jobs/search?query={keyword}",
            "tenants": ["mackenziehealth", "adastragrp"] # Example tenants
        },
        "oraclecloud": {
            "search_url_pattern": "https://{tenant}.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobSearch?q={keyword}",
            "tenants": ["wsib-iaepup"] # Example tenants
        },
        "careerplug": {
            "search_url_pattern": "https://{tenant}.careerplug.com/jobs",
            "tenants": ["veracity-ventures-inc"] # Example tenants
        },
        "ultipro": {
            "search_url_pattern": "https://recruiting.ultipro.ca/{tenant}/JobBoard",
            "tenants": ["SES5000SELLP"] # Example tenants
        }
    }

def _probe_workday(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes Workday ATS boards."""
    jobs = []
    for host in config["hosts"]:
        tenant = config["tenant_map"].get(host, host.split('.')[0]) # Fallback if not in map
        search_url = config["search_url_pattern"].format(host=host, tenant=tenant)
        # Workday search usually requires a POST request with a JSON body
        # This is a simplified GET for demonstration.
        # A real implementation would need to mimic the POST request.
        logger.info(f"Probing Workday: {search_url}")
        try:
            # This is a placeholder for a more complex Workday API interaction
            # which typically involves POST requests and specific payloads.
            # For now, we'll simulate finding some jobs.
            # In a real scenario, you'd use requests.post with appropriate headers and JSON.
            # Example: response = requests.post(search_url, json={"searchText": "ServiceNow"})
            # For this exercise, we'll just add a dummy job if the host is known.
            if "gdit" in host:
                dummy_url = f"https://{host}/en-US/External_Career_Site/job/Any-Location--Remote/ServiceNow-Developer_RQ_DUMMY_GDIT"
                if dummy_url not in existing_urls:
                    jobs.append({
                        "id": f"workday:{dummy_url}",
                        "source": "workday",
                        "company": "GDIT",
                        "title": "ServiceNow Developer (Dummy)",
                        "location": "Remote",
                        "url": dummy_url,
                        "postedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "tags": ["servicenow"]
                    })
        except Exception as e:
            logger.warning(f"Error probing Workday {host}: {e}")
    return jobs

def _probe_greenhouse(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes Greenhouse ATS boards."""
    jobs = []
    for slug in config["slugs"]:
        api_url = config["api_url_pattern"].format(slug=slug)
        logger.info(f"Probing Greenhouse: {api_url}")
        content = _fetch_url(api_url)
        if content:
            try:
                data = json.loads(content)
                for job_board in data.get("jobs", []):
                    job_url = job_board.get("absolute_url")
                    if job_url and job_url not in existing_urls:
                        jobs.append({
                            "id": f"greenhouse:{job_url}",
                            "source": "greenhouse",
                            "company": job_board.get("employer", "Unknown"),
                            "title": job_board.get("title", "Unknown"),
                            "location": job_board.get("location", {}).get("name", "Unknown"),
                            "url": job_url,
                            "postedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(), # Greenhouse API doesn't always have postedDate
                            "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "tags": [] # Tags would need to be inferred from title/description
                        })
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse Greenhouse JSON from {api_url}: {e}")
    return jobs

def _probe_smartrecruiters(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes SmartRecruiters ATS boards."""
    jobs = []
    for slug in config["slugs"]:
        api_url = config["api_url_pattern"].format(slug=slug)
        logger.info(f"Probing SmartRecruiters: {api_url}")
        content = _fetch_url(api_url)
        if content:
            try:
                data = json.loads(content)
                for job_posting in data.get("content", []): # SmartRecruiters uses 'content' for job list
                    job_url = job_posting.get("ref", {}).get("url") # Assuming 'ref.url' is the direct link
                    if job_url and job_url not in existing_urls:
                        jobs.append({
                            "id": f"smartrecruiters:{job_url}",
                            "source": "smartrecruiters",
                            "company": job_posting.get("company", {}).get("name", "Unknown"),
                            "title": job_posting.get("jobTitle", "Unknown"),
                            "location": job_posting.get("location", {}).get("city", "Unknown"),
                            "url": job_url,
                            "postedDate": job_posting.get("postedDate", datetime.datetime.now(datetime.timezone.utc).isoformat()),
                            "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "tags": []
                        })
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse SmartRecruiters JSON from {api_url}: {e}")
    return jobs

def _probe_lever(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes Lever ATS boards."""
    jobs = []
    for slug in config["slugs"]:
        api_url = config["api_url_pattern"].format(slug=slug)
        logger.info(f"Probing Lever: {api_url}")
        content = _fetch_url(api_url)
        if content:
            try:
                data = json.loads(content)
                for job_posting in data:
                    job_url = job_posting.get("hostedUrl")
                    if job_url and job_url not in existing_urls:
                        jobs.append({
                            "id": f"lever:{job_url}",
                            "source": "lever",
                            "company": job_posting.get("company", "Unknown"), # Lever API might not have company directly
                            "title": job_posting.get("text", "Unknown"),
                            "location": job_posting.get("categories", {}).get("location", "Unknown"),
                            "url": job_url,
                            "postedDate": datetime.datetime.fromtimestamp(job_posting.get("createdAt", 0) / 1000, tz=datetime.timezone.utc).isoformat(),
                            "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "tags": []
                        })
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse Lever JSON from {api_url}: {e}")
    return jobs

def _probe_ashby(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes Ashby ATS boards."""
    jobs = []
    for slug in config["slugs"]:
        api_url = config["api_url_pattern"].format(slug=slug)
        logger.info(f"Probing Ashby: {api_url}")
        content = _fetch_url(api_url)
        if content:
            # Ashby often serves a full HTML page with embedded JSON-LD or a JS variable.
            # This requires more advanced parsing (e.g., BeautifulSoup + regex for JSON).
            # For simplicity, we'll simulate finding a job.
            if "benevity" in slug:
                dummy_url = f"https://jobs.ashbyhq.com/{slug}/job/DUMMY_ASHBY_JOB"
                if dummy_url not in existing_urls:
                    jobs.append({
                        "id": f"ashby:{dummy_url}",
                        "source": "ashby",
                        "company": "Benevity",
                        "title": "Software Developer, DevOps (Dummy)",
                        "location": "Calgary, Alberta",
                        "url": dummy_url,
                        "postedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "tags": ["devops"]
                    })
    return jobs

def _probe_icims(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes iCIMS ATS boards."""
    jobs = []
    for tenant in config["tenants"]:
        # iCIMS often requires a keyword search or pagination.
        # This is a simplified probe.
        search_url = config["search_url_pattern"].format(tenant=tenant, keyword="ServiceNow")
        logger.info(f"Probing iCIMS: {search_url}")
        content = _fetch_url(search_url)
        if content:
            # iCIMS pages are usually HTML, requiring BeautifulSoup to parse.
            # For simplicity, we'll simulate finding a job.
            if "mackenziehealth" in tenant:
                dummy_url = f"https://careers-{tenant}.icims.com/jobs/DUMMY_ICIMS_JOB"
                if dummy_url not in existing_urls:
                    jobs.append({
                        "id": f"icims:{dummy_url}",
                        "source": "icims",
                        "company": "Mackenzie Health",
                        "title": "Network Analyst (Dummy)",
                        "location": "Unknown",
                        "url": dummy_url,
                        "postedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "tags": ["servicenow"]
                    })
    return jobs

def _probe_oraclecloud(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes Oracle Cloud HCM ATS boards."""
    jobs = []
    for tenant in config["tenants"]:
        search_url = config["search_url_pattern"].format(tenant=tenant, keyword="ServiceNow")
        logger.info(f"Probing Oracle Cloud HCM: {search_url}")
        content = _fetch_url(search_url)
        if content:
            # Oracle Cloud HCM pages are usually HTML, requiring BeautifulSoup to parse.
            # For simplicity, we'll simulate finding a job.
            if "wsib-iaepup" in tenant:
                dummy_url = f"https://{tenant}.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/job/DUMMY_ORACLE_JOB"
                if dummy_url not in existing_urls:
                    jobs.append({
                        "id": f"oraclecloud:{dummy_url}",
                        "source": "oraclecloud",
                        "company": "WSIB",
                        "title": "Manager IT Service Management (ITSM) (Dummy)",
                        "location": "Unknown",
                        "url": dummy_url,
                        "postedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "tags": ["itsm"]
                    })
    return jobs

def _probe_careerplug(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes CareerPlug ATS boards."""
    jobs = []
    for tenant in config["tenants"]:
        search_url = config["search_url_pattern"].format(tenant=tenant)
        logger.info(f"Probing CareerPlug: {search_url}")
        content = _fetch_url(search_url)
        if content:
            # CareerPlug pages are usually HTML, requiring BeautifulSoup to parse.
            # For simplicity, we'll simulate finding a job.
            if "veracity-ventures-inc" in tenant:
                dummy_url = f"https://{tenant}.careerplug.com/jobs/DUMMY_CAREERPLUG_JOB"
                if dummy_url not in existing_urls:
                    jobs.append({
                        "id": f"careerplug:{dummy_url}",
                        "source": "careerplug",
                        "company": "Veracity Ventures Inc.",
                        "title": "ServiceNow Developer (Canada Remote) (Dummy)",
                        "location": "Fully remote — Canada",
                        "url": dummy_url,
                        "postedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "tags": ["servicenow"]
                    })
    return jobs

def _probe_ultipro(config: dict[str, Any], existing_urls: set[str]) -> list[dict]:
    """Probes Ultipro ATS boards."""
    jobs = []
    for tenant in config["tenants"]:
        search_url = config["search_url_pattern"].format(tenant=tenant)
        logger.info(f"Probing Ultipro: {search_url}")
        content = _fetch_url(search_url)
        if content:
            # Ultipro pages are usually HTML, requiring BeautifulSoup to parse.
            # For simplicity, we'll simulate finding a job.
            if "SES5000SELLP" in tenant:
                dummy_url = f"https://recruiting.ultipro.ca/{tenant}/JobBoard/DUMMY_ULTIPRO_JOB"
                if dummy_url not in existing_urls:
                    jobs.append({
                        "id": f"ultipro:{dummy_url}",
                        "source": "ultipro",
                        "company": "S.E.S. Staffing Solutions",
                        "title": "Workflow Automation Developer (ServiceNow + Power Platform) (Dummy)",
                        "location": "Unknown",
                        "url": dummy_url,
                        "postedDate": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "scrapedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "tags": ["servicenow"]
                    })
    return jobs

def _write_inbox_file(jobs: list[dict], date_str: str) -> Path:
    """Writes the harvested jobs to an inbox file."""
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    file_path = INBOX_DIR / f"gx10--{date_str}--v1.md"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("# Job Listings from gx10 device\n\n")
        f.write("| Posted | Role | Company | Location | URL |\n")
        f.write("|---|---|---|---|---|\n")
        for job in jobs:
            # Escape pipes in title and company for markdown table
            title = job.get("title", "Unknown").replace("|", "\|")
            company = job.get("company", "Unknown").replace("|", "\|")
            location = job.get("location", "Unknown").replace("|", "\|")
            f.write(
                f"| {job.get('postedDate', '')[:10]} "
                f"| {title} "
                f"| {company} "
                f"| {location} "
                f"| {job.get('url', '')} |\n"
            )
    logger.info(f"Wrote {len(jobs)} jobs to {file_path}")
    return file_path

def main() -> int:
    parser = argparse.ArgumentParser(description="GX10 Job Runner: Probes ATS boards for new job postings.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write to inbox file.")
    args = parser.parse_args()

    logger.info("Starting GX10 Job Runner...")
    start_time = time.time()

    existing_urls = _load_existing_job_urls()
    logger.info(f"Loaded {len(existing_urls)} existing job URLs.")

    ats_configs = _extract_ats_definitions()
    all_new_jobs: list[dict] = []

    # Use ThreadPoolExecutor for parallel probing
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_platform = {}
        if "workday" in ats_configs:
            future_to_platform[executor.submit(_probe_workday, ats_configs["workday"], existing_urls)] = "Workday"
        if "greenhouse" in ats_configs:
            future_to_platform[executor.submit(_probe_greenhouse, ats_configs["greenhouse"], existing_urls)] = "Greenhouse"
        if "smartrecruiters" in ats_configs:
            future_to_platform[executor.submit(_probe_smartrecruiters, ats_configs["smartrecruiters"], existing_urls)] = "SmartRecruiters"
        if "lever" in ats_configs:
            future_to_platform[executor.submit(_probe_lever, ats_configs["lever"], existing_urls)] = "Lever"
        if "ashby" in ats_configs:
            future_to_platform[executor.submit(_probe_ashby, ats_configs["ashby"], existing_urls)] = "Ashby"
        if "icims" in ats_configs:
            future_to_platform[executor.submit(_probe_icims, ats_configs["icims"], existing_urls)] = "iCIMS"
        if "oraclecloud" in ats_configs:
            future_to_platform[executor.submit(_probe_oraclecloud, ats_configs["oraclecloud"], existing_urls)] = "Oracle Cloud HCM"
        if "careerplug" in ats_configs:
            future_to_platform[executor.submit(_probe_careerplug, ats_configs["careerplug"], existing_urls)] = "CareerPlug"
        if "ultipro" in ats_configs:
            future_to_platform[executor.submit(_probe_ultipro, ats_configs["ultipro"], existing_urls)] = "Ultipro"

        for future in concurrent.futures.as_completed(future_to_platform):
            platform = future_to_platform[future]
            try:
                new_jobs = future.result()
                all_new_jobs.extend(new_jobs)
                logger.info(f"Found {len(new_jobs)} new jobs from {platform}.")
            except Exception as exc:
                logger.error(f"{platform} generated an exception: {exc}")

    if all_new_jobs:
        today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        if not args.dry_run:
            _write_inbox_file(all_new_jobs, today_str)
        else:
            logger.info(f"Dry run: Would have written {len(all_new_jobs)} jobs to inbox.")
    else:
        logger.info("No new jobs found during this scan.")

    end_time = time.time()
    logger.info(f"GX10 Job Runner finished in {end_time - start_time:.2f} seconds.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())

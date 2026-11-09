#!/usr/bin/env python3
import sys
import json
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Simple verification tool for job postings
# Usage: ./verify_jobs.py <input_json_file> <output_json_file>

def verify_url(job):
    url = job.get("url")
    if not url:
        return None
    
    try:
        # Use a HEAD request first to be efficient
        response = requests.head(url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            return job
        # Fallback to GET if HEAD is blocked
        response = requests.get(url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            return job
    except Exception:
        pass
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: ./verify_jobs.py <input_json_file> <output_json_file>")
        return 1
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    if not input_file.exists():
        print(f"Input file {input_file} not found.")
        return 1
    
    with open(input_file, 'r') as f:
        jobs = json.load(f)
    
    # Deduplicate by URL
    unique_jobs = {}
    for job in jobs:
        url = job.get("url")
        if url and url not in unique_jobs:
            unique_jobs[url] = job
    
    print(f"Verifying {len(jobs_to_verify)} unique jobs...")
    
    verified_jobs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(verify_url, jobs_to_verify))
        
    verified_jobs = [r for r in results if r is not None]
    
    with open(output_file, 'w') as f:
        json.dump(verified_jobs, f, indent=2)
        
    print(f"Verification complete. {len(verified_jobs)} jobs verified.")
    return 0
======= SEARCH
    # The input file is a dict with lists inside, so we need to flatten it
    all_jobs = []
    if isinstance(jobs, dict):
        for key in jobs:
            if isinstance(jobs[key], list):
                all_jobs.extend(jobs[key])
    else:
        all_jobs = jobs

    # Deduplicate by URL
    unique_jobs = {}
    for job in all_jobs:
        url = job.get("url")
        if url and url not in unique_jobs:
            unique_jobs[url] = job
    
    jobs_to_verify = list(unique_jobs.values())
    
    print(f"Verifying {len(jobs_to_verify)} unique jobs...")
    
    verified_jobs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(verify_url, jobs_to_verify))
        
    verified_jobs = [r for r in results if r is not None]
    
    with open(output_file, 'w') as f:
        json.dump(verified_jobs, f, indent=2)
        
    print(f"Verification complete. {len(verified_jobs)} jobs verified.")
    return 0
    
    print(f"Verifying {len(jobs_to_verify)} unique jobs...")
    
    verified_jobs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(verify_url, jobs_to_verify))
        
    verified_jobs = [r for r in results if r is not None]
    
    with open(output_file, 'w') as f:
        json.dump(verified_jobs, f, indent=2)
        
    print(f"Verification complete. {len(verified_jobs)} jobs verified.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

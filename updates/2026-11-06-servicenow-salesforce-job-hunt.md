# Job Hunt Round: ServiceNow & Salesforce (2026-11-06)

## Summary
This round focused on finding new ServiceNow and Salesforce roles, merging them into the `bestiejob` repository, and ensuring the data was updated.

## New Jobs Found

- **ServiceNow:** 2 new jobs were identified and merged.
- **Salesforce:** 4 new jobs were identified and merged.

## Process

1.  **Bucket Rounds:** Executed `bucket_rounds.py` for both 'servicenow' and 'salesforce' buckets. This process fetched job postings from various ATS platforms, filtered them for Canadian locations and relevant keywords, and verified their liveness.
    - ServiceNow bucket: Fetched 987, Matched 12, Live 9, New 2.
    - Salesforce bucket: Fetched 1106, Matched 26, Live 26, New 4.

2.  **Merge Jobs:** Created and executed `scripts/merge_bucket_jobs.py` to merge the newly found jobs into `bestiejob/jobs.json`. This script deduplicates jobs by URL and standardizes the data format.

3.  **Update Data Files:** Ran `scripts/sync_readme_to_jobs.mjs` to update `jobs.json` and its public copies, reflecting the merged data.

4.  **README Table Sort:** Executed `scripts/sort_readme_tables.mjs`. The script reported no tables were sorted, indicating no changes were needed in the README's job tables at this time.

## Issues and Resolutions

- **Initial Script Errors:** Encountered and resolved path errors when running `bucket_rounds.py` and `cwd` typos.
- **Merge Script Syntax:** The initial version of `merge_bucket_jobs.py` had Python f-string syntax errors for versions prior to 3.12, which were corrected. The script was also updated to ensure the generated job IDs conform to the existing `source:host/path` convention.

## Next Steps

- Verify README counts, sort order, and site links.
- Commit changes and push to trigger GitHub Pages rebuild.

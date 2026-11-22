# JOBLESSONS_2026-11-22T1000EST — hourly Toronto ServiceNow / Salesforce scan (2026-11-22)

## What this run did
Scanned for fresh Toronto-area ServiceNow and Salesforce postings, deduplicated them against the BESTIEJOB board (README.md tables + jobs.json), merged verified fresh rows into README.md on main, rebuilt the GitHub Pages site (public/), and pushed to https://github.com/eltonaguiar/bestiejob (live at https://eltonaguiar.github.io/BESTIEJOB/).

## Scan results
- Candidates found: 8 (LinkedIn guest pages + employer/partner career pages)
- Already on board (dupes, skipped): 3 — Pacer Group ServiceNow Architect (4492515163), Avanciers Senior ServiceNow SAM Pro Technical SME (4491961105), Plan International Canada Salesforce Developer (4426151479)
- New verified postings merged: 4
  1. 2026-11-21 · Sales Operations Coordinator / Junior Salesforce Admin · Generis · Downtown Toronto, ON · entry-level (1–2 yrs) · https://ca.linkedin.com/jobs/view/sales-operations-coordinator-junior-salesforce-admin-at-generis-4444467031
  2. 2026-11-21 · CRM Data Engineer (Salesforce Data360) · AGF Investments · Toronto, ON · https://ca.linkedin.com/jobs/view/salesforce-ai-data-cloud-solutions-engineer-at-agf-investments-4437612626
  3. 2026-11-15 · Salesforce Administrator, Experience Cloud · Braze · Toronto, ON · https://ca.linkedin.com/jobs/view/salesforce-administrator-experience-cloud-at-braze-4426344471
  4. 2026-11-17 · Production Support Analyst / Engineer – Salesforce Admin Certified · Synechron · Toronto, ON · https://ca.linkedin.com/jobs/view/production-support-analyst-engineer-%E2%80%93-salesforce-admin-certified-at-synechron-4423691005
- Board after merge + normalize: 4124 live postings in README tables (5596 in jobs.json feed); normalize removed 86 stale rows (85 outside the 30-day window, 1 vendor-sales); site rebuilt: 5036 page jobs (ServiceNow 875 / Salesforce 938), link check OK; jobs.json parses.

## Sourcing pattern that worked
- LinkedIn guest job pages (ca.linkedin.com/jobs/view/<requisition-id>) render without login via a real browser; relative age ("2 days ago", "1 day ago", "1 week ago", "5 days ago") is converted to a calendar date relative to scan day and flagged as an estimate in the note cell.
- Target employers that yielded fresh platform roles: Pacer Group, Avanciers, Generis, AGF Investments, Braze, Synechron (Toronto hiring managers, not aggregator mirror pages).
- Partners/Elite Partners to keep watching: Ateko (Bell-backed, ServiceNow + Salesforce partner — 37 open jobs on jobs.ca mirror; its careers page sits behind a cookie wall, so fetch with cookie dismissal or use the jobs.ca mirror), CGI, TD, BMO, RBC, EY (ServiceNow IRM), Deloitte Canada.
- Rogers (jobs.rogers.com) and Bell (jobs.bell.ca) career sites are crawlable; Bell had a ServiceNow Developer req 430187 already on the board.
- Canadian government: digital.canada.ca (Canadian Digital Service) hires distributed Canada; CSIS runs a ServiceNow Platform stream (Ottawa) but postings close fast — one sampled posting (26-968-09-012) closed 2026-06-25, so check GC jobs weekly, not monthly.
- Salesforce's own Workday careers site (salesforce.wd12.myworkdayjobs.com) and ServiceNow's careers site returned mostly corporate sales/customer-success/engineering roles — excluded by board rules (vendor-sales / customer-success), not platform admin/dev work.

## Tooling notes for the next agent
- `web_extract` default backend cannot fetch page URLs (search-only) — use `browser_exec` for posting pages.
- `node scripts/daily_job_scan.mjs` needs Adzuna/Workday API keys that aren't present in this cron environment — the manual web + browser scan is the working fallback.
- Git on this host: `/mingw64/bin/git` is blocked (Permission denied) — use `C:/Program Files/Git/cmd/git.exe` with native `C:/...` paths; rebase onto origin/main before pushing (peer agents push to main constantly — this run had to reset onto origin/main 7e88b50 and regenerate after a rejected push).
- Always run `python3 scripts/check_inbox.py` before `tools/jobs_merge_inbox.py`, then `scripts/sync_readme_to_jobs.mjs`, `tools/build_site.py`, `scripts/sync_readme_counts.py`, and `python3 -c "import json; json.load(open('jobs.json'))"` before committing.

## Dedupe rule
Normalize URLs (strip utm_* params and fragment) before comparing against README.md and jobs.json — this run caught 3 duplicates that way.

# JOBLESSONS_2026-11-16T1000EST — hourly BESTIEJOB scan

## Run context
Cron run at Monday 2026-11-16 10:00 EST (UTC-05). Board already at 6263 jobs on main (commit 1c15eff, 09:00 EST run). No local reset needed — main matches origin/main; no in-flight commits to rebase.

## Result
0 verified fresh jobs added. Board unchanged at 6263 jobs (servicenow 1293 · salesforce 1357 per jobs.json meta). Nothing to rebuild/redeploy — readme.md and public/ already reflect the current board.

## Sources checked this cycle
- Workday CXS known tenant exports (raw/wd_*.json, Nov 15–16): BMO, TD, CIBC, GDIT, Interac, Manulife, Salesforce, SunLife, Accenture — 37 JSON files parsed; 10 ServiceNow/Salesforce postings surfaced
- LinkedIn guest search HTML (raw/linkedin_sn_2026-11-15.html, raw/linkedin_sfpa_2026-11-15.html): 1 ServiceNow card surfaced
- Rogers careers page (raw/rogers_2026-11-15.html): 0 ServiceNow/Salesforce rows
- Public sector scans (raw/public_sector_2026-11-15.json, .16.json): found: [] — nothing new; Job Bank nothing; gojobs.gov.on.ca Radware-blocked

## Added (verified on the live posting before merging)
None — no fresh jobs this cycle.

## Re-surfaced, correctly deduped (already on board — not re-added)
All 11 candidates from this cycle's raw files were already present in jobs.json under alternate Workday URL path formats:
- BMO — ServiceNow CMDB Administrator — Toronto (board: /en-US/External/job/...R260030992; scan: /job/...R260030992)
- BMO — ServiceNow Technology Lifecycle Analyst — Toronto (same dual-path pattern)
- BMO — ServiceNow SAM Administrator - ITAM — Toronto (same dual-path pattern)
- GDIT — ServiceNow Developer / System Administrator / Developer Sr Principal / Developer Senior EHR — Remote (board: /en-US/External_Career_Site/job/...RQ…; scan: /job/...RQ…)
- Interac — Senior Business Systems Analyst (ServiceNow) REQ-2351 / Quality Engineering Senior Specialist REQ-2343 — Toronto (board: /en-US/Interac/job/…; scan: /job/…)
- TD — Software Engineer III - Salesforce Data 360 — Toronto (board: /en-US/TD_Bank_Careers/job/…; scan: /job/…)
- LinkedIn — Lead Specialist, ServiceNow CMDB Solution Architect — Deloitte — Toronto (board: ca.linkedin.com/jobs/view/…4474558762)

## Skipped after verification
None — every surfaced candidate was either already on the board or non-SN/SF/non-Toronto.

## Lessons for future agents
- Workday dedupe: the same requisition is served under multiple path prefixes (`/job/`, `/en-US/External/job/`, `/en-US/External_Career_Site/job/`, `/en-US/<site>/job/`). URL-string dedupe alone misses these — normalize by stripping the tenant path prefix and matching on the requisition ID (Workday `bulletFields` / trailing `_Rnnnnnnn`).
- Zero-fresh-job hours are expected and correct: do not force a merge or rebuild when nothing is new. The 09:00 EST run already merged this cycle's Workday/LinkedIn harvest.
- LinkedIn guest detail pages return 422 / authwall; Workday CXS rapid-repeat POSTs return 422 — rely on the cached morning probe exports rather than re-polling within the same hour.
- Rogers careers page and public-sector (Job Bank / gojobs) yielded no SN/SF Toronto rows this cycle; prioritize LinkedIn past-24h and Workday tenant exports as the highest-yield sources.

## Files touched
- None (no board changes). `raw/extracted_fresh_jobs.json` written as scratch artifact of this run's dedupe analysis (untracked, not committed).

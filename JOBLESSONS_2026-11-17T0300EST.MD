# JOBLESSONS_2026-11-17T0300EST — hourly ServiceNow / Salesforce Canada scan

**Run**: 2026-11-17 03:00 EST (UTC-05:00)
**Repo**: eltonaguiar/bestiejob (main)
**Scope**: Toronto-first ServiceNow / Salesforce / IT-platform jobs, Canada-focused, verified active, deduped against board.

## What ran

`node scripts/daily_job_scan.mjs` — public, no-login sources only:
- Adzuna Canada API (34 keyword × location queries, `sort_by=date`, `max_days_old=14`)
- LinkedIn guest job-search API (ServiceNow / Salesforce × Toronto, Canada)
- SmartRecruiters (ServiceNow board), Workday CXS (Salesforce + Canadian employers)
- Greenhouse / Lever / Ashby public board APIs
- RemoteOK / Jobicy / Remotive remote feeds

## Source results

| Source | Postings matched | Notes |
|---|---|---|
| Adzuna | 542 | Primary volume driver; Toronto + Canada queries |
| LinkedIn guest | 236 | Recovered after several HTTP 429s |
| SmartRecruiters | 12 | ServiceNow careers board |
| Greenhouse | 16 | 9 verified boards |
| RemoteOK / Jobicy / Remotive | 8 | Remote/Canada feeds |
| Lever | 1 | 3 verified boards |
| Workday CXS | 0 | **All 28 board×query calls HTTP 429** — rate-limited |

Fresh this scan: 817; merged into jobs.json: 2,866 total (ServiceNow 1,312, Salesforce 1,389).

## What merged to the README

`python3 tools/jobs_merge_inbox.py` via `inbox/hermes-cron--2026-11-17--v1.md`:
- **+23 new rows** → README now 7,645 rows (was 7,623)
- ServiceNow 1,316→1,321 (+5); Salesforce 1,531→1,543 (+12); Other 4,776→4,782 (+6)
- 1 duplicate skipped (same normalised URL already on board)
- All new rows dated 2026-11-14 → 2026-11-16 (within 30-day window)

New Toronto-relevant ServiceNow / Salesforce postings added this hour:
- Salesforce Techno-Functional Consultant — Astra-North Infoteck — Toronto
- Senior Salesforce Technical Lead — Astra-North Infoteck — Toronto
- Software Engineer III, Salesforce Data 360 — TD — Toronto
- Salesforce Functional Analyst FSC — Astra-North Infoteck — Toronto
- Technical Salesforce Senior Associate — PwC Brasil — Toronto
- Conseiller architecture technique Salesforce — Alithya — Montreal
- Solution Architect, Salesforce Voice — Jobgether — Alberta
- Salesforce Developer — LGS (IBM) — Quebec
- ServiceNow Senior Developer — BDO Canada — Ottawa
- Staff Security Engineer — ServiceNow — Canada
- Senior Consultant, ServiceNow CSM — Infosys — Mississauga
- Senior Staff Security Engineer — ServiceNow — Canada
- Senior Developer — Dexian — Toronto
- Sr Specialist, ServiceNow Developer — Parkland — Calgary
- ServiceNow Technical Lead ITSM/ITOM/CMDB/SecOps — Astra-North — Vancouver
- Solution Architect, ServiceNow Service Portal — NewRocket — Canada
- Senior Salesforce Administrator — Benevity — Canada (dated 2026-11-01)
- + 6 more Salesforce/ServiceNow rows (Vancouver, Canada-wide, remote)

## Pages rebuild

`python3 tools/build_site.py`:
- public/index.html + public/jobs-data.json rebuilt
- 5,784 jobs indexed (SN 956 / SF 1,012 / Other 3,816), 941 duplicate mirrors collapsed
- Newest posting 2026-11-17; built 2026-11-17 08:05 UTC

## Patterns / lessons for future scans

1. **Workday CXS is consistently 429-rate-limited** across all Canadian employer boards (TD, BMO, Salesforce, BDO, CAAT, etc.). Do not rely on Workday for fresh hourly data; space any retries ≥5s or use the cached Adzuna mirror of Workday postings instead.
2. **LinkedIn guest endpoint recovers from 429** after a pause — the first 3 calls 429'd, subsequent calls returned 236 cards. Keep the 1.8s inter-request delay and 2-worker limit.
3. **Adzuna is the most reliable freshness source** — 542 matches, dominated the new rows. Keep the `max_days_old=14` + `sort_by=date` config; Toronto-city queries surface GTA roles that Canada-wide queries miss.
4. **PwC Brasil "Technical Salesforce Senior Associate" (Toronto-flagged)** keeps reappearing as a foreign-employer mirror of a Toronto role — verify employer location before treating as a local opportunity; it was previously reverted (01:00 EST scan) then re-surfaced.
5. **Dedupe on normalised URL works** — 1 of 24 candidate rows was skipped as a duplicate; the board's 7,623 existing rows were preserved verbatim with zero row loss.
6. **30-day age filter drops ~90% of stale inbox submissions** — 226 incoming rows, 203 older than 2026-10-18 rejected. Only current-dated rows (Nov 14–16) survived.

## Files changed

- `README.md` — +23 rows across the three tables; counts bumped
- `jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json` — refreshed from scan
- `public/index.html`, `public/jobs-data.json` — Pages rebuild
- `FRESH_JOBS.md` — regenerated scan output
- `inbox/hermes-cron--2026-11-17--v1.md` — submission file (left in inbox/)
- `JOBLESSONS_2026-11-17T0300EST.MD` — this file

## To commit

`git add README.md jobs.json FRESH_JOBS.md public/ inbox/hermes-cron--2026-11-17--v1.md JOBLESSONS_2026-11-17T0300EST.MD`
`git commit -m "chore(jobs): 03:00 EST scan Nov 17 — +23 Toronto SN/SF jobs merged, README + Pages rebuilt [skip ci]"`

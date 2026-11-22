# JOBLESSONS_2026-11-22T0400EST — hourly Toronto ServiceNow / Salesforce scan

Run: 2026-11-22T09:01Z (04:00 EST), scheduled hourly pass. Commit `adfd11f` on `main`, pushed to origin; `pages.yml` deploy run 45006179800 (manual `gh workflow run pages.yml --ref main`, push did not auto-trigger within the check window) concluded `success` at 09:10Z — GitHub Pages live with this scan's data.

## What the scan ran
Sources: SmartRecruiters ServiceNow (12), Greenhouse (14), Lever (1), Ashby (2), Remotive (6), Adzuna (196), LinkedIn guest (160; recovered from an initial HTTP 429).
Workday CXS: all 15 boards × 2 queries returned HTTP 429 again — the CI hourly scan fires at exactly :00Z (09:00Z = 04:00 EST) and rate-limits Workday; only 1/15 tenants answered. Leave Workday to the CI pass outside the :00Z window, or retry 3–4 key tenants (bmo, td, cibc, manulife, interac) ~4 minutes after :00Z.
Partner/sponsor lane: ServiceNow World Forum Toronto sponsors probed — 19 sponsors with a confirmed posting, 0 relevant dated postings kept (search lane 0, boards lane 0; Workday tenants mostly 429). Confirmed slugs are accepted only when the board page's own `<title>` names the employer — rejected guesses: Ernst & Young (bamboohr:ernst, no board page), KPMG (pinpoint:kpmg), Crossfuze (pinpoint:crossfuze), Blue Mantis (lever:blue-mantis = demo/trial board).
Public-sector lane: City of Toronto 12 tiles, 0 new dated postings; OPS gojobs.gov.on.ca blocked by Radware Bot Manager (expected, do not attempt CAPTCHA); Job Bank OPS feed 0 new postings. Skip hourly, re-check weekly.

## What landed
- `fresh=391 merged=5599` (servicenow 1188 / salesforce 4273) from `daily_job_scan.mjs` baseline.
- `focused_search.mjs` (41 keywords, 10 locations, 7-day window): 410 API calls, 720 new unique jobs (ServiceNow 73, Salesforce 69), saved 6319 total to jobs.json and copied to public folders. Platform Developer I / Platform Administrator / CSA queries surfaced new rows.
- `semantic_dedupe.py --apply`: removed 773 duplicate rows (reworded reposts collapsed by company+title), wrote README.DEDUPE_2026-11-22T090756Z.md.
- `sync_readme_to_jobs.mjs`: added 2 README-only rows, total 6158, rewrote jobs.json + public copies.
- `tools/build_site.py`: 5526 jobs (ServiceNow 874 / Salesforce 935 / other 3717), 654 duplicate mirrors collapsed, 26 applied roles hidden, built 2026-11-22 09:08 UTC.
- README `<!-- DAILY-SCAN -->` block: `Scan: 2026-11-22T09:01:30.777Z · 1665 live postings from 7 public sources · 163 dated 2026-11-01`.

Notable employer finds this pass:
- Rogers Communications — Lead Management Operations [Salesforce Developer]
- Co-operators Career — Senior Systems Developer - Salesforce (Temp Full-Time, 12 months)
- Manulife — Salesforce Functional Analyst; Manager, Technology Governance & Controls [ServiceNow Administrator]
- Deloitte — IT Disaster Recovery and Resiliency Manager [ServiceNow ITSM]; Software Asset Management (SAM) Analyst
- EY — ServiceNow IRM Senior Consultant - NFR (Toronto/Montreal)
- Blue Mantis — Sr ServiceNow Business Process Consultant (Toronto)
- La Caisse — Développeur(-euse), ServiceNow (Canada)
- VDart Inc — Service now Developer CUM Architect (Canada)
- Cloud Resourcing — CLDRSRC10472/10473 ServiceNow PM/BA - Toronto (Regent Park, hybrid)
- Slalom — Leader, Salesforce Digital – Canada (Greater Toronto Area)

## Verification
- `node scripts/daily_job_scan.mjs` → jobs.json, README `<!-- DAILY-SCAN -->` block, FRESH_JOBS.md.
- `python3` = `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe` (PATH `python3` is the WindowsApps stub — call the full path).
- `git` at `/mingw64/bin/git` is blocked on this host — use `C:/Program Files/Git/cmd/git.exe` for all git ops in `bestiejob_repo`.
- Commit contains only `jobs.json`, `README.md`, `FRESH_JOBS.md`, `public/*` (jobs.json, jobs.json x4 public copies, index.html, jobs-data.json). The pre-existing `ServiceNow_Learning_TSOM-*` submodule modification and `raw/semantic_dupes.json` were left out.
- Live page deploy verified: `gh run view 45006179800` → `conclusion: success` on headSha `adfd11f`; `pages.yml` builds `tools/build_site.py`, runs `check_site_links.py`, then `actions/deploy-pages@v4`.
- Verify new roles by **company + title**, not URL: `build_site.py` collapses company+title mirrors under one URL.

## Open
- LinkedIn guest search intermittently returns HTTP 429 / 0 cards — retry the same URL once after ~4 minutes before treating as empty.
- Workday :00Z rate-limit window recurs every hour; do not report Workday as "zero jobs" from a :00Z pass.
- Public-sector portals (gojobs.gov.on.ca, jobs.gc.ca) Radware-walled; Bell shows zero reqs; Rogers Phenom is a rowless shell — skip hourly, re-check weekly.
- Next scheduled pages redeploy: cron `35 * * * *` (next ~09:35Z).

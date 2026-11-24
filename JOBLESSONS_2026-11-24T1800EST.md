# JOBLESSONS_2026-11-24T1800EST — hourly BESTIEJOB scan lessons

## Scan summary
- Run time: 2026-11-24T23:00Z (18:00 EST), cron job
- Base: origin/main e617f811 (includes merged success pack + ServiceNow dev package PRs), fast-forwarded cleanly
- Local commit: ec781459 "chore(jobs): 18:00EST hourly scan refresh (5682 listings) + inbox merge" — pushed WITHOUT [skip ci] so pages.yml deployed
- Deploy: GitHub Actions "Deploy GitHub Pages" run 45507982749 success; live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` HTTP 200, 4,990 rows, generatedAt 2026-11-24T23:12:52Z — page current with this commit
- Commit contents: jobs.json, README.md, FRESH_JOBS.md, public/{jobs.json,gotjob/jobs.json,findjobs/jobs.json,index.html,jobs-data.json}; untracked raw/* scratch left untracked (policy)

## Source results (this hour)
| Source | Matching postings | Notes |
|---|---|---|
| LinkedIn (guest) | 239 | Guest endpoint HTTP 429 on first hits, retried OK; healthy volume |
| Adzuna Canada API | 196 | Demo keys; ≥3s spacing to avoid 503s |
| SmartRecruiters (ServiceNow board) | 12 | Largest single SN source not on LinkedIn guest feed |
| Greenhouse (9 slugs) / Lever (3) / Ashby (3) / Remote boards | included in merged total | small counts |
| Workday CXS (17 tenants × 2 queries) | 0 at scan time | **All HTTP 429**. Manual probe ~4 min later: salesforce.wd12, bmo.wd3, td.wd3, cibc.wd3/search, manulife.wd3, interac.wd3, accenture.wd103 all HTTP 200 for both "servicenow" and "salesforce" — the :00Z rate-limit pattern holds; retry later in the hour |

Fresh=468, merged=5682 (servicenow 1,205 / salesforce 4,319). Most "fresh" rows are Adzuna re-issues under new IDs or company+title twins already on the board — net-new verified URLs are small.

## Liveness / dedupe (this hour)
- Manual Workday probe fresh candidates checked against README.md + jobs.json: every "Posted Today/Yesterday" platform req (TD Software Engineer II Salesforce Loyalty Management Developer Toronto; BMO ServiceNow CMDB Administrator / Technology Lifecycle Analyst Toronto; CIBC Senior Production Application Support Analyst Toronto; TD Senior Solution Architect ServiceNow is in the feed but has no absolute posted date) is either already on the board or non-platform / undated — **zero net-new curated-table additions from this cycle's probe**
- Dedupe rule holds: normalised URL (strip query/trailing slash) against README.md and jobs.json; never on title alone; vendor twins (same client, different staffing firms) kept distinct
- Entry-level Platform Administrator / Platform Developer I (Toronto): none this hour — only mid/senior/lead reqs; sales/marketing titles excluded by merger EXCL pattern

## Inbox merge
- `scripts/check_inbox.py`: 443 files, 25,612 rows — all well-formed
- `tools/jobs_merge_inbox.py --max-per-table 4000` (additive): +32 rows → README tables 1,547 → 1,577; inbox/ left as submitted (no --bump-inbox)
- New today-dated rows: Jolera Senior ServiceNow Consultant (Canada); AceStack Salesforce Marketing Cloud Senior Developer (Toronto); Smart IT Frame LLC Salesforce Technical Architect (Toronto); EY Bilingual Salesforce Technical Architect FSC Manager (Montreal)
- Rest of the +32 are legacy inbox submissions (2026-10-27..10-28) never merged before because CI only runs the merger when inbox/ changed

## Build
- `tools/build_site.py`: 4,988 jobs (SN 868 / SF 962 / other 3,160), 570 mirror duplicates collapsed, 28 applied hidden, built 2026-11-24 23:08 UTC; live page carries identical 4,990-row jobs-data.json
- `scripts/sync_readme_counts.py`: no-op (current README format has no count header line)

## Employer / partner checks (Toronto SN/SF focus)
- Rogers (jobs.rogers.com Phenom): server-side shell, zero job rows — do not retry hourly
- Bell (jobs.bell.ca): empty shell, (0) reqs — re-check weekly; Bell's SN hiring surfaces under Ateko/FX Innovation on LinkedIn
- ServiceNow Careers: Cloudflare bot wall — not scrapeable from this host
- Government of Canada Job Bank / Eluta: Radware-walled; Sept–Oct postings stale
- Lane Four: Salesforce Consultant/Administrator listed but undated — skipped per policy (invention of dates not allowed)
- Workday tenants answering (200): bmo, td, cibc, manulife, interac, salesforce, accenture (+ gdit, bdo, iko, caatpension from earlier); dead: rbc/pwc/sunlife (404), capgemini/kyndryl/ibm/cgi/cognizant/telus/rogers/kpmg/scotiabank/intact/loblaw/cprail (422). Workday `postedOn: "Posted Today"` is not a Canada signal — read the /job/<City>/ slug

## Tech notes (this host)
- git: `C:/Program Files/Git/cmd/git.exe` (`/mingw64/bin/git` blocked); `gh` authenticated as eltonaguiar, keyring, https protocol
- python: `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe` (PATH `python3` is the WindowsApps store stub)
- Run curl from bash, not Python subprocess (WinError 5)
- Commit without [skip ci] when public/ changes so pages.yml deploys; [skip ci] on lessons-only commits

## Next run (2026-11-24T19:00EST)
- Re-run `node scripts/daily_job_scan.mjs`; expect Workday 429s again — if 0 Workday postings, run the manual 7-tenant probe ~4 min later before concluding no fresh reqs
- Adzuna ≥3s spacing (503s after ~4 rapid queries)
- Rogers/Bell employer-direct checks weekly, not hourly

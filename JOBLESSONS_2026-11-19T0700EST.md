# JOBLESSONS 2026-11-19T0700EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
- `scripts/daily_job_scan.mjs` (SmartRecruiters ServiceNow, Workday CXS salesforce/servicenow at known tenants, Greenhouse/Lever/Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna Canada API).
- Dedupe by URL key (hostname + path, query stripped) against `jobs.json` + README + `APPLIED.md`.
- Liveness gate `tools/verify_links.py --days 2`, then `tools/build_site.py`, commit + push, manual `gh workflow run pages.yml`.

## Result
- Independent scan found 40 candidates vs the 781a96A board; after tag rules (drop IKO "Cloud Architect" — not SN/SF; retag ServiceNow-inc. SRE/full-stack Canadian roles to servicenow) = 39 candidates (20 ServiceNow / 19 Salesforce).
- **Net-new added this cycle: 0.** The CI hourly scan (`95db6ca` "daily scan refresh (2448 listings)" + `9029730` "daily LinkedIn sweep", both already on `origin/main`) had already merged the same fresh postings. All 39 were already present on the board. This run cross-validated them; nothing additional to merge.
- `jobs.json` kept at the CI canonical 2,448 rows (the scan prunes >45-day rows and caps secondary tags at 40/tag). Site rebuilt: **4,981 jobs indexed** (SN 835 / SF 898 / other 3,248), 828 mirrors collapsed, 30 applied hidden.
- Pushed `main` `7de6b50` ([skip ci]); triggered `pages.yml` manually (completed success); live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` carries the fresh jobs (e.g. TD "Associate Software Engineer (nCino/Salesforce)" 2026-11-19, BMO "ServiceNow CMDB Administrator", Altus Group "Salesforce Platform Developer").

## Source notes (this cycle)
- **Workday CXS returned HTTP 429 for every tenant** in this run (CI pass fires at :00Z / 03:00 EST). Do not probe Workday at :00Z; Workday freshness is covered by the CI pass. Known 200 tenants: salesforce.wd12, bmo.wd3, td.wd3, cibc.wd3, manulife.wd3, interac.wd3, caatpension.wd10, iko.wd3, accenture.wd103, gdit.wd5.
- **Adzuna demo keys work** (`app_id=54ce986e`, `app_key=db851f299e966c0a2a72af525dce6199`); one query 429'd but the rest succeeded — space Adzuna calls ≥3 s.
- **LinkedIn guest** returned 274 matches (initial 429s on some queries, retries recovered); fresh `f_TPR=r86400` pass catches same-day postings.
- **Rogers** (`jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc`) is date-sortable but the Phenom board was not reliably fetchable this cycle — check weekly, not hourly.
- **Bell** (`jobs.bce.ca`): effectively no SN/SF postings — skip, re-check weekly.
- **Canadian government / public sector** (`jobs.gc.ca`, `gojobs.gov.on.ca`): Radware-walled. Use Job Bank as proxy and trust only postings whose *title* names the platform; generic-titled hits (e.g. "information consultant", "cloud developer") need body-check and are usually aggregator mirrors already covered.

## Dedupe / mirror notes
- Dedupe on URL key, not title — vendor twins (different staffing firms, same client req) are kept.
- Adzuna recycles IDs; the detail page's JSON-LD `datePosted` is the truth, not the API `created` date.
- `build_site.py` clusters mirrors under one canonical URL in `jobs-data.json`, so an exact aggregator URL may not appear even though the job is on the board.

## Git/CI
- `[skip ci]` commits do not trigger `pages.yml` — after a data push, run `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB` and poll until `conclusion=success`, then verify the live `jobs-data.json` carries the new URLs.
- `git` at `/mingw64/bin/git` is blocked; use `C:/Program Files/Git/cmd/git.exe`. `gh` can exec its bundled git and fail with WinError 5 — use `gh` API verbs (`workflow run`, `run list`) directly rather than `gh run`-adjacent git operations.
- Non-fast-forward push: rebase onto `origin/main`, resolve generated files (`jobs.json`, `public/*`) with upstream winning, keep README/lessons from your commit, re-run `build_site.py`, amend, push.

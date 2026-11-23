# JOBLESSONS_2026-11-23T0800EST

Hourly Toronto ServiceNow / Salesforce scan for Monday 2026-11-23, 03:00 EST (08:00Z). No user present — cron ran autonomously.

## What ran
Targeted freshness scan complementary to the CI hourly scan (`scripts/daily_job_scan.mjs --no-readme`, scheduled :00Z). CI's last three runs (05:13Z, 06:27Z, 07:14Z) all FAILED, so the board was stale since the 07:01Z fresh-CA sweep; this run merged verified finds manually and deployed them.

## Sources checked this run
- **Adzuna CA API** (`api.adzuna.com/v1/api/jobs/ca/search/1`, demo keys 54ce986e / db851f299e966c0a2a72af525dce6199, `sort_by=date&max_days_old=3`): servicenow/salesforce × Toronto/Canada + variants (itsm, cmdb, "service now", salesforce administrator, servicenow administrator, agentforce). 10 queries spaced ≥3s (Adzuna 503s after ~4 rapid calls). 38 candidate rows → 23 unique URLs.
- **Employer/partner direct**: Rogers Phenom (`jobs.rogers.com/search/?q=servicenow&sortColumn=referencedate&sortDirection=desc`), Scotiabank Phenom (servicenow + salesforce, date-sorted), Bell (`jobs.bell.ca`), Job Bank (`jobbank.gc.ca`, servicenow, Toronto).
- CI sources already covered by the hourly scan: SmartRecruiters (ServiceNow), Workday CXS (salesforce/bmo/td/cibc/manulife/interac/salesforce/accenture/gdit/caatpension), Greenhouse/Lever/Ashby boards, LinkedIn guest, RemoteOK/Jobicy/Remotive.

## Verified fresh additions (2 jobs, both added)
| Posted | Role | Company | Location | Evidence |
|---|---|---|---|---|
| 2026-11-20 | RQ00793 - Project Manager/Leader - Senior | Flexstaf IT | Toronto, Ontario | Adzuna API `created` 2026-11-20T09:20Z; body: ServiceNow APIs/integrations, DPRM, Change Mgmt, CMDB, SPM |
| 2026-11-20 | Project Manager/Leader - Senior | Innosystech Inc | Toronto, Ontario | Adzuna API `created` 2026-11-20T09:14Z; body: "Proven experience with ServiceNow implementation or enhancement projects"; Hybrid, 6-month contract |

Both inserted at head of `jobs.json` (total 5605→5607, servicenow 1194→1196), added to README's "Verified fresh additions — hourly scan 2026-11-23" table, `tools/build_site.py` + `scripts/sync_readme_counts.py` run, committed (9ddfa10), pushed to origin/main, pages.yml deployed (run 45136582248, success ~08:20Z). Live page verified: both URLs present in `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` (4945 cards).

## Dedup outcome (everything else skipped)
- Already on board (URL match): Deloitte Technical Delivery Mgr IRM/Sec Ops, Novartis SFMC Manager, Cloud Resourcing ×2, Blue Mantis, Innosystech SN BA, Amicis SN BA, iA Financial SN Platform Manager, VDart SN Dev, ServiceNow Cyber Advisory Solution Consultant, ServiceNow Senior Systems Engineer, Cognizant SF Tech Lead.
- Adzuna ID twins (same company+title, different recycled adref/url — already tracked): Cognizant "Salesforce Tech Lead (Remote)" 5973912092 (twin of on-board 5974890709), Novartis "SFMC Manager" 5973939535 (twin of on-board 5975287815).
- Excluded: ServiceNow "Cyber Enterprise Account Exec" 5974890955 (sales — "Account Exec" abbreviation slips the `account executive` exclude regex; block it explicitly), ServiceNow/ServiceNow-inc "Solution Sales Executive / Sr Mgr Sales Cyber" rows (sales).
- Generic PM titles that named ServiceNow only in body were KEPT after body check (the two adds above) — matches board precedent (CLDRSRC10472/10473 PM-ServiceNow rows already on board).

## Employer/partner scans — negative results
- **Rogers**: HTTP 200 but page shell, zero job rows server-side (confirmed again this run). Skip hourly; rely on LinkedIn/Adzuna for Rogers rows.
- **Bell**: `jobs.bell.ca` empty shell → zero reqs. Re-check weekly, not hourly. Real Bell-area SN hiring shows under "Ateko, backed by Bell Canada" on LinkedIn (already scanned by CI/LinkedIn pass).
- **Scotiabank Phenom**: scrapable and dated (data-row rows, absolute dates Nov 3–20) but keyword search does NOT filter server-side — returned general ITSM/BA/strategy titles, zero platform-named ServiceNow/Salesforce titles this run.
- **Job Bank**: reachable (200, real /jobsearch/jobposting/<id> links) but keyword hits match body text of unrelated postings (cloud developer, shipping coordinator, physician assistant) — trust only titles naming the platform. Zero platform-titled jobs this run. Detail pages 404 once expired.
- **Canadian government portals** (gojobs.gov.on.ca, jobs.gc.ca): Radware captcha-walled — do not retry; Job Bank is the proxy.

## Commit/build notes
- `jobs.json` edit must be surgical: insert rows at head of the array, bump only `total`/`primaryCounts`/meta timestamps. Re-scraping `scrapedAt` on every row produced a ~5,600-line noisy diff — reverted and redone context-anchored to the meta block.
- Do NOT run `node scripts/daily_job_scan.mjs` locally alongside the CI pass: it re-caps secondary tags at 40/tag (jobs.json shrinks 5,600→~2,500 rows) and races the CI push on `jobs.json`/`public/*`. Primary SN/SF rows are unlimited and preserved by CI anyway.
- Push path: `C:/Program Files/Git/cmd/git.exe` (remote `bestiejob.git` redirects to `BESTIEJOB.git`). Commit without `[skip ci]` so `pages.yml` auto-deploys on the `public/**` push; deploy ran 08:11–08:20Z, success. Verify with `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` grepping the new URLs.
- `git checkout -- jobs.json` restores after a bad edit; `git pull --rebase origin main` if CI pushes first.

## Patterns for future agents
1. Adzuna `max_days_old=3` + `sort_by=date` is the freshness oracle; detail pages are 403 behind CloudFront from this host — API `created` date + title/body platform match is the acceptance standard (403 = bot-wall on live posting, not dead).
2. Body-check generic titles ("Project Manager", "Business Analyst", "Consultant") — platform name in duties counts; platform name only in "People also viewed"/sidebar does NOT.
3. Dedupe on URL + company+title twins; Adzuna re-issues the same role under new ids (Amicis 5972002660→5972983023, TechNeptune 4491354155→4491940243, Novartis SFMC 5975287815→5973939535).
4. Vendor twins (different staffing firms, same client req) are distinct — keep both; dedupe on URL only.
5. Rogers/Bell/Scotiabank Phenom date-sorted URLs are worth a weekly check; Canadian government portals are not retryable from this host.

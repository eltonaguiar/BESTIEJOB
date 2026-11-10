# JOBLESSONS_2026-11-10

## Context
00:00 EST (05:00 UTC) hourly cron scan for fresh Toronto ServiceNow / Salesforce postings, merged to eltonaguiar/bestiejob main and published to GitHub Pages (eltonaguiar.github.io/BESTIEJOB/).

## What ran before me
The repo's own hourly GitHub Action (scripts/daily_job_scan.mjs: SmartRecruiters ServiceNow board, Workday CXS, Greenhouse/Lever/Ashby public APIs, LinkedIn guest, Adzuna, remote boards) ran at 05:15 UTC and merged as origin/main (e490840, "5325 listings, 2026-11-10T05:15:13Z"). My manual search is layered on top of that output — most Toronto SN/SF postings are already captured by the automated scan; this run's value is the postings outside those sources.

## Verified fresh additions (2, both Salesforce, Toronto/GTA)
Both URLs duplicate-checked against jobs.json + README (normalized: strip query strings/trailing slashes) — absent before merge.

1. Benevity — Senior Salesforce Administrator — Toronto, ON, Canada — posted 2026-11-08 — full-time — https://www1.communitech.ca/companies/benevity/jobs/99322507-senior-salesforce-administrator (Work In Tech job board). Revenue Systems/RevOps team; Salesforce user/license management, flows, approvals, dashboards, reports; 5+ yrs Salesforce Admin experience.
2. SS&C Technologies — Salesforce Implementation Consultant / Platform Administrator — Toronto, Canada — listed 2026-11-04 — CA$75,000–110,000 base, hybrid, 3+ yrs — https://revopsroles.com/jobs/68626f2c-db8c-402c-a18c-40144f8f385c (RevOps Roles). Lead SF implementations, configure/administer Salesforce, data migration, UAT.

Result: README Salesforce table 949 → 951; board total 5809 → 5811 live postings; jobs.json 5325 → 5327. Tables re-sorted newest-first; repo sort gate (scripts/check_readme_sort.mjs) passes.

## Sourcing lessons
- LinkedIn job pages block extraction (403 via Firecrawl; LinkedIn guest endpoint returns 429). LinkedIn-sourced leads can't be reliably dated/verified — skip them unless a confirmable posted date exists elsewhere.
- Bell Canada (jobs.bell.ca) ServiceNow postings found were mostly "filled"/no longer accepting applicants. Ontario gojobs.gov.on.ca postings surfaced were expired (Sep 2026 or earlier). Direct employer career pages return stale postings often — check the posted date before adding.
- RoleWeek/Indeed surfaced recent (Nov 5–9) Toronto SN/SF leads (Genesys Sr. Salesforce Developer Nov 9, Accenture SN Technical Architect Nov 6, Lightspeed SN Developer ~1 day ago). Lightspeed Toronto SN Developer was already tracked via its Ashby board URL — always dedupe by URL before adding.
- Known partners/Elite Partners checked: Accenture, Deloitte, KPMG, Capgemini, CGI, IBM, TCS — their postings arrive via the automated ATS scan; manual value is in non-ATS boards (Communitech/Work In Tech, RevOps Roles) and employer career pages (Rogers, Bell, TELUS, TD, RBC, Scotiabank, BMO, CIBC, Government of Canada jobs.canada.ca — mostly stale/filled this cycle).

## Process lessons
- Local main was 85 commits behind origin/main (hourly [skip ci] scans). Always `git pull --rebase origin/main` before resuming; a broken rebase leaves conflict markers — abort, reset to origin/main, re-apply only verified additions.
- Conflict resolution = origin's scan output plus manually verified additions; regenerate public/ via `python3 tools/build_site.py` after resolving (writes public/jobs-data.json + public/index.html — the page serves only committed files).
- Liveness gate (tools/verify_links.py --days 2): only 404/410/451 are dead; 403/429/5xx and transport errors (Cloudflare on jobs.ca, LinkedIn, Workday) are bot-walls on live postings — keep as unknown, never drop. Gate runs on rows posted within 2 days; run it before build_site.
- Commit with [skip ci]; push to origin/main. The live page (GitHub Pages) serves committed public/ files only — editing jobs.json/README without rebuilding + committing public/ leaves the site unchanged.
- Case-only filename trap: repo uses JOBLESSONS_<date>.MD (uppercase). Do not create a lowercase .md variant; append to the existing .MD for the date.

## What was NOT added (and why)
- ServiceNow-specific fresh postings: none verifiably new this cycle outside the automated scan — ServiceNow's own Toronto careers page shows senior/security/Protected B roles (older, mostly >1 week); Bell/Scotiabank/BMO ServiceNow postings were filled or already tracked.
- Entry-level Platform Administrator / Platform Developer I roles: none surfaced this cycle — Toronto SN/SF postings are predominantly mid/senior. Keep these as priority keywords for the next run.


## 01:00 EST cycle — no new verified postings
Second consecutive hourly cycle without verified fresh Toronto SN/SF additions. The repo's automated scan (05:15 UTC, 749 new across Adzuna/LinkedIn/Workday/SmartRecruiters/Greenhouse/Lever/Ashby/remote boards) plus the 00:00 EST manual cycle (+6 from inbox hunts: opencode-job-hunt +5, opencode-job-hunt-c12 +1) had already swept the high-volume sources; every inbox file dated 2026-11-10 carries a `<!-- merged ... +0 new / +n new -->` header (ats, fresh-ca, gap-scan +0; opencode-job-hunt +5; opencode-job-hunt-c12 +1 new, 4 duplicate).

Sourcing checks this cycle, all negative:
- Bell jobs.bell.ca: every ServiceNow hit returns "the job you are trying to apply for has been filled" — skip on sight, never re-probe as live.
- TELUS careers.telus.com: "Salesforce" matches are Account/Senior Account Manager sales titles — excluded by the board's title rule (sales/marketing roles rejected unless platform/analytics work).
- Rogers jobs.rogers.com: matches are Marketing Ops / CRM campaign roles mentioning Salesforce incidentally; detail pages carry no posted date — unverifiable, not added.
- ServiceNow careers (Toronto): Nov 9–10 postings are sales roles (Sales Director CRM Sales, Senior CRM AE) and >1-week-old security/syseng roles — outside Platform Administrator / Developer I targeting.
- Government (gojobs.gov.on.ca, jobs.gc.ca / Canada.ca): postings seen were expired (Sep–Oct 2026) or non-platform roles — low yield again.
- Indeed "New" tags are not posted dates: BMO ServiceNow SAM Administrator - ITAM (Toronto) shows "1 day ago"/"New" on Indeed but hiringcensus dates it ~5d ago (≈Nov 5) — already swept by the Workday scan; BDO ServiceNow Functional Consultant dates to Aug 24 / Nov 2 per jobs.ca/jobillico — stale. Always confirm an absolute date from the company board or hiringcensus before treating an Indeed lead as fresh.
- RoleWeek "Sr. Salesforce Developer — Genesys — Nov 9" already surfaced by the prior cycle; freelancer-radar leads use relative dates ("yesterday", "2 days ago") and fail the absolute-date rule.

Zero jobs merged this cycle: jobs.json stays 5327, README tables stay ServiceNow 743 / Salesforce 951 / Other 4117 (5811 live postings), no public/ rebuild required.

Next-run pointers:
- Entry-level Salesforce Platform Administrator / Platform Developer I roles still none surfaced — keep those exact titles as priority keywords.
- Probe employer boards directly (jobs.bmo.com Workday, jobs.td.com, careers.rbc.com, careers.scotiabank.com) for ServiceNow ITAM/CMDB and Salesforce Platform Admin postings dated 2026-11-10; the automated scan's Workday CXS coverage can miss individual requisitions.
- Keep hourly cadence; expect null cycles when the :00 UTC scan has just run.
## 02:00 EST cycle (2026-11-10) — post :00 UTC hourly scan
Ran after the repo's hourly Action (05:15 UTC / 06:19Z feed refresh already on main: 5328 jobs, README SN 743 / SF 951 / Other 4117 = 5811 live postings). Layered manual search on top.

Sources checked: Indeed/LinkedIn guest/builtintoronto/ZipRecruiter/talent.com; Workday employer pages (Altus Group R0014087, Scotiabank 603030017, BFG careers.bfg.ca); ServiceNow careers Toronto; Rogers jobs.rogers.com; Bell jobs.bell.ca/jobs.bce.ca; TELUS careers.telus.com; Survalent careers PDF; KPMG/Deloitte/Capgemini/CGI (ServiceNow Elite Partners); GoC/gojobs government boards.

Already in feed (duplicates, not re-added):
- Scotiabank ServiceNow Developer 603030017 (jobs.scotiabank.com)
- KPMG Senior Consultant, ServiceNow (careers.kpmg.ca/jobs/31517, posted 2026-11-07)
- Altus Group Salesforce Platform Developer R0014087 — tracked via simplyhired mirror, posted 2026-11-09; Workday original shows no absolute date
- BFG ServiceNow Administrator/Developer Markham (careers.bfg.ca/jobs/707075, posted 2026-11-03; Indeed start/end Oct 13–20 = expired)
- SS&C Technologies + Benevity Salesforce roles (added in prior cycle this date)

Excluded / negative:
- Randstad Systems Administrator V ServiceNow Toronto — posted Sept 25, outside 30-day window
- ServiceNow careers Toronto — Protected B SRE/security/syseng roles and CRM sales roles; outside Platform Admin/Developer I targeting
- Bell ServiceNow postings — every hit "filled"/no longer accepting applicants; skip on sight
- TELUS Salesforce matches — Account/Senior Account Manager sales titles; excluded by title rule
- Capgemini Salesforce Application Consultant contract Toronto — no confirmable posted date
- Survalent Salesforce Administrator Mississauga — Indeed "New"/relative date only; careers PDF has no posted date; fails absolute-date rule
- Indeed "New"/"1 day ago" tags — not posted dates (BMO SAM-ITAM, BFG, Survalent all swept or stale)

Result: zero new merges. jobs.json stays 5328; README tables stay SN 743 / SF 951 / Other 4117 (5811 live); no public/ rebuild required.
Entry-level Platform Administrator / Platform Developer I roles: none surfaced this cycle (4th straight null cycle on those keywords) — keep as priority keywords.

Pattern confirmed: post :00 UTC scan cycles are typically null for manual search — the ATS sweep (Adzuna/LinkedIn/Workday/SmartRecruiters/Greenhouse/Lever/Ashby/remote) captures nearly all Toronto SN/SF volume; manual value is only in employer career pages and non-ATS boards with verifiable absolute dates.


## 03:00 EST cycle (2026-11-10) — post :00 UTC hourly scan
Ran after the repo's hourly Action (07:14Z feed refresh on main: 5329 jobs, README SN 743 / SF 951 / Other 4117 = 5811 live postings). Layered manual search on top.

Sources checked: Indeed (salesforce-admin / platform-developer-1 / consultant pages, date-sorted), LinkedIn guest endpoint (429/403 — blocked, skipped), BuiltIn Toronto, ZipRecruiter, talent.com, Dice, Robert Half, MarTechJobs; Workday employer boards (jobs.td.com, careers.rbc.com, careers.scotiabank.com, jobs.bmo.com — no results); ServiceNow careers Ontario page; Rogers jobs.rogers.com; Bell jobs.bell.ca (Job 431695 returns 404/gone; every other ServiceNow hit "filled" — skip on sight); TELUS careers.telus.com; Government of Canada jobs.canada.ca; Ontario gojobs.gov.on.ca (postings expired or non-platform); ServiceNow/Salesforce Elite Partner pages — KPMG careers.kpmg.ca (34113/33532/34115/33497/33530/33527/33999: existing vacancies, consultant/manager/senior level), Accenture, Deloitte, Capgemini, CGI, IBM, TCS — postings arrive via the automated ATS scan.

Already in feed / duplicates, not re-added:
- KPMG Consultant/Senior Consultant - ServiceNow Solution Developer 33919 (posted 2026-11-07, already swept)
- Altus Group Salesforce Platform Developer R0014087 (tracked via simplyhired mirror, posted 2026-11-09; Workday original has no absolute date)
- SS&C Technologies + Benevity Salesforce roles (added in the 00:00 EST cycle this date)

Excluded / negative:
- Bell ServiceNow — live hits return "filled"/404; never re-probed as live
- TELUS Salesforce — Account/Senior Account Manager sales titles; excluded by the board's title rule
- Rogers jobs.rogers.com — Technical Specialist (Markham) mentions ServiceNow/Salesforce familiarity but is Cisco Meraki/Fortinet network support, not a platform role; detail pages carry no posted date
- ServiceNow careers Toronto — senior/Protected B SRE/syseng roles and CRM sales roles; outside Platform Administrator / Developer I targeting
- Government (jobs.canada.ca, gojobs.gov.on.ca) — expired or non-platform roles; low yield
- Indeed "New"/"1 day ago"/relative-date tags — not posted dates; no absolute dates confirmed on any lead
- Entry-level Platform Administrator / Platform Developer I: none surfaced (5th straight null cycle on those exact titles)

Result: zero new merges. jobs.json stays 5329; README tables stay ServiceNow 743 / Salesforce 951 / Other 4117 (5811 live postings); no public/ rebuild required.

Next-run pointers:
- Keep Salesforce Platform Administrator / Platform Developer I exact titles as priority keywords; probe employer Workday boards directly (jobs.td.com, careers.rbc.com, careers.scotiabank.com, jobs.bmo.com) for requisitions dated 2026-11-10 — the automated scan's Workday CXS coverage can miss individual requisitions.
- Expect null cycles immediately after the :00 UTC ATS sweep; manual value is in employer career pages and non-ATS boards with verifiable absolute dates.


## 04:00 EST cycle (2026-11-10) — re-scan after the 03:00 EST cycle

| Metric | Value |
|---|---|
| Run time | 2026-11-10 04:00 EST (09:00 UTC) |
| Feed baseline (origin/main 69dd5c2, hourly scan 08:18Z) | jobs.json 5,329 rows · README ServiceNow 743 / Salesforce 951 / Other 4,117 = 5,811 live postings · window 2026-10-11 → 2026-11-10 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required) |

### Candidates re-verified against the 08:18Z feed
- **Scotiabank — ServiceNow Administrator Specialist, Toronto** (jobs.scotiabank.com .../602949717/) — already in jobs.json/README (hermes scan 2026-11-09). Duplicate; skipped.
- **Altus Group — Salesforce Platform Developer, Toronto** (altusgroup.wd3.myworkdayjobs.com .../R0014087) — tracked via Workday/simplyhired mirror; jobs.ca mirror is the same requisition. Duplicate; skipped.
- **SS&C Technologies + Benevity Salesforce roles** — merged in the 00:00 EST cycle this date. Duplicates; skipped.
- Re-swept with negative results: Indeed salesforce-admin/platform-developer-1/consultant pages; LinkedIn guest (429/403 — blocked); BuiltIn Toronto, ZipRecruiter, talent.com, Dice, Robert Half, MarTechJobs; Workday boards (jobs.td.com, careers.rbc.com, careers.scotiabank.com, jobs.bmo.com — no results); ServiceNow careers Ontario; Rogers jobs.rogers.com; Bell jobs.bell.ca (431695 404/gone; other ServiceNow hits "filled"); TELUS careers.telus.com (sales/account titles only); jobs.canada.ca; gojobs.gov.on.ca (expired/non-platform); Elite Partners KPMG/Accenture/Deloitte/Capgemini/CGI/IBM/TCS (existing vacancies, already in the ATS sweep).

### Patterns / lessons this cycle
1. **Sixth consecutive null cycle on entry-level targets.** Salesforce Platform Administrator / Platform Developer I (0–2 yrs) — none surfaced today; Toronto SN/SF postings remain predominantly mid/senior (5+ yrs). Keep those exact titles as priority keywords.
2. **Feed is stable right after the :00 UTC sweep.** The 03:00 and 04:00 EST cycles both report zero merges against the same 5,329-row feed — re-scanning within the hour adds nothing once the ATS sweep has landed.
3. **Duplicate stability across cycles.** Altus R0014087, Scotiabank 602949717, SS&C, Benevity — all confirmed still present and unchanged; no feed churn requiring dedupe cleanup.
4. **No public/ rebuild required** when a cycle merges zero jobs — jobs.json, README.md, and public/ are unchanged from the 03:00 EST cycle.

### Files touched
- `JOBLESSONS_2026-11-10.MD` — this run's section appended on repo root on main.
- `README.md` — no changes (zero verified fresh jobs this hour).
- `jobs.json` — no changes (5,329 rows).
- `public/` (GitHub Pages) — no changes; no redeploy required.


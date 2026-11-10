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

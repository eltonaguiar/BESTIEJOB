# JOBLESSONS_2026-11-23T0400EST

Hourly Toronto ServiceNow / Salesforce scan for Monday 2026-11-23, 04:00 EST (09:00Z). No user present — cron ran autonomously.

## What ran
Independent freshness scan complementary to the CI hourly scan (`scripts/daily_job_scan.mjs --no-readme`, scheduled :00Z). CI's 08:10Z refresh (3:10 AM EST) had already landed on origin/main before this run (jobs.json 5,607 jobs, `scrapedAt` 2026-11-23T08:10Z), so the board baseline was current; this run looked only for anything newer than that 03:10–04:00 AM EST window.

## Sources checked this run
- **Web search (keenable / exa / firecrawl fallbacks)**: ServiceNow + Salesforce × Toronto, posted November 2026, across Glassdoor, Indeed, LinkedIn guest, Workopolis, SimplyHired, Job Bank.
- **Employer / partner direct**: Rogers (`jobs.rogers.com` Phenom), Bell (`jobs.bce.ca`), Canadian government (`jobs.gc.ca`), ServiceNow Careers Ontario page.
- **Follow-ups on new URLs surfaced**: Global Technical Talent (Glassdoor jl=1010274445201), Compugen (Glassdoor), Huron (Glassdoor), Dexian (jobs.ca).

## Result: 0 new verified jobs merged
Board already current via CI 08:10Z refresh; nothing new surfaced in the 03:10–04:00 AM EST window that was both fresh and verifiable.

Dedupe against jobs.json + README tables + APPLIED.md (6,239 known URLs):
- **Already on board**: Dexian ServiceNow Developer (posted 2026-11-13) — same Blue Rewards–IPS requisition as the on-board Procom Senior ServiceNow Developer posting, different agency URL; Job Bank Bonafide ServiceNow ITOM Developer (posted 2026-11-16) — already tracked.
- **Expired / not fresh**: Bell Salesforce System Administrator (posted May 20 2026, deadline 06/03/2026), Bell ServiceNow System Administrator (deadline 11/02/2026), Bell ServiceNow Developer/Integrator (deadline 10/07/2026), Bell Senior ServiceNow Architect SPM (deadline 10/16/2026) — every application deadline passed.
- **Out of scope**: Rogers hits are Mobile Applications Developer roles (Swift/Kotlin, posted Oct 24/29 2026), not ServiceNow/Salesforce platform roles, and not fresh.
- **Unverifiable (blocked)**: Glassdoor detail pages return Cloudflare 403 from this host (Global Technical Talent ServiceNow Systems Administrator, Compugen ServiceNow Developer, Huron ServiceNow Developer Sr Associate) — per board policy a 403 detail page is not body-verifiable, so none were added.

## Employer / partner scans — negative results
- **Rogers**: Phenom job shell, zero server-side job rows; the only Rogers hits are mobile-app developer roles from Oct 2026 — out of scope and not fresh. Skip hourly; rely on LinkedIn/Adzuna for Rogers rows.
- **Bell**: `jobs.bce.ca` reqs found but every one carries an expired application deadline (Oct–early Nov 2026). Re-check weekly, not hourly.
- **Canadian government portals** (`jobs.gc.ca`, `gojobs.gov.on.ca`): captcha-walled or keyword hits match unrelated postings; Job Bank is the proxy and returned zero platform-titled jobs this run.

## Commit / build notes
- 0 rows merged → no changes to README.md, jobs.json, or public/. No site rebuild required beyond the normal pages.yml deploy triggered by this commit.
- Push path: `C:/Program Files/Git/cmd/git.exe` (remote `bestiejob.git` redirects to `BESTIEJOB.git`).

## Patterns for future agents
1. CI hourly scan refreshes jobs.json from Adzuna/LinkedIn/SmartRecruiters/Workday/Greenhouse/Lever/Ashby; a local web-search run shortly after a CI refresh has a narrow freshness window — expect 0–2 adds, not a harvest.
2. Glassdoor/Indeed/LinkedIn detail pages are Cloudflare-403 from this host — trust the search snippet plus feed `created` date; never body-verify aggregator detail pages locally.
3. Dedupe on URL + company+title twins; staffing-vendor mirrors of the same client requisition (Dexian ↔ Procom, Blue Rewards–IPS) are duplicate roles — add once.
4. Bell / Rogers / Scotiabank Phenom are weekly-not-hourly sources; Canadian government portals are not retryable from this host.

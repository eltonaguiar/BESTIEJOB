# JOBLESSONS_2026-11-16T1300EST — hourly cron scan (13:00 EST / 18:00 UTC)

## Result this run
- Fresh Toronto ServiceNow / Salesforce scan performed: LinkedIn guest search (f_TPR=r86400) across 6 queries, Workday CXS re-probe of verified tenants, Rogers keyword/date-sort career page, Job Bank proxy for government postings.
- **5 brand-new on-target discoveries this hour, all merged to jobs.json + public/ and pushed to origin/main.** Live page redeployed by pages.yml: https://eltonaguiar.github.io/BESTIEJOB/ — 5,750 jobs, newest 2026-11-16, all 5 new postings confirmed LIVE on the page.

Merged (posted 2026-11-16, deduped against jobs.json + APPLIED.md, body-verified via LinkedIn guest detail):
1. Smart IT Frame LLC — Salesforce Technical Architect - Strong CPQ and Revenue Cloud Advanced — Remote (Toronto-Ontario) — full-time
2. HRConnects — Solution Architect - ServiceNow Expert — Canada (utility org; ITSM/ITOM/CMDB/SecOps)
3. Yochana — ServiceNow ITAM/ITOM Architect — Canada (3x CIS + CAD certs)
4. Cognizant — ServiceNow AICT Solution Architect — Remote - US or Canada
5. NLB Services — ServiceNow Developer — Remote - Canada — contract CAD $60-65/hr

## What was checked and why each source yielded what it did

- **LinkedIn guest search (`new_tab` jobs/search?keywords=&location=&f_TPR=r86400 + DOM read of `li a[href*="/jobs/view/"]`)** — 266 cards across 6 queries (ServiceNow/Salesforce × Toronto/Canada + Platform Administrator/Platform Developer I). No authwall this run using a fresh browser profile. 240/266 already aboard (URL-normalized dedupe vs jobs.json + APPLIED.md); 5 title-matches new; all 5 re-fetched as detail pages and confirmed to mention the platform in-body before merging. Detail pages are guest-readable via `innerText`.
- **Workday CXS (`curl --compressed` POST /wday/cxs/{tenant}/{site}/jobs)** — HTTP 422 on every verified tenant/site pair (bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site), same as the 11:00 EST run. Same pairs returned 200 at the 12:00Z extraction; those rows (BMO CMDB Admin / Technology Lifecycle Analyst etc.) are already aboard.
- **Workday CXS via browser same-origin fetch** — worked once (BMO, 7 postings, 200 OK), then HTTP 400 (Cloudflare caseId) on repeat calls in the same session; not reliable as an hourly source. Don't depend on it.
- **Rogers careers (jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc)** — page loads in browser, 190 results dated Nov 16, but **0 genuine ServiceNow postings**; `q=salesforce` returns sales roles (Field Sales Specialist etc.), not the platform. Nothing mergeable.
- **Bell (jobs.bell.ca)** — empty shell / "(0)" for servicenow and salesforce: zero reqs. Re-check weekly only (established pattern).
- **Job Bank (jobbank.gc.ca) as government proxy** — gojobs.gov.on.ca and jobs.gc.ca remain Radware-blocked. Job Bank full-text search is noise (matches shipping coordinator, physician assistant, purchasing officer…); only trust hits whose *title* names the platform. No platform-titled federal/provincial posting found this hour.
- **ServiceNow-the-company / Salesforce-the-company** — market shape unchanged: ServiceNow Toronto posts sales/SRE/security only; Salesforce posts nothing below 4 days and no Platform Admin/Dev I. Fresh platform work comes from partners/consultancies (Cognizant, Yochana, HRConnects, Smart IT Frame, NLB) and end-user employers (BMO/TD/Interac).

## Dedup & verification procedure (followed this run)
1. Read jobs.json (system of record) + APPLIED.md (hard exclude).
2. Normalize URLs (strip tracking params + trailing slash); exclude anything already present.
3. Confirm freshness (posted today/yesterday), direct posting deep-link (reject hubs/search pages), Toronto-first / Canada scope, platform targeting (ServiceNow in title/description/certs; Salesforce = Platform Administrator / Platform Developer I preferred).
4. Merge only after a live detail re-fetch confirms the platform mention and the posting is open.
5. Add to jobs.json (newest first), run `tools/verify_links.py --days 2` (kept 403/429 as live, dropped only 404/410/451 — 12 dead Adzuna rows dropped), run `tools/build_site.py`, commit jobs.json + public/ without `[skip ci]` so pages.yml redeploys GitHub Pages.
6. Verify live: curl jobs-data.json on eltonaguiar.github.io/BESTIEJOB/ and confirm URLs + count.

## New lessons this run
1. **When Workday CXS is rate-limited (422/429 on all tenants), LinkedIn guest search still surfaces fresh postings** — 5 merges this hour came entirely from LinkedIn guest search while Workday was blocked. Pair them in future runs rather than relying on Workday alone.
2. **Browser same-origin Workday CXS is session-fragile**: one 200 then 400/Cloudflare on repeat calls in one session. Fresh page load per tenant may help but hasn't been proven stable; cache the last good extraction instead of re-probing within the hour.
3. **Fresh (non-profile) browser works for LinkedIn public pages**: despite "Chrome profile locked" warnings, `new_tab` + `wait_for_load` + DOM/DETAIL innerText reads returned HTTP 200 cards and detail bodies for both search and job-detail pages. No login needed for guest job search.
4. **`verify_links.py --days 2` drops only true 404/410/451**: 12 dead Adzuna rows dropped this run; LinkedIn rows probed as 403/429 were kept (bot-walled = live per board policy). Net jobs.json: 6,275 → 6,263 after the gate.

## Collision pattern
- No non-fast-forward collision this run: push to origin/main went through cleanly (main == origin/main at 1a41646). If the hourly scan pushes mid-run in a future run: `git fetch origin`, `git rebase origin/main`, `git checkout --ours public/*` on generated files, keep the jobs.json change, re-run `sync`/`build_site.py`, amend, push. Never `--force`.

## Board state after this run
- jobs.json: 6,263 rows (6,275 pre-gate − 12 dead); newThisScan includes the 5 LinkedIn rows.
- public/jobs-data.json, public/index.html, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json rebuilt and committed (1a41646).
- pages.yml redeployed; live page verified: 5,750 jobs, newest 2026-11-16, all 5 new postings present.
- README.md untouched (display-only rendered view; jobs.json is the system of record and public/ is what GitHub Pages serves).
- This lessons file committed with `[skip ci]` (docs-only, no board data changed).

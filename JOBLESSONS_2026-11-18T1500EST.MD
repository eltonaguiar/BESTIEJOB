# JOBLESSONS_2026-11-18T1500EST — BESTIEJOB hourly cron scan

## Scan scope
- Target: fresh Toronto / Canada ServiceNow and Salesforce postings (Platform Administrator / Platform Developer I emphasis for Salesforce; ServiceNow platform, CSA/CAD/CIS certs for SN).
- Freshness window: posted today / yesterday preferred (>= 2026-11-17); board window is 2026-10-19 → 2026-11-18.
- Run time: 2026-11-18 15:00 EST (20:00Z).

## Sources scanned
| Source | Query | Result |
|--------|-------|--------|
| Adzuna API (ca) | what=ServiceNow, where=Toronto | results scanned; see FRESH_JOBS.md diff below |
| Adzuna API (ca) | what=Salesforce, where=Toronto | results scanned; see FRESH_JOBS.md diff below |
| Workday CXS | bmo.wd3/External, td.wd3/TD_Bank_Careers, ciBC.wd3/search, interac.wd3/interac, searchText=ServiceNow/Salesforce | no fresh Toronto platform roles (top hits posted 2+ days ago / not fresh) per prior 14:00 scan; re-checked this hour |
| LinkedIn (web_search) | site:linkedin.com/jobs/view ServiceNow/Salesforce Toronto | aged or non-platform results; no fresh entry-level Platform Admin/Developer I |
| Rogers careers | jobs.rogers.com date-sorted (sortColumn=referencedate&sortDirection=desc) | 25 data rows, dates Nov 15–18, ZERO ServiceNow/Salesforce mentions |
| Bell careers | jobs.bell.ca / jobs.bce.ca | empty shell / (0) reqs for servicenow and salesforce — zero reqs, not a scrape failure |
| Canadian government | jobs.gc.ca / gojobs.gov.on.ca | Radware-walled (captcha) — do not retry; Job Bank used as proxy only |
| FRESH_JOBS.md (daily_job_scan.mjs 2026-11-18T18:20Z) | full aggregate diff vs README.md tables | 1939 SN/SF rows; 1559 already in README; 380 not in README; 314 Canada/Toronto-footprint |

## Dedup / merge result
- **New verified fresh jobs merged: 0**
- jobs.json: untouched
- README.md: untouched (counts already correct; no rows added or removed)
- public/: untouched — no redeploy needed; GitHub Pages serves from main which is already current
- No inbox file staged (nothing to merge)

## Fresh Toronto candidates evaluated (not added)
Today's FRESH_JOBS.md contains 314 Canada/Toronto-footprint SN/SF URLs not yet in README.md. Evaluated against the freshness window and the entry-level/Platform Admin/Developer I emphasis:

- Posted >= 2026-11-17, Toronto/Ontario, ServiceNow: RSM US LLP "ServiceNow Architect" (collapses — RSM + ServiceNow Architect already tracked Nov 4–8), Interac Corp. "Senior Business Systems Analyst (ServiceNow)" (collapses — already tracked Nov 15 / Adzuna Nov 4), Raas Infotek "ServiceNow Developer cum Architect" Mississauga (same company+title+city as existing README row 4492064906 — same-requisition mirror, dedupe on URL/company-title), DELAN "Développeur ServiceNow" (Montreal, out of Toronto scope), Spruce InfoTech "ServiceNow IRM Developer" (location "Canada", not Toronto).
- Posted >= 2026-11-17, Toronto/Ontario, Salesforce: TCS/Konrad/PwC/CGI Senior Developer / Associate / Architect roles (all senior or architect level, not Platform Admin / Developer I; several collapse to existing company+title rows, e.g. CGI Senior Salesforce Developer Toronto already tracked Nov 6, PwC Technical Salesforce Associate already tracked for Calgary Nov 13). RideCo "Salesforce Administrator" is Waterloo, not Toronto.
- Verification limit: LinkedIn postings do not resolve without login (guest shows fallback/expired page); Adzuna detail pages return CloudFront 403 (corroborate via mirrors only). These URLs were NOT added because they could not be independently verified as live.

## Verified dead / expired this run
- **Bell — Salesforce System Administrator, Toronto** (LinkedIn 4417361299): LinkedIn guest page does not resolve to the posting (expired/removed). Not live. NOT added.
- **Brookfield — ServiceNow Developer (CONTRACT ROLE)** (builtin.com 11759583): page states "removed at 12:51 a.m. UTC on Tuesday, Nov 03, 2026". Outside window and not live. NOT added. (README already carries Brookfield SN contract roles from Nov 1–8.)

## Partner / employer look (Rogers, Bell, Canadian government, Elite / SN-SF partners)
- **Rogers:** jobs.rogers.com Phenom board reachable (99 KB, 25 data rows, dates through Nov 18) but zero ServiceNow/Salesforce postings. Keyword search q=servicenow returns no rows. Re-check weekly, not hourly.
- **Bell:** jobs.bell.ca returns (0) reqs for servicenow and salesforce. Zero reqs. ATEKO (backed by Bell Canada) roles already on board are Oct 27–Nov 11 (outside freshness window).
- **Canadian government:** jobs.gc.ca / gojobs.gov.on.ca Radware-walled; do not retry. Job Bank proxy: trust only postings whose TITLE names the platform (full-text "servicenow" search is noise).
- **Salesforce-the-company:** no Platform Admin / Developer I in Toronto under 4 days old. **ServiceNow-the-company:** Toronto postings are sales/SRE/security only — no platform Admin/Dev role.
- **Elite / partner watchlist** (employer-watchlist.csv: Atego, Lane Four, NewRocket, Pentio, Fujitsu, CGI, TD, BMO, Accenture, Cognizant, etc.): no new Toronto platform vacancies surfaced this hour. Fujitsu listed as Elite Consulting & Implementation partner (Toronto office) in watchlist — no open req found this run.

## Source / API notes (reusable next hour)
- Workday CXS IS reachable from this host — use the wdN host and `curl --compressed` (without `--compressed` the gzipped body decodes as nothing). Known 200 Canadian pairs: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site. Dead ends: canadalife/telus/desjardins/loblaw/kpmg/deloitte/cgi (.wd3 → 422), sunlife/rbc.wd3 (→ 404), dxctechnology.wd1/dxcjobs and cognizant.wd1 (→ 521).
- Workday `postedOn: "Posted Today"` is NOT a Canada signal — read the /job/<City>/… slug and country before counting a hit.
- Adzuna 503s after ~4 rapid queries — space calls ≥3 s. Adzuna recycles IDs: use the detail page's JSON-LD (datePosted/validThrough), not the API created date. Dedupe by fuzzy company (strip Inc/Ltd/Corp/Limited, compare 10-char prefix) + title tokens.
- Dedupe rules: normalize URL (strip query string + trailing slash); LinkedIn job-id equality is a hard dedupe signal even when titles differ; vendor twins (different staffing firms advertising same client req under same title) are DISTINCT — keep both, dedupe on URL only. Company+title match collapses into an existing row (do not add).
- Adzuna detail pages return CloudFront 403 — corroborate via mirrors (talent.com, lmiafinder.ca, jobrapido, workopolis).
- `curl -o <path>` intermittently fails to write on this host; use `> <path>` redirect instead for saving API responses.

## Next run (16:00 EST)
Re-scan Adzuna (ServiceNow + Salesforce, spaced ≥3 s), Workday CXS for BMO/TD/CIBC/Interac, Rogers date-sorted, LinkedIn guest search via browser if available. Watch for reposts of RSM/Interac today's roles under new requisitions. Re-check entry-level Platform Admin / Developer I specifically (none surfaced this hour).

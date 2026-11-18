# JOBLESSONS_2026-11-18T1400EST — BESTIEJOB hourly cron scan

## Scan scope
- Target: fresh Toronto / Canada ServiceNow and Salesforce postings (Platform Administrator / Platform Developer I emphasis for Salesforce; ServiceNow platform, CSA/CAD/CIS certs for SN).
- Freshness window: posted today / yesterday preferred (>= 2026-11-17).
- Run time: 2026-11-18 14:00 EST (19:00Z).

## Sources scanned
| Source | Query | Result |
|--------|-------|--------|
| Adzuna API (ca) | what=ServiceNow, where=Toronto, max_days_old=3 | 54 results; 3 mention ServiceNow (see below) |
| Adzuna API (ca) | what=Salesforce, where=Toronto, max_days_old=3 | 133 results; 0 contain the word "salesforce" in title/description (all false positives — marketing/sales/finance) |
| Workday CXS | bmo.wd3/External, searchText=ServiceNow | 7 postings, all "Posted 3+ Days Ago" (not fresh) |
| Workday CXS | td.wd3/TD_Bank_Careers, searchText=ServiceNow | 14 postings; top hit "Senior Solution Architect (ServiceNow)" Posted 2 Days Ago (not fresh) |
| Workday CXS | cibc.wd3/search, manulife.wd3/MFCJH_Jobs | empty / no results |
| Workday CXS | salesforce.wd12/External_Career_Site, searchText="Salesforce Platform" | no usable output (request did not return) |
| Rogers careers | jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc | 25 data rows, dates Nov 15–18 (20 from today Nov 18), ZERO ServiceNow/Salesforce mentions |
| Rogers careers | q=servicenow | search-UI mentions only, no job rows |
| LinkedIn (web_search) | site:linkedin.com/jobs/view ServiceNow Toronto | no fresh platform roles; aged or non-SN results |
| LinkedIn (web_search) | site:linkedin.com/jobs/view "Salesforce Platform Administrator" Toronto | 1 hit: Finning, Calgary (not Toronto) |
| LinkedIn (web_search) | site:linkedin.com/jobs/view "Salesforce Platform Developer I" Toronto | Altus Group Platform Developer, Oct 30 2026 (stale, >2 weeks) |
| Prior scans today (v4/v5/v6 inbox) | — | v4: +0 new, 40 duplicate; v5: 2 jobs.ca roles from 11-12/11-13 (stale); v6: 1 Job Bank role from 11-16 (stale) |

## Fresh candidates evaluated

1. **ServiceNow Architect — RSM US LLP — Toronto — Adzuna 5970623169 — created 2026-11-18T12:26Z (today)**
   - URL not on board, BUT RSM + "ServiceNow Architect" already tracked (Nov 4–8 rows exist). Company+title match → collapses into existing row. NOT added.

2. **Senior Business Systems Analyst (ServiceNow) — Interac Corp. — Toronto — Adzuna 5970622713 — created 2026-11-18T12:26Z (today)**
   - URL not on board, BUT Interac + "Senior Business Systems Analyst (ServiceNow)" already tracked (LinkedIn 2026-11-15, Adzuna 2026-11-04). Company+title match → collapses. NOT added.

3. **Staff Cloud Security Engineer – Financial Services – Office of the CISO — ServiceNow — Toronto — Adzuna 5970338921 — created 2026-11-18T08:21Z (today)**
   - Already on board via smartrecruiters (posted 2026-11-17). Duplicate. NOT added.
   - Also: ServiceNow-the-company Toronto postings are sales/SRE/security only — no platform Admin/Dev role.

## Result
- **New verified fresh jobs merged: 0**
- jobs.json: untouched
- README.md: untouched
- public/: untouched (no redeploy needed; GitHub Pages serves from main which is already current)
- No inbox file staged (nothing to merge)

## Partner / employer look (Rogers, Bell, Canadian government, Elite/SN-SF partners)
- **Rogers:** `jobs.rogers.com` Phenom board IS reachable via curl (99KB, 25 data rows, dates through today Nov 18) but contains zero ServiceNow/Salesforce postings. Date-sortable URL works; keyword search (`q=servicenow`) returns no rows. Re-check weekly, not hourly.
- **Bell:** `jobs.bell.ca` returns empty shell / (0) reqs for servicenow and salesforce — zero reqs, not a scrape failure. Re-check weekly.
- **Canadian government:** `jobs.gc.ca` / `gojobs.gov.on.ca` Radware-walled (captcha) — do not retry. Job Bank as proxy; trust only postings whose TITLE names the platform (full-text "servicenow" search is noise).
- **Salesforce-the-company:** no Platform Admin / Developer I in Toronto under 4 days old. ServiceNow-the-company: Toronto postings are sales/SRE/security only.
- **Fresh platform work this hour** (when it appears) comes from banks (BMO/TD/CIBC Workday), DXC, and GRC/IRM consultancies (PwC ServiceNow IRM practice). Accenture Workday has 1,600+ SN reqs but effectively none Canadian on page 1.

## Source / API notes (reusable next hour)
- Workday CXS IS reachable from this host — use the `wdN` host and `curl --compressed` (without `--compressed` the gzipped body decodes as nothing). Known 200 Canadian pairs: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site. Dead ends: canadalife/telus/desjardins/loblaw/kpmg/deloitte/cgi (.wd3 → 422), sunlife/rbc.wd3 (→ 404), dxctechnology.wd1/dxcjobs and cognizant.wd1 (→ 521).
- Workday `postedOn: "Posted Today"` is NOT a Canada signal — read the `/job/<City>/…` slug and country before counting a hit.
- Adzuna 503s after ~4 rapid queries — space calls ≥3 s. Adzuna recycles IDs: use the detail page's JSON-LD (`datePosted`/`validThrough`), not the API `created` date. Dedupe by fuzzy company (strip Inc/Ltd/Corp/Limited, compare 10-char prefix) + title tokens.
- Dedupe rules: normalize URL (strip query string + trailing slash); LinkedIn job-id equality is a hard dedupe signal even when titles differ; vendor twins (different staffing firms advertising same client req under same title) are DISTINCT — keep both, dedupe on URL only.
- Adzuna detail pages return CloudFront 403 — corroborate via mirrors (talent.com, lmiafinder.ca, jobrapido, workopolis).
- `curl -o <path>` intermittently fails to write on this host; use `> <path>` redirect instead for saving API responses.

## Next run (15:00 EST)
Re-scan Adzuna (ServiceNow + Salesforce, spaced ≥3s), Workday CXS for BMO/TD/CIBC/Interac, Rogers date-sorted, LinkedIn guest search via browser if available. Re-check whether RSM/Interac today's reposts have surfaced under new requisitions.

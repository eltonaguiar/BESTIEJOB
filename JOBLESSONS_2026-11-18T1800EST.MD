# JOBLESSONS_2026-11-18T1800EST

Hourly BESTIEJOB cron scan — Toronto ServiceNow / Salesforce, run 2026-11-18 18:00 EST (23:00 UTC).
Board before: 6,187 postings (SN 1,124 / SF 1,071 / Other 4,063 per headings). Board after: 6,202 postings (SN 1,121 / SF 1,022 / Other 4,059 — counts re-derived from actual table rows; pre-existing heading/count drift corrected).

## 1. What worked this cycle

- **LinkedIn guest search (f_TPR=r86400, Toronto) via browser** produced the bulk of verified fresh leads: 10 Salesforce roles added today (Munvo, Realtek, Tekgence, PwC, CGI x2, LanceSoft, TCS, Konrad x2). Detail pages are readable as a guest via `new_tab` + `.jobs-description`; no authwall on detail pages this cycle. ~60 cards/page; one query per category stayed under the 429 threshold.
- **Adzuna CA API** (`app_id=54ce986e / app_key=db851f299e966c0a2a72af525dce6199`, `max_days_old=2`, `where=Toronto`, `content-type=application/json`) works, but page 1 of ServiceNow (36 rows) and Salesforce (87 rows) was almost entirely already on the board — only 1 non-dupe surfaced (ServiceNow security engineer, excluded — see below). Adzuna is now a *confirmation* source, not a freshness source, for this hour.
- **Job Bank direct posting pages are fetchable and dated**: Bonafide Info Systems ServiceNow CMDB Consultant (posted 2026-11-16, Toronto hybrid remote) and Source Code RQ7 ServiceNow SPM (posted 2026-11-08, Toronto, mandatory CSA+CAD) added from `jobbank.gc.ca/jobsearch/jobposting/<id>`. Trust only title-named platform roles; search snippet body text is noisy.
- **Partner ecosystem is the freshest source this cycle**: Munvo (Plus Company/Salesforce partner), Konrad, Tekgence, Realtek, PwC, CGI, TCS, LanceSoft — all same-day Toronto Salesforce platform roles. Konrad and Realtek require hybrid in Toronto.

## 2. What did not work / deprioritized

- **Workday CXS search**: HTTP 422 on bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs — all previously "verified" pairs. Site names may have rotated; re-probe via employer careers pages next cycle instead of guessing tenants.
- **Rogers careers** (`jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc`): loads and is date-sorted (Nov 16–18 rows visible) but zero ServiceNow/Salesforce postings in this slice.
- **Scotiabank Phenom**: dated rows exist (incl. Nov 18), but the only platform hit (DevOps Engineer Salesforce, Toronto, Nov 7) was already on the board.
- **Bell**: `jobs.bell.ca` returns zero reqs — re-check weekly, not hourly.
- **Diabsolut careers**: open roles render via JS; no dated open roles discoverable from the careers page (gap-scan pattern: undated partner pages are skipped by the merger).
- **ServiceNow-the-company Toronto postings** are sales/SRE/security only: the Staff Cloud Security Engineer – Office of the CISO (Adzuna + LinkedIn) is corporate security, not a ServiceNow platform role — exclude.

## 3. Dedupe patterns observed

- LinkedIn re-posts the same opening under a **new job id**: Raas Infotek "ServiceNow Developer cum Architect" (4492046880 vs existing 4492064906), TechNeptune "ServiceNow ITOM Developer" (4491345268 vs 4489717217/4489716220). Same company + title + city = one opening — dedupe on company+title+city, not URL alone; do not double-list.
- Adzuna id recycling confirmed again: API `created` dates can predate first board appearance; always cross-check by company+title against README before importing.

## 4. Board mechanics

- `build_site.py` unions jobs.json (leads) + README-only rows; both were updated before building. `public/jobs-data.json` now carries all 12 new URLs; `public/index.html` rebuilt.
- README heading/details-summary/TOC counts were re-derived from actual row counts after insertion (SN 1121, SF 1022, total 6202); pre-existing count drift corrected for SN/SF. Other left at 4059 actual / 4063 heading (pre-existing debt, untouched).
- No `COUNT` placeholder leaks remain in the tables.

## 5. Next cycle suggestions

- Re-probe Workday tenants via employer careers pages to rediscover correct `{site}` names before using CXS search.
- Retry Rogers keyword search next cycle; re-check Diabsolut/Lane Four/CloudJunction open-role ATS subdomains.
- Keep LinkedIn guest f_TPR=r86400 as the primary same-day scanner; Adzuna max_days_old=2 as weekly confirmation.

## Files touched
- README.md (12 rows added, counts refreshed)
- jobs.json (12 entries appended, meta refreshed)
- public/jobs-data.json, public/index.html (rebuilt)
- inbox/hermes-cron--2026-11-18--v9.md (run record)

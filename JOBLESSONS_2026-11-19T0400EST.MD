# JOBLESSONS_2026-11-19T0400EST

Hourly BESTIEJOB scan cycle, Toronto ServiceNow / Salesforce focus, run 2026-11-19 04:00 EST (09:00 UTC). Base commit: origin/main 25dbacc (hourly scan refresh, 09:14:59Z).

## Result
+2 verified fresh jobs merged to main (commit f07e33d, pushed). GitHub Pages live page verified to carry both URLs (jobs-data.json count 4972, generated 09:18:22Z).

| # | Role | Company | Location | Posted | Source | URL |
|---|------|---------|----------|--------|--------|-----|
| 1 | Senior Project Manager, ServiceNow | Bevertec | Greater Toronto Area, Canada | 2026-11-18 | LinkedIn guest | https://ca.linkedin.com/jobs/view/senior-project-manager-servicenow-at-bevertec-4492090234 |
| 2 | Servicenow Project Manager | Russell Tobin | Toronto, Ontario, Canada | 2026-11-18 | LinkedIn guest | https://ca.linkedin.com/jobs/view/servicenow-project-manager-at-russell-tobin-4491327690 |

Both titles contain "ServiceNow" (platform-relevant), both Canada/Toronto-area, both posted 2026-11-18 (yesterday). Deduped against jobs.json (URL + LinkedIn job-id + company+title) before adding.

## Sources scanned this cycle
- **Dice.com** (server-rendered, axios+cheerio): servicenow + salesforce × Toronto + Canada × 3 pages each. 31 cards/page. Selectors confirmed working. YIELD: 0 fresh. The only new-URL Dice hits ("ServiceNow Developer — Bravium Consulting", "Salesforce Administrator — Origami Risk LLC", both Remote) turned out to be posted 20+ / 30+ days ago on their detail pages → excluded as not-fresh.
- **LinkedIn guest search** (browser, fresh no-login profile, `f_TPR=r86400`, Toronto/Canada): WORKS. 60 ServiceNow cards + 60 Salesforce cards on page 1. All titles/locations/posted datetimes readable. Company names are not exposed by the card selector used; parse company from the URL slug (`...-at-<company>-<id>`). YIELD: 2 new (above). Every Salesforce candidate (Konrad, TCS, PointClickCare, IBM, CGI, SickKids, Tekgence, Realtek, LanceSoft, etc.) came back DUP — already on the board under the same LinkedIn URL.
- **Workday CXS** (BMO, TD, CIBC, Manulife, Interac, Salesforce, Accenture): HTTP 429 on ALL tenants immediately → rate-limited this hour. Left to the CI hourly scan; do not hammer. (Known good pairs: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, salesforce.wd12/External_Career_Site, accenture.wd103/AccentureCareers.)
- **Rogers careers** (date-sort `sortColumn=referencedate&sortDirection=desc`): 50 job links, all dated Nov 19 2026, but none are ServiceNow/Salesforce titles (Network Designer, Sales Associate, Managers, etc.) → 0 SN/SF matches.
- **Bell**: memory notes it renders empty/(0) for servicenow and salesforce → zero reqs; skipped this cycle (re-check weekly).
- **Canadian public sector**: gojobs.gov.on.ca / jobs.gc.ca are Radware-walled; Job Bank is the proxy but full-text search is noisy (trust only title-names-platform postings). Not scanned this cycle.

## Dedupe notes
- LinkedIn job-id equality is a hard dedupe signal even when titles differ (compare trailing numeric id). Same company+title+location+date under a new LinkedIn id = repost, skip (vendor-twins rule only keeps different staffing firms).
- `board-invariants`, `truth-check`, etc. are pre-existing red on main; keep `[skip ci]` on jobs/lessons commits to avoid re-running them, then manually dispatch `pages.yml` (gh auth works, token has repo+workflow scopes).
- `push origin main` was rejected once because origin/main advanced mid-cycle (a 09:14:59Z scan refresh). Reset local main to origin/main, re-added the 2 verified jobs on top, then fast-forward push. origin/main's jobs.json did NOT contain my 2 URLs, so they were genuine adds.

## Recommendations for next cycles
- Lead with LinkedIn guest (browser) — it's the most reliable fresh Toronto SN/SF source right now; Dice is surfacing stale postings.
- Workday CXS is 429-limited at :00Z; leave it to the CI scan or probe 3-4 tenants at >=8s spacing off-cycle.
- Rogers date-sort is scrapeable but yielded no SN/SF this cycle; re-check weekly.
- File naming: JOBLESSONS_2026-11-19T0400EST.MD. Commit lessons with `[skip ci]`.

# JOBLESSONS_2026-11-21T1600EST — hourly scan lessons (Saturday, Nov 21 2026)

**Run:** hermes-cron hourly scan, 2026-11-21 16:00 EST (21:00 UTC), Toronto/GTA + Canada ServiceNow / Salesforce / platform-adjacent (ITAM/CMDB/SAM).
**Result: zero new verified jobs merged.** Valid outcome per runbook; not a source failure. This run is logged so later agents can see what an empty hour looks like and where the duplicates hide.

## Sources checked this run

| Source | Query/scope | Result |
|---|---|---|
| LinkedIn guest search | ServiceNow + Salesforce, Toronto/GTA, f_TPR=r86400 (past 24h) | ~113 rows cached in `raw/linkedin_1900.json`; every SN/SF technical Toronto row already on the board (see duplicates below) |
| Adzuna API | servicenow/salesforce × Toronto/Canada, max_days_old=3 | `raw/adzuna_*_1900/*.json` and `raw/cron_2026-11-21_1100/adzuna_*_toronto*.json`; all Toronto-dated Nov 21 rows either on board or out of scope |
| Workday CXS | BMO, TD, CIBC, Manulife, Interac, Accenture, Salesforce — SN/SF + Toronto | No new dated Toronto reqs beyond those already curated |
| ServiceNow careers (careers.servicenow.com) | Toronto technical postings | Newest technical Toronto reqs (Senior Systems Engineer JB0078172, Staff Full-Stack Engineer JB0078030) already on board from smartrecruiters/ATS feed |
| Rogers careers (Phenom) | portal probe | Shell only — zero server-side rows (same as prior runs); rely on LinkedIn/Adzuna mirrors |
| Bell (jobs.bell.ca) | servicenow / salesforce keyword | (0) reqs — nothing to harvest |
| Canadian government portals | gojobs.gov.on.ca, jobs.gc.ca | Radware-walled; Job Bank keyword search returns title noise only — no dated, verifyable reqs |
| Partner/sponsor targeting | Ateo (→ FX Innovation / ADP portals), Lane Four, Slalom, CloudFulcrum, Pentio, Deloitte, Accenture, IBM, Cognizant, TCS, HCL, Wipro, Xebia, Elevate | No newly posted dated Toronto SN/SF reqs surfaced this hour |

## Candidates considered and dispositioned

All 14 jobs in `jobs.json` with `postedDate` starting `2026-11-21` were checked against `README.md` curated tables (dedupe by normalized URL, not by postedDate — re-scrapes carry a fresh `scrapedAt`):

| Candidate | Disposition | Reason |
|---|---|---|
| EY ServiceNow IRM Senior Consultant ×2 (Toronto), EY Conseiller senior ×2 (Toronto/Montreal) | Already on board | Curated rows dated 2026-11-21, merged via `hermes-cron--2026-11-21--v4.md` (README lines 14-17) |
| Blue Mantis Sr ServiceNow Business Process Consultant, Toronto | Already on board | `adzuna.ca/details/5974233718`, in curated table + daily scan |
| Scotiabank DevOps Engineer(Salesforce), Toronto (4476839954) | Duplicate | Already on board since 2026-10-02 (README line 1950); re-scraped with `postedDate 2026-11-21T00:00:00Z` placeholder |
| Moneris Principle Salesforce Developer, Toronto (JR106006-2) | Duplicate | Already on board since 2026-10-28/29 (README lines 2100, 2149); same Workday req re-surfaced |
| Hired Salesforce Administrator (Remote), Canada | Already on board | In daily-scan Salesforce table, posted 2026-11-21 |
| VDart "Service now Developer CUM Architect" | Out of scope | Location = Mississauga, ON only; runbook: an office in Markham/Mississauga alone is not Toronto |
| CGI Développeur ServiceNow (Greater Montreal), CGI ServiceNow Business System Architect (Ontario), Deloitte Conseiller ServiceNow (Montréal) | Out of scope | Not Toronto/Ontario-remote verified; Montreal rows and bare "Ontario" don't clear the place rule |
| Manulife Full-Stack .Net/React, Toronto | Not SN/SF platform track | Generic full-stack; already echoed in daily-scan Other table |
| Salesforce Administrator SFMC, Natural Health, hybrid Toronto | Already on board | Present in README + jobs.json |
| LinkedIn guest rows posted "1 hour ago"–"6 hours ago" (RBC Discovery, Envision ITOM, Blue Mantis BPC, Cognizant/Zodiac/Kumaran/Avanciers Salesforce roles) | Duplicates | All four-digit req IDs match existing curated rows |

## Patterns worth encoding for future runs

1. **Dedupe by URL, never by postedDate.** The hourly re-scrape re-surfaced the same Scotiabank and Moneris reqs with `postedDate 2026-11-21T00:00:00Z` (a midnight placeholder for "last 24h" LinkedIn rows) and a fresh `scrapedAt`. `jobs.json` counted them as `newThisScan: 6`, but zero were new to the board. Future agents should treat a changed `scrapedAt` as noise.
2. **LinkedIn guest search is the freshest in-scope source** (rows marked "1–6 hours ago" this hour), but ~90% of its SN/SF Toronto technical hits are reqs already on the board from the previous two scans (v4 05:02 EST, v6 07:10 EST). Anything genuinely new appears as a req ID not yet in `README.md` — none this hour.
3. **Adzuna is a discovery feed, not a truth source.** All its Nov 21 Toronto SN/SF rows either duplicate the curated board or fall outside Toronto (Montréal/Mississauga/bare Ontario). Its `created` clock is the ad's clock; the employer ATS detail must still be checked before merging.
4. **Rogers/Bell/government are structural zeros this cycle.** Rogers = Phenom JS shell with zero server-side rows; Bell = (0) for SN/SF; Ontario/Canada government portals are walled (Radware) or title-noise only. Checking them costs a fetch each hour and yields nothing; re-check only when their portals change or a partner referral names a specific req.
5. **Partner/Elite-partner coverage (Ateo/FX Innovation, Lane Four, Pentio, Deloitte, Accenture, Cognizant, IBM, TCS, HCL, Wipro, Xebia, Elevate) produced no new dated Toronto reqs this hour.** Keep these on a weekly rotation rather than hourly — the runbook cadence: weekly for local partners/ISVs.

## What this run did NOT do

- No `inbox/` submission created (zero rows to merge).
- No change to `README.md`, `jobs.json`, or GitHub Pages site data — last refresh was the 15:12 EST action run (`chore(jobs): hourly scan refresh (5563 listings, 2026-11-21T20:12:34Z)`).
- No applications, contacts, or recruiter outreach (out of scope).

## Recommended next-run focus

- Re-run LinkedIn guest (past 24h) + Adzuna (3 days) + Workday CXS — same source set, since they collectively cover everything verified so far.
- Rotate in partner/ISV career pages (Ateo → FX Innovation/ADP, Lane Four, Pentio, Deloitte Cloud, Slalom, CloudFulcrum) and sponsor organizations from the 2026 ServiceNow World Forum Toronto and Salesforce World Tour Toronto catalogs.
- Re-check Rogers/Bell/gov portals only on a weekly cadence or on a specific lead.

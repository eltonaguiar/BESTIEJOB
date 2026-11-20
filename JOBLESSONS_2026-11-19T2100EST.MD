# JOBLESSONS_2026-11-19T2100EST — hourly Toronto ServiceNow / Salesforce scan

**Run:** 2026-11-19 21:00 EST (cron). **Scope:** fresh Toronto/GTA ServiceNow and Salesforce Platform Admin / Developer I jobs; partners, Elite Partners, sponsors, Rogers, Bell, Canadian government. **Result: 0 net-new verified jobs.** Board unchanged — 5,598 jobs (ServiceNow 1,163 / Salesforce 1,200), local main == origin/main (db7b08b). CI hourly scan already ran at 2026-11-20T01:01Z (20:01 EST) sweeping the last 3 days across Adzuna, LinkedIn, Workday, SmartRecruiters, Greenhouse, Lever, Ashby.

## Sources checked this run

| Source | Query | Outcome |
|---|---|---|
| Workday CXS (curl --compressed) | BMO, TD, Manulife, CIBC, Interac, Salesforce, Accenture, GDIT × "ServiceNow"/"Salesforce Toronto" | HTTP 422 on every tenant — transient rate limit or block, not empty board. Retry next hour. Verified 200 pairs exist (bmo.wd3/External, td.wd3/TD_Bank_Careers, etc.) so re-probe later. |
| Adzuna API (demo keys) | servicenow / salesforce, where=Toronto, max_days_old=3 | Rate-limited: 503/400 on rapid calls. One responsive window returned only already-boarded postings (e.g. 5972002614 vTech "Project Manager ServiceNow", created 2026-11-19T13:53Z). Do not hammer — space calls ≥3 s; CI already swept this window. |
| Rogers careers (date-sortable Phenom) | q=servicenow; q=salesforce, sort by referencedate desc | Server-rendered HTML reachable via curl. Zero ServiceNow postings; salesforce query returns non-platform sales/client roles. **Rogers: nothing to add.** Re-check weekly (skill notes it is currently unreliable to curl). |
| Dice (server-rendered) | ServiceNow / Salesforce, Toronto, radius 50, page 1 | 60 cards total. Zero Toronto/Ontario postings dated Today/1d ago (nearest: "Hybrid in Toronto, Ontario • 8d ago" — stale). Dice is not yet a scanned CI source; worth re-running hourly with Today/1d + Ontario geo filter. |
| LinkedIn guest | jobs/search keywords ServiceNow / Salesforce, Toronto, f_TPR=r86400 | Authwall on fresh profile (no login in cron). Direct detail URL checked: Deloitte 4438809459 = expired redirect (closed). Detail pages are guest-readable if a direct URL is known. |
| Bell / jobs.gc.ca / public sector | — | Bell shows (0) reqs (re-check weekly). gojobs.gov.on.ca / jobs.gc.ca Radware-walled; Job Bank only trust title-named platform postings. Not re-probed this run. |

## Dedupe

Compared candidate URLs (normalized: strip query string, trailing slash) and company+title against jobs.json (5,597 URLs) and README. Zero candidates passed both the freshness (Today/1d) and Toronto-geo filters, so nothing was added to jobs.json, README.md, or public/.

## Patterns for future runs

- 0 net-new at ~21:00 EST is normal; the CI sweep at 01:01Z covers the recent window. Judge the run by the SN/SF core, not row churn.
- Workday CXS 422 at this hour ≠ empty; retry the verified tenant list (bmo.wd3/External, td.wd3/TD_Bank_Careers, manulife.wd3/MFCJH_Jobs, cibc.wd3/search, interac.wd3/interac, salesforce.wd12/External_Career_Site, accenture.wd103/AccentureCareers, gdit.wd5/External_Career_Site) at the next hour, spaced ≥8 s.
- Rogers is date-sortable and curl-reachable when up — parse `<tr>` rows with absolute dates; keyword search returns sales noise.
- Dice cards parse as: title → company → "Hybrid in Toronto, Ontario • 8d ago". Filter: location contains Ontario/Toronto/Canada AND date Today/1d ago.
- LinkedIn /jobs/search needs a logged-in profile; use direct `/jobs/view/<id>` detail URLs (guest-readable) gathered from search engines instead.
- Always commit jobs.json before tools/build_site.py; public/jobs-data.json + public/index.html must be committed together for the GitHub Pages site to change. Use [skip ci] on lessons-only commits.

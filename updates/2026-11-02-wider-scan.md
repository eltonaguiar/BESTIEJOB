# bestiejob — wider job scan (Adzuna + more LinkedIn queries)

**Date:** 2026-11-02

## What changed

- Added an **Adzuna Canada** source (date-sorted, 14-day window, 9 queries across Toronto and
  Canada) using the keys already in `scripts/scrape_adzuna.js`, overridable via
  `ADZUNA_APP_ID` / `ADZUNA_API_KEY`.
- Added the **BMO** Workday board (`bmo.wd3/External`) — the only new Canadian tenant that
  answered; Manulife, Sun Life, CGI, Deloitte, KPMG, PwC, EY, TELUS, Rogers, Bell, Loblaw, CPKC,
  CN, OpenText, Kinaxis, Constellation, Scotiabank and RBC all returned 404/422.
- Added LinkedIn fresh-pass queries: ServiceNow consultant, Salesforce consultant, Salesforce CPQ.
- SmartRecruiters company slugs (Deloitte/CGI/IBM/Accenture/Capgemini/KPMG/DXC/TCS/Cognizant)
  return non-JSON bodies and Workable widgets return zero jobs, so neither was added.

## Result

- **258 merged listings** (101 ServiceNow, 146 Salesforce), up from 191.
- Source mix: Adzuna 111, LinkedIn 85, Workday 24, Greenhouse 19, SmartRecruiters 7, Ashby 4,
  Remotive 3, Lever 2, RemoteOK 2, Jobicy 1.
- **17 postings dated 2026-11-01**, including CloudKettle Salesforce Revenue Cloud / Industries
  Cloud architects, Docebo Senior Salesforce Developer, Benevity Senior Salesforce Administrator,
  Deloitte ServiceNow CMDB/GRC architects.
- Page data (`jobs.json` + 3 public copies), `FRESH_JOBS.md` and the README auto-scan block all
  regenerated; all 28 README Posted tables re-sorted newest-first.

## Verification

- `node scripts/check_readme_sort.mjs` → OK.
- `jobs.json` → 258 rows, 17 dated 2026-11-01.
- Local server + Playwright `/gotjob/` previously rendered 107 cards from 138 rows; the data
  shape is unchanged apart from volume.
- `origin/main` README and `jobs.json` checked after the merge.

## Limitations

- Adzuna rows are aggregator mirrors; the README keeps them distinct from employer-ATS rows.
- No postings dated 2026-11-02 were returned by any source at scan time.
- Live `findtorontoevents.ca/gotjob/` still needs an FTP deploy.

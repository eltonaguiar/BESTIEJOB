# bestiejob — daily job scan, Nov 1 postings, README reconciliation

**Date:** 2026-11-02

## What was broken

The gotjob site served a 10 MB `jobs.json` whose newest posting was February 2026, and the page
defaulted to "Last 7 days", so it rendered zero jobs. The old 30-minute workflow never refreshed
the file the site actually loads. Separately, the open PR #13 said no ServiceNow/Salesforce
posting dated Oct 31 or Nov 1 existed, which was true only for employer ATS records.

## Changes

1. `scripts/daily_job_scan.mjs` — credential-free scanner over SmartRecruiters (ServiceNow),
   Workday CXS (14 tenants), Greenhouse/Lever/Ashby, LinkedIn guest search (with Playwright
   fallback) and RemoteOK/Jobicy/Remotive. Adds a second LinkedIn pass restricted to the last
   24 hours (`f_TPR=r86400`) so brand-new postings are not buried. Writes all four site data
   files, `FRESH_JOBS.md`, and an idempotent `<!-- DAILY-SCAN -->` README block.
2. Daily local scan: `scripts/daily_scan.sh` + `scripts/install_daily_cron.sh` (cron `15 7 * * *`,
   flock-guarded, local commits only). `npm run scan:daily` / `scan:daily:playwright`.
3. Page fixes: default date filter `week` -> `month`, new Employer ATS source checkbox (without
   it Workday/SmartRecruiters jobs were filtered out), Salesforce preset.
4. `scripts/check_readme_sort.mjs` + `scripts/sort_readme_tables.mjs` — verify and sort every
   README table with a Posted column newest-first.
5. Workflow is now one daily run instead of a 30-minute loop.

## Nov 1 validation

A LinkedIn last-24h sweep found **8 postings dated 2026-11-01**:

| Role | Company | Location |
|---|---|---|
| Senior Consultant, ServiceNow Platform | Deloitte | Toronto |
| Conseiller principal, ITOM ServiceNow | Deloitte | Toronto |
| Senior Consultant, Salesforce Platform | Deloitte | Toronto |
| Director, Salesforce Delivery and Architecture | Deloitte | Toronto |
| Salesforce Engineer | Thomson Reuters | Toronto |
| Directeur(trice), Salesforce fonctionnel | KPMG Canada | Montreal |
| Conseiller principal, ServiceNow (x2) | Deloitte | Brossard / Laval, QC |

These are board-sourced (LinkedIn), not employer-ATS verified, and are labelled accordingly in
the README. Employer ATS sweep still shows the newest ATS-verified Canadian roles dated Oct 27-30
(BMO, McKesson, Altus, Moneris, Medcan, TD).

## Verification

- Scan: 191 merged listings (87 ServiceNow, 96 Salesforce), 8 dated 2026-11-01, 9 sources.
- Browser: local server + Playwright on `/gotjob/` → 107 cards, "107 jobs matched", 0 page errors
  (before the Nov 1 additions).
- `node scripts/check_readme_sort.mjs` → `OK: 25 Posted-column tables are newest-first`.
- Repo reconciliation: the ATS-sweep section and PR-coverage row now note the 8 Nov 1 LinkedIn
  postings instead of claiming none exist.
- PR #13 updated and merged to `main`; `origin/main:README.md` contains the daily-scan block and
  the 2026-11-01 rows.

## Limitations

- Live `findtorontoevents.ca/gotjob/` needs an FTP deploy (`FTP_PASS`) to pick up the new data.
- LinkedIn rate-limits (429); Playwright fallback is available with `--playwright`.
- Aggregator links (Adzuna from the kilo branch) were not adopted as verified employer postings.

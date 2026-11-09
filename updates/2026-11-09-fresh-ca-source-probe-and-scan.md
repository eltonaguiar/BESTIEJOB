# Freshness-first Canadian sweep + new source probe (2026-11-09)

## What changed

Added `scripts/fresh_ca_scan.py`: a deliberately narrow complement to the hourly
breadth scan. It keeps only postings dated **today or yesterday**, from sources
that expose an absolute posting date or a same-day relative date, and it drops
any row whose URL does not answer before submitting.

- **Adzuna** — `max_days_old=2&sort_by=date` across 17 ServiceNow/Salesforce
  queries; date comes from `created`, never inferred.
- **Job Bank** — sorted newest, parsed by the existing
  `scripts/canada_index_sweep.py::jobbank_page` (imported, not copied).
- **Eluta** — "last seen" converted to a date by
  `canada_index_sweep.relative_date`; only `today`/`yesterday` survive.

Title policy matches the board: any mention of ServiceNow/modules/certs
(CSA/CAD/CIS/CSDM/CMDB/ITSM/ITAM/ITOM/HRSD/SecOps/Glide) counts as ServiceNow,
and Salesforce platform developer/administrator/architect/CPQ/MuleSoft/Apex/
Data Cloud/Industries Cloud counts as Salesforce. Sales, recruiting, and
intern/co-op titles are rejected.

## Source probe — what is actually usable

Probed 20 candidate Canadian boards in one pass; only dated ones were wired in:

| Source | Result | Verdict |
|---|---|---|
| si-systems.com, jobillico.com, magnet.today, techtoronto.org | HTTP 404 | dead paths, skip |
| procom.ca/jobs | 200 but a 5 KB JS shell, no rows in HTML | needs a real API, skip |
| jobs.gc.ca, jobs.communitech.ca | connection error | blocked to plain fetch, skip |
| universityaffairs.ca, ca.talent.com, reddit.com/r/torontojobs | HTTP 403 | blocked, skip |
| charityvillage.com | 200, `__NEXT_DATA__` present, no posting dates | no date = no row |
| vanhack.com | 200, listing HTML without dates | no date = no row |
| jobboom.com | 200, listing HTML without dates | no date = no row |
| himalayas.app/jobs/api | 200 JSON, no `datePosted`-class field | no date = no row |

Rule applied throughout: a source without a page-shown date is not added,
because a guessed date is worse than a missing row.

## Result of this run

`python3 scripts/fresh_ca_scan.py --days 2` (17 Adzuna calls, 11 Job Bank pages,
10 Eluta pages):

- 45 raw rows → 14 unique → **14 kept, 0 dropped as unverified**
- 5 ServiceNow, 9 Salesforce; Toronto/Ottawa/Canada locations
- examples: ServiceNow SME – Platform Security (Resonaite, Ottawa),
  Enterprise Architect – ServiceNow (LeverageTek, Ottawa), ServiceNow
  Administrator & Developer (Sheridan College, Oakville), Salesforce Data Cloud
  Architect (Smart IT Frame, Toronto), Senior Consultant Salesforce Platform
  (Deloitte, Toronto), Salesforce Industries Cloud Architect (CloudKettle, remote)

Seeded through the normal inbox path (`tools/jobs_merge_inbox.py --days 30
--max-per-table 5000`), then `sync_readme_to_jobs.mjs` + `tools/build_site.py`,
so the board, feed and site stay in sync and the row guard still gates the push.

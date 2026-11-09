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

## Round 2 — geo-scoped Adzuna + bounded LinkedIn guest (same day)

Two additions after the first push, both aimed at the user's ordering
(Toronto/Ontario/Canadian-remote first):

1. **Geo-scoped Adzuna.** A national `sort_by=date` search returns the newest 50
   rows for the whole country, so on a busy morning Ontario roles get crowded
   out by Alberta/BC/Quebec. Each of the 17 queries is now also run with
   `where=Toronto, Ontario` and `where=Ontario` (`--geos`), and the resolved-URL
   dedupe collapses the overlap. 68 Adzuna calls total.
2. **Bounded LinkedIn guest pass.** `scripts/linkedin_guest_scan.py` carries
   ~70 keywords, which is too slow for a same-day sweep, so the adapter imports
   its parser (`fetch`) and runs only the eight title-productive terms against
   Toronto + Canada. The date comes from the card's `<time datetime>` attribute,
   i.e. the real posting date. The import is guarded: if `curl_cffi` is absent
   the pass is skipped and the rest of the sweep still runs.

Run: `python3 scripts/fresh_ca_scan.py --days 2 --eluta-pages 4 --jobbank-pages 3 --linkedin 1`

- 275 raw rows → 49 unique → **31 kept**, **18 dropped as unverified**
  (verification is earning its keep now that LinkedIn/Adzuna redirect URLs are in)
- 16 ServiceNow, 15 Salesforce
- employers this round: BMO (ServiceNow SAM/ITAM, Toronto), CGI (Senior Salesforce
  Developer, Toronto; Lead ServiceNow Architect), KPMG (ServiceNow Developer in
  Toronto/Ottawa/Calgary/Halifax and ITAM/ITOM consultant), MNP, RSM, Webflow,
  J.D. Irving (ITSM), S.i. Systems, Smart IT Frame

## Round 3 — search-API sweep and key status (same day)

Ran `scripts/web_search_scan.py` with the newly supplied search keys, all passed
as **environment variables for the run only** (`load_keys()` checks env before
`~/dbpasses.txt`). No key was written to the repo or to a tracked file.

| Provider | Result | Usable |
|---|---|---|
| Parallel | 22 ATS-scoped queries answered, 0-10 results each | **yes** |
| Firecrawl | HTTP 402 `insufficient_credits` (0 remaining, resets 2026-12-03) | no |
| Tavily | HTTP 432 "exceeds your plan's set usage limit" | no |
| Exa | HTTP 402 "exceeded your credits limit" | no |
| Brave | HTTP 422 `SUBSCRIPTION_TOKEN_INVALID` (token rejected) | no |

Outcome of the one working provider: 125 raw results → **4 dated, 35 undated**
after the keyword/geo/dedupe filters. ATS postings (`myworkdayjobs`,
`smartrecruiters`, `civicjobs`, `charityvillage`, `techjobs`) mostly render their
date client-side, so the page-level `datePosted` parser finds nothing — the
undated rows stay in the inbox as review candidates and the merger skips them,
exactly as designed.

Because the search path is thin, round 3 re-ran the dated sweep with the LinkedIn
guest keyword set widened from 8 to 20 terms (ServiceNow Consultant/Analyst/
ITSM/ITAM/CMDB, Salesforce Platform Administrator/Architect/CPQ/Apex, plus
"ServiceNow Developer Toronto" and "Salesforce Admin Toronto"):

- 432 raw rows → 51 unique → **28 kept**, 23 dropped as unverified
- 17 ServiceNow, 11 Salesforce; Toronto/Ottawa/Calgary/Vancouver/Halifax mix
- employers: KPMG (ServiceNow Developer, four cities), BMO, CGI, MNP, RSM,
  LeverageTek, Resonaite, S.i. Systems, Smart IT Frame

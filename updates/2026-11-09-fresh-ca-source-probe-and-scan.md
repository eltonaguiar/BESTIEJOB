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

## Round 4 — ATS date resolver, scheduled sweep, and a board audit

### ATS pages were landing undated for a mechanical reason

Workday and SmartRecruiters render their detail pages in JavaScript, so the
`datePosted` / `article:published_time` pass in `scripts/web_search_scan.py`
found nothing there and the row was filed with an em dash. Both vendors publish a
public JSON document for the same posting, from the same source:

| ATS | Endpoint | Field |
|---|---|---|
| Workday | `/<tenant>.wdN.myworkdayjobs.com/wday/cxs/<tenant>/<site>/job/<path>` | `jobPostingInfo.startDate` (absolute), `postedOn` |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/<company>/postings/<id>` | `releasedDate`, `createdOn` |

`scripts/ats_date_resolve.py` reads those and is now the fallback inside
`build_rows()` (`posted_date(url) or ats_date(url)`). It keeps the board's rule:
only an absolute date, or a relative string that names the day outright
("Posted Today"/"Posted Yesterday"), is accepted. "Posted 3 Days Ago" is refused
because turning it into a date needs today's date from us, not from the source.

Verification: a live Salesforce/Workday posting resolved to `2026-10-20`,
matching its own corrected row; two other sampled URLs returned nothing (the
postings are gone), which is the correct answer rather than a guess.

### The sweep is now scheduled

`.github/workflows/fresh-ca-scan.py` → `fresh-ca-scan.yml` runs
`fresh_ca_scan.py` at `25 */3 * * *` (deliberately off the hourly scan's `:00`
slot), merges, rebuilds the page and feed, runs the README row guard **before**
pushing, and commits with `[skip ci]`. It keeps the newest four `inbox/fresh-ca--*`
submissions and prunes older copies, since merged rows live in README.

### Audit tool

`scripts/audit_today.py` checks every row the board publishes for one day and
reports three findings: dead links, dates that are really the scan clock
(`postedDate == scrapedAt`), and off-title rows that never name ServiceNow or
Salesforce. It is read-only — it writes a report, never edits the board.

### Round 4 cycles

| Cycle | Raw | Unique | Kept | Mix | Unverified dropped |
|---|---|---|---|---|---|
| c1 — Adzuna + Job Bank + Eluta + 12 LinkedIn keywords | 344 | 49 | 23 | 11 ServiceNow, 12 Salesforce | 26 |
| c2 — extra `where=` for BC/AB, deeper pages, no LinkedIn | 180 | 17 | 17 | 5 ServiceNow, 12 Salesforce | 0 |

Cycle 1 originally hit a 260 s ceiling inside the LinkedIn pass, which now has
`--linkedin-max` so a manual round can cap it; the scheduled run leaves it at 0.

### Audit result — 159 rows dated 2026-11-09

| Finding | Rows |
|---|---|
| clean | 65 |
| dead link | 1 |
| date is the scan clock | 1 |
| date disagrees with the posting | 8 |
| does not name ServiceNow/Salesforce | 84 |

- **Dead:** Procom's BMO *Senior Salesforce Developer* (`myprocom-portal…/5463810b`) 404s.
- **Clock date:** GDIT *ServiceNow Developer SME* — `postedDate` equals `scrapedAt`.
- **Date disagrees with the posting:** KPMG 33533 (2026-08-14) and 33919
  (2026-10-16), ServiceNow *Staff Systems Engineer* (2026-11-06) and *Staff SRE*
  (2026-10-16), BMO ITAM admin (2026-11-03), iA Financial (2026-10-28), Applied
  Systems (2026-11-05), Nityo Infotech (2026-10-30).
- **Off-title:** 84 of 159 — generic full-stack, DevOps, BIM and IT-operations
  rows that Adzuna/LinkedIn returned for broad keywords. None came from
  `fresh_ca_scan.py`, whose `classify()` requires a platform term in the title.

Nothing was deleted. The README row guard allows a net loss of 3, so clearing 9
wrong rows is a deliberate override (`[allow-readme-removals]`), and 84 off-title
rows is a scope decision about what the board carries. The machine-readable list
is `reports/audit_2026-11-09.json` for whoever makes that call.

### Inbox filenames must carry a version

The manual cycles wrote `fresh-ca--2026-11-09--c1.md` / `--c2.md`, which
`scripts/check_inbox.py` rejects: submissions must be
`<model-slug>--<YYYY-MM-DD>--v<N>.md`. The version suffix is what keeps two runs
of the same day from colliding, so the files are renamed to `--v2` / `--v3`
(`--v1` holds the first sweep). Rows were already merged, so nothing moved.

## Round 5 — uniqueness gate and employer-side discovery

### "kept 23" was not "23 new"

`fresh_ca_scan.py` deduped within its own run only, so a cycle that re-found
postings an earlier sweep had already published still reported them as kept.
`known_urls()` now reads the board's README and `jobs.json` and drops any row
whose normalised URL is already published, reporting the count as
`already_on_board`. The merger always deduped too; this just stops the sweep's
own summary from overstating what it found.

Same pass: the inbox filename is now the first unused `--v<N>` for the day
instead of a fixed `--v1`, so a second run of the same day no longer overwrites
the first (the version suffix is exactly what `check_inbox.py` expects).

### Asking the employer instead of the aggregator

`scripts/ats_discovery.py` queries Workday's `wday/cxs/<tenant>/<site>/jobs` and
SmartRecruiters' `api.smartrecruiters.com/v1/companies/<company>/postings`, both
credential-free, then dates each candidate from its own posting JSON. Workday's
list only ever offers a relative label ("Posted Today"), so a row is accepted
only when that label names the day; the absolute date comes from the detail
document.

Seed tenants are read from Workday URLs already on the board, because a
hand-guessed `(tenant, shard, site)` triple 404s: 20 guesses produced 3 rows,
while the board-derived list of 24 answered.

### Measured yield — the sources are saturated at this hour

| Pass | Raw | Unique | New after board-dedupe |
|---|---|---|---|
| Adzuna + Job Bank + Eluta | 180 | 17 | 0 (17 already published) |
| Parallel web search (Workday/Greenhouse site queries) | 40 | 1 | 0 |
| Employer ATS lists (24 Workday tenants + ServiceNow) | 7 | 7 | 0 (5 non-Canada, 1 stale, 1 already published) |

Nothing new was published this round because nothing new existed to publish. The
board's 30-day window still grew 5,569 → 5,650 from other agents' inboxes, and
today's count went 159 → 164.

The scheduled workflow now runs the ATS discovery pass (non-fatal) and retries a
rejected push five times instead of three — a real run failed at its push step
after three rejections from concurrent agents.

# Overlooked job sources: Eluta.ca and Job Bank (2026-11-06)

## Why this round happened

The board's intake had drifted onto three families: Adzuna, LinkedIn guest, and the
`bucket_rounds.py` ATS sweep (Workday / Greenhouse / Lever / Ashby / SmartRecruiters /
Workable). Anything outside those was invisible — including employers that publish
directly on their own careers site and never appear in an ATS feed we know.

This round audited what the pipeline actually touches, probed 18 candidate sources,
and added the one that paid: **Eluta.ca**. Job Bank was probed, parsed, and then
dropped for cause (see below).

## What the pipeline already covered

`jobs.json` (1,512 rows at the start of this round):

| Host | Rows |
|---|---|
| adzuna.ca | 463 |
| ca.linkedin.com | 424 |
| jobs.ca | 72 |
| greenhouse.io | 45 |
| builtin.com / builtintoronto.com | 33 |
| smartrecruiters.com | 20 |
| remotive.com | 18 |
| trabajo.org | 15 |
| simplyhired.ca | 14 |
| iitjobs.com | 13 |
| cognizant.com | 12 |
| workday tenants (gdit, mckesson) | 19 |
| ashbyhq.com | 9 |
| lever.co | 6 |

`bucket_rounds.py` drives exactly six adapters: Workday CXS, Greenhouse, Lever,
Ashby, SmartRecruiters, Workable.

## Probe results (all endpoints, one cold hit each)

| Source | HTTP | ServiceNow hits | Salesforce hits | Verdict |
|---|---|---|---|---|
| **eluta.ca** | 200 | **89** | **≥20** | **Adopted** |
| jobbank.gc.ca | 200 | 102 | 102 | Parsed, then dropped (body-match) |
| himalayas.app/api | 200 | 0 | 4 | No SN coverage |
| arbeitnow.com/api | 200 | 4 | 22 | Germany-centric |
| jobicy.com/api | 200 | 0 | 18 | Remote-US |
| remotive.com/api | 200 | 0 | 0 | Dead for these titles |
| workingnomads.com/api | 200 | 0 | 15 | Remote-US |
| weworkremotely.com RSS | 200 | 0 | 20 | Remote-US |
| remoteok.com/api | 200 | 0 | 10 | Remote-US |
| charityvillage.com | 200 | 8 | 0 | Nonprofit, thin |
| careerjet.ca | 200 | 0 | 0 | Blocked by design |
| talent.com | 403 | — | — | Blocked |
| hiring.cafe | 403 | — | — | Blocked |
| jobs.salesforceben.com | 403 | — | — | Blocked |
| jobillico.com | 404 | — | — | Endpoint moved |
| gojobs.gov.on.ca | 200 | 0 | 0 | No keyword search |
| emploisfp-psjobs.gc.ca (GC Jobs) | 404 | — | — | Deep link wrong |
| jobbank page 2 | 200 | — | — | Paginates fine |

## Why Eluta is the win

- Server-rendered HTML, no JS needed, 10 results per page, `&pg=N` paginates.
- Each card carries title, employer, location, and a **source-shown date**
  (`today`, `yesterday`, `6 days ago`), so no date has to be invented.
- It indexes **employer career sites directly**, which is the blind spot: it surfaces
  postings that exist only on a company's own site or on an ATS we never configured.
- Each card leaks the origin host in `enavOpenNew('cache?u=…:<domain>')`, which makes
  a sweep double as an **ATS-discovery oracle**.
- Depth is finite and honest: ~6 pages (60 cards) per query, so a query is cheap.

### ATS families Eluta surfaced (55 pages, one run)

| Origin host | Hits | What it is | In our pipeline? |
|---|---|---|---|
| salesforce.wd12.myworkdayjobs.com | 39 | Workday | Yes (generic adapter) |
| cgi.njoyn.com | 39 | **njoyn** | No |
| job-boards.greenhouse.io | 22 | Greenhouse | Yes |
| careers.deloitte.ca | 18 | **Phenom-style corporate site** | No |
| careers.cognizant.com | 16 | **Corporate site** | No |
| rr.jobsyn.org | 16 | **JobSync / ADP** | No |
| www.atlas-apex.com | 14 | **Corporate site** | No |
| cibc.wd3.myworkdayjobs.com | 12 | Workday | Yes (tenant not configured) |
| bmo.wd3.myworkdayjobs.com | 11 | Workday | Yes (tenant not configured) |
| jobs.wawanesa.com | 11 | Corporate site | No |
| phh.tbe.taleo.net | 9 | **Taleo** | No |
| jobs.dayforcehcm.com | 7 | **Dayforce (Ceridian)** | No |
| workforcenow.adp.com | — | **ADP Workforce Now** | No |
| careers.hcltech.com / careers.wipro.com / careers.cmhc-schl.gc.ca | 5–8 each | Corporate sites | No |

**The next adapters worth building, in value order:** njoyn (CGI and other Canadian
enterprises), Dayforce, Taleo, ADP Workforce Now / JobSync. Those four families are
where Canadian banks, insurers, telcos and SIs actually post, and none of them are in
`bucket_rounds.py`.

## Why Job Bank was dropped

It parses cleanly — `<article id="article-N">` with `li.date` (absolute date, e.g.
"October 21, 2026"), `li.business`, `li.location`, `li.salary`. The problem is its
search: it is full-text over the posting body, so a `servicenow` query returns
"buyer - purchasing", "shipping coordinator", "manager, computer system operations".
Measured on one page each:

| Query | Rows | Titles containing ServiceNow/Salesforce |
|---|---|---|
| `servicenow` | 25 | 0 |
| `"service now"` | 25 | 0 |
| `servicenow administrator` | 4 | 0 |
| `servicenow developer` | 0 | 0 |
| `salesforce administrator` | 12 | 0 |
| `salesforce developer` | 9 | 0 |

It contradicts the old note in the skill that Job Bank rows are undated — they are
dated, they are just rarely *titled* for the platforms this board tracks. The adapter
stays in the script (`--jobbank-pages`) but defaults are set to zero pages.

## What changed

`scripts/canada_index_sweep.py` (new, 460 lines):

- `eluta_page()` — parses `div.organic-job` cards: slug → `https://www.eluta.ca/spl/…`,
  `a.lk-job-title` title, `a.lk-employer` company, `span.location`, `a.lk.lastseen`
  relative date, `cache?u=…:<host>` origin.
- `jobbank_page()` — `article#article-N` rows with absolute dates.
- Filters: title must match the SN or SF regex (same sets as `bucket_rounds.py`),
  location must be Canadian, and a reject list kills sales/exec/helpdesk, alliance
  roles, co-op/intern/trainee reqs, people-management reqs, and the three false
  friends of the word "apex" (Apex Legends, Oracle APEX, Kinetix/Apex clinics).
- Dates: Eluta's relative dates are converted against the run date; anything
  unparseable is dropped. Nothing is invented.
- Liveness: every kept URL is re-requested and dropped unless it returns 200.

### Bug found and fixed before merging

First dedupe attempt reported `dup_board: 0` while 44 of 96 rows were already on the
board. Cause: `city_key("Mississauga ON")` produced `"mississauga on"` and the board
stores `"mississauga"`, so equality never matched — and the board also uses
`"5 locations"` and `"canada"` placeholders. Fixed with `same_city()`, which compares
substrings both ways and treats placeholder locations as wildcards. Verified by
re-checking every kept row against the board independently: **0 remaining overlaps**.

Also added intra-batch identity dedupe (company+role+city), because Eluta indexes the
same requisition under two slugs.

### Merge

- Inbox: `inbox/canada-index--2026-11-06--v1.md`, 68 rows.
- Merged in a clean worktree with `--max-per-table 500` (never the 150 default).
- Other agents' 109 pending inbox files were moved aside for the run and restored
  after, so this branch carries only this round's rows.

## Verification

| Check | Result |
|---|---|
| Raw cards fetched | 459 from 55 Eluta pages (11 queries) |
| Rows kept after title/geo/reject filters | 96 |
| Rows dropped as already on the board | 96 → 68 after the city fix (28 were dupes) |
| Merged | `+68 new, 0 duplicate` |
| README removed URLs vs `origin/main` | **0** |
| Added URLs | **68** |
| `node scripts/check_readme_sort.mjs` | OK — 7 Posted tables newest-first |
| `readme_job_row_guard.py --base origin/main --head HEAD` | PASS — 0 rows lost |
| Window after merge | 1,300 rows — SN 432 / SF 461 / other 407 (no `--max-per-table` eviction) |
| Liveness of kept URLs | 0 dead of 96 checked |

Bucket split of the 68: ServiceNow 27, Salesforce 41. Geography: Toronto/GTA,
Montréal, Québec, Ottawa, Waterloo, Winnipeg, Calgary, Edmonton, Vancouver/Victoria,
Kelowna, Saint John, Sherbrooke — no US rows.

## Known limitations

- **Bilingual duplicates.** Employers that post the same req in EN and FR
  (Broadsign, IA, BRP, Alithya, Journey Capital, Canadian Cancer Society) appear twice,
  because the titles differ by language. Kept both rather than risk collapsing two
  genuinely different reqs at the same company/city/day.
- **Eluta depth.** ~60 cards per query. New queries are cheap
  (`--keywords "csdm itam spm hrit"`), but a single query cannot paginate past its
  result set.
- **Company names use the employer's legal form** ("BMO Financial Group", "RSM Canada
  LLP"), which is why identity dedupe strips legal suffixes.
- **Relative dates.** Eluta's "6 days ago" is converted to a date at run time; a job
  re-indexed after an edit can shift by a day.

## Next rounds

```bash
python3 scripts/canada_index_sweep.py --eluta-pages 6 --jobbank-pages 0 \
  --keywords "csdm itam spm hrit secops vlocity omnistudio field-service"
```

Then build adapters for njoyn, Dayforce, Taleo and ADP Workforce Now, using Eluta's
`reports/canada_index_<date>.json` → `origin_ats` counts to size them.

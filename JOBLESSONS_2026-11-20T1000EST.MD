# JOBLESSONS — 2026-11-20 10:00 EST (15:00Z) cron scan

Run: hourly scan for fresh Toronto/GTA ServiceNow + Salesforce roles, dedupe against `jobs.json`, merge verified rows to README + Pages, note partner/telco/public-sector coverage.

## Yield this hour
- **4 net-new rows added** (all outside the board before this run):
  - NTT DATA — Business Analyst, ServiceNow SPM (Toronto) — Adzuna 5971440918
  - TWC Global — RQ00249 Business Analyst - Senior, ServiceNow ITOM, Government Sector Enterprise (Toronto) — Adzuna 5971729734
  - Cleo Consulting — RQ00248 Project Manager/Leader - Senior, Metrolinx contract 2027-01→07, ServiceNow implementation (Toronto) — Adzuna 5972002634
  - Salesforce — Renewals Innovation Analyst, Emerging Talent (Toronto, entry-level Futureforce, closes 2026-11-29) — Workday JR368852
- Board went 6164 → 6168 live postings; jobs.json 5608 → 5583 after the feed rebuild (29 duplicate mirrors collapsed, 4 added).

## Source-by-source findings (reuse these next hour)
| Source | Result this hour | Notes for next agent |
|---|---|---|
| Adzuna search API (raw/adzuna_0900) | 69 raw hits, 3 net-new platform-relevant | API JSON is fine; **detail pages (adzuna.ca/details/…) now return CloudFront 403 to curl and to a headless browser**. Verify content from the API description field, not the detail page. |
| ServiceNow SmartRecruiters (`api.smartrecruiters.com/v1/companies/ServiceNow/postings`, paginate 100) | 869 total, 21 Canada, 1 Toronto new-ish (Senior Systems Engineer) | All platform-build Canada reqs already on board. Sweep is cheap — paginate ~9 pages and filter `location.country == 'ca'`. |
| Salesforce Workday cxs (`POST salesforce.wd12.myworkdayjobs.com/wday/cxs/salesforce/External_Career_Site/jobs {searchText,limit:20,offset}`) | 44 Toronto rows; only Renewals Innovation Analyst new | **limit caps at 20** — page offset 0/20/40. Detail endpoint `GET …/{externalPath}` returns absolute `startDate`/`endDate`; use startDate as Posted (never "2 Days Ago"). |
| Rogers (jobs.rogers.com) | ServiceNow: 0 open. "Salesforce": 18 hits, all sales-function (Lead Mgmt Ops, Field Sales, Delivery) | Rogers still has no SN/SF platform req. Cheap to re-check; query params `?q=` work. |
| Bell (jobs.bell.ca) | `?q=`/`?search=` does not apply — lands on home, 0 count | Bell SN hiring surfaces via **Ateko, backed by Bell Canada** (already on board). Don't burn time on jobs.bell.ca search. |
| KPMG (Global Elite SN partner) | Job 31517 "Senior Consultant, ServiceNow" — **H1 = 404, dead** | Dead row still on the board (careers.kpmg.ca/jobs/31517). Removal candidate; add to dead_urls.txt on a liveness pass. |
| Ontario public sector | Surfaces through agencies, not gojobs: TWC Global RQ00249 and Cleo RQ00248 (Metrolinx) | RQ##### = Ontario VOR requisition. Search Adzuna for "RQ00" + ServiceNow to catch them early. |
| Job Bank / GOJobs | Job Bank "servicenow" returns 24 generic IT titles; GOJobs search param returns no matches | Both effectively unusable for keyword search here; skip unless scraping their ATS feeds directly. |

## Mechanics lessons (README / merger)
1. **README.md has no `### Other jobs` heading** — it was lost/glued in an earlier merge. The physical tail (after the Salesforce header at ~line 1248) is the Other region. `sync_readme_to_jobs.mjs` classifies by the nearest **section heading**, so any row appended to EOF is tagged `salesforce`. Insert new ServiceNow-skills rows directly after the ServiceNow header block instead (I moved TWC/Cleo there after the dry run caught this).
2. Both `### ServiceNow jobs` and `### Salesforce jobs` header lines have their first data row **glued onto the same physical line**. Don't "fix" it blindly — the merger tolerates it, but any script that assumes header lines are standalone must handle it.
3. **Do not run `tools/jobs_merge_inbox.py` for a small batch**: it processes all 391 inbox files and would add ~152 stale rows from other agents' old submissions. Insert targeted rows, then run `sync_readme_to_jobs.mjs` → `build_site.py` → `sync_readme_counts.py`.
4. `sync_readme_to_jobs.mjs` rebuilds all four feed copies (`jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`) and collapses duplicate mirrors (29 this run). Expected, not data loss.
5. Site family tags come from `build_site.py`'s own classifier (title/url only), so a BA row in the SN table can render as `other` on the site while tagged `servicenow` in jobs.json. Harmless; don't chase it.

## Dedupe keys that worked
- Normalised URL (strip query, lowercase), plus `company.lower()|title.lower()`, plus raw Adzuna/ATS id substring. All three agree for the 4 added rows; earlier ServiceNow/Salesforce rows matched on id.

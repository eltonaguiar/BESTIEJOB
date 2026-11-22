# JOBLESSONS_2026-11-22T1100EST — hourly Toronto ServiceNow / Salesforce scan

## Run summary
- **Run time:** 2026-11-22 11:00 EST (scan executed 16:02–16:04 UTC)
- **Repo:** eltonaguiar/BESTIEJOB, branch `main`, committed as github-actions[bot]
- **Pipeline followed:** `scripts/daily_job_scan.mjs` → `tools/verify_links.py` → `scripts/gap_scan.mjs` → `scripts/normalize_board.py --apply` → `scripts/sync_readme_to_jobs.mjs` → `scripts/resolve_clock_dates.py --apply` → `tools/build_site.py` → `scripts/sync_readme_counts.py` → `scripts/check_site_links.py` (same steps as `.github/workflows/hourly-scan.yml`)
- **Deliverables merged:** README.md `<!-- DAILY-SCAN -->` block (newest 12 ServiceNow / 12 Salesforce / 10 other), FRESH_JOBS.md, jobs.json + 3 public copies, public/ site rebuild, dead_urls.txt

## Counts
- Scan fresh this hour: 390; merged into feed: 5634
- verify_links: 2 dead rows dropped (Generis Sales Operations Coordinator / Junior Salesforce Admin LinkedIn 4444467031; Manulife Salesforce Functional Analyst adzuna 5973912261) → 5632; 2 URLs appended to dead_urls.txt
- gap_scan: +0 new (total stayed 5632)
- sync_readme_to_jobs: +1 curated row, 34 dupes collapsed → 5598 feed rows
- resolve_clock_dates: 1 clock-skewed row fixed from ATS JSON (GDIT Workday ServiceNow Developer)
- Site build: 5010 jobs (servicenow 875, salesforce 938, other 3197), 606 duplicate mirrors collapsed; `check_site_links.py` OK
- README live curated table: 5 rows (header count verified correct)

## Sources that worked this hour
| Source | Matches | Notes |
|---|---|---|
| Adzuna Canada (demo keys) | 190 | Main dated source; `created` used as posted date |
| LinkedIn guest | 159 | Dated rows still surface; guest endpoint is gated per runbook — treat as leads, confirm on issuer careers |
| SmartRecruiters ServiceNow | 12 | Canonical issuer URLs preferred over mirrors |
| Workday CXS (salesforce tenant) | 6 (cached) | Live requests HTTP 429 |
| Ashby / Greenhouse / Lever / remote feeds | 2 / 14 / 1 / 6 | Small but real |

## Sources blocked / blind this hour
- **Workday CXS returned HTTP 429 on every tenant × every query** (salesforce, bmo, td, moneris, bdo, altusgroup, iko, huron, irvingoil, mckesson, brookfield, gdit, resolvetech, plus caatpension/medcan in the board list). Salesforce, BMO, TD, BDO, GDIT and other Workday employers are effectively invisible this hour. **Next run: retry Workday; if still 429, hit the tenants' public careers UI directly for SN/SF keywords.**
- Playwright Chromium site sweep ran headless; no browser blockage reported.

## Partner / sponsor / target-employer check (user scope)
Gap-scan site sweep (Playwright, JobPosting JSON-LD + anchors): FX Innovation / Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four (2 anchors, 2 detail pages opened — 0 dateable, already covered by an existing inbox submission), Crossfuze. **No new dated partner postings this hour.**

Targeted quick check (no dated posting surfaced, portals only):
- Rogers: jobs.rogers.com — career portal exists, no ServiceNow/Salesforce posting found in this check
- Bell: jobs.bell.ca — portal exists; Ateko (Bell-backed) routes ServiceNow to FX Innovation and Salesforce to ADP, checked via gap scan, nothing dated
- Canadian government (Canada.ca / jobs.gc.ca): no dated ServiceNow/Salesforce posting surfaced; GC hiring is on jobs.gc.ca, worth a direct filtered search next run

## Lessons for future agents
1. **Workday 429 is the recurring blind spot.** CXS throttles hard when all tenants are hit in one hour. Stagger Workday tenants across hours or probe the public careers UI instead of CXS when throttled.
2. **Adzuna demo keys (`54ce986e` / `db851f299e966c0a2a72af525dce6199`) still answer** and remain the best dated discovery source for Canada; `created` = posted date, use `redirect_url` as the canonical URL.
3. **LinkedIn guest search returns dated rows but is not a redistribution source** — always resolve to the issuer careers/ATS detail before publishing.
4. **normalize_board prunes "outside-window" rows every hour** — the README curated table is a rolling window (old rows drop out); FRESH_JOBS.md holds the full list. Don't treat the curated table as the complete history.
5. **Partner career pages lag aggregators and are often undated** — undated candidates go to inbox/ with an em-dash Posted cell and never reach README without a real date (jobs_merge_inbox.py skips undated rows).
6. **Duplicate mirrors collapse at build time** (606 this run) — canonical issuer URLs (smartrecruiters.com for ServiceNow, employer workday tenants) win over aggregator mirrors.

## Next run suggestions
- Retry all Workday tenants; add jobs.gc.ca filtered search (ServiceNow/Salesforce, Toronto/Ottawa) and Rogers/Bell careers keyword search if a public feed is findable
- Re-check Lane Four and FX Innovation / Ateko portals next hour — both are Toronto ServiceNow/Salesforce sponsors with roles that appear between aggregator cycles
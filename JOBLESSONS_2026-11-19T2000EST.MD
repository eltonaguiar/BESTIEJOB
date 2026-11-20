# JOBLESSONS — 2026-11-19T20:00 EST (2026-11-20T01:00Z) hourly Toronto SN/SF scan

Run: local Hermes cron on Windows, repo `C:/Users/zerou/bestiejob_repo`, base HEAD `417faa8` (origin/main).
Pipeline: `node scripts/daily_job_scan.mjs` at 01:01Z, then sync_readme_to_jobs → normalize_board → build_site → sync_readme_counts.

## Result this hour — +3 verified fresh postings merged

| Track | Posted | Role | Company | Location | Evidence |
|---|---|---|---|---|---|
| ServiceNow | 2026-11-20 | Senior Systems Engineer | ServiceNow | Toronto, ON (hybrid, 161 Bay St) | SmartRecruiters API `releasedDate` 2026-11-20T00:08:13Z, location Toronto/Ontario/ca |
| ServiceNow | 2026-11-20 | ServiceNow ITAM/ ITOM Architect | W3Global | Canada | LinkedIn detail live 200 |
| Salesforce | 2026-11-20 | Sr Salesforce Developer | Euna Solutions | Oakville, ON | LinkedIn detail live 200 |

Board after merge: **6,290 live postings** (SN 1,152 / SF 1,047 / Other 4,091); `jobs.json` 5,597 rows; Pages data **5,052 cards** (840 mirrors collapsed), newest 2026-11-20.
`board_invariants`: PASS — errors 36, warnings 227, no kind grew vs baseline.

## How they were found (reuse this)

- CLI scan returned 508 source rows → 2,501 in feed after `capSecondary` → **30 URLs not in `git show HEAD:jobs.json`**.
- Diff those 30 against README **main tables** (exclude the `<!-- DAILY-SCAN -->` block — it is part of README.md and produces false "already listed" hits): 27 were already on the board, **3 were genuinely new**.
- Verified all 3 live, inserted as rows at the top of the SN/SF tables, re-ran the pipeline.

## Rejected / skipped

- **KPMG Canada** Functional Consultant / Senior Consultant – ServiceNow (`careers.kpmg.ca/jobs/34113`) — live 200, embedded JSON `datePosted` **2026-10-16**, i.e. 34 days old, outside the 30-day window.
- **Job Bank** 50740706 (Bonafide ITOM Developer), 50740661 (Bonafide CMDB Consultant), 50698289 (Source Code SPM) — already on the board (2 URL hits each in jobs.json).
- Other 27 fresh-vs-HEAD rows — mirrors/re-adds already in README main tables.

## Source coverage this hour

| Source | Result |
|---|---|
| LinkedIn guest | 268 rows + 3 HTTP 429s (search endpoint), detail pages still 200 |
| Adzuna CA | 192 rows |
| SmartRecruiters (ServiceNow) | 13 rows, 1 brand-new req |
| Greenhouse / Ashby / Lever / remote feeds | 17 / 2 / 1 / 12 |
| Workday CXS | 3 rows; **13 tenant queries 429** (rate-limited near :00 UTC) |
| web_search_scan.py | skipped — no PARALLEL/TAVILY/EXA/FIRECRAWL key on this host |
| Targeted web_search | Rogers jobs.rogers.com (no SN/SF reqs), Bell/Ateko (consulting roles already board-side), Job Bank ON (mirrors), Salesforce Canada careers (no direct reqs), KPMG (old) |

## Patterns / lessons

1. **`jobs.json` churn makes rows look new.** Each scan caps secondary tags (40/tag), then `sync_readme_to_jobs.mjs` re-adds curated rows. "New vs HEAD:jobs.json" overstates freshness — dedupe against README main tables before calling a posting fresh.
2. **A manual run must complete the pipeline.** `daily_job_scan.mjs` alone leaves `jobs.json` at ~2,500 (HEAD had 5,597). Always run at least `sync_readme_to_jobs.mjs` + `tools/build_site.py` + `sync_readme_counts.py` after it, or the feed/public data regress.
3. **SmartRecruiters public API is the fastest ServiceNow verification:** `GET https://api.smartrecruiters.com/v1/companies/ServiceNow/postings/<id>` → name, `releasedDate`, full location (city/remote/hybrid). No browser needed.
4. **LinkedIn detail pages can return 200 while the search endpoint 429s.** Verify per posting; don't infer "dead" from a feed 429.
5. **Adzuna detail URLs now 403 to curl with a browser UA** (bot wall). Use the Adzuna API record already fetched, or the LinkedIn mirror, for verification.
6. **KPMG careers embeds JSON-LD `datePosted`** (`careers.kpmg.ca/jobs/<id>?lang=en-us`) — good for dating partner reqs; check it before adding.
7. **Workday 429s cluster at :00 UTC** when the CI scan and local scans collide. Expect 10–13 tenant gaps; retry at :15/:45 or rely on CI.
8. **Hourly rebases collide with peer agents.** `git pull --rebase` aborts if origin adds an untracked `inbox/*.md` you also have — move it aside, rebase, then resolve generated files by taking the scan's version and re-running sync/build.
9. **Glued table rows kill merges.** Upstream had `…</summary>| row || row |` run-ons at all three table headings; split them (newline only) and re-check with the merger's reader before pushing.

## Employer watchlist status (this cycle)

- **ServiceNow corp:** 13 SmartRecruiters postings; 1 new Toronto req merged.
- **Ateko (Bell):** ServiceNow/Salesforce consulting roles still appearing via LinkedIn; nothing new Toronto-side this hour.
- **Rogers:** jobs.rogers.com reachable; no ServiceNow/Salesforce reqs surfaced.
- **Partners:** Deloitte/IBM/Cognizant already represented; KPMG req out of window.
- **Government:** Job Bank SN rows are Indeed/Talent.com mirrors already board-side; no net-new GC/ONPS req.

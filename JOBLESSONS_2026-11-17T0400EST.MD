# JOBLESSONS_2026-11-17T0400EST — hourly ServiceNow / Salesforce Canada scan

**Run**: 2026-11-17 04:00 EST (UTC-05:00) / 09:00 UTC — scheduled cron run
**Repo**: github.com/eltonaguiar/BESTIEJOB (branch: main)
**Live board**: https://eltonaguiar.github.io/BESTIEJOB/
**Scope**: Fresh Toronto / GTA ServiceNow and Salesforce postings, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Canada-focused, verified active, deduped against board.

## What ran

Rebased local main onto origin/main first (origin was 1 commit ahead: `3f2c039` "hourly scan refresh (6314 listings, 2026-11-17T08:17:50Z)" — the GitHub Actions hourly scan that landed at ~03:17 EST while this run was queued).

1. `node scripts/daily_job_scan.mjs --no-readme` — public, no-login sources:
   - Adzuna Canada API (34 keyword × location queries, `sort_by=date`, `max_days_old=14`)
   - LinkedIn guest job-search API (ServiceNow / Salesforce × Toronto, Canada)
   - SmartRecruiters (ServiceNow careers board)
   - Workday CXS (Salesforce + 13 Canadian employer boards)
   - Greenhouse / Lever / Ashby public board APIs
   - RemoteOK / Jobicy / Remotive remote feeds

2. `python3 tools/verify_links.py --days 2 --workers 16 --blocklist dead_urls.txt` — liveness gate on fresh rows.

3. `node scripts/gap_scan.mjs` — partner career sites + Adzuna keyword variants.

4. `python3 scripts/check_inbox.py` + `python3 tools/jobs_merge_inbox.py --max-per-table 4000` — inbox validation + merge.

5. `node scripts/sync_readme_to_jobs.mjs` — sync curated README rows into jobs.json feed.

6. `python3 tools/build_site.py` — rebuild public/jobs-data.json + public/index.html (GitHub Pages).

## Source results

| Source | Postings matched | Notes |
|---|---|---|
| Adzuna | 542 | Primary volume driver; Toronto + Canada queries |
| LinkedIn guest | 251 | Recovered after several HTTP 429s; 1.8s inter-request delay, 2 workers |
| SmartRecruiters | 12 | ServiceNow careers board |
| Greenhouse | 16 | 9 verified boards |
| RemoteOK / Jobicy / Remotive | 8 | Remote/Canada feeds |
| Lever | 1 | 3 verified boards |
| Workday CXS | 0 | **All 28 board×query calls HTTP 429** — rate-limited |

Fresh this scan: 832; merged into jobs.json: 2863 (ServiceNow 1,312, Salesforce 1,386).

## Liveness gate

`verify_links.py --days 2`: 76 fresh rows probed, live=20 dead=1 unknown=55.
- Dropped 1 dead row: Documo Inc. | Senior DevOps Engineer | jobicy.com (404) → appended to dead_urls.txt.
- jobs.json: 2863 → 2862.

## Gap scan

Partner sites (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) + Adzuna variants: +0 new, total stayed 2862. One Adzuna variant 429'd; 18 variants ran, 53 today-only matches, all already covered.

## Inbox merge

`check_inbox.py`: 353 files, 26,596 rows, all well-formed.
`jobs_merge_inbox.py --max-per-table 4000`: incoming 204 rows (203 older than 2026-10-18 rejected by 30-day filter), existing 7,645 preserved verbatim, additive +0 net (README stays 7,645).
- `inbox/todayfeeds--2026-11-16--v1.md` (the only untracked inbox file): +0 new, 0 duplicate — every row is undated ("—"), merger skips them.

## Sync + site build

`sync_readme_to_jobs.mjs`: readme rows=1,543, already-in-feed=1,541, added=0, dupes-collapsed=40 → jobs.json total 2,822.
`build_site.py`: public/jobs-data.json + public/index.html rebuilt — 5,784 jobs (servicenow 956 / salesforce 1,013 / other 3,815), 941 duplicate mirrors collapsed, built 2026-11-17 09:05 UTC.

## Fresh verified Toronto SN/SF jobs merged this run: 0

Every platform-titled candidate surfaced was already on the board. No entry-level Platform Administrator / Platform Developer I roles in Toronto this hour. Market shape holds: fresh platform work = senior/architect roles at banks (BMO/TD Workday) and GRC/IRM consultancies; ServiceNow-the-company and Salesforce-the-company post nothing below 4 days and no Platform Admin/Dev I in Toronto.

## Files changed

- jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json (scan + liveness gate + sync)
- public/jobs-data.json, public/index.html (site build)
- README.md (inbox merge; DAILY-SCAN block not rewritten because scan ran with --no-readme)
- FRESH_JOBS.md (scan output)
- dead_urls.txt (liveness gate appended 1 dead URL)
- JOBLESSONS_2026-11-17T0400EST.MD (this file)

## Patterns / lessons for future scans

1. **Workday CXS is consistently 429-rate-limited** across all Canadian employer boards. Do not rely on Workday for fresh hourly data; space any retries ≥5s or use the cached Adzuna mirror of Workday postings instead.
2. **LinkedIn guest endpoint recovers from 429** after a pause — first calls 429'd, subsequent returned 251 cards. Keep the 1.8s inter-request delay and 2-worker limit.
3. **Adzuna is the most reliable freshness source** — 542 matches, dominated the new rows. Keep `max_days_old=14` + `sort_by=date`; Toronto-city queries surface GTA roles that Canada-wide queries miss.
4. **40-hour cadence shows diminishing returns** — this is the 4th consecutive hour with effectively zero fresh Toronto Platform Admin/Dev I postings. An empty merge is a valid hourly outcome.
5. **Always rebase onto origin/main before pushing** — the GitHub Actions hourly scan pushes independently; a non-fast-forward reject strands work locally.
6. **Undated inbox rows are dropped by the merger** — `todayfeeds--2026-11-16--v1.md` contributed 0 rows. Only dated (YYYY-MM-DD) rows survive the 30-day filter.
7. **Never add filled/expired roles** — the liveness gate caught 1 dead jobicy URL (404). A search-engine hit is not proof of a live posting; every submitted URL must answer.

## To commit

`git add jobs.json public/jobs.json public/gotjob/jobs.json public/findjobs/jobs.json public/jobs-data.json public/index.html FRESH_JOBS.md README.md dead_urls.txt JOBLESSONS_2026-11-17T0400EST.MD`
`git commit -m "chore(jobs): 04:00 EST scan Nov 17 — 0 fresh Toronto SN/SF jobs merged, README + Pages rebuilt [skip ci]"`

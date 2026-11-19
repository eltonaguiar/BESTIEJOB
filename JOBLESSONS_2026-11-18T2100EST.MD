# JOBLESSONS_2026-11-18T2100EST

Hourly Toronto ServiceNow / Salesforce scan — cron run 2026-11-18 21:00 EST (America/Toronto).

## What ran

Fresh CA sweep (today + yesterday window: 2026-11-18 → 2026-11-19):

- Adzuna — dated API, `max_days_old` + `sort_by=date`, 68 calls, geos: national, Toronto Ontario, Ontario
- Job Bank — 13 keyword pages (servicenow / salesforce variants)
- Eluta — 6 keyword pages
- LinkedIn guest pass — SKIPPED: the 19:00 EST daily_job_scan already covered the past-24h LinkedIn guest window (~2 h ago); re-running the same window returns the same already-evaluated requisitions.

Every kept URL was live-checked (HTTP 2xx/3xx) before submission.

## Dedupe result

Raw 84 → unique 9 → kept **1** after date window, liveness, URL dedupe and title+company+city fingerprint dedupe against README.md + jobs.json:

- NEW: `2026-11-18 | Analyste Fonctionnel Salesforce | DELAN | Canada | https://www.adzuna.ca/details/5970900783` — Salesforce table, via `fresh-ca--2026-11-19--v1.md`
- 8 rows already on the board (URL duplicates) — dropped, not re-added.

## What changed

- README.md: +1 row; header count retold 6206 → 6209 live postings (`scripts/sync_readme_counts.py`). Also fixed one unreadable row (`[[C] Salesforce Engineer / Developer` → `[(C) Salesforce Engineer / Developer` at mlse.wd3.myworkdayjobs.com) that had tripped `tools/jobs_merge_inbox.py`'s no-row-loss guard — the merger refuses to write when a table row doesn't parse, so a broken row blocks every merge until fixed.
- jobs.json / public/jobs.json / public/gotjob/jobs.json / public/findjobs/jobs.json rebuilt via `node scripts/sync_readme_to_jobs.mjs` (5478 jobs; readme rows 6202, 3092 already in feed, +3107 added this sync run).
- Site rebuilt via `python3 tools/build_site.py` (823 ServiceNow / 887 Salesforce / 3245 Other; newest posting 2026-11-19).
- inbox/ pruned by `--bump-inbox` (merged submissions superseded; newest four fresh-ca versions kept, matching the fresh-ca-scan.yml convention).
- JOBLESSONS_2026-11-18T2100EST.MD (this file) committed.

## Lessons

- One hour (20:00 → 21:00 EST) yielded exactly 1 net-new Canadian Salesforce posting and zero new ServiceNow postings — zero is a real finding, not a failed scan; the board is already refreshed hourly by parallel scans.
- Adzuna's dated API is the freshest Canadian SN/SF source; Job Bank keyword matching stays noisy (most "servicenow"/"salesforce" hits are non-platform roles) — verify platform-build duties before counting a req.
- Indeed.ca (Cloudflare) and dice.com (US-only) remain unusable for Toronto SN/SF from this network; employer Workday/Lever/Greenhouse boards and Job Bank are the reliable Canadian channels.
- Rogers / Bell / Canadian government: covered indirectly via Job Bank's Government of Canada feed (mirrors OPS competitions) and Adzuna aggregator; no direct Rogers/Bell careers-board hits in this window.

## Files touched

JOBLESSONS_2026-11-18T2100EST.MD (new); README.md; jobs.json; public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json, public/index.html; inbox/*.md (pruned).

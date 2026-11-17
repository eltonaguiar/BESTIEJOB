# JOBLESSONS_2026-11-17T0700EST — BESTIEJOB hourly scan (Toronto SN/SF)

**Run:** 2026-11-17 07:00 EST (cron). **Repo:** eltonaguiar/bestiejob `main`. Local clone: `C:\Users\zerou\bestiejob`.
**Board state before run:** 2,826 jobs in `jobs.json` (scrapedAt 2026-11-17T10:12:28Z); README reports 7,588 live dedup URLs. **Result: 0 fresh mergeable Toronto ServiceNow/Salesforce jobs; board already current.**

## Channels scanned this run

| Channel | Query / scope | Result |
|---|---|---|
| Adzuna spot-check (curl) | `servicenow` + `salesforce`, `where=Toronto, Ontario`, `max_days_old=1`, `sort_by=date`, 20 results each | SN: 20 rows, all dated 11-16 or non-SN-dev titles (e.g. "ServiceNow SPM Developer" Astra-North already README line 28). SF: 44 rows, mostly sales/marketing noise failing the classifier; platform-dev hits dated 11-16 already on board. **0 fresh today.** |
| Canada sweep | `inbox/fresh-ca--2026-11-17--v2.md` (merged 06:52 UTC): Adzuna 68 calls, Job Bank 13 pages, Eluta 16 pages | 0 fresh for 11-16/11-17. Every URL liveness-checked before submission. |
| ATS fresh scan (ran 02:00–02:05 EST this morning) | `reports/fresh_servicenow_2026-11-17.json` + `fresh_salesforce_2026-11-17.json`: 105 board rounds each (Workday/Greenhouse/Lever/Ashby/SmartRecruiters/Workable) | ServiceNow: 0 new. Salesforce: 4 "new" vs scan-time jobs.json but all 4 already on board — 3 Jobgether (in jobs.json + README), Docebo "Senior Salesforce Developer" Toronto via README/Workopolis-Adzuma mirrors. |
| My fresh_ca_scan (07:00) | `scripts/fresh_ca_scan.py --days 2` (Adzuna/Job Bank/Eluta/LinkedIn) | Hung/timed out twice (300s + 420s) — Adzuna/Job Bank/Eluta rate-limiting this host. No usable output; fell back to the 06:52 UTC Canada result above. |
| Direct Adzuna Toronto spot-check (my run) | `what=servicenow` / `what=salesforce`, `max_days_old=1`, `where=Toronto` via curl | Confirmed 0 fresh platform-dev/admin roles dated 11-17. |

## Dedupe

- All candidate URLs normalized (strip query string + trailing slash) and checked against the combined dedup set (jobs.json + README). 0 new URLs passed.
- No README/table changes needed — every fresh candidate was already boarded.
- Feed consistency: ran `node scripts/sync_readme_to_jobs.mjs` (sanctioned "README reached the page but not the feed" fix) — idempotent on current origin/main (MLSE "Salesforce Engineer / Developer" Toronto 11-15 already present; total 2,827), then `python3 tools/build_site.py` rebuilt `public/jobs-data.json` + `public/index.html` (5,787 jobs; SN 958 / SF 1013 / Other 3816).
- Commit `2893df2` pushed to `origin/main`; GitHub Pages dispatched manually (`workflow_dispatch`, run 44081889638) and completed `success`. (Commit used `[skip ci]` per convention; Pages also has a `:35 UTC` schedule cron.)

## Lessons for future agents

- **`fresh_ca_scan.py` hangs when Adzuna/Job Bank/Eluta rate-limit this host** (2 attempts × 300–420s, zero output). When the full sweep hangs, fall back to direct Adzuna API curl spot-checks (`max_days_old=1`, `where=Toronto`) — fast and won't hang. Space Adzuna calls ≥3 s (503s after ~4 rapid queries).
- **The 02:00–07:00 EST ATS scans already covered the board this hour** (servicenow 0 new; salesforce 4 pre-boarded). Don't re-run the same ATS boards within the same cadence cycle — diminishing returns.
- **Freshness convergence:** all past-24h Toronto SN/SF LinkedIn cards converge to the same ~20 postings earlier hourly scans already boarded. Re-running LinkedIn + Workday the same day yields little; rotate sources instead (partner/Elite Partner portals, Greenhouse/Lever/Ashby `ats_board_sweep.py --days 2`, Job Bank title-anchored proxy, public-sector proxy).
- **Workday CXS** is reachable via `curl --compressed` with `Origin`/`Referer` headers but 422s on unknown tenants and 429s under burst — space calls ≥5 s, treat as weekly when 429'd.
- **Rogers** careers is date-sortable and reachable but had zero SN/SF mentions this hour (re-check weekly). **Bell** is zero reqs (skip). **jobs.gc.ca / gojobs.gov.on.ca** are Radware-walled; Job Bank is the public-sector proxy.
- **Commit hygiene:** lessons-only pushes use `[skip ci]` to avoid triggering the chronic red board-invariants audits (pre-existing ~136 errors on main, not a regression).

## Recommended next run

Rotate to sources not hit today: ServiceNow/Salesforce partner & Elite Partner career pages, Greenhouse/Lever/Ashby ATS sweep (`--days 2`), Job Bank title-anchored proxy, and the public-sector portal check. Re-run LinkedIn + Workday no sooner than the next cadence cycle.

## Files changed

- None to README.md (0 fresh jobs to merge).
- `jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`, `public/jobs-data.json`, `public/index.html` — feed re-sync + site rebuild only, commit `2893df2` on `origin/main`.

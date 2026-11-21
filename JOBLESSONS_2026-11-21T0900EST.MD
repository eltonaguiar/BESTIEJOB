# JOBLESSONS_2026-11-21T0900EST

Hourly BESTIEJOB SN/SF/other scan run at 2026-11-21 09:00 EST (14:00Z), main branch. Repo: eltonaguiar/BESTIEJOB.

## What this run did
- `node scripts/daily_job_scan.mjs` (no `--no-readme`, so the visible `<!-- DAILY-SCAN -->` README block was refreshed — the CI never does this).
- `tools/verify_links.py --days 2` (liveness gate on fresh rows only).
- `python3 tools/build_site.py` + `python3 scripts/sync_readme_counts.py`.
- Committed jobs.json, README.md, FRESH_JOBS.md, public/ (jobs-data.json, index.html, jobs.json, gotjob/jobs.json, findjobs/jobs.json) as 930059f `[skip ci]`; pushed to origin/main; triggered `pages.yml` for immediate deploy.

## Results
- fresh=467 merged=5583 {servicenow: 1189, salesforce: 4258}. Net-zero board growth: ~467 rows aged past the 45-day max-age and were pruned as 467 fresh ones came in — steady state, not data loss.
- Primary SN/SF core unchanged at 1189 / 4258; site rendered 5,060 jobs (servicenow 871 / salesforce 931 / other 3258), 779 duplicate mirrors collapsed, 30 applied rows hidden.
- Header count synced 5448 -> 5487 live postings.
- Live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` verified (HTTP 200) to carry fresh URLs incl. LinkedIn EY "ServiceNow IRM Senior Consultant - NFR" (4491983802) and Adzuna Manulife "Full-Stack Software Engineer" (5973912284).

## Source behavior this run
- Workday CXS: all 15 boards returned HTTP 429 → [workday] 0 matching postings. Rate-limiting persists past :00Z; the CI's :00Z hourly pass carries Workday. A manual post-:00Z probe (e.g. 10 tenants at 8s spacing) pays off within ~4 minutes — re-probe bmo/td/cibc/manulife/interac/salesforce/accenture before concluding zero fresh reqs.
- LinkedIn guest: first call HTTP 429 (authwall-shaped), retry returned 230 cards. Always judge by length + digest distinctness, not status alone; healthy card HTML ~31KB and differs per query. `f_TPR=r86400` used; `r3600` is near-empty pre-dawn EST.
- Adzuna API (api.adzuna.com, demo keys 54ce986e / db851f299e966c0a2a72af525dce6199): 200 matching postings — works from this host; www.adzuna.ca is CloudFront-walled.
- SmartRecruiters ServiceNow: 13; Lever: 1; Remote boards: 9.
- Dedupe: URL + trailing job-id equality, not normalized title (LinkedIn job-id is a hard dedupe signal even when titles differ).

## Deploy path
- `[skip ci]` commit does NOT trigger pages.yml. After the push, run `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB`; deploy lands ~40s. Verify with `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` grepping a fresh URL / comparing job count to `git show origin/main:public/jobs-data.json`.
- Next CI (:00Z) will regenerate jobs.json from its own feeds (capped ~2,500) and overwrite this manual push — manual pushes are additive, not final. Re-verify board totals after the scan completes.

## Liveness gate
- verify_links --days 2 probed 84 fresh rows: live=29, dead=0, unknown=55 (403/429/5xx/transport errors treated as LIVE, not dropped — correct; only 404/410/451 are dead). No postings pruned.

## Standing filters applied (kept)
- Toronto/GTA/Canada/remote geo; ServiceNow or Salesforce Platform Admin/Developer I targeting; exclude sales-executive / "Apex Legends" false positives; dedupe against jobs.json + APPLIED.md; never prune pre-existing dead links per user instruction.

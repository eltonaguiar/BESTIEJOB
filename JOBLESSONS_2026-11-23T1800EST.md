# JOBLESSONS_2026-11-23T1800EST — BESTIEJOB hourly scan, 18:00 EST (2026-11-23T23:04Z)

## Result
**0 net-new verified Toronto ServiceNow/Salesforce jobs merged this hour.** Valid hourly outcome — same as the 06:00 EST scan.

## What ran
- `node scripts/daily_job_scan.mjs` (Adzuna CA API via demo keys `54ce986e`/`, Workday CXS probes, LinkedIn guest search, SmartRecruiters/Lever/Ashby/Greenhouse boards from employer-watchlist.csv): 490 fresh postings harvested, 5,664 total in jobs.json (1,201 ServiceNow / 4,306 Salesforce tags), `merged=5664`.
- Workday CXS probes (bmo/td/cibc/manulife/altus/gdit/etc.) returned HTTP 429 — rate-limited, no data. LinkedIn guest returned HTTP 429. These are source failures, not zero jobs.
- `verify_links.py --days 2`: 43 rows probed, 25 live, 0 dead, 18 unknown — nothing dropped.
- `normalize_board.py --apply`: removed 2 rule-breaking rows (README 1479 → 1477).
- `resolve_clock_dates.py --apply`: no changes.
- `tools/jobs_merge_inbox.py --max-per-table 4000`: additive merge of pending inbox — +11 rows (README 1507 → 1516), mostly duplicates skipped. Old submissions merged: fresh-ca--2026-11-23--v1/v3/v5/v11, hermes-cron--2026-11-21--v23, kilo--v73, peer--v151, buffy--v181.
- `build_site.py`: site built with 4,963 jobs (861 ServiceNow / 944 Salesforce / 3,158 Other).
- `board_invariants.py`: PASS.

## Deploy
- Commit `e9dc5e9` pushed to `origin/main` (remote redirected to eltonaguiar/BESTIEJOB.git).
- GitHub Actions on push: Deploy GitHub Pages (run 45286338685), board invariants, README job-row guard, Job Source Truth Check — all **success**.
- Live page verified at https://eltonaguiar.github.io/BESTIEJOB/ — title "BESTIEJOB — ServiceNow, Salesforce & IT platform jobs", serving the rebuilt public/ data.

## Dedupe checks (candidates found via search, already on board — not re-added)
- Interac "Technical ServiceNow, Lead (6-month contract)" Toronto, LinkedIn 4126302101 — already in jobs.json.
- Take-Two "Senior Lead, ServiceNow ITOM" Toronto, LinkedIn 4481160381 / adzuna 5940716605 — already on board (posted 2026-11-12).
- ServiceNow careers roles (Senior Systems Engineer 744000162621080 Nov 20; Staff Full-Stack Engineer 744000162410339 Nov 19; Staff Cloud Security 744000162152969 Nov 17) — already on board via SmartRecruiters scan.

## Checked, nothing fresh/live
- Rogers careers (jobs.rogers.com Technology list): only Oct 26–30 postings.
- Bell (jobs.bce.ca): ServiceNow System Administrator and Senior Technical Advisor both had application deadline 10/20/2026 — expired; Director/Manager ServiceNow roles are non-build tracks.
- jobs.gc.ca / Government of Canada portals: nothing fresh.
- Sun Life ServiceNow Specialist (ITAM/CMDB, Toronto) and Scotiabank ServiceNow Solutions Architect ITAM: no current posting found (Scotiabank hits were Apr 2025 requisitions).
- Ateko/FX Innovation, Lane Four, NewRocket, Pentio: covered by prior scans; nothing new this hour.

## Leads found but NOT employer-verifiable this hour (held out of the board)
- TD "Cyber Security ServiceNow Engineer II / Sr. Developer SecOps" Toronto — description surfaced via jobs.anitab.org mirror (page now dead); TD Workday (td.wd3.myworkdayjobs.com) returns JS shell/429 from this host; apply route not confirmed. Not added.
- EQ Bank "Senior ServiceNow CMDB Consultant (6 months contract)" Toronto, LinkedIn 4144379061 (~2026-11-16) — LinkedIn guest wall and Lever board not renderable; not body-verified. Not added.

## Patterns / next hour
- Adzuna `sort_by=date` with `max_days_old=3` remains the only source reliably returning fresh CA platform postings (201 this hour); Workday/LinkedIn guest are increasingly rate-limited (429/422) — treat as leads only.
- Employer-direct portals (Rogers, Bell, GC) cycle slowly; re-check weekly, not hourly.
- Next scan: 2026-11-23T19:00 EST.

## Commit
`e9dc5e9 chore(jobs): hourly scan refresh — 18:00 EST (2026-11-23T23:04Z), 4,505 live postings, +11 merged inbox rows` — pushed to origin/main; GitHub Pages redeployed successfully.
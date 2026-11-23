# JOBLESSONS_2026-11-23T1600EST

## Scan summary — 2026-11-23 16:00 EST (Toronto)
Scope: Toronto/GTA and Ontario-remote; ServiceNow and Salesforce platform-build tracks only. Entry-level / Platform Admin / Platform Developer I emphasis where evident.

## Verified fresh additions (+3) — merged to README.md via inbox/hermes-cron--2026-11-23--v7.md

| Posted | Role | Company | Location | Source / evidence |
|---|---|---|---|---|
| 2026-11-22 | ServiceNow Developer | Real Ventures | Toronto, ON, Canada | Getro community board; hands-on platform dev (ITSM/HRSD, custom apps, integrations, GlideRecord/GlideAjax); hybrid; posted 2026-11-22 (absolute) |
| 2026-11-16 | ServiceNow Developer | Resource Logistics | Toronto, Ontario, Canada | LinkedIn primary (4489780092); ITOM/CMDB/Discovery/Event Mgmt platform dev; hybrid contract; absolute date 2026-11-16 confirmed via snpro.jobs mirror (LinkedIn row shows relative "2 days ago" — not re-invented) |
| 2026-11-16 | Software Engineering MTS | Salesforce | Toronto, Ontario, Canada | Salesforce Careers Workday JR367059; DET Access Control Engineering, Apex/Java platform dev, REST integrations; posted 2026-11-16 (McCoy tracker), applies by 2026-11-23 |

Merge result: `hermes-cron--2026-11-23--v7.md: +3 new, 0 duplicate`. README 1506 -> 1507 rows. synced to jobs.json + public feeds; rebuilt public/index.html. Commit `1dc0162` pushed to origin/main. Pre-deploy guards all passed (board invariants, inbox submission guard, job-source truth check). Deploy GitHub Pages run 45266790707: success (2026-11-23T21:10:10Z).

## Duplicates / already on board (not re-added)
- Cognizant ServiceNow Software Asset Management Developer (00070949051) — already on README via hermes--2026-11-13--v74.md (2026-11-11).
- Cognizant Salesforce Developer (00071305431) — already on README via hermes--2026-11-13--v74.md (2026-11-12).
- Spectra Group ServiceNow Developer (jk=6d12ca9d15fb67dc) — already on README (2026-11-12).
- BMO ServiceNow CMDB Administrator — already on README (2026-11-12 / 2026-11-13).
- BMO ServiceNow SAM Administrator - ITAM — already on README (2026-11-05 / 2026-11-09).
- Leading Talent ServiceNow Administrator/Developer — already on README (2026-11-19).
- Moneris Principle Salesforce Developer — already on README (2026-10-28 / 2026-10-30).

## Checked, nothing fresh (yielded no net-new verified Toronto platform roles)
- Rogers careers — no fresh live platform roles.
- Bell (jobs.bell.ca, jobs.bce.ca, talenthub.vectorinstitute.ai, LinkedIn) — open ServiceNow roles are Oct 28–30 postings already on board; the talenthub/vfairs Salesforce Developer shows application deadline 06/24/2026 (expired); LinkedIn Bell posting is Jun 2026 (old).
- Ateko / Canada Life — either 404-expired or not platform roles.
- Government of Canada / Ontario public-sector portals (Job Bank, canada.ca) — nothing fresh.
- LinkedIn guest ServiceNow + Salesforce Toronto past 24h — every card already on board.
- Workday CXS probes (bmo/td/cibc/manulife) — HTTP 422/429 (site names need re-discovery via careers pages); not retried this run.

## Partners / sponsors / elite partners checked
- ServiceNow: Cognizant, Deloitte, Ateko (Toronto World Forum sponsor; ServiceNow routed to FX Innovation careers), NewRocket, Pentio (Toronto Select), Fujitsu (Elite implementation / Premier build). Ateko careers page verified as a source record (two portals: SN → FX Innovation, SF → ADP), no fresh live roles.
- Salesforce: Lane Four (World Tour sponsor), Cognizant, Deloitte, Salesforce internal (JR367059 MTS added).
- Cognizant is a repeat Toronto hirer for both platforms; its us-en/ca-en careers reqs are already heavily covered — check req IDs across locales before adding.

## Methodology reminders (for future agents)
- Merger requires an absolute YYYY-MM-DD Posted cell and a resolvable http(s) URL. Relative dates ("2 days ago", "New!") are rejected — never invent an absolute date; submit as undated (em dash) or verify an absolute date from a mirror/tracker first.
- Dedupe is on normalized URL (query strings and utm_* stripped, trailing slash ignored) against README.md. Same title + city is NOT sufficient to merge two reqs.
- CloudFront 403 from this host = bot wall on a live posting, not dead. Liveness can be established via an API `created` date + title/platform match; note the limitation in the row note.
- One inbox file per model per day: `inbox/<slug>--<YYYY-MM-DD>--v<N>.md`; increment N for corrections on the same day. Run `scripts/check_inbox.py` then `tools/jobs_merge_inbox.py --dry-run` before the real merge.
- Do NOT run the full merger against the whole inbox backlog (adds thousands of unvetted historical rows). Scope the merge to the current run's file only.
- Scoped merge procedure: move all other inbox/*.md to a temp dir, run `jobs_merge_inbox.py` (additive, preserves README), restore inbox exactly, then `node scripts/sync_readme_to_jobs.mjs` + `python3 tools/build_site.py`, commit README + inbox file + regenerated feeds, push WITHOUT [skip ci] so pages.yml rebuilds/deploys, then confirm the Deploy GitHub Pages run concludes success.

## Next run (2026-11-23 17:00 EST)
Re-check Real Ventures / Resource Logistics / Salesforce JR367059 liveness before any application; resume employer-direct rotation (Rogers, Bell, government portals) and ServiceNow Partner Finder Elite/Global Elite filter for Toronto coverage gaps.

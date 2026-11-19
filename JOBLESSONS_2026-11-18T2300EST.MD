# JOBLESSONS_2026-11-18T2300EST

Hourly Toronto ServiceNow / Salesforce scan — 2026-11-18 23:00 EST (2026-11-19 04:00Z). Run as cron job against github.com/eltonaguiar/bestiejob on `main`.

## Result
- Fresh verified Toronto SN/SF jobs merged: **2** (1 ServiceNow, 1 Salesforce)
- README.md: +2 rows; public/ site rebuilt (4,955 jobs indexed; 823 SN / 887 SF / 3,245 Other)
- board_invariants.py: PASS (ratchet: no error/warning kind grew)
- check_site_links.py: OK (every card links to its posting; tabs/aria/stamp/fit present)
- Pushed to `main`; GitHub Pages deploys via pages.yml on push to public/ + README.md

## Jobs merged (inbox/hermes-cron--2026-11-18--v12.md)

| Posted | Role | Company | Location | Track | Evidence |
|---|---|---|---|---|---|
| 2026-11-18 | Business Analyst – ServiceNow Strategic Portfolio Management (SPM) | NTT DATA North America | Toronto, Ontario, Canada | ServiceNow | LinkedIn guest page read in full; JSON-LD datePosted 2026-11-18T04:22:50Z; SPM module duties |
| 2026-11-18 | Salesforce Senior Solutions Architect | IBM | Toronto, Ontario, Canada | Salesforce | LinkedIn guest page read in full; JSON-LD datePosted 2026-11-18T17:19:54Z; "designing, implementing, and supporting Salesforce CRM solutions with LWC and integration experience"; FULL_TIME |

## Sources checked this cycle
- `scan_boards.py --read` on watchlist ATS APIs with adapters: eqbank, versapay, alimentiv, electricmind (Lever); levio (Greenhouse); ensiti (SmartRecruiters). Yielded keyword leads only — no dated Toronto SN/SF postings cleared for merge. Leads are not postings; no dates = no merge.
- FRESH_JOBS.md daily harvest (2026-11-19T00:02Z, 2,406 postings): 846 Toronto SN/SF rows, 133 not already on README; after the 30-day window (cutoff 2026-10-20), gated/listing filters and dedupe against README tables + APPLIED.md, only the 2 above were new and verifiable.
- Prior cycle's inbox (hermes-cron--2026-11-18--v10, already merged +12): explicitly dropped ServiceNow ITOM Developer (TechNeptune 4491345268) and ServiceNow Developer cum Architect (Raas Infotek 4492046880) as same company+title+city mirrors of rows already on the board under other LinkedIn ids — respected and not re-submitted.
- Direct LinkedIn guest fetches: ca.linkedin.com/jobs/view/<id> returns HTTP 200 with JobPosting JSON-LD (datePosted, description, location) under a browser UA — sufficient to verify date + duties without login. PwC 4492083143 rendered guest-limited (no datePosted/duties) → dropped per the absolute-date rule; date not guessed from the harvest clock.
- NTT DATA 4490843088 and IBM 4491324074 confirmed absent from README.md and APPLIED.md before merge.

## Patterns / lessons for future agents
1. Check `inbox/` for today's existing files before staging: earlier cycles may already have merged or explicitly dropped today's leads. Re-submitting dropped mirrors creates duplicate-url noise the merger silently skips.
2. Same company + same title + same city under a different LinkedIn job id = repost/mirror, not a new opening (established by this repo's prior cycles; do not re-litigate per run).
3. Anonymous LinkedIn guest pages ARE verifiable: fetch with `curl -A "<browser UA>" -L`, parse `<script type="application/ld+json">` JobPosting. Require datePosted (absolute) + platform + build duties + Canadian location before staging.
4. If a LinkedIn guest view hides datePosted and duties (PwC pattern), the row fails the fresh-feed rules — skip it; never backfill a date from FRESH_JOBS.md or the scan clock.
5. Adzuna.ca/details/* and other aggregator mirrors are discovery leads, not truth: the merger's `is_listing_url`/`domain_is_gated` and freshness window drop most of them; employer-direct URLs (lever.co, greenhouse.io, ashbyhq.com, smartrecruiters, myworkdayjobs.com, ca.linkedin.com/jobs/view/) are the preferred canonical links.
6. Toronto scope per runbook: City of Toronto or GTA districts; fully remote open to Ontario also in scope. Mississauga/Markham office alone is out of scope per the strict reading, though the board already carries some Mississauga rows — match existing board norms, don't expand unilaterally.
7. Always run the full local pipeline before pushing: check_inbox → jobs_merge_inbox → sync_readme_to_jobs.mjs → build_site.py → board_invariants.py → check_site_links.py. Push to main triggers pages.yml (build + deploy) automatically; no separate deploy step needed.
8. Filename collision risk: `hermes-cron--2026-11-18--v11.md` already existed on origin/main with different content — use the next free version (`v12`) and re-verify against origin/main after a reset.

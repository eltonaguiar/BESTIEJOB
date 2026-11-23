# JOBLESSONS_2026-11-23T1400EST

14:00 EST hourly scan for Toronto/Canada ServiceNow + Salesforce postings against eltonaguiar/BESTIEJOB main.

## Result

- Scan sources: SmartRecruiters (ServiceNow), Workday CXS (15 boards), Greenhouse, Lever, Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna Canada (29 queries, sort_by=date, max_days_old=14).
- `fresh=506 merged=5659` (SN 1199 / SF 4303). **fresh is not new-rows:** diffing URL sets against `origin/main:jobs.json` found **39 genuinely new URLs**; the rest were already on the board (Adzuna re-issues ids, LinkedIn cards previously ingested). Always diff URL sets before reporting additions.
- New roles include: BMO ServiceNow CMDB Administrator (Toronto), OSI Digital Salesforce Platform Developer (Toronto), Celestica "Student Intern, Salesforce Developer 1" (Toronto), Alithya "Analyste d'affaires Salesforce" (Montreal), Doctors of BC Salesforce Administrator (Vancouver), Deloitte/TD/Konrad platform reqs.
- Liveness gate (`verify_links.py --days 2 --workers 16`): 35 fresh rows probed, 21 live, 0 dead, 14 unknown (403/429/transport errors kept — never treated as dead). Nothing dropped.
- Workday CXS returned HTTP 429 on all 15 boards at :00Z — rate limit, not zero postings. The CI hourly pass carries Workday; a manual re-probe of 3–4 key Canadian tenants (bmo, td, cibc, manulife, interac) at ≥8s spacing ~4 minutes after :00Z returns HTTP 200.
- Commit: `chore(jobs): 14:00 EST scan refresh — 39 new Canada SN/SF postings (5659 listings)` — 8 files (jobs.json, public/**, README.md, FRESH_JOBS.md). Push raced the CI :00Z sweep (3c2b197): rebased onto origin/main, took `--theirs` on the 6 generated files, pushed 55043c0.
- `pages.yml` deploy (triggered by the push; public/** + README.md changed): run 45246598136, success. Live `jobs-data.json` = 4,960 jobs (859 SN / 943 SF / 3,158 other).
- **Verification signal:** `build_site.py` collapses company+title mirrors, so new roles may vanish by URL from `jobs-data.json` while still rendering. All 5 sampled new roles confirmed LIVE on the page by company+title (BMO ServiceNow CMDB Administrator, Deloitte ServiceNow Platform Senior Consultant, Celestica Salesforce Developer 1 intern, Altus Group Salesforce Platform Developer, Doctors of BC Salesforce Administrator); 4 of 5 are MISS by raw URL — expected, not data loss.

## Patterns for future agents

- Diff URLs against `git show origin/main:jobs.json`, not `fresh=N`, before claiming new jobs.
- Check the live page by `company + title` in `jobs-data.json`, never by URL alone.
- Workday 429 at :00Z is normal; leave Workday to CI, or re-probe key Canadian tenants after ~4 minutes.
- LinkedIn guest search worked this run (272 cards, healthy ~31 KB distinct bodies). If it returns identical long bodies on HTTP 200, that's the authwall — retry once after ~4 minutes, digest+length check, not status alone.
- `capSecondary(perTag=40)` is by design: local runs cut jobs.json secondary rows; do not hand-merge 'other' rows back.
- CI hourly scan overwrites manual pushes; treat a manual push as additive, verify board totals after the scan completes before declaring the board updated.

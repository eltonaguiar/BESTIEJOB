# JOBLESSONS_2026-11-17T0200EST

Hourly BESTIEJOB scan — Tuesday 2026-11-17 02:00 EST (07:00 UTC). Cron run of the Toronto ServiceNow / Salesforce job scan.

## Scan run
- `python3 scripts/fresh_scan.py --family servicenow --days 7` and `--family salesforce --days 7` over the repo's 105 employer ATS boards (Workday, Greenhouse, Lever, Ashby, SmartRecruiters, Workable); cutoff 2026-11-10; every candidate HTTP liveness-checked (2xx/3xx).
- ServiceNow: 13,137 fetched · 6 fresh · 3 live · **0 net-new** — every fresh SN posting already on the board (URL dedupe against README.md + jobs.json).
- Salesforce: 13,237 fetched · 6 fresh · 4 live · 4 net-new vs jobs.json; 1 already present in README.md (Docebo — Senior Salesforce Developer, Toronto, 2026-11-10, via ats-sweep) → skipped as duplicate. **3 merged** (all Jobgether via Lever, location Canada, live-verified HTTP 200):
  1. 2026-11-13 · Associate Vice President, Salesforce Engineering & Development · jobs.lever.co/jobgether/72434945-c782-4d3e-9b31-1ab1a75c21b7
  2. 2026-11-13 · Solution Architect, Salesforce Voice · jobs.lever.co/jobgether/af053390-3bd6-4a14-b02e-f9a95abab903
  3. 2026-11-10 · Associate Salesforce Administrator · jobs.lever.co/jobgether/31937f76-54e7-4341-8158-d03a295821a8
- Board after merge: README 7588 live postings (was 7585); Salesforce table 1531 (was 1528); ServiceNow unchanged at 1316; jobs.json 6318 rows, salesforce primaryCount 1388.
- Site rebuilt with `python3 tools/build_site.py` (newest 2026-11-17, built 07:10 UTC); public/index.html + public/jobs-data.json committed so GitHub Pages (pages.yml deploys on push to main) serves the update.

## Dedupe / merge lessons
- Diff candidate URLs against **both** README.md and jobs.json — the two disagree (board-invariants count-disagreement: 1). The Docebo row lived in README but not jobs.json; URL grep on README caught it.
- Keep tables newest-first: insert rows at the date boundary (after last 2026-11-16 row, before first 2026-11-15 row), never at the top of the table.
- README.md uses CRLF line endings; table rows start with `| ` — an extra leading pipe (`||`) creates a 6th empty cell and breaks table parsing.
- Row format: `| Posted | Role | Company | Location | Source / note |` with note like `via lever |`.

## Source notes (this cycle)
- LinkedIn guest detail pages are readable; seeMoreJobPostings API 429s after ~4 rapid queries — space calls ≥5s. The 2026-11-16 LinkedIn sweep (NLB Services, AllianceIT, Yochana, Cognizant, Smart IT Frame, HRConnects) was fully deduped at the 01:00 run; nothing new at 02:00.
- Workday CXS rate-limits at 422 on bursts — space calls ≥5s (carried from prior cycles).
- Rogers / Bell / Canadian government: public-sector scan blocked by Radware bot manager; Job Bank feed returned 0 dated Toronto SN/SF postings in window. Rogers career-site HTML harvested; no fresh SN/SF Toronto this cycle.
- SN/SF partners in the 105-board sweep (NeuraFlash, RapDev, Zaelab, Flosum, Crossfuze, Accenture, Deloitte, Cognizant): none fresh in window.

## Git
- Peer agents push to main constantly; on push rejection, `git pull --rebase --autostash origin main && git push`. Commits carry `[skip ci]` so they don't re-trigger the hourly scan workflow.

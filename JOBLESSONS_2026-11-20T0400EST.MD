# Job-search lessons — 2026-11-20 04:00 EST (09:00Z) — BESTIEJOB hourly cron

Run of `node scripts/daily_job_scan.mjs` on origin/main `c306128` (08:18Z CI refresh), then `verify_links.py --days 2`, `build_site.py`, `sync_readme_counts.py`.
Result: **524 fresh / 2525 merged** (SN 1172 / SF 1212); site **5036 cards** (SN 849 / SF 918 / Other 3269); README DAILY-SCAN block **473 live postings / 9 sources**; header **6208 live postings**.

## Source behaviour this cycle
- **Workday CXS 429 at :00Z again — all 15 boards, both queries.** The 09:00Z run collided with the CI hourly scan as predicted. Carried Workday rows survive the 45-day window, so nothing was lost. Manual runs should start at :10Z+ to refresh Workday.
- **LinkedIn guest API:** first call 429, then recovered — 284 matching postings across 40 queries (mapLimit(2) + 1.8 s pacing rides it out). Do not abort on a single 429.
- **Adzuna:** 196 matching, no 503s this cycle. Demo keys still valid (`54ce986e` / `db851f299e966c0a2a72af525dce6199`).
- **SmartRecruiters (ServiceNow):** 13 matching, all non-Canada engineering roles except one Toronto Principal Solution Architect (10-29) already on the board.
- **verify_links --days 2:** 164 probed → 81 live / 0 dead / 83 unknown (403/429/5xx bot-walls kept). Nothing dropped.

## Fresh Toronto/GTA SN/SF signal (11-19 → 11-20)
- **Salesforce:** CanPrev — Salesforce Administrator (North York, 11-20); Avanciers — Salesforce Business Systems Analyst (Toronto, 11-20); Jobgether — Salesforce Business Process Analyst (Canada, 11-20, two LinkedIn ids 4492537774 / 4492529940).
- **ServiceNow:** Ateko backed by Bell Canada — Spécialiste d'implantation ServiceNow / Implementation Specialist (Canada, 11-19); Acronym Solutions — ServiceNow Platform Developer (Etobicoke, 11-19); Flexstaf I.T. — Senior ServiceNow Consultant (Toronto, 11-19); PwC — Senior Associate, Workflows & Automation (Sr ServiceNow Developer) (Canada, 11-19); LGS, an IBM Company — ServiceNow Developer + Architecte solutions HRSD/CSM/IRM (Ville-Marie QC, 11-19); La Caisse — Premier développeur ServiceNow (Montreal, 11-19).
- **Banks:** TD — Associate Software Engineer (nCino/Salesforce) 11-19; TD — Senior Solution Architect (ServiceNow) 11-18; BMO — ServiceNow CMDB Administrator (11-17) and ServiceNow Technology Lifecycle Analyst (11-12).
- **Consultancies/partners on the board:** Accenture (SF Techno-Functional/AMS Lead), CGI (SF BA Toronto), PwC (SN Dev + SF Associate), TCS (Sr SF Dev), Cognizant (SN SAM Dev + SF Dev), Coforge, KPMG Canada (SN Solution Developer), Deloitte (SN Platform Senior Consultant), Wipro (SN Implementation Architect Mississauga), IBM/LGS (Quebec SN roles), NTT DATA, Virtusa.
- **Rogers:** `jobs.rogers.com/search/?q=servicenow` now returns HTTP 200 / 56 KB but zero job rows server-side (Phenom shell) — no Rogers SN/SF surfaced; keep relying on Adzuna/LinkedIn.
- **Bell:** real SN hiring still surfaces as **Ateko, backed by Bell Canada** (French/English titles) — confirmed again with a 11-19 Implementation Specialist. Search "Ateko", not "Bell".
- **Government of Canada/Ontario:** no dated SN/SF posting captured; Job Bank / gojobs remain Radware-walled and keyword hits are body-text false positives.

## Dedupe lessons
- **Jobgether duplicates its own posting under two LinkedIn ids** (4492537774 / 4492529940) with identical title/company — same role, keep one card.
- **Apptoza reposts the same title under new ids** (4491623443 vs 4491626483, ServiceNow BA Toronto) — `build_site.py` mirror-collapse already keeps one; do not add both to README tables.
- **TD nCino/Salesforce is one req, two URLs:** Adzuna `details/5971441048` vs Workday `R_1508918`; the site canonicalises to the Workday URL. Keep the Workday row as canonical.
- New scan rows are correctly landing in the README main tables (Apptoza line 2248, TD nCino line 2254, TD SN Architect line 108, TCS line 1240) — dedupe against README is working.

## Operational
- `jobs.json` shrinks to ~2,525 rows after a local scan (`capSecondary` caps secondary tags at 40) while the site stays at ~5,036 cards via the README union. This is by design; the CI `sync_readme_to_jobs.mjs` re-widens the feed within the hour. **Never hand-merge the "other" rows back.**
- Stage ONLY: jobs.json, README.md, FRESH_JOBS.md, public/jobs-data.json, public/index.html, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json, and the lessons file. The `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` submodule gitlink and untracked `leads-*.jsonl` / `reports/*` / `README.BAK_*` stay out.
- Push with `[skip ci]`, then `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB` for immediate live reflect; verify the live `jobs-data.json` carries a fresh URL (Ateko `4492156434` was present pre-deploy).

## Hourly agent recipe (confirmed again)
1. `git fetch origin main && git reset --hard origin/main`.
2. `node scripts/daily_job_scan.mjs` (no `--no-readme`).
3. `python3 tools/verify_links.py --days 2` (drop only 404/410/451).
4. `python3 tools/build_site.py && python3 scripts/sync_readme_counts.py`.
5. Write `JOBLESSONS_<date>T<HH>00EST.MD`; stage the generated files only; commit `[skip ci]`; push.
6. `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB`; poll the run; curl the live `jobs-data.json` and grep a fresh URL.

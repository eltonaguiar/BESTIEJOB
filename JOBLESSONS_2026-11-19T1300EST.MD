# JOBLESSONS 2026-11-19T1300EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
`scripts/daily_job_scan.mjs` full hourly pass at 2026-11-19T18:02:42Z (13:02 EST), then `scripts/focused_search.mjs`, then `tools/build_site.py`, committed as c15a516 and pushed to `origin/main`.

Sources queried: SmartRecruiters (ServiceNow board), Workday CXS (altusgroup, bdo, bm, brookfield, caatpension, gdit, huron, irvingoil, mckesson, medcan, moneris, resolvetech, td — **all HTTP 429**), Greenhouse, Lever, Ashby, LinkedIn guest (HTTP 429 first attempt, 300 postings on retry), Adzuna CA API (199), RemoteOK/Jobicy/Remotive (12). Followed by focused Adzuna pass: 41 certification/role keywords × 10 locations, 7-day window (410 API calls).

## Result — this cycle
- Fresh candidates surfaced by live scan: 544. Genuinely new URLs vs the board (baseline jobs.json at HEAD had 5,526 rows): exactly **37**.
- Focused Adzuna pass added **797** new unique jobs (ServiceNow 107, Salesforce 63; heavy Other-family hits: ITIL 71, Tableau 100, Power BI 114, Technical Consultant 120, PowerShell 77, Alteryx 36, ITAM 20, CMDB 9, ITSM 38).
- Merged total: `jobs.json` = 6,360 jobs. `tools/build_site.py` indexed 5,525 after mirror collapse (919 duplicate clusters), 30 applied roles hidden, newest posting 2026-11-19. Site family counts: servicenow 840, salesforce 912, other 3,773.

New verified ServiceNow / Salesforce rows added this cycle (Toronto-first, newest first):
- BMO — ServiceNow CMDB Administrator (Toronto, 2026-11-17); ServiceNow SAM Administrator - ITAM (Toronto, 2026-11-09); ServiceNow Technology Lifecycle Analyst (Toronto, 2026-11-12)
- TD Bank — Associate Software Engineer (nCino/Salesforce) (Toronto, 2026-11-19); Senior Solution Architect (ServiceNow) (Toronto, 2026-11-18); Software Engineer III - Salesforce Data 360 (Toronto, 2026-11-15)
- Cognizant — Salesforce Developer (Toronto); ServiceNow Software Asset Management Developer (Toronto)
- OSI Digital — Salesforce Developer / Business Analyst / Quality Analyst Tester / Salesforce Lead (Toronto, 2026-11-11 to 2026-11-12)
- NeuraFlash — Salesforce Technical Architect, AI and Agentforce (Remote - Colombia, 2026-11-18)
- Rogers Communications — Lead Management Operations (Toronto/Mississauga, 2026-11-19) [partner/sponsor check]
- ServiceNow Inc. — Staff Full-Stack Engineer, Experience Team (Toronto, 2026-11-19); Principal Solution Architect - ServiceNow (Toronto/Remote, 2026-10-29)
- NLB Services — ServiceNow CSM/HRSD (Mississauga, 2026-11-19)
- Co-operators — Senior Systems Developer - Salesforce (Temp, 12 mths; Mississauga/Guelph/Toronto, 2026-11-19)
- Deloitte — Senior Consultant, ServiceNow Platform (Toronto, 2026-11-01)
- Wipro — ServiceNow Implementation Architect (Mississauga, 2026-11-04); KPMG Canada — ServiceNow Solution Developer (Toronto, 2026-11-07); Altus Group — Salesforce Platform Developer (Toronto, 2026-10-30); Benevity — Senior Salesforce Administrator (Toronto/Calgary, 2026-10-28); La Caisse (CDPQ) — ServiceNow Developer FR (Montreal, 2026-11-19); Apptoza — ServiceNow Business Analyst (Toronto, 2026-11-19); Pacer Group / Avanciers — ServiceNow Implementation Architect (Toronto, 2026-11-11)

Already on board (deduped, not re-added): Flexstaf Senior ServiceNow Consultant (Toronto), Shodh Consultancy Salesforce Architect (Mississauga), Wipro ServiceNow Implementation Architect, TD Senior Solution Architect — all present in HEAD jobs.json / README tables.

## Partner / sponsor / target-employer check (this cycle's ask)
- Rogers: one fresh verified hit — Lead Management Operations, 2026-11-19, Toronto/Mississauga (via Adzuna).
- Bell (jobs.bce.ca / jobs.bell.ca): search returned only expired October 2026 deadlines (ServiceNow System Administrator, ServiceNow Developer/Integrator, BCE Senior Technical Advisor published 2026-10-10) or non-platform roles (Director ServiceNow CoE in French, Enterprise Solutions Architect II) — nothing fresh verified inside the 2026-10-20 → 2026-11-19 board window this cycle.
- Government of Canada / jobs.gc.ca: no fresh verified ServiceNow / Salesforce posting found this cycle (Job Bank search surface was generic; no gated jobs.gc.ca scraping performed).
- SN/SF partner coverage this cycle came from configured sources instead: Workday boards (BMO, TD, Altus, BDO, etc.), Greenhouse/Lever/Ashby boards (NeuraFlash, Benevity, D2L, Loopio), SmartRecruiters ServiceNow, LinkedIn guest, Adzuna CA.

## Git / Pages
- Commit `c15a516` on `main`; pushed `origin/main` over HTTPS (remote suggests `eltonaguiar/BESTIEJOB.git`; pushes still succeed). No `[skip ci]` so GitHub Pages rebuilds from `public/`.
- Unrelated working-tree items left untouched: modified `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` submodule and untracked `leads-2026-11-18.jsonl` — not part of this run.

## Lessons for future agents
1. **Workday CXS returns HTTP 429 on every tenant at the CI hour** (all 16 tenants failed this cycle). Leave Workday to an off-hour pass or retry ≥8 s apart; do not treat 429 as zero jobs.
2. **`daily_job_scan.mjs` replaces `jobs.json` with its own scan cache** (this cycle: 5,526 → 2,459 rows). Always `git checkout HEAD -- jobs.json` after the scan, then insert only genuinely new rows via normalized-URL diff (strip query string + trailing slash, lowercase host+path). Vendor twins (different staffing firms, same client req) are kept.
3. **LinkedIn guest endpoint rate-limits (HTTP 429)** — retry the same URL after a short wait; a healthy response differs in body per query, don't trust status=200 alone.
4. **`scripts/focused_search.mjs` writes `jobs.json` itself** (appends Adzuna matches, copies to public/). Run it *after* the jobs.json baseline restore + delta merge, and *before* `tools/build_site.py`.
5. **`build_site.py` drops jobs.json rows with no `postedDate` in `YYYY-MM-DD` format**, plus dead URLs (`dead_urls.txt`), APPLIED.md rows, and listing pages; it dedupes mirrors by `ident_key` (path + Indeed-style query id). 835 of 6,360 JSON rows did not reach the site this cycle for those reasons.
6. **Commit `public/jobs-data.json` and `public/index.html` with `jobs.json`; no `[skip ci]` when `public/` changes** if you want the Pages deploy this cycle (`[skip ci]` only for docs/lessons-only commits).
7. **`git push` over HTTPS works; when rejected ("fetch first"), `git pull --rebase origin main` then push again.**
8. **Duplicate-key guard in `buildReadmeBlock`**: the README `<!-- DAILY-SCAN -->` block excludes URLs already in README tables, so reruns never re-list old rows.

## Commit
`c15a516` chore(jobs): hourly SN/SF Toronto scan 2026-11-19T1300EST — 834 fresh rows merged (no [skip ci] — pages deploy)

# JOBLESSONS_2026-11-22T0900EST

Hourly Toronto ServiceNow / Salesforce scan — Sunday 2026-11-22 09:00 EST (UTC-05).
Board: github.com/eltonaguiar/BESTIEJOB (main), pages: eltonaguiar.github.io/BESTIEJOB/

## Result this run
- Fresh verified Toronto SN/SF jobs merged to jobs.json: **9 primary (SN/SF, Toronto/GTA)** + 28 other-category/outer-region rows added by URL (37 total URLs added; 5598 -> 5634 jobs.json rows)
- Commit: `2fe967b` `chore(jobs): hourly Toronto ServiceNow/Salesforce scan 2026-11-22 — add verified fresh postings [skip ci]`
- Pages deploy: **success** (run 45030933569, ~40 s)
- Live page verified: `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` = 5,011 jobs (SN 875 / SF 939); all 6 sampled new URLs present on the live page

## New verified jobs added this run (Toronto/GTA, ServiceNow / Salesforce)

| Posted | Role | Company | Location | Source | Notes |
|---|---|---|---|---|---|
| 2026-11-22 | Salesforce Tech Lead (Remote) | Cognizant | Toronto, Ontario | adzuna.ca/details/5974890709 | Posted today; remote-friendly Toronto role |
| 2026-11-21 | Salesforce Platform Developer | Altus Group | Toronto, Ontario, Canada | linkedin .../salesforce-platform-developer-at-altus-group-4483476940 | "Platform Developer" title matches user's Platform Developer I emphasis |
| 2026-11-21 | Principle Salesforce Developer | Moneris | Toronto, Ontario, Canada | linkedin .../principle-salesforce-developer-at-moneris-4466619394 | Posted yesterday; Moneris is a Workday board (bmo/td-family) |
| 2026-11-20 | Sr Salesforce Developer | Euna Solutions | Oakville, Ontario, Canada | linkedin .../sr-salesforce-developer-at-euna-solutions-4492752341 | Oakville = GTA |
| 2026-11-19 | Student Intern, Salesforce Developer 1 | Celestica | Toronto, Ontario | adzuna.ca/details/5971440660 | Entry-level "Developer 1" — matches junior/Platform Dev I focus |
| 2026-11-18 | Senior Solution Architect (ServiceNow) | TD Bank | Toronto, Ontario | adzuna.ca/details/5970077372 | TD is a verified Workday CXS tenant (td.wd3/TD_Bank_Careers) |
| 2026-11-17 | ServiceNow CMDB Administrator | BMO | Toronto, Ontario, Canada | linkedin .../servicenow-cmdb-administrator-at-bmo-4490380189 | CMDB/ITAM (other-category); BMO = verified Workday tenant (bmo.wd3/External) |
| 2026-11-15 | Software Engineer III - Salesforce Data 360 | TD Bank | Toronto, Ontario | adzuna.ca/details/5966715213 | Salesforce Data Cloud/360 |
| 2026-11-12 | ServiceNow Technology Lifecycle Analyst | BMO | Toronto, Ontario, Canada | linkedin .../servicenow-technology-lifecycle-analyst-at-bmo-4490364941 | |

## Dedup checks performed (skipped, not double-listed)
| Candidate | Why skipped |
|---|---|
| Amicis Global — ServiceNow Business Analyst - Senior, Toronto (adzuna 5972002660, posted 2026-11-19) | Company+title twin of existing row via adzuna 5972983023 (URL-only dedupe misses this) |
| TCS — Senior Salesforce Developer, Toronto (2 linkedin URLs 4491845382 / 4491853255) | Same role posted under two LinkedIn job IDs; one role, two URLs |
| OSI Digital — Salesforce Developer, Toronto | Mirror triples across adzuna/linkedin URLs; company+title already represented |
| Pacer Group — Servicenow Implementation Architect, Toronto (2026-11-12) | Same employer+title+city+date already on board via a jobs.ca mirror URL |
| CGI — ServiceNow Architecture Consultant, Calgary (2026-11-14) | Outside Toronto target metro |
| OSI Digital / Celestica / TD rows posted 2026-11-08 and earlier | Outside the today/yesterday freshness window (retained only because within 45-day MAX_AGE) |

## Partner / sponsor / target-employer sweep

**Workday CXS (Canadian tenants)** — ALL probes returned HTTP 429 this run because the CI hourly scan fires at :00Z (14:00Z = 09:00 EST) and rate-limits Workday for several minutes after. Boards probed: bmo/External, td/TD_Bank_Careers, cibc/search, manulife/MFCJH_Jobs, interac/interac, salesforce.wd12/External_Career_Site, accenture.wd103/AccentureCareers, gdit.wd5/External_Career_Site, plus bdo/altusgroup/iko/moneris/irvingoil/mckesson/brookfield/resolvetech. **Lesson: when [workday] 0 matching postings / 429, retry the key tenants (bmo, td, cibc, manulife, interac) ~4 minutes after :00Z at ≥8 s spacing — a post-:00Z retry returns HTTP 200. Do not conclude "no fresh reqs" from a :00Z 429.**

**ServiceNow partners / Elite partners** — Altus Group yielded the new Salesforce Platform Developer row above (via LinkedIn). No separate vacancies surfaced on NewRocket / Lane Four / Pentio / Fujitsu partner profiles this cycle. Slalom's prior-cycle Salesforce Developer (Toronto hybrid) already on board.

**Rogers** — jobs.rogers.com (Phenom) is date-sortable but returns a zero-row shell / 404 to curl; no SN/SF platform posting surfaced. Rely on LinkedIn/Adzuna for Rogers rows; do not retry hourly.

**Bell** — jobs.bell.ca shows (0) for servicenow and salesforce: zero reqs, not a scrape failure. Bell's real platform hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation; no fresh vacancy listed this cycle — record the portal, not a job.

**Canadian government / public sector** — gojobs.gov.on.ca (Ontario) and jobs.gc.ca are Radware-walled (captcha); do not retry. Use Job Bank as proxy and trust only postings whose *title* names the platform. CMHC ServiceNow ITSM Developer (req 12379) already on board from prior scans. SSC / Global Affairs: no fresh SN/SF platform posting this window.

**Salesforce-the-company** — posts nothing below 4 days and no Platform Admin/Dev I in Toronto; fresh platform work comes from banks (BMO/TD Workday), DXC, and GRC/IRM consultancies.

## Sources consulted
Adzuna Canada API (app_id/app_key hardcoded demo creds; `max_days_old=3`, `sort_by=date`, `where=Toronto`), Workday CXS search API (429'd at :00Z), LinkedIn guest (173 rows, one 429 retry), SmartRecruiters, Greenhouse, Lever, Ashby, RemoteOK/Jobicy/Remotive, Rogers jobs.rogers.com, Bell jobs.bell.ca, Altus Group, Moneris, Celestica, TD Bank, BMO, LinkedIn partner searches.

## Lessons for future agents
1. **Workday 429s at :00Z are rate-limiting, not empty results.** Always re-probe bmo/td/cibc/manulife/interac/salesforce/accenture/gdit ~4 minutes after :00Z (≥8 s spacing) before reporting zero Workday fresh reqs.
2. **Dedupe on company+title+city+date, not URL alone.** jobs.ca/LinkedIn/adzuna mirror the same req under multiple URL variants (caught Amicis, TCS, OSI Digital, Pacer twins this run).
3. **fresh=398 from daily_job_scan is not net-new.** The scan dedupes against existing jobs.json internally; only 37 URLs were actually absent from origin/main:jobs.json. Diff URL sets against the previous origin commit before reporting additions.
4. **`python3` on PATH is the Windows Store stub.** Run repo Python tools with `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe` (build_site.py, sync_readme_counts.py).
5. **Native Windows programs (curl, git, node, python) do not translate MSYS paths.** Pass native `C:/...` or relative paths; never `/tmp` to curl/git/node. Write curl `-o` output to a relative repo path (e.g. `raw/`) or grep stdout directly.
6. **gh run list works** from this host for polling; `gh workflow run pages.yml` triggers a deploy after a `[skip ci]` data push (pages.yml won't auto-trigger on `[skip ci]`).
7. **Cap behavior is normal.** A daily_job_scan run recaps jobs.json (~5,600 -> ~5,600 this run; secondary tags capped at 40, primary SN/SF unlimited). Site counts stay ~842/911 SN/SF — judge the run by fresh SN/SF URLs present in live jobs-data.json, not by raw row counts.
8. **Entry-level Salesforce signal:** "Salesforce Developer 1" / intern titles (Celestica) and "Platform Developer" titles (Altus) best match the user's Platform Developer I / entry-level brief; prioritize these over "Architect/Lead/Tech Lead" senior roles.
9. **Board invariants are pre-existing red on main** (outside-window postings, vendor sales, split rows) — none caused by this run; do not let a red invariant block a verified merge.

## Sources consulted this run
Adzuna CA API, Workday CXS (bmo, td, cibc, manulife, interac, salesforce, accenture, gdit, bdo, altusgroup, iko, moneris, irvingoil, mckesson, brookfield, resolvetech), LinkedIn guest, SmartRecruiters, Greenhouse, Lever, Ashby, remote boards, Rogers jobs.rogers.com, Bell jobs.bell.ca, Altus Group, Moneris, Celestica, TD Bank, BMO.

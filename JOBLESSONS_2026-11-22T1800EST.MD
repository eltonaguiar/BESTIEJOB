# JOBLESSONS_2026-11-22T1800EST

Hourly Toronto ServiceNow / Salesforce scan — Sunday 2026-11-22 18:00 EST (UTC-05).
Board: github.com/eltonaguiar/BESTIEJOB (main), pages: eltonaguiar.github.io/BESTIEJOB/

## Result this run
- Fresh verified jobs merged: **1**
- Twin URLs suppressed (not added): **36**
- Commit: `9e7f1bf` `chore(jobs): hourly scan 2026-11-22 18:00 EST — +1 verified new Toronto Salesforce posting (INNOVA Salesforce Specialist); suppressed 36 Adzuna/LinkedIn id-recycle twin URLs [skip ci]`
- Pages deploy: **success** (run 45082815589); live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` verified to carry the new URL (4,930 jobs on site, matching local build)

## New verified job (added to README Salesforce table, jobs.json, and live page)

| Posted | Role | Company | Location | Notes |
|---|---|---|---|---|
| 2026-11-22 | Salesforce Specialist | INNOVA | Toronto, Ontario, Canada | Posted today; LinkedIn deep link https://ca.linkedin.com/jobs/view/salesforce-specialist-at-innova-4492364527 ; not previously on the board (URL, company + title + city all clear) |

## Dedup checks performed against README.md + jobs.json + APPLIED.md (skipped, not added)

36 twin URLs surfaced by the scan were suppressed. Pattern: Adzuna re-issues the same role under a new `adzuna.ca/details/<id>` with a shifted `created` date, and LinkedIn reposts the same req under a new job id — so URL-only dedupe under-reports saturation; the twin-check must match company + title + city (+date).

Representative skips:

| Candidate | Why skipped |
|---|---|
| Adzuna 5972002660 — ServiceNow Business Analyst - Senior, Amigis Global, Toronto | Same role already on board via adzuna.ca/details/5972983023 (id recycle, date shifted 11-19→11-20) |
| LinkedIn 4491845382 / 4491853255 — Senior Salesforce Developer, TCS, Toronto | Both are twins of the board's existing TCS "Salesforce Senior Developer" (jobs.ca, 11-18); same title words + company + city + date |
| LinkedIn 4490380189 — ServiceNow CMDB Administrator, BMO, Toronto | Already on board via builtintoronto.com (11-17) |
| Workday bmo.wd3 — ServiceNow Technology Lifecycle Analyst, Toronto | Already on board via bmo.wd3 Workday R260030995 (11-12) |
| Adzuna 5975311384 / 5975311367 — Intact Back-End Email Developer (Salesforce Marketing Cloud) × EN+FR | Same role already on board via adzuna.ca/details/5968012098 (11-16, Canada-wide); adzuna id recycle |
| LinkedIn 4483476940 — Salesforce Platform Developer, Altus Group, Toronto | Already on board via simplyhired.ca mirror (11-11) |
| Linkedin 4491325080 — Salesforce Architect (Loyalty & Data 360), Konrad | Already on board via adzuna.ca/details/5972733701 (11-20) |
| Adzuna 5963223318/5963219598/5963222927 — OSI Digital Salesforce roles, Toronto | Already on board under other adzuna ids |
| Jobgether 5974899621 — Salesforce Business Process Analyst | Twin of board row adzuna.ca/details/5974901121 |

## Partner / sponsor / target-employer sweep

**Workday CXS retry (post-:00Z)** — all 10 probes returned HTTP 200 (BMO, TD, CIBC, Manulife, Interac × servicenow/salesforce; spaced ≥10s, Content-Type/Accept/Origin headers only, no Referer, `--compressed`): no fresh platform roles. BMO's CMDB Administrator and Technology Lifecycle Analyst, and TD's Senior Solution Architect (ServiceNow), are already on the board. Do not probe Workday at :00Z — CI owns that minute and 429s everything.

**Rogers** — `jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc` renders in a browser (date-sorted table, e.g. "Developer | Toronto | Nov 22") but shows **0 ServiceNow/Salesforce platform postings** (generic roles: Client Relationship Manager, Sales Associate, Manager Finance…). Rely on LinkedIn/Adzuna for Rogers rows; check weekly, not hourly.

**Bell** — `jobs.bell.ca` shows 0 SN/SF platform reqs. Bell-backed ServiceNow hiring runs under **Ateko / FX Innovation**.

**Ateko / FX Innovation** (Bell-backed ServiceNow partner) — `fxinnovation.com/en/jobs` checked: current postings are GCP Cloud DevOps Professional and Payroll Technician — no SN/SF platform vacancy. Portal recorded as a source to revisit; no job added.

**Canadian government / public sector** — Job Bank keyword search returns a search shell only (`servicenow in various locations - Search`, no actionable platform rows); `gojobs.gov.on.ca` and `jobs.gc.ca` are Radware-walled. No fresh SN/SF platform posting. Trust only Job Bank hits whose *title* names the platform.

**Adzuna variant sweep** (now platform, servicenow discovery/service mapping/csdm/catalog/service desk, itsm analyst, salesforce omnistudio/revenue cloud/data cloud/service cloud/community cloud, agentforce × Toronto/Canada, max_days_old=7): ~200 hits across 18 queries; all already tracked or non-platform (sales executives, marketing ops, counsel, recruiters). No additions.

## Lessons for future agents

1. **Adzuna id recycling is the dominant noise source.** The same role returns under new `adzuna.ca/details/<id>` with a shifted `created` date (Amigis 5972002660 → 5972983023; Intact 5968012098 → 5975311384/67). Always twin-check company + title + city + date against `git show origin/main:jobs.json`, README, and APPLIED.md before counting a scan hit as new.
2. **URL-only dedupe is insufficient.** Jobs.ca mirrors LinkedIn reqs under multiple URL variants; Altus "Salesforce Platform Developer" was already on the board via simplyhired under a different URL (caught by company+title+city, not by URL).
3. **Workday CXS 429s at :00Z (CI hour).** Manual probes succeed with ≥10s spacing a few minutes after the CI commit, using `Content-Type`/`Accept`/`Origin` headers only (no Referer) and `curl --compressed`. This run: all 10 Canadian-tenant probes HTTP 200, zero fresh platform roles.
4. **LinkedIn guest search is intermittent but reliable as a deep-link source.** Today's only genuine new job came from LinkedIn (INNOVA Salesforce Specialist, posted today). Retry once on empty responses; never infer platform content from the card title alone — read `.jobs-description`/body text before accepting.
5. **When 1–3 verified new jobs are found, insert textually into `jobs.json` (head of the `jobs` array), bump `meta`, regenerate the README `<!-- DAILY-SCAN -->` block from the pruned feed, run `tools/build_site.py`, then commit `jobs.json`, `README.md`, `public/*`, `FRESH_JOBS.md` together.** Do not run `tools/sync_readme_counts.py` after a scan rewrite — it would replace the board-total "N live postings" header with a table-row count and break the convention seen in today's committed blocks.
6. **Never commit mirror URLs that double-list roles already on the board.** When a scan finds 0 net-new roles, output a lessons-only `[skip ci]` commit instead.

## Sources consulted
Adzuna CA API (36 standard queries + 18 variants), Workday CXS (BMO, TD, CIBC, Manulife, Interac, Salesforce.com, GDIT, Altus, CAAT Pension, etc.), LinkedIn guest search (ServiceNow/Salesforce × Toronto/Canada, f_TPR=r86400), SmartRecruiters (ServiceNow), Greenhouse/Lever/Ashby boards, RemoteOK/Jobicy/Remotive, Rogers jobs.rogers.com (date-sorted), Bell jobs.bell.ca, Ateko/FX Innovation fxinnovation.com/en/jobs, Job Bank (servicenow), APPLIED.md, dead_urls.txt.

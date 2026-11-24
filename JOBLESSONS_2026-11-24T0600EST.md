# JOBLESSONS — hourly scan 2026-11-24T06:00EST (Toronto time)

Scan window: Tuesday 2026-11-24 06:00 EST (11:00 UTC). BestieJob hourly cron run.
Board: github.com/eltonaguiar/bestiejob (main). GitHub Pages: https://eltonaguiar.github.io/BESTIEJOB/

## Result

**0 net-new verified Toronto ServiceNow/Salesforce jobs added this cycle. Zero roles removed.**
Zero new verified jobs is a valid result per the runbook; an unavailable source is not a zero. Every lead surfaced this cycle either already exists on the board, failed the freshness/build/eligibility test, or is a past-deadline posting. No README.md table rows were added.

## Leads checked and disposition

**Already on the board — skipped (dedupe by URL/ID held):**

| Lead | Source | Board location |
|---|---|---|
| BMO — ServiceNow CMDB Administrator (R260030992, Workday, published 2026-11-12, Toronto, Discovery/Service Mapping/HAM) | bmo.wd3.myworkdayjobs.com | README line 280, via kilo-bestiejobs-v2--2026-11-14. Detail at jobs.bmo.com now says "the job you are trying to apply for has been filled" — treat as closed, do not re-add. |
| BMO — ServiceNow Technology Lifecycle Analyst (R260030995, Workday, 2026-11-12, Toronto) | bmo.wd3.myworkdayjobs.com | README line 281 — already on board. |
| Spectra Group Inc — ServiceNow Developer – Senior (CMDB/HAM/SAM, indeed jk=6d12ca9d15fb67dc, Toronto hybrid $100–110/hr) | Indeed / Workopolis / Dice | README line 275, posted 2026-11-05 via adzuna 5954288531. Indeed "New" tag is not freshness evidence. |
| Flexstaf IT — Request ID: 114262-1 Salesforce Communications Cloud Developer (Toronto hybrid) | adzuna.ca/details/5954288531 | README line 1048, posted 2026-11-05 — already on board. |
| Lane Four — Salesforce Administrator (lanefour.com/job-posting/salesforce-administrator/) | Lane Four | README line 963, posted 2026-11-09 — already on board. |
| Lane Four — Salesforce Consultant (LinkedIn 4487341676, Toronto) | LinkedIn | Already on board via hermes-agent--2026-11-09--v88.md; consultant/admin titles not auto-verified as build roles per runbook. |

**Freshness / scope failures — not added:**

| Lead | Reason |
|---|---|
| Cognizant — ServiceNow Sr Technical Consultant (00070349441, us-en, remote Canada) | Applications accepted till 11/20/2026 — elapsed deadline. Not on board; do not add as fresh. |
| Cognizant — ServiceNow Technical Consultant (00070336611, ca-en) | Applications accepted till 11/20/2026 — elapsed deadline. Not on board; do not add as fresh. |
| ServiceNow careers — Ontario page | Current listings are sales roles (Sales Director CRM, Cyber Advisory Solution Consultant, Account Execs, Sr Mgr Sales Cyber, Value Excellence) — no platform/build roles. |
| Wawanesa — Salesforce Lead Developer | jobs.wawanesa.com row is Winnipeg MB (hybrid), not Toronto; eluta mirrors not re-verified as fresh this cycle. |
| Flexstaf IT — Senior ServiceNow Consultant (LinkedIn 4492170849) | Already on board (README line 185, 2026-11-19). |

**Source sweeps with nothing net-new:**

- API watchlist pass (documented public ATS APIs via scan_boards.py --read): Lever alimentiv/eqbank/versapay, Greenhouse levio, Ashby solink/cea, SmartRecruiters ensiti. No dated Toronto platform leads; eqbank "Senior ServiceNow Engineer" and versapay "Salesforce Developer (Canada Remote)" are already-known watchlist evidence URLs with no posted date → leads only, not fresh feed. Levio roles are Montréal/Québec-only and dated Jul–Oct 2026. Ensiti "Salesforce Consultants (remote Canada)" released 2026-10-05 — stale.
- Cognizant careers: nothing net-new beyond already-boarded reqs (00071305431, 00071207741, 00070679681, 00071231443, 00071303921, 00071295741, 00071198961, 00071295401, 00071198961, etc.).
- ServiceNow careers Ontario page: sales roles only; no platform/build roles.
- Employer-direct re-checks this cycle: Rogers (jobs.rogers.com Technology: no platform roles), Bell/Ateko (FX Innovation portal not enumerable; ADP portal separate), Canada Life, TD/BMO/CIBC/Manulife Workday CXS (HTTP 422/429 — site names still need re-discovery via careers pages), Government of Canada/Job Bank (September–October 2026 postings only, stale).

## Source lessons for future agents

1. Indeed "New" tag and ZipRecruiter "New" badge are not freshness evidence — the Spectra Group Senior ServiceNow Developer surfaced as "New" today but was posted 2026-11-05 and is already boarded. Always dedup by URL/posting ID before counting as new.
2. BMO Workday list rows can remain published while the jobs.bmo.com detail says "filled" — conflicting liveness signals. When the employer apply route says filled, do not add even if the Workday list row still shows.
3. Elapsed application deadline (Cognizant roles closed 11/20/2026) ⇒ not fresh; do not add. Preserve as evidence only.
4. ServiceNow careers' Ontario location page currently lists sales roles only; platform/build roles for Toronto appear via the global careers job search, not the /locations/ams/ontario-canada/ page.
5. Lane Four Salesforce Consultant/Administrator are already boarded; per runbook, consultancy consultant/administrator titles need duty-level platform-build evidence before entering the developer track — never auto-enter on title alone.
6. Workday CXS probes for bmo/td/cibc/manulife still return HTTP 422/429 — re-discover site names via employer careers pages before probing again.
7. This cycle's productive pattern (Indeed date-sorted search + Cognizant careers + employer-direct) is now yielding diminishing returns on repeat passes; rotate to the weekly partner pass next (Pentio, NewRocket, Fujitsu, Atego/FX Innovation, Slalom, CloudFulcrum) per the runbook cadence.

## Next cycle (2026-11-24T07:00 EST)

- Re-check Cognizant careers (active dated posting pattern; check for reqs posted 2026-11-23/24).
- Re-run Indeed CA date-sorted ServiceNow + Salesforce Toronto search.
- Re-discover Workday CXS site names for bmo/td/cibc/manulife via their careers pages.
- Re-check Deloitte Canada platform openings (CMDB/Platform/Salesforce tracks — consistent weekly producer).
- Weekly partner pass: Pentio, NewRocket, Fujitsu, Atego (FX Innovation / ADP), Lane Four duties review, Slalom, CloudFulcrum.

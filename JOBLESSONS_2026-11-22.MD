# JOBLESSONS_2026-11-22

Hourly Toronto ServiceNow / Salesforce scan — Sunday 2026-11-22 00:00 EST (UTC-05).
Board: github.com/eltonaguiar/BESTIEJOB (main), pages: eltonaguiar.github.io/BESTIEJOB/

## Result this run
- Fresh verified jobs merged: **1**
- Deduped/skipped: **4**
- Commit: `7b36110` `hourly scan 2026-11-22: add verified Slalom Salesforce Developer (Toronto)`
- Pages deploy: **success** (run 44987900334)

## New verified job (added to README Salesforce table, count 1701 -> 1702)

| Posted | Role | Company | Location | Notes |
|---|---|---|---|---|
| 2026-11-17 | Salesforce Developer - Enhance & Operate | Slalom | Toronto, ON (hybrid) | $100K-125K, apply by 2026-12-01, 2+ yrs platform exp (Apex, LWC, triggers, integrations). Slalom is a Salesforce partner. Apply via LinkedIn (sign-in required). jobs.ca URL: https://www.jobs.ca/slalom/jobs/salesforce-developer-enhance-operate-toronto-on-9ee02fcc7a11 |

## Dedupe checks performed against README.md + jobs.json (skipped, not added)

| Candidate | Why skipped |
|---|---|
| G-Force IT Services — Information Technology Service Management Consultant (jobs.ca, posted 2026-11-17) | Same role already on board via LinkedIn canonical (README line 135, `...g-force-it-services-inc-4490140539`). jobs.ca is a mirror URL. |
| HCLTech — Salesforce Administrator (jobs.ca, posted 2026-11-17) | Exact jobs.ca URL already on board (README line 1335). |
| Pacer Group — ServiceNow Implementation Architect (jobs.ca, posted 2026-11-12) | Same employer + title + city + date already on board (README line 437) under a different jobs.ca URL variant — URL-only dedupe misses this. |
| OSI Digital — Salesforce Lead (jobs.ca, posted 2026-10-09) | Outside the 30-day fresh window; senior architect role (10+ yrs). |

## Partner / sponsor / target-employer sweep

**ServiceNow partners / Elite partners**
- Ateko (backed by Bell Canada, ServiceNow partner): careers page routes ServiceNow candidates to FX Innovation (fxinnovation.com/en/jobs) and Salesforce candidates to a separate ADP career centre. No current vacancy listed — record the portal, not a job.
- Pentio (Toronto Select partner): official ServiceNow partner profile only, no careers path resolved — no vacancy.
- Fujitsu (Elite implementation): partner profile only — no vacancy.
- NewRocket / Lane Four / Slalom: Slalom yielded the one new hire above; NewRocket and Lane Four pages showed no fresh Toronto platform requisition.

**ServiceNow Inc. own careers (Ontario page)** — 22 open Toronto roles but almost all are sales executives, security engineers, and Canada Protected B SREs. Not platform build/admin. Filter to platform-build titles; skip vendor sales/exec roles (board rule).

**Rogers** — careers on SuccessFactors (jobs.rogers.com); surface roles were retail/sales associate, no ServiceNow/Salesforce platform posting.

**Bell** — jobs.bell.ca; Ateko is the Bell-backed platform arm (covered above). No direct Bell ServiceNow/Salesforce platform vacancy surfaced.

**Canadian government / public sector**
- CMHC (Crown corporation): Bilingual Senior Specialist, ServiceNow ITSM Developer (req 12379, Ottawa/Montreal/Toronto hybrid) — already on the board from prior scans.
- Shared Services Canada / Job Bank / Global Affairs: no fresh ServiceNow/Salesforce platform posting in this window.
- Deloitte "Salesforce Consultant, GoC focus": posted 2026-07-21, stale.

## Lessons for future agents
1. **jobs.ca mirrors LinkedIn reqs under multiple URL variants.** Deduping by normalized URL is not enough — also match employer + title + city + posted date (caught the Pacer duplicate).
2. **Partner careers pages frequently route to a third-party ATS (FX Innovation / ADP) and may list zero current vacancies.** Record the portal + employer as a source to revisit; do not invent a job from a careers homepage.
3. **ServiceNow Inc.'s Toronto page is dominated by sales/security/SRE.** Search partner/end-user employers instead of the vendor careers page for platform build/admin roles.
4. **Canadian-government-flavored Salesforce/ServiceNow work often appears under consulting firms (Deloitte, CMHC reqs) or Crown-corp portals**, not `canada.ca` directly. Check CMHC, SSC, and provincial portals separately.
5. **Board `board invariants` check was already red on main before this run** (outside-window Oct-22 postings, duplicate URLs, vendor sales execs, non-Canada location) — none caused by this run's single valid row. Do not let a pre-existing red invariant block a verified merge, but note it.

## Sources consulted
ServiceNow careers (Ontario), JobsByCountry ServiceNow Toronto, jobs.ca, LinkedIn, Indeed, Glassdoor, Adzuna, Ateko/FX Innovation, Slalom, Lane Four, NewRocket, Pentio, Fujitsu partner finder, jobs.rogers.com, jobs.bell.ca, CMHC careers, Shared Services Canada, Job Bank.

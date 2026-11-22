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
ServiceNow careers (Ontario), JobsByCountry ServiceNow Toronto, jobs.ca, LinkedIn, Indeed, Glassdoor, Adzuna, Atego/FX Innovation, Slalom, Lane Four, NewRocket, Pentio, Fujitsu partner finder, jobs.rogers.com, jobs.bell.ca, CMHC careers, Shared Services Canada, Job Bank, gojobs.gov.on.ca, jobs.gc.ca.


## Hourly scan — Sunday 2026-11-22 01:00 EST (UTC-05)

### Result this run
- Fresh verified jobs merged: **0** — no new unique roles to add
- Source postings scanned: **414** (adzuna 196 · linkedin 182 · smartrecruiters 12 · greenhouse 14 · remote-feeds 7 · lever 1 · ashby 2)
- Workday CXS: **0** — all 15 Canadian tenants (BMO, TD, CIBC, Manulife, Interac, CAAT Pension, GDIT, Accenture, Salesforce, etc.) returned HTTP 429; the CI hourly scan owns the :00Z minute
- Deduped/skipped: **39** URL variants surfaced by the scan — every one is a company+title twin already on the board under an alternate URL (e.g. BMO "ServiceNow CMDB Administrator" already on board via LinkedIn and fresh-ca scan URLs; TD "Senior Solution Architect (ServiceNow)" via adzuna.ca/details/5970088512 + TD Workday)
- Board unchanged: jobs.json stays at 5,561 rows (1,188 ServiceNow / 4,273 Salesforce primary-tagged); no jobs.json, README.md, or public/ commit — committing mirror URLs would double-list roles already on the board

### Dedupe evidence (all 39 scan "additions" already on board)
- Cloud Resourcing "CLDRSRC10472 - Project Manager - ServiceNow - ITSM/ITOM/CSM - Toronto - Hybrid" → already on board via README adzuna.ca/details row
- La Caisse "Développeur(-euse), ServiceNow" → already on board
- Capco "Full-Stack Software Developers" → already on board
- ServiceNow "Principal Solution Architect- ServiceNow" (Toronto) → already on board via builtin.com/job/principal-solution-architect-servicenow/11971031
- Benevity "Senior Salesforce Administrator" → already on board via communitech.ca and adzuna.ca/details/5949576662
- Alimentiv "ServiceNow Platform Specialist" (Toronto + London, ON) → already on board via adzuna.ca/details/5946002922 / 5946002886 / 5946002306

### Partner / sponsor / target-employer sweep (re-checked this window)
- **Rogers** — jobs.rogers.com (Phenom) renders a page shell with zero server-side job rows; no ServiceNow/Salesforce platform posting. Check weekly, not hourly.
- **Bell** — jobs.bell.ca shows zero ServiceNow/Salesforce platform reqs; Bell-backed SN hiring appears under Ateko/FX Innovation, no fresh vacancy listed this window.
- **Canadian government / public sector** — gojobs.gov.on.ca and jobs.gc.ca are Radware-walled (captcha); Job Bank keyword search is noisy (trust title-only matches); CMHC, Shared Services Canada, Global Affairs: no fresh SN/SF platform posting.

### Lessons for future agents
1. Workday CXS 429s on all Canadian tenants at the top of the hour (CI hourly scan at 03:00 EST / 08:00Z). Manual Workday probes succeed ~4 minutes after the CI commit with ≥8s spacing between 3–10 tenants — never probe Workday at :00Z.
2. Adzuna/LinkedIn are saturated for Toronto SN/SF: every source posting this run matched an existing board row. URL-only dedupe under-reports saturation — always twin-check employer + title + city + date before claiming a "new" job.
3. `fresh=N merged=M` from the scan counts source hits, not net-new board rows — diff URL sets against `git show HEAD:jobs.json` before reporting additions.
4. When 0 net-new jobs are found, do not commit mirror URLs to jobs.json — double-listing breaks the employer+title card clustering on the live page; a lessons-only `[skip ci]` commit is the correct output.

## Hourly scan — Sunday 2026-11-22 07:00 EST (UTC-05) (this run)

### Result this run
- Fresh verified jobs merged: **0** — every fresh candidate was already tracked or failed verification
- Sources scanned: Adzuna CA API (servicenow/salesforce × Toronto/Ontario, max_days_old=3); Workday CXS (BMO, TD, CIBC, Manulife, Interac, Accenture, Salesforce.com × ServiceNow/Salesforce); Phenom (jobs.scotiabank.com, jobs.rogers.com × q=servicenow/q=salesforce, date-sorted); LinkedIn guest search (ServiceNow & Salesforce, Toronto/GTA, f_TPR=r86400, 60 cards each); Dice.com Toronto page 1 (servicenow/salesforce)
- Fresh LinkedIn hits, all **already on the board**: Altus Group "Salesforce Platform Developer" (Toronto, 20h ago, CAD 105–115k); Deloitte "Senior Consultant, AI – NowAssist" (Toronto, 17h ago — NowAssist is ServiceNow's GenAI product, genuine SN platform role); Moneris "Principle Salesforce Developer" (Toronto, 17h); Scotiabank "DevOps Engineer(Salesforce)" (Toronto, 21h)
- Verified then **excluded**: S M Software "Software Developer – CRM – Intermediate" (Toronto, 10h) = Oracle Siebel IP18/Open UI, not Salesforce; DEPT "CRM Campaign Managers (Talent Pool)" (Toronto, 17h) = not a live role
- Phenom and Dice surfaces: keyword noise / no fresh Canadian platform rows (Rogers 0 ServiceNow rows; Scotiabank hits = incident mgmt/security/sales only)
- Board unchanged: no jobs.json, README.md, or public/ commit — no net-new rows to add this hour

### Lessons this run
1. LinkedIn guest search intermittently returns 0 cards on a live query (Salesforce/Toronto returned 0 once, 60 cards on retry) — retry before declaring a source empty.
2. Workday CXS returned HTTP 200 on all 14 Canadian-tenant probes (probed after :05Z, `curl --compressed`, Content-Type/Accept/Origin headers only, no Referer); freshest platform hit was BMO ServiceNow CMDB Administrator at 10 days — nothing fresh enough to add.
3. Adzuna returns HTTP 503 when queries repeat faster than ~3s — space calls ≥3s, retry once; the API param is `content-type`, not `content_type`.
4. "CRM" in a title ≠ Salesforce: confirmed exclusions were Oracle Siebel (S M Software) and a DEPT talent-pool ad (explicitly not a live role).
5. When 0 net-new jobs are found, the correct output is a lessons-only `[skip ci]` commit — do not commit mirror URLs that would double-list roles already on the board.

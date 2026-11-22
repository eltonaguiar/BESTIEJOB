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

## Hourly scan — Sunday 2026-11-22 09:00 EST (UTC-05) (this run)

### Result this run
- Fresh verified jobs merged: **0** — every fresh candidate was already tracked or failed verification
- Sources checked: Adzuna CA retry output (servicenow/salesforce × Toronto/Ontario, created 2026-11-21 → 2026-11-22); live web searches (LinkedIn guest, Indeed, Glassdoor, Built In) for Toronto SN/SF posted Nov 20–22
- Fresh candidates checked against README.md + jobs.json — all dupes or excluded:
  - Cognizant "Salesforce Tech Lead (Remote)" Toronto, adzuna 5974890709 / 5973912092, posted 2026-11-22 → already on board via LinkedIn 4492842720 (README line 40, posted 2026-11-20); mirror URL, same employer+title+city
  - IBM "Salesforce Senior Solution Architect" Toronto, adzuna 5973912179, posted 2026-11-21 → already on board via fresh-ca--2026-11-22--v1.md (adzuna canonical row)
  - Novartis "SFMC Manager" Toronto → already on board via LinkedIn 4491648837 (README line 896, posted 2026-11-19)
  - ServiceNow "Senior Systems Engineer" Toronto, adzuna 5973912516 → already on board via SmartRecruiters 744000162621080 (README line 79, posted 2026-11-20); mirror URL
  - ServiceNow sales roles (Cyber Advisory Solution Consultant, Solution Sales Executive Moveworks, Sr Mgr Sales Cyber, Toronto) → vendor sales execs, excluded by board rule
  - BMO "ServiceNow SAM Administrator - ITAM" R260030096 → already on board since 2026-11-09 (README lines 467/586/587)
  - Procom "Senior ServiceNow Developer" Toronto 2a757e2b, posted 2026-11-04 → already on board (README line 603)
  - Remaining web-search hits (CareerBeacon GTT/Forhyre/Nityo, Movo/Spectraforce, Built In Brookfield/Acronym) → posted 4–29 days ago or closed; previously tracked or out of window
- Board unchanged: no jobs.json, README.md, or public/ commit — no net-new rows to add this hour

### Lessons this run
1. Adzuna CA API returned HTTP 503 on repeated salesforce queries — space calls ≥3s, retry once; the API param is `content-type`, not `content_type`
2. URL-only dedupe under-reports saturation — always twin-check employer + title + city + posted date before claiming a "new" job (caught again with the Cognizant Tech Lead mirror URL)

## Hourly scan — Sunday 2026-11-22 10:00 EST (UTC-05) (this run)

### Result this run
- Fresh verified jobs merged: **0** — no new unique roles to add
- fresh_ca_scan (Adzuna CA API `max_days_old=2, sort_by=date` across servicenow/salesforce/ITSM/CMDB/ITAM queries, `where=` national + Toronto, Ontario + Ontario; Job Bank 12 pages; Eluta 6 pages): 110 raw rows → 15 unique → 0 kept; all 15 already on the board by normalized URL (reports/fresh_ca_2026-11-22.json, inbox/fresh-ca--2026-11-22--v3.md; stats: requests 68, jobbank_pages 12, eluta_pages 6, unverified_dropped 0, already_on_board 15)
- The 09:00 EST GitHub Actions hourly scan (commit 2fe967b) had already merged today's aggregator batch into README.md: 34 rows dated 2026-11-22 (12 ServiceNow, 12 Salesforce, 10 Other); top scan block "Scan: 2026-11-22T14:02:19.526Z · 2294 live postings from 7 public sources". GitHub Pages redeployed 09:36 EST and is current with the board.
- Board unchanged: no jobs.json, README.md, or public/ commit — no net-new rows to add this hour

### Partner / sponsor / target-employer sweep (re-checked this window)
- Rogers (jobs.rogers.com): ServiceNow/Salesforce appear only as adjacent tools in delivery/sales/marketing-ops roles (Technical Specialist Markham, Delivery Specialist Toronto, Digital Campaigns Manager, Client Relationship Manager) — no platform dev/admin posting; not added.
- Bell (jobs.bce.ca): ServiceNow System Administrator and Senior Technical Advisor postings (Oct 6, apply-by Oct 20) expired; 2027 Grad/Intern programs mention SF/SN familiarity but are not platform roles.
- Canadian government (jobs.gc.ca): no fresh ServiceNow/Salesforce platform posting surfaced.
- Elite/solution partners (KPMG — ServiceNow Global Elite Partner, Slalom, Accenture, Deloitte, CGI, Cognizant, NeuraFlash): KPMG Sr Consultant ServiceNow Toronto (apply-by Nov 9) expired; no fresh Toronto platform roles found.

### Lessons this run
1. When 0 net-new jobs are found, the correct output is a lessons-only `[skip ci]` commit — do not commit mirror URLs that would double-list roles already on the board.
2. fresh_ca_scan with the public Adzuna demo key is slow (~7.5 min for 68 Adzuna + Job Bank + Eluta calls without LinkedIn) — time-box it; the CI hourly scan at :00Z already covers Adzuna/LinkedIn/Job Bank/Eluta, so the manual sweep adds most value on the partner/employer targets the aggregators miss.
3. URL dedupe held this hour: all 15 unique scan rows were already on the board under the same normalized URL — because the 09:00 EST scan already published today's batch, URL-only dedupe was sufficient.


## Hourly scan — Sunday 2026-11-22 12:00 EST (UTC-05) (this run)

### Result this run
- Fresh verified jobs merged: **0** — every fresh candidate was already tracked, expired, outside the fresh window, or not a ServiceNow/Salesforce platform role
- Base commit: `77ce9de` (11:14 EST hourly scan refresh, 5600 listings: Adzuna 190 · LinkedIn 152 · Workday 17 · Greenhouse 14 · Lever 1 · Ashby 2 · SmartRecruiters 12 · Remotive 6; 1195 ServiceNow / 4285 Salesforce primary-tagged)
- Direct-employer postings dated Nov 21–22 checked: Deloitte, Envision Technology, Procom, CIBC (jobs.ca); LinkedIn guest search
- Board unchanged: no jobs.json, README.md, or public/ commit — no net-new rows to add this hour

### Dedupe / exclusion checks (README.md + jobs.json)
| Candidate | Disposition |
|---|---|
| Deloitte — Senior Consultant, IT Operations Management / Discovery (ServiceNow team), Toronto, jobs.ca 96d8925e69f7 | Already tracked in jobs.json under LinkedIn canonical `4460512143`; posting dates Nov 14 / 27d ago on mirrors — outside fresh window either way |
| Envision Technology — ServiceNow ITOM Developer, Toronto | Same requisition already on board via LinkedIn `4492816283` (posted 2026-11-20); jobs.ca "Nov 21" is a mirror re-date |
| Deloitte — Lead Specialist, ServiceNow CMDB Solution Architect, Toronto, jobs.ca 1791c72ef02a | Already on board since 2026-11-14 under the same jobs.ca URL |
| Deloitte — Senior Consultant, AI – NowAssist, Toronto, posted Nov 21 | Already tracked in jobs.json under LinkedIn canonical `4460501313` |
| CIBC — IT Administration Analyst, Toronto, posted Nov 21 | Excluded: ServiceNow SRM access provisioning, not a platform build/admin role |
| Procom — IT Operations & Service Transition Consultant (ITSM), Toronto, Nov 21 | Generic ITSM; ServiceNow optional — not an SN role |
| Bell — ServiceNow System Administrator, Toronto | Expired (apply-by Oct 21, 2026) |
| Government of Canada — Senior Salesforce Developer (LinkedIn 4481939757) | Posted Nov 18; SECRET clearance; location not Toronto-confirmed; outside window |

### Partner / sponsor / target-employer sweep
- **Rogers** (jobs.rogers.com, Phenom): page shell renders zero server-side rows; no ServiceNow/Salesforce platform posting
- **Bell** (jobs.bell.ca): no fresh SN/SF platform requisition; the ServiceNow SysAdmin role expired Oct 21
- **Canadian government** (jobs.gc.ca): Radware captcha wall; no fresh platform posting surfaced
- **Salesforce Canada careers**: sales/Customer Success hiring only; no platform dev/admin posting surfaced

### Lessons this run
1. Employer mirrors re-date old requisitions — Envision ITOM and Deloitte CMDB Architect showed "Nov 21" on jobs.ca but are already tracked under older URLs; dedupe on employer + title + city, not the mirror's posted date.
2. jobs.ca card dates can be stale — the Deloitte IOM/Discovery card said Nov 21 while careers.deloitte.ca shows Posting Start Date 1/21/26; verify on the employer canonical before trusting a date.
3. `git pull --ff-only` before merging: the 11:14 EST scan commit `77ce9de` landed while this run was scanning, so the dedupe base must be current.
4. "ServiceNow" in duties ≠ platform role — CIBC IT Administration Analyst (SRM access provisioning) and the Procom ITSM consultant (ServiceNow optional) were checked and excluded.
5. With 0 net-new jobs, the correct output is a lessons-only `[skip ci]` commit — do not commit mirror URLs that would double-list roles already on the board.

### Sources consulted
jobs.ca (Deloitte, Envision, Procom, CIBC), LinkedIn guest search, careers.deloitte.ca, Glassdoor/ApplyTOP date mirrors, jobs.rogers.com, jobs.bell.ca, jobs.gc.ca, Salesforce careers Canada, LinkedIn 4481939757, hourly scan commit `77ce9de`.

## Hourly scan — Sunday 2026-11-22 13:00 EST (UTC-05) (this run)

### Result this run
- Fresh verified jobs merged: **~30 net-new URLs** (jobs.json 5,600 → 5,630; SN 1,193 / SF 4,280)
- Base: origin/main `843c499` (CI 12:11 EST scan refresh, 5,600 listings)
- Local direct scan (`node scripts/daily_job_scan.mjs`, unpiped — piped/redirected runs exit `stdin is not a tty` on this host): fresh=382 source hits, merged=5,630 after URL dedupe + capSecondary
- Workday CXS: all 17 Canadian tenants HTTP 429 again this hour — rate-limited well past :00Z; carried 0 postings
- Freshest merged roles (posted Nov 21–22, not previously on board):
  - Jobgether — Salesforce Business Process Analyst, Canada (adzuna 5974899621, 2026-11-22)
  - Cognizant — Salesforce Tech Lead (Remote), Toronto (adzuna 5973912092, 2026-11-21)
  - Altus Group — Salesforce Platform Developer, Toronto (LinkedIn 4483476940, 2026-11-21)
  - Moneris — Principle Salesforce Developer, Toronto (LinkedIn 4466619394, 2026-11-21)
  - Euna Solutions — Sr Salesforce Developer, Oakville (LinkedIn 4492752341, 2026-11-20)
  - TD Bank — Senior Solution Architect (ServiceNow), Toronto (adzuna 5970077372, 2026-11-18)
  - Amicis Global — ServiceNow Business Analyst - Senior, Toronto (adzuna 5972002660, 2026-11-19)
- Commit: `77faf60` (8 files: jobs.json, README.md DAILY-SCAN block, FRESH_JOBS.md, public/ feeds); pages.yml deploy run 45053302232 → success (~32s)
- Live page verified: https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json serves 4,930 cards and contains BMO ServiceNow CMDB Administrator (Toronto) — a URL absent from the pre-scan board — confirming the deploy carried this run's data

### Partner / sponsor / target-employer sweep (re-checked this window)
- **Rogers** (jobs.rogers.com Phenom): zero server-side job rows; no SN/SF platform posting — rely on LinkedIn/Adzuna mirrors
- **Bell** (jobs.bell.ca): zero SN/SF platform requisitions; ServiceNow hiring surfaces under Ateko (Bell-backed) / FX Innovation, no fresh vacancy this window
- **Canadian government** (jobs.gc.ca, gojobs.gov.on.ca): Radware captcha wall; Job Bank keyword search noisy (trust title-only matches); CMHC/SSC/Global Affairs no fresh SN/SF platform posting
- **Salesforce/ServiceNow vendor careers**: vendor sales/SRE/security roles only; platform build/admin comes from partners and end-users (Altus, Moneris, Cognizant, TD, BMO, CGI, KPMG, Deloitte)

### Lessons this run
1. `node scripts/daily_job_scan.mjs` must run unpiped/unredirected on this host — `> file` or `| tail` makes it exit `stdin is not a tty` immediately without writing. Run it in the foreground so jobs.json/README/public actually get rewritten.
2. Push-rejection recovery: if `git push origin main` is rejected because the CI hourly scan committed first, do not hand-resolve the generated files — `git reset --hard origin/main`, re-run the scan + `tools/build_site.py`, recommit, repush.
3. Workday CXS 429s persisted all hour (18:06Z) on every Canadian tenant, not just the :00Z CI minute — treat Workday as CI-owned for hourly freshness.
4. Net-new ≠ source hits: `fresh=382` source hits collapsed to ~30 net-new URLs after dedupe — always diff URL sets against `git show origin/main:jobs.json` before reporting additions.

## Hourly scan — Sunday 2026-11-22 16:00 EST (UTC-05) (this run)

### Result this run
- Fresh verified jobs merged: **0** — board unchanged (no jobs.json, README.md, or public/ commit)
- Board base: origin/main `c3dcbd5`; jobs.json at `2026-11-22T18:06:40.456Z` scan (5,597 rows; 1,193 ServiceNow / 4,280 Salesforce primary-tagged); README DAILY-SCAN block `Scan: 2026-11-22T18:06:40.456Z · 5626 live postings from 7 public sources`
- Sources re-scanned this hour:
  - Adzuna CA live outputs (14:03 EST: servicenow/salesforce × Toronto/Ontario + ITOM Toronto) — 144 unique SN/SF postings across 13 files; **all already on board** by normalized URL or employer+title+city twin
  - LinkedIn guest search + today's LinkedIn scan artifacts — fresh SN/SF hits (TechNeptune CMDB Consultant, Blue Mantis Sr SN Business Process Consultant, Cognizant SF Tech Lead, Avanciers SF Developer/Architect/BSA, Euna Sr SF Developer) all **company+title dupes** of rows already on the board
  - Workday CXS manual retry at 16:03 EST (curl --compressed, Content-Type/Accept/Origin headers only, no Referer, ≥8s spacing) — **HTTP 422 on all 15 Canadian tenants** (BMO/TD/CIBC/Manulife/Interac/CAAT Pension/GDIT/Accenture/Salesforce.com × ServiceNow & Salesforce): Workday blocking probes this hour, not "zero postings" — logged as blocked, carried nothing
  - Phenom: jobs.rogers.com server-side shell = zero rows (re-checked); jobs.scotiabank.com date-sorted = incident/security/sales only; jobs.bell.ca = zero platform reqs (Bell-backed SN hiring runs under Ateko/FX Innovation — their careers page and LinkedIn show no fresh vacancy this window)
  - Canadian public sector: gojobs.gov.on.ca and jobs.gc.ca Radware-captcha walled; Job Bank OPS employer feed empty; no fresh SN/SF platform posting
- Detail checks: Lane Four (Toronto Salesforce partner) Salesforce Consultant and Salesforce Administrator pages both HTTP 200 but **no posted date** on either → undated, freshness unverifiable → not added; ServiceNow vendor sales roles (Cyber Advisory Solution Consultant, Solution Sales Executive Moveworks, Sr Mgr Sales Cyber, Toronto) excluded by board rule; CIBC IT Administration Analyst (SRM access provisioning, not platform build/admin) excluded; Procom ITSM consultant (ServiceNow optional, generic) excluded.
- Dedupe base: origin/main refreshed before scanning; every candidate matched an existing board row — 0 net-new.

### Board decision
- No jobs.json / README.md / public/ change: committing mirror URLs would double-list roles already tracked under canonical URLs. Correct output for 0 net-new is this lessons-only `[skip ci]` commit.

### Lessons this run
1. Saturation: all freshness vectors (Adzuna API, Workday CXS, LinkedIn guest) ran today and returned only board-known rows — always diff URL sets against `git show origin/main:jobs.json` and twin-check employer + title + city + date before reporting a "new" job.
2. Workday CXS returned HTTP 422 on every Canadian tenant at 16:03 EST, well past the :00Z CI minute — treat 422 as host/IP blocking, not as an empty board; do not log a 422 hour as zero fresh requisitions.
3. Undated partner pages (Lane Four) cannot be admitted as fresh without a posted date — fetch the detail page and skip when undated.
4. When 0 net-new jobs are found: lessons-only `[skip ci]` commit; never commit mirror URLs that would double-list roles.

### Sources consulted
Adzuna CA API (servicenow/salesforce/ITOM × Toronto/Ontario), LinkedIn guest search + scan artifacts, Workday CXS (BMO/TD/CIBC/Manulife/Interac/CAAT Pension/GDIT/Accenture/Salesforce.com), jobs.rogers.com, jobs.scotiabank.com, jobs.bell.ca, ateko.com + fxinnovation.com careers, Lane Four careers, Job Bank (OPS employer feed), gojobs.gov.on.ca, jobs.gc.ca, Salesforce/ServiceNow vendor careers pages.

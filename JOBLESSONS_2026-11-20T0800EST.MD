# JOBLESSONS — 2026-11-20 08:00 EST (13:00Z) hourly ServiceNow / Salesforce scan

Run context: Hermes cron hourly scan. Start `origin/main` = a720a48 (5,575 rows, CI 12:48Z sweep). Ran local `node scripts/daily_job_scan.mjs` (no flags) → fresh=530, merged=**5,603**; Workday 429 on every tenant again. Then browser LinkedIn: SN/SF × Toronto 24h + Canada 7d = 219 unique cards.

Outcome: **1 verified net-new** merged to README + site — Insight Global, *Product Owner* (Salesforce CRM required, insurance; 12-mo contract, $55–57/hr, hybrid Guelph/Toronto). Board 5,603→**5,604**; site **5,043 cards (SN 859 / SF 920 / other 3,264)**. Guards: `check_readme_sort` OK, `board_invariants` PASS (34 errors, no growth), `check_site_links` OK.

## The big lesson: jobs.json can be BEHIND README, not ahead

The local scan "added" 29 rows vs origin's jobs.json, and every one was **already visible on README**:

- ServiceNow (company): Staff Full-Stack Engineer ×2, Principal Solution Architect
- TD Bank: Associate Software Engineer (nCino/Salesforce), Senior Solution Architect (ServiceNow), Software Engineer III – Salesforce Data 360
- BMO: ServiceNow CMDB Administrator, ServiceNow Technology Lifecycle Analyst
- Deloitte: Senior Consultant, ServiceNow Platform (DTC)
- KPMG Canada: Consultant/Senior Consultant – ServiceNow Solution Developer
- Cognizant: ServiceNow SAM Developer, Salesforce Technical Architect
- OSI Digital: Salesforce Developer ×3 (Toronto ×2, Vancouver), Salesforce Lead, Salesforce BA, Salesforce QA Tester
- Tata Consultancy Services: Senior Salesforce Developer
- Altus Group: Salesforce Platform Developer
- Benevity: Senior Salesforce Administrator (Toronto ×2, Calgary)
- Alimentiv: ServiceNow Platform Specialist (Toronto, London)
- IKO: Salesforce Senior Developer (Mississauga)
- NeuraFlash: Salesforce Technical Architect (Remote – Colombia → non-Canada, do not promote)
- Apptoza: ServiceNow Business Analyst ×2

**Implication:** never assume "not in jobs.json" = "not on the board". The CI rebuilds jobs.json from sources each hour and can drop rows that the visible README (built by fresh-ca / gap sweeps) already carries. Dedupe must check README + APPLIED + jobs.json, which this run did. A jobs.json-only check would have re-added 29 duplicates.

## What worked

- **Browser LinkedIn DOM stayed the freshness oracle.** 4 queries → 60 cards each, no authwall after retries (SF Toronto rendered 0 once; a re-navigate + 4 scrolls fixed it). Unique 219; 147 tracked; 72 not; 52 after sales/marketing noise filter.
- **Body checks still decide generic titles.** Most "other" candidates were rejected by reading the sentence around the keyword, exactly as prior lessons warned.
- **Textual jobs.json insert + one README row + `build_site.py`** is a clean, low-diff merge for a single add. Window count bumped 6180→6181; new head row verified in `public/jobs-data.json` as family `other`.

## Rejected this hour (keyword = tool/example, not platform role)

- CI Financial — Service Desk Analyst ×2: ServiceNow is the ticketing tool (L1/L2 support). Reject.
- Manulife — Manager, Post Incident Reviews & Incident Mgmt: process role, no SN/SF in body.
- Scotiabank — Senior Analyst, Business Support Strategy & Incident Mgmt: no platform content.
- USask — Enterprise Service Management Specialist: "ESM/ITSM platforms, such as TeamDynamix, ServiceNow, Jira SM" (example list; Saskatoon).
- Endress+Hauser — Business Applications Specialist: "ERP/CRM (e.g., SAP, Salesforce)" (example list).
- Lyft — Sr TPM, Finance (Quote to Cash): "Zuora, Salesforce CRM, Oracle, Hubspot" (tool list).
- S M Software RQ11675 / RQ11846 — Microsoft Dynamics 365 CRM + MuleSoft (Ontario govt contracts). Not Salesforce.
- ThoughtStorm — Oracle Siebel CRM Developer (Siebel, not SF).
- Euna Integrations PM, Fidelity Technical Analyst Sr, WSP Workspace PM — previously-known example/tool matches.
- WSIB — Enterprise Risk Management Manager ×4 (Scarborough / Mississauga / North York / Hamilton): same role as the tracked Toronto row (4492156479); duplicates, skip.

## Partner / sponsor / tech-company watch (all already tracked)

Deloitte, KPMG, Cognizant, OSI Digital, TCS, IBM/LGS, Accenture, PwC, CGI, TD, BMO, ServiceNow (vendor), Salesforce (vendor), Altus Group, Benevity, Alimentiv, IKO. Rogers/Bell were not surfaced as fresh SN/SF cards this hour (their Workday boards 429'd); government roles arrived only via the S M Software RQ contracts (Dynamics, rejected).

Seen but off-target: Salesforce Inc — *Analytics Specialist SE (Commercial FINS & Canada)*, Vancouver, Senior/Lead pre-sales solution engineering. Real vendor role, but Vancouver + pre-sales → not added to a Toronto-first board.

## Source yields (for future agents)

- Local scan: fresh=530, merged=5603. Workday 0 (429 on bdo, medcan, altusgroup, iko, huron, irvingoil, mckesson, brookfield, gdit, resolvetech). Adzuna succeeded (210 matching). LinkedIn HTTP partially 429'd but returned 273 rows.
- Browser LinkedIn: SN Toronto 60, SF Toronto 60 (after retry), SN Canada 60, SF Canada 60 → 219 unique → 72 not tracked → 52 after noise filter → 1 added.

## Market pattern (Nov 20, 2026 — 08:00 EST)

Toronto SN/SF remains at practical saturation: 0 net-new ServiceNow Toronto cards, and the only SF Toronto non-matches were Dynamics 365 and Oracle Siebel. Net-new is now overwhelmingly (a) generic-title roles only a body read reveals, (b) city twins, (c) French-language Quebec rows. Expect ~0–2 visible adds per hourly pass. The scan's main value is reconciling jobs.json to README and refreshing the DAILY-SCAN top-12.

## Run recipe that worked

1. `git fetch` → `git reset --hard origin/main` (CI pushes hourly).
2. `node scripts/daily_job_scan.mjs` (writes jobs.json, FRESH_JOBS.md, README DAILY-SCAN block).
3. Browser LinkedIn: SN/SF Toronto `f_TPR=r86400`, SN/SF Canada `f_TPR=r604800`; re-navigate if a query returns 0.
4. Dedupe by URL + 10-digit job id against jobs.json **and README and APPLIED**; then company+title; never title-only.
5. Body-check every generic title via `/jobs/view/<id>` → `.jobs-description`; read the sentence around the keyword.
6. Textual insert at head of jobs.json, bump `meta.total`; insert README row at correct date position; bump window count.
7. `python tools/build_site.py`; `node scripts/check_readme_sort.mjs`; `python scripts/board_invariants.py`; `python scripts/check_site_links.py`.
8. Commit `[skip ci]`, push, trigger `pages.yml`, verify live `jobs-data.json` carries the new id.

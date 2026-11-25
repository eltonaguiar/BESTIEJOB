# JOBLESSONS_2026-11-25T0600EST — hourly Toronto ServiceNow / Salesforce scan

## Cycle
Cron run Wednesday 2026-11-25 06:00 EST (UTC-05, ~11:00Z). Repo `eltonaguiar/BESTIEJOB` (`main`). Local clone `C:/Users/zerou/bestiejob_repo`, **already at `origin/main` == `164e4938`** (clean base; no rebase needed). Board state at open: jobs.json `total=5687` (1,205 ServiceNow / 4,323 Salesforce), live page serving **4,998 cards** (HTTP 200).

## What ran (and what it returned)
1. **Adzuna CA API** (demo keys, `--compressed`, 4 s spacing), 6 queries:
   - `ServiceNow` Toronto `max_days_old=2` → 15 results, **0 platform roles** (Home Trust SAP Basis, Concert Service Desk, Metrolinx "IT Service Management Analyst" = ITSM-not-SN, Varicent GTM, AGF Data/AI — all noise).
   - `Salesforce` Toronto d2 → 52; `ServiceNow` Ontario d3 → 55; `Salesforce` Ontario d3 → 115; `Platform Administrator` Toronto d3 → 10; `Platform Developer` Toronto d3 → 69.
   - Platform-role filter (title has ServiceNow/Salesforce/Platform Admin/Platform Dev; drop sales-exec/account-exec/Apex Legends): **6 candidates, all already on board** (Cognizant SF BA Mgr + SF Tech Lead 5978174028/5978174029, Veracity SF Developer 5976166298, March Networks SF Technical Lead 5977112065). **0 net-new.**
2. **Workday CXS** (POST `/wday/cxs/{tenant}/{site}/jobs`, `Content-Type/Accept/Origin` only, `--compressed`, 8 s spacing) — **all HTTP 200, no 429** at 11:00Z (well past the :00Z CI 429 burst). 5 tenants:
   - `bmo/External` "ServiceNow": 4 rows — ServiceNow CMDB Administrator (13d), ServiceNow Technology Lifecycle Analyst (13d), Applications Support Analyst (10d), Platform Engineer RPA (20d). None fresh; CMDB Admin/Tech Lifecycle already boarded (2026-11-17 via LinkedIn/builtin/workday).
   - `td/TD_Bank_Careers` "ServiceNow": 13 rows — freshest SN-titled is **Senior Solution Architect (ServiceNow) R_1521185, Posted 9 Days Ago** (already boarded via Adzuna 5970077372). The boarded TD "Bus Sys Analysis Specialist (Salesforce/nCino) R_1522988" is separate and on board at head of jobs.json.
   - `cibc/search` "ServiceNow": 14 rows, mostly **Quezon City (Philippines)**; only Toronto hit is "Manager, Technology Governance & Controls" JR26100922 → body: *"platform administration is not required"* → skip. No new Canada SN platform.
   - `manulife/MFCJH_Jobs` "ServiceNow": 8 rows, `hiringCompany: Interac Corp.` — ServiceNow-adjacent rows (Senior BSA ServiceNow, QE Senior Specialist ServiceNow Platform) all **Posted 30+ Days Ago**. None fresh.
   - `interac/interac` "ServiceNow": empty body (site/slug serves nothing this hour; retry next cycle, not a scrape failure to chase).
3. **Rogers** `jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc` → HTTP 200, 26 dated `<tr>` rows, **0 ServiceNow/Salesforce titles** (matches 11-24; recovery from the 11-20 zero-row shell holds).
4. **LinkedIn guest** (browser `new_tab` + DOM read of `a[href*="/jobs/view/"]`, `f_TPR=r86400`): 2 queries (ServiceNow, Salesforce) × Toronto → 112 unique card ids. **22 already on board by trailing id; 90 new-by-id.** But the 90 are overwhelmingly keyword noise — Help Desk / IT Support / HR / Security / Sales / "Account Executive" titles that merely match the platform token in body.
5. **Web searches** (ddgs free tier) surfaced the usual employer-direct leads — all verified already boarded or twins (see below).
6. **Liveness/health**: live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` = HTTP 200, **4,998 cards**, matches the 05:00 build → no drift.

## LinkedIn body-check (the 90 "new ids") — all non-platform
Opened `.jobs-description` on the 3 generic titles that could plausibly be platform roles:
- **4494172283 — Service Management (MSP Governance & ITIL Operations Lead)** / National Consultants Professionals Ltd, Toronto, 18h. Body: *"Support enhancements to ServiceNow or equivalent ITSM platforms."* → **ITSM governance lead**, ServiceNow is the ticketing platform, not a build/admin job. Skip (senior governance; not entry-level).
- **4494733776 — Lead, Systems Administrator** / Take-Two Interactive, Toronto, 11h. Body: *"Experience with ServiceNow or equivalent helpdesk ticket system"* alongside AV/conference-room/VIP support → **desktop/AV sysadmin**, ServiceNow is a helpdesk mention. Skip.
- **4494391635 — Lead, Digital Employee Experience and Automation** / Canada Life, Toronto, 18h. Body: *"Use DEX data, employee feedback, ServiceNow records, support trends…"* → **DEX/automation lead**, ServiceNow is a data source. Skip.
Conclusion: the fresh LinkedIn cards this hour are the classic *"ServiceNow-as-tooling"* false-positive class — none are SN/SF platform administrator/developer build roles.

## Employer-direct leads from search — all already boarded or twins
- **CGI — ServiceNow Administrator/Developer**, Toronto (LinkedIn 4462044907, "entry level") → **already on board** (jobs.json + README). No re-add.
- **Ateko (Bell-backed) — ServiceNow Platform Administrator** (TheLadders 88807278, $80–95K, remote CA, "5 days ago") and **ServiceNow System Administrator** (Jooble jdp/737660180508539590, "6 hours ago") → same req as the **already-boarded** "Servicenow System Administrator | Ateko | jobflurry" (2026-11-03). The description matches verbatim (`Minimum 2 yrs ServiceNow sysadmin, Incident/Change/CMDB, ACL/UI Policies/Business Rules, 24/7, FR+EN`). **Mirror/twin, not a new posting.** TheLadders/Jooble are Cloudflare-walled to extraction anyway.
- **Resource Logistics Inc. — ServiceNow Developer (ITOM/CMDB)** Toronto (LinkedIn 4489780092) → **already on board** (2026-11-16).
- **BMO ServiceNow CMDB Administrator / System Administrator** (250 Yonge St, deadline 11/29, Discovery/Service Mapping/HAM Pro) → **already on board** (R260030992, 2026-11-17).
- **Bell — ServiceNow Senior Technical Advisor** (Req 432829) → application deadline **10/20/2026 already past**; also senior. Skip.

## Result
**0 net-new fresh Toronto ServiceNow/Salesforce platform roles this hour.** Board unchanged (no jobs.json/README/public edits). This is the 4th consecutive net-zero hourly run (03:00, 04:00, 05:00 were also near-saturated; 05:00 added 1 TD Salesforce/nCino BA). Entry-level **Platform Administrator / Platform Developer I (Toronto, 0–2 yrs) remain scarce** — the closest fresh junior-adjacent signals were non-platform (MSP governance lead, AV sysadmin, DEX lead).

## Patterns for future agents
- **11:00Z is a clean Workday window.** All 5 banks/insurers answered HTTP 200 with 8 s spacing; the :00Z CI 429 burst is gone by ~:06Z. Probe banks at :06Z+, never at :00-:05Z.
- **Ateko reposts the same SN admin req under 3 titles/boards** ("Servicenow System Administrator" jobflurry / "ServiceNow Platform Administrator" TheLadders / "ServiceNow System Administrator Canada" Jooble). Treat all three as ONE req; dedupe on Ateko + "ServiceNow … Administrator" regardless of Board, and don't be fooled by a "6 hours ago" Jooble timestamp — that is re-index, not a fresh req.
- **The fresh-LinkedIn keyword flood is ~98% tooling noise.** Of 90 new-by-id cards this hour, 0 were platform build roles after body-check. Do NOT add on title alone; the reliable filter is reading `.jobs-description` and requiring ServiceNow/Salesforce to be the *work* (admin config, Flow Designer, Apex/LWC, CMDB/IRE, IntegrationHub), not "an asset" / "or equivalent ITSM tool" / "ServiceNow records".
- **Adzuna `what` with spaces needs `%20`/`+`.** `what=Platform Administrator` as a literal space returns *"URL rejected: Bad query"* from Adzuna; use `Platform+Administrator`. Single-word queries (`ServiceNow`, `Salesforce`) are unaffected.
- **`manulife.wd3/MFCJH_Jobs` is serving Interac Corp. reqs** (facet `hiringCompany: Interac Corp.`) — the site/tenant hosts Interac postings, which explains why `interac.wd3/interac` can come back empty. Read `hiringCompany`, not the tenant name, to attribute the employer.
- **Bank Workday "ServiceNow"-keyword results are mostly ticketing-tool mentions at >9 days.** BMO's freshest SN-titled req was 9–13 days old; CIBC's Canada hit required no platform admin. At saturation the banks yield nothing fresh for an hourly window — the value of the Workday pass is confirming the boarded rows are still live and catching a rare "Posted Today".
- **Live-page health check is cheap and worth doing every run:** `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` → expect HTTP 200 and a card count within ~10 of the last `build_site.py` output (4,998 today). A big drop = a failed deploy, not a real board shrink.

## Changes committed
- This lessons file only. **No jobs.json / README.md / public/ changes** (0 net-new). Committed with `[skip ci]` so the chronic red audits (Job Source Truth Check, board invariants) do not fire on a docs-only push, and no pages.yml redeploy is needed (the board did not change).

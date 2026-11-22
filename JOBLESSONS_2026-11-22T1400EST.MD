# JOBLESSONS_2026-11-22T1400EST

Hourly Toronto ServiceNow / Salesforce scan — Sunday 2026-11-22 14:00 EST (UTC-05).
Board: github.com/eltonaguiar/BESTIEJOB (main), pages: eltonaguiar.github.io/BESTIEJOB/

## Result this run
- Fresh verified jobs merged: **0**
- jobs.json / README.md / public/: **unchanged** — lessons-only commit, no pages redeploy required
- Base commit: origin/main `6556502` (CI 13:06 EST scan refresh, 5,626 postings; 1,193 ServiceNow / 4,280 Salesforce primary-tagged)

## Sources scanned this window
- Adzuna CA API (demo key): `servicenow`/`salesforce`/`itom`/`now assist` × Toronto + Ontario, max_days_old=1, sort_by=date — 4 queries (~13s total, ≥3s spacing)
- LinkedIn guest jobs API: `ServiceNow` and `Salesforce`, Canada, f_TPR=r86400 — 10 cards each
- Workday CXS: `bmo.wd3/External` answered (200); `td.wd3`, `cibc.wd3`, `manulife.wd3`, `interac.wd3`, `accenture.wd103`, `salesforce.wd12`, `gdit.wd5`, `caatpension.wd10`, `iko.wd3` → HTTP 422 each

## Dedupe results (against README.md + jobs.json + APPLIED.md)
- Deloitte "Conseiller principal ou conseillère principale, ITOM, ServiceNow" — Toronto, 45 min ago — LinkedIn id 4459429838 — **already on board** (same LinkedIn id)
- Deloitte "Conseiller principal IA – Now Assist" — Toronto, 1 hour ago — LinkedIn id 4459418991 — **already on board**
- Other LinkedIn guest cards: CCTV/BFG (not platform), SS&C service delivery (not platform), Deloitte Director Salesforce Delivery (on board, line 35 of scan block), Slalom/UST/iA (on board or not Toronto), Salesforce/Phreesia/Too Good To Go account executives (sales, excluded)
- Adzuna fresh rows: ServiceNow Inc. sales roles (vendor sales execs, excluded by board rule); Cloud Resourcing ITSM/ITOM/CSM PM Toronto (already on board); Novartis SFMC Manager Toronto (already on board)

## Partner / sponsor / target-employer sweep
- **Deloitte**: both fresh ServiceNow platform postings surfaced by LinkedIn guest were already merged by the CI scan — partner sweep via LinkedIn guest catches them at posting time but id-dedupe against the current origin commit is what prevents doubles.
- **Rogers** (jobs.rogers.com Phenom): zero server-side job rows; no SN/SF platform posting — check weekly, not hourly.
- **Bell** (jobs.bell.ca): no fresh SN/SF platform requisition; Bell-backed SN hiring appears under Ateko/FX Innovation, no fresh vacancy this window.
- **Canadian government / public sector**: jobs.gc.ca and gojobs.gov.on.ca Radware-walled; Job Bank via fresh_ca_scan = 0 new; CMHC/SSC/Global Affairs no fresh SN/SF platform posting.
- **Salesforce/ServiceNow vendor careers**: sales/SRE/security only; platform build/admin comes from partners and end-user employers.

## Lessons for future agents
1. LinkedIn guest cards expose the trailing numeric job id — a hard dedupe signal. Both fresh Deloitte ServiceNow platform postings matched existing board rows by id; still twin-check employer + title + city + date before calling a job new.
2. Workday CXS direct curl is unreliable mid-hour on this host: only `bmo.wd3/External` returned 200 (nothing fresh — all postings 7–17 days old); the other 9 Canadian tenants returned HTTP 422. Treat Workday as CI-owned for hourly freshness; don't burn the run on retries.
3. Adzuna `what` with a space must be %20-encoded (curl rejects raw spaces). `now assist` Toronto returned 0 results; `itom` Toronto returned only the already-tracked Cloud Resourcing req.
4. 0-net-new hour: lessons-only `[skip ci]` commit is the correct output — do not commit mirror URLs that would double-list roles already on the board.

## Sources consulted
Adzuna CA API, LinkedIn guest jobs API, Workday CXS, jobs.rogers.com, jobs.bell.ca, jobs.gc.ca, gojobs.gov.on.ca, Job Bank (via fresh_ca_scan), Deloitte careers.

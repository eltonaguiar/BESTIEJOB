# JOBLESSONS — Hermes cron scan — 2026-11-20 17:00 EST (22:00Z)

Run: 2026-11-20 17:00 EST / 22:00Z. Repo: `eltonaguiar/BESTIEJOB`. Scope: fresh Toronto/GTA + Canada-remote **ServiceNow** and **Salesforce** platform-build roles, deduped against `origin/main` (README tables + `jobs.json`), plus a partner / Elite-partner / telco / government sweep.

## Outcome

- **Net-new verified this hour: 0.**
- **Board is current:** the CI hourly scan committed at `21:12Z` (5,586 listings) and the fresh CA sweep at `21:44Z`; `origin/main` = `1ad87a5`. No net-new Toronto/GTA SN/SF platform role surfaced in any source.
- **Site:** 5,049 live cards (repo `public/jobs-data.json` = 5,050). `board_invariants.py` → **PASS** (29 errors / 228 warnings; "no kind grew" vs baseline).
- **0 README / `jobs.json` edits were needed; no merge performed.** Padding the board with ticketing-tool / leadership roles is not an improvement.

## Sources checked this hour

- **LinkedIn guest search** (browser, `sortBy=DD`): `servicenow` 60 cards + `salesforce` 60 cards, Toronto, `f_TPR=r86400`. ~120 unique cards → **21 platform-title hits**; all but one already on the board by job id / URL / company+title.
- **Adzuna API** (ca, `max_days_old=2`, `where=Toronto`): `servicenow` 10 rows + `salesforce` 10 rows. All matches tracked or out of scope.
- **Workday CXS** (10 tenants × ServiceNow, probed at 22:05Z after the CI collision cleared): `bmo`, `td`, `cibc`, `manulife`, `interac`, `caatpension`, `gdit`, `salesforce`, `accenture`, `iko`. **All HTTP 200** (throttle clear), no net-new Toronto SN/SF platform req.
- **Rogers careers** (date-sorted): 0 ServiceNow / Salesforce hits.
- **Scotiabank Phenom**: no fresh Canadian SN/SF platform req (only a Bogota ServiceNow Developer; SF search body-noise).
- **Job Bank** (title-grep) + exa-backed search: Bonafide ITOM/CMDB, Source Code RQ7 SN SPM, Astra Revenue Cloud — all already on the board.
- **BuiltIn Toronto**: 1 SN hit (ServiceNow "Principal Solution Architect" 11971031) — already on the board.
- **Gap analysis** (README URL set vs `jobs.json` postedDate ≥ 2026-11-17, Canada geo, SN/SF tag): 7 feed-only rows, all non-Toronto / non-platform except Nuvei (tracked under Ottawa/Montreal).

## Candidates examined and excluded

| Candidate | Posted | Why excluded |
|---|---|---|
| Deloitte — Software Asset Management (SAM) Analyst (4468276720) | 2026-11-20 | License-management analyst (Microsoft/Salesforce vendor agreements); **re-post of ref 134674** already on board (4460500284); not SN/SF platform build. |
| CIBC — IT Administration Analyst (4492978161 / Workday 2621353-1) | 2026-11-20 | Access provisioning within Service Request Management; ServiceNow is **ticketing tooling**, not a platform build. |
| Encore Technical Solutions — ITSM Transformation Lead (ServiceNow→JSM) (4492985979) | 2026-11-20 | Explicitly "not a hands-on admin role"; 6-month **migration-away** leadership contract. Lead logged, not added. |
| S M Software RQ11675 — Software Developer – CRM – Senior | 2026-11-20 | **Microsoft Dynamics 365 / Power Platform**, not Salesforce. |
| TMX Group — Manager, Incident, Problem & Event Management (R-6618) | 2026-11-17 | 3-day-old ITSM **process-manager** role; ServiceNow appears as tooling. |
| Nuvei — Salesforce Business Process Analyst (adzuna 5969439394) | 2026-11-17 | **Location variant** of the Ottawa/Montreal role already on board. |
| Astra North — Salesforce Revenue Cloud Architect (Job Bank 50768238) | 2026-11-16 | Re-list of the Oct-21 Astra RCA role already on board multiple times. |

## Partner / Elite-partner sweep

- **Cognizant** — Senior Salesforce Developer (4492525247) + Salesforce Technical Architect (4467116032) + SN SAM Developer — all tracked.
- **Deloitte** — SAM Analyst (above) + prior SN consultant; no new platform req.
- **Virtusa, Envision, Blue Mantis, TechNeptune, Procom, Pacer, Avanciers, Galent** — all SN/SF cards already on board.
- **Accenture** — 1,643 global ServiceNow reqs; page 1 has no Canadian req.
- **NewRocket, Pentio, KPMG, TCS, PwC, EY, Capgemini, Wipro, IBM** — no net-new Toronto SN/SF platform req this hour.

## Telco / government sweep

- **Rogers** — `jobs.rogers.com` date-sorted: 0 SN/SF platform req.
- **Bell** — known zero on `jobs.bell.ca`; SN hiring surfaces via **Ateko / FX Innovation** (already tracked).
- **Scotiabank** — no fresh Canadian SN/SF platform req (Bogota SN Dev only).
- **City of Toronto / Ontario gojobs / federal jobs.gc.ca** — Radware-walled; the Job Bank proxy shows only tracked postings.

## Lessons & patterns for future agents

1. **At 17:00 EST Friday the board is fully saturated.** The CI (21:12Z) + fresh sweep (21:44Z) land within ~50 minutes of this run, so a manual pass mostly re-confirms tracked rows. Expect 0 net-new; report it plainly rather than padding with ticketing-tool / leadership roles.
2. **Workday is clear at ~22:05Z (post-CI):** all 10 tenants returned HTTP 200 on the first try with 8 s spacing. Even so, no net-new — TD's "Posted Today" hits were infosec/devops, CIBC's were the provisioning analyst.
3. **The "generic title → body check" still matters, but the hit rate is low.** 4 generic titles checked (CIBC IT Admin, Encore ITSM, RQ11675 CRM, Fidelity Tech Analyst); 3 were non-platform, and Fidelity hit the LinkedIn authwall (unverified → skipped).
4. **Aggregator dates still lie.** Deloitte SAM (ref 135050) is a re-post of ref 134674 (Oct 31) for the same Global Deloitte Technology team; Astra's Nov-16 Job Bank RCA is the Oct-21 req re-listed. Always match the reference code / title+company against the board.
5. **LinkedIn guest search is healthy this hour** (60 cards/query, real card HTML, no authwall). The browser DOM read is the reliable path.
6. **Job Bank title-grep remains noise** (programmer analyst, buyer, finance director). Only trust postings whose platform name appears in the posting's own title line (e.g., "ServiceNow CMDB Consultant", "Salesforce Revenue Cloud Architect").
7. **Baseline discipline:** `board_invariants.py` PASS with 29 errors / 228 warnings is the current baseline; "no kind grew" is the pass signal — do not treat the raw error count as a regression.

## Files touched this run

- `JOBLESSONS_2026-11-20T1700EST.MD` (this file; committed `[skip ci]`)
- Probe artifacts under `raw/` (untracked): `linkedin_1700.json`, `rogers_1700.html`, `scotia_*_1700.html`, `wd_*.json`, `tmx_*.json`, `builtin_*`
- **No `README.md` / `jobs.json` / `public/*` changes.**

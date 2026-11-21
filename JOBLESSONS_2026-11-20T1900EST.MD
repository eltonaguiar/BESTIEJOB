# JOBLESSONS — Hermes cron scan — 2026-11-20 19:00 EST (00:00Z Nov 21)

Run: 2026-11-20 19:00 EST / 2026-11-21 00:00Z. Repo: `eltonaguiar/BESTIEJOB`.
Scope: fresh Toronto/GTA + Canada-remote **ServiceNow** and **Salesforce** platform-build roles, deduped against `origin/main` (README tables + `jobs.json`), plus partner / Elite-partner / telco / government sweep.

## Outcome

- **Net-new verified this hour: 0.** Third consecutive hour at 0 (17:00, 18:00, 19:00 EST).
- **Board at run start:** `origin/main` = `78d796e` (CI hourly scan, 23:12:52Z, **5,588 listings**). Local fast-forwarded from `24cde29` before analysis.
- **CI itself added 3 URL-new rows at 23:12Z:** Apptoza *ServiceNow Technical Lead* + *ServiceNow Lead* (Vancouver, BC) and Cognizant *Salesforce Tech Lead (Remote)* (Toronto — the repost that this run independently found). The pipeline is absorbing reposts correctly.
- **Live page healthy:** `https://eltonaguiar.github.io/BESTIEJOB/` → HTTP 200; `jobs-data.json` = **5,053 cards**, identical to repo `public/jobs-data.json`. Fresh cards confirmed by company+title (RBC SN Discovery, CanPrev SF Admin, Cognizant SF Tech Lead, Envision SN ITOM).
- **No `README.md` / `jobs.json` / `public/*` edits were made or committed.** With 0 net-new there was nothing to merge; the hourly CI owns those files and rewrites them wholesale.

## Sources checked this hour

- **LinkedIn guest search (browser, `f_TPR=r86400`, `sortBy=DD`):** ServiceNow 70 cards, Salesforce 60 cards. Targeted follow-ups: *Salesforce Administrator* Toronto (walled, 0 cards), ServiceNow Mississauga (walled, 0), ServiceNow Markham (60, identical Toronto relevance set), *Salesforce Platform Developer* Canada (45).
- **Adzuna API** (`ca`, `max_days_old=3`, `where=Toronto`): ServiceNow count 42, Salesforce count 91; page 2 of ServiceNow returned a non-JSON body, Salesforce page 2 was sales/marketing noise.
- **Workday CXS:** 10 tenants × 2 queries (`servicenow`, `salesforce`) — **all HTTP 200** at 00:02–00:04Z: `bmo`, `td`, `cibc`, `manulife`, `interac`, `caatpension`, `gdit`, `salesforce`, `accenture`, `iko`.
- **Rogers Phenom** (date-sorted): ServiceNow search returned **0 rows**; Salesforce search returned 18 rows, all field/retail sales.
- **Scotiabank Phenom:** ServiceNow search 10 rows; only platform role is *ServiceNow Developer* (Bogota, CO, Nov 3). Toronto rows are ITSM/security/CIAM body matches.
- **Ateko / FX Innovation (Bell):** careers page routes to `fxinnovation.com/en/jobs` (JS shell). LinkedIn shows Ateko SN Dev + Implementation Specialist (Nov 19) and ITOM/ITAM Architect (Nov 8) — all already tracked.
- **Partner / Elite sweep:** Cognizant, Deloitte, PwC, HCLTech, NewRocket, GlideFast, Insight Global, CGI, MNP, Accenture, KPMG (via board), plus web search.
- **Government:** Job Bank title-grep (template noise only); City of Toronto hiring freeze; Ontario `gojobs` and federal `jobs.gc.ca` remain Radware-walled.

## Candidates examined and excluded

| Candidate | Where found | Resolution |
|---|---|---|
| RBC — Senior ServiceNow Discovery & Service Mapping Engineer (4468324868) | LinkedIn, 11h | **On board** (2026-11-20). Live card resolves to canonical `rbc.wd3.myworkdayjobs.com/RBCGLOBAL1/...`. |
| CIBC — Senior Production Application Support Analyst (ServiceNow Admin/CMDB) (4493222509, 13 min) | LinkedIn | **On board** via CIBC Workday `2621353-1`. LinkedIn is a mirror. |
| Leading Talent — ServiceNow Administrator/Developer (Toronto, Nov 19) | leadingtalent.ca | **CGI repost** — page footer is CGI boilerplate ("At CGI, we value…"); same vacancy as CGI LinkedIn 4462044907 already on board. |
| Cognizant — Salesforce Tech Lead (Remote) (4492842720, 1h) | LinkedIn | **Repost** of req 00071200141 (on board as 4492525247). The CI added this new id itself at 23:12Z. |
| Encore Technical Solutions — ITSM Consultant (4492985979) | LinkedIn, 3h | ITSM transformation lead / ServiceNow→JSM migration-away; previously excluded. |
| TMX — Manager, Incident, Problem & Event Management (adzuna 5973150445) | Adzuna, today | Repost of R-6618 ITSM process-manager; ServiceNow appears as tooling, not platform build. |
| OSI Digital — Boomi Developer (5973286699) | Adzuna, today | Boomi integration developer; not Salesforce/ServiceNow platform. |
| KTek — Technical Operations & Governance Analyst (4492933460) | LinkedIn | Already on board. |
| Procom — IT Operations & Service Transition Consultant (ITSM) (4492596285) | LinkedIn | Already on board. |
| Fidelity Canada — Technical Analyst Sr (4491903115) | LinkedIn | Cloudflare "Just a moment…" wall on the detail page — **unverified**, skipped. |
| Bayshore — Patient Communications & Journey Automation Lead (4491965366) | LinkedIn | CRM/marketing-automation leadership, not platform build. |
| ServiceNow, Inc. Toronto (Cyber Advisory SC, Sales Exec Moveworks, Sr Mgr Sales Cyber, Cyber Enterprise AE, Staff Full-Stack Engineer) | LinkedIn, 1h | Vendor sales / product-engineering roles — out of scope. |
| Cognizant — ServiceNow SAM Developer (00070949051) / HCLTech — SF Administrator / Make-A-Wish — Sr SF Admin / Swoon — SN Developer / PwC — Sr SN Developer / NewRocket — Moveworks Dev+Architect / Insight Global — SF Developer | Search + board | All already tracked. |
| Akkodis SF Technical Consultant (Calgary), Medavie Team Leader SF (NB), LGS SF Architect (QC), IH FSC Architect (MTL) | LinkedIn | Out of Toronto/GTA scope. |

## Lessons & patterns for future agents

1. **Friday-evening saturation is stable.** Three consecutive hours (17:00/18:00/19:00 EST) produced 0 net-new. Report 0 plainly; padding with vendor sales, GTM, AWS, Boomi, or ITSM-tooling roles degrades the board.
2. **Rogers and Scotiabank Phenom boards are now cheap HTML parses** — no Playwright needed. Both render `<tr data-row>` with `<td>` absolute dates (`Nov 20, 2026`). Rogers SN query = 0 rows; its Salesforce search is sales/retail only. Scotia's only SN platform row is Bogota. Re-check these weekly-to-hourly, but expect zero.
3. **Agency reposts clone the employer page footer.** Leading Talent's "new" Toronto SN Admin/Developer is a verbatim CGI posting (footer: "At CGI, we value the strength that diversity brings…"). Before counting an agency/recruiter row as new, read the footer/boilerplate and match the employer's own req.
4. **Workday was NOT throttled at :00Z this hour.** All 20 CXS calls returned 200 at 00:02–00:04Z even though `hourly-scan.yml` fired at 00:00Z. The :00Z 429 is not deterministic — probe first, don't assume.
5. **Merge `origin/main` before adding any row.** The CI ingested Cognizant 4492842720 within the same hour this run found it. Adding a row the CI already merged creates a duplicate and a rebase conflict.
6. **`board_invariants` outside-window drift is calendar-driven, not a regression.** It rose 32 → 101 errors as the 76 README rows dated **2026-10-21** crossed the 30-day window (baseline 43 recorded 2026-11-14). No data edits this run. A baseline re-record is the correct fix; do not delete rows to satisfy the ratchet.
7. **"ServiceNow Administrator/Developer" is the most-mirrored title on the board** (CGI, Central 1, Sheridan, BFG, MNP). Dedupe on company + location first; a title-only search returns mostly mirrors.
8. **Adzuna page 2 can return a non-JSON body** (empty/HTML) for a valid query — treat it as "no data", not "zero postings"; page 1 plus LinkedIn carries the hour at saturation.
9. **README's top `<!-- DAILY-SCAN -->` block is stale (20:01Z) while `jobs.json` is at 23:12Z.** It is only refreshed by a local `node scripts/daily_job_scan.mjs` run without `--no-readme`; the CI always runs `--no-readme`. Leave it alone in a 0-net-new hour rather than triggering a capSecondary shrink + CI collision.

## Files touched this run

- `JOBLESSONS_2026-11-20T1900EST.MD` (this file; committed `[skip ci]`)
- Raw probe artifacts under `raw/` (untracked): `adzuna_1900_*`, `linkedin_1900.json`, `linkedin_targeted_1900.json`, `wd_1900/*`, `rogers_1900_*`, `scotia_1900_*`, `ateko_1900.html`, `fx_1900.html`, `leadingtalent_1900.txt`, `procom_pm_1900.txt`, `live_jobs_1900.json`, `prev_jobs_1900.json`
- **No `README.md` / `jobs.json` / `public/*` changes committed.**

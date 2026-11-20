# JOBLESSONS — 2026-11-20 09:00 EST (14:00Z) hourly ServiceNow / Salesforce scan

Run context: Hermes cron hourly scan. Start `origin/main` = 11d17f6 (agency scan, `jobs.json` already at scrapedAt 2026-11-20T14:02:58.800Z, **5,606 rows**, SN 1,184 / SF 4,281). A local `node scripts/daily_job_scan.mjs` printed only `stdin is not a tty` and produced byte-identical files — the CI/agency workflows had already run the 14:02:58 scan, so the local pass was a no-op. **Check `git show origin/main:jobs.json` scrapedAt before spending 5 minutes on a local scan.**

Outcome: **2 verified net-new** merged to `jobs.json` + README + site — **Procom**, *IT Operations & Service Transition Consultant (ITSM)* (Toronto, hybrid, 12-mo contract, ServiceNow preferred) and **KTek Resourcing**, *Technical Operations & Governance Analyst* (Scarborough; ServiceNow ITSM reporting + Power BI + ITIL, 7+ yrs). Board 5,606→**5,608**; site **5,046 cards (SN 862 / SF 920 / other 3,264)**. Guards: `check_readme_sort` OK, `board_invariants` **PASS (33 errors, baseline 34, no kind grew)**, `check_site_links` OK.

## Source yields this hour

- **Browser LinkedIn DOM** (still the freshness oracle): SN/SF × Toronto `f_TPR=r86400` + SN/SF × Canada `f_TPR=r604800` = **240 cards, 218 unique URLs**, no authwall this run. After URL + 10-digit job-id + company/title dedupe against jobs.json + README + APPLIED only **2 were untracked**.
- **Workday CXS** (10 probes: bmo/TD/CIBC/Manulife/Interac/Accenture/Salesforce, ServiceNow + Salesforce): no fresh Canada platform roles. BMO/Deloitte/TD/CIBC/Manulife rows were support, PM, governance or marketing; Interac "ServiceNow" rows were **Posted 30+ Days Ago** stale; TD's fresh Salesforce req was Mount Laurel, NJ. Confirmed the host rule again: the URL must be the full `{tenant}.wd{N}.myworkdayjobs.com` — `https://bmo.wd3/...` dies with "Could not resolve host".
- **Adzuna API** (7 queries, 3–4 s spacing): 32 SN / 78 SF / 5 "salesforce administrator" / 4 "servicenow developer" results, almost all sales/BD noise or already tracked (CGI SF BA, Serefin SF DevOps, Mackenzie HR Tech & ServiceNow HRSD, Versaterm, Rockwell). No net-new.
- **Job Bank (`jobbank.gc.ca`) "servicenow" full-text**: 24 rows, **zero title-naming the platform** (Cloud developer, Cybersecurity consultant, Buyer, Programmer analyst). Same noise as prior lessons — Job Bank full-text is not a usable SN/SF oracle.
- **ICF** (`careers.icf.com` R2603696): ServiceNow Developer is **Reston, Virginia / US federal** — not Canada, reject.
- **NewRocket (Elite SN partner)**: Greenhouse `highmetric` board = 44 jobs; the IRM/GRC Solution Architect (Canada) is **already tracked since 2026-11-03** (tryremotely row). The "Director, Business Process Architecture; ServiceNow, Risk & SecOps – Toronto" listing is a **Feb-2026 vintage** post; the current Director role is US West. No add.
- **ConfigureTek / Configure Consulting**: ServiceNow Technical/Associate Consultant Toronto listings are old Glassdoor entries (no fresh date), no direct live ATS link — skip.

## Dedupe discipline that mattered

1. **jobs.json alone is not the board.** Check README + APPLIED + company/title too — the CI/agency scans rebuild jobs.json and can drop rows the README still carries.
2. **Keyword-title filters miss generic titles.** Akkodis "Business Analyst – Senior" (4492511354) body-reads as *ServiceNow Business Analyst* — it was already tracked, but the filter had excluded it from the SN-title pass; body-check remains essential. KTek's "Technical Operations & Governance Analyst" likewise only reveals SN/CMDB/ITIL in the body.
3. **Reposts are mirrors.** NewRocket IRM/GRC reads "10 hours ago" on BuiltIn but the board has carried it since 11-03; the Feb-2026 Toronto director post is not fresh. Compare against `postedDate` + existing rows, never the aggregator's "posted X hours ago".

## Rejected this hour (tool/process/sales, not platform work)

- CI Financial — Service Desk Analyst ×2 (ServiceNow is the ticketing tool, L1/L2).
- Manulife — Manager, Post Incident Reviews & Incident Management; Scotiabank — Senior Analyst, Business Support Strategy & Incident Mgmt (process roles, no SN/SF build).
- WSIB — Enterprise Risk Management Manager ×4 (Scarborough/Mississauga/North York/Hamilton) — same role as tracked Toronto row 4492156479.
- S M Software RQ11846 / RQ11845 — Microsoft Dynamics CRM + MuleSoft (Ontario govt), not Salesforce; RQ11675 same D365 pattern.
- Endress+Hauser — Business Applications Specialist ("ERP/CRM e.g. SAP, Salesforce" example list); Lyft Sr TPM Finance ("Zuora, Salesforce, Oracle" tool list).
- Salesforce Inc — Business Development Rep, Enterprise AE Tableau, SMB AE Data Foundation: sales roles, reject.
- ICF ServiceNow Developer — US federal (Reston, VA).
- Job Bank servicenow hits — all off-title.

## Partner / sponsor / tech-company watch (all already tracked unless noted)

Deloitte (incl. Senior Manager GRC Technology Delivery — Archer + ServiceNow IRM), KPMG, Cognizant (incl. SN Technical/Senior Technical Consultant), Accenture, PwC, CGI (SF BA FSC), IBM/LGS, NTT DATA (SN BA SPM, SN Architect Burnaby), NewRocket/Highmetric (IRM/GRC, FSO/CSM, Moveworks), SPECTRAFORCE (SN Developer, CMDB/HAM/SAM), G-FORCE IT (SN dev/ITSM), TD, BMO, CIBC, Manulife, Interac, ServiceNow (vendor: Staff Full-Stack, Senior Systems Engineer), Salesforce (vendor: Renewals analyst, SWE MTS — not platform admin/dev). **Rogers**: only Lead Management Operations ×2 (Pefferlaw/Cambridge, non-platform); Phenom board still shell-only. **Bell/Ateko (backed by Bell Canada)**: *Développeur.euse ServiceNow* (4492170001) tracked; no new req. **Government**: Job Bank noise; Ontario govt reqs via S M Software are D365/MuleSoft; no title-named SN/SF.

## Market pattern (Nov 20, 2026 — 09:00 EST)

Toronto SN/SF is at practical saturation: **218 unique LinkedIn cards produced 2 net-new**, both staffing-agency ITSM/adjacent roles. Primary SN/SF tables got zero new rows; the fresh work now hides in (a) generic analyst titles that body-read as ServiceNow, (b) ITSM/ITIL service-transition contracts, (c) city twins of already-tracked reqs. Expect 0–2 adds/hour; the hourly run's main value is reconciling jobs.json to README and refreshing the DAILY-SCAN top-12.

## README mechanics learned this hour

- There is **no `### Other jobs` heading** in the current README (mangled one-line renderer); other-family rows live at the end of the file. `extract_rows()` parses any `| YYYY-MM-DD | [title](url) | company | location | note |` line, so **appending rows at EOF is safe**.
- `check_readme_sort.mjs` only validates tables that have a `Posted` header row; the mangled blocks are not checked as tables, so appending a newer row at EOF does not trip it.
- `classify()` maps `itsm|itam|cmdb|itom` in the title to the **servicenow family**, so an "ITSM" contract shows under the ServiceNow tab even when ServiceNow is only a preferred tool — tag it `["servicenow","itsm"]` and say so in the excerpt.
- Small-batch merge that worked: textual splice at `"jobs": [` (compact JSON, preserve newline style), bump `meta.total` + `primaryCounts`, append README rows, `build_site.py`, `sync_readme_counts.py` (6,162→6,164), guards, commit `[skip ci]`, push, `gh workflow run pages.yml`, verify live `jobs-data.json`.

## Run recipe (refined)

1. `git fetch` → confirm `git show origin/main:jobs.json` scrapedAt; if it is <1 h old, **skip the local scan** (it will be a no-op) and go straight to targeted harvest.
2. Browser LinkedIn: SN/SF Toronto `r86400`, SN/SF Canada `r604800`; save all cards to one JSONL; dedupe against jobs.json + README + APPLIED (URL, trailing numeric id, company+title).
3. Workday CXS for the known 200 tenants only; read `postedOn` + `/job/<City>/` slug; ignore "30+ Days Ago".
4. Adzuna API for breadth (3–4 s spacing), then discard sales/BD/recruiter titles.
5. Body-check every generic or ambiguous title (`/jobs/view/<id>` → `.jobs-description`, sentence around the keyword).
6. Add only verified net-new; textual jobs.json insert + README append; rebuild; run the four gates; commit `[skip ci]`; push; trigger `pages.yml`; grep the live `jobs-data.json` for the new ids.

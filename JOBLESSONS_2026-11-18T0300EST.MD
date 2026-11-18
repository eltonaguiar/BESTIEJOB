# JOBLESSONS_2026-11-18T0300EST — BESTIEJOB hourly cron scan

## Run
- Time: 2026-11-18 03:00 EST (08:00Z). Board: eltonaguiar/BESTIEJOB `main` → eltonaguiar.github.io/BESTIEJOB.
- Target: fresh Toronto / Canada ServiceNow + Salesforce postings; partner / sponsor / employer sweep (Rogers, Bell, Canadian government, ServiceNow- and Salesforce-the-company).
- Sources swept: LinkedIn guest (24h, Toronto ON — ServiceNow + Salesforce keyword searches, 60 cards each), Adzuna Canada demo API (16 queries × 3 geos: national / Toronto / Ontario), Workday CXS (10 Canadian bank/partner tenants), SmartRecruiters (ServiceNow-the-company, 100-postings page 1).

## Result
- **2 verified fresh, on-target Salesforce postings merged** (both at Fiix / Rockwell Automation, Toronto):
  - *Revenue Operations & Automation Specialist* — posted 2026-11-18 (8h before scan). Hands-on Salesforce ops/automation: keeps Salesforce data accurate, quotes/orders/renewals in **Salesforce Agentforce Revenue Management (ARM)**, builds automation with **Salesforce Flow / Agentforce / Slack**. Closest to a Salesforce admin/ops role.
  - *Product Owner, Revenue & Support Operations* — posted 2026-11-17. Owns the roadmap/backlog for **Salesforce ARM, Service Cloud, Zendesk, TaskRay**, retires legacy Salesforce CPQ; partners with Salesforce admins and developers.
  - Both inserted at head of `jobs.json` (2572 → 2574, primaryCounts.salesforce 1307 → 1309) and one clean README row each at the top of the Salesforce table.
- Everything else this hour was already on the board (dedupe held) or off-target:
  - LinkedIn 24h "servicenow": ServiceNow Principal Solution Architect, BMO CMDB Admin, Mackenzie HRSD Manager, Envision ITOM Developer, NTT DATA BA (SPM), ServiceNow Staff Cloud Security, W3Global Dev/Architect — all ON-BOARD.
  - LinkedIn 24h "salesforce": Loblaw Sr SWE, McKesson Sr CRM Dev Lead, Accenture Techno-Functional, Citco Solution Architect, Munvo SFMC Consultant, Cognizant Data Cloud, TD nCino, Serefin DevOps, Co-operators Agentic SF Delivery, Celestica intern, Nuvei Business Process Analyst — all ON-BOARD.
- `tools/build_site.py`: 5017 jobs (SN 810 · SF 938 · Other 3269), 862 duplicate mirrors collapsed, 35 applied hidden, newest 2026-11-18. Both Rockwell URLs confirmed in `public/jobs-data.json` and `public/index.html`.

## Employer / partner sweep (user directive)
- **Rogers** — LinkedIn "Lead Management Operations" (Aurora, 15h) surfaced under the Salesforce keyword search but is a marketing/lead-ops role; `jobs.rogers.com` itself not re-scraped this hour (last hour it loaded 99 KB with 0 ServiceNow/Salesforce reqs). Keep weekly direct check.
- **Bell** — `jobs.bell.ca` empty shell (0 reqs), unchanged. Weekly.
- **Canadian government** — `jobs.gc.ca` / `gojobs.gov.on.ca` Radware-walled (do not retry). Public-sector SN/SF comes through Job Bank only when the *title* names the platform.
- **ServiceNow-the-company** — SmartRecruiters page 1 = 100 reqs, 836 total; 3 Canada (Sr Solution Sales Executive CRM/CPQ Toronto, Staff Cloud Security Engineer Toronto, Sr CRM Account Executive Montreal) — sales/security, all already on board. No platform roles.
- **Salesforce-the-company** — 2 fresh Workday hits, both Sales roles (Sales Senior Agentic Experience Specialist, Sales Senior Solution Architect – Agentforce) across "4/5 Locations"; sales titles, not platform. `GTM Strategy and Operations Associate Analyst` (Toronto, 9h) on LinkedIn is a GTM/sales-ops role — excluded.

## Reusable lessons (new / refined this cycle)
- **Adzuna "Apex" is a false-positive magnet.** `Servicenow` query returned ServiceNow's *Sr Solution Sales Executive CRM (CPQ)* (sales role, caught only because "CPQ" hits the SF regex) and *Respawn Entertainment — Tools Developer (Apex Legends)* — the video game, not Salesforce Apex. Add title-level excludes for `sales executive|solution sales` and reject `Apex Legends` before treating an "Apex" hit as Salesforce.
- **Generic titles that mention the platform only as tooling are NOT platform roles.** Staples *IT Operations Process Coordinator* and TMX *Manager, Incident, Problem & Event Management* both say "ServiceNow", but only as one of several ticketing/ITSM tools ("ServiceNow, or an equivalent ITSM tool"; "enterprise ITSM platforms (e.g., ServiceNow, Jira)"). They are data-center / ITSM-process roles, not Admin/Dev. Body-check the *context* around the keyword, not just its presence.
- **"CRM" ≠ Salesforce.** S M Software *RQ11878 Software Developer – CRM – Senior* returned "salesforce" 6× but is a **Siebel CRM** developer (Ministry of Public and Business Service Delivery). The SF hits came from the "People also viewed" sidebar. Always read the description body; the page-layout `.jobs-description` selector has changed — `document.body.innerText` sliced from "Job Description" is the reliable fallback now.
- **Product/sales-ops roles over a Salesforce platform do count when the body is genuinely Salesforce-centric.** The two Fiix/Rockwell roles name ARM / Service Cloud / Salesforce Flow / Agentforce repeatedly and partner with Salesforce admins — legitimate SF-ecosystem rows, unlike a pure marketing "Lead Management Operations" role.
- **Workday CXS 429s hard when the CI hourly scan runs concurrently.** At 08:00Z (03:00 EST) the `hourly-scan.yml` cron fires at the same moment; BMO/TD/Manulife/CIBC/Interac all returned HTTP 429 on my manual probe. Retry only 3–4 tenants at ≥8 s spacing, or rely on the CI's own Workday pass (it commits to `main` right after). "Posted Today" hits still need the `/job/<City>/` slug read — Salesforce's 2 fresh hits were sales roles in "4/5 Locations".
- **LinkedIn guest search still returns 60 cards cleanly** at `r86400` via `new_tab` + reading `li a[href*="/jobs/view/"]` + `time[datetime]`; no authwall this run. Detail-page `.jobs-description` returned empty on several lazy-loaded pages — body-innerText fallback worked.
- **README tables are one mangled mega-line per section**, but the Salesforce block carries clean newline-delimited rows after the mega-line (lines 1134–2561 this run). Insert new rows right after the `### Salesforce jobs …` heading line, not into the mega-line. `jobs.json` remains the render source; `build_site.py` unions and jobs.json wins.

## Files changed
- `jobs.json` (+2 jobs: Rockwell RevOps 2026-11-18, Rockwell Product Owner 2026-11-17; total 2574, salesforce 1309)
- `README.md` (+2 Salesforce rows at top of the Salesforce table)
- `public/jobs-data.json`, `public/index.html` (rebuilt — both Rockwell URLs present)
- `JOBLESSONS_2026-11-18T0300EST.MD` (this file)

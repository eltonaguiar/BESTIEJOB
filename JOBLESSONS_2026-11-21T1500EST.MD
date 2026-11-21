# JOBLESSONS_2026-11-21T1500EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
- 15:00 EST (2026-11-21T20:01 UTC) cron scan of public sources for Toronto ServiceNow / Salesforce roles.
- Board before: 5561 jobs (1193 ServiceNow · 4263 Salesforce). Board after: 5567 jobs (+6, all Salesforce).
- Merged to README.md DAILY-SCAN block, jobs.json meta, and public/ (rebuilt via `tools/build_site.py`; `scripts/check_site_links.py` OK: 5061 jobs, tabs/aria/stamp/fit links valid).
- Pushed to main as `650456b` (remote eltonaguiar/BESTIEJOB); `pages.yml` rebuilds GitHub Pages (https://eltonaguiar.github.io/BESTIEJOB/) on push to `public/**` + `README.md`.

## Verified fresh jobs added (all Toronto-area Salesforce, body-verified from source listings)
| Posted | Role | Company | Location | Source / terms |
|---|---|---|---|---|
| 2026-11-20 | Salesforce Developer | Avanciers Inc | Toronto, ON | jobs.ca — contract, CAD $75-85/hr, hybrid 2d/wk onsite, deadline 2026-12-15 |
| 2026-11-19 | Salesforce Agentic Developer | Paralucent | Greater Toronto Area, Canada | careers.paralucent.com — published 2026-11-19, contract, Agentforce/Apex/Flow/REST |
| 2026-11-19 | Salesforce Developer | CGI | Toronto, ON | jobs.ca — posted 2026-11-19, $85k-135k CAD, hybrid 3d/wk onsite, FSC |
| 2026-11-19 | Senior Salesforce Developer | Tata Consultancy Services | Toronto, ON | jobs.ca — posted 2026-11-19, $100k-120k CAD, on-site, PD I/II + Agentforce |
| 2026-11-17 | Student Intern, Salesforce Developer 1 | Celestica | Toronto, ON | careers.celestica.com req 141238 — 16-month internship from May 2027, North York |
| 2026-11-10 | Salesforce Developer | Intelli-CloudWare Inc | Toronto, ON | jobs.ca — posted 2026-11-10, on-site, Platform Developer I/II, apply by 2026-11-24 |

## Dedupe check (against jobs.json: URL key and title+company+location key)
Already on board, skipped:
- Procom Senior ServiceNow Developer (BMO/CMDB-HAM-SAM, Toronto) — URL already present.
- Deloitte Salesforce Developer (Digital Customer, Toronto, posted 2026-11-21) — URL already present.
- Docebo Senior Salesforce Developer (Ashby, Toronto hybrid) — title+company+location matched an existing row under another URL.
9 leads checked → 6 new added.

## Employer / partner sweeps (Rogers, Bell, Government of Canada, partners)
- Rogers: jobs.rogers.com (SuccessFactors) Technology portal checked — no open Toronto ServiceNow/Salesforce requisition surfaced; one North York Solution Architect listing was filled.
- Bell: jobs.bell.ca checked — no SN/SF Toronto developer/admin requisition surfaced (a CCaaS AI Practise Lead mentions Salesforce/ServiceNow integration work, not a platform role).
- Government of Canada: GC Digital Talent / CSIS checked — the ServiceNow stream (CSIS Senior Technical Officer, Stream 10) and other GC IT roles are Ottawa-based, out of Toronto scope; nothing Toronto-dated added.
- ServiceNow careers (Ontario page) and ATS partner sweep (Greenhouse/Lever/Ashby) surfaced no fresh Toronto posting beyond the board.

## Patterns / lessons for future scans
1. jobs.ca carries employer requisitions (CGI, Deloitte, TCS, Avanciers, Intelli-CloudWare) with literal "Posted <date>" stamps — high-signal, easy to verify; prioritize it each cycle.
2. Employer careers pages (Paralucent, Celestica) publish dated roles before aggregators mirror them — check partner careers directly, not just aggregators.
3. Always dedupe on both URL and (title, company, location): the same requisition arrives under LinkedIn/adzuna/jobs.ca mirrors with different URLs.
4. ServiceNow Toronto hits were thin this cycle (Procom/BMO req already on board). Next cycle: widen ServiceNow to implementation partners (Pentio, Ateko/FX Innovation, Lane Four, NTT Data, Accenture, Deloitte) instead of generic search strings.
5. Entry-level track: only one entry-level Salesforce hit this cycle (Celestica intern). Keep junior / Platform Developer I / associate queries running weekly.
6. Do not count GC/partner "ServiceNow mentioned in integration duties" roles as platform requisitions — label them Other/integration only when body-verified.

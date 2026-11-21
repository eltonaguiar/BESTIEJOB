# JOBLESSONS_2026-11-20T2300EST

## Run summary
- Cron run: Friday 2026-11-20 23:00 EST (2026-11-21T04:00Z). Base: origin/main 745a673, fast-forwarded before scanning so the scan reads the CI's latest jobs.json and avoids racing the hourly CI commit.
- Scan: `node scripts/daily_job_scan.mjs` (no `--no-readme`, so the README `<!-- DAILY-SCAN -->` block was refreshed too).
- Result: `fresh=477 merged=5613`; liveness gate (`verify_links.py --days 2`) probed 119 fresh rows, dropped 1 dead, kept 5612.
- New URLs added to board: **28** (13 ServiceNow-tagged, 15 Salesforce-tagged, 0 other).
- Commit `31bd6ce` pushed to main; `pages.yml` triggered for GitHub Pages deploy.

## Sources that returned fresh postings (this run)
- adzuna: 176 (Canada API, demo keys `54ce986e` / `db851f299e966c0a2a72af525dce6199`, `sort_by=date`, `max_days_old=14`, `content-type=application/json`)
- linkedin: 263 (guest `seeMoreJobPostings`, general pass + `f_TPR=r86400` fresh 24h pass)
- smartrecruiters: 12 (ServiceNow board)
- greenhouse: 14 (verified boards incl. NeuraFlash)
- lever: 1
- ashby: 2
- remote (remoteok/jobicy/remotive): 9

## Sources that returned NOTHING this run
- workday: 0 matching postings — ALL 15 boards x 2 queries returned HTTP 429.
  - Cause: the CI `hourly-scan.yml` runs at the same minute and rate-limits Workday CXS. A manual run at :00Z gets 429s on BMO/TD/Manulife/CIBC/Interac/salesforce/accenture; do **not** conclude zero postings.
  - Lesson: leave Workday to the CI pass, or re-probe key Canadian tenants (bmo, td, cibc, manulife, interac, caatpension, salesforce, accenture, bdo, gdit) 3-4 minutes later at >=8s spacing. A 10-tenant probe at 16:06Z returned HTTP 200 on all 20 calls after a 16:02Z scan 429'd everything.

## Fresh Toronto/GTA ServiceNow + Salesforce roles added (28 net-new)
ServiceNow (13):
- BMO — ServiceNow CMDB Administrator (Toronto, 2026-11-17, LinkedIn)
- BMO — ServiceNow Technology Lifecycle Analyst (Toronto, 2026-11-12, LinkedIn)
- TD Bank — Senior Solution Architect (ServiceNow) (Toronto, 2026-11-18, Adzuna)
- Cognizant — ServiceNow Software Asset Management Developer (Toronto, 2026-11-11, LinkedIn) [ITAM]
- Pacer Group — ServiceNow Implementation Architect (Toronto, 2026-11-11, LinkedIn)
- Avanciers Inc. — ServiceNow Implementation Architect (Toronto, 2026-11-11, LinkedIn)
- KPMG Canada — Consultant/Senior Consultant - ServiceNow Solution Developer (Toronto, 2026-11-07, LinkedIn) [Elite Partner]
- Wipro — ServiceNow Implementation Architect (Mississauga, 2026-11-04, LinkedIn)
- Amicis Global — ServiceNow Business Analyst - Senior, Toronto (3 days onsite) (Toronto, 2026-11-19, Adzuna)
- plus 4 more ServiceNow-tagged rows

Salesforce (15):
- TD Bank — Associate Software Engineer (nCino/Salesforce) (Toronto, 2026-11-19, Adzuna)
- Jobgether — Salesforce Business Process Analyst (Canada, 2026-11-20, LinkedIn)
- Tata Consultancy Services — Senior Salesforce Developer (Toronto, 2026-11-18, LinkedIn)
- OSI Digital — Salesforce Developer (Toronto 2026-11-12; Vancouver 2026-11-12; Toronto 2026-11-11, LinkedIn + Adzuna)
- OSI Digital — Salesforce Quality Analyst Tester (Toronto, 2026-11-11, Adzuna)
- OSI Digital — Salesforce Business Analyst (Toronto, 2026-11-11, Adzuna)
- OSI Digital — Salesforce Lead (Toronto, 2026-11-08, Adzuna)
- plus 7 more Salesforce-tagged rows

## Company / partner patterns confirmed
- Banks are the steadiest Toronto SN/SF source: BMO Workday + TD Bank (Adzuna/LinkedIn) post ServiceNow Admin/CMDB/Architect and Salesforce nCino/Developer roles regularly.
- Elite / implementation partners post Canadian platform roles: KPMG Canada, Wipro, Cognizant, Pacer Group, Avanciers Inc., OSI Digital, NeuraFlash (Salesforce AI/Agentforce).
- OSI Digital re-posts the same Salesforce Developer req under multiple Adzuna ids — dedupe on company+title, not URL alone, else twins inflate the board.

## Negative patterns (do not re-scan hourly)
- Rogers Phenom board (`jobs.rogers.com/search/...`) returns HTTP 200 but a ~56 KB page shell with zero job rows server-side. Rely on LinkedIn/Adzuna for Rogers rows; do not retry hourly.
- Bell Canada (`jobs.bell.ca`) renders an empty shell / `(0)` for both `servicenow` and `salesforce`: zero reqs, not a scrape failure. Re-check weekly.
- Public-sector portals `gojobs.gov.on.ca` (Ontario) and `jobs.gc.ca` are Radware-captcha-walled. Use Job Bank as the proxy and trust only postings whose **title** names the platform.
- ServiceNow-the-company posts only sales/SRE/security in Toronto; Salesforce-the-company posts nothing below 4 days and no Platform Admin/Dev I. Fresh platform work comes from banks, DXC, and GRC/IRM consultancies (e.g. PwC's ServiceNow IRM practice).

## Dedupe / quality rules enforced
- Dedupe on normalized URL (strip query string + trailing slash) AND company+title fuzzy match (Adzuna recycles ids; `Maple Leaf Sports & Entertainment Partnership` vs `MLSE`, `Interac Corp.` vs `Interac`).
- Never prune existing dead links (user standing instruction). Liveness gate `--days 2` probes fresh rows only; only true 404/410/451 are dropped (1 dropped this run). 403/429/5xx and transport errors are kept as live (66 unknown this run).
- `is_listing_url()` filter: hub/company landing pages and search URLs are not postings.
- Workday `postedOn: "Posted Today"` is not a Canada signal — read the `/job/<City>/` slug and country before counting a fresh hit.

## GitHub Pages deploy
- `public/` rebuilt with `tools/build_site.py`: 5051 jobs (servicenow 867 / salesforce 929 / other 3255), 799 duplicate mirrors collapsed, built 2026-11-21 04:04 UTC.
- `pages.yml` triggered after push; verify live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` carries the new URLs (e.g. BMO `servicenow-cmdb-administrator-at-bmo-4490380189`, TD `5970077372`).

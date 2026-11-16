# JOBLESSONS_2026-11-16 — hourly cron scan (14:00 EST / 19:00 UTC)

## Result this run
- Fresh Toronto ServiceNow / Salesforce scan performed at 14:00 EST: LinkedIn guest search (ServiceNow Toronto + Salesforce Toronto, past 24h, 61 + 60 cards), Workday CXS tenant probes, Indeed category search, Rogers / Bell / public-sector checks.
- **0 brand-new verified merges this hour.** README.md unchanged: ServiceNow 1,295 / Salesforce 1,505 / Other 4,777 = 7,542 live postings, window 2026-10-02 → 2026-11-16, "as of 2026-11-16".
- No jobs.json, README.md, or public/ changes; no GitHub Pages redeploy required (pages.yml triggers on README.md / public/ pushes only).

## Sources checked — all zero new merged
- **LinkedIn guest** (browser, fresh non-profile session, ca.linkedin.com/jobs/search, f_TPR=r86400): page 1 = past-24h postings. Every on-target lead is already aboard:
  - NLB Services CSM/HRSD (Mississauga) and ITOM/CMDB Developer (Toronto) — in jobs.json
  - TechNeptune Consulting ITOM Developer (Toronto) — in README
  - Resource Logistics ServiceNow Developer (Toronto) — in jobs.json
  - Four Seasons Senior Salesforce Developer (Toronto) — in README
  - HCLTech Salesforce Administrator (Toronto) — in README (merged 12:00 EST run)
  Remaining cards are off-target: generic QA (Co-operators x2, Grand Software Solutions), Salesforce Marketing Cloud / CPQ / Revenue Cloud / architect titles, "Software Developer – CRM", US/DC roles (Burgeon IT "Any nearest DC Office in Canada"), and location-unconfirmed Raas Infotek "SerivceNow Architect (Multiple Position)". LinkedIn job-detail pages returned no body text this hour, so title-only leads were **deferred, not merged**.
- **Workday CXS** (POST /wday/cxs/{tenant}/{site}/jobs, searchText ServiceNow/Salesforce): all 12 tenants × 2 queries returned HTTP 429 Too Many Requests — rate-limited this hour, no data. Earlier today (05:16Z / 12:00 EST runs) all tenants returned HTTP 200: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, sunlife.wd3/Experienced-Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site, telus.wd3/TELUS, rbc.wd3/RBC_Careers, rogers.wd3/RogersCareers.
- **Indeed** (ca.indeed.com category pages via web search): no extractable fresh Toronto SN/SF postings; Indeed guest detail blocked (422).
- **Rogers / Bell**: LinkedIn cards show only non-platform roles (Rogers: Employee Relations, Lead Management Operations; Bell partner Ateko: Infrastructure Services Coordinator). No SN/SF platform titles. Bell careers is JS-rendered, not curl-scrapeable.
- **Public sector / government**: jobs.gc.ca NXDOMAIN; gojobs.gov.on.ca Radware-walled; Job Bank OPS employer feed 0 platform-titled postings; City of Toronto 0 SN/SF cards.
- **Partners / Elite sponsors** (gap scan, earlier today): Lane Four Salesforce Consultant/Administrator undated (merger skips undated rows); FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Crossfuze returned 0 postings.

## Dedup & verification procedure followed
- Candidate key = normalized URL (tracking params stripped) against README.md + jobs.json + APPLIED.md (APPLIED.md is a hard exclude).
- Merge bar: posted today/yesterday; direct posting deep-link (no hubs/search pages); Toronto/GTA/Canada location; title shows ServiceNow or Salesforce platform work. Salesforce emphasis: Platform Administrator / Platform Developer I (esp. entry-level/junior). ServiceNow: developer / administrator / architect / analyst roles.
- Title-only leads without body/location confirmation are not merged.

## Market-shape notes (2026-11-16, stable)
- Hourly supply near zero for several consecutive runs today (07:00 and 14:00 EST = 0 fresh merged): normal late-2026 pattern — do not commit "just to have a commit".
- ServiceNow-the-company and Salesforce-the-company Toronto postings are sales / SRE / software engineering, not Platform Admin / Dev I.
- Fresh platform work comes via consultancies / staffing (NLB Services, TechNeptune, Resource Logistics, AllianceIT) and banks' Workday tenants (BMO, TD, CIBC).

## New lessons
1. LinkedIn guest search works again via a fresh non-profile browser session (ca.linkedin.com/jobs/search + f_TPR=r86400 returned 142 SN / 60 SF cards), but LinkedIn job-detail pages are blocked this hour — verify bodies next run before merging title-only leads (Co-operators QA, EllisDon Specialist, Grand Software QA).
2. Workday CXS returned HTTP 429 on every tenant this hour after heavy earlier probing — back off; retry next hour with curl --compressed and wider gaps between probes.
3. Zero-merge hours are expected: record them in JOBLESSONS and skip the board commit rather than forcing an empty one.

# JOBLESSONS_2026-11-23T1900EST

Hourly BESTIEJOB scan for Toronto ServiceNow / Salesforce jobs, run Monday 2026-11-23 19:00 EST (2026-11-24T00:02Z). Base: origin/main a49a5d3 (CI 18:18 EST scan). Commit 8bfac0c pushed to origin/main; GitHub Pages redeployed via pages.yml run 45294156749 (success, ~40 s). Live page: https://eltonaguiar.github.io/BESTIEJOB/ — 4,961 jobs (SN 860 / SF 943 / other 3158).

## Scan results

`node scripts/daily_job_scan.mjs` (no `--no-readme`, so the README `<!-- DAILY-SCAN -->` block was rewritten). Sources: SmartRecruiters(ServiceNow), Workday CXS, Greenhouse, Lever, Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna Canada API.

Source hit counts: Adzuna 199, LinkedIn 261, SmartRecruiters 12, Greenhouse 12, Ashby 2, Lever 1, Remote boards 6, Workday 0 — all 14 Canadian Workday boards returned HTTP 429 because the CI hourly scan (`0 * * * *` UTC = 19:00 EST) was running in its Workday probe window at the same minute. Per the runbook, Workday was left to the CI pass; manual re-probe of 3–4 key tenants (bmo, td, cibc, manulife, interac, salesforce, accenture) at ≥8 s spacing ~4 minutes after :00Z pays off if Workday freshness is needed.

Fresh from sources: 493 postings. Merged total: 5,661 (servicenow 1,201 / salesforce 4,303). Carry-prune dropped 1 stale row (>45 days). **Net-new URLs added to jobs.json: 35 (ServiceNow 16 / Salesforce 19), 0 removed.** Sources of the 35: Adzuna 14, LinkedIn 19, SmartRecruiters 1, Ashby 1.

## New Toronto/Canada SN/SF postings added (35)

ServiceNow (16): Amicis Global — ServiceNow BA Senior, Toronto; TD Bank — Senior Solution Architect (ServiceNow), Toronto; BMO — ServiceNow CMDB Administrator, Toronto + ServiceNow Technology Lifecycle Analyst, Toronto; CGI — ServiceNow Architecture Consultant, Calgary; Parkland Corporation — Sr Specialist ServiceNow Developer, Calgary; Deloitte — Senior Consultant ServiceNow Platform (DTC), Toronto; CONFIGURETEK — ServiceNow Developer, Ottawa; Cognizant — ServiceNow Software Asset Management Developer, Toronto; Pacer Group — ServiceNow Implementation Architect, Toronto; Avanciers Inc. — ServiceNow Implementation Architect, Toronto; KPMG Canada — Consultant/Senior Consultant ServiceNow Solution Developer, Toronto; Wipro — ServiceNow Implementation Architect, Mississauga; ServiceNow — Principal Solution Architect ServiceNow, Toronto/remote; Alimentiv — ServiceNow Platform Specialist, Toronto + London ON.

Salesforce (19): Cognizant — Salesforce Tech Lead (Remote), Toronto; Altus Group — Salesforce Platform Developer, Toronto; Konrad — Senior Salesforce Loyalty Developer + Salesforce Architect (Loyalty & Data 360), Toronto; Euna Solutions — Sr Salesforce Developer, Oakville; Flexstaf IT — Salesforce Revenue Cloud Architect, Toronto; Celestica — Student Intern Salesforce Developer 1, Toronto (entry-level Platform Developer match); Tata Consultancy Services — Senior Salesforce Developer ×2, Toronto; TD Bank — Software Engineer III Salesforce Data 360, Toronto; OSI Digital — Salesforce Developer ×3 (Toronto/Vancouver), Salesforce QA Tester + Business Analyst, Toronto; Deloitte — Senior Consultant Salesforce Platform (DTC), Toronto; Benevity — Senior Salesforce Administrator ×3 (Toronto×2, Calgary).

## Partner / target-company coverage this run

Banks/telecoms/technical: BMO, TD Bank, CGI, Telus/Bell/Rogers — Bell shows zero reqs (browser shows `(0)` for servicenow/salesforce — re-check weekly, not hourly); Rogers Phenom board returns a zero-row shell — rely on LinkedIn/Adzuna for Rogers rows. Scotiabank Phenom is dated-scrapeable but surfaced nothing new this window. Public-sector portals (gojobs.gov.on.ca, jobs.gc.ca) are Radware-walled — Job Bank remains the proxy, trust only title-named platform hits. Consultancies/partners: Deloitte, KPMG Canada, CGI, Wipro, Cognizant, Pacer Group, Avanciers, Altus Group, Konrad, Euna, Flexstaf, OSI Digital, Benevity, Alimentiv, ServiceNow itself.

## Entry-level / Platform Admin / Platform Developer I notes

Best entry-level match: Celestica "Student Intern, Salesforce Developer 1" (Toronto). Platform Admin-adjacent: Benevity "Senior Salesforce Administrator", Altus Group "Salesforce Platform Developer". Generic titles still need body-checks — Adzuna `apex`/`cpq` matches include false positives (Apex Legends gamedev, CPQ sales execs); reject before adding.

## Render caveat (verified against live jobs-data.json)

`build_site.py` collapses company+title mirrors. Verify new roles on the live page by **company + title**, not exact URL: 32 of 35 new roles rendered on jobs-data.json. Cognizant "Salesforce Tech Lead" and Wipro "ServiceNow Implementation Architect" render under alternative source twins (LinkedIn / Adzuna). 3 rows live in jobs.json but do not render as separate page cards: Benevity "Senior Salesforce Administrator" ×3 (ashby + 2 linkedin) — no surviving card carries that exact title; the pre-existing Benevity LinkedIn card is "Salesforce Administrator" (older req 4071588529). Jobs.json remains the system of record; the dropped rows are preserved there.

## Adzuna id recycling (re-confirmed)

Adzuna re-issues the same role under new ids; dedupe by fuzzy company + title tokens, not URL alone. `created` dates can be stale — check the detail page's JSON-LD `datePosted` when a surfaced ad looks old.

## What did not yield

Workday (429 window — CI pass covers it), LinkedIn detail pages (authwall risk — cards only, body-check ambiguous titles via browser `innerText` sliced from "Job Description"), Indeed/www.adzuna.ca (walled/CloudFront 403 — use the API), Job Bank keyword search (boilerplate false positives — trust only platform-titled hits), 100jobs.org (SPA shell — never cite as a posting).

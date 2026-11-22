# JOBLESSONS_2026-11-22T0200EST

Hourly BESTIEJOB cron scan — Toronto ServiceNow / Salesforce / platform-adjacent IT jobs.
Ran: Sunday 2026-11-22 02:00 EST (07:00Z). Base: origin/main 34b86b4 "fresh CA sweep 2026-11-22T06:48Z".
Commit: 96cd7d1 "cron: hourly Toronto SN/SF scan 2026-11-22T0705Z — 40 net-new URLs, dead Bell row dropped, site rebuilt".
Live page verified: https://eltonaguiar.github.io/BESTIEJOB/ ; deploy ran via pages.yml and completed ~40s after push.

## Result
- jobs.json: 5,595 rows (5,561 before this cycle's sweep base; 38 net-new URLs vs the pre-sweep base)
- Site: 5,016 cards (ServiceNow 875 · Salesforce 928 · other 3,213); 753 duplicate mirrors collapsed
- New ServiceNow mentions: 15 · New Salesforce mentions: 22 (some roles match both)
- Dropped: 1 dead row (Bell Canada Salesforce Developer, jobs.bell.ca 404 shell); 3 non-Canada rows (NeuraFlash "remote – Colombia") curated out before build

## Newly added roles (new to jobs.json this run; newest first)

ServiceNow
- 2026-11-21 Cloud Resourcing — CLDRSRC10472 Project Manager - ServiceNow ITSM/ITOM/CSM — Toronto (Hybrid) — adzuna.ca/details/5974418392
- 2026-11-21 La Caisse — Développeur(-euse), ServiceNow — Canada — adzuna.ca/details/5974102765
- 2026-11-18 TD Bank — Senior Solution Architect (ServiceNow) — Toronto — live on page via td.wd3.myworkdayjobs.com Workday req
- 2026-11-17 BMO — ServiceNow CMDB Administrator — Toronto — live via jobs.bmo.com
- 2026-11-17 BMO — ServiceNow Technology Lifecycle Analyst — Toronto — live via BMO Workday
- 2026-11-11 Cognizant — ServiceNow Software Asset Management Developer — Toronto
- 2026-11-11 Pacer Group — ServiceNow Implementation Architect — Toronto
- 2026-11-11 Avanciers Inc. — ServiceNow Implementation Architect — Toronto
- 2026-11-07 KPMG Canada — Consultant/Senior Consultant - ServiceNow Solution Developer — Toronto (Elite partner)
- 2026-11-04 Wipro — ServiceNow Implementation Architect — Mississauga (partner; page shows Adzuna mirror 5957373997)
- 2026-11-01 Deloitte — Senior Consultant, ServiceNow Platform (DTC) — Toronto (Elite partner)
- 2026-10-29 ServiceNow Inc. — Principal Solution Architect — Toronto/Remote — SmartRecruiters
- 2026-10-28 Alimentiv — ServiceNow Platform Specialist — Toronto & London

Salesforce
- 2026-11-21 Manulife — Salesforce Functional Analyst — Toronto/Waterloo — live via manulife.wd3 Workday req JR26101237
- 2026-11-21 IBM — Salesforce Senior Solution Architect — Toronto — adzuna.ca/details/5973912179
- 2026-11-21 Cognizant — Senior Salesforce Developer — Toronto — adzuna.ca/details/5973912092
- 2026-11-21 Altus Group — Salesforce Platform Developer — Toronto — live via simplyhired mirror
- 2026-11-21 Moneris — Principle Salesforce Developer — Toronto
- 2026-11-19 TD Bank — Associate Software Engineer (nCino/Salesforce) — Toronto
- 2026-11-19 Celestica — Student Intern, Salesforce Developer 1 — Toronto (entry-level)
- 2026-11-18 Konrad — Salesforce Architect (Loyalty & Data 360) — Toronto
- 2026-11-18 Tata Consultancy Services — Senior Salesforce Developer — Toronto (two mirrored LinkedIn URLs, both kept — distinct job IDs)
- 2026-11-12 OSI Digital — Salesforce Developer (Toronto + Vancouver), Salesforce QA Tester, Salesforce Business Analyst
- 2026-11-08 OSI Digital — Salesforce Lead — Toronto (OSI is a Salesforce partner)
- 2026-10-28 Benevity — Senior Salesforce Administrator — Toronto & Calgary — page renders as "Salesforce Administrator" under older LinkedIn card 4071588529 (mirror collapse)

Keyword/other
- 2026-11-21 CAA Club Group — Manager, Application Support & DevOps — Vaughan — linkedin 4458040990
- 2026-11-21 Communications & Power Industries — Business Intelligence Analyst - Data and Automation — Georgetown ON

## Partners / sponsors / target employers found this cycle
Confirmed Canadian platform hiring: BMO, TD, Manulife, CIBC (Workday boards — but see rate-limit note below), KPMG, Deloitte, Wipro, Cognizant, TCS, IBM, OSI Digital, Altus Group, Moneris, Celestica, Konrad, La Caisse, CAA Club Group, ServiceNow Inc., Alimentiv, Pacer Group, Avanciers, EY (ServiceNow IRM), LGS, CGI.

Bell: jobs.bell.ca is a dead/empty shell — this cycle's Bell row was dropped as 404. Bell's real ServiceNow hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn (Implementation Specialist, Développeur.euse ServiceNow, Architecte ITOM/ITAM already on the board from prior scans).
Rogers: Phenom board (jobs.rogers.com) unreachable — 404 shell / zero rows server-side. Rely on LinkedIn + Adzuna for Rogers leads; do not retry hourly.
Canadian government: jobs.gc.ca and gojobs.gov.on.ca are Radware-walled (captcha). Use Job Bank as proxy; trust only postings whose TITLE names ServiceNow/Salesforce (keyword body matches are noise — "shipping coordinator", "engineer in agronomy" false positives).

## What worked / what didn't
- Adzuna API (demo keys app_id=54ce986e / app_key=db851f299e966c0a2a72af525dce6199; pass explicitly or HTTP 400): 20 geo/keyword queries (Toronto, Ottawa, Mississauga; servicenow, salesforce, itsm, cmdb, itam, apex, agentforce, nCino, platform developer, etc.), max_days_old=14, sort_by=date. 196 matches — main freshness oracle. Space calls ≥3s (503s after ~4 rapid queries).
- LinkedIn guest search: intermittent HTTP 429; retry once after ~4 minutes — worked this run (163→170 postings). Detail pages serve authwalls intermittently; judge from cards + body.innerText only.
- SmartRecruiters (ServiceNow board): 12 matches, reliable.
- Greenhouse 14 / Lever 1 / Ashby 2 / remote boards 6: steady small contributors.
- Workday CXS: ALL boards HTTP 429 at 07:04Z (bmo, td, cibc, manulife, interac, accenture, salesforce, bdo, gdit, altusgroup, iko, huron, irvingoil, mckesson, brookfield, moneris, resolvetech). Known pattern: 429s hit at :00Z with the CI hourly scan and persist well past it; manual re-probe of ~10 tenants at ≥8s spacing succeeds 4–10 min later. Action: do not re-probe Workday in the same hour; let the CI pass carry Workday rows (they're carried into jobs.json by feed_carry).
- Adzuna re-issues the same role under new IDs (e.g. Amicis BA Senior 5972002660 vs 5972983023 twins). Dedupe on URL + job id; company+title twins are distinct rows in jobs.json but collapse to ONE card on the page (build_site mirror-collapse).

## Verification rules that kept this run honest
1. Never report additions by URL alone — build_site.py collapses company+title mirrors, so a new URL can vanish from jobs-data.json while the role still renders under an older surviving card (verified: Altus via simplyhired, Wipro via Adzuna 5957373997, Manulife via Workday req). Check live page by normalized company + title, and grep jobs-data.json for both.
2. Push race with CI: origin/main advanced (34b86b4, fresh CA sweep at 06:48Z) between my scan and push → push rejected non-fast-forward. Recipe: back up the commit (`git branch cron-scan-...`), `git reset --hard origin/main`, re-run `node scripts/daily_job_scan.mjs` (no --no-readme), `tools/verify_links.py --days 2`, curate out non-Canada rows, `tools/build_site.py`, `scripts/sync_readme_counts.py`, re-commit, push. Do NOT hand-merge generated-file conflicts.
3. Commit data pushes WITHOUT [skip ci] so pages.yml deploys; lessons/docs commits WITH [skip ci].
4. verify_links.py --days 2 only probes fresh rows (46 probed this run; 1 dead dropped). It never sweeps pre-existing dead links — per user standing instruction, do not prune dead links already on the board (Bell's dead row resurrects via README union; that's by design).
5. python3 on PATH is the Windows Store stub — run repo Python tools with C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe; git must be C:/Program Files/Git/cmd/git.exe (msys /mingw64 git is blocked).
6. GEO_KEEP's "remote|worldwide|anywhere" catch admits non-Canada remotes (NeuraFlash Colombia slipped in). Tighten to Canada-relevant geography next cycle.

## Git note
Commit 0e3bde4 (first attempt) abandoned and superseded by 96cd7d1 on branch cron-scan-2026-11-22T0700Z as backup. Remote canonical location: https://github.com/eltonaguiar/BESTIEJOB.git (push to .../bestiejob.git redirects).

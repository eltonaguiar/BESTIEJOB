# JOBLESSONS — BESTIEJOB hourly scan, 2026-11-21 19:00 EST

## Run summary
- Cron run: Saturday 2026-11-21 19:00 EST (America/Toronto)
- Board baseline: README.md / jobs.json at commit a7d52fa ("hourly scan 2026-11-21T18:00EST"), 5,590 listings; last scan stamp 2026-11-21T23:01:31Z (= 18:01 EST)
- Outcome: **0 new verified Toronto ServiceNow/Salesforce jobs**; nothing merged into README.md/jobs.json. Zero new verified jobs is a valid result per the runbook.

## Scope applied
- Tracks: ServiceNow (substantive platform/build duties), Salesforce (Apex/LWC/platform build), Other adjacent (ITAM, CMDB/CSDM, Discovery/MID Server, Integration Hub, etc.)
- Geography: City of Toronto / Ontario-eligible remote; a GTA office alone is not Toronto.
- Employers checked: Rogers, Bell, Canadian government, ServiceNow & Salesforce Elite/Select partners, World Forum / World Tour sponsors.

## Sources checked
- Web search: Indeed/LinkedIn/Glassdoor/ZipRecruiter/Toronto SN + SF queries; ServiceNow careers (careers.servicenow.com); Salesforce careers.
- Employer watchlist (employer-watchlist.csv, 24 sources): Atego, BMO/Procom, Cognizant, TD, Altus, Ensiti, Levio, NewRocket, Pentio, Lane Four, BDO, City of Toronto, Hydro One/Acronym, etc.
- Company careers direct: jobs.rogers.com (SuccessFactors), jobs.bell.ca / jobs.bce.ca, careers.servicenow.com, GCjobs / CMHC / House of Commons.
- Existing raw harvest in raw/ (Rogers, Scotiabank, CIBC, TD, BMO, LinkedIn, Workday) — mostly static JS shells or already indexed by the 18:01 scan.

## Dedupe against board (every candidate already present)
| Candidate | Source/URL | Status |
|---|---|---|
| Senior Salesforce Developer, Government of Canada | linkedin .../jobs/view/senior-salesforce-developer-at-government-of-canada-4481939757 | already in jobs.json |
| Senior ServiceNow Developer, Procom (banking client) | myprocom-portal .../jobs/senior-servicenow-developer-toronto-2a757e2b | already in jobs.json |
| Senior Systems Engineer, ServiceNow | smartrecruiters .../servicenow/744000162621080 | already in jobs.json |
| ServiceNow Developer contract, Brookfield | workday ...R2053249 | already in jobs.json |
| Staff Security Engineer roles, ServiceNow | careers.servicenow.com + LinkedIn | already in jobs.json |
| Bilingual Senior Specialist ServiceNow ITSM, CMHC | careers.cmhc-schl.gc.ca .../601524317 | already in jobs.json |
| ServiceNow Platform Developer, Acronym/Acroynon | linkedin 4492159456 / 4484516741 | already in jobs.json |
| Bell Salesforce Marketing Cloud Email Developer | jobs.bce.ca .../1378220200 | already in jobs.json |

## Partners / Elite / sponsors checked
- ServiceNow Elite/Global Elite implementation partners with Canada/Toronto coverage: Fujitsu (Elite consulting), plus Select/local boutiques Pentio (Toronto) and NewRocket (elite); Ateko (Toronto World Forum sponsor — ServiceNow routed to FX Innovation careers).
- Salesforce Canada partners / World Tour Toronto sponsors: Lane Four, Slalom, Ateko, CloudFulcrum; CloudKettle (a Bell Canada company).
- Technical end-users / sponsors: Rogers (jobs.rogers.com SuccessFactors — JS shell, no static listings), Bell (jobs.bell.ca/jobs.bce.ca), Canadian government (GCjobs, CMHC, House of Commons, ServiceNow Protected B Canada roles), City of Toronto.

## Lessons / patterns
1. The 18:01 EST hourly scan (Adzuna + LinkedIn + SmartRecruiters + Greenhouse + Lever + Ashby + RemoteOK/Jobicy/Remotive) is comprehensive for Toronto SN/SF; a same-day +1 hour re-scan at 19:00 returned only duplicates. Re-scanning within the same day adds little unless a new source is added.
2. Company careers pages (Rogers SuccessFactors, Bell) render as JS shells in static fetch; their listings only reach the board via LinkedIn/aggregator mirrors already captured.
3. Government roles (CMHC, House of Commons, ServiceNow Protected B) are already indexed via LinkedIn/careers domains; "gcjobs" searches surface the same reqs.
4. Aggregator URLs (e.g. myrichmondhillontario.ca for Acronym) are duplicates of employer/LinkedIn reqs already in the board — dedupe by employer + role + canonical URL, not by aggregator link.
5. All Rogers/Bell/Government candidates found this run were already in jobs.json; the board's dedupe by normalized URL is working.

## Next-run recommendations
- Do not re-run the same 9-source scan within the same day expecting new hits; rotate to a different channel (partner careers pages directly, provincial job banks, or a new watchlist employer) before expecting incremental verified jobs.
- When adding a new employer, verify via employer careers + ATS detail (form_reached / apply_shown), not a careers homepage or mirror.
- Keep JOBLESSONS timestamped per run so future agents can compare hourly outcomes.

## Board state
- README.md and jobs.json unchanged this run (no new verified jobs to merge).
- public/ (GitHub Pages, eltonaguiar.github.io/BESTIEJOB/) already built 2026-11-21 18:24 after the 18:01 scan; no rebuild needed.

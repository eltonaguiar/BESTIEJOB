# JOBLESSONS_2026-11-16 — hourly cron scan (19:00 EST / 00:00 UTC)

## Result this run
- Fresh Toronto ServiceNow / Salesforce scan at 19:00 EST: `scripts/daily_job_scan.mjs` (SmartRecruiters ServiceNow, Workday CXS, Greenhouse, Lever, Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna Canada). 797 fresh postings surfaced; jobs.json now 2845 listings (SN 1307 / SF 1373).
- **41 verified fresh merges into README.md** (all posted 2026-11-16 except one 2026-11-15, all Canada-scope, direct posting deep-links, deduped against jobs.json + README tables + APPLIED.md + dead_urls.txt):
  - ServiceNow table 1297 → 1315 rows (+18)
  - Salesforce table 1505 → 1528 rows (+23)
  - Board total 7544 → 7585 live postings
  - public/ rebuilt with `python3 tools/build_site.py` (5769 cards, 45 applied hidden); `scripts/check_site_links.py` OK.
  - Committed and pushed to main → GitHub Pages redeploys via pages.yml.

Priority matches for the Platform Administrator / Platform Developer I (entry-level/junior) emphasis — Toronto-area, platform build/admin roles:
ServiceNow
- ServiceNow ITOM / CMDB Developer — AllianceIT Inc — Toronto, ON, Canada — LinkedIn
- ServiceNow IRM Sr. Developer — BURGEON IT SERVICES — Toronto, ON, Canada — LinkedIn
- ServiceNow IRM Senior Developer — BURGEON IT SERVICES — Greater Toronto Area — LinkedIn
- ServiceNow HRSD — NLB Services — Mississauga, ON — LinkedIn
- ServiceNow CSM/HRSD — NLB Services — Mississauga, ON — LinkedIn
- ServiceNow Developer — Resource Logistics Inc. — Toronto, ON — LinkedIn
- ServiceNow Developer — NLB Services — Canada — LinkedIn
- ServiceNow Developer — Envision Technology Solutions — Toronto, ON — LinkedIn
- ServiceNow SPM Developer — Astra-North Infoteck Inc. — Toronto, ON — Adzuna
- Senior Solution Architect (ServiceNow) — TD Bank — Toronto, ON — Workday (employer board)

Salesforce
- Salesforce Administrator (Remote) — Hired — Canada — LinkedIn
- Salesforce Developer – Financial Services Cloud (FSC) — Astra-North Infoteck Inc. — Toronto, ON — Adzuna
- Senior Salesforce Financial Services Cloud Developer — Astra-North Infoteck Inc. — Toronto, ON — Adzuna
- Senior Salesforce Developer (Apex / LWC) — Astra-North Infoteck Inc. — Toronto, ON — Adzuna
- Salesforce FSC Developer — Pacer Group — Toronto, ON — Adzuna
- Software Engineer III - Salesforce Data 360 — TD Bank — Toronto, ON — Adzuna
- Salesforce Engineer / Developer — MLSE — Toronto, ON — Adzuna
- Salesforce Consultant — Robert Half — Canada — LinkedIn

Secondary (merged, but architect / Marketing Cloud / migration / other Canada — not the Platform Admin/Dev I emphasis): 13 Salesforce rows (Technical Architect CPQ/Revenue Cloud ×2 Smart IT Frame, Cognizant, Alithya, Univedge Loyalty Cloud, Plus Company Marketing Cloud, Lumenalta MuleSoft, Keyloop CPQ PM, VTRAC Commerce Migration, Astra-North Marketing Cloud/GCP, Salesforce.com Talent Advisor, Xideral French Canada) and 8 ServiceNow rows (3 Vancouver architects/leads, Raas/Yochana ITAM architects, Cognizant AICT architect, TD duplicate req, Conseiller ITSM Montreal).

## Sources checked — 19:00 EST
- **Workday CXS** (POST /wday/cxs/{tenant}/{site}/jobs, curl --compressed, one call at a time, ~6s gaps): all 10 Canadian tenants × {ServiceNow, Salesforce} returned **HTTP 429** this hour — bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, sunlife.wd3/Experienced-Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site, plus moneris/caatpension/bdo/altus/iko/huron/irvingoil/mckesson/brookfield/gdit/resolvetech. No usable data. **Back off; sleep ≥6s between probes; retry next hour — do not conclude boards are empty from 429s.** (Same wall as the 15:00 and 18:00 EST runs.)
- **LinkedIn guest**: 255 cards (ServiceNow/administrator/developer/consultant + Salesforce variants, f_TPR=r86400 where supported). Detail pages not re-fetchable at scale this run; titles treated as scan-verified, not body-verified.
- **Adzuna Canada**: 503 (28 date-sorted queries, max 14 days, Toronto + Canada-wide incl. it reporting/it asset management/cmdb/itsm reporting/apex/cpq/marketing cloud/agentforce).
- **SmartRecruiters ServiceNow**: 12. **Lever**: 1 (Alimentiv). Greenhouse/Ashby/remote feeds: no new Canada platform hits.
- **gap_scan** (raw/gap_scan_2026-11-16.json): partner/Elite-sponsor career sites (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) — Lane Four Salesforce roles undated (merger skips undated); all others 0.
- **Rogers** (jobs.rogers.com, date-sorted): 0 open positions matching servicenow/salesforce. **Bell** (jobs.bell.ca): 0 reqs; JS-rendered, not curl-scrapeable — re-check weekly, not hourly.
- **Public sector/government**: jobs.gc.ca NXDOMAIN; gojobs.gov.on.ca Radware-walled; Job Bank OPS feed 0 platform-titled postings; City of Toronto 0 SN/SF cards.
- Known Workday CXS tenants (200, curl --compressed, wdN host, bare tenant host is NXDOMAIN): bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site, sunlife.wd3/Experienced-Jobs, caatpension.wd10/Careers, iko.wd3/IKO_Careers.

## Dedup & verification procedure followed
1. Candidate key = normalised URL (strip utm_/tracking query, trailing slash) checked against jobs.json (system of record) + README.md tables + APPLIED.md (hard exclude — never re-add applied roles) + dead_urls.txt.
2. Freshness bar: postedDate within yesterday/today (2026-11-15 → 2026-11-17 UTC scan day); direct posting deep-link (is_listing_url() rejects hubs/search pages — LinkedIn /jobs/*-jobs, Indeed /q-, Adzuna hub, jobs.ca company hubs all excluded).
3. Canada scope (region hints: Ontario/Quebec/BC/Alberta/Canada/remote; US/offshore hints excluded).
4. Platform title bar: tags/family = ServiceNow or Salesforce only; excluded non-platform matches (Incident Coordinator, Project Manager/Leader).
5. Excluded Salesforce roles that aren't Platform Admin/Dev I from the *priority* list (architect/CPQ/Revenue Cloud/Marketing Cloud/MuleSoft/Consultant-general) but kept them on the board because the board already carries architect/consultant rows — segmented in this lessons file so the user can prioritize applications.
6. Rows inserted at top of the matching README table (newest first); Contents / section heading / details-summary counts and window total bumped; public/ rebuilt; check_site_links passed before push.

## Market-shape notes (2026-11-16, stable)
- Hourly supply near zero: 41 merges this hour after 0-merge runs at 13:00–18:00 EST. Normal late-2026 pattern — commit what's verified, skip empty hours.
- Fresh platform work comes via consultancies/staffing (Astra-North, BURGEON, NLB, Envision, Resource Logistics, Pacer, Robert Half, Hired) and banks' Workday tenants (TD via Workday careers site); vendor twins (different staffing firms, same client req) are kept as distinct postings.
- ServiceNow-the-company: Toronto postings are sales/SRE/security only; no Platform Admin/Dev I. Salesforce-the-company: Vancouver LMTS only, nothing below 4 days old in Toronto.
- Rogers/Bell: no platform reqs this hour. Partners/Elite sponsors (Accenture, Deloitte, KPMG, PwC, CGI, Capgemini, FX Innovation, Lane Four): no new Toronto SN/SF hits; Accenture Workday has 1,600+ ServiceNow requisitions but effectively none Canadian on page 1 — use its national careers site.

## Recurring collision pattern
- The GitHub Actions hourly scan (`chore(jobs): hourly scan refresh ... [skip ci]`) pushes to origin/main at :00 UTC — the same moment this run pushes. If rejected (non-fast-forward): `git fetch origin && git pull --rebase --autostash origin main && git push origin main`; never `--force` (destroys the scan's jobs.json/public work). [skip ci] only on docs-only commits; data commits must not carry it so pages.yml redeploys.

## New lessons
1. Workday CXS is now 429ing across all 10 Canadian tenants on :00 UTC hours (15:00, 18:00, 19:00 EST runs) — rate limit is time-of-day correlated, not tenant-specific; shift non-critical probes off the hour.
2. LinkedIn guest search returns cards but detail-page bodies can't be re-fetched at scale; mark LinkedIn-only leads "scan-verified, not body-verified" in README notes.
3. jobs.json (scan system of record, 2845 listings) leads README (7585 rendered rows): README carries older/readme-only rows jobs.json has pruned — build_site.py unions both, so nothing public is lost when README lags.
4. README heading counts and Contents anchors drifted (ServiceNow Contents 1298 vs body 1297; Other 4777 vs 4776) — when merging, set Contents count equal to the new body count so anchors stay valid.

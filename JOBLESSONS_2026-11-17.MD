# JOBLESSONS_2026-11-17 — 00:00 EST (05:00 UTC) hourly scan

**Scope:** fresh Toronto/GTA ServiceNow + Salesforce jobs, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Dedupe against jobs.json, README.md tables, and APPLIED.md (URL normalization: strip query strings/trailing slashes). Merge verified fresh jobs to jobs.json + README + public/ (GitHub Pages).

## What ran
1. Canonical hourly scan: `node scripts/daily_job_scan.mjs` (SmartRecruiters ServiceNow, Workday CXS 14 boards × servicenow/salesforce, Greenhouse/Lever/Ashby boards, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna 29 CA queries).
   - fresh=836, merged=2864 (jobs.json 2844 → 2864 before liveness gate).
   - `python3 tools/verify_links.py --days 2`: 162 fresh rows probed, 1 dead dropped (jobicy.com Senior DevOps Engineer — 404), 104 unknown kept, 2863 retained.
   - `python3 tools/build_site.py`: public/jobs-data.json + public/index.html rebuilt — locally 5784 jobs (servicenow 956 / salesforce 1012 / other 3816), built 2026-11-17 05:07 UTC.
2. Targeted Toronto SN/SF enrichment (sources the aggregators under-cover): LinkedIn guest browser (Toronto, f_TPR=r86400) × ServiceNow and × Salesforce; Workday CXS extra tenants cibc.wd3/search, interac.wd3/interac, manulife.wd3/MFCJH_Jobs, accenture.wd103/AccentureCareers; Rogers date-sort listing; Job Bank text search; partner/Elite Partner career pages (Deloitte, Cognizant, CGI, KPMG, TCS, IBM, DXC, Accenture national site, Salesforce careers); Job Bank as proxy for jobs.gc.ca/gojobs.gov.on.ca (both Radware-walled).
3. Race with origin: the Actions hourly scan (a0c1611, 04:15 UTC, 6289 listings) landed while this run was in flight. Rebased onto it with upstream wins on generated files (jobs.json + public/*), pushed 69e442b. Live page: HTTP 200; jobs-data.json serves 5767 jobs (servicenow 954 / salesforce 1006).

## Fresh verified Toronto SN/SF jobs merged this run: 0
Every platform-titled candidate surfaced was already on the board:

- LinkedIn guest, Toronto, past 24h — ServiceNow: 61 cards; all SN-titled ones already present (4490660430 NLB CSM/HRSD, 4490926514 Envision CMDB Consultant, 4490602725 AllianceIT ITOM/CMDB Developer, 4490663180 NLB HRSD, 4491539817 TD Senior Solution Architect, 4489780092 Resource Logistics Developer, 4490936151 IMR Soft CMDB Consultant). Salesforce: 60 cards; the only Platform-titled hit, HCLTech Salesforce Administrator 4490676918, was already in jobs.json (ingested by this run's own scan pass and also on origin's board). Noise: PwC Brasil roles (not Canada), Four Seasons/Salesforce-the-company MTS (not Platform Admin/Dev I), Smart IT Frame "Salesforce Technical Architect CPQ" 4490945616 (previously flagged off-target).
- Workday CXS extra tenants: HTTP 429 on every probe — Workday is rate-limiting this host right now (the scan's Workday boards 429'd too, except salesforce which returned 2 postings). Space calls ≥5s; treat Workday as weekly, not hourly, when 429'd.
- Rogers jobs.rogers.com date-sort page 1: retail sales/finance roles dated Nov 15–16, zero ServiceNow/Salesforce titles.
- Job Bank: text search is noise (no platform-titled postings); jobbank.gc.ca posting pages 404 once expired, so search hits are not proof of live postings.
- Partners/Elite Partners: Deloitte Senior Consultant Salesforce Platform (Jul 9 — stale), Cognizant Salesforce Solution Architect Toronto (Nov 4 — architect tier), Cognizant Jr ServiceNow ITOM/SOMT (Sep 10 — stale). No entry-level Platform Administrator / Platform Developer I anywhere this hour.
- Bell: skipped — jobs.bell.ca shows (0) for servicenow and salesforce; re-check weekly, not hourly.

## Recurring pattern
This is the third consecutive hour (20:00/21:00/22:00/23:00 EST Nov 16, plus 00:00 EST Nov 17) with effectively zero fresh Toronto Platform Admin/Dev I postings. Market shape holds: fresh platform work = senior/architect roles at banks (BMO/TD Workday) and GRC/IRM consultancies (PwC ServiceNow IRM practice); ServiceNow-the-company and Salesforce-the-company post nothing below 4 days and no Platform Admin/Dev I in Toronto.

## Inbox
`inbox/todayfeeds--2026-11-16--v1.md` is well-formed (passes check_inbox.py) but every row is undated ("—"), so the merger skips them — nothing merged from it.

## Files changed
- jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json (scan + liveness gate)
- public/jobs-data.json, public/index.html (site build)
- README.md (DAILY-SCAN block refreshed), FRESH_JOBS.md (rewritten)
- Commit 69e442b `chore(jobs): 00:00 EST scan refresh (2863 listings, 2026-11-17T05:07Z) [skip ci]`, pushed to origin/main; GitHub Pages serving it.

## Recommended next-hour focus
- Re-probe Workday CXS tenants after a cooldown (cibc/interac/manulife/accenture were 429'd this hour).
- Keep LinkedIn guest browser (not the API — API 429s; Playwright fallback works) for Toronto f_TPR=r86400 sweeps.
- Rogers: page 1 clear today; consider paging only if a platform title appears.
- Do not re-scan jobs.gc.ca/gojobs.gov.on.ca until the Radware wall lifts; Job Bank title-filtered search remains the public-sector proxy.

## 08:00 EST scan (this run) — merged 0

**Named-employer spot checks (Rogers, Bell, Government of Canada/Ontario):**
- Rogers: jobs.rogers.com date-sort page 1 — zero ServiceNow/Salesforce titles; page clear for the second scan in a row.
- Bell: web search surfaced ServiceNow Developer / Integrator, Req 431695 (Toronto among Montreal/Ottawa/Toronto/Quebec City). Opened the posting: "the job you are trying to apply for has been filled" → dropped, not merged. Salesforce query returned only sales-rep roles mentioning Salesforce (not Platform Admin/Dev I) → noise. Existing Bell rows stay on board: 432824 ServiceNow System Administrator (2026-10-25), 432829 ServiceNow Senior Technical Advisor (2026-10-19).
- Government of Canada/Ontario: jobs.gc.ca and gojobs.gov.on.ca behind Radware bot manager; Job Bank title-filtered Toronto proxy returned 0 platform postings. Still walled — re-check weekly, not hourly.

**Dedupe vs board:** every LinkedIn-fresh SN/SF card in today's raw files (NLB CSM/HRSD 4490660430, Envision CMDB Consultant 4490926514, AllianceIT ITOM/CMDB 4490602725, NLB HRSD 4490663180, TD Senior Solution Architect 4491539817, Resource Logistics 4489780092, IMR Soft 4490936151, Smart IT Frame CPQ 4490672278/4490945616) was already on the board or previously flagged off-target — none new.

**Result:** 0 fresh verified Toronto SN/SF jobs merged this hour — third scan today (00:00, 07:00, 08:00 EST) with no new Platform Administrator / Platform Developer I postings. Board state unchanged: README tables, jobs.json and public/ untouched; no generated-file commit needed. Live page keeps serving the previous build.

## 09:00 EST scan (this run) — merged 0

**Scope:** fresh Toronto/GTA ServiceNow + Salesforce jobs, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Dedupe against jobs.json + README.md tables. Named-employer spot checks: Rogers, Bell, Government of Canada/Ontario, ServiceNow/Salesforce partners & Elite Partners.

**What ran / checked:**
1. Today's Workday tenant scans (raw/wd20261117/): BMO ServiceNow CMDB Administrator & Technology Lifecycle Analyst (Toronto, 5d ago), BMO SAM Administrator–ITAM (14d), Interac Sr Business Systems Analyst & QE Senior Specialist (Toronto, 30d+), TD Senior Solution Architect SN (Toronto, yesterday), TD Software Engineer III Salesforce Data 360 (Toronto, 4d), Manulife Salesforce Functional Analyst (Waterloo, 15d). All already on the board or off-target (non-Toronto, senior, architect, or functional analyst — none Platform Admin/Dev I).
2. 08:00 EST 105-board canonical scan (on origin/main): 0 net-new ServiceNow, 4 net-new Salesforce — Jobgether AVP Salesforce Engineering & Voice, Jobgether Associate Salesforce Administrator (Canada-wide, not Toronto), Docebo Senior Salesforce Developer (Toronto, senior tier). None entry-level Platform Admin/Dev I in Toronto.
3. LinkedIn guest browser: 0 cards (guest/API rate-limited this hour).
4. Web-search due diligence: Bell ServiceNow SysAdmin (Posted Oct 22, deadline Nov 3 — filled/expired, 3+ yrs), Bell Enterprise Solutions Architect II (architect tier), Job Bank Gov of Canada ServiceNow SPM developer contract (5+ yrs, CSA+CAD — intermediate/senior). Workopolis/Glassdoor surface intermediate+ roles only (CGI Toronto $80k–$130k, BFG Markham intermediate). No Platform Administrator / Platform Developer I posted ≤7 days in Toronto.

**Named employers:** Rogers jobs.rogers.com page 1 — zero SN/SF titles (clear 2nd scan in a row). Bell — expired/filled SysAdmin + architect + sales-rep noise; existing Bell rows 432824/432829 stay on board. Government of Canada/Ontario — jobs.gc.ca & gojobs.gov.on.ca still Radware-walled; Job Bank Toronto proxy = 0 platform postings. SN/SF partners & Elite Partners (Deloitte, Cognizant, CGI, KPMG, TCS, IBM, DXC, Accenture) — architect-tier or stale Jul–Sep postings only.

**Result:** 0 fresh verified Toronto SN/SF jobs merged this hour — fourth consecutive scan today (00:00, 07:00, 08:00, 09:00 EST) with no new Platform Administrator / Platform Developer I postings. Board state unchanged: README tables, jobs.json and public/ untouched; no generated-file commit needed. Live page keeps serving the previous build.

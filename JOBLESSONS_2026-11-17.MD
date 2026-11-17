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

## 10:00 EST scan (this run) — merged 0

**Scope:** fresh Toronto/GTA ServiceNow + Salesforce jobs, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Dedupe against jobs.json + README.md tables.

**What ran / checked:**
1. Adzuna CA API, `max_days_old=2&sort_by=date&where=Toronto`, `what=ServiceNow` (40 results) and `what=Salesforce` (pp. 1–2, 140 results): only one platform-titled hit — "ServiceNow SPM Developer", Astra-North Infoteck Inc., Toronto, created 2026-11-16T12:16:09Z — already on board as `adzuna:adzuna.ca/details/5968012935` (jobs.json:230). Salesforce page 2 surfaced only Technical Lead (Astra-North), Senior Production Support Engineer (Astra-North), Technical Architect (Cognizant) — lead/architect/senior tiers, none Platform Administrator / Platform Developer I.
2. LinkedIn guest browser, Toronto f_TPR=r86400 × ServiceNow and Salesforce: sign-in modal ("Sign in to view more jobs") blocked the results panel — 0 cards accessible; guest/API wall for a second consecutive hour.
3. Workday CXS known tenants (BMO/TD/CIBC/Manulife/Interac/Accenture/Salesforce): 429 on every probe since this morning — rate-limited host; treated as weekly, not hourly.
4. Rogers `jobs.rogers.com` date-sort page 1 (rows dated Nov 13–17, incl. Nov 17): 25 rows, all sales/retail/finance/HR — zero ServiceNow/Salesforce titles; clear for the third scan in a row.
5. Bell: `jobs.bell.ca` returns (0) for both platforms — weekly re-check only.
6. Government of Canada/Ontario: jobs.gc.ca and gojobs.gov.on.ca behind Radware bot manager; Job Bank raw search HTML is a JS shell with no job cards, and full-text search is title-noise — no usable postings. Job Bank as public-sector proxy returned nothing platform-titled.
7. Partners / Elite Partners via web search: SS&C Technologies "Salesforce Implementation Consultant & Platform Administrator" Toronto (posted Nov 3, 2026 — stale, 3–5+ yrs exp); Infotek Consulting "Salesforce Platform Administrator/Architect" Toronto (posted 2026-11-10, expired 2026-11-16); Make-A-Wish Canada "Senior Salesforce Administrator" (Nov 5, 5+ yrs, senior). None fresh (≤2 days), none entry-level Platform Admin/Dev I.

**Dedupe vs board:** the sole Adzuna hit already exists on the board (adzuna:adzuna.ca/details/5968012935). No new URLs, titles, or company+title pairs to add.

**Result:** 0 fresh verified Toronto SN/SF jobs merged this hour — fifth consecutive scan today (00:00, 07:00, 08:00, 09:00, 10:00 EST) with no new Platform Administrator / Platform Developer I postings. Board state unchanged by this run; origin's own 14:14 UTC scan refresh (c87e23e, 2827 listings) is already deployed. Live page verified: HTTP 200, jobs-data.json serves 5787 jobs, matches `public/jobs-data.json` in repo.

**Market shape holds:** fresh platform work = senior/architect roles at banks (BMO/TD Workday) and GRC/IRM consultancies; ServiceNow-the-company and Salesforce-the-company post nothing below 4 days and no Platform Admin/Dev I in Toronto.

**Recommended next-hour focus:** re-probe Workday CXS tenants after cooldown (≥5s spacing between calls); keep attempting LinkedIn guest browser (wall may lift); Rogers page 1 clear — page deeper only if a platform title appears; public-sector portals stay Radware-walled, re-check weekly; Adzuna demo key remains usable (51 requests, 0 misses).


## 17:00 EST scan (this run) — merged 0

**Scope:** fresh Toronto/GTA ServiceNow + Salesforce jobs, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Dedupe against jobs.json + README.md tables.

**What ran / checked:**
1. Adzuna CA API, `max_days_old=2&sort_by=date`, `what=` over 17 ServiceNow/Salesforce queries × 3 geos (Toronto, Ontario, Canada) = 51 requests, window 2026-11-16 → 2026-11-17; every candidate URL HTTP-verified (2xx or 401/403 treated as live). 32 platform-titled Canadian candidates.
2. Named-employer spot checks: Rogers (Workopolis ITSM ServiceNow role, Brampton — posting date not confirmed fresh, not added), Bell (jobs.bell.ca/jobs.bce.ca — 0 platform postings; existing Bell rows 432824/432829 stay on board), TD (Salesforce Data 360 ×2 — already on board), ServiceNow Careers Ontario, Salesforce Canada careers, Job Bank as GC/Ontario public-sector proxy (0 platform postings; jobs.gc.ca/gojobs.gov.on.ca Radware-walled).

**Dedupe vs board:** 31 of 32 candidates already on the board by canonical URL. The 32nd ("ITSM Platform Migration Lead – Zendesk to OpenText SMAX", Astra North Infoteck Inc., Waterloo, adzuna.ca/details/5968301899, created 2026-11-16) is the same posting already on README via LinkedIn guest (ca.linkedin.com/jobs/view/...4490686438) — same role/company/location/date, different URL — so treated as already-covered, not merged. No genuinely new URL, title, or company+title pair to add.

**Result:** 0 fresh verified Toronto SN/SF jobs merged this hour — sixth consecutive scan today with 0 new Platform Administrator / Platform Developer I postings. Board state unchanged: README tables, jobs.json and public/ untouched; no generated-file commit needed. Live page keeps serving the previous build (HTTP 200).

**Market shape holds:** fresh platform work = senior/architect roles at banks (BMO/TD Workday) and GRC/IRM consultancies; ServiceNow-the-company and Salesforce-the-company post nothing below 4 days and no Platform Admin/Dev I in Toronto.

**Recommended next-hour focus:** re-probe Workday CXS tenants after cooldown (≥5s spacing; host is 429'd); keep attempting LinkedIn guest browser; Rogers page 1 clear for multiple scans; public-sector portals stay Radware-walled, re-check weekly; Adzuna demo key remains usable (51 requests, 0 misses).

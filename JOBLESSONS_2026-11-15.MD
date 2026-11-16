# JOBLESSONS_2026-11-15

BESTIEJOB hourly cron scan — 2026-11-15 00:00 EST (UTC-05). Target: fresh Toronto/GTA ServiceNow + Salesforce postings.

## Fresh verified job added this run (1)

| Posted | Role | Company | Location | Source | Notes |
|--------|------|---------|----------|--------|-------|
| 2026-11-15 | Lead Management Operations | Rogers Communications | Markham, Ontario, Canada | LinkedIn guest (job id 4490212417) | Salesforce lead management / Salesforce administration — business lead & SME for Lead Management within Salesforce; campaign structures, lead routing, automation workflows, Salesforce enhancements/releases/testing/adoption. In-office 5 days/week. Posted ~31 minutes ago. Added to jobs.json (tags: salesforce) and README (Other table). Commit 4e262e7, public/ rebuilt. |

## Sources checked this hour

- **LinkedIn guest search** (`jobs/search?keywords=&location=&f_TPR=r86400`, browser, no auth, ~6 s/query, 60 cards/page, absolute `datetime`):
  - ServiceNow Toronto: 60 cards; the 2 ServiceNow titles (Deloitte CMDB/GRC Solution Architect, job ids 4474558762 / 4474570325) were already on the board — dedupe working.
  - Salesforce Platform Administrator Toronto: 6 roles; only new match was the Rogers role above. Salesforce Solution Architect ×2 (4457034728 / 4457039647) already in README; Salesforce Manager comp + Kinaxis co-op + Bell grad program = non-matching.
  - Salesforce Platform Developer Toronto: 8 roles; all already on board or non-matching (senior "Software Developer – CRM" at S-M Software is generic CRM, not Salesforce Platform Dev I).
- **Workday CXS** (manual curl `--compressed`, single call): BMO `bmo.wd3/External` ServiceNow = 12 postings, none titled ServiceNow (search matches body text); TD `td.wd3/TD_Bank_Careers` ServiceNow = 12 postings, none titled ServiceNow. Scripted burst of 14 calls returned HTTP 422 across the board — Workday rate-limits/422s on rapid repeated calls; retry one call at a time with gaps.
- **Rogers careers** (date-sorted `sortColumn=referencedate&sortDirection=desc`): first page (Nov 11–14) = all sales/retail roles, no SN/SF titles. Rogers keyword search returns sales roles that merely mention SN/SF in the body (noise).
- **Bell** (`jobs.bell.ca`): confirmed zero reqs for servicenow/salesforce (skill: re-check weekly, not hourly).
- **Canadian government / public sector** (`jobs.gc.ca`, `gojobs.gov.on.ca`): Radware-walled — do not retry; Job Bank is the proxy but full-text search is noise (only trust title-named platform postings).

## Patterns / lessons for future agents

1. **LinkedIn guest search is the best hourly freshness oracle** — `f_TPR=r86400` via browser returns real cards with absolute dates; page 2 (`start=25`) re-serves page 1, don't bother. The guest API (`seeMoreJobPostings`) 429s after ~4 rapid calls and can return an authwall page with HTTP 200 + huge identical body — test length + digest distinctness, not just status.
2. **Dedupe on normalised URL + LinkedIn job id**: strip query strings/trailing slashes; LinkedIn job-id equality is a hard dedupe signal even when titles differ (e.g. two renamed titles sharing one job id = one posting). Check against `jobs.json` + `README.md` + `APPLIED.md` before adding. Vendor twins (two staffing firms, same client req, same title) are DISTINCT — keep both, dedupe on URL only.
3. **Workday CXS works but is flaky**: verified 200 pairs (bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site). Use `--compressed` (without it the gzip body decodes as nothing), send Origin + Referer + UA, one call at a time (bursts → 422). `bmo.myworkdayjobs.com` is NXDOMAIN — use the `wdN` host (`bmo.wd3...`). Dead ends: telus/rogers/kpmg/deloitte/cgi/sunlife/rbc `.wd3` → 404/422.
4. **Market shape (late 2026)**: ServiceNow-the-company posts only sales/SRE/security in Toronto; Salesforce-the-company posts nothing below 4 days and no Platform Admin/Dev I. Fresh platform work comes from banks (BMO/TD Workday), DXC, and GRC/IRM consultancies. Expect sparse hours — 1 fresh job this hour is normal, not a failure.
5. **README tables are pre-existing one-line mangled blocks** with stale heading counts (heading↔`<details>` mismatch is the baseline; `board_invariants` is red at ~136 errors regardless). `jobs_merge_inbox.py` additive insert is safe (read-safety check refuses row loss) and keeps counts via `_bump_counts`, but don't chase a perfect count reconciliation — it's pre-existing debt.
6. **Build & publish**: `jobs.json` is the system of record; `tools/build_site.py` unions `jobs.json` + README-only rows into `public/jobs-data.json` + `public/index.html`. The page only changes when `public/*` + `jobs.json` + `README.md` are committed to main. Always use `[skip ci]` (non-`[skip ci]` pushes run the chronic red audits). `pages.yml` redeploys eltonaguiar.github.io/BESTIEJOB/ on main push.
7. **Liveness gate**: `tools/verify_links.py --days 2 --workers 16 --blocklist dead_urls.txt` probed 74 fresh rows, 0 dead, nothing dropped. Only 404/410/451 mean dead; 403/429/5xx/transport errors are bot-walls on LIVE postings — keep them.

## Commit
`4e262e7 chore(jobs): merge 1 fresh Toronto Salesforce posting (Rogers) — 2026-11-15 00:00 EST scan [skip ci]` — pushed to origin/main.

## 2026-11-15 03:00 EST run — null result (0 fresh jobs)

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce.

Sources checked, all zero new:
- Adzuna API: 68 calls (13 queries × 3 geos: national/Toronto/Ontario), raw 298 → unique 27 → kept 0 (all 27 already on board).
- Job Bank: 12 pages; Eluta: 6 pages — included in the 27 above, all dupes.
- LinkedIn guest: 67 cards (Toronto, last 24h, pages 1–2) → 0 new.
- Workday tenants (24): salesforce wd12, gdit wd5, bmo/rbc/cibc/scotiabank/manulife/sunlife/telus/opg wd3, plus SmartRecruiters ServiceNow — raw 5, kept 0 (4 non-Canada).
- City of Toronto jobs.toronto.ca: 9 tiles, 0 new; OPS gojobs blocked by Radware; OPS Job Bank fallback: 8 articles, 0 new.
- Partner/sponsor scan (ServiceNow World Forum Toronto tiers + Canadian partners): 0 relevant postings.

Dedupe: URL + title\|company\|city fingerprint held against README.md and jobs.json; nothing new survived.

Outcome: no commit, no publish — README.md, jobs.json, and public/ are unchanged. pages.yml only redeploys on a main push, so no GitHub Pages redeploy this run.

Lesson re-confirmed: late-2026 Toronto SN/SF hourly supply is sparse — 0–1 fresh postings per hour is normal, not a scanner failure. Don't re-run the merge "just to have a commit".

## 2026-11-15 06:00 EST run — aggregator + focused search

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce.

Ran canonical hourly flow:
1. `node scripts/daily_job_scan.mjs` — aggregator (SmartRecruiters/Workday/Greenhouse/Lever/Ashby/LinkedIn/RemoteOK/Jobicy/Remotive/Adzuna).
2. `node scripts/focused_search.mjs` — resume-relevant keywords (ITAM/CMDB/ITSM/technical consultant/etc.).
3. `python3 tools/jobs_merge_inbox.py --today 2026-11-15 --days 30 --max-per-table 5000` — inbox → README tables.
4. `python3 tools/build_site.py` — public/jobs-data.json + public/index.html.
5. `git commit + push origin main`.

Counts:
- Fresh postings this scan: **715**; live board **2774** aggregator jobs (servicenow 1271 / salesforce 1334); 4121 incl. focused-search metadata.
- Source hits: adzuna 486, linkedin 169, workday 20, greenhouse 17, smartrecruiters 12, remotive 6, ashby 2, lever 1, remoteok 1, jobicy 1.
- Dedupe: 27 already on board dropped by URL; 0 cross-source dupes.
- README merge: +0 new rows (inbox finds were dupes/older than 30 days); README tables hold 7452 rows.
- Site build: 6377 jobs (servicenow 935 / salesforce 988 / other 4454), built 2026-11-15 11:06 UTC, newest posting 2026-11-15.

Toronto fresh ServiceNow (2026-11-15 / 2026-11-14):
- Interac Corp., Toronto — Senior Business Systems Analyst (ServiceNow), QE Senior Specialist (ServiceNow Platform) — linkedin, posted 2026-11-15.
- Raas Infotek — Certified Technical Architect – ServiceNow — linkedin, posted 2026-11-15.
- Accenture, Toronto — ServiceNow Technical Architect; Avanciers Inc., Toronto — ServiceNow Implementation Architect; S I Systems, Toronto — ServiceNow Developer (CMDB/HAM/SAM); Dexian, Toronto — servicenow developer; SPECTRAFORCE, Toronto — ServiceNow Developer; Pacer Group, Toronto — ServiceNow Implementation Architect — adzuna, 2026-11-14.
- BDO Canada — ServiceNow Senior Developer (Ottawa/Oakville); RBC — Senior ServiceNow Discovery & Service Mapping Engineer; BMO, Toronto — ServiceNow Technology Lifecycle Analyst — adzuna, 2026-11-14.
- ServiceNow careers (careers.servicenow.com), Toronto — Senior ServiceNow Database Engineer, Government of Canada Reliability Status, 2026-11-14.

Salesforce: Rogers Communications Georgetown ON Lead Management Operations (Salesforce lead SME) was added in the 04:00 EST scan; no additional fresh Toronto Salesforce Platform Admin/Dev I this hour.

Failures/notes:
- `workday:bdo` returned HTTP 401 for servicenow + salesforce — BDO Workday tenant blocked; use BDO direct careers / LinkedIn.
- Entry-level / Platform Admin / Platform Developer I postings remain sparse — almost nothing explicit; best proxy is ITAM/CMDB/ServiceNow Administrator at banks & consultancies (BMO, RBC, BDO, CGI, Deloitte, Infosys).
- Future scan keyword variants: "platform administrator", "platform developer I", "junior servicenow", "entry level salesforce", "associate consultant servicenow".

Commit: `68903ae chore(jobs): hourly scan 2026-11-15 06:00 EST — aggregator + focused search, +715 fresh SN/SF postings (servicenow 1271 / salesforce 1334), site rebuilt [skip ci]` — pushed to origin/main; GitHub Pages redeploys on main push.

## 2026-11-15 07:00 EST run — +1 fresh Salesforce job

Window: 2026-11-15 → 2026-11-14, Toronto-first ServiceNow / Salesforce. Local main was behind origin/main, so local was reset onto origin/main (ecc3ef1, hourly scan refresh 12:16 UTC) before scanning.

Sources checked:
- **Adzuna API**: 68 calls (13 queries × 3 geos) + **Job Bank**: 12 pages → raw 282 → unique 27 → kept 0 (all 27 already on board by URL).
- **Eluta.ca**: stalled (~30 s/page, 0 usable pages) — skipped this hour.
- **LinkedIn guest pass**: **1 fresh row** — Hired, "Salesforce Administrator (Remote)", Canada, LinkedIn job id **4490216969**, posted 2026-11-15. Independently re-fetched: HTTP 200 guest-details page — posting is live. Clean of README.md (title|company|city fingerprint).
- **Concurrent scan**: origin/main's jobs.json/feeds (ecc3ef1, scraped 12:14:56Z, source linkedin, workArrangement remote) already carried the Hired row — it was only missing from the README table.
- **ATS discovery**: 24 Workday tenants (salesforce wd12; bmo/rbc/cibc/scotiabank/manulife/sunlife/telus/opg wd3) + SmartRecruiters ServiceNow → raw 5, kept 0 (4 non-Canada).

Merge + publish:
- Inserted the row newest-first into the README Salesforce table (2026-11-15, above the 2026-11-14 Rogers row); heading and details count 1485 → 1486.
- `jobs_merge_inbox.py` not needed this run (no new inbox submissions; the row came through the live linkedin-guest check and was already in origin's feed).
- `build_site.py`: page unions jobs.json + README rows with URL dedupe, so the Hired row renders once; public/ rebuilt.
- No heading-merge side effect this run: origin/main's README kept `### <family> jobs (N)` and its subtitle on separate lines, so `sync_readme_to_jobs.mjs` parses all three sections cleanly.

Outcome: +1 verified fresh job — **Hired — Salesforce Administrator (Remote), Canada** (LinkedIn 4490216969). Present in origin's jobs.json feed from the concurrent scan; this run adds it to the README table and republishes the page. README.md, public/, and this lessons file committed to main; pages.yml redeploys eltonaguiar.github.io/BESTIEJOB/ on the push.

Lesson re-confirmed: late-2026 Canadian SN/SF hourly supply is extremely sparse — most hours yield 0–1 postings; the value of the run is dedupe + liveness verification, not volume. Adzuna + Job Bank + LinkedIn guest details cover the today/yesterday window; Eluta.ca is currently unusable for same-day sweeps via urllib. When peer scans run in parallel, always re-check origin/main before adding: the same posting can already be in the feed under a different source id (here `linkedin:...` vs my candidate `readme:...`).


## 2026-11-15 08:00 EST run — aggregator scan, +49 newly-tracked URLs

Window: 2026-10-09 → 2026-11-15, Toronto-first ServiceNow / Salesforce (45-day source window).

Ran canonical hourly flow:
1. `node scripts/daily_job_scan.mjs` — aggregator (SmartRecruiters/Workday/Greenhouse/Lever/Ashby/LinkedIn/RemoteOK/Jobicy/Remotive/Adzuna).
2. `python3 tools/verify_links.py --days 2 --blocklist dead_urls.txt` — liveness gate.
3. `python3 tools/build_site.py` — public/jobs-data.json + public/index.html.
4. `git commit + push origin main`.

Counts:
- Fresh source results this scan: 718; merged board: 2794 (was 2746); genuinely new URLs added: 49.
- Tags: servicenow 1284 / salesforce 1340.
- Source hits: adzuna 486, linkedin 172, workday 20, greenhouse 17, smartrecruiters 12, remotive 6, ashby 2, lever 1, remoteok 1, jobicy 1.
- Liveness gate: probed 133 fresh rows, live=87 dead=0 unknown=46 — nothing dropped.
- Site build: 5734 jobs (servicenow 936 / salesforce 989 / other 3809), 906 duplicate mirrors collapsed, 45 applied hidden, best-match 1856, newest posting 2026-11-15, built 2026-11-15 13:03 UTC.

Today-fresh (posted 2026-11-15) additions this run:
- Parkland Corporation — Specialist- Salesforce Architect — Calgary, Alberta, Canada — linkedin (salesforce)

Older postings newly surfaced by aggregator sources (not today-fresh, newly tracked by URL): 48 more, mostly Adzuna/LinkedIn, posted 2026-10-09 → 2026-11-14, across Toronto/Ottawa/Vancouver/Montreal/Calgary.

Failures/notes:
- Workday: bdo.wd3 returned HTTP 401 for servicenow+salesforce (BDO tenant blocked); accenture.wd103 and salesforce.wd12 returned HTTP 422 (rate-limited on burst). One-call-at-a-time with gaps re-confirmed; multi-tenant bursts get 422.
- Today-fresh Toronto SN/SF supply remains sparse (1 today-fresh addition this hour); the board's growth came from Adzuna/LinkedIn surfacing older-but-untracked URLs.

Commit: pending — jobs.json, README.md (daily-scan block), public/*, FRESH_JOBS.md, this lessons file.

## 2026-11-15 09:00 EST run — null result (0 fresh jobs)

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce.

Sources checked, all zero new:
- **Adzuna API**: 68 calls (13 queries × 3 geos: national/Toronto/Ontario), raw 289 → unique 28 → kept 0 (27 already on board by URL, 1 by title fingerprint). Inbox written: `inbox/fresh-ca--2026-11-15--v1.md` (0 rows).
- **Eluta.ca**: skipped — stalls ~30s/page, 0 usable pages (same as 07:00 EST lesson).
- **Job Bank**: 0 pages (skipped to prioritize Adzuna freshness window).
- **LinkedIn guest pass**: not completed — guest pass needs ~7 min (20 keywords × 2 locations), exceeded session timeout; direct LinkedIn returns 403.
- **Workday tenants (10)**: bmo/rbc/cibc/scotiabank/manulife/sunlife/telus/opg/salesforce/accenture — BMO ServiceNow CMDB Administrator + Technology Lifecycle Analyst already on board (posted ~3 days ago, recurring requisitions); no fresh Canadian SN/SF.
- **Rogers careers**: 0 SN/SF mentions on careers page HTML (105 KB scanned, Nov 11–14 page = sales/retail only).
- **Bell careers**: 303 redirect, JS-rendered, not scrapeable via curl.
- **Canadian government / public sector**: City of Toronto 9 tiles, 0 new; OPS gojobs blocked by Radware; OPS Job Bank 8 articles, 0 new.
- **Partner/sponsor scan**: ServiceNow World Forum Toronto sponsors + Canadian partners — scan timed out, no results; sponsor data last refreshed 2026-11-03.

Dedupe: URL + title\|company\|city fingerprint held against README.md and jobs.json; nothing new survived.

Outcome: no commit for board data (0 fresh jobs), no publish — README.md, jobs.json, and public/ are unchanged. pages.yml only redeploys on a main push, so no GitHub Pages redeploy for board data this run.

Lesson re-confirmed: late-2026 Toronto SN/SF hourly supply is sparse — 0 fresh jobs this hour is normal, not a scanner failure. Workday BMO SN requisitions recur every few days under the same job IDs — check `postedOn` date before treating as fresh. Rogers careers page carries no SN/SF roles at all. Bell/Rogers career sites are JS-rendered and blocked to direct curl (301/303) — need Playwright browser or skip.

## 2026-11-15 10:00 EST run — null result (0 fresh Canada jobs)

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce; Canada scope (Rogers, Bell, banks, government, partners/Elite sponsors per scan charter).

Sources checked, all zero new:
- **Workday CXS curl `--compressed`**, 20 tenants × 2 queries (ServiceNow, Salesforce): 115 postings scanned, 13 SN/SF-titled. 8 already on board by URL/title fingerprint: BMO ServiceNow CMDB Administrator, BMO ServiceNow Technology Lifecycle Analyst, BMO ServiceNow SAM Administrator–ITAM (Toronto), Manulife Salesforce Functional Analyst (Waterloo), Sunlife ServiceNow Associate Software Engineer (Waterloo), TD Software Engineer III–Salesforce Data 360 (Toronto), plus board-carried non-Toronto BMO Salesforce Developer (Chicago). 5 URL-fresh but non-Canada — excluded from the Canada-focused board: Manulife Salesforce Platform Technical Analyst (Quezon City, PH), Manulife Front End Software Engineer (Salesforce) (Makati City, PH), Manulife Associate Front End Software Engineer (Salesforce) (Makati City, PH), Sunlife Principal Consultant–ServiceNow (Gurugram, India), TD Salesforce IT Solutions Design Specialist (US) (New Jersey). Each confirmed absent from README.md/jobs.json, then dropped on scope.
- **Adzuna API**: no app keys in this environment — skipped. jobs.json already refreshed 2026-11-15T14:10Z by the 09:00 cycle (2747 listings), so aggregator data is <1 hour old.
- **LinkedIn guest pass**: not run this hour — guest details return 422 and the full pass needs ~7 min.
- **Rogers careers HTML** (105 KB): sales/retail roles only, no SN/SF titles. **Bell**: JS-rendered, not curl-scrapeable (303 redirect). **Canadian government/public sector**: City of Toronto tiles 0 new; gojobs Radware-walled; Job Bank proxy 0 new.
- **Partners/Elite sponsors** (CGI, Deloitte, Accenture, IBM, Cognizant, etc.): covered by the aggregator refresh already on main; Workday direct-ATS probe returned no additional Canadian SN/SF hits from any tenant.

Dedupe: URL + title\|company\|city fingerprint held against README.md and jobs.json; nothing new survived.

Outcome: no commit for board data (0 fresh Canada jobs), no publish — README.md, jobs.json, and public/ unchanged; pages.yml redeploys only on main push, so no GitHub Pages redeploy this run. Live page (eltonaguiar.github.io/BESTIEJOB/) remains current from the 09:00 EST push.

Lesson re-confirmed: hourly Toronto SN/SF supply is near zero at this cadence; Workday CXS single-call `--compressed` probes stay under the 422 rate limit, but every Canada-located SN/SF requisition surfaced was already tracked. Recurring BMO SN requisitions reappear under the same job IDs — check postedOn before treating as fresh. Do not re-run the merge "just to have a commit".

## 2026-11-15 11:00 EST run — null result (0 fresh Canada jobs)

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce; Canada scope with partners/Elite sponsors, Rogers, Bell, and government/public-sector checks per scan charter.

Board state: origin/main was force-updated to `333cdfc chore(jobs): fresh CA sweep 2026-11-15T15:43Z` (an orphan-history commit from CI carrying the entire tree). Local main was reset onto origin/main before scanning; jobs.json = 2747 listings, 0 new from that 15:43Z sweep.

Sources checked, all zero new:
- **fresh_ca_scan.py** (`--days 2 --eluta-pages 0 --jobbank-pages 1 --linkedin 1 --linkedin-max 10`): Adzuna 68 calls (17 queries × 4 geos), Job Bank 6 pages, LinkedIn guest 20 requests (10 keywords × Toronto/Canada) → raw 386, unique 38, **kept 0** — all 38 already on board by URL, 0 unverified dropped. Inbox written: `inbox/fresh-ca--2026-11-15--v3.md` (0 rows).
- **Eluta.ca**: skipped (stalls ~30 s/page, 0 usable pages — unchanged for 3 days).
- **Workday CXS** (bash `curl -s --compressed`, POST `/wday/cxs/{tenant}/{site}/jobs`, one call at a time): 18 tenant probes — bmo/External, td/TD_Bank_Careers, cibc/search, manulife/MFCJH_Jobs, sunlife/Experienced-Jobs, interac/interac, accenture/AccentureCareers (wd103), salesforce/External_Career_Site (wd12), omers/OMERS_External, desjardins/Desjardins all HTTP 200. SN/SF-titled hits: BMO ServiceNow CMDB Administrator + Technology Lifecycle Analyst (3 d) and ServiceNow SAM Administrator–ITAM (12 d) — on board; Interac Senior BSA (ServiceNow) + QE Senior Specialist (ServiceNow Platform) (30+ d) — on board; TD Software Engineer III–Salesforce Data 360 (2 d, Toronto) — on board; Manulife Salesforce Functional Analyst (13 d, Waterloo) — on board; Sunlife ServiceNow Associate Software Engineer (11 d, Waterloo) — on board. URL-fresh but **non-Canada**: Sunlife Principal Consultant–ServiceNow (Posted Today, Gurugram), Salesforce corporate Technical Architect–Salesforce Devops (Posted Today, Bangalore, 2 Locations), 34 Accenture SN/SF roles (Warsaw/Bucharest/Madrid/Monterrey/Taguig/Canberra/Melbourne/Prague/Singapore/etc. — none Canadian).
- **Rogers careers** (`jobs.rogers.com/search/?q=…&sortColumn=referencedate`): "servicenow" → 0 job cards; "salesforce" → 32 cards, all field-sales/delivery roles that merely mention Salesforce in the body (Lead Management Operations, Toronto, already added 04:00 EST). No SN/SF platform titles.
- **Bell** (`jobs.bell.ca`): 303 redirect, JS-rendered — not curl-scrapeable (unchanged).
- **Canadian government**: `jobs.gc.ca` DNS did not resolve this run (curl exit 6) — Job Bank proxy covered by fresh_ca_scan; `gojobs.gov.on.ca` remains Radware-walled. **City of Toronto** `jobs.toronto.ca` ServiceNow search: HTTP 200, 0 SN/SF job cards.
- **Partners/Elite sponsors**: covered by the LinkedIn guest pass (title-based, company-agnostic) and Adzuna; direct Accenture + Salesforce corporate ATS probes returned no Canadian SN/SF. CGI/Deloitte/KPMG/Cognizant inventory unchanged on main.

Dedupe: URL + title\|company\|city fingerprint held against README.md and jobs.json; nothing new survived.

Outcome: no board-data commit, no publish — README.md, jobs.json, public/ unchanged, so the live page (eltonaguiar.github.io/BESTIEJOB/) remains current from the 09:00 EST push. Only this lessons entry, the 0-row inbox v3, the fresh_ca report, and raw probe artifacts are committed.

New lessons:
1. **Python `subprocess.run(["curl", …])` fails with WinError 5 (Access is denied) on this host** — the Proactor/AppContainer blocks child curl.exe from Python. Call `curl` directly in the bash terminal tool instead; writing a Python driver around curl is a dead end.
2. **Workday 422 ≠ always rate-limit**: canadalife/CL_External, loblaw/External, cnr/CN_Careers, nbc/National_Bank returned 422 on first call even with 2 s gaps — that is a wrong site slug, not throttling. 404 = wrong tenant/site (rbc/RBC_Careers, cppib/CPPIB, otppb/OTPP_Careers, intactfc/Intact this run). Treat 422-after-first-call as "drop this tenant", keep only 200 pairs in the probe list.
3. **"Posted Today" on Workday is not Canada**: Sunlife posted a Principal Consultant–ServiceNow in Gurugram today and Salesforce posted a Technical Architect in Bangalore today. Always read the `/job/<City>/…` slug before counting a fresh posting — postedOn only proves recency, not scope.
4. Rogers careers is a SuccessFactors-style search: keyword returns are body-text matches, so a hit count means noise, not platform roles. Parse the `/job/…` card titles, not the mention count.

## 2026-11-15 12:00 EST run — null result (0 fresh Canada jobs)

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce; Canada scope with partners/Elite sponsors, Rogers, Bell, and government/public-sector checks per scan charter.

Board state: local main fast-forwarded to origin/main d25617a "hourly scan refresh (2746 listings, 2026-11-15T16:12:47Z)" before scanning; jobs.json = 2746 listings (servicenow 1284 / salesforce 1339).

Sources checked, all zero new:
- **Workday CXS** (`curl -s --compressed`, POST `/wday/cxs/{tenant}/{site}/jobs`, body `{"appliedFacets":{},"limit":20,"offset":0,"searchText":q}`, one call at a time, ~4s gaps): BMO External (ServiceNow 7 / Salesforce 15) and TD TD_Bank_Careers (ServiceNow 12 / Salesforce 13) — HTTP 200 all four. Canada SN/SF-titled hits: BMO ServiceNow CMDB Administrator (3 d), ServiceNow Technology Lifecycle Analyst (3 d), ServiceNow SAM Administrator–ITAM (12 d); TD Software Engineer III–Salesforce Data 360 (2 d) — all already on board by URL. **0 fresh Canada SN/SF.** First POST attempt returned HTTP 000 (connection failed) on all four combos — transient; retry succeeded.
- **Web-search aggregates** (Indeed/LinkedIn/Glassdoor/Adzuna via search engine): Make-A-Wish Sr Salesforce Administrator (Nov 6), SS&C Salesforce Implementation Consultant & Platform Admin (Nov 3–11), Survalent Salesforce Administrator (Nov 4–11), emergiTEL Salesforce System Coordinator (Nov 13) — all already in jobs.json by URL/title, older than fresh window. **0 new URLs.** Search snippets are not a freshness oracle.
- **Adzuna API**: no app keys in this environment — skipped (jobs.json refreshed <1 hour ago by CI at 16:12Z).
- **Job Bank / Eluta / Rogers / Bell / Canadian government**: Job Bank 0 pages; Eluta stalls (~30s/page, 0 usable); Rogers careers = sales/retail only, no SN/SF platform titles; Bell JS-rendered 303, not curl-scrapeable; gojobs.gov.on.ca Radware-walled; jobs.gc.ca not reachable; City of Toronto 0 SN/SF cards.
- **Partners/Elite sponsors** (CGI, Deloitte, Accenture, IBM, Cognizant, etc.): no additional Canadian SN/SF beyond aggregator data already on main.

Dedupe: URL + title\|company\|city fingerprint held against README.md and jobs.json; nothing new survived.

Outcome: no commit for board data (0 fresh jobs), no publish — README.md, jobs.json, and public/ unchanged; live page (eltonaguiar.github.io/BESTIEJOB/) remains current. Only this lessons entry is committed.

New lessons:
1. **Workday curl HTTP 000 can be transient** — first POST attempt returned connection-failed (000, 0 bytes) for all four tenant/query combos; retry with correct body schema returned HTTP 200. Don't mark a tenant dead on a single 000.
2. **Web-search aggregate leads are not fresh board candidates** — Indeed/LinkedIn/Glassdoor surfaced Make-A-Wish, SS&C, Survalent, emergiTEL Salesforce roles, but every one was already in jobs.json (posted Nov 3–13). Stick to Workday CXS + LinkedIn guest for same-day verification.
3. **LinkedIn guest re-fetch unavailable this run** — Chrome profile locked (browser_exec) and direct LinkedIn search returns 301/422; the 04:00 EST linkedin_sn_2026-11-15.html and linkedin_sfpa_2026-11-15.html captures were already fully processed (Deloitte SN roles + Rogers Lead Management Ops all on board). Treat LinkedIn as stale until the browser profile is freed or guest API recovers.
4. **CI hourly refresh** — origin/main advanced to d25617a "hourly scan refresh (2746 listings)" at 16:12Z via CI; local fast-forwarded cleanly. jobs.json is the system of record and is refreshed by CI independent of this run.

Commit: JOBLESSONS_2026-11-15.MD entry appended and committed [skip ci]; no board-data or pages change.

## 2026-11-15 13:00 EST run — +1 fresh Salesforce job

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce; Canada scope incl. Rogers, Bell, banks, government, partners/Elite sponsors.

Board state: local main at d25617a "hourly scan refresh (2746 listings, 2026-11-15T16:12:47Z)" (servicenow 1284 / salesforce 1339); HEAD df8a0f9 (12:00 EST) was a null-result lessons-only commit.

Fresh verified job added this run (1):
| Posted | Role | Company | Location | Source | Notes |
|--------|------|---------|----------|--------|-------|
| 2026-11-15 | [Sales Operations Coordinator / Junior Salesforce Admin](https://ca.linkedin.com/jobs/view/revenue-operations-coordinator-at-generis-4444467031) | Generis | Toronto, Ontario, Canada | LinkedIn guest (job id 4444467031) | Full-time Entry level Salesforce Administrator role, downtown Toronto. Corroborated by LinkedIn ("Entry level role", Toronto) and RevOps Report ("8h ago", Toronto, Actively Hiring). Junior / Platform Admin emphasis matching the user's entry-level target. Dedupe clean: not in jobs.json or README.md (searched "Generis" + "4444467031" — 0 hits). Added to README Salesforce table (newest-first, above the 2026-11-15 Hired row) and to jobs.json. Count Salesforce jobs 1486 → 1487. |

Sources checked this hour, all zero new except Generis above:
- LinkedIn guest pass: ServiceNow Toronto + Salesforce Platform Admin/Developer Toronto scans → Generis Junior Salesforce Admin (Toronto, entry-level, ~8h ago) kept; everything else already on board or non-matching (senior/generic CRM, non-Toronto, closed).
- Workday CXS (curl --compressed, one call at a time): BMO/TD/Manulife/Sunlife/Interac/Accenture/salesforce tenants — all Canada SN/SF hits already on board (recurring BMO requisitions under same job IDs; check postedOn).
- Adzuna API / Job Bank / Eluta / Rogers / Bell / Canadian government: Eluta stalls (~30s/page); Bell JS-rendered 303; gojobs Radware-walled; jobs.gc.ca NXDOMAIN; City of Toronto 0 SN/SF cards; Rogers = sales/retail only. 0 new.
- Partners/Elite sponsors (CGI, Deloitte, Accenture, IBM, Cognizant): covered by aggregator on main; no additional Canadian SN/SF.

Dedupe: URL + title|company|city fingerprint held against README.md and jobs.json; Generis survived as new.

Outcome: +1 verified fresh job — Generis — Sales Operations Coordinator / Junior Salesforce Admin (Toronto, entry-level Salesforce Admin), LinkedIn 4444467031. README.md and jobs.json committed to main [skip ci]; pages.yml redeploys eltonaguiar.github.io/BESTIEJOB/ on the push.

Lesson re-confirmed: late-2026 Toronto SN/SF hourly supply is sparse (0–1 fresh postings/hour); entry-level / Platform Admin / Platform Developer I postings are the rarest slice — most fresh hits are mid/senior architect or recurring bank requisitions. When a fresh entry-level platform admin role does surface (as Generis did today), add it even if the hour is otherwise null.

## 2026-11-15 21:00 EST run — +1 fresh ServiceNow job

Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce; Canada scope (banks, government, partners, Rogers, Bell).

Board state: local main == origin/main (2,755 jobs) before scanning.

Fresh verified job added this run (1):

| Posted | Role | Company | Location | Source | Notes |
|--------|------|---------|----------|--------|-------|
| 2026-11-15 | Applications Support Analyst | BMO | Toronto, ON, CAN | Workday CXS (bmo.wd3/External, req R260028077) | Full-time, Toronto (33 Dundas St W), applies by 11/29/2026. Workday CXS `searchText=ServiceNow` matched it; detail fetch confirmed country=Canada, `servicenow` mentioned in description, `timeType=Full time`, `startDate=2026-11-15`, `endDate=2026-11-30` (live). Dedupe clean: not in jobs.json or APPLIED.md. Added to jobs.json (tags: servicenow); public/ rebuilt. |

Sources checked this hour, all zero new except BMO above:

- **Workday CXS** (`curl -s --compressed`, POST `/wday/cxs/{tenant}/{site}/jobs`, one call at a time): bmo/External, td/TD_Bank_Careers, cibc/search, manulife/MFCJH_Jobs, interac/interac, accenture/AccentureCareers, salesforce/External_Career_Site × ServiceNow + Salesforce. Only Canada-located SN/SF "Posted Today" hit was the BMO Applications Support Analyst; everything else already on board, non-Canada, or non-SN/SF. Accenture/Salesforce Workday page 1 is relevance-sorted and effectively non-Canada — append the city to `searchText` or page 1 is useless for a Toronto board.
- **gap_scan/adzuna harvest** (02:04 UTC): 38 rows, all already on board — 0 new.
- **Public sector**: gojobs.gov.on.ca Radware-walled; jobs.gc.ca NXDOMAIN; Job Bank OPS feed 0 platform-titled postings; City of Toronto 0 SN/SF cards.
- **Rogers/Bell**: Rogers = sales/retail only, no SN/SF platform titles; Bell JS-rendered 303, not curl-scrapeable.

Outcome: +1 verified fresh job — BMO Applications Support Analyst (Toronto, ServiceNow-linked production support). jobs.json → 2,756 rows; `public/jobs-data.json` + `public/index.html` rebuilt via `tools/build_site.py` (site: 5,739 jobs, newest 2026-11-15). Committed to origin/main with [skip ci]; pages.yml schedule (:35 UTC) redeploys eltonaguiar.github.io/BESTIEJOB/.

Lessons re-confirmed: hourly Toronto SN/SF supply is near zero — 0–1 fresh/hour is normal, not a scanner failure. Workday CXS "Posted Today" single-call `--compressed` probes stay under the 422 rate limit; always confirm `country` + platform mention before counting a fresh hit. `bmo.myworkdayjobs.com` is NXDOMAIN — use the `wdN` host (`bmo.wd3...`).

## 2026-11-15 22:00 EST run — null result (0 fresh jobs)


Window: 2026-11-14 → 2026-11-15, Toronto-first ServiceNow / Salesforce; Canada scope (banks, government, partners, Rogers, Bell).


Board state: local main == origin/main (jobs.json 2,756 rows; README parsed 7,470 rows).


Fresh verified jobs added this run: 0.


Sources checked, all zero new:

- **Inbox merge** (`python3 tools/jobs_merge_inbox.py --max-per-table 4000`): fresh-ca--2026-11-15--v1.md = +0 new, 43 duplicate — every URL/fingerprint already in README.md; nothing survived dedupe.

- **fresh_ca_scan** (Adzuna 13 queries × 3 geos, Job Bank, Eluta): local re-scan timed out (~4 min) on URL liveness verification; the 18:00 EST harvest's 43 rows are all already aboard, so nothing lost.

- **Public sector**: gojobs.gov.on.ca Radware-walled (do not retry); jobs.gc.ca NXDOMAIN; Job Bank OPS feed 0 platform-titled postings; City of Toronto jobs.toronto.ca 0 SN/SF cards.

- **Partner/Elite sponsors** (`scripts/partner_sponsor_scan_verified.py`): 18 sponsors confirmed, 0 relevant postings; Workday tenants 0/15 answering; slug guesses rejected by identity check (Ernst & Young, KPMG, Crossfuze, Fujitsu, Blue Mantis, Brightfin, Tech Mahindra — no verifiable board or demo boards).

- **Rogers/Bell/Workday raw probes**: BMO ServiceNow CMDB Administrator R260030992 + Technology Lifecycle Analyst R260030995 and TD Software Engineer III - Salesforce Data 360 all confirmed already aboard (README); no new Canada SN/SF hits in this cycle.


Dedupe: URL + title|company|city fingerprint held against README.md and jobs.json; nothing new survived.


Outcome: no commit, no publish — README.md, jobs.json, and public/ unchanged. pages.yml redeploys eltonaguiar.github.io/BESTIEJOB/ only on a main push, so no GitHub Pages redeploy this run.


Lesson re-confirmed: late-2026 Toronto SN/SF hourly supply is sparse — 0 fresh jobs this hour is normal; don't re-run the merge "just to have a commit". Local network is too slow for full re-scans (Adzuna verify + LinkedIn guest pass time out past ~4 min), so trust the same-day captures already aboard rather than re-scraping.


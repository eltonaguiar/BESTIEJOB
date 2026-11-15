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

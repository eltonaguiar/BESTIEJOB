# JOBLESSONS_2026-11-12 — hourly BESTIEJOB scan (2026-11-12 00:00 EST / 05:00 UTC)

## Scope
Toronto-first ServiceNow / Salesforce / IT-platform job board (`eltonaguiar/bestiejob`, main). Hourly cron scan: find fresh postings dated ~today/yesterday, dedupe against the board, merge verified rows into README.md's three tables, rebuild GitHub Pages (`public/`), push to main. Pages redeploy on push via `.github/workflows/pages.yml`.

## Result this run
**0 verified fresh rows added to the live tables.** The scan ran and the site was rebuilt, but no new row passed all three gates (fresh + direct posting URL + not already on the board).

| Metric | Value |
|---|---|
| Scan start | 2026-11-12T05:02:17Z |
| Fresh postings surfaced by scan | 783 across 10 public sources |
| jobs.json total after sync | 2,888 |
| Live page indexed | 2,442 jobs (SN 876 / SF 915 / Other 651) |
| Duplicate mirrors collapsed | 314 |
| Applied roles hidden | 35 |
| Board tables | ServiceNow 595 / Salesforce 612 / Other 583 — **unchanged** |
| Dead links dropped | 1 (appended to dead_urls.txt) |

## Source breakdown (this scan)
- SmartRecruiters (ServiceNow): 13 · Workday (BMO/TD/Altus/BDP/CAAT/etc.): 14 · LinkedIn guest: 307 · Adzuna: 422 · Greenhouse: 16 · Lever: 1 · Ashby: 2 · RemoteOK/Jobicy/Remotive: 8
- 4 Adzuna queries returned HTTP 503/429 (rate-limited): `servicenow administrator/Toronto`, `servicenow lead/Toronto`, `salesforce remote/Canada`, `it asset management/Toronto` — re-try next hour, those keywords are not lost (other Adzuna queries cover them).
- LinkedIn guest: 307 cards; endpoint 429s after ~4 rapid queries — the script already paces at 1.8s/query with 2 workers; do not increase concurrency.

## Dedupe outcome
- Every URL from this scan's fresh set was already on the board (Adzuna/LinkedIn/Workday re-surface the same requisitions hourly) or fell outside the 30-day window → skipped, 0 added.
- Verify-links gate probed 154 rows posted within 2 days: 30 live, **1 dead**, 123 unknown (bot-walled/403). Dropped: ivari Canada "Salesforce Manager, Sales & Marketing Clouds" (LinkedIn 4093448492, now 404) → dead_urls.txt.
- `scripts/sync_readme_to_jobs.mjs` added 367 README-only rows into jobs.json (feed now a superset of README); `tools/build_site.py` rebuilt `public/jobs-data.json` + `public/index.html` from README tables + jobs.json.

## Target-company checks (Rogers / Bell / partners / GC) — nothing fresh addable
- **Rogers (jobs.rogers.com):** "Technical Specialist, Markham" (req 343759) mentions ServiceNow/Salesforce only as comparable preferred tools — not an SN/SF role, skipped. Rogers "Lead Management Operations" req 343961 was already added to the board in the previous run.
- **Bell (jobs.bell.ca):** ServiceNow Developer / Integrator (job id 431695, Ottawa/Toronto/Montreal/Quebec City) looked fresh on Indeed (~6h ago) but the canonical page returns **HTTP 410 "the job ... has been filled"** — verified closed, skipped. Earlier Bell SN roles (432824 System Administrator, 432829 Senior Technical Advisor) are already on the board.
- **Canadian government / Job Bank:** hits were Aug–Sept 2026 (e.g. Upstaff ServiceNow CSA/CAD consultant for Ontario, posted Sept 29) — outside the 30-day window. Nothing fresh.
- **ServiceNow Careers Ontario page:** 16 jobs listed; dated Toronto hits are sales/security/SRE roles (Nov 5–9), no fresh SN dev/admin/postings for Nov 11–12.
- **Salesforce careers Canada:** no fresh Toronto Platform Admin / Platform Developer I postings surfaced.
- **Partner career-site gap scan:** 7 sites (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) — 0 dateable postings; Lane Four's 2 Salesforce anchors publish no date → logged to `inbox/gap-scan--2026-11-12--v1.md` as undated (merger deliberately skips undated rows).

## Adzuna note
Adzuna detail pages return HTTP 405 to extractors — trust the dated sweep files (`inbox/fresh-ca--2026-11-11--v*.md`) for title/company/location/date, then diff the URL set against the board before adding. Adzuna emits one URL per city for the same requisition — dedupe by URL first, then company+title+date for near-dupes (vendor twins like Pacer/Nityo advertising the same req are distinct rows and both stay).

## Files changed
`README.md` (daily-scan block refreshed), `jobs.json` (+367 feed rows from sync), `dead_urls.txt` (+1), `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`, `public/jobs-data.json`, `public/index.html`, `JOBLESSONS_2026-11-12.MD`

## Left as-is (untracked working queue, per repo convention)
`inbox/*` (incl. new `inbox/gap-scan--2026-11-12--v1.md`), `raw/*`, `docs/JOB_GAP_STRATEGY.md`, `README.BAK_*` backups.

## Hourly scan — 2026-11-12 01:00 EST (06:00 UTC) — NULL RUN (second pass)

| Metric | Value |
|---|---|
| Run time | 2026-11-12 01:00 EST (06:00 UTC) |
| Baseline (README.md tables + jobs.json on main) | 1,793 live postings · ServiceNow 596 · Salesforce 613 · Other 584 · window 2026-10-12 → 2026-11-11 · HEAD c988068 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required) |

### Candidates reviewed (01:00 pass)

- **Cognizant — ServiceNow Software Asset Management Developer** (req 00070949051, Toronto ON-199 Bay Street, published Nov 11 2026, hybrid, $92k–$105k CAD, applies till 11/30/2026) — verified live on careers.cognizant.com. **NOT added**: duplicate — same role already on the board via LinkedIn `ca.linkedin.com/jobs/view/servicenow-software-asset-management-developer-at-cognizant-4489032943` dated 2026-11-11. Same role arrives via employer ATS and LinkedIn under different URLs; dedupe by role + company + location, not URL alone.
- **ServiceNow Careers Ontario** (16 Ontario jobs) — latest Toronto listings are Senior CRM Account Executive (Nov 09, sales), Sales Director - CRM Sales (Nov 09, sales), and Staff/Senior Staff Security Engineer roles (already on board from Nov 05–06). No fresh technical ServiceNow Toronto posting for Nov 11–12.
- **Bell (jobs.bell.ca)** — every ServiceNow hit returned "has been filled": System Administrator 432824, Senior Manager Platform Delivery 432892, Developer/Integrator 431695, Senior Technical Advisor 432829, Business Analyst CoE BECACA429615, Senior Architect SPM BECACA431688. Filled roles never enter the board; mark dead in the source scan.
- **Rogers (jobs.rogers.com)** — Sr Business Systems Analyst ServiceNow ITSM (Req 317411, Brampton/Toronto, no posting date → freshness unverifiable, skipped); Lead Management Operations Salesforce (Req 343961, posted ~Oct 28, outside window, already flagged); Technical Specialist Markham (Cisco/Fortinet networking; SN/SF only as "comparable" tools, not a platform role). Nothing fresh/addable.
- **jobs.gc.ca** — zero ServiceNow/Salesforce Toronto results; GC platform work comes via prime vendors on their own ATS.
- **Indeed.ca "New" tags / LinkedIn** — Moneris Principal Salesforce Developer, CGI Senior Salesforce Developer, Survalent Salesforce Admin, LTM Salesforce DevOps, CoreKloud FSC Developer, Altus Group Platform Developer, Deloitte Senior Consultant Salesforce Platform — all aggregator/search-result listings without direct date-verifiable URLs; LinkedIn behind HTTP 422 login wall. Each either already on the board or unverifiable. Never add without a verifiable direct posting URL + date.

### Patterns / lessons (01:00 pass)

1. **Second consecutive null run.** The 00:00 EST refresh and the 01:00 EST web scan both found 0 new table rows — zero fresh merges on most hourly runs is the norm, not a failure.
2. **Dedupe before trusting "fresh."** The Cognizant SAM Developer looked fresh (Nov 11) but was already on the board via a different URL (LinkedIn 4489032943). Normalize by role + company + location.
3. **Bell filled-roles gate holds.** All six Bell ServiceNow reqs checked are filled; don't re-surface filled roles each hour.
4. **Indeed "New" + LinkedIn dates are not independently verifiable.** Capture the direct posting URL and date at search time, or skip.

## Hourly scan — 2026-11-12 05:00 EST (10:00 UTC) — NULL RUN (third pass)

| Metric | Value |
|---|---|
| Run time | 2026-11-12 05:00 EST (10:00 UTC) |
| Baseline (README.md tables + jobs.json on main) | 2,859 live postings · ServiceNow 1,048 · Salesforce 1,116 · Other 695 · window 2026-10-13 → 2026-11-12 · HEAD 57701f9 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required) |

### Candidates reviewed (05:00 pass)

- **Cognizant — ServiceNow Software Asset Management (SAM) Developer** (req 00070949051, Toronto ON-199 Bay Street, published Nov 11 2026, hybrid) — verified live on careers.cognizant.com. **NOT added**: same req already on the board via `careers.cognizant.com/uki-en/jobs/00070949051/...` dated 2026-11-11. Dedupe by role + company + location, not URL alone; a second URL for an on-board role is not a fresh row.
- **Lane Four — Salesforce Administrator** (Toronto, entry-level 0–2 yrs) — page verified live but the role is already on the board from 2026-11-09 (`lanefour.com/job-posting/salesforce-administrator/`). Source publishes no posting date; merger skips undated rows. Not re-added.
- **Scotiabank — ServiceNow Administrator Specialist** (Toronto, Req 261367) — extraction returned "not accepting any further applicants"; closed, excluded.
- **Levioconsulting — ServiceNow Developer** (gh_jid=8684331002) — HTTP 404; dead posting, excluded.
- **ServiceNow Careers / Bell / Rogers corporate roles** — filled, sales/security/SRE (not platform), outside window, or already on board. Nothing fresh addable.

### Patterns / lessons (05:00 pass)

1. **Third consecutive null run.** 00:00, 01:00, and 05:00 EST all found 0 new table rows — zero fresh merges on most hourly runs is the norm, not a failure.
2. **URL-only dedupe is insufficient.** The Cognizant careers.us-en URL was absent from the URL dedupe set, but req 00070949051 is already on the board via the uki-en URL. Always dedupe by role + company + location.
3. **Undated postings are skipped.** Lane Four is live but publishes no posted date; the board records the source's posted date, so undated rows are deliberately not merged.
4. **Always re-verify liveness before adding.** Scotiabank (closed) and Levioconsulting (404) surfaced in search but fail the liveness gate — never add closed/dead roles.

## Hourly scan — 2026-11-12 06:00 EST (11:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-12 06:00 EST (11:00 UTC) |
| Baseline (README.md tables on main before merge) | 2,893 parsed rows · ServiceNow 596 / Salesforce 614 / Other 584 · window 2026-10-13 → 2026-11-12 · HEAD 79a1018 |
| Fresh postings surfaced by this sweep | 126 unique URLs (Adzuna 51 calls, Job Bank 6 pages, Eluta 6 pages); 109 URL-verified |
| Fresh, live, not already on board | 3 postings (1 ServiceNow, 2 Salesforce) |
| Jobs merged to README.md tables | +3887 rows from the whole inbox backlog (2,893 → 6,780 parsed); this sweep's 3 postings all present in final tables (one arrived via another inbox submission in the same merge, logged as +2 new / 1 duplicate against it) |
| Jobs merged to GitHub Pages (public/) | rebuilt with `tools/build_site.py`: 5,043 unique jobs (761 mirror duplicates collapsed, 41 applied hidden) |

### Candidates reviewed (06:00 pass)

- **Dimensional Tech — Specialized IT Consultant (ServiceNow) - Senior, 1 yr contract**, Canada, posted 2026-11-12 — **added** to the ServiceNow table (`adzuna.ca/details/5962883790`).
- **Danaher Corporation — Salesforce Field Service (FSL) Developer**, Vaughan, York region, posted 2026-11-11 — **added** to the Salesforce table (`adzuna.ca/details/5961935818`).
- **Chapman Tate Associates — ERP Salesforce Financial Consultant**, British Columbia, Canada, posted 2026-11-11 — **added** to the Salesforce table (`adzuna.ca/details/5961946448`).
- Targeted **Rogers / Bell / BCE / Government of Canada / Canada.ca** Adzuna queries: 2 unique URLs, both already on the board — 0 addable.
- **Partner / elite-partner sweep** (`scripts/partner_sponsor_scan_verified.py`: Ateko, Deloitte Canada, EY, KPMG, Cognizant, Fujitsu, TELUS, CGI + ServiceNow World Forum sponsors): boards lane 0 relevant, search lane 0 relevant, 1/15 Workday tenants answered — nothing fresh addable.
- **Lane Four gap scan**: Salesforce Consultant + Salesforce Administrator, both undated — skipped per policy, no invented dates.

### Fixes

- Repaired **13 pre-existing unparseable README rows** (nested/double bracket titles from 2026-11-02 → 2026-11-04, e.g. `[[[Hiring] …](…)`, `[[IT Project Manager [4987]](…)`) that trip the merger's `rows_are_readable()` guard; all three tables re-verified parseable before merging.
- Patched `tools/jobs_merge_inbox.py`: `insert_rows` now sanitizes submission titles through `_clean_title()` (collapses leading brackets, turns inner `]` into `:`) so a malformed inbox title can't break the written README and block the next merge. Syntax-checked with `py_compile`.
- Header summary and Contents counts bumped to match: **ServiceNow 1185 / Salesforce 1355 / Other 4206 = 6,746 live postings**.

### Patterns / lessons (06:00 pass)

1. **First non-null hourly merge today.** The 00:00, 01:00, and 05:00 EST runs were null runs; this sweep found 3 verified fresh postings, all from Adzuna's dated API (`sort_by=date`, geo-scoped to Toronto/Ontario). Job Bank and Eluta contributed nothing new this hour.
2. **Role + company + location dedupe catches re-surfaced requisitions.** The Cognizant SAM Developer role re-seen this hour via another submission was skipped as a duplicate — it was already on the board under a different URL.
3. **The merger guard blocks before it drops.** `rows_are_readable()` aborted the write until all 13 unparseable README title rows were repaired — fix unparseable titles before merging, never after with `--allow-row-loss`.

## Hourly scan — 2026-11-12 08:00 EST (13:00 UTC) — NULL RUN (fifth pass)

| Metric | Value |
|---|---|
| Run time | 2026-11-12 08:00 EST (13:00 UTC) |
| Baseline (README.md tables on main) | 6,746 live postings · ServiceNow 1,185 · Salesforce 1,355 · Other 4,206 · window 2026-10-13 -> 2026-11-12 · HEAD 9779fe8 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md tables | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required; public/ last rebuilt 06:00 EST via tools/build_site.py) |

### Scans run (08:00 pass)
- scripts/fresh_ca_scan.py --days 2 (Adzuna 51 calls, Job Bank 6 pages, Eluta 6 pages): 3 fresh rows surfaced.
- scripts/today_feeds_scan.py --days 1 (Workday, SmartRecruiters, Greenhouse, Lever, Ashby, Job Bank): 13 rows; 1 SN/SF-relevant (Salesforce Technical Architect Director - PubSec / Mulesoft Canada, workday JR362275), rest data/analytics roles outside board scope.
- scripts/public_sector_scan.py: City of Toronto 9 tiles (all dated), OPS gojobs blocked by Radware bot manager, OPS Job Bank fallback 10 articles -> 0 new postings.
- scripts/partner_sponsor_scan_verified.py: boards lane 0 relevant, search lane 0 relevant, 1/15 Workday tenants answered -> 0 fresh addable.

### Candidates reviewed (08:00 pass) — all deduped, 0 added
- Dimensional Tech - Specialized IT Consultant (ServiceNow) - Senior, Canada, posted 2026-11-12 (adzuna.ca/details/5962883790): already on board at README line 1224 (via fresh-ca--2026-11-12--v1.md). Duplicate.
- Danaher Corporation - Salesforce Field Service (FSL) Developer, Vaughan, York region, posted 2026-11-11 (adzuna.ca/details/5961935818): already on board at README line 1224 (via fresh-ca--2026-11-12--v1.md). Duplicate.
- Chapman Tate Associates - ERP Salesforce Financial Consultant, British Columbia, Canada, posted 2026-11-11 (adzuna.ca/details/5961946448): already on board at README line 1223 (via fresh-ca--2026-11-11--v8.md). Duplicate.
- Salesforce - Technical Architect Director - PubSec - Mulesoft Canada (workday JR362275, "4 Locations"): already on board since 2026-10-22 via LinkedIn ca.linkedin.com/jobs/view/technical-architect-director-pubsec-mulesoft-canada-at-salesforce-4473930835 (README line 2516) and ...-4473921931 (line 1436). Cross-source duplicate - same role, different source URL; dedupe by role + company + location, not URL alone.

### Target-company checks (Rogers / Bell / partners / GC) - nothing fresh addable
- Rogers / Bell / BCE / Government of Canada / Canada.ca Adzuna queries: 0 fresh addable (all already on board or outside the 30-day window).
- ServiceNow Careers Ontario: no fresh SN developer/admin posting for Nov 11-12 (latest are sales/security/SRE).
- Salesforce careers Canada: no fresh Toronto Platform Admin / Platform Developer I posting.
- Partner / elite-partner sweep (Ateko, Deloitte Canada, EY, KPMG, Cognizant, Fujitsu, TELUS, CGI + ServiceNow World Forum sponsors): nothing fresh addable.

### Patterns / lessons (08:00 pass)
1. Fifth pass today with zero table additions at this hour. Null runs are the norm; a scan that surfaces rows but adds none is still a successful dedupe verification - the board did not stagnate, it simply had nothing genuinely new this hour.
2. Re-surfaced Adzuna requisitions are the bulk of "fresh." All 3 fresh_ca rows were already on the board from the 06:00 EST merge - Adzuna re-emits the same requisition hourly under the same URL, so URL dedupe catches them before they reach the tables.
3. Workday "Posted Today" roles still need liveness + dedupe. The Salesforce Technical Architect Director re-surfaced on todayfeeds but is already on board via LinkedIn since Oct 22 - same role, different source URL; dedupe by role + company + location.
4. Public-sector and partner boards add almost nothing dated. OPS blocked by bot manager (Job Bank fallback had nothing dated), partner Workday tenants 1/15 answering with 0 relevant - rely on aggregators (Adzuna dated API) + employer ATS feeds for dated Canadian SN/SF rows.


## Hourly scan — 2026-11-12 12:00 EST (17:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-12 12:00 EST (17:00 UTC) |
| Baseline (README.md tables + jobs.json on main @ origin 394ea96, 16:16 UTC scan) | 6,750 live postings · ServiceNow 1,187 (TOC) / 1,189 (table header) · Salesforce 1,357 (TOC) / 1,362 (table header) · Other 4,206 · window 2026-10-13 → 2026-11-12 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 6 |
| Jobs merged to README.md tables | +6 → ServiceNow 1,191 · Salesforce 1,366 · total 6,756 live postings |
| Jobs merged to GitHub Pages (public/) | pending `git push origin main` — `.github/workflows/pages.yml` rebuilds + redeploys on push (README.md is a trigger path) |

### Candidates reviewed and merged (all posted 2026-11-12, Toronto unless noted)
- BMO — ServiceNow CMDB Administrator (R260030992), Toronto ON — workday — bmo.wd3.myworkdayjobs.com — added to ServiceNow table
- BMO — ServiceNow Technology Lifecycle Analyst (R260030995), Toronto ON — workday — bmo.wd3.myworkdayjobs.com — added to ServiceNow table
- Cognizant — Salesforce Developer (req 00071305431, remote in Canada / Toronto 199 Bay Street, applies till 11/20/2026, $80–95K CAD) — **verified live directly on careers.cognizant.com** — added to Salesforce table (cognizant · salesforce)
- Galent — Salesforce Omnistudio Developer (4488534223), Toronto — linkedin — added
- Apptoza Inc. — Salesforce Senior FSC Developer / Technical Lead (4488530420), Toronto — linkedin — added
- OSI Digital — Salesforce Quality Analyst Tester (5963156514), Toronto — adzuna — added

### Dedupe outcome (checked against board before merging)
- OSI Digital adzuna URLs (Salesforce Business Analyst 5963222927, Developer 5962893078) — skipped: LinkedIn versions (4490082587, 4490093184) already absorbed by origin's 16:16 UTC scan.
- Already on board, skipped: Cognizant SAM Developer 00070949051; Cognizant Salesforce FSC Developer 00070907531; Scotiabank ServiceNow Developer 603030017 + Salesforce Developer 604373417; Bell ServiceNow System Administrator 432824; Robert Half Salesforce Developer 000954410; Lightspeed ServiceNow Developer 4482543161; Triunity ServiceNow Developer (Handshake 11766074); Take-Two ITOM 4481160381; CAAT Pension Technical Lead 4481155245 (same LinkedIn URLs as earlier-dated rows).

### Target-company checks (Rogers / Bell / partners / GC) — nothing fresh addable beyond the 6 above
- Rogers (jobs.rogers.com): Technical / corporate listings checked — no ServiceNow or Salesforce developer/admin role surfaced.
- TELUS (careers.telus.com): searched — no fresh Toronto SN/SF posting.
- Bell (jobs.bell.ca): ServiceNow hits (Developer/Integrator 431695, System Administrator 432824, Senior Technical Advisor 432829, Senior Manager Platform Delivery 432892) return "has been filled" — skipped.
- Government of Canada / jobs.gc.ca / Canada.ca: nothing dated fresh; GC platform work comes via prime vendors on their own ATS.
- ServiceNow Careers Ontario page: 16 Ontario jobs — Toronto hits are sales/security/SRE, no fresh SN dev/admin.
- Salesforce careers Canada: hub hiring is sales/Customer Success — no fresh Toronto Platform Admin / Platform Developer I.
- Partners hiring SN/SF in Toronto this period seen in feeds: Cognizant, Deloitte, KPMG, Accenture, Infosys, CGI, TCS, Wipro, HCLTech, Crossfuze, BDO, MNP, OSI Digital, Apptoza, Galent.

### Patterns / lessons (12:00 pass)
1. Re-dedupe against rebased `origin/main` before merging: the 16:16 UTC hourly scan had already absorbed the day's LinkedIn fresh batch (OSI Digital, Smart IT Frame, Enterprise Solutions). Merging blindly would duplicate rows.
2. Role + company + location dedupe beats URL-only dedupe: Cognizant publishes the same requisition under locale variants (us-en / uki-en / ca-en). Match on req ID (e.g. 00071305431), not URL prefix.
3. BMO Workday requisitions (R260030xxx) appear same-day on Workday before aggregators — check Workday first for net-new Toronto roles.
4. Always confirm apply status on jobs.bell.ca: Bell SN postings surface in search but show "has been filled" — never list filled roles as fresh.
5. Verify at least one high-value posting per run directly on the employer ATS (done: Cognizant Salesforce Developer 00071305431).
6. `scripts/sync_readme_to_jobs.mjs` parsed 0 README rows this run — these tables lack the separator/header rows the parser expects (pre-existing gap). README.md is authoritative; `public/` is rebuilt by `tools/build_site.py` via pages.yml on push.

### Files changed
- README.md (+6 rows; counts refreshed: TOC + table headers)
- jobs.json + public/jobs.json + public/gotjob/jobs.json + public/findjobs/jobs.json (sync_write attempted; README authoritative)
- JOBLESSONS_2026-11-12.MD (this entry)

## Hourly scan — 2026-11-12 13:00 EST (18:00 UTC) — NULL RUN (seventh pass)

| Metric | Value |
|---|---|
| Run time | 2026-11-12 13:00 EST (18:00 UTC) |
| Baseline (README.md tables + jobs.json on main @ HEAD e8d3578) | 6,756 live postings · ServiceNow 1,191 · Salesforce 1,366 · Other 4,206 · window 2026-10-13 → 2026-11-12 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md tables | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required; public/ republished on the 12:00 EST push via .github/workflows/pages.yml) |

### Scans run (13:00 pass)
- scripts/fresh_ca_scan.py --days 2 --linkedin 0 --eluta-pages 2 --jobbank-pages 1 --geos "||Toronto, Ontario|Ontario": hit the 240s wall clock before completing (LinkedIn guest pass + Adzuna calls are the slow path). Partial report generated 13:09:38Z surfaced 1 row past URL+liveness+board dedupe — Yochana "ServiceNow Product and Platform Consultant" (adzuna.ca/details/5961953846, posted 2026-11-11, Remote Canada) — already on the board (added via fresh-ca--2026-11-12--v1.md in the 12:00 EST merge). No inbox file was written (scan timed out before the inbox step).
- Manual verification sweep (web search + direct page fetch + README/jobs.json URL dedupe): all candidates below already on board, closed, filled, or out of scope.

### Candidates reviewed (13:00 pass) — all deduped, 0 added
- Cognizant — Salesforce Developer (req 00071305431, Toronto/remote 199 Bay Street, applies till 11/20/2026, $80–95K CAD): verified live directly on careers.cognizant.com — already on board (2026-11-12, cognizant · salesforce)
- City of Toronto — Systems Integration Specialist (AMANDA Developer/Administrator, posting 12-Nov-2026 to 26-Nov-2026, Salesforce is an asset): already on board (2026-11-12, city-government)
- Scotiabank — ServiceNow Developer (Req 260518 / 603030017): already on board (2026-11-04); employer page now returns "not accepting any further applicants" — closed, excluded
- Yochana — ServiceNow Product and Platform Consultant (adzuna 5961953846): already on board (Remote Canada)
- Survalent / Amyantek / Benevity / Procom / Altus Group Salesforce + ServiceNow roles (Toronto/Mississauga, posted 2026-11-04 → 2026-11-11): already on board
- Bell ServiceNow reqs (Developer/Integrator 431695, System Administrator 432824, Senior Technical Advisor 432829, Senior Manager Platform Delivery 432892): return "has been filled" — skipped
- Rogers — Technical Specialist Markham (Req 343759, SN/SF only as comparable tools, not a platform role); Lead Management Operations Salesforce (Req 343961): already on board or out of scope
- ServiceNow Careers Ontario page (16 jobs): Toronto hits are sales/security/SRE, no fresh SN dev/admin
- Salesforce careers Canada: hub hiring is sales/Customer Success — no fresh Toronto Platform Admin / Platform Developer I

### Target-company checks (Rogers / Bell / partners / GC) — nothing fresh addable
- Rogers, Bell, TELUS, Government of Canada / jobs.gc.ca / Canada.ca: nothing fresh addable this hour
- Partner / elite-partner sweep (Ateko/FX Innovation, Deloitte, EY, KPMG, Cognizant, CGI, TCS, Wipro, HCLTech, Crossfuze, BDO, MNP, OSI Digital, Apptoza, Galent, Lane Four, CloudKettle): nothing fresh addable

### Patterns / lessons (13:00 pass)
1. Seventh pass today with zero table additions. Null runs are the norm at this hour; a scan that surfaces rows but adds none is still a successful dedupe verification — the board did not stagnate, it simply had nothing genuinely new this hour.
2. fresh_ca_scan.py timed out at 240s; its partial report still dedupes cleanly and its single survivor was already on the board. Split Adzuna and the LinkedIn guest pass into separate sub-runs to fit the session wall clock.
3. URL-only dedupe catches re-emitted Adzuna requisitions; role + company + location dedupe catches locale-variant Cognizant requisitions (us-en / uki-en / ca-en).
4. Confirm apply status before listing: Bell filled roles and the closed Scotiabank role both surfaced in search but fail the liveness/apply gate — never list closed or filled roles as fresh.

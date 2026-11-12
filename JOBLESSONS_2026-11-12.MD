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



# JOBLESSONS — 2026-11-20 14:00 EST (19:00Z) hermes cron

Toronto-first ServiceNow / Salesforce scan. Sources: LinkedIn guest, Adzuna (demo creds in
`scripts/daily_job_scan.mjs`), SmartRecruiters, Workday CXS (retried), Greenhouse, Lever, Ashby,
remote feeds. Dedupe against README tables + `jobs.json` + `APPLIED.md` by URL **and LinkedIn job id**.

## Result

- Scan output: `fresh=526 merged=5614` (SN 1191 / SF 4290), `scrapedAt 2026-11-20T19:01:41Z`.
- Workday step hit HTTP 429 on **all** tenants at :01Z (CI hourly collision). A 9-tenant retry at
  ~19:07Z returned **HTTP 200 on all 20 calls** and recovered one real miss (CIBC).
- Genuinely-new SN/SF today: the automated scan produced **0** (see mirror note below). The hourly
  value came from the Workday retry + body checks: **3 verified ServiceNow roles merged**.
- README now **6119 live postings**; page rebuilt (5047 cards; SN 868 / SF 925; 830 mirror collapses).
- `board_invariants.py`: **PASS** (29 errors / 227 warnings, `no kind grew`). `check_readme_sort`: OK.

## Merged (3) — all ServiceNow

| Posted | Role | Company | Location | Evidence |
|---|---|---|---|---|
| 2026-11-20 | Senior Production Application Support Analyst (ServiceNow Admin/CMDB) | CIBC | Toronto, ON | Workday CXS "Posted Today" + job-page body: **ServiceNow Administrator certification required**, 5+ yrs ITSM/CMDB/MID servers/CSDM/ITAM. Missed by scan (Workday 429). |
| 2026-11-20 | ServiceNow SAM Pro Consultant (Senior SAM Pro Technical SME) | Pacer Group | Canada (Remote) | LinkedIn detail page live, posted <1h, **CA$115–120K**, full-time permanent. |
| 2026-11-19 | ServiceNow CSM/HRSD | NLB Services | Mississauga, ON (hybrid) | Adzuna API `created 2026-11-19T…`, 3 days onsite; detail 403 (CloudFront, blocked≠closed). |

## Held / rejected (do not re-add without new evidence)

- **Avanciers "Senior Salesforce Developer" (4491935174)** — **title-twin mirror** of the already-tracked
  "Salesforce Consultant" (same LinkedIn job id 4491935174). Not new. (Job-id equality is a hard dedupe.)
- **Yochana — ServiceNow Developer cum Architect (Mississauga, 4492501308)** — the detail URL now
  redirects to a generic LinkedIn search page; posting expired/unavailable. Drop, not a vacancy.
- **ServiceNow Inc — Staff Cloud Security Engineer / Sr Solution Sales Executive CRM (CPQ) (Toronto)** —
  security-engineering and vendor-sales roles; not ServiceNow platform build. Off-track.
- **LGS, an IBM Company — 6–7 ServiceNow roles (Ville-Marie, Quebec)** — developer, HRSD/CSM/IRM
  architect + Now Assist AI. Substantive and from an Elite partner, but **Quebec**; held as leads for a
  Canada-wide batch rather than a Toronto-first hour.
- **PwC — Technical Salesforce Associate (Adzuna, "Canada")** — mirrors the PwC Ottawa LinkedIn row
  already on the board; Ottawa, not Toronto. Skip.
- Normalize dropped 28 rows: 26 outside-window, 1 non-canada (NeuraFlash Colombia), 3 vendor-sales.

## Patterns / gotchas learned this run

1. **Workday 429 at :01Z is transient — retry ~5–8 min later.** The `daily_job_scan.mjs` Workday step
   runs at exactly :01Z and collides with the CI hourly scan (`cron: 0 * * * *`); every tenant 429'd.
   A hand-run bash probe of 9 tenants at ~19:07Z (8 s spacing, `--compressed`, Content-Type/Accept/Origin
   only, **no Referer**) got HTTP 200 on all 20 calls. The retry recovered the CIBC role the scan could
   not see — **always re-probe Workday after a 429-heavy scan before concluding "no new reqs".**
2. **Generic Workday titles hide ServiceNow platform roles — body-check "Posted Today" rows.**
   CIBC "Senior Production Application Support Analyst" and "IT Administration Analyst" both surfaced
   under `searchText=ServiceNow`. Body read: the *Support Analyst* requires a **ServiceNow Administrator
   cert + ITSM/CMDB/MID/CSDM** (real platform role → merged); the *IT Administration Analyst* only
   *uses* ServiceNow for tasks (Exchange/AD admin → skip). Same source, opposite verdicts.
3. **`sync_readme_to_jobs.mjs` narrowed jobs.json 5613→5584 (dupes-collapsed=30, added=1).** It is NOT
   a pure no-op this hour — it re-collapses duplicates. Judge health by SN/SF core + the live
   `jobs-data.json`, not the raw jobs.json count. Site SN/SF (868/925) stayed healthy.
4. **The heading-glued README bug persists.** `### ServiceNow jobs (…)_…_<details>…</summary>| row |…`
   still glues ~15 rows onto the heading line (no newline). `insert_rows` inserts the new rows cleanly
   *after* that glued block; `_bump_counts` bumps the heading number but not the `<summary>` number
   (re.match misses the mid-line summary), so heading/summary drift grows by 1/insert. Pre-existing;
   `board_invariants` does not ratchet it. Fix at source someday by splitting the heading line.
5. **Vendor twins are distinct, keep both.** Pacer Group "SAM Pro Consultant" (4492825407) and the
   already-boarded Avanciers "Senior SAM Pro Technical SME" (4491961105) are separate staffing-firm
   postings of a similar client need — the user applies to each, so both stay.
6. **Rogers careers now returns rows but only sales roles.** `jobs.rogers.com/search/?q=salesforce&sortColumn=referencedate`
   rendered real `data-row`s (Field Sales Specialist, Account Manager, Delivery Specialist) — **no
   ServiceNow/Salesforce platform req**. `q=servicenow` returned none. Bell (`jobs.bell.ca`) is still
   zero for both; Bell SN hiring surfaces as **Ateko / FX Innovation** on LinkedIn.
7. **Job Bank `servicenow` search is template noise** — returned "shipping coordinator", "cloud
   developer", "programmer analyst" etc.; **no posting title names the platform**. Only trust a Job
   Bank hit whose *title* names ServiceNow/Salesforce.
8. **Accenture's fresh Toronto SF role is already tracked.** `AccentureCareers` with `searchText="Salesforce Toronto"`
   surfaced "Salesforce Data 360 Cloud MarTech Consultant" (R00373203, Posted Today) — same req as the
   board's Accenture Data Cloud MarTech row. Append the city to `searchText` on Accenture/Salesforce or
   page 1 is all non-Canada.
9. **CIBC Workday paths are lowercase `search` site + Title-Case city.** `https://cibc.wd3.myworkdayjobs.com/en-US/search/job/Toronto-ON/<Title-slug>_<reqid>`.

## Partner / elite / sponsor coverage this hour

- **ServiceNow ecosystem**: ServiceNow Inc (vendor — only security/sales in Toronto), CGI, PwC, LGS (IBM,
  Quebec cluster), Pacer Group (found 1), Ateko/FX (Bell), Compugen, Cognizant, Accenture, Kyndryl.
  CIBC + Interac + BMO + TD are the live ServiceNow *end-users* in the GTA.
- **Salesforce ecosystem**: PwC Canada (Associate, Ottawa), Deloitte, Slalom, NeuraFlash, Traction Rec,
  OSI Digital, Avanciers, IBM, CGI, Cognizant — Toronto SF volume is agency/consultancy-heavy.
- **Toronto enterprises hiring platform talent**: Rogers (sales only today), Bell (0; via Ateko), TD,
  BMO, CIBC (found SN role), Scotiabank, Manulife, Sun Life, Canada Life, Loblaw, Celestica, Mackenzie,
  Citco, WSIB, Ontario Health, Metrolinx, City of Toronto. **Government**: no fresh GoJobs/Shared
  Services Canada SN/SF posting found (portals Radware-walled; Job Bank noise only).
- Events: ServiceNow World Forum Toronto / Salesforce World Tour Toronto sponsor lists = employer leads,
  not vacancies.

## Coverage gaps this run

- Workday: scan step 0/15 (429); retry read 9 tenants (ServiceNow) + Accenture/TD/BMO/Manulife
  (Salesforce) — GDIT is US-only, Salesforce vendor board all non-Canada.
- Adzuna: 207 postings; detail pages 403 (CloudFront) to datacenter IPs — accept API `created`+title.
- LinkedIn: 275 cards; 1 detail 429/authwall; Yochana detail expired.
- No brand-new 2026-11-20 SN/SF platform req beyond CIBC — consistent with a Friday-afternoon, saturated board.

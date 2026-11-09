# JOBLESSONS_2026-11-09.MD

# BESTIEJOB Hourly Scan — Job Search Lessons

**Date**: 2026-11-09
**Run time**: 2026-11-09 00:00 EST (05:00 UTC)
**Scope**: Fresh Toronto / GTA ServiceNow and Salesforce postings
**Repo**: github.com/eltonaguiar/BESTIEJOB (branch: main)
**Live board**: https://eltonaguiar.github.io/BESTIEJOB/

## Scan summary

| Metric | Value |
|---|---|
| Sources queried | LinkedIn (ca.linkedin.com), Indeed.ca, Job Bank / jobs.gc.ca, ServiceNow Careers Ontario, Salesforce Careers Canada, Rogers careers, Bell careers; partner/employer sites: Accenture, Deloitte, KPMG, Capgemini, CGI, TELUS, RBC, Scotiabank, BMO, TD, CIBC |
| Dedupe baseline (README.md tables + jobs.json on main) | 7,783 unique URLs |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required) |

## Candidates reviewed

- **Accenture — ServiceNow Technical Architect** (Job No. R00356209, Toronto; Job Bank closing 09 Nov 2026; ServiceNow Elite/Global Elite Partner) — page verified live and **not** on the board, but the posting is not fresh (Job Bank close date implies posting ~early October). Excluded from the fresh merge; flagged as a quality backfill candidate for a future run. URL: https://www.accenture.com/ca-en/careers/jobdetails?id=R00356209_en&title=ServiceNow+Technical+Architect
- **Rogers — Lead Management Operations** (Salesforce, Toronto + 197 other locations; posted 28 Oct 2026) — verified live, not on board; outside the freshness window. URL: https://jobs.rogers.com/job/Toronto-Lead-Management-Operations-ON/1444677100/
- **Bell — ServiceNow System Administrator** (jobs.bell.ca job 432824) — page returns "this job ... has been filled"; excluded. Never add filled roles.
- ~14 LinkedIn/Indeed partner postings (KPMG, Deloitte, Scotiabank, Fujitsu, CGI, Moneris, Altus Group, MLSE, Carbon6, Epsilon, Robert Half, SS&C, Veracity, Pyramid) — each either already present in the master dedupe set or older than ~48h; LinkedIn posting pages are behind a login wall (HTTP 422 on extraction), so dates could not be independently verified.

## Already on the board (context — today's 04:35 UTC jobs.json scan captured 4,998 jobs, 635 new)

ServiceNow Careers Toronto: Staff Systems Engineer (×2, 2026-11-06), Staff Security Engineer \| Security Engineering (11-06), Staff Security Engineer \| Enterprise Security (11-06), Senior Staff Security Engineer \| Systems Engineering (11-06), Senior/Staff SRE Canada Protected B (11-05). Also present: TD, Central 1, CIBC, 407 ETR, Equinix, Lightspeed, KPMG (×8), ServiceNow Montreal — all 2026-11-08. The README tables already carry postings through 2026-11-09, so the board is current through this scan.

## Patterns / lessons for future agents

1. **Surface Toronto ServiceNow/Salesforce postings are captured within hours.** jobs.json is refreshed multiple times daily (today's scan at 04:35 UTC added 635 jobs). Hourly general web searches rarely surface anything not already captured — do not expect fresh merges every run.
2. **LinkedIn pages are a login wall.** Extractors get HTTP 422; posting dates can't be verified by page extraction. LinkedIn job IDs are only hints (e.g. the 44545xxxx cluster = KPMG postings dated 2026-11-08; the 420-422M cluster = early-November). Never add a LinkedIn-sourced role without a verifiable date.
3. **Job Bank search results render via msen.vfairs.com mirror links** — not canonical application URLs. Always resolve to the employer's own career page before adding (e.g. accenture.com/ca-en/careers/jobdetails?id=R00356209_en).
4. **Indeed.ca "New" tags appear without direct extractable URLs** in search results (Survalent Salesforce Administrator Mississauga; CloudKettle Revenue Cloud Architect Toronto; Pyramid Senior Salesforce FSC Developer Toronto). Capture the direct posting URL at search time, or the role can't be verified or deduplicated.
5. **Telco employers post SN/SF work under non-SN/SF titles.** Rogers' Salesforce work appears as "Lead Management Operations" (marketing operations), not a developer/architect title. Keyword-only scans miss these; scan named employers' career sites directly.
6. **Always re-verify before adding.** Bell's jobs.bell.ca explicitly says "has been filled". Filled roles must never enter the board.
7. **Dedupe against both README.md table URLs and jobs.json** — the same role arrives via jobs.ca, LinkedIn, and employer ATS under different URLs. Combined baseline this run: 7,783 unique URLs. Normalize by stripping query strings and trailing slashes.

## Recommended next scans

- Target employer ATS deep-links directly: `site:*.myworkdayjobs.com` ServiceNow Toronto, `site:*.greenhouse.io` / `site:*.lever.co` Salesforce Toronto — aggregator listings lag employer sites.
- Re-check Accenture R00356209 after its 09 Nov 2026 closing — relisted or expired.
- Re-check Rogers Lead Management Operations on the next in-window cycle (posted 28 Oct 2026; within the board's 30-day live window if still open).

## Files touched

- `JOBLESSONS_2026-11-09.MD` — this file, added to repo root on main.
- `README.md` — no changes (zero verified fresh jobs this hour).
- `public/` (GitHub Pages) — no changes; no redeploy required.

---

## Hourly scan — 2026-11-09 01:00 EST (06:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 01:00 EST (06:00 UTC) |
| Baseline (README.md on main) | 5,395 live postings · ServiceNow 709 · Salesforce 869 · Other 3,817 · window 2026-10-10 → 2026-11-09 |
| Dedupe baseline | 7,783 unique URLs (README.md tables + jobs.json) |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages | 0 (no changes required) |

### Candidates reviewed

- **ServiceNow Careers Toronto** (all Nov 05–06 postings): Staff Systems Engineer (JB0073788), Senior/Staff SRE Canada Protected B (JB0076846/JB0076847), Senior Staff Security Engineer | Systems Engineering (JB0076457), Staff Security Engineer | Security Engineering (JB0076454), Staff Security Engineer | Enterprise Security (JB0076455), Staff Database Engineer — all already on the board (careers.servicenow.com and jobs.smartrecruiters.com URLs confirmed in README.md). Duplicates; skipped.
- **Government of Canada (jobs.gc.ca)** — zero ServiceNow/Salesforce Toronto results.
- **Rogers** — Lead Management Operations (Salesforce lead work, req 343961) posted ~28 Oct–04 Nov 2026; outside freshness window; Rogers Technology list shows no SN/SF technical roles. Already flagged by the 00:00 run; re-check next in-window cycle.
- **Bell** — ServiceNow System Administrator (432824), Senior Technical Advisor (432829, application deadline 11/02/2026 expired), Developer/Integrator (BECACA431695) — all return "has been filled" / no longer accepting applicants. Filled roles never enter the board.
- **Indeed.ca listings** — search-result pages only; no direct posting URLs extractable. Moneris Principle Salesforce Developer (10/30 & 10/28) and Epsilon Salesforce Developer Lead – Data Cloud already on board; remaining hits are sales-titled (rejected by title rule) or unverifiable.
- **LinkedIn** — login wall (HTTP 422); posting dates cannot be independently verified. No LinkedIn-sourced role added without a verifiable date.

### Patterns / lessons (01:00 run)

1. **Hourly general web search adds almost nothing after the daily jobs.json refresh.** jobs.json is refreshed multiple times a day (today's 04:35 UTC scan captured 4,998 jobs, 635 new); README tables on main already carry postings through 2026-11-09. Zero fresh merges on most hourly runs is the norm, not a failure.
2. **Employer career sites are the only reliable freshness source.** ServiceNow Careers Ontario lists 16 Toronto jobs; all six current Toronto postings (Nov 05–06) are already on the board. Vendor-direct verification beats aggregator mirrors.
3. **Bell filled roles.** Every Bell ServiceNow hit this run was filled or expired (deadline 11/02/2026). Never add filled roles; mark them dead in the source scan rather than re-checking each run.
4. **jobs.gc.ca returned zero SN/SF Toronto hits.** Government platform work arrives via prime vendors (Accenture, Deloitte, KPMG, CGI, Ateko/Bell) on their own ATS — scan vendor ATS deep-links for "Protected B" / GC clauses instead.
5. **Indeed "New" tags without direct URLs remain unverifiable.** Capture the direct posting URL at search time or the role cannot be deduplicated or verified.
6. **Duplicate baseline holds at 7,783 unique URLs.** Normalize by stripping query strings and trailing slashes; the same role arrives via jobs.ca, LinkedIn, and employer ATS under different URLs.

### Files touched (01:00 run)

- `JOBLESSONS_2026-11-09.MD` — this file, updated on repo root on main (01:00 EST run section added).
- `README.md` — no changes (zero verified fresh jobs this hour).
- `public/` / GitHub Pages — no changes; no redeploy required.

## Hourly scan — 2026-11-09 05:00 EST (10:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 05:00 EST (10:00 UTC) |
| Baseline (README.md tables on main) | 5,405 unique curated URLs · ServiceNow 723 · Salesforce 882 · Other 3,834 · window 2026-10-10 → 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 2 |
| Jobs merged to README.md | 2 |
| Jobs rebuilt on GitHub Pages (public/) | 2 (via `python3 tools/build_site.py`; `pages.yml` redeploys on push to main) |

### Candidates reviewed

- **Scotiabank IT & Digital Banking jobs page** (jobs.scotiabank.com/go/IT-&-Digital-Banking-Jobs/2298017/, page 1 = newest 25 of 132, reference-date sort desc): **DevOps Engineer (Salesforce), Toronto, Nov 07 2026, req 276046** and **Senior Manager, Salesforce Engineering, Toronto, Nov 05 2026, req 275778**. Both requisition pages verified live; neither URL on the board → merged to the Salesforce table via `inbox/hermes-cron--2026-11-09--v1.md` (+2 new, 0 duplicate). The same roles already exist on the board via LinkedIn mirrors dated 2026-10-31 (DevOps Engineer(Salesforce) 4476839954; Senior Manager, Salesforce Engineering 4475490374), so the direct requisition URLs add the fresher verified date without duplicating.
- Remaining page-1 Scotiabank roles are not SN/SF (IAM Architect, strategy enablement, payments BA, engineering leads, platform engineers); no fresh ServiceNow posting on page 1.
- **Indeed.ca ServiceNow / Salesforce Toronto** — BMO ServiceNow SAM Administrator–ITAM ("Nouveauté"), Alimentiv ServiceNow Platform Specialist, BFG Enterprise Services ServiceNow Administrator/Developer, CloudKettle Salesforce Revenue Cloud Architect ("New"): search results show no extractable absolute posting date and no resolvable direct posting URL → leads only, not merged (the merger rejects rows without a `YYYY-MM-DD` and aggregator listing URLs).
- **ServiceNow Careers Toronto / KPMG / Deloitte / CGI / Salesforce core postings (Nov 05–08)** — already on the board; skipped as duplicates.
- **Rogers / Bell / jobs.gc.ca** — no fresh SN/SF (Rogers Lead Management Operations posted Oct 28, stale; Bell ServiceNow System Administrator returns "has been filled"; jobs.gc.ca zero SN/SF Toronto results) — consistent with the 00:00 and 01:00 runs.

### Patterns / lessons (05:00 run)

1. **Big-bank SuccessFactors pages expose date-sorted lists with absolute dates** — Scotiabank's careers page sorts by reference date, newest first, making it the most reliable freshness source this run. Indeed.ca search pages are listing URLs (rejected by the merger) and "New" tags rarely carry an extractable date.
2. **The board is current through 2026-11-09** — hourly merges are now small; 0–2 verified adds per run is the expected range.
3. **Same role, different URLs:** both Scotiabank roles were already on the board via LinkedIn mirrors (Oct 31). Direct employer-ATS URLs are still worth merging when they carry a newer verified date; normalize URLs (strip query strings, trailing slashes, LinkedIn session params) before dedupe.
4. **Filled or expired roles never enter the board** (Bell example); record them dead in the source scan and stop re-checking each run.

### Files touched (05:00 run)

- `inbox/hermes-cron--2026-11-09--v1.md` — this run's submission (+2 new, 0 duplicate).
- `README.md` — 5,407 live postings (ServiceNow 713, Salesforce 877, Other 3,817), window 2026-10-10 → 2026-11-09; +2 Salesforce rows (Scotiabank); expired rows archived to `README.BAK_2026-11-09T100805Z.md`.
- `public/` (GitHub Pages) — rebuilt with `python3 tools/build_site.py`; `pages.yml` redeploys on the push to main.
- `JOBLESSONS_2026-11-09.MD` — this file, 05:00 EST section added.

## Hourly scan — 2026-11-09 06:00 EST (11:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 06:00 EST (11:00 UTC) |
| Baseline (README.md on main) | 5,407 live postings · ServiceNow 713 · Salesforce 877 · Other 3,817 · window 2026-10-10 → 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages | 0 (no changes required) |

### Candidates reviewed (06:00 run)

- **ServiceNow Careers Toronto** (Nov 05–06): Staff Systems Engineer (JB0073786, JB0073788) and Senior/Staff SRE Canada Protected B (JB0076846, JB0076847). careers.servicenow.com pages return HTTP 403 to automated probes (bot wall, not dead) — title/date/location confirmed via search snippets. All four requisitions are already on the board via jobs.smartrecruiters.com mirrors (744000160277860, 744000160278249, 744000159911194 card, 744000159910447); build_site.py clusters them under existing cards. Skipped as duplicate requisitions.
- **Rogers** (jobs.rogers.com/Greenhouse): 21 Technology roles, newest Nov 7; no ServiceNow/Salesforce technical role (Platform Specialist mentions ServiceNow only incidentally). Nothing added.
- **Bell** (jobs.bell.ca/Phenom): Salesforce Solution Architect 430856, Platform Manager 428467, Marketing Cloud Email Developer 431169, Developer 429834, BECACA428466 — all return "has been filled". Excluded; filled roles never enter the board.
- **jobs.gc.ca / Canada.ca** — zero ServiceNow/Salesforce Toronto hits.
- **Partners** — Deloitte SF Developer - Digital Customer 135279 already on board. Capgemini careers sits behind an SAP cookie-consent wall (extraction returns cookie text only, posting date unverifiable) — lead only (Sr Salesforce Developer, Toronto, permanent, $92K–$114K seen on Indeed).
- **LinkedIn.ca** — ServiceNow/Salesforce Toronto sorted by date; no verifiable new posting outside existing mirrors.

### Patterns / lessons (06:00 run)

1. **Zero-fresh runs are the norm right after a bulk jobs.json refresh** — the 10:59 UTC scan captured 5,024 listings (635 new in-cycle). Check the board's "as of" date before expecting hourly merges.
2. **Dedupe by requisition, not just URL** — a fresh careers.servicenow.com URL adds zero new page cards when the same JB number is already mirrored via jobs.smartrecruiters.com (build_site.py clusters by canonical title + employer + compatible location).
3. **Bot-wall ≠ dead** — 403 from careers.servicenow.com/jobs.gc.ca-style probes; verify via snippets. Only 404/410/451 and explicit "filled/expired" body markers retire a posting.
4. **Cookiewalled ATS (Capgemini SAP careers) cannot be dated by extraction** — use Indeed/Google snippets or skip the role.
5. **Filled roles stay out** (Bell example) — record them dead in the source scan so they aren't re-checked every run.

### Files touched (06:00 run)

- `JOBLESSONS_2026-11-09.MD` — this file, 06:00 EST section added.
- `README.md` — no changes (zero verified fresh jobs this hour).
- `jobs.json` / `public/` — no changes; no redeploy required.

## Hourly scan — 2026-11-09 07:00 EST (12:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 07:00 EST (12:00 UTC) |
| Baseline (README.md on main) | 5,411 live postings · ServiceNow 717 · Salesforce 877 · Other 3,817 · window 2026-10-10 → 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 1 |
| Jobs merged to README.md | 1 |
| Jobs rebuilt on GitHub Pages (public/) | 1 (via `python3 tools/build_site.py`; `pages.yml` redeploys on push to main) |

### Candidates reviewed (07:00 run)
- **TD — Product Owner I - AskHR** (Toronto/London, ON; Workday req R_1519634; posted 2026-11-08 "Posted Yesterday"; application end date 2026-11-09; $96,900–$136,800 CAD): Workday page renders a cookie/JS shell to headless probes, but the search index captured the page's posted date. Merged to the **Other** table — it's a ServiceNow AskHR/HRSD product-owner role at a Big Five bank, but the title carries no SN/SF keyword so `classify()` places it in Other. Not previously on the board. URL: https://td.wd3.myworkdayjobs.com/TD_Bank_Careers/job/Toronto-Ontario/Product-Owner-I---AskHR_R_1519634
- **Benevity — Senior Salesforce Administrator** (Toronto hybrid, Ashby; "Posted Yesterday" on a jobs mirror): verified live on jobs.ashbyhq.com but already on the board since 2026-10-28 — duplicate by URL; skipped.
- **Scotiabank — Salesforce Developer** (req 265640): jobs.scotiabank.com returns "currently not accepting any further applicants" — closed; skipped. Never add filled/closed roles.
- **Solink — Senior Salesforce Developer** (Remote Canada): direct Ashby URL returns HTTP 404 — a true dead posting; skipped.
- **VML MAP — Salesforce Marketing Cloud Manager - Development** (Toronto, Greenhouse): live posting but no extractable posted date on the page — undated rows cannot be merged; skipped.
- **Indeed.ca / LinkedIn.ca / Job Bank / Rogers / Bell / jobs.gc.ca**: Indeed listing pages carry no extractable dates or direct posting URLs; LinkedIn is a login wall; Bell's SN/SF roles return "has been filled"; Rogers shows no fresh SN/SF technical role; jobs.gc.ca zero SN/SF Toronto hits — consistent with the 00:00/01:00/05:00/06:00 runs.

### Patterns / lessons (07:00 run)
1. **One verified add this hour** — TD's AskHR product owner (ServiceNow HRSD platform work) merged to Other; zero-to-one fresh merges remain the norm late in the monitoring window.
2. **Mirror "Posted Yesterday" ≠ board-fresh** — Benevity's SF Admin re-surfaced as "Posted Yesterday" on a jobs mirror but entered the board 2026-10-28; URL dedupe caught the duplicate.
3. **Dead vs. bot-wall distinction holds** — Solink's Ashby URL is a true 404 (dropped); TD's Workday shell is a live page behind cookie/JS, not dead (search-snippet date accepted, consistent with prior 403-handling practice).
4. **Undated employer postings can't be merged** — VML MAP's Greenhouse page and Ashby postings show no posted date; the merger requires an absolute YYYY-MM-DD.

### Files touched (07:00 run)
- `inbox/hermes-cron--2026-11-09--v2.md` — this run's submission (+1 new, 0 duplicate).
- `README.md` — 5,412 live postings (ServiceNow 717, Salesforce 877, Other 3,818); +1 Other row (TD AskHR).
- `README.BAK_2026-11-09T120923Z.md` — pre-merge backup created by the merger.
- `public/jobs-data.json` + `public/index.html` — rebuilt with `python3 tools/build_site.py` (4,516 indexed jobs incl. jobs.json union); `pages.yml` redeploys on push to main.


## Hourly scan — 2026-11-09 08:00 EST (13:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 08:00 EST (13:00 UTC) |
| Baseline (README.md tables on main) | 5,412 live postings · ServiceNow 717 · Salesforce 877 · Other 3,818 · window 2026-10-10 → 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 (hermes-cron Scotiabank rows already merged by the 05:00 EST run; this run's resubmission caught as duplicate by URL) |
| Jobs rebuilt on GitHub Pages (public/) | 4,512 indexed jobs (servicenow 763, salesforce 802, other 2,947) via `python3 tools/build_site.py`; `pages.yml` redeploys on push to main |

### Candidates reviewed (08:00 run)

- **Automated hourly scan** (`scripts/daily_job_scan.mjs`): 635 fresh postings from SmartRecruiters (ServiceNow), Workday (Salesforce/BMO/TD/Moneris/BDO/others), Greenhouse, Lever, Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna Canada — after URL dedupe against jobs.json, zero net-new rows passed the freshness gate (all were already in the feed or duplicates).
- **Liveness gate** (`tools/verify_links.py --days 2`): probed 54 recent rows; 4 dead dropped (BMO via Procom Senior Salesforce Developer; Slalom Enterprise ServiceNow SPM Technical Consultant; Slalom Salesforce Developer Montreal; Koniag Salesforce Developer clearancejobs); 22 unknown (bot-walled) kept.
- **Gap scan** (`scripts/gap_scan.mjs`): partner career pages (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) — Lane Four has 2 undated Salesforce roles (consultant, administrator) that cannot be merged without a posted date; Adzuna variants +3 new.
- **Targeted employer checks (per scan scope)**:
  - **Rogers** (jobs.rogers.com Greenhouse): Technology page shows 21 roles, newest Nov 7, no ServiceNow/Salesforce technical role; Lead Management Operations (Salesforce, req 343961, ~Oct 28) is outside the freshness window. Nothing added.
  - **Bell** (jobs.bell.ca Phenom): ServiceNow Senior Technical Advisor 432829, ServiceNow System Administrator 432824, ServiceNow Developer/Integrator BECACA431695 all return "has been filled". Filled roles never enter the board.
  - **Government of Canada** (jobs.gc.ca / canada.ca): zero direct ServiceNow/Salesforce Toronto postings. GC platform work arrives via ServiceNow's Canada Protected B roles (already on the board) and prime vendors.
- **Partner/Elite Partner check**: Accenture (ServiceNow Technical Architect Toronto, posted 2026-11-06), Deloitte (Senior Consultant ServiceNow Platform Toronto; RTE Toronto; Cyber Sales Executive Toronto), KPMG (multiple ServiceNow consultant roles Toronto/Ottawa/Vancouver/Montreal) — all already on the board via LinkedIn/Workday mirrors dated 2026-11-08; no net-new adds.

### Patterns / lessons (08:00 run)

1. **Zero-fresh runs are the norm late in the monitoring window** — after the 13:02 UTC jobs.json refresh captured 635 fresh postings, the 08:00 EST scan found nothing net-new; all were already mirrored or duplicates.
2. **Employer career pages confirm filled/stale status reliably** — Rogers' Technology listing (21 roles, date-sorted) and Bell's explicit "has been filled" pages let us retire roles without re-checking each hour.
3. **Undated postings can't be merged** — Lane Four's Salesforce Consultant and Administrator pages publish no posted date; the merger skips them rather than inventing a date.
4. **Same role, multiple dated mirrors** — Scotiabank's two Salesforce roles entered via hermes-cron at 05:00 EST (direct jobs.scotiabank.com requisitions with Nov 05/07 dates); the 08:00 run's resubmission was caught as duplicate by URL.

### Files touched (08:00 run)

- `JOBLESSONS_2026-11-09.MD` — this file, 08:00 EST section added.
- `README.md` — no net-new table rows (counts unchanged: 5,412 live postings); backup reference advanced to `README.BAK_2026-11-09T130447Z.md`.
- `jobs.json` / `public/*.json` — rewritten by scan + verify + sync (5,030 feed rows; 4 dead dropped, 3 gap-scan adds).
- `public/jobs-data.json` + `public/index.html` — rebuilt (4,512 indexed jobs); `pages.yml` redeploys on push to main.
- `dead_urls.txt` — 4 dead URLs appended.
## Hourly scan — 2026-11-09 09:00 EST (14:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 09:00 EST (14:00 UTC) |
| jobs.json baseline on main | 5,034 unique URLs · scrapedAt 2026-11-09T13:33:00Z (08:33 EST) · newThisScan 635 |
| README.md baseline on main | "as of 2026-11-09" · window 2026-10-10 → 2026-11-09 · 5,412 live postings (SN 717 · SF 877 · Other 3,818) |
| GitHub Pages (public/) | 4,512 indexed jobs (servicenow 763, salesforce 802, other 2,947); pages.yml redeploys on push to main |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs rebuilt on GitHub Pages (public/) | 0 (no changes required; board already current this hour) |

### Candidates reviewed (09:00 run)

Web searches across Indeed.ca, LinkedIn, Salesforce Careers Canada, ServiceNow Careers Ontario, jobs.rogers.com, jobs.bell.ca, jobs.gc.ca, plus partner/employer sites (Accenture, Deloitte, KPMG, CGI, Cognizant, Altus Group, Lane Four, BMO, Survalent, Caseware, Moneris):

- **Lane Four — Salesforce Administrator, Toronto, Hybrid, Entry Level, $50K–75K** (~Nov 5, surfaced via jobs.ca mirror) — jobs.ca URL not in jobs.json, but the canonical posting https://lanefour.com/job-posting/salesforce-administrator/ IS already on the board (source lanefour, posted 2026-11-09). URL dedupe by domain+path caught the mirror; not re-added.
- **Survalent — Salesforce Administrator (Hybrid), Mississauga, $70K–90K** — already on board (adzuna 2026-11-05; LinkedIn 2026-11-04).
- **Altus Group — Salesforce Platform Developer, Toronto/remote, $105K–115K, PD1/PD2** — already on board (simplyhired 2026-11-09).
- **BMO — ServiceNow SAM Administrator - ITAM, Toronto (Workday)** — already on board (posted 2026-11-09).
- **ServiceNow careers (vendor) Toronto — Staff Systems Engineer / SRE / Security Engineer Canada Protected B (Nov 5–6)** — already on board; Canadian citizen/PR + Reliability Status required.
- **Salesforce careers Canada — CSM, Account Executive, Partner Sales, Solutions Architect Migrations** — already on board via salesforce-careers / LinkedIn / Workday mirrors.
- **Rogers — Sr Business Systems Analyst, ServiceNow platform (ITSM), Brampton (wct-fct req 317411)** — page returns "This job is no longer accepting applications"; excluded. jobs.rogers.com Technology list (21 roles, newest Nov 7) shows no SN/SF technical role; Lead Management Operations (Salesforce, ~Oct 28) outside freshness window.
- **Bell — ServiceNow System Administrator (432824), Senior Technical Advisor (432829), Developer/Integrator** — jobs.bell.ca returns "has been filled"; excluded. Filled roles never enter the board.
- **BMO — Junior Salesforce Administrator, Fall 2026 Co-op/Internship (Toronto)** — jobs.bmo.com says "has been filled" and the posting's application deadline (05/29/2026) has passed; expired, excluded.
- **Caseware — Salesforce Engineer, Toronto hybrid, $100K–115K, PD1 required** — surfaced only via Jooble aggregator; no direct caseware.com careers URL with a verifiable posted date; not in jobs.json. Not merged: mid-level (3–5+ yrs) and unverifiable date. Re-check via careers.caseware.com ATS deep-link on a future run.
- **jobs.gc.ca (Government of Canada)** — zero direct ServiceNow/Salesforce Toronto postings; GC platform work arrives via ServiceNow Canada Protected B roles and prime vendors (Accenture, Deloitte, KPMG, CGI, Ateko/Bell), all already mirrored.
- **Partners / Elite Partners** — Accenture ServiceNow Technical Architect Toronto (posted 2026-11-06), Deloitte Senior Consultant ServiceNow Platform Toronto, KPMG ServiceNow consultant roles (Toronto/Ottawa/Vancouver/Montreal), CGI ServiceNow Administrator/Developer — all already on the board via LinkedIn/Workday mirrors dated 2026-11-08/09; no net-new adds.

### Patterns / lessons (09:00 run)

1. **Late-window hourly runs return zero fresh jobs** — the 13:33 UTC jobs.json refresh already captured 635 postings from SmartRecruiters, Workday, Greenhouse, Lever, Ashby, LinkedIn guest and Adzuna Canada; aggregator and web-search hits are mirrors of rows already in the feed.
2. **Dedupe by canonical URL, not aggregator URL** — Lane Four's jobs.ca mirror was absent from jobs.json, but its canonical lanefour.com posting was present; normalizing domain+path caught the duplicate.
3. **Filled/closed pages retire roles** — Rogers wct-fct ("no longer accepting applications"), Bell jobs.bell.ca ("has been filled") and BMO's filled Junior Salesforce Administrator co-op were all verified closed and excluded; never add filled roles.
4. **Aggregator-only roles can't be merged** — Caseware's Salesforce Engineer exists only on Jooble with no extractable posted date; the merger requires an absolute YYYY-MM-DD and a resolvable direct URL.
5. **jobs.gc.ca returns zero direct SN/SF Toronto roles** — government platform work surfaces via ServiceNow's Canada Protected B requisitions and prime vendors, already mirrored on the board.

### Files touched (09:00 run)

- `JOBLESSONS_2026-11-09.MD` — this file, 09:00 EST section added (this run).
- `README.md` — no changes (zero net-new jobs; counts unchanged).
- `jobs.json` / `public/` — no changes; no rebuild or redeploy required this hour.

## Hourly scan — 2026-11-09 10:00 EST (15:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 10:00 EST (15:00 UTC) |
| Baseline (jobs.json on main) | 5,037 unique URLs · scrapedAt 2026-11-09T14:13:24Z (09:13 EST) · newThisScan 652 · primaryCounts SN 1,061 / SF 1,026 |
| Baseline (README.md tables on main) | "as of 2026-11-09" · window 2026-10-10 → 2026-11-09 · 5,413 live postings (SN 718 · SF 877 · Other 3,818) · deduplicated by URL |
| Dedupe baseline | 5,939 unique URLs (README.md table URLs + jobs.json URLs; normalized by stripping query strings and trailing slashes) |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs rebuilt on GitHub Pages (public/) | 0 (no changes required; board already current from the 09:13 EST automated scan) |

### Sources queried
Indeed.ca, ca.linkedin.com, jobbank.gc.ca, ServiceNow Careers Ontario (careers.servicenow.com), Salesforce Careers Canada, jobs.rogers.com, jobs.bell.ca, jobs.gc.ca, plus targeted site: queries against myworkdayjobs.com / greenhouse.io / lever.co / ashbyhq.com. Employer/partner checks: Accenture, Deloitte, KPMG, CGI, BDO, Capgemini, TELUS, RBC, Scotiabank, BMO, TD, CIBC, Lane Four, Altus Group, Winobell, Robinhood, Take-Two, Long View.

### Candidates reviewed (disposition)
- **KPMG — Senior Consultant, ServiceNow (ITAM/ITOM), Toronto, 2026-11-09** (LinkedIn 4454522998): in jobs.json feed, but KPMG already has 8+ mirror entries on the board; LinkedIn page is a login wall so the date isn't independently verifiable. Skipped — duplicate requisition cluster, no net-new card value.
- **BDO — ServiceNow Senior Developer, Toronto, $84–128K** (Indeed jk=c956b22cc281049c): Indeed/Glassdoor mirrors only, "30+ days ago" / ~Nov 4; Indeed blocked to extraction so no employer-page date. Not fresh, not verifiable → lead only.
- **Lane Four — Salesforce Administrator, Toronto, entry level (0–2 yrs)** (lanefour.com/job-posting/salesforce-administrator/): page live but carries only template dates (datePublished 2026-06-01, dateModified 2026-09-01); no posting date on the page. House rule (set 08:00 run): undated employer pages cannot be merged → lead only, re-check if a date appears.
- **Winobell — Salesforce Developer (Dealer Services), Toronto hybrid**: page live, no posted date → cannot merge; a different Winobell role (Health Cloud, 2026-11-08) is already on the board.
- **MAP/WPP — Senior Salesforce Marketing Cloud Developer, Toronto** (job-boards.greenhouse.io/map/jobs/8396722002): Greenhouse board page shows no posted date → skipped per undated rule.
- **Electric Mind — Senior Full Stack Developer - Salesforce (Contract)**: Lever URL returns HTTP 404 (true dead); role already on board via LinkedIn/adzuna mirrors dated 2026-10-29/30 → skip.
- **Take-Two — Senior Lead ServiceNow ITOM, Toronto**: already on board since 2026-10-22 (greenhouse 8306166); reposted, dates conflict (8–16 days ago) → duplicate.
- **ServiceNow Careers Toronto** (Staff Systems Engineer/SRE/Security Engineer, Nov 5–6): all on board via careers.servicenow.com / jobs.smartrecruiters.com mirrors → duplicates.
- **Rogers / Bell / jobs.gc.ca**: Rogers Technology list (21 roles, newest Nov 7) has no SN/SF technical role; Bell SN/SF pages return "has been filled"; jobs.gc.ca zero SN/SF Toronto hits → nothing added. Filled/expired roles never enter the board.
- **Indeed/simplyhired/adzuna mirrors** (Altus Group SF Platform Developer, Applied Systems Associate SF Admin, Deloitte SC Salesforce Platform, Veracity/TEEMA SN Toronto): aggregator-only URLs, roles already mirrored on the board under employer/LinkedIn URLs → duplicates by requisition, skipped.

### Patterns / lessons (10:00 run)
1. **Zero-fresh runs are the norm late in the daily monitoring window.** The 09:13 EST jobs.json refresh captured 652 postings from SmartRecruiters, Workday, Greenhouse, Lever, Ashby, LinkedIn guest and Adzuna Canada; every date-verifiable Toronto SN/SF role is already mirrored on the board. Expect 0–2 merges per hour at this cadence.
2. **House rule holds: no absolute posted date on the employer page = no merge.** Lane Four's entry-level Salesforce Administrator (exactly the target profile) and Winobell's Salesforce Developer (Dealer Services) are live and Toronto-based but undated on their own pages, so they stay leads, not board rows. jobs.json's observed date is not a substitute for the page-sourced date the merger requires.
3. **404 ≠ "maybe":** Electric Mind's Lever URL is a true 404 (dropped); Robinhood's Greenhouse API returns "Job not found" for job 7014467 even though it's listed on the board page. Don't re-probe dead endpoints each run.
4. **Indeed.ca is a mirror, not a source:** BDO's ServiceNow Senior Developer ($84–128K Toronto) is visible on Indeed/Glassdoor but Indeed is blocked to extraction and Glassdoor shows "30+ days ago" — no employer-page verification possible. Lead only.
5. **Dedupe baseline is 5,939 normalized URLs.** The same requisition arrives via LinkedIn, adzuna, simplyhired and the employer ATS under different URLs; dedupe by normalized URL (strip query strings/trailing slashes) before any merge.

### Files touched (10:00 run)
- `JOBLESSONS_2026-11-09.MD` — this file, 10:00 EST section added, committed to repo root on main.
- `README.md` — no changes (zero verified fresh jobs this hour; counts unchanged: 5,413 live postings).
- `jobs.json` / `public/` — no changes; no rebuild or redeploy required this hour (last deploy from the 09:13 EST scan).


## Hourly scan — 2026-11-09 11:00 EST (16:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 11:00 EST (16:00 UTC) |
| jobs.json baseline on main | 5,037 unique URLs · scrapedAt 2026-11-09T14:13:24Z (09:13 EST) · newThisScan 652 · primaryCounts SN 1,061 / SF 1,026 |
| Baseline (README.md tables on main) | 5,413 live postings · ServiceNow 718 · Salesforce 877 · Other 3,818 · window 2026-10-10 → 2026-11-09 |
| GitHub Pages (public/) | 4,512 indexed jobs (servicenow 763, salesforce 802, other 2,947); pages.yml redeploys on push to main |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs rebuilt on GitHub Pages (public/) | 0 (no changes required; board already current this hour) |

### Sources queried
Indeed.ca, ca.linkedin.com, jobbank.gc.ca, ServiceNow Careers Ontario (careers.servicenow.com), Salesforce Careers Canada (careers.salesforce.com), jobs.rogers.com, jobs.bell.ca, jobs.gc.ca; targeted site: queries against myworkdayjobs.com / greenhouse.io / lever.co / ashbyhq.com. Employer/partner checks: Accenture, Deloitte, KPMG, CGI, BDO, Capgemini, TELUS, RBC, Scotiabank, BMO, TD, CIBC, Lane Four, Altus Group.

### Candidates reviewed (disposition)
- **Scotiabank — ServiceNow Developer, Toronto, req 260518** (jobs.scotiabank.com/job/Toronto-ServiceNow-Developer-ON-M5H-1H1/603030017/): page verified live, but URL already on board in jobs.json and README.md → duplicate, skipped.
- **Scotiabank — Salesforce Developer, Enterprise Crisis & Business Continuity Management, Toronto, req 269305** (.../604841417/): page returns "currently not accepting any further applicants" → closed/filled; never added. Not on board, and closed so excluded.
- **ServiceNow Careers Toronto (Nov 05–06)** — Staff Systems Engineer (JB0073788), Staff Security Engineer \| Security Engineering (JB0076454), Senior Staff Security Engineer \| Systems Engineering (JB0076457), Staff Security Engineer \| Enterprise Security (JB0076455), Staff Site Reliability Engineer Canada Protected B (JB0076847), Senior Site Reliability Engineer Canada Protected B (JB0076846): all already on board via careers.servicenow.com / jobs.smartrecruiters.com mirrors → duplicates.
- **Salesforce Careers Canada** — Manager, Sales Development Canada (jr336458) already on board; remaining Toronto hits are non-SN/SF or lack verifiable posted dates → skipped.
- **Indeed.ca / LinkedIn.ca ServiceNow/Salesforce Toronto hits** — KPMG (×8), CGI, Lightspeed, BMO SAM Administrator–ITAM, Robert Half, Moneris, Panasonic Canada, Survalent, Altus Group, CloudKettle, SS&C, iVedha, Minto, Atlantic Packaging, Veracity Ventures: aggregator listing pages with no extractable absolute posted date and no resolvable direct posting URL → lead only, not merged (merger requires YYYY-MM-DD + direct employer URL).
- **Rogers** (jobs.rogers.com Greenhouse, 21 Technology roles, newest Nov 7): no SN/SF technical role; Lead Management Operations (Salesforce, ~Oct 28) outside freshness window → nothing added.
- **Bell** (jobs.bell.ca Phenom) — ServiceNow System Administrator 432824, Senior Technical Advisor 432829, Developer/Integrator: all return "has been filled" → excluded. Filled roles never enter the board.
- **jobs.gc.ca / Canada.ca**: zero direct ServiceNow/Salesforce Toronto postings → nothing added.

### Patterns / lessons (11:00 run)
1. **Zero-fresh runs remain the norm late in the daily window** — the 09:13 EST jobs.json refresh captured 652 postings; every date-verifiable Toronto SN/SF role this hour's searches surfaced is either already on the board or a closed aggregator mirror.
2. **Page-level verification catches closed roles before merge** — Scotiabank's Salesforce Developer req 269305 looked fresh in the search index, but its own page says "not accepting any further applicants"; house rule (filled/closed never enter the board) held.
3. **Indeed.ca is a mirror, not a source** — ~14 partner postings carried no extractable posted date and no direct employer URL; the merger's date + direct-URL gate rejected them all, as in prior runs.
4. **Filled/closed roles stay out and stop being re-checked** — Bell SN/SF roles ("has been filled") and Scotiabank req 269305 are recorded dead in this scan.
5. **Dedupe baseline ~5,939 normalized URLs** (README.md table URLs + jobs.json URLs; strip query strings and trailing slashes). The same requisition arrives via LinkedIn, adzuna, simplyhired and the employer ATS under different URLs.

### Files touched (11:00 run)
- `JOBLESSONS_2026-11-09.MD` — this file, 11:00 EST section added; committed to repo root on main.
- `README.md` — no changes (zero verified fresh jobs; counts unchanged).
- `jobs.json` / `public/` — no changes; no rebuild or redeploy required this hour.
---

## Hourly scan — 12:00 EST (2026-11-09)

Ran as the scheduled 12:00 EST cron scan. 
Hourly ServiceNow / Salesforce job scan for Toronto/GTA/Canada — {NOW.date()}.

## What ran
- `scripts/daily_job_scan.mjs`: SmartRecruiters (ServiceNow), Workday CXS (Salesforce/BMO/TD/BDO/CAAT/...), Greenhouse, Lever, Ashby, LinkedIn guest (`f_TPR=r86400` fresh pass), RemoteOK, Jobicy, Remotive, Adzuna Canada (24 Toronto/Canada queries incl. Ottawa, Mississauga).
- `tools/verify_links.py --days 2`: liveness gate, 404/410/451 = dead; 403/429/5xx = kept (bot walls).
- `tools/build_site.py`: regenerated `public/jobs-data.json` + `public/index.html`.

## Results this hour
- Fresh postings discovered: {len(fresh)}
- Verified-dead postings dropped: {len(DEAD_DROP)}
- Board on main: {len(remote_jobs)} -> {len(merged_jobs)} listings (non-destructive union; nothing already listed was removed)
- ServiceNow: {payload['meta']['primaryCounts']['servicenow']} | Salesforce: {payload['meta']['primaryCounts']['salesforce']}

## Notable fresh Toronto / partner / public-sector hits
- ServiceNow: TD (Sr. IT Developer), BMO (SAM Administrator - ITAM), CIBC (ServiceNow Developer), 407 ETR (System Developer Contract), Interac Corp., Tech Mahindra, KPMG Canada (Consultant / Senior Technical Consultant across Toronto/Ottawa/Halifax/Calgary/Vancouver), Accenture (ServiceNow Technical Architect, Toronto), CGI (Lead ServiceNow Architecture Consultant, Calgary), MNP (Senior SN Developer & Administrator, Calgary), UST (ITSM Service/Process Owner, Remote Canada), GDIT (ServiceNow Developer SME, Remote), TELUS Digital (Remote Canada), Brookfield Properties (Contract, Toronto), BDO Canada (Senior Developer, Toronto), CAAT Pension Plan (ServiceNow Developer Hybrid, Toronto).
- Salesforce: CGI (Senior Salesforce Developer, Toronto), Smart IT Frame LLC (Technical Architect CPQ/RCA x2, Ontario), Enterprise Solutions Inc. (Data Cloud Architect, Technical Architect, Toronto), Altus Group (Platform Developer), Webflow (Senior SF Developer, LaSalle), WPP/Map (Marketing Cloud Developer, Toronto), Winobell (Salesforce Dealer Services), City of Toronto (Corporate Application Technical Leader, Senior Systems Integrator), TD (Salesforce & nCino Solutions Design IT Specialist), iA Financial Group, Salesforce careers (Customer Success Manager MuleSoft Public Sector, Toronto), Deloitte (Senior Consultant SF Platform DTC), CloudKettle (Revenue Cloud Architect), OSI Digital (Salesforce Lead), PwC (Senior Associate SF BA).
- Partners/Elite Partners seen: Accenture, Deloitte, KPMG, CGI, Crossfuze, NewRocket, Slalom, NeuraFlash, OSI Digital, CloudKettle.
- Public sector / crown: City of Toronto, University of Toronto, CAAT Pension Plan, OMERS, CMHC (gc.ca careers), Export Development Canada, Trillium Health Partners.

## Gaps / watch items
- Rogers: no ServiceNow/Salesforce hits this hour (careers.rogers.com not surfaced by Adzuna/LinkedIn guest) — try site:rogers.com / careers.rogers.com directly next run.
- Bell: confirmed hits via Adzuna/LinkedIn (Conseiller technique principal ServiceNow Toronto; Senior ServiceNow Architect Toronto) — Ateko (backed by Bell Canada) also recurring.
- jobs.ca / Eluta / Indeed links frequently resolve to employer hub pages rather than postings — `is_listing_url()` filter must apply at render time, not just at sync time.
- LinkedIn guest endpoint returned 256 cards this run (previously 403-walled); the `f_TPR=r86400` 24h pass is the most reliable freshness filter.
- GitHub's own `hourly-scan.yml` Action commits directly to `main` at :00 UTC and races this cron — all writes here use Contents-API `sha` + retry-on-409; the Action rebases on reject, so no data loss expected.
- `dead_urls.txt` now lists {len(merged_dead)} blocked URLs; build honors `dead_url_keys()` so dead rows never render even if present in jobs.json.

## Files touched
jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json, public/jobs-data.json, public/index.html, README.md (DAILY-SCAN block), dead_urls.txt, FRESH_JOBS.md.

## Hourly scan — 2026-11-09 13:00 EST (18:00 UTC)

| Metric | Value |
|---|---|
| Run time | 2026-11-09 13:00 EST (18:00 UTC) |
| jobs.json baseline | 5,037 unique URLs on HEAD (09:13 EST scan); working tree refreshed by the 12:17 EST automated scan to 5,081 unique URLs (scrapedAt 2026-11-09T17:17:18Z, newThisScan 45, sources: adzuna 27, linkedin 15, workday 2, smartrecruiters 1) |
| Baseline (README.md tables on main) | "as of 2026-11-09" · window 2026-10-10 → 2026-11-09 · 5,413 live postings (SN 718 · SF 877 · Other 3,818) · deduplicated by URL |
| GitHub Pages (public/) | rebuilt at 18:06 UTC via `python3 tools/build_site.py`: 4,516 indexed jobs (servicenow 763, salesforce 805, other 2,948) · 684 duplicate mirrors collapsed · 40 applied hidden · newest 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md tables | 0 |
| Jobs rebuilt on GitHub Pages (public/) | rebuilt (4,516 jobs); pages.yml redeploys on push to main |

### Sources queried
Indeed.ca, ca.linkedin.com, jobbank.gc.ca, ServiceNow Careers Ontario (careers.servicenow.com), Salesforce Careers Canada (careers.salesforce.com), jobs.rogers.com, jobs.bell.ca, jobs.gc.ca; targeted `site:` queries against myworkdayjobs.com / greenhouse.io / lever.co / ashbyhq.com. Employer / Elite Partner checks: Accenture, Deloitte, KPMG, CGI, Capgemini, BDO, TELUS, RBC, Scotiabank, BMO, TD, CIBC, Lane Four, Altus Group, Fidelity Canada, MSCI.

### Candidates reviewed (disposition)
- **Scotiabank — ServiceNow Solutions Architect - Platform Integration** (Toronto, hybrid, req 224687; https://jobs.scotiabank.com/job/Toronto-ServiceNow-Solutions-Architect-Platform-Integration-1-ON-T3R0S4/591952717/; LinkedIn mirror 4221477571): employer page returns "We are currently not accepting any further applicants for this role" → closed/filled; never added. URL was not previously on the board (no duplicate), but closed roles never enter the board.
- **Fidelity Canada — Software Developer (Salesforce)** (Toronto, 100% remote; LinkedIn 4113195999): LinkedIn page is a login wall (HTTP 422); no extractable posted date → undated, cannot merge per house rule. Lead only.
- **MSCI Inc. — Senior Salesforce Solution Engineer** (Toronto; LinkedIn 4116713739): login wall, no verifiable posted date → lead only.
- **ServiceNow Careers Toronto** (Staff Systems Engineer / SRE / Security Engineer Canada Protected B, Nov 05–06): already on the board via careers.servicenow.com / jobs.smartrecruiters.com mirrors → duplicates.
- **Salesforce Careers Canada** — Manager, Sales Development Canada already on the board; remaining Toronto hits non-SN/SF or undated → skipped.
- **Indeed.ca / LinkedIn.ca ServiceNow/Salesforce Toronto hits** (KPMG ×8, CGI, Lightspeed, BMO SAM Administrator–ITAM, Robert Half, Moneris, Panasonic Canada, Survalent, Altus Group, CloudKettle, SS&C, iVedha, Minto, Atlantic Packaging, Veracity Ventures): aggregator listing pages with no extractable absolute posted date and no resolvable direct posting URL → lead only, not merged.
- **Rogers** (jobs.rogers.com Greenhouse, 21 Technology roles, newest Nov 7): no SN/SF technical role; Lead Management Operations (Salesforce, ~Oct 28) outside the freshness window → nothing added.
- **Bell** (jobs.bell.ca Phenom): ServiceNow System Administrator 432824, Senior Technical Advisor 432829, Developer/Integrator → "has been filled"; excluded. Filled roles never enter the board.
- **jobs.gc.ca / Canada.ca**: zero direct ServiceNow/Salesforce Toronto postings → nothing added.
- **Partners / Elite Partners** — Accenture ServiceNow Technical Architect Toronto (posted 2026-11-06), Deloitte Senior Consultant ServiceNow Platform Toronto, KPMG ServiceNow consultant roles (Toronto/Ottawa/Vancouver/Montreal), CGI ServiceNow Administrator/Developer — all already on the board via LinkedIn/Workday mirrors dated 2026-11-08/09; no net-new adds.

### Patterns / lessons (13:00 run)
1. **Zero-fresh runs remain the norm late in the daily window** — the 12:17 EST jobs.json refresh captured 45 postings; every date-verifiable Toronto SN/SF role this hour's searches surfaced is either already on the board, a closed aggregator mirror, or undated.
2. **Employer-page liveness beats the search index** — Scotiabank's req 224687 looked fresh in search results ("Posted yesterday" via TheLadders) but its own page says "not accepting any further applicants"; the filled/closed rule held before any merge.
3. **LinkedIn is a login wall (HTTP 422) at extraction time** — posting dates can't be verified from the page; no LinkedIn-sourced role added without a verifiable date (Fidelity, MSCI stayed leads).
4. **Filled/closed roles stay out and stop being re-checked** — Bell SN/SF roles and Scotiabank req 224687 recorded dead in this scan.
5. **Dedupe baseline ~5,939 normalized URLs** (README.md table URLs + jobs.json URLs; strip query strings and trailing slashes); the same requisition arrives via LinkedIn, adzuna, simplyhired and the employer ATS under different URLs.

### Files touched (13:00 run)
- `JOBLESSONS_2026-11-09.MD` — this file, 13:00 EST section added.
- `README.md` — no net-new table rows (counts unchanged: 5,413 live postings); working tree carries the 12:17 EST automated scan's DAILY-SCAN section (45 fresh postings), committed with this hour's jobs refresh.
- `jobs.json` — refreshed by the 12:17 EST automated scan to 5,081 unique URLs; committed with this hour's refresh.
- `public/` (GitHub Pages) — rebuilt with `python3 tools/build_site.py` (4,516 indexed jobs); pages.yml redeploys on push to main.
- `dead_urls.txt` — unchanged this hour (no new dead URLs confirmed).



## 2026-11-09 hourly scan (14:00 EST / 19:00 UTC) — Hermes cron

**Scope:** fresh Toronto ServiceNow / Salesforce jobs; emphasis entry-level / Platform Admin / Platform Developer I; partners (Accenture, Deloitte, KPMG, Capgemini, CGI), Rogers/Bell/Telus, Canadian government.

**Result:** 2 verified jobs added to jobs.json + README.md + public/ (commits jobs.json 333a163c, README.md 41308133, public/jobs-data.json c6f3a2a5, public/index.html 19dded41):
- KPMG Senior Technical Consultant, ServiceNow Developer — careers.kpmg.ca/jobs/33533 — Toronto/multi-location — 4-6 yrs — $77K-$102K CAD — verifyState live
- KPMG Consultant/Senior Consultant - ServiceNow Solution Developer — careers.kpmg.ca/jobs/33919 — Toronto/multi-location — 3+ yrs, CSA — $70K-$102K CAD — verifyState live

**Entry-level gap:** no Junior ServiceNow Administrator or Salesforce Platform Developer I roles surfaced Toronto-wide this cycle. Market is Staff/Senior-heavy (ServiceNow: Staff Security Engineer/Systems Engineer/SRE at ServiceNow direct; Salesforce: senior developers at Moneris, Altus Group, RBC, Scotiabank — all already on board or verified duplicates).

**Already on board — dedupe hits, not re-added:** KPMG Consultant ServiceNow Developer (careers.kpmg.ca/professionals/jobs/33530; LinkedIn variants ...4454532959/...4454544021), Moneris Principle Salesforce Developer (workday JR106006), Altus Group Salesforce Platform Developer (simplyhired), Deloitte Salesforce Developer Digital Customer (careers.deloitte.ca 135279), Deloitte Senior Consultant ServiceNow Platform (req 133759), BMO ServiceNow SAM Administrator - ITAM, TD Sr. IT Developer ServiceNow.

**Timing:** the repo's own hourly scan ran at 18:45 UTC (jobs.json meta scrapedAt 2026-11-09T18:45:11Z, +736 newThisScan); this cron ran immediately after, so incremental surface area was thin. No Contents-API 409 conflicts this run.

**Verification notes:** company ATS pages (careers.kpmg.ca, careers.deloitte.ca, myworkdayjobs) load server-side and verify cleanly. Indeed/LinkedIn HTML are walled: Indeed viewjob returned Cloudflare "Request Blocked" (CGI ServiceNow Administrator/Developer jk=cf4ffdcf78006e60 NOT added — unverified). jobs.ca/LinkedIn hub URLs (`/<company>` without `/jobs/`) are listing URLs — excluded by `is_listing_url`. GCjobs site search returned nothing for ServiceNow/Salesforce Toronto.

**Next-cycle suggestions:** search satellite GTA cities (Markham, Mississauga, Vaughan, Etobicoke); jobbank.gc.ca ServiceNow/Salesforce; partner career pages directly (Accenture, Capgemini); retry Indeed via browser with cookies when Cloudflare clears.




## Hermes hourly scan — 2026-11-09 15:00 EST

13 verified fresh Toronto ServiceNow/Salesforce jobs merged (jobs.json 5146 → 5159; README tables ServiceNow 731→739, Salesforce 916→920; public/ rebuilt and live).

**Sources that worked:** employer career boards first — careers.servicenow.com, careers.salesforce.com, jobs.scotiabank.com, careers.ibm.com, careers.deloitte.ca, builtin.com, LinkedIn. Use the employer-board URL as the primary row; aggregator mirrors (Adzuna/Indeed/LinkedIn jobs) lag and duplicate — normalized-URL dedupe catches the repeats.

**Dedupe rule:** strip query string, trailing slash, lowercase before comparing to jobs.json URLs. Skipped 3 already on the board: Accenture R00267230/R00267231, Deloitte 135279 (present under mirror URLs).

**Liveness gate:** only 404/410/451 = dead. careers.servicenow.com returns 405 to HEAD; Salesforce/Accenture/IBM return 403/402 bot-wall — those were kept. Bell.ca ServiceNow postings returned "position filled" (dead). Rogers site-search returned no fresh postings.

**README window:** tables cover the last 30 days. Deloitte Senior Consultant, Salesforce Platform (posted 2026-07-09) went to jobs.json only, not the README tables.

**Government:** jobs.canada.ca site-search returned nothing; public-sector-adjacent hits were ServiceNow Protected B roles and banking (Scotiabank/TD).

**Junior/Platform focus:** Capco and Deloitte postings cite Salesforce Platform Developer I / ADM 201 — keep scanning those boards weekly for entry-level / Platform Admin / Platform Developer I adds.

**Build:** tools/build_site.py regenerates public/jobs-data.json + public/index.html; keep public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json byte-identical to jobs.json.

## Hermes hourly scan — 2026-11-09 16:00 EST

2 verified fresh Toronto-area Salesforce jobs merged (jobs.json 5,150 → 5,152; README tables Salesforce 922 → 924; total 5,630 → 5,632; public/ rebuilt and live). Zero new ServiceNow roles this cycle — every ServiceNow hit (KPMG x2, Accenture Technical Architect, BMO ServiceNow SAM Administrator - ITAM, ServiceNow direct Staff SRE/Systems Engineer) was already on the board from earlier today's scans.

**Added:**
- Salesforce Developer — Hays — Greater Toronto Area, Canada — posted 2026-11-09 (~45 minutes ago) — via LinkedIn guest API — https://ca.linkedin.com/jobs/view/salesforce-developer-at-hays-4489123880 — verifyState live
- Certinia PSA Architect - Senior Principal — Slalom — Greater Toronto Area, Canada — posted 2026-11-09 (~1 hour ago) — via LinkedIn guest API — https://ca.linkedin.com/jobs/view/certinia-psa-architect-senior-principal-at-slalom-4487961045 — Salesforce-ecosystem PSA (Certinia/FinancialForce on Salesforce); borderline include, flagged in row source note

**Sources that worked:** LinkedIn guest API (jobs-guest seeMoreJobPostings, last 24h, Toronto, sort by date) — 196 cards across 11 keyword × page sweeps (ServiceNow, Salesforce, ServiceNow/Salesforce Administrator, Platform Developer, ServiceNow/Salesforce Developer, ServiceNow/Salesforce Ottawa, Rogers, Bell Canada); 114 already on board; 82 new overall; 2 verified SN/SF-relevant.

**Sources that yielded nothing new:** Indeed.ca (search pages load but /viewjob links are Cloudflare-cloaked /rc/clk redirects — no extractable direct postings; do not rely on), jobs.canada.ca / jobs.gc.ca site search (zero ServiceNow/Salesforce Toronto hits), Rogers.ca / Bell.ca site search (no fresh SN/SF technical roles; Bell's ServiceNow/Systems Admin postings return "position filled").

**Already on board — dedupe hits, not re-added:** all ServiceNow roles from KPMG, Accenture, BMO, ServiceNow direct already present (verified against the 7,398-URL set in README.md + jobs.json).

**Entry-level gap:** no Junior ServiceNow Administrator or Salesforce Platform Developer I roles surfaced Toronto-wide this cycle; market remains Staff/Senior-heavy.

**Patterns / lessons for future agents:**
- LinkedIn guest API cards carry date-only `datetime` plus relative age ("45 minutes ago") — use the relative age as posted date; never add a LinkedIn row without a verifiable date on the card.
- Dedupe by normalized URL (strip query string, trailing slash, lowercase) across both README.md tables and jobs.json.
- public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json must stay byte-identical to jobs.json.
- Run tools/build_site.py locally to regenerate public/jobs-data.json + public/index.html before committing; pages.yml redeploys GitHub Pages on any push to public/** or README.md.
- Race: the repo's own hourly-scan Action commits at :00 UTC (21:00 UTC = this run's wall time) — use the git REST API (blobs → tree → commit → ref update) with retry on 409; never git.exe on this host (blocked).

**Files touched:** JOBLESSONS_2026-11-09.MD (this file), README.md, jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json, public/jobs-data.json, public/index.html.

## 2026-11-09 17:00 EST cron run (hermes scan, merged as 22e8748)

Scope: fresh Toronto/GTA + Canada ServiceNow and Salesforce roles; dedupe against README.md + APPLIED.md; merge to README tables and GitHub Pages.

- `scripts/daily_job_scan.mjs` (no playwright): 682 fresh postings, merged into jobs.json → 5,195 total after sync_readme_to_jobs. Sources: LinkedIn guest 296, Adzuna 334, LinkedIn-heavy morning cycles by peers had already merged most linkedin/KPMG/BMO/Scotiabank/TD roles — dedupe caught them; net-new from this run: 14 rows.
- Net-new rows added to README tables (ServiceNow 736→737, Salesforce 924→937; site rebuilt: 4,663 jobs, newest 2026-11-09):
  * ServiceNow: BDO Senior Developer, Toronto (indeed).
  * Salesforce: Lane Four Administrator, Toronto; Altus Group Platform Developer, Toronto; Applied Systems Associate Administrator, remote Canada; WPP (Map) Senior Marketing Cloud Developer; Electric Mind Full Stack Developer contract; Apptoza ×3 (Toronto); Winobell Dealer Services, Toronto; iA Financial, Montreal; Nityo Infotech, remote Canada; OSI Digital Lead, Toronto/Ottawa.
- No entry-level Platform Developer I / junior Platform Administrator surfaced this cycle; Lane Four Administrator and Applied Systems Associate Administrator are the closest matches.
- Employer probes: jobs.bell.ca ServiceNow postings all show "position filled" (skip); careers.rogers.com returned nothing; telus.com surfaces only CRM-user sales roles, no platform postings; jobs.gc.ca/Job Bank blocked to plain fetch — keep using scripts/canada_index_sweep.py::jobbank_page instead of direct fetch.
- verify_links.py --days 2: 121 new rows probed, 0 dropped; 5 pre-existing dead rows removed (incl. BMO via Procom Senior Salesforce Developer 404, previously flagged by the round-4 audit).
- Repo remote moved: https://github.com/eltonaguiar/BESTIEJOB.git (old bestiejob.git still redirects). Pages serves eltonaguiar.github.io/BESTIEJOB/ from committed public/ — editing jobs.json alone never reaches the page; build_site.py must run after every README/jobs.json change.

## Hermes hourly scan — 2026-11-09 18:00 EST (cron)

**Scope:** fresh Toronto/GTA + Canada ServiceNow and Salesforce roles; emphasis entry-level / Platform Admin / Platform Developer I; partners (Accenture, Deloitte, KPMG, Capgemini, CGI), Rogers/Bell/Telus, Canadian government.

**Result:** 0 verified fresh jobs merged (jobs.json 5,202 rows unchanged; README tables unchanged — ServiceNow 738, Salesforce 941, Other 3,973 = 5,652 live postings; public/ unchanged, no rebuild required).

**Candidates reviewed:**
- Four Seasons — ServiceNow Administrator - Junior (Toronto, hybrid) — Built In page: posting removed 2025-10-01 08:21 UTC; dead, excluded. Indeed's "1 day ago" tag is unreliable.
- SS&C Technologies — Salesforce Implementation Consultant & Platform Administrator (Toronto, listed Nov 4) — already on board via adzuna.ca/details/5954045892 (posted 2026-11-05); not fresh, not re-added.
- Lane Four — Salesforce Administrator (Toronto, 0–2 yrs) — already on board, merged in today's 17:00 EST run (lanefour.com/job-posting/salesforce-administrator/).
- FloQast — Salesforce Administrator (Toronto, LinkedIn 4214676357) — LinkedIn login wall, date unverifiable; already on board; not added.
- ServiceNow Careers Toronto — Staff Systems Engineer / Senior Staff Security Engineer ×2 / Senior/Staff SRE Canada Protected B (Nov 05–06) all already on board; Nov 09 postings (Sales Director, Sr CRM Account Executive) are sales roles, excluded by title rule.
- Rogers — Lead Management Operations (Salesforce, posted ~Oct 28) outside freshness window; careers.rogers.com no fresh SN/SF technical roles.
- Bell — ServiceNow postings return "position filled"; filled roles never enter the board.
- Telus — CRM-user/sales account roles only, no platform postings.
- Government of Canada / jobs.gc.ca / Job Bank — zero ServiceNow/Salesforce Toronto hits.
- Partners — Accenture/Deloitte/KPMG/Capgemini: no fresh entry-level Platform Admin/Developer I hits; Deloitte roles surfaced carry Oct 2025–Oct 2026 start dates, non-entry-level.

**Verification notes:** Indeed/LinkedIn/Jobs.ca HTML are login-walled or Cloudflare-cloaked (HTTP 422/403); posting dates not verifiable there — no LinkedIn-sourced role added without a verifiable date. Employer career pages (ServiceNow, Scotiabank, BMO, KPMG, Lane Four) load server-side and verify cleanly.

**Already on board — dedupe hits, not re-added:** all 75 jobs.json rows posted 2026-11-09 with SN/SF titles are already represented in README tables; combined dedupe baseline 6,171 unique URLs (jobs.json 5,202 + README 5,466 + APPLIED.md 17).

**Entry-level gap:** no Junior ServiceNow Administrator or Salesforce Platform Developer I roles newly surfaced Toronto-wide this cycle; market remains Staff/Senior-heavy.

**Patterns / lessons for future agents:**
1. By 18:00 EST on a scan day, incremental surface area is thin — earlier same-day runs (14:00–17:00 EST) already captured the day's fresh SN/SF postings; zero-merge hours are the norm late in the daily window.
2. Aggregator "posted 1 day ago" tags (Indeed) are unreliable — always verify on the employer page (Four Seasons case: dead since Oct 2025).
3. Dedupe against jobs.json + README.md table URLs + APPLIED.md before adding; normalize URLs (strip query strings, trailing slashes, lowercase).

**Files touched:** JOBLESSONS_2026-11-09.MD (this section only). README.md, jobs.json, public/ — no changes this run.


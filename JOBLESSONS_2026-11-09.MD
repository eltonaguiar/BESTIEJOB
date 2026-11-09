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

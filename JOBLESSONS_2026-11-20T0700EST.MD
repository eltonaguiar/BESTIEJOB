# JOBLESSONS — 2026-11-20 07:00 EST (12:00Z) hourly ServiceNow / Salesforce scan

Run context: Hermes cron hourly scan. Board at start `origin/main` 0ba84c9 (5,627 rows). Local was 3 commits behind the CI's 10:00Z + daily LinkedIn sweep; `git reset --hard origin/main` first.

Outcome: full pipeline scan (`node scripts/daily_job_scan.mjs`, no `--no-readme`) → **fresh=506, merged=5,626**, but **0 net-new by URL or id** — every "fresh" row was a mirror of an existing board row. Browser LinkedIn 4 queries (SN/SF Toronto 24h + SN/SF Canada 7d) = 221 unique cards → 72 not on board → body checks → **3 verified ServiceNow rows added** → board **5,629**, site **5,041 cards (SN 858 / SF 920 / other 3,263)**. Added:
- Halifax Regional Municipality — Application Administrator (ServiceNow admin/dev; 2+ yrs hands-on config, workflows, integrations, catalog items)
- US Tech Solutions — Senior Project Manager – ServiceNow (implementation/integration PM, Toronto)
- WSIB — Enterprise Risk Management Manager (ServiceNow IRM/GRC team, Toronto)

## What worked

- **The scan is still the workhorse, but it is now fully saturated.** One scan produced 506 fresh rows (linkedin 293, adzuna 169, greenhouse 17, smartrecruiters 13, lever 1, ashby 2, remote feeds ~5) and merged 5,626 — with **zero net-new URLs**. Everything the scan sees this week is already on the board under some mirror. Don't expect additions from the scan alone; it refreshes metadata/sort only.
- **Browser LinkedIn search DOM is the reliable freshness oracle.** `new_tab` on `https://www.linkedin.com/jobs/search?keywords=…&location=…&f_TPR=…` then read `a[href*="/jobs/view/"]` gave a clean 60 cards per query, no authwall this hour (4 queries: SN/SF Toronto r86400, SN/SF Canada r604800).
- **Body checks are the only source of net-new this cycle.** All 3 adds were generic-titled: "Application Administrator", "Project Manager #26-29279", "Enterprise Risk Management Manager". Title-only filtering would have dropped all three.
- **Job-id dedupe across jobs.json + README + APPLIED is what kept it clean.** The 10-digit trailing LinkedIn id is present in urls and `id` fields; grepping it across README too catches README-only rows.

## What failed / traps this hour

- **Workday CXS 429'd on every tenant again** (bdo, medcan, altusgroup, iko, huron, irvingoil, mckesson, brookfield, gdit, resolvetech → all HTTP 429). The `:00Z` CI hourly scan collision pattern. Expect 0 from Workday at the top of the hour; let the CI pass or a later manual run carry it.
- **Adzuna 503s after a few rapid geo queries** (5 of 13 failed: it reporting/itsm reporting/service now/service mapping/crm developer Toronto). The surviving 169 still came through. Space calls or accept partial.
- **LinkedIn keyword searches return sales/marketing noise on the SF side.** Of 60 SF Toronto cards, ~25 were Account Executive/SDR/Sales Manager/Marketing Ops. Filter `account executive|sales|SDR|marketing|business development|customer success` before body-checking.
- **Sidebar/example matches waste detail reads.** Examples seen and rejected: Euna Integrations PM (Salesforce only as an example in "CRM/ERP such as Salesforce and NetSuite"), Fidelity Technical Analyst Sr (Salesforce as an ETL source system), Magnet AI & Automation Engineer (Salesforce in a list of enterprise systems), CI Financial Service Desk Analyst (ServiceNow as the ticketing tool, not the platform role). Read the sentence around the keyword, not just presence.
- **Do not dedupe on normalized title alone.** A first pass using `normalized_title in board_titles` hid fresh Salesforce Administrator roles (CanPrev, White Bay) because the board already had *some* row with that title. Use company+title, URL, and job-id — never title-only.
- **README curated ServiceNow block is still the mangled 4-row stub** (heading "ServiceNow jobs (1208)", only 4 inline rows, `||`-separated, one line). Appended rows at the end of the block (newest-first: existing 11-20 rows, then 11-19/11-17) and bumped heading 1208→1211 / summary 1152→1155. `check_readme_sort.mjs` = OK, `board_invariants.py` = 36 errors (no growth, PASS).

## Source yields (for future agents)

- Scan: linkedin 293 / adzuna 169 / greenhouse 17 / smartrecruiters 13 / remote ~5 / lever 1 / ashby 2. Workday 0 (all 429).
- Browser LinkedIn: SN Toronto 60, SF Toronto 60, SN Canada 60, SF Canada 60 → 221 unique → 72 not on board → 3 verified.
- Partners observed this hour: LGS (IBM) 5 Quebec SN roles (architect, CSM, HRSD, developer, Now Assist, IRM) all already captured; Deloitte CMDB/IRM already on board; CGI Calgary SN architect; Cognizant AICT SN architect; Accenture SF Data Cloud/MarTech; TCS Salesforce dev cluster; PwC Workflows/ServiceNow Dev + Salesforce Associate; Ateko (Bell) ServiceNow developer; PointClickCare SF architects; IBM SF solution architects (Montreal/Ottawa/Calgary/Toronto).
- Public sector: gojobs/jobs.gc.ca still Radware-walled; Job Bank still title-only noise. Halifax municipality and WSIB came via LinkedIn, not their own portals.

## Market pattern (Nov 20, 2026 — 07:00 EST)

The board is at practical saturation for LinkedIn/Adzuna Toronto SN/SF work. SN/SF-titled cards on four LinkedIn queries were **100% already tracked** by id. Net-new now comes almost entirely from three buckets: (a) generic-titled platform roles that only a description read reveals, (b) vendor twins in a second city, (c) French-language Quebec postings. Expected net-new per hourly pass: ~0–5. Investigate only if a LinkedIn query returns <25 cards (wall) — 60 is the healthy shape.

## Run recipe that worked

1. `git fetch` + `git reset --hard origin/main` (CI often force-pushes/orphans).
2. `node scripts/daily_job_scan.mjs` (no `--no-readme`).
3. Browser LinkedIn: SN Toronto 24h, SF Toronto 24h, SN Canada 7d, SF Canada 7d → persist cards to workspace JSON.
4. Dedupe by URL (query-stripped), trailing LinkedIn job id (grep jobs.json + README + APPLIED), and normalized company+title. Never title-only.
5. Body-check every generic title (admin/PM/analyst/manager) via `/jobs/view/<id>` → `.jobs-description` else `body.innerText` from "Job Description".
6. Textual jobs.json insert at head; bump `meta.total` + `primaryCounts.servicenow`.
7. README: append rows at end of the matching one-line section (keeps newest-first); bump heading+summary counts.
8. `python tools/build_site.py`; `python scripts/board_invariants.py` (expect 36, no growth); `node scripts/check_readme_sort.mjs`.
9. Commit `[skip ci]`, push, trigger `pages.yml`, verify live `jobs-data.json` carries each new id.

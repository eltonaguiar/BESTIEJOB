# JOBLESSONS — 2026-11-20 06:00 EST (11:00Z) hourly ServiceNow / Salesforce scan

Run context: Hermes cron hourly scan. Board at start `origin/main` ee4c36b (5,585 rows). CI hourly scan also fires at :00Z.

Outcome: full pipeline scan (`node scripts/daily_job_scan.mjs`) → **fresh=542, merged=5,618**, then browser LinkedIn sweeps + body checks added **5 verified rows** (4 ServiceNow, 1 Salesforce) → board 5,623 rows, site 5,037 cards (SN 855 / SF 919 / other 3,263), README header 6,194 live postings. Added:
- Akkodis — Business Analyst – Senior (ServiceNow BA, 12-mo hybrid Toronto)
- G-FORCE IT Services — IT Service Management Consultant (ServiceNow Developer: ITSM/CMDB/Discovery/MID Server)
- Novartis — SFMC Manager (Salesforce Marketing Cloud stack owner, Toronto)
- La Caisse (CDPQ) — Développeur(-euse)- FR (ServiceNow team, Montreal)
- NLB Services — ServiceNow CSM/HRSD/IRM/ITAM/SPM (Calgary; distinct vendor posting from NLB Mississauga)

## What worked

- **The scan itself is still the workhorse.** One `node scripts/daily_job_scan.mjs` (no `--no-readme`) produced 542 fresh rows: linkedin 288, adzuna 210, greenhouse 17, smartrecruiters 13, remoteok/jobicy/remotive 11, lever 1, ashby 2. It rewrites jobs.json, FRESH_JOBS.md and the README `<!-- DAILY-SCAN -->` block in one pass.
- **Browser LinkedIn 24h searches found what the scan's mirror-dedupe hid.** Three queries (`ServiceNow` Toronto r86400, `Salesforce` Toronto r86400, `ServiceNow` Canada r604800) × 60 cards; after URL + job-id + company/title dedupe only 6 candidates were new.
- **Body checks decided 2 of 6 candidates.** Generic titles are still the biggest trap: Akkodis "Business Analyst – Senior" is a ServiceNow BA; G-FORCE "ITSM Consultant" is a ServiceNow Developer. Both would have been missed on title alone.
- **Section-aware README insertion keeps sort order.** Find the first table row whose date is older than the new row and insert before it; `check_readme_sort.mjs` then reports OK. `board_invariants.py` stayed at 36 errors (ratchet: no kind grew).

## What failed / traps

- **Workday CXS 429'd on every tenant this hour** — the node scan's whole Workday sweep (15 boards × 2 queries) returned 0 matching postings, and a standalone BMO probe earlier returned 200 only before concurrency. This is the :00Z CI-collision pattern; expect 0 from Workday at the top of the hour and let a later pass or the CI run carry it.
- **LinkedIn detail pages intermittently serve the "Join LinkedIn" authwall** (body len ~402, `h1: Join LinkedIn`). USask "Enterprise Service Management Specialist" and Halifax "Application Administrator" could not be verified → skipped rather than guessed. Retry later or treat as unverified.
- **Salesforce keyword search is 80% sales/marketing noise.** `Enterprise Account Executive`, `SDR`, `Lead Management Operations`, `SFMC Manager` (borderline), `Marketing Operations Manager` dominate. Filter to admin/developer/architect/analyst titles before dedupe.
- **"salesforce" hits from the sidebar, again.** S M Software RQ11675 "Software Developer – CRM – Senior" (Toronto, 8h) is **Microsoft Dynamics 365 / Power Platform**; the only `salesforce` token on the page was a "People also viewed" card. Same class as the City of Hamilton rejection.
- **Title mirrors across sources.** LinkedIn `Staff Systems Engineer` (ServiceNow Toronto, 16h) duplicates the SmartRecruiters row posted 2026-11-09 (same company+title+city). Company+title matching catches it; URL matching does not.
- **A trailing LinkedIn id can appear twice under different slugs.** NLB job `4490660430` already existed as a README-only "ServiceNow CSM/HRSD" (Mississauga) row while the live card is "ServiceNow CSM/HRSD/IRM/ITAM/SPM" (Calgary). Grep the trailing id across README too, not only jobs.json — the stale row was removed rather than double-listed.
- **jobs.json insert must stay textual.** Inserting 5 rows at the head added ~26 lines; re-dumping the JSON would have rewritten all ~4k lines.

## Source yields this hour (for future agents)

- Scan: LinkedIn 288 / Adzuna 210 / Greenhouse 17 / SmartRecruiters 13 / remote feeds 11.
- Browser LinkedIn: SN Toronto 60 cards, SF Toronto 60 cards, SN Canada 60 cards → 6 new candidates → 5 verified.
- Workday: 0 (all 429).
- Partners observed: LGS (IBM) posted 5 Quebec SN roles (architect, CSM, HRSD, IRM, Now Assist) — all captured by the scan; Deloitte CMDB Solution Architect and KPMG Senior Manager GRC already on board; Ateko (Bell) Développeur ServiceNow already on board. Rogers surfaced only marketing-ops roles, Bell only the Ateko brand.
- Public sector: gojobs/jobs.gc.ca still Radware-walled; Job Bank still title-only.

## Market pattern (Nov 20, 2026)

Late-week, pre-holiday market: the board is near-saturated for LinkedIn/Adzuna Toronto SN/SF work. Net-new rate is now ~5 per hourly pass, mostly (a) vendor twins of existing reqs in a second city, (b) generic-titled platform roles that only a body check reveals, (c) French-language Quebec postings. Investigate only when LinkedIn returns <25 cards (wall) — 60 cards is the healthy shape.

## Run recipe that worked

1. `git fetch` + confirm local == origin/main.
2. `node scripts/daily_job_scan.mjs` (no `--no-readme`).
3. Browser LinkedIn: SN Toronto 24h, SF Toronto 24h, SN Canada 7d → collect cards.
4. Dedupe by URL (query-stripped), trailing LinkedIn job id, and normalized company+title.
5. Body-check every generic title (BA/consultant/analyst/developer without platform name).
6. Textual jobs.json insert at head; bump `meta.total` + `primaryCounts`.
7. README: insert rows at the sorted position in the matching section; `node scripts/check_readme_sort.mjs`.
8. `python3 tools/build_site.py`; `python3 scripts/sync_readme_counts.py`; `python3 scripts/board_invariants.py` (expect 36 errors, no growth).
9. Commit `[skip ci]`, push, trigger `pages.yml`, verify the live `jobs-data.json` carries each new URL.

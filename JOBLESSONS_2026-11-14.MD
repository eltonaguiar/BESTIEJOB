# JOBLESSONS_2026-11-14

Hourly Toronto / Canada ServiceNow + Salesforce board scan — Saturday 2026-11-14 01:00 EST (06:00 UTC).

## Result this cycle
- Fresh ServiceNow / Salesforce jobs merged to the board: **1**
  - Salesforce CPQ Lead Developer — E-Solutions — Canada — posted 2026-11-13 — Adzuna `adzuna.ca/details/5964819538` — URL verified live (HTTP 200).
- The 05:12 UTC hourly scan (remote `bab75bf`, 2650 listings) already captured this role plus 12 others, so the board on `main` reflects it; this cycle added no net new listing beyond what upstream had merged.
- GitHub Pages redeploys on main push via `pages.yml`.

## Sources scanned (this hour)
- Freshness-first scan (`scripts/fresh_ca_scan.py`, window 2026-11-14 / 2026-11-13): Adzuna API (~68 calls), Job Bank (11 pages), Eluta (6 pages). **0 fresh rows**.
- Adzuna sweep (`reports/adzuna_sweep_2026-11-14T0500Z.json`): 8 SN/SF Canada candidates. 7 already on the board (deduped by normalised URL); 1 fresh (E-Solutions above).
  - Already on board: Cognizant (SN SAM Developer), KPMG (Manager SN Technical Lead), Accenture (SN Technical Architect), S.I. Systems (SF Senior Developer), Tekgence (SF Revenue Cloud Architect), OSI Digital (SF QA Tester).
  - Excluded: Intellibee "Salesforce developer, St Paul, MN, US" (US role); Metrolinx/CorGTA/Mackenzie (not SN/SF titles).

## Dedupe / verification rules applied
- Dedupe key = normalised URL (strip query string + trailing slash, lowercase) against both `README.md` and `jobs.json`.
- A row counts as "on board" if its Adzuna ID or redirect URL appears in either store.
- Title must match the SN/SF classifier and must not match the sales/marketing exclude list.
- Location must be Canada/Toronto-first. US roles excluded even when flagged Canada.
- APPLIED.md is a hard exclude — applied roles never resurface.
- Every added URL is curl-verified live before merging.

## Known partners / sponsors / technical companies seen
- ServiceNow/Salesforce partners: Cognizant, Accenture, Deloitte, TCS, Procom, Fxinnovation, Alldus, Triunity, Ondaro.
- Banks/telecom/utilities with SN/SF practices: TD Bank, BMO, CIBC, National Bank of Canada, Interac, Rogers (Ateko backed by Bell), Bell, Trans Mountain, Loblaw, Mackenzie Investments.
- Canadian government / public sector adjacent: CAAT Pension Plan, Robertson & Company (Government of Canada client), United Way Greater Toronto.

## Process notes / pitfalls
- `tools/jobs_merge_inbox.py` additive merge REFUSES to write when the README tables hold glued multi-posting rows. This README's Salesforce table has glued rows, so the merger was blocked; do NOT use `--allow-row-loss` (it would silently drop existing postings).
- Local Playwright is headless-only (Chrome profile locked); needs explicit `executable_path` to ms-playwright chromium.
- Workday CXS is reachable via the `wdN` host (e.g. `bmo.wd3.myworkdayjobs.com`) with `curl --compressed`; bare tenant host is NXDOMAIN; `urllib` blocked by Workday CXS; LinkedIn guest detail returns 422.
- `inbox/` and `reports/` are scan working artifacts; this cycle's `inbox/fresh-ca--2026-11-14--v1.md` stayed header-only (0 fresh rows).

## Recommended next-cycle focus
- Re-scan Workday tenants (TD, BMO, CIBC, Interac, Loblaw) via `wdN` host + `curl --compressed`.
- Target Rogers / Bell / Canadian federal/provincial government postings (CSDM/ITAM/CMDB footprint) under the "other" board spec.
- Re-run `scripts/fresh_ca_scan.py` each hour; if it times out (>300s), run in background and merge the report when complete.

---
## Cycle: Saturday 2026-11-14 19:00 EST (2026-11-15 00:00 UTC)
- Fresh ServiceNow / Salesforce jobs merged to the board: **0** — all fresh candidates already tracked (see below). `jobs.json`, `readme.md`, and GitHub Pages unchanged; board holds 2,728 jobs.

### Fresh candidates checked (all already on board)
- Workday CXS BMO (bmo.wd3/External): ServiceNow CMDB Administrator + ServiceNow Technology Lifecycle Analyst (Toronto, posted 2 days ago; $55,500–$120,000, CSA/CIS Discovery/CIS Service Mapping preferred) — tracked 2026-11-12T22:05Z.
- Workday CXS TD (td.wd3/TD_Bank_Careers): Software Engineer III - Salesforce Data 360 (Toronto, posted yesterday) — tracked.
- LinkedIn guest browser scan 2026-11-14T11:32Z: 8 fresh postings (KTek ServiceNow Consultant; Experis Salesforce Technical Architect; Pacer Salesforce FSC Developer; LanceSoft Salesforce Revenue Cloud Technical Architect; Parkland Sr ServiceNow Developer Calgary; plus 3 GRC roles) — all already on board. Interac "Technical Service Now, Lead" repost (LinkedIn id 4126302101) matches the row tracked 2026-10-28; not re-added.

### Out of scope / negative results this cycle
- Adzuna hourly: Danaher ITSM Reporting Specialist ×2 (adzuna.ca/details/5964331993, 5964305343), posted 2026-11-13 — London, ON (Middlesex), not Toronto; new URLs but outside Toronto scope.
- Teck ERP Security & GRC Specialist (1 day ago, Toronto) — SAP GRC/IAG, no ServiceNow/Salesforce mention; skipped per platform-mention rule.
- Kelly IT Risk & GRC Specialist (1 day ago, GTA) — no ServiceNow/Salesforce mention; skipped.
- fresh_ca sweep (Adzuna 68 calls, Job Bank 11 pages, Eluta 6 pages): 0 rows.
- ATS board sweep (scripts/ats_board_sweep.py --days 2, 455 employer boards): 29,507 raw → 798 keyword-relevant → 83 Canadian → 5 dated ≤2d → 4 already on board → 0 new.
- Rogers jobs.rogers.com (Phenom): 404 / 9-byte body to curl — weekly check only. Bell jobs.bell.ca: (0) reqs for servicenow/salesforce. Public sector (gojobs.gov.on.ca, jobs.gc.ca): Radware bot manager blocked.

### Techniques confirmed this cycle
- Workday CXS reachable via `curl --compressed` with `Origin` + `Referer` headers on the `wdN` host (bmo.wd3, td.wd3 verified); bare tenant host is NXDOMAIN. GET `/wday/cxs/{tenant}/{site}/job/{externalPath}` returns jobPostingInfo with absolute dates and full description.
- LinkedIn guest `seeMoreJobPostings` returns HTTP 200 with an authwall body after ~4 rapid calls (337,822 bytes vs ~31 KB healthy) — check status + body digest/length, never `len()` alone; sleep ~25 s between batches of four.
- `scripts/sync_readme_to_jobs.mjs` is a silent no-op on the current README (one-line-mangled tables); jobs.json is the system of record, README is display-only.
- verify_links rule: 404/410/451 = dead; 403/429/5xx = bot wall, keep. Never prune existing dead links.

### Market shape (late 2026, Toronto)
ServiceNow-the-company posts only sales/SRE/security in Toronto; Salesforce-the-company posts nothing below 4 days old and no Platform Admin/Dev I. Fresh platform work comes from banks (BMO/TD/CIBC Workday) and GRC/IRM consultancies. No entry-level Salesforce Platform Admin/Dev I surfaced this cycle — keep `site:ca.linkedin.com/jobs/view "Platform Administrator" Toronto f_TPR=r86400` as the priority query next run.


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

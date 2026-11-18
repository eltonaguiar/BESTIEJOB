# JOBLESSONS_2026-11-18T0000EST

Hermes cron job scan — fresh Toronto/Canada ServiceNow & Salesforce jobs.
Run time: 2026-11-18T05:02Z (2026-11-18 00:02 EST).
Board: https://github.com/eltonaguiar/bestiejob (main) → https://eltonaguiar.github.io/BESTIEJOB/

## What this run did
1. Ran `scripts/daily_job_scan.mjs` against public ATS/job feeds (SmartRecruiters, Workday CXS, Greenhouse, Lever, Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna Canada).
2. Wrote jobs.json (+ public mirrors), FRESH_JOBS.md, and the `<!-- DAILY-SCAN -->` block in README.md.
3. Curated fresh Canada SN/SF postings (posted 2026-11-16 → 2026-11-18), deduped against README.md tables + jobs.json, excluded non-technical corporate roles (legal, recruiting, PMO, delivery management, pure business-process analyst) and same-requisition mirrors.
4. Submitted via `inbox/hermes-cron--2026-11-18--v1.md`; merged into README.md's three tables with `tools/jobs_merge_inbox.py`.
5. Rebuilt GitHub Pages with `tools/build_site.py` (public/jobs-data.json + public/index.html).
6. Committed and pushed to origin/main with [skip ci].

## Result
- Scan: 637 fresh postings, 2604 total merged (servicenow 1139, salesforce 1300).
- Curated fresh Canada SN/SF candidates not on board: 40 (servicenow 21, salesforce 19).
  - Posted: 2026-11-18 → 2, 2026-11-17 → 22, 2026-11-16 → 16.
- All 40 submitted URLs verified present in README.md.
- README table counts bumped: ServiceNow 1130 → 1154; Salesforce 1461 → 1477; Other unchanged (4039).
- Pages site rebuilt: 5006 jobs (SN 808, SF 934, Other 3264), 863 duplicate mirrors collapsed, 35 applied hidden, newest 2026-11-18, built 2026-11-18 05:09 UTC.

## Employers represented in the fresh batch
ServiceNow: IG Wealth Management, Spruce InfoTech, FOP Consultants, Nutrien (Calgary/Saskatoon), Envision Technology Solutions (Toronto), Mackenzie Investments (GTA), ServiceNow (Staff Cloud Security, Toronto), HRConnects (Vancouver), Hydro One / Acronym Solutions (ServiceNow contract, Toronto), W3Global (Mississauga), S I Systems (Calgary), Raas Infotek (Canada).
Salesforce: TD Bank (Associate Software Engineer nCino/Salesforce, Toronto — entry-level, via Workday employer ATS), Celestica (Student Intern Salesforce Developer 1, Toronto), Electric Mind (Toronto), The Citco Group (Toronto), Serefin (Toronto), White Bay (North York, SFMC admin), UST (Revenue Cloud BSA), TFI International (Montreal), myview (Brampton), Maarut (Toronto, data cloud), Astra-North Infoteck (Toronto technical leads), IKO North America (Mississauga), CYNET SYSTEMS (Mississauga).

## Toronto / partner / sponsor check (user directive: Rogers, Bell, GC, ServiceNow/Salesforce partners)
- Rogers (jobs.rogers.com): no fresh SN/SF posting surfaced (one Digital & eCommerce developer requisition, not platform-specific).
- Bell (jobs.bce.ca): ServiceNow Administrator / System Administrator roles found but dated Oct 6, 2026 with application deadline 11/02/2026 — already past, outside the 30-day window; nothing fresh merged.
- Government of Canada (gjobs.ca / jobs.gc.ca / talent.canada.ca): IRCC Salesforce Developer role dated Jun 16, 2026 — closed; nothing fresh merged.
- ServiceNow/Salesforce partners & sponsors (World Forum / World Tour sponsor seeds): not separately swept this run; the Workday/Greenhouse/Lever board list (BMO, TD, CAAT, D2L, Benevity, Loopio, NeuraFlash, EQ Bank, Alimentiv, Versapay) was re-scanned via the normal pipeline.

## Source health (rate limits / failures, recurring)
- Adzuna demo key: mostly HTTP 503/429 — only 350 usable results; treat Adzuna as discovery, not truth.
- Workday CXS: HTTP 429 on bursts — space calls ≥5s (per prior lessons); only 3 usable this run.
- LinkedIn guest seeMoreJobPostings: 429s after ~4 rapid queries — script uses 2 workers + 1800ms pause; recovered to 246 results this run.
- SmartRecruiters (ServiceNow): 12 usable; Greenhouse 16; Lever 1; Ashby 2; remote boards 7.
- Takeaway: employer ATS feeds (SmartRecruiters/Workday/Greenhouse/Lever/Ashby) are the most reliable verified source; aggregators (Adzuna/LinkedIn) need dedupe and date scepticism.

## Dedupe notes
- Dedupe key: normalised URL; same-requisition mirrors across sources (e.g. TD nCino via Workday vs LinkedIn) use different URLs and are NOT caught by URL dedupe — near-duplicates remain on the board, consistent with existing style (e.g. IG Wealth manager ×3 LinkedIn URLs).
- Company aliasing helps (TD Bank ≠ TD) but mirror postings under different ATS URLs still duplicate.
- inbox/ is left as submitted (no --bump-inbox) per hand-run convention.

## Recommendations for next run
- Re-scan employer ATS boards first (ServiceNow SmartRecruiters, BMO/TD/CAAT Workday, Greenhouse/Lever/Ashby tenants) — highest verification yield.
- Add Rogers, Bell, and GC careers pages to a monthly employer re-check list; this cycle they yielded only stale roles.
- Consider a ServiceNow Partner Finder / Salesforce AppExchange partner sweep for Elite/Select Toronto implementation boutiques (e.g. Pentio, Ateko, Lane Four, NewRocket, CloudFulcrum) that aren't on the current ATS tenant list.
- Keep spacing Adzuna/Workday/LinkedIn requests to avoid 429/503.

## Files changed
- README.md (30 new rows merged into tables; daily-scan block refreshed)
- jobs.json + public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json (scan rewrite)
- public/jobs-data.json, public/index.html (pages rebuild via build_site.py)
- FRESH_JOBS.md (scan rewrite)
- JOBLESSONS_2026-11-18T0000EST.MD (this file)

# JOBLESSONS_2026-11-21T0700EST

**Run:** hourly BESTIEJOB cron, Saturday 2026-11-21 07:00 EST (12:00Z). Board: eltonaguiar/BESTIEJOB on main. Local main was 1 commit behind origin/main (CI hourly scan ran at 12:00Z) — fast-forwarded onto origin/main before layering manual adds.

## What was scanned
- LinkedIn guest search (browser, fresh profile, no auth): `keywords=ServiceNow` and `keywords=Salesforce`, location Toronto/Ontario/Canada, `f_TPR=r86400` — 60 cards per query, readable as guest via `li a[href*="/jobs/view/"]` on the search page; detail pages readable via `document.body.innerText` sliced from "Job Description". `.jobs-description` selector returns empty on lazy-loaded LinkedIn pages — do not rely on it.
- Adzuna API (demo keys `app_id=54ce986e` / `app_key=db851f299e966c0a2a72af525dce6199`): `what=servicenow|salesforce`, `where=Toronto|Canada`, `max_days_old=3`, `sort_by=date`, param is literally `content-type` (not `content_type` → HTTP 400). Space calls ≥3–4 s (503s after ~4 rapid queries).
- Workday CXS POST `/wday/cxs/{tenant}/{site}/jobs` with `{"appliedFacets":{},"limit":20,"offset":0,"searchText":"..."}`, headers Content-Type/Accept/Origin only (Referer empties responses), `--compressed` required. All 14 Canadian-tenant probes returned HTTP 200 at 12:00Z — no 429 this hour. Workday 429s cluster at :00Z (CI hour); retry 3–4 tenants at ≥8 s spacing after :00Z+10 min. Verified 200 pairs: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site.
- Partner targeting: LinkedIn 24h scans surfaced Deloitte (SN partner) and nCino already tracked; Accenture Workday "Salesforce Data 360 Cloud MarTech Consultant" = twin of existing Adzuna row (company+title match, don't double-list).
- Rogers: Phenom board is a server-side shell (0 rows) — rely on LinkedIn/Adzuna, do not retry hourly. Bell: `jobs.bell.ca` shows (0) for servicenow/salesforce — zero reqs, re-check weekly. Canadian government: gojobs.gov.on.ca / jobs.gc.ca Radware-walled; Job Bank keyword search is title-noise (trust only titles naming the platform).

## Results this run
- **1 net-new add:** Deloitte — Software Asset Management (SAM) Analyst, Toronto (hybrid), LinkedIn 4468276720, ref 135050, posted ~17h ago (2026-11-20). ITAM/SAM "other" tag. Body-verified: JD names Salesforce + Microsoft vendor-license SAM work. Near-twin of the Oct-31 Deloitte SAM posting ref 134674 (4460500284): distinct LinkedIn req id, both kept.
- Dedupe checks passed: URL absent from jobs.json; no company+title twin; absent from APPLIED.md.
- Added to jobs.json (row spliced at head of `jobs` array; meta.total 5632→5633, newThisScan 504→505, sources.linkedin 250→251, scrapedAt/generatedAt refreshed) and to README "Other keyword matches — newest 10" (inserted newest-first, dropped the stale last row to keep 10). Copied jobs.json to public/findjobs, public/gotjob, public/jobs.json mirrors (verified byte-identical). Ran tools/build_site.py (site: 5,064 jobs: SN 874 / SF 932 / other 3,258) and scripts/sync_readme_counts.py (header 5491→5542).
- Committed + pushed to main; GitHub Pages rebuilds via pages.yml on the public/ push — verify live `jobs-data.json` carries the Deloitte URL after deploy.

## Skipped candidates (documented in inbox/hermes-cron--2026-11-21--v2.md)
- CIBC Senior Production Application Support Analyst 4493222509: twin of boarded CIBC Workday _2621365 (ServiceNow Admin/CMDB body-verified) — same role, different URL mirror; dedupe on company+title.
- Canadian Cancer Society Technical Business Analyst 4492852691: same posting already on board via ADP Workforcenow deep link (...jobId=594878); LinkedIn URL is a mirror.
- S M Software Solutions RQ11675 "Software Developer – CRM – Senior": Microsoft Dynamics 365 / Power Platform (Ontario MECP contract) — "CRM" ≠ Salesforce; body-check context, never trust raw keyword counts.
- nCino Senior Implementation Consultant 4485101504: URL already on board from an earlier scan.

## Patterns for future agents
- LinkedIn job-id equality is a hard dedupe signal even when titles differ — compare the trailing numeric id, not the slug.
- "CRM" in title ≠ Salesforce; "ServiceNow" in body as generic ITSM tooling ≠ platform role (body-check duties text, not sidebar keyword hits).
- Reposts under new LinkedIn ids with new reference codes (Deloitte 135050 vs 134674) are distinct reqs; Adzuna recycles ids — verify by Adzuna detail-page JSON-LD datePosted, not the API `created` date.
- Commit hygiene: never hand-respect merge conflicts on the six generated files — rebase onto origin/main, reset hard if needed, re-run scan+build on fresh base, then commit. `[skip ci]` on lessons/docs commits only; data pushes without it so pages.yml deploys.

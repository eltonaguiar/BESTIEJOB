# JOBLESSONS_2026-11-21T2000EST

Hourly BESTIEJOB scan run: Saturday 2026-11-21 20:00 EST (scan executed 20:02 EST / 2026-11-22T01:02Z). Base: `main` reset to `origin/main` (aborted stale in-progress rebase whose orig-head predates origin/main).

## What ran
`node scripts/daily_job_scan.mjs` (no `--no-readme`, per verified local recipe) → rewrote jobs.json, public job feeds, FRESH_JOBS.md, README `<!-- DAILY-SCAN -->` block → `python3 tools/build_site.py` → `python3 scripts/sync_readme_counts.py`. Result committed... see "Outcome" below — this run's local commit was abandoned because origin/main advanced first (see below).

## Scan results by source
- LinkedIn guest: 190 matching cards (Toronto + Canada, `f_TPR=r86400` fresh pass + general pass). Worked over plain `fetch`; no Playwright needed this run.
- Adzuna Canada API (demo keys): 182 matching postings across 27 queries (Toronto/Ottawa/Mississauga/Canada-wide; SN/SF + ITAM/CMDB/ITSM/B/A variants).
- SmartRecruiters ServiceNow: 12. Greenhouse: 14 (incl. NeuraFlash — Salesforce partner). Lever: 1. Ashby: 2. RemoteOK/Jobicy/Remotive: 7.
- Workday CXS (15 boards: Salesforce, BMO, TD, CIBC, Manulife, Interac, Accenture, GDIT, BDO, CAAT, Altus, IKO, Moneris, Huron, ResolveTech): **HTTP 429 on all 30 queries** at 01:02Z — the documented :00Z rate-limit window.

## Manual Workday re-probe (8–12 min past :00Z, 8s spacing, no `Referer` header)
All 15 boards returned HTTP 200, but **zero "Posted Today" Canada reqs**. Salesforce board's 3 "Posted Today" hits were Bangalore/Auckland (non-Canada) — `postedOn: "Posted Today"` is not a Canada signal; the `/job/<City>/` slug/location check is required. CI's concurrent fresh CA sweep (73dc6b3, 01:02Z) *did* get Workday 200s with 16 postings — the CI hourly pass carries Workday; manual runs should re-probe key Canadian tenants 4+ minutes past :00Z.

## Net-new jobs added to the board this hour: 5 (all LinkedIn `ca.linkedin.com/jobs/view/<id>` deep links)
1. Leader, Salesforce Digital – Canada — Slalom — Greater Toronto Area, Canada (2026-11-22) — Slalom is a Salesforce/ServiceNow partner.
2. Salesforce Enterprise Solution Architect — VySystems — Canada (2026-11-21) — VySystems is a Salesforce partner.
3. ServiceNow Implementation Architect — Pacer Group — Toronto, Ontario (2026-11-11) — staffing/vendor twin; keep alongside other vendors advertising the same req.
4. ServiceNow Implementation Architect — Avanciers Inc. — Toronto (2026-11-11) — Avanciers is a ServiceNow partner.
5. ServiceNow Implementation Architect — Wipro — Mississauga, Ontario (2026-11-04) — Wipro is a major SN/SF integrator.

The scan's other 403 "fresh" hits were already on the board (Adzuna re-issues the same role under new ids; dedupe key = hostname+pathname catches URL-level dupes but not id-recycled twins). Verified: none of the 5 appear in APPLIED.md.

## Named targets checked
- **Rogers:** `jobs.rogers.com` Phenom board = server-rendered shell, zero job rows; rely on LinkedIn/Adzuna for Rogers rows; do not retry hourly.
- **Bell:** `jobs.bell.ca` shows (0) for servicenow and salesforce in-browser — zero reqs, not a scrape failure; re-check weekly. Bell-area SN hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn — search "Ateko", not just "Bell".
- **Canadian government:** gojobs.gov.on.ca and jobs.gc.ca are Radware-captcha walled — do not retry; Job Bank is the proxy, trust only postings whose *title* names the platform.
- **Workday verified 200 pairs this run:** bmo, td, cibc, manulife, interac, caatpension, gdit, salesforce, accenture, bdo, altusgroup, iko, moneris, huron, irvingoil — banks/integrators are the main Canadian SN/SF demand; ServiceNow-the-company posts almost no Toronto platform admin/dev work.

## Outcome
Local scan produced jobs.json with 5,595 rows, but origin/main advanced to `73dc6b3` ("fresh CA sweep 2026-11-22T01:02Z", 5,565 rows, incl. Workday 16) while this run was in flight. All 5 net-new LinkedIn jobs from this scan were already present in origin/main's `jobs.json` and `public/jobs-data.json`, so the local commit was abandoned (`git reset --hard origin/main`) rather than hand-resolving generated-file conflicts. No re-scan: CI's sweep is the superset for this hour.

Site built locally from this run's data: 5,028 cards (SN 872 / SF 932 / other 3,224), 755 duplicate mirrors collapsed, 30 applied-hidden; `public/jobs-data.json` carries all 5 new URLs. Lessons committed separately as `[skip ci]`; pages redeploy triggered via `gh workflow run pages.yml`.

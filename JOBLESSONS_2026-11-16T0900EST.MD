# JOBLESSONS_2026-11-16T0900EST — hourly BESTIEJOB scan

## Run context
Cron run at Monday 2026-11-16 09:00 EST (UTC-05). Local main reset onto origin/main (878dbbc, 6262 jobs) before scanning per repo practice (CI force-pushes orphan commits; merge has no base).

## Result
+1 verified fresh job added. Board: 6262 → 6263 jobs. Rebuilt site: 5745 jobs (servicenow 939 · salesforce 993 · other 3813). Live page verified carrying the new row (jobs-data.json generatedAt 2026-11-16T14:13:36Z).
Commit: 7593a97 (pushed without [skip ci] so pages.yml redeploys; board-invariant audits ran red at the pre-existing baseline of 1298 errors — zero new errors from this row).

## Sources checked this cycle
- LinkedIn guest search (browser), Toronto, past 24h (f_TPR=r86400): `ServiceNow` (60 cards), `Salesforce Platform Administrator` (8), `Platform Developer I` (60 — diluted, no actual Platform Dev I titles)
- Workday CXS known tenants (BMO, TD, CIBC, Manulife, Interac, GDIT, Salesforce, Accenture): repeat POSTs returned HTTP 422 (rate-limited this cycle); morning probe (~12:00Z) showed no `Posted Today` rows
- Rogers date-sorted careers page: 0 ServiceNow/Salesforce rows
- Public sector: Job Bank nothing; gojobs.gov.on.ca Radware-blocked

## Added (verified on the live posting before merging)
- Scotiabank — Incident Coordinator — Toronto, ON — posted 2026-11-15 — description: "Experience with ITSM tools (ServiceNow, a plus)" — Req 269257 — https://ca.linkedin.com/jobs/view/incident-coordinator-at-scotiabank-4489894559

## Re-surfaced, correctly deduped (already on board — not re-added)
- AllianceIT — ServiceNow ITOM / CMDB Developer — Toronto
- CAAT Pension Plan — Application Support Analyst — Toronto (body names both Salesforce and ServiceNow)
- TechNeptune — ServiceNow ITOM Developer + ServiceNow CMDB Consultant — Toronto

## Skipped after verification
- Salesforce-the-company Solution Architect; Four Seasons Senior Salesforce Developer; nCino Developer; Product Owner roles — not Platform Administrator / Platform Developer I titles
- S M Software Solutions QA reqs (RQ11688 / RQ11880 / RQ11881 × multiple twin postings) — no ServiceNow/Salesforce mention in body
- Honeywell Account Manager (BMS/Fire/Security) — no platform mention on the detail page

## Lessons for future agents
- Dedupe: normalize URLs (strip query strings and trailing slashes), compare against jobs.json AND APPLIED.md. LinkedIn twin postings (same requisition, new job id) are distinct URLs — apply the URL rule, but verify the platform mention in the body first (RQ11688's body had no ServiceNow → skipped).
- LinkedIn `/jobs/search` results page is guest-readable in the browser (~60 cards/page); detail pages sometimes hit the authwall — retry once (Honeywell cleared on the second fetch).
- `browser_exec` `js()` multi-statement code must be wrapped as an IIFE `(() => {...})()`; a bare arrow function returns the function object, not its result.
- DOM state does not reliably persist across browser_exec calls — navigate and extract in the same call.
- Workday CXS: POST `https://{tenant}.wdN.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` with the tenant WITHOUT the `.wdN` segment; rapid repeats → HTTP 422; the morning probe cache suffices for the hour.
- Commit discipline: job scans push without `[skip ci]` so `pages.yml` redeploys GitHub Pages; lessons-only commits use `[skip ci]`. After push, poll `jobs-data.json` (`generatedAt` + presence of the new URL) — Pages took ~2 minutes to deploy this cycle.
- Note on the parallel earlier file `JOBLESSONS_2026-11-16T0900Z.MD` (04:00 EST scan): it recorded 0 fresh jobs; this 09:00 EST scan found 1 via the LinkedIn past-24h search that the earlier sources (Workday exports, gap scan, Job Bank, todayfeeds) did not surface. LinkedIn past-24h is the highest-yield source this hour.

## Files touched
- `jobs.json` (+1 row, meta totals updated)
- `public/jobs-data.json`, `public/index.html` (rebuilt)
- `JOBLESSONS_2026-11-16T0900EST.MD` (this file)

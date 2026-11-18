# JOBLESSONS_2026-11-18T0200EST — BESTIEJOB hourly cron scan

## Run
- Time: 2026-11-18 02:00 EST (07:05Z). Board: eltonaguiar/BESTIEJOB main → eltonaguiar.github.io/BESTIEJOB.
- Target: fresh Toronto / Canada ServiceNow + Salesforce postings; partner / sponsor / employer-of-interest sweep (Rogers, Bell, Canadian government, ServiceNow- and Salesforce-the-company).
- Sources swept: LinkedIn guest (24h, Toronto ON), Workday CXS (19 Canadian + partner tenants), SmartRecruiters (ServiceNow), Greenhouse / Lever / Ashby Canadian tenants, Adzuna Canada (demo key).

## Result
- **1 verified fresh, on-target posting merged**: NTT DATA North America — *Business Analyst – ServiceNow SPM*, Toronto, req 397935, posted ~2h before scan. Routed into `jobs.json` (inserted at head, 2569 → 2570) and the README ServiceNow table.
- Everything else this hour was already on the board (dedupe held) or off-target:
  - LinkedIn 24h "servicenow" returned the known batch — BMO ServiceNow CMDB Administrator (13h), ServiceNow Principal Solution Architect (13h), Envision ITOM Developer (16h), Mackenzie HRSD manager (8h), W3Global Developer/Architect (13h) — all ON-BOARD.
  - LinkedIn 24h "salesforce" — Loblaw Sr SWE Salesforce, McKesson Sr SF CRM Lead, Accenture SF Techno-Functional Lead, Citco SF Solution Architect, White Bay SFMC Admin, Munvo SFMC Consultant, Cognizant Data Cloud Dev, Serefin DevOps, Celestica Intern, TD nCino — all ON-BOARD.
- `tools/build_site.py`: 5016 jobs (SN 811 · SF 938 · Other 3267), 863 duplicate mirrors collapsed, 35 applied hidden, newest 2026-11-18. URL 4490843088 confirmed in `public/jobs-data.json` + `public/index.html`.

## Employer / partner sweep (user directive)
- **Rogers** — `jobs.rogers.com` reachable this hour (HTTP 200, 99 KB, date-sorted rows Nov 13–17 2026) but **zero** "ServiceNow"/"Salesforce" occurrences on the listing page → no SN/SF reqs to add. Re-check next cycle; unlike prior weeks the board itself loads fine.
- **Bell** — `jobs.bell.ca` still returns HTTP 303 → empty shell (0 reqs). Keep weekly.
- **Canadian government** — `jobs.gc.ca` / `gojobs.gov.on.ca` Radware-walled (do not retry). Job Bank `searchstring=servicenow` returns a search shell full of noise; trust only postings whose *title* names the platform.
- **ServiceNow-the-company** — SmartRecruiters page 1 = 100 reqs, only 3 Canada: Sr Solution Sales Executive CRM (CPQ) Toronto, Staff Cloud Security Engineer Toronto, Sr. CRM Account Executive Montreal — sales/security, all already on board. No platform roles.
- **Salesforce-the-company** — nothing fresh below 4 days and no Platform Admin/Dev I in Toronto (unchanged market shape).

## Reusable lessons (new / refined this cycle)
- **Generic titles hide platform roles.** LinkedIn "Business Analyst" at NTT DATA was actually *Business Analyst – ServiceNow SPM* with SPM in the body. Title-only SN/SF tagging misses these — when a generic BA / analyst / consultant title surfaces under the keyword search, fetch the description before discarding.
- **`.jobs-description` selector is required for body checks.** Reading `document.body.innerText` pulls the "People also viewed" sidebar; a CRM dev posting matched "salesforce" only because a *related job* was named "Sr. Salesforce Developer". Scope the extraction to `.jobs-description, .jobs-box__html-content` and re-read around the keyword hit.
- **Do not run the whole-inbox merger for a 1-row batch.** `jobs_merge_inbox.py --dry-run` reported it would re-add TD nCino/Salesforce and IG Wealth HRSD as "new" because the README's inline-mangled table rows are not matched by its URL dedupe. Direct injection (jobs.json row + one README line) is safer for small verified batches and avoids duplicate rows.
- **Adzuna demo keys work when passed explicitly.** `app_id=54ce986e`, `app_key=db851f299e966c0a2a72af525dce6199`; omit either → HTTP 400. 195 rows pulled across 4 queries this hour, 0 new SN/SF.
- **Workday CXS is fine but this hour was stale/US-only.** Posted-Today hits were Resolve Tech (US Remote FL) and GDIT (Any Location/Remote) — not Canadian. Always read the `/job/<City>/` slug; "Remote" is not a Canada signal.
- **Concurrent CI keeps main moving.** Local was 2 commits behind on start (hourly scan 06:21Z + fresh-ca sweep 06:50Z). Reset to `origin/main` before scanning; expect the hourly Action to commit while you work — rebase on push.
- **README row counts are stale debt** ("Show 1130 postings" / "6594 live postings" vs 6631 parsed). Left untouched; `sync_readme_counts.py` in CI owns it. Only the row itself was added.

## Files changed
- `jobs.json` (+1 job, meta.total 2570, primaryCounts.servicenow 1142)
- `README.md` (+1 ServiceNow row)
- `public/jobs-data.json`, `public/index.html` (rebuilt)
- `JOBLESSONS_2026-11-18T0200EST.MD` (this file)
- `inbox/hermes-cron--2026-11-18--v2.md` was written, validated, then removed after the direct merge so a future whole-inbox merge cannot re-add the row as a duplicate.

# JOBLESSONS_2026-11-23T2000EST — Hourly BESTIEJOB scan (20:00 EST / 2026-11-24 01:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,661 URLs, scrapedAt 2026-11-24T00:02:36Z from the :00Z CI scan) + README.md + APPLIED.md. No new verified live jobs to merge this hour.

## Scan sources
| Source | Query | Result |
|--------|-------|--------|
| Adzuna CA API | `what=ServiceNow`, `max_days_old=2`, `where=Canada`, sort by date | Results already on board |
| Adzuna CA API | `what=salesforce`, `max_days_old=2`, `where=Canada`, sort by date | Overwhelmingly sales/CRM-strategy roles, not Platform Admin/Dev I |
| Workday CXS | bmo/td/cibc/manulife/interac/caatpension tenants | HTTP 000 — Workday not reachable from this host (carried by CI scan at :00Z) |
| Web search | Rogers ServiceNow / Salesforce Toronto | 0 relevant (jobs.rogers.com Phenom board walled/bot-blocked; times out) |
| Web search | Bell ServiceNow / Salesforce Toronto | 0 fresh (jobs.bell.ca empty shell; Bell SN hiring under "Ateko / FX Innovation" — already covered) |
| Web search | Canadian government ServiceNow/Salesforce (Job Bank / gojobs.gov.on.ca / jobs.gc.ca) | 0 fresh (Radware-walled; non-platform roles only) |
| Web search | ServiceNow careers Toronto (careers.servicenow.com) | Senior Systems Engineer (Nov 20) already on board; no new platform admin/dev reqs |
| Web search | Salesforce careers Canada (salesforce.com/company/careers) | No fresh Toronto platform admin/dev postings surfaced |
| Aggregator check | freelanceradar.co ServiceNow/Salesforce Toronto | Jobs there already captured via LinkedIn/Adzuna sources in jobs.json |

## Fresh candidate investigated (NOT added)
- **Quarry Consulting — Salesforce Administrator (hybrid, North York)**, LinkedIn 4490381214. Confirmed live listing via LinkedIn guest API: North York ON, hybrid 3 days/week on-site, contract 1 year, rate $50.00 incorporated / $40.00 T4 per hour, posted "1 week ago" (~2026-11-16), 2–3 yrs Salesforce coordination/admin experience. **However: listing states "No longer accepting applications" — closed/expired, so it does not meet the board's live-posting policy and was NOT merged.** Re-check next run only if it relists.

## Dedup result (everything else already on board)
- TCS Salesforce Senior Developer / Senior Salesforce Developer (jobs.ca e1263bb1f0ce; LinkedIn 4491845382, 4491853255, 4491841920) — Toronto, posted Nov 18–19 — already in jobs.json
- HCLTech Salesforce Administrator Toronto (LinkedIn 4490676918, Nov 16) — already in jobs.json
- Quarry Consulting Salesforce System Coordinator/Administrator North York (LinkedIn 4487822864, Nov 10) — already in jobs.json
- SPECTRAFORCE ServiceNow Developer Toronto (LinkedIn 4492200627) — already in jobs.json
- Deloitte Senior Consultant ServiceNow Platform DTC Toronto (LinkedIn 4460515123, Nov 1) — already in jobs.json
- ServiceNow Senior Systems Engineer Toronto (smartrecruiters 744000162621080, Nov 20) — already in jobs.json
- Alimentiv ServiceNow Platform Specialist Toronto (LinkedIn 4483654163, Oct 28) — already in jobs.json
- Sheridan College ServiceNow Administrator & Developer Oakville (LinkedIn 4486264240, Nov 6) — already in jobs.json
- Resource Logistics ServiceNow Developer Toronto (LinkedIn 4489780092, Nov 16) — already in jobs.json
- G-Force IT Services ITSM Consultant Toronto (LinkedIn 4490140539, Nov 17) — already in jobs.json
- Leading Talent ServiceNow Administrator/Developer Toronto (expires 2026-12-19) — already in jobs.json
- Spectra Group ServiceNow Developer Toronto (dice, Nov 12) — already in jobs.json
- Cognizant ServiceNow SAM Developer Toronto — already in jobs.json (2 entries)
- BMO/TD/CIBC/Manulife/Interac Workday SN/SF reqs — Workday unreachable; carried by CI scan

## Net new this hour: 0

## GitHub Pages verification
- `jobs.json` working tree matches HEAD (scrapedAt 2026-11-24T00:02:36Z, total 5,661). No content changes to commit besides this lessons file.
- README.md unchanged (no rows added) → `pages.yml` is not retriggered (its push paths filter is public/**, README.md, tools/build_site.py, .github/workflows/pages.yml). No redeploy needed; the site deployed from the 19:02 EST scan is current.
- Live page cross-check: `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` — compare job count against `git show origin/main:public/jobs-data.json` before declaring any deploy current.

## Lessons for future agents
1. **LinkedIn "1 week ago" ≠ live.** Always check the application status line — Quarry 4490381214 looked fresh but is closed ("No longer accepting applications"). The guest API (`.../jobs-guest/jobs/api/jobPosting/<id>`) exposes both the posted-ago relative date and the closed status without login.
2. **Adzuna `what` matches description text.** `salesforce` returns sales strategists, CRM consultants, marketing roles. Filter titles with `\bsalesforce\b|\bapex\b|\bvisualforce\b|\bsoql\b` and exclude `\b(account executive|sales manager|business development|recruiter|talent acquisition|pre-?sales)\b`.
3. **ServiceNow-the-company Toronto postings are mostly sales/SRE/security.** Filter out "Solution Sales Executive", "Cyber Sales", "Sr Mgr, Sales", "Staff Full-Stack Engineer" unless specifically wanted.
4. **Workday CXS unreachable from this host (HTTP 000).** Do not manually probe BMO/TD/CIBC/Manulife/Interac — the CI hourly scan at :00Z carries Workday freshness. Do not retry hourly.
5. **Rogers/Bell/government portals yield nothing fresh.** Rogers Phenom board walled/times out; Bell zero SN/SF reqs; GC Job Bank/gojobs/jobs.gc.ca Radware-walled. Bell SN hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn — search that name instead.
6. **Zero new jobs this hour is normal.** Evening EST sees few employer posts; the :00Z Adzuna sweep already captured the day's postings. Expect 0–5 net-new per hour.
7. **Commit discipline:** only commit when there is a real change. This hour there is no README/jobs.json change, so this lessons file is the sole commit; no Pages redeploy is required or triggered by it.

## Next hour (21:00 EST)
- Re-run Adzuna `max_days_old=1` sweep for `ServiceNow` and `Salesforce Administrator/Developer` in Toronto/Canada
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions with `+new` rows to merge
- Re-probe Quarry 4490381214 only if it relists as accepting applications

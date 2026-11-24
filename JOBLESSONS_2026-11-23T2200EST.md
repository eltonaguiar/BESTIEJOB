# JOBLESSONS_2026-11-23T2200EST — Hourly BESTIEJOB scan (22:00 EST / 2026-11-24T03:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,627 URLs, scrapedAt 2026-11-24T01:12:43Z from the :00Z CI scan) + README.md + APPLIED.md. **No new verified live jobs to merge this hour.** Net new: 0.

## Scan sources
| Source | Query | Result |
|--------|-------|--------|
| Adzuna CA API | `what=ServiceNow`, `max_days_old=1`, `where=Toronto`, sort by date | 5 rows; 0 platform-relevant after filter (cyber/risk/security and general IT only) |
| Adzuna CA API | `what=ServiceNow`, `max_days_old=3`, `where=Toronto`, sort by date | page-1 rows; all dups or non-platform |
| Adzuna CA API | `what=Salesforce`, `max_days_old=1`, `where=Toronto`, sort by date | 0 platform-relevant (marketing/sales/QA text matches only) |
| Adzuna CA API | `what=Salesforce`, `max_days_old=3`, `where=Toronto`, sort by date | page-1 rows; all dups or non-platform |
| Adzuna CA API | `what=ServiceNow/Salesforce`, `max_days_old=3`, `where=Canada`, sort by date | 184 rows total across 4 endpoint calls; 0 fresh after platform filter + dedupe |
| SmartRecruiters | ServiceNow company board, all 11 pages (1,001 postings) | 26 Canada postings; newest released 2026-11-20 (Senior Systems Engineer Toronto, Cyber Advisory Solution Consultant Toronto) — both already on board (README, via hermes-cron--2026-11-20--v41 / adzuna 5974890953/5974890955). Nothing released after the 21:00 EST scan. |
| Inbox | fresh-ca--2026-11-23--v4/v6/v8/v10, ats--v4/v6/v8/v10, hermes-cron--v9, linkedin-guest--v6 | All already merged earlier today (v4 +1 KTek, v6 +4 incl. Smart IT Frame/Gravity/Global Consulting, v8/v10 +0). Nothing pending. |
| Workday CXS | bmo/td/cibc/manulife/interac/caatpension tenants | HTTP 000/422 — Workday not reachable from this host; CI :00Z scan carries Workday freshness. Not retried hourly. |
| Web search | Rogers ServiceNow / Salesforce Toronto | 0 relevant (jobs.rogers.com Phenom board walled/bot-blocked, times out) |
| Web search | Bell ServiceNow / Salesforce Toronto | 0 fresh — jobs.bce.ca shows 3 ServiceNow reqs (System Administrator, Senior Technical Advisor, Senior Manager Platform Delivery) but application deadlines 10/05/2026, 10/16/2026, 11/02/2026 — all expired before today (11/23/2026) |
| Web search | Canadian government ServiceNow/Salesforce (Job Bank / gojobs.gov.on.ca / jobs.gc.ca) | 0 fresh (Radware-walled; non-platform roles only) |
| Web search | ServiceNow careers Toronto (careers.servicenow.com) | Cloudflare-blocked from this host; SmartRecruiters direct API used instead (see above) |
| Web search | Salesforce careers Canada (salesforce.com/company/careers) | No fresh Toronto platform admin/dev postings surfaced |

## Fresh candidates investigated (NOT added)
None this hour — every Adzuna/SmartRecruiters platform candidate resolved to an existing board row or fell outside the platform-build scope (sales, cyber risk, marketing, general IT).

## Dedup result
All remaining hits were sales/CRM-strategy, marketing, cyber/risk, or general IT roles — none are ServiceNow/Salesforce platform-build requisitions. URL-only dedupe is insufficient (Adzuna/LinkedIn mirror requisitions under different URLs), so title + company + location signatures were cross-checked as well.

## Net new this hour: 0

## GitHub Pages verification
- No README.md or jobs.json change this hour → `pages.yml` push filter (`public/**`, `README.md`, `tools/build_site.py`, `.github/workflows/pages.yml`) not triggered; no redeploy required.
- The site remains current from the :00Z CI scan (jobs.json scrapedAt 2026-11-24T01:12:43Z, 5,627 listings).
- Live page cross-check pending: compare `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` job count against `git show origin/main:public/jobs-data.json`.

## Lessons for future agents
1. **Evening EST (after 21:00) consistently yields 0 net-new** — the :00Z Adzuna sweep already captured the day's postings; expect 0–5 net-new per hour, often 0.
2. **Bell's own board shows expired SN/SF reqs** (deadlines 10/05–11/02/2026) — do not re-add; Bell platform hiring surfaces under Ateko/FX Innovation, already covered.
3. **SmartRecruiters company board is directly paginable** (`api.smartrecruiters.com/v1/companies/servicenow/postings?limit=100&offset=N`) and is the best source for ServiceNow's own Canada reqs — 26 Canada postings found, none fresh this hour.
4. **Commit discipline:** only commit when there is a real change; this hour the lessons file is the sole commit, no Pages redeploy required or triggered by it.

## Next hour (23:00 EST)
- Re-run Adzuna `max_days_old=1` sweep for `ServiceNow` and `Salesforce` in Toronto/Canada
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions with `+new` rows to merge
- Re-check Ateko/FX Innovation careers page directly for any fresh ServiceNow/Salesforce Toronto requisitions

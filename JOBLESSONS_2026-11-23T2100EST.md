# JOBLESSONS_2026-11-23T2100EST — Hourly BESTIEJOB scan (21:00 EST / 2026-11-24 02:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,627 URLs, scrapedAt 2026-11-24T00:02:36Z from the :00Z CI scan) + README.md + APPLIED.md. **No new verified live jobs to merge this hour.** Net new: 0.

## Scan sources
| Source | Query | Result |
|--------|-------|--------|
| Adzuna CA API | `what=ServiceNow`, `max_days_old=3`, `where=Toronto`, sort by date | 34 total; 0 fresh after platform filter + dedupe |
| Adzuna CA API | `what=ServiceNow`, `max_days_old=3`, `where=Canada`, sort by date | 92 total; 0 fresh after platform filter + dedupe |
| Adzuna CA API | `what=Salesforce`, `max_days_old=3`, `where=Toronto`, sort by date | 77 total; 0 fresh after platform filter + dedupe |
| Adzuna CA API | `what=Salesforce`, `max_days_old=3`, `where=Canada`, sort by date | 283 total; 0 fresh after platform filter + dedupe |
| Adzuna CA API | `what=ServiceNow Administrator / Salesforce Administrator / Salesforce Developer`, `where=Toronto` | 19 total; all dups or non-platform |
| Workday CXS | bmo/td/cibc/manulife/interac/caatpension tenants | HTTP 000/422 — Workday not reachable from this host (carried by CI scan at :00Z) |
| Web search | Rogers ServiceNow / Salesforce Toronto | 0 relevant (jobs.rogers.com Phenom board walled/bot-blocked; times out) |
| Web search | Bell ServiceNow / Salesforce Toronto | 0 fresh (jobs.bell.ca empty shell; Bell SN/SF hiring under "Ateko / FX Innovation" — already covered; Ateko ServiceNow Architect FSM LinkedIn 4472356457 is an older req, not fresh) |
| Web search | Canadian government ServiceNow/Salesforce (Job Bank / gojobs.gov.on.ca / jobs.gc.ca) | 0 fresh (Radware-walled; non-platform roles only) |
| Web search | ServiceNow careers Toronto (careers.servicenow.com) | No new platform admin/dev reqs |
| Web search | Salesforce careers Canada (salesforce.com/company/careers) | No fresh Toronto platform admin/dev postings surfaced |

## Fresh candidates investigated (NOT added)
- **Cognizant — Salesforce Tech Lead (Remote), Toronto**, Adzuna 5973912092, created 2026-11-21. Same company + same title + same city as existing board rows LinkedIn 4492842720 (2026-11-20) and 4492525247 (2026-11-19). Near-duplicate / re-issued aggregator ad for an already-boarded requisition → NOT merged.
- **Intact Financial — Développeur(euse) principal(e) en développement de courriels dorsaux (Salesforce Marketing Cloud), Montréal**, Adzuna 5976294123, created 2026-11-23. French-locale alternate of existing board row Adzuna 5976294092 "Senior Back-End Email Developer (Salesforce Marketing Cloud)" (README line 29, posted 2026-11-23), same company + city + role. Preserved as locale alias, not a new row → NOT merged.
- **LifeLabs — IT Service Management Practice Lead (Toronto/Burnaby hybrid)**, Adzuna 5974915847, posted 2026-11-22. Previously held as a lead, not added: API description truncated with no ServiceNow/platform-build evidence.
- **Techo-Bloc — General Counsel**, Longueuil, created 2026-11-23. Matched platform regex on description text but is a legal role, not platform → false positive, dropped.

## Dedup result (everything else already on board)
All remaining Adzuna hits were sales/CRM-strategy, marketing, cyber/risk, or general IT roles — none are ServiceNow/Salesforce platform-build requisitions. Every live platform candidate found this hour resolved to an existing board row (URL match or title+company+location near-dup).

## Net new this hour: 0

## GitHub Pages verification
- `jobs.json` working tree matches HEAD (scrapedAt 2026-11-24T00:02:36Z, total 5,627). No content changes besides this lessons file.
- README.md unchanged (no rows added) → `pages.yml` is not retriggered (push paths filter: public/**, README.md, tools/build_site.py, .github/workflows/pages.yml). No redeploy needed; the site deployed from the 19:02 EST scan is current.
- Live page cross-check: `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` — compare job count against `git show origin/main:public/jobs-data.json` before declaring any deploy current.

## Lessons for future agents
1. **URL-only dedupe is insufficient.** Adzuna and LinkedIn mirror the same requisition under different URLs; always cross-check title + company + location (Cognizant "Salesforce Tech Lead (Remote)" Toronto appeared on both LinkedIn and Adzuna this hour).
2. **Locale alternates are aliases, not new rows.** Intact Financial's French SFMC ad (5976294123) is the same requisition as the English ad already on the board (5976294092) — preserve as alias.
3. **Adzuna `what` matches description text.** `servicenow`/`salesforce` return cyber/risk, marketing, sales-strategy, and general-IT roles. Filter titles/duties for platform-build terms and exclude sales/recruiting/strategy.
4. **Workday CXS unreachable from this host (HTTP 000/422).** Do not manually probe BMO/TD/CIBC/Manulife/Interac — the CI hourly scan at :00Z carries Workday freshness. Do not retry hourly.
5. **Rogers/Bell/government portals yield nothing fresh.** Rogers Phenom board walled/times out; Bell zero SN/SF reqs on its own board (hiring surfaces under Ateko/FX Innovation); GC Job Bank/gojobs/jobs.gc.ca Radware-walled.
6. **Zero new jobs this hour is normal.** Evening EST sees few employer posts; the :00Z Adzuna sweep already captured the day's postings. Expect 0–5 net-new per hour.
7. **Commit discipline:** only commit when there is a real change. This hour there is no README/jobs.json change, so this lessons file is the sole commit; no Pages redeploy is required or triggered by it.

## Next hour (22:00 EST)
- Re-run Adzuna `max_days_old=1` sweep for `ServiceNow` and `Salesforce Administrator/Developer` in Toronto/Canada
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions with `+new` rows to merge
- Re-check Ateko/FX Innovation careers page directly for any fresh ServiceNow/Salesforce Toronto requisitions

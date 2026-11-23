# JOBLESSONS_2026-11-23T0700EST — Hourly BESTIEJOB scan (07:00 EST / 12:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,607 URLs) + README.md + APPLIED.md. No new verified fresh jobs to merge this hour.

## Scan sources
| Source | Query | Result |
|--------|-------|--------|
| Adzuna CA API | `what=ServiceNow`, `max_days_old=1`, `where=Toronto, Ontario`, `sort_by=date`, pp=50 | 15 results; 0 fresh SN platform postings |
| Adzuna CA API | `what=Salesforce`, `max_days_old=1`, `where=Toronto, Ontario` | 28 results; 0 fresh SF platform postings |
| Adzuna CA API | `what=ServiceNow`, `max_days_old=2`, `where=Ontario` | 35 results; 0 fresh platform postings |
| Adzuna CA API | `what="Salesforce Administrator"`, `max_days_old=2`, `where=Ontario` | 8 results; 0 fresh platform postings |
| Web search | Rogers / Bell / Canadian government / Salesforce Platform Administrator Toronto | no fresh verified platform postings |

## Dedup result
- Adzuna surfaced 30 platform-titled results across the four queries
- 6 already on the board (Deloitte Technical Delivery Mgr IRM/Sec Ops `5975652935`; ServiceNow Cyber Advisory Solution Consultant `5974890953`; Novartis SFMC Manager `5975287815`; RSM Salesforce Supervisor CPQ SA `5974913547`; plus non-platform already-tracked rows)
- 1 near-duplicate repost twin: **Salesforce Tech Lead (Remote), Cognizant, Toronto** — adzuna `5973912092` (posted 2026-11-21) vs board row adzuna `5974890709` (posted 2026-11-22); same title/company/location, different adzuna id → treated as repost twin, not added
- **Net new this hour: 0**
- Nothing in APPLIED.md matches these URLs

## Employer-direct / partner probes (named-employer sweep)
- **Rogers**: jobs.rogers.com Phenom board returns a walled/zero-row shell; no SN/SF platform rows surfaced
- **Bell**: jobs.bell.ca empty for SN/SF; Bell's real ServiceNow hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn — already covered
- **Canadian government**: jobs.gc.ca / gojobs.gov.on.ca Radware-walled; Job Bank used as proxy — no fresh title-named platform postings
- **Salesforce Platform Administrator Toronto** (web search): SS&C Technologies, Desjardins/Collabria, etc. — postings older than this window or not date-confirmed fresh; not added unverified

## GitHub Pages verification
- Live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` returns 4,945 jobs — matches repo `public/jobs-data.json` (4,945 jobs). No README change this hour → no redeploy required; site current.

## Lessons for future agents
1. **Adzuna `what` matches description text, not just title.** A `salesforce` query returns sales strategists, CRM consultants, marketing roles. Filter titles with `\bsalesforce\b|\bapex\b|\bvisualforce\b|\bsoql\b|\blightning\b|\bsfmc\b` and exclude `\b(account executive|sales manager|business development|recruiter|talent acquisition|pre-?sales|marketing|growth marketing|performance marketing|strategic partner)\b`.
2. **ServiceNow-the-company posts mostly sales and SRE/security in Toronto.** Filter out "Solution Sales Executive", "Cyber Sales", "Sr Mgr, Sales", "Secure Design Manager" unless specifically wanted.
3. **Workday CXS is not reachable from this host (HTTP 000/422).** Do not manually probe BMO/TD/CIBC/Manulife/Interac Workday boards — do not retry hourly.
4. **Rogers and Bell yield nothing fresh.** Rogers Phenom board walled; Bell jobs.bell.ca empty. Bell SN hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn — search that name instead.
5. **Canadian government portals are Radware-walled** (jobs.gc.ca, gojobs.gov.on.ca). Use Job Bank as proxy; trust only title-named platform postings.
6. **Zero new jobs this hour is normal.** At 07:00 EST few employers post; the prior 06:00 EST scan also returned 0 net-new. Expect 0–5 net-new per hour.
7. **Adzuna re-issues the same role under new ids (repost twins).** Same title + company + location within ~24h under a different adzuna id is a repost — dedupe by URL catches exact duplicates but not twins; flag twins rather than add duplicate noise.
8. **Detail pages (`www.adzuna.ca/details/<id>`) return CloudFront 403 from this host.** Treat as a bot-wall on a live posting, never as dead; rely on API `created` date + title + redirect_url.
9. **Always verify live page vs repo before declaring a deploy:** `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` and compare job count with `git show origin/main:public/jobs-data.json`.

## Next hour (08:00 EST)
- Re-run Adzuna `max_days_old=1` sweep for `ServiceNow` and `Salesforce` in Toronto/Canada
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions to merge

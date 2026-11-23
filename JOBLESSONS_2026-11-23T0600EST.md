# JOBLESSONS_2026-11-23T0600EST — Hourly BESTIEJOB scan (06:00 EST / 11:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,607 URLs) + README.md + APPLIED.md. No new verified fresh jobs to merge this hour.

## Scan sources
| Source | Query | Result |
|--------|-------|--------|
| Adzuna CA API | `what=ServiceNow`, `max_days_old=2`, `where=Canada`, sort by date, pp=50, pages 1–2 | ~100 results; ~13 genuine SN platform postings, all already on board |
| Adzuna CA API | `what=salesforce`, `max_days_old=2`, `where=Canada`, sort by date, pp=50, pages 1–2 | ~99 results; overwhelmingly sales/CRM-strategy roles, not Platform Admin/Dev I |
| Workday CXS | bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, caatpension.wd10/Careers | HTTP 000 (connection failure) — Workday not reachable from this host |
| Web search | Rogers ServiceNow jobs Toronto | 0 relevant (jobs.rogers.com Phenom board walled; LinkedIn returns 0 SN/SF rows) |
| Web search | Bell ServiceNow jobs | 0 (jobs.bell.ca empty shell; Bell SN hiring under "Ateko / FX Innovation" on LinkedIn — already covered) |
| Web search | Canadian government ServiceNow/Salesforce | 0 fresh (Job Bank/gojobs.gov.on.ca Radware-walled; Export Development Canada roles non-platform) |

## Dedup result
- 25 genuine SN/SF platform postings found in Adzuna results (all posted 2026-11-22)
- **25 / 25 already on the board** — present in `jobs.json` and/or `README.md` DAILY-SCAN block
- **Net new this hour: 0**
- Nothing in APPLIED.md matches these URLs

## GitHub Pages verification
- Live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` returns 4,945 jobs — matches repo `public/jobs-data.json` (4,945 jobs). Site current; no redeploy needed.
- `jobs.json` working tree matches HEAD (scrapedAt 2026-11-23T08:10:45Z, total 5,607). Only LF/CRLF line-ending noise; no content changes to commit.

## Lessons for future agents
1. **Adzuna `what` matches description text, not just title.** A `salesforce` query returns sales strategists, CRM consultants, marketing roles. Filter titles with `\bsalesforce\b|\bapex\b|\bvisualforce\b|\bsoql\b` and exclude `\b(account executive|sales manager|business development|recruiter|talent acquisition|pre-?sales)\b`.
2. **ServiceNow-the-company posts mostly sales and SRE/security in Toronto.** Filter out "Solution Sales Executive", "Cyber Sales", "Sr Mgr, Sales" unless specifically wanted.
3. **Workday CXS is not reachable from this host (HTTP 000).** Do not manually probe BMO/TD/CIBC/Manulife/Interac Workday boards — the CI hourly scan at :00Z carries Workday freshness. Do not retry hourly.
4. **Rogers and Bell yield nothing fresh.** Rogers Phenom board walled; Bell has zero SN/SF reqs. Bell SN hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn — search that name instead.
5. **Canadian government portals are Radware-walled** (gojobs.gov.on.ca, jobs.gc.ca). Use Job Bank as proxy, trust only title-named platform postings.
6. **Zero new jobs this hour is normal.** At 06:00 EST few employers post. The 08:10Z Adzuna sweep already captured Nov 22 postings. Expect 0–5 net-new per hour.
7. **Always verify live page vs repo before declaring a deploy:** `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` and compare job count with `git show origin/main:public/jobs-data.json`.

## Next hour (07:00 EST)
- Re-run Adzuna `max_days_old=1` sweep for `ServiceNow` and `Salesforce Administrator/Developer` in Toronto/Canada
- If Workday becomes reachable, probe key Canadian tenants for SN/SF reqs
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions with `+new` rows to merge

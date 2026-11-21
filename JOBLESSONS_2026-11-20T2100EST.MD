# JOBLESSONS_2026-11-20T2100EST

Hourly BESTIEJOB scan run: 2026-11-21T02:02Z via `node scripts/daily_job_scan.mjs` (no --no-readme), then `tools/verify_links.py --days 2 --blocklist dead_urls.txt`, `tools/build_site.py`, `scripts/sync_readme_counts.py`.

## Result this hour
- fresh=456 postings returned by the 9-source scan; merged=5618 rows in jobs.json (servicenow 1190 / salesforce 4296).
- Net-new ROLES added to the board: 0. 31 postings arrived under URLs not previously on the board, but all 31 are company+title twins of roles already tracked (Adzuna re-issues the same role under a new redirect id, e.g. TD/OSI Digital/KPMG/BMO mirrors). Per board rules they are not double-listed; the new mirror URLs now live in jobs.json as alternates for existing cards.
- Site rebuilt: public/jobs-data.json + public/index.html — 5,052 jobs indexed (867 ServiceNow / 930 Salesforce / 3,255 other), 816 mirror clusters collapsed, newest posting 2026-11-20.

## Source behavior this hour
| Source | Matching postings | Notes |
|---|---|---|
| LinkedIn (guest, Toronto + Canada) | 238 | 2 of 14 query-location passes hit HTTP 429; one retry passed. Healthy card HTML is ~31 KB and differs per query — authwall is a 337,822-byte body with identical md5. |
| Adzuna CA API | 177 | Demo keys 54ce986e / db851f299e966c0a2a72af525dce6199. `max_days_old=14`, `sort_by=date`, `content-type=application/json`. |
| SmartRecruiters (ServiceNow) | 12 | Canada engineering/admin roles kept via forceTags; sales roles excluded by title regex. |
| Greenhouse / Lever / Ashby | 14 / 1 / 2 | Verified board slugs only (neuraflash, d2l, alimentiv-2, eqbank, benevolity, loopio, …). |
| Remote boards (remoteok/jobicy/remotive) | 9 | Canada/remote-eligible only. |
| Workday CXS (15 Canadian boards) | 0 fresh | ALL 30 board×query probes returned HTTP 429 — the CI hourly scan at :00Z rate-limits Workday; the 3 workday rows in jobs.json are carried cache, not fresh probes. Manual retry works ~4+ minutes past :00Z (8 s spacing between tenants). |

## Partner / sponsor / technical-company checks (task scope)
- Rogers: jobs.rogers.com renders a zero-row shell to raw fetch (Phenom); keyword search returns sales/marketing roles mentioning Salesforce in body, not platform roles. MLSE (Rogers-owned) Salesforce Engineer posting found via web search is dated 2026-09-30 — outside the 30-day window. Do not retry Rogers hourly; rely on LinkedIn/Adzuna for Rogers-sourced rows.
- Bell: jobs.bell.ca shows (0) for servicenow and salesforce — zero reqs, not a scrape failure. Bell's real ServiceNow hiring surfaces under Ateko (fxinnovation.com/en/jobs): ServiceNow Implementation Specialist (Remote · Canada) and ServiceNow Architect listed; verify posted dates (<30 days) before adding. Re-check weekly, not hourly.
- Canadian government / Job Bank: `servicenow`/`salesforce` keyword hits land on generic "IT consultant" postings that merely name the platform in body text; per protocol only trust postings whose TITLE names the platform. Found Job Bank postings were stale (advertised-until dates in Sep–Oct 2026) or non-platform titles. gojobs.gov.on.ca and jobs.gc.ca are Radware-walled — do not retry; Job Bank is the proxy.
- Lane Four: Salesforce Administrator (lanefour.com/job-posting/salesforce-administrator/) — LinkedIn-dated 2026-08-31, stale, not added.
- Salesforce careers (ca): Toronto hub hiring sales / Customer Success only; no Platform Administrator or Platform Developer I below 4 days. Salesforce Workday board (salesforce.wd12/External_Career_Site) search had fresh hits but all non-Canada locations.
- Market shape (unchanged): fresh platform work comes from banks (BMO/TD Workday), DXC, and GRC/IRM consultancies (PwC ServiceNow IRM practice, KPMG Canada). Accenture Workday has 1,600+ ServiceNow reqs but effectively none Canadian in page 1.

## Recommended next-hour actions
1. Re-probe Workday Canadian tenants (bmo, td, cibc, manulife, interac, caatpension, accenture, salesforce) at ≥8 s spacing, ≥4 minutes past :00Z.
2. Check fxinnovation.com/en/jobs dates for Ateko ServiceNow roles; add any posted within 30 days.
3. Re-run the full hourly scan; 0 net-new hours are normal at board saturation — report twins, not URL count, as "new".

Commit scope: jobs.json, README.md (DAILY-SCAN block), FRESH_JOBS.md, public/*, this lessons file. [skip ci] — then trigger `pages.yml` for immediate deploy and verify https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json carries the new scan's URLs.

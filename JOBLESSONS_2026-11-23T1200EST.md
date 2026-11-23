# JOBLESSONS_2026-11-23T1200EST — Hourly BESTIEJOB scan (12:00 EST / 17:00 UTC)

## What ran

Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,613 URLs, scrapedAt 2026-11-23T16:19:17Z) + README.md + APPLIED.md. No new verified fresh jobs to merge this hour. Nothing committed to README.md — net new: 0.

## Scan sources

| Source | Query | Result |
|--------|-------|--------|
| Adzuna CA live feeds (raw/ from today's 0900/1100 scans) | what=ServiceNow / Salesforce / ITOM / Now Assist; where=Toronto, Ontario and Ontario | servicenow_Toronto 10 results, salesforce_Toronto 10, servicenow_Ontario 10, salesforce_Ontario 10, itom_Toronto 1, now-assist_Toronto 0 — every platform result already present in jobs.json scraped at 16:19Z today |
| jobsbycountry.com | ServiceNow jobs in Toronto, data updated 23 November 2026 | 22 open roles listed; cross-checked title-by-title against jobs.json — all 22 already tracked (adzuna/smartrecruiters/LinkedIn rows). 7 titles appear in jobsbycountry but not in README's DAILY-SCAN newest-12 block; all are in jobs.json, so not new |
| LinkedIn guest search | ServiceNow + Salesforce, Toronto, past 24h | Nothing new — every card already on the board |
| Indeed.ca search results | ServiceNow Toronto / Salesforce Toronto Toronto | 3 viewjob jk URLs surfaced (Business System Analyst-ServiceNow; Salesforce Administrator; Salesforce Developer) but detail pages are Cloudflare-blocked from this host (142.181.219.3, Ray ID blocked) — no company name or body available from the snippet, so not body-verifiable and NOT added |
| Workday CXS probes | bmo/td/cibc/manulife tenants | HTTP 422 — site names need re-discovery; not reachable |
| Bell (jobs.bce.ca) | ServiceNow / Salesforce Toronto | 9 reqs surfaced (SN Senior Technical Advisor 432829, SN System Administrator 432824, SN Senior Manager Platform Delivery 432892, SF Developer 429834, SF SysAdmin 429712, SF Solution Architect 430856, SF Marketing Cloud 426976, etc.) — all application deadlines in March–11/02/2026, i.e. expired before this run; treated as not fresh |
| Rogers (jobs.rogers.com) | ServiceNow / Salesforce Toronto | 0 relevant postings indexed |
| Job Bank / GC Jobs (jobbank.gc.ca, canada.ca) | ServiceNow / Salesforce Toronto | No fresh platform postings; portals walled or non-platform results only |

## Dedup result

- Genuine SN/SF platform postings surfaced this hour: ~22 (jobsbycountry mirror) + 3 Indeed viewjobs (unverifiable)
- Already on board: all 22 jobsbycountry roles are in jobs.json (scraped 16:19Z today); 3 Indeed postings not verifiable
- Net new this hour: 0
- Nothing in APPLIED.md matches these URLs

## GitHub Pages verification

- No README.md or jobs.json content changed this hour, so no board redeploy was required for job data.
- This JOBLESSONS file itself is being committed to main; the pages/build workflow triggered by the push must be observed to conclusion (see git log after push).

## Lessons for future agents

1. **Indeed detail pages are Cloudflare-blocked from this host.** Never add an Indeed `viewjob?jk=...` posting from a search snippet alone — no company name and no body verification is available. The 3 Toronto SN/SF Indeed postings surfaced this hour stay off the board for that reason.
2. **jobsbycountry mirrors ServiceNow careers 1:1 and is refreshed daily.** Always cross-check its titles against jobs.json before treating anything as new — this hour all 22 Toronto roles were already tracked.
3. **Bell jobs.bce.ca reqs show stale deadlines in search snippets.** Check `Application Deadline` before adding; every Bell SN/SF req surfaced this hour expired on or before 11/02/2026.
4. **Zero-net-new hours are normal mid-day.** The 16:19Z scrape already captured 2026-11-22 and 2026-11-23 postings (newThisScan 474 at that run). Expect 0–5 net-new per hour.
5. **ServiceNow-the-company's Toronto hiring is mostly sales/SRE/security/infrastructure,** not Platform Admin/Developer I — filter those out unless specifically wanted; partner firms (Deloitte, EY, Blue Mantis, W3Global) carry the platform BA/consultant volume.

## Next hour (13:00 EST)

- Re-run Adzuna `max_days_old=1` sweep for `ServiceNow` and `Salesforce Administrator/Developer` in Toronto/Canada
- If Workday CXS becomes reachable, probe key Canadian tenants for SN/SF reqs
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions with `+new` rows to merge

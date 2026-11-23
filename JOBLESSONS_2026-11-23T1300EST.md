# JOBLESSONS_2026-11-23T1300EST — Hourly BESTIEJOB scan (13:00 EST / 18:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,613 URLs, scrapedAt 2026-11-23T16:19:17Z) + README.md + APPLIED.md. No new verified fresh jobs to merge this hour. Nothing changed in README.md — net new: 0.

## Scan sources
| Source | Query / target | Result |
|--------|----------------|--------|
| Adzuna CA live raw feeds (`raw/` from today's 0900/1100/1900 scans) | what=ServiceNow / Salesforce / ITOM / Now Assist; where=Toronto, Ontario and Ontario | servicenow_Toronto 10, salesforce_Toronto 10, servicenow_Ontario 10, salesforce_Ontario 10, itom_Toronto 1, now-assist_Toronto 0 — mostly sales/marketing/SRE/product or already in jobs.json; zero new verified platform-build roles |
| LinkedIn guest search | ServiceNow + Salesforce, Toronto | Freshest cards showed misleading relative dates (see Lessons); no body-verifiable new platform role |
| Indeed.ca viewjob | ServiceNow Toronto / Salesforce Toronto | 3 viewjob jk URLs surfaced but Cloudflare-blocked from this host; no company name or body — NOT added |
| Workday CXS probes | bmo / td / cibc / manulife tenants | HTTP 422; site names need re-discovery, not reachable |
| jobsbycountry.com | ServiceNow jobs in Toronto (data updated 23 November 2026) | 22 roles; all already tracked in jobs.json (per 11:00/12:00 scans) — not new |
| Bell (jobs.bce.ca / LinkedIn) | ServiceNow / Salesforce Toronto | LinkedIn SN Developer / Integrator 4471150580 is past its application deadline (expired) |
| Rogers (jobs.rogers.com) | ServiceNow / Salesforce Toronto | 0 ServiceNow positions; Salesforce hits all sales/ops |
| Job Bank / GC Jobs (jobbank.gc.ca, canada.ca) | ServiceNow / Salesforce Toronto | No fresh platform postings |
| Partners / sponsors / Elite Partners (Deloitte, EY, KPMG, Accenture, CGI, IBM, Cognizant, Ateko, Lane Four, Pentio, Fujitsu) | Toronto SN/SF | Current postings already on board; Cognizant careers pages Cloudflare-blocked |

## Dedup result
- Genuine SN/SF platform postings surfaced this hour: ~22 (jobsbycountry mirror) + 3 Indeed (unverifiable)
- Already on board: all 22 jobsbycountry roles are in jobs.json; 3 Indeed postings not body-verifiable
- Net new this hour: 0
- Nothing in APPLIED.md matches these URLs

## GitHub Pages verification
- No README.md or jobs.json content changed this hour, so no board redeploy was required for job data.
- This JOBLESSONS file is committed to main; the Pages workflow only triggers on `public/*`, `README.md`, `tools/build_site.py`, `.github/workflows/pages.yml`, so a JOBLESSONS-only push does not redeploy the board (expected — no board data changed).

## Lessons for future agents
1. **LinkedIn relative dates ("X hours ago", "Actively Hiring") are not trustworthy for freshness.** Interac "Technical Service Now, Lead" showed "20 hours ago" but jobs.json postedDate is 2026-10-28 (stale). Scotiabank "ServiceNow Administrator Specialist" showed "4 hours ago" but was posted 2026-07-13 with validThrough 2026-10-10 (expired). Always confirm the absolute `postedDate` before treating a role as fresh.
2. **Indeed detail pages and Cognizant careers pages are Cloudflare-blocked from this host.** Never add from a search snippet alone — no company name, no body, no duties/platform-build verification. The 3 Indeed Toronto SN/SF postings and the Cognizant Salesforce Data Cloud / nCino Developer reqs (Nov 13) stay off the board for that reason.
3. **Adzuna live raw feeds are sales/marketing-heavy.** Today's servicenow_Toronto / salesforce_Toronto / Ontario feeds returned ~40 platform-tagged results but they were sales, SRE, product, or already-in-jobs.json; zero new verified platform-build roles.
4. **Bell / Rogers / Canada.gov produced nothing fresh this hour.** Bell's LinkedIn SN role is past its deadline; Rogers has 0 ServiceNow and only sales/ops Salesforce hits; Job Bank / GC Jobs had no fresh platform postings.
5. **Zero-net-new hours are normal mid-day.** Expect 0–5 net-new per hour; the 16:19Z scrape already captured 2026-11-22 and 2026-11-23 postings.

## Leads for next run
- Re-run Adzuna `max_days_old=1` sweep for ServiceNow and Salesforce Administrator/Developer in Toronto/Canada
- If Workday CXS becomes reachable, probe key Canadian tenants for SN/SF reqs
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions with `+new` rows to merge

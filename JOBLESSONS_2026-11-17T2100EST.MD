# JOBLESSONS_2026-11-17 21:00 EST hourly scan

## Result
**0 fresh verified Toronto ServiceNow/Salesforce jobs merged.** Base was `origin/main` ee61982 (`chore(jobs): hourly scan refresh (2858 listings, 2026-11-18T01:20:14Z)` — scrapedAt 2026-11-18T01:18:27Z, i.e. the :00 UTC hourly scan finished at 20:18 EST). `jobs.json` holds 2858 listings (1329 ServiceNow / 1405 Salesforce), README section "Current jobs — as of 2026-11-17". No changes to `jobs.json`, `README.md`, or `public/`, so no site rebuild or GitHub Pages redeploy this hour. Live page `https://eltonaguiar.github.io/BESTIEJOB/` returned HTTP 200.

## Sources checked this run

| Source | Query/coverage | Fresh SN/SF hits | Status |
|---|---|---|---|
| Adzuna API `ca/search` | servicenow/salesforce/itsm/cmdb + variants, Canada + Toronto/Ontario, max_days_old=2, sort_by=date | 0 | **Blocked:** API returned its "something isn't right" HTML error page from this host (worked at the 00:30Z run, failed at 21:00Z). No candidates pulled. |
| `scripts/fresh_ca_scan.py --days 2` | Adzuna + Job Bank + Eluta, Toronto/Ontario | 0 | **Hung:** Job Bank / Eluta page scraping did not return within 120s (twice); no `inbox/` or `reports/` file written. |
| ServiceNow Careers | careers.servicenow.com Toronto/Ontario listings + Direct leads (Director Regional Product Management Nov 13, SRE/Staff SRE Nov 5-6) | 0 new | 83 careers.servicenow.com URLs already present in `jobs.json`; roles are product/security/SRE, not Platform Admin/Dev I. |
| Bell | jobs.bce.ca "ServiceNow Senior Technical Advisor, Toronto"; LinkedIn "ServiceNow System Administrator at Bell" | 0 new | bce.ca/bell URLs and the Bell SN SysAdmin posting already in `jobs.json`/`README.md`. |
| LinkedIn search results | ServiceNow Administrator/Developer CGI, J&M Group, Bell, BFG Enterprise Services | 0 new | CGI + Bell already on board; J&M Group + BFG not in board but no fresh posted date verifiable (listings showed "1-2 weeks ago"); treated as not-fresh. |
| Salesforce Canada careers | salesforce.com/company/careers/locations/north-america/canada/ | 0 | Hub page only; no dated Toronto SN/SF platform postings extracted. |

Cross-check method: candidate URLs deduplicated against `jobs.json` `.url` (8060 URLs incl. non-primary) and README table `[title](url)` links.

## Seen but not added (off-target)
- **ServiceNow** "Director, Regional Product Management, Toronto" (Nov 13) — product management at ServiceNow Inc., not a ServiceNow platform admin/dev role. Not added.
- **ServiceNow** SRE / Staff SRE / security engineer Toronto (Nov 5-6, Canada Protected B) — infrastructure/security roles, not ServiceNow platform roles. Not added.
- Architect/contract/remote-Canada hits from earlier scans (Raas Infotek, Smart IT Frame CPQ architect) remain off-target for the Platform Admin / Platform Developer I entry-level targeting.

## Rate limits and caveats
- Adzuna API is intermittent from this host: OK at 00:30Z, error page at 21:00Z — never depend on it as the sole freshness source.
- Job Bank / Eluta page scrapes hang this host (>120s); time out and move on rather than blocking the run.
- LinkedIn guest `seeMoreJobPostings` API 429s after ~4 rapid queries — space calls ≥5s. Guest detail/list pages remain readable.
- Workday CXS search returns HTTP 422 on bursts — space calls ≥5s.
- The :00 UTC hourly scan already refreshes the board (45-day aggregator + ATS sweep), so a 21:00 EST run's incremental window is ~45 minutes; partner/direct checks are the useful addition at this cadence.

## Recommendation for next hourly run
- Re-try Adzuna + Job Bank/Eluta freshness-first scan first (it adds today/yesterday-dated rows the breadth-first hourly scan can bury).
- If Adzuna is blocked again, fall back to direct employer checks: ServiceNow Careers, Salesforce Canada, Bell jobs.bce.ca, Rogers jobs.rogers.com, Canadian government jobs.gc.ca — all verified dedupe-able against `jobs.json`.
- Keep prioritizing entry-level **Platform Administrator / Platform Developer I** titles; architect/contract/remote-Canada hits go in lessons, not the board.

## Files changed this run
- `JOBLESSONS_2026-11-17T2100EST.MD` (this file) only; no board data changes.

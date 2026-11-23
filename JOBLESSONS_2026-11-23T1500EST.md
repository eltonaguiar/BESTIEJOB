# JOBLESSONS_2026-11-23T1500EST

**Run:** hourly scan, Monday 2026-11-23 15:00 EST (20:00 UTC), Toronto ServiceNow / Salesforce focus.
**Result:** 1 net-new verified Toronto posting added to README.md main branch; commit e8957aa pushed to origin/main; GitHub Pages deploy succeeded (eltonaguiar.github.io/BESTIEJOB/).

## Sources checked this hour

| Source | Query/scope | Outcome |
|---|---|---|
| Adzuna CA API (`max_days_old=3`, sort by date) | SN/SF/ITSM/CMDB/Agentforce variants, Toronto/Ontario/Canada | Fresh feed; 5 raw files from the 08:00Z scan + live files |
| LinkedIn guest search | ServiceNow + Salesforce, Toronto, past 24h | 3 cards; VySystems already on board; Tenstorrent GRC not platform-scoped; SCIEX already on board |
| Employer-direct | Rogers, Bell, Canada Life, Ateko careers | No fresh live platform roles; Bell SN roles are Oct 28–30 postings already on board |
| Government of Canada / Ontario portals | canada.ca, gojobs.gov.on.ca | Nothing fresh |
| Workday CXS | bmo/td/cibc/manulife | HTTP 422/429 again — site names need re-discovery via careers pages |
| Web search | Rogers/Bell/GovC/partner (Pentio/Lane Four/Ateko/CloudFulcrum) SN/SF Toronto Nov 2026 | Lane Four consultant/BSA roles ~Nov 8–10 (outside 3-day fresh window) — weekly re-check, not hourly |

## Verified fresh addition (added to README.md)

| Posted | Role | Company | Location | Source | Evidence |
|---|---|---|---|---|---|
| 2026-11-22 | Request ID: 114275 - Salesforce Revenue Cloud Architect | Flexstaf IT | Toronto, Ontario | adzuna | adzuna id 5975115720, API `created` 2026-11-22T08:47:19Z; Toronto ON hybrid contract; excerpt confirms Revenue Cloud design/build (Quote-to-Cash, Contract-to-Cash, Billing, Subscription Management, Revenue Lifecycle). Detail page behind CloudFront 403 from this host — liveness via API `created` date + title/platform match per board policy (403 = bot-wall on a live posting, not dead). Already present in jobs.json (added by the 14:00 EST CI scan, scrapedAt 2026-11-23T19:06Z) but missing from README until this run. |

## Held as leads (not added)

- **LifeLabs — IT Service Management Practice Lead** (adzuna 5974915847, posted 2026-11-22, Toronto / Burnaby hybrid): surfaced in the ITSM keyword scan, but the API description is truncated at ~500 chars with no ServiceNow or platform-build evidence. ITSM Practice Lead is governance/strategy, not hands-on platform work — below the board's substantive-duties bar. Re-check the employer page directly before adding.
- **Salesforce — Renewals Innovation Analyst, Emerging Talent** (adzuna 5972722264, posted 2026-11-20): Salesforce internal renewals/sales role, not platform build — out of scope.

## Patterns / lessons for future runs

1. **Adzuna fresh window pays off once per cycle.** The 08:00Z and 14:00 EST scans already absorbed Konrad (Senior Salesforce Loyalty Developer / Salesforce Architect), Cognizant Salesforce Tech Lead, Cloud Resourcing CLDRSRC10472, LifeLabs-adjacent rows, etc. Re-scanning the same Adzuna window within hours yields diminishing returns — space repeat Adzuna queries farther apart or vary keywords/locations instead of repeating identical calls.
2. **CloudFront 403 is not dead.** Adzuna detail pages return 403 from this host; board policy treats `created` date + title/platform match as liveness evidence. Keep applying that rule consistently rather than dropping 403'd postings.
3. **LinkedIn guest search is nearly fully picked over.** Past-24h Toronto SN/SF guest results keep returning cards already on the board (VySystems, SCIEX). Diminishing returns — rotate to employer-direct or vary the search window instead of repeating daily.
4. **Workday CXS is blocked at :00Z** (429 rate limit on all 15 boards; 422 on bmo/td/cibc/manulife probes). The CI hourly pass carries Workday discovery; local runs should not re-probe Workday CXS expecting different results — re-discover site names via careers pages first.
5. **Employer-direct portals (Rogers, Bell, Canada Life, Ateko) cycle slowly.** Bell's open SN roles are Oct 28–30 and already on the board. Check these weekly, not hourly; record "no fresh roles" as a negative result rather than resubmitting old postings.
6. **Government/public-sector portals surface nothing fresh** for SN/SF Toronto — keep as a periodic (weekly) check of jobs.canada.ca/gojobs.gov.on.ca, not an hourly source.
7. **README.md vs jobs.json divergence risk.** This run found a posting (Flexstaf Revenue Cloud Architect, adzuna 5975115720) present in jobs.json but absent from README.md's tables — the 14:00 EST CI scan added it to the feed but it wasn't rendered into the README sections. Future runs should diff jobs.json adzuna URLs against README rows before closing out, not just the reverse.
8. **Partner directories are weekly, not hourly.** Lane Four (Toronto Salesforce partner) consultant/BSA roles appeared in web search but post ~Nov 8–10, outside the fresh window. Re-check partner careers (Lane Four, Pentio, Ateko, CloudFulcrum) after each event/weekly cycle.

## Deploy verification

- Commit e8957aa `chore(jobs): 15:00 EST scan refresh — +1 verified Toronto posting (Flexstaf IT Salesforce Revenue Cloud Architect) [skip ci]` pushed to origin/main.
- GitHub Actions "Deploy GitHub Pages" workflow (manual dispatch from the push) run 45255895599: completed success, 2026-11-23T20:07:05Z; pages status `built`, source branch `main`, URL https://eltonaguiar.github.io/BESTIEJOB/.
- The live page builds from jobs.json (5659 listings) which already contains the Flexstaf row, so the new posting is live on the page.

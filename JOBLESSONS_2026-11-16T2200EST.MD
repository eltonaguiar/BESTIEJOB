# JOBLESSONS_2026-11-16 22:00 EST hourly scan

## Result
**0 fresh verified Toronto ServiceNow/Salesforce jobs merged.** Every fresh SN/SF hit from this hour's scan was already on the board (URL dedupe against `jobs.json`, 6284 jobs, 6284 unique URLs) or failed the freshness/scope filter. No changes to `jobs.json`, `README.md`, or `public/`, so no site rebuild or GitHub Pages redeploy this hour.

Live board verified earlier this cycle: `https://eltonaguiar.github.io/BESTIEJOB/` HTTP 200; `jobs.json` served HTTP 200. Board data is current through scrapedAt `2026-11-16T23:10:30.220Z` (~18:10 EST). Counts: ServiceNow 1306 / Salesforce 1373 primary; SN/SF Toronto/Ontario 1093; 49 SN/SF postings dated 2026-11-16 already on the board, incl. **HCLTech — Salesforce Administrator — Toronto** (entry-level Platform Admin) and **TD Bank — Senior Solution Architect (ServiceNow) — Toronto**.

## Why nothing was new this hour
- This run's LinkedIn scan (6 queries: servicenow_toronto, salesforce_toronto, sf_admin_toronto, sf_dev1_toronto, servicenow_canada, salesforce_canada — 266 results) returned only 1 SN/SF URL not on the board (Smart IT Frame — Salesforce Technical Architect CPQ/Revenue Cloud), rejected as off-target: Architect level, not Platform Administrator / Platform Developer I targeting.
- LinkedIn verified set (5): same Smart IT Frame hit; the other 4 already on the board.
- Workday tenant probes (Accenture, BMO, CIBC, GDIT, Interac, Manulife, Salesforce, Sun Life, TD): all SN/SF Canada hits either already on the board under aggregator/curated URLs (BMO ServiceNow CMDB Administrator & Technology Lifecycle Analyst since Nov 14; BMO ServiceNow SAM Administrator-ITAM since Nov 5; CIBC Senior Manager Salesforce Delivery since Nov 4; Manulife Salesforce Functional Analyst Waterloo/Toronto since Nov 2; TD Salesforce Data 360 since Nov 16) or stale (IKO Salesforce Senior Developer Mississauga ×2, 30+ days; Accenture London ServiceNow roles, 18–30 days, non-Toronto).
- Public sector (Job Bank / OPS): blocked by Radware bot manager — no extractable postings.
- Partner/gap scan (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze career pages): no jsonLd job anchors extractable.
- Web search (Indeed, Glassdoor.ca, LinkedIn, jobs.ca): today's hits are all roles already on the board or 3d+/30d+ postings already scanned (Bell ServiceNow System Administrator Toronto 23d; Scotiabank ServiceNow Administrator Specialist Toronto 30d+; Brookfield ServiceNow Developer contract Toronto 5+ yrs).

## Sources checked this run
| Source | Query/coverage | Fresh SN/SF hits | Status |
|---|---|---|---|
| LinkedIn fresh scan | ServiceNow + Salesforce + Platform Administrator + Platform Developer I — Toronto + Canada (6 queries, 266 results) | 0 new | All SN/SF hits already on board (URL dedupe) |
| LinkedIn verified | 5 individually opened postings | 0 new | 1 off-target (Smart IT Frame Salesforce Technical Architect); 4 on board |
| Workday CXS tenant probes | Accenture, BMO, CIBC, GDIT, Interac, Manulife, Salesforce, Sun Life, TD — SN/SF Canada | 0 new | All dupes or stale |
| Public sector (Job Bank / OPS) | Canada federal + Ontario public service | 0 | OPS blocked by Radware; Job Bank feed no fresh SN/SF |
| Partner/gap scan | 7 SN/SF partner career sites | 0 | No extractable postings |
| Web search | Indeed/Glassdoor/LinkedIn/jobs.ca — SN + SF — Toronto + Canada | 0 new | Today's hits already on board |
| jobs.json URL dedupe | 6284 jobs; 6284 unique URLs; today's Toronto SN/SF present | 0 new | Board current through ~18:10 EST |

## Seen but not added (off-target / stale / dupe)
- **Smart IT Frame** — "Salesforce Technical Architect - Strong CPQ and Revenue Cloud Advanced", Toronto — Architect level, not Platform Admin/Dev I. Not added (same decision as 20:00/21:00 runs).
- **BMO** — ServiceNow SAM Administrator - ITAM, Toronto, 13 days old — already on board since 2026-11-05 (adzuna). Not re-added.
- **CIBC** — Senior Manager, Salesforce Delivery, Toronto, 12 days old — already on board since 2026-11-04. Not re-added.
- **Manulife** — Salesforce Functional Analyst, Waterloo/Toronto, 14 days old — already on board since 2026-11-02. Not re-added.
- **IKO** — Salesforce Senior Developer, Mississauga ×2, 30+ days old — outside 30-day window. Not added.
- **Accenture** — ServiceNow Technical Architect / Lead Developer, London, 18–30 days old — location not Toronto-confirmed, stale. Not added.
- Various senior/architect/contract SN/SF roles (Brookfield, PwC, OSI Digital, CGI, Deloitte, Altus Group, Medcan, Intelli-CloudWare) — mid/senior level, not entry-level Platform Admin / Platform Developer I targeting. Not added.

## Rate limits and caveats
- Workday CXS search endpoint is burst-limited: repeated POSTs return HTTP 422. Space calls ≥5s; a single spaced call still works.
- LinkedIn guest: `seeMoreJobPostings` API 429s after ~4 rapid queries — read `status` + body digest, not just `len`, and sleep ~25s between batches of four. List and detail pages are readable as guest via DOM.
- Workday `postedOn: "Posted Today"` is not a Canada signal — always read the `externalPath` slug/country before counting a hit.
- Entry-level targeting = Platform Administrator / Platform Developer I. Architect, contract, remote-Canada, and senior SN/SF hits go in lessons, not the board.

## Recommendation for next hourly run
- Re-probe Workday tenants after the rate-limit window; prioritize entry-level **Platform Administrator / Platform Developer I** titles.
- Keep Rogers weekly (not hourly) and public-sector via Job Bank only; Bell and other telco career pages are low-yield for SN/SF.
- Do not re-add stale (~2+ week) off-board candidates — they were already scanned and correctly excluded.

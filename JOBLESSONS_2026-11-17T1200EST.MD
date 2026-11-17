# JOBLESSONS_2026-11-17 12:00 EST hourly scan

## Result
**0 fresh verified Toronto ServiceNow/Salesforce jobs merged.** Every fresh SN/SF hit from today's scans was already on the board (deduped against `jobs.json` URLs + `README.md` rows). No changes to `jobs.json`, `README.md`, or `public/`, so no site rebuild or GitHub Pages redeploy this hour (the scheduled Pages cron at :35 UTC still redeploys the live site independently).

## Scan basis (this run)
- Fresh SERVICENOW scan — `reports/fresh_servicenow_2026-11-17.md` (generated 07:02 UTC): 105 boards, 13,137 postings fetched, 0 net-new fresh SN jobs.
- Fresh SALESFORCE scan — `reports/fresh_salesforce_2026-11-17.md` (generated 07:03 UTC): 105 boards, 13,237 postings fetched, scanner reported 4 net-new, **all 4 already on the board** (URL dedupe).

## Dedupe detail — Salesforce "fresh" hits were duplicates
| Posted | Title | Company | Location | Already on board as |
|---|---|---|---|---|
| 2026-11-13 | Associate Vice President, Salesforce Engineering & Development | Jobgether | Canada | `README.md` line 1393 — `lever:jobgether/72434945-c782-4d3e-9b31-1ab1a75c21b7` |
| 2026-11-13 | Solution Architect, Salesforce Voice | Jobgether | Canada | `README.md` line 1394 — `lever:jobgether/af053390-3bd6-4a14-b02e-f9a95abab903` |
| 2026-11-10 | Associate Salesforce Administrator | Jobgether | Canada | `README.md` line 1395 — `lever:jobgether/31937f76-54e7-4341-8158-d03a295821a8` |
| 2026-11-10 | Senior Salesforce Developer | Docebo | Toronto, Ontario | `README.md` line 1696 — `ashby:docebo/0bbdde71-476f-4f46-bfdc-d4536cdcf7ad` (also on board as an Adzuna row per JOBLESSONS_2026-11-11; cross-source identity match blocks the dup) |

Freshness window cutoff: 2026-11-10. Liveness verified (HTTP 2xx/3xx) on the scanner side; board dedupe is by URL, then by company+title identity.

## Sources checked this run
| Source | Query/coverage | Fresh SN/SF hits | Status |
|---|---|---|---|
| Workday career sites (105-board sweep) | BMO, TD, CIBC, Manulife, Interac, GDIT, Salesforce, Accenture, Deloitte, CGI, ServiceNow, NeuraFlash, etc. — SN + SF, Canada | 0 new | All hits already on board or non-Canada |
| Greenhouse / Lever / Ashby / SmartRecruiters / Workable | SN + SF partner ATS boards | 0 new | All already deduped |
| LinkedIn guest / Indeed / Adzuna (prior harvests) | SN/SF Platform Admin / Platform Developer I — Toronto + Canada | 0 new this hour | Already merged in the 11:00 EST scan (250 fresh Canada postings) |

## Partner / sponsor / public-sector coverage (user-requested list)
- **Rogers**: checked (raw/rogers_today.html) — 0 ServiceNow/Salesforce mentions today.
- **Bell** (jobs.bell.ca): known empty for SN/SF — checked weekly, not hourly.
- **Canadian government / public sector** (jobs.gc.ca, gojobs.gov.on.ca): radware-walled; Job Bank proxy returned nothing.
- **SN/SF partners scanned in the 105-board set**: TD Bank, BMO, CIBC, Manulife, Sun Life, Salesforce, Accenture, Deloitte, CGI, ServiceNow, NeuraFlash, Interac, OMERS, TMX Group, SOTI, Canadian Tire, Brookfield, Moneris. Rogers and Bell are **not** in the 105-board ATS set — keep them as separate weekly checks.

## Rate limits and caveats
- Workday CXS search endpoint is burst-limited: repeated POSTs return HTTP 422. Space calls ≥5s; a single spaced call still works. Noon harvest is the freshest Workday data available this hour.
- LinkedIn guest: `seeMoreJobPostings` API 429s after ~4 rapid queries — sleep ~25s between batches of four; list/detail pages are readable as guest via DOM.
- Workday `postedOn: "Posted Today"` is not a Canada signal — always read the `externalPath` slug/country before counting a hit.

## Recommendation for next hourly run (13:00 EST)
- Re-probe Workday tenants after the rate-limit window; prioritize entry-level **Platform Administrator / Platform Developer I** titles.
- Keep architect / contract / remote-Canada SN/SF hits in lessons, not the board, unless they match Platform Admin/Dev I targeting.
- Keep Rogers weekly (not hourly) and public-sector checks via Job Bank only.

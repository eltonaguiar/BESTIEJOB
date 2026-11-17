# JOBLESSONS_2026-11-16 20:00 EST hourly scan

## Result
**0 fresh verified Toronto ServiceNow/Salesforce jobs merged.** Every fresh SN/SF hit from today's scans was already on the board (deduped against `jobs.json` URLs). No changes to `jobs.json`, `README.md`, or `public/`, so no site rebuild or GitHub Pages redeploy this hour.

## Sources checked this run

| Source | Query/coverage | Fresh SN/SF hits | Status |
|---|---|---|---|
| LinkedIn guest fresh | ServiceNow / Salesforce / Platform Administrator / Platform Developer I — Toronto + Canada (6 queries, 266 results) | 0 new | All SN/SF-titled hits already on board (URL dedupe) |
| Workday CXS re-probe | BMO, TD, CIBC, Manulife, Interac, GDIT, Salesforce, Accenture — ServiceNow + Salesforce | 0 new | Rate-limited (HTTP 422) after 1 call; noon (12:00Z) harvest already fully deduped — all 8 Canada-path SN/SF postings on board. "Posted Today" hits were India/Gurugram only, not Canada |
| inbox/todayfeeds--2026-11-16--v1.md | Employer ATS + Job Bank today | 0 | 11 rows, all undated ("—") — merger skips undated rows; none are entry-level Platform Admin/Dev I |
| Rogers jobs (date-sorted HTML) | — | 0 | No ServiceNow/Salesforce mentions today |
| Bell (jobs.bell.ca) | — | 0 | Known empty for SN/SF — checked weekly, not hourly |
| Public sector (gojobs.gov.on.ca, jobs.gc.ca) | — | 0 | Radware-walled; Job Bank proxy returned nothing |

## Seen but not added (off-target)

- **Raas Infotek** — "SerivceNow Architect (Multiple Position)", Remote Canada, contract, ~10h ago, three architect roles (CTA, ITAM/ITOM, Multi-Domain; 6–8+ yrs, CISA/CIS/CAD certs). Verified on LinkedIn guest detail page. **Not added:** senior architect contract roles, remote Canada, outside the Platform Admin / Platform Developer I entry-level targeting.
- **Smart IT Frame** — "Salesforce Technical Architect - Strong CPQ and Revenue Cloud Advanced", Toronto, posted 2026-11-16. **Not added:** architect-level, not Platform Admin/Dev I.

## Rate limits and caveats

- Workday CXS search endpoint is burst-limited: repeated POSTs return HTTP 422. Space calls ≥5s; a single spaced call still works. Noon harvest is the freshest Workday data available this hour.
- LinkedIn guest: `seeMoreJobPostings` API 429s after ~4 rapid queries — check `status` + body digest, not just `len`, and sleep ~25s between batches of four. Search list pages and detail pages are readable as a guest via DOM (`innerText`).
- Workday `postedOn: "Posted Today"` is not a Canada signal — always read the `externalPath` slug/country before counting a hit.

## Recommendation for next hourly run

- Re-probe Workday tenants after the rate-limit window; prioritize entry-level **Platform Administrator / Platform Developer I** titles.
- Keep architect / contract / remote-Canada SN/SF hits in lessons, not the board, unless they match the Platform Admin/Dev I targeting.
- Keep Rogers weekly (not hourly) and public-sector checks via Job Bank only.

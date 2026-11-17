# JOBLESSONS_2026-11-16 21:00 EST hourly scan

## Result
**0 fresh verified Toronto ServiceNow/Salesforce jobs merged.** Every fresh SN/SF hit from this hour's scan was already on the board (URL dedupe against `jobs.json`, 6284 jobs, 6284 unique URLs). No changes to `jobs.json`, `README.md`, or `public/`, so no site rebuild or GitHub Pages redeploy this hour.

Live board verified: `https://eltonaguiar.github.io/BESTIEJOB/` HTTP 200; `jobs.json` served HTTP 200.

## Why nothing was new this hour
- The board was refreshed at ~18:10 EST (scrapedAt `2026-11-16T23:10:30.220Z`) and already carries today's (2026-11-16) Toronto postings from LinkedIn, Adzuna and Workday, e.g. **HCLTech — Salesforce Administrator — Toronto** (entry-level Platform Admin, on board), **TD Bank — Senior Solution Architect (ServiceNow) — Toronto** (on board).
- This run's web search (Indeed, Glassdoor, LinkedIn, jobs.ca, LandThatRole, Scoutify, notify.careers) surfaced the same fresh postings — all already deduped onto the board.
- Candidate LinkedIn URLs NOT on the board were checked individually and rejected as **stale**, not missed:
  - Scotiabank — ServiceNow Administrator Specialist — Toronto (posted Oct 20, ~4 weeks old, outside the 30-day window; Platform Admin targeting but too old)
  - CGI — ServiceNow Administrator/Developer — Toronto (~2 weeks old)
  - Bird Construction / Scotiabank — ServiceNow Developer (shared redirect URL, mid-level, not Platform Admin/Dev I targeting)

## Sources checked this run
| Source | Query/coverage | Fresh SN/SF hits | Status |
|---|---|---|---|
| Web search (Indeed/Glassdoor/LinkedIn/jobs.ca/LandThatRole/Scoutify/notify.careers) | ServiceNow + Salesforce + Platform Administrator + Platform Developer I — Toronto + Canada (8+ queries) | 0 new | Today's hits already on board (URL dedupe) |
| jobs.json URL dedupe | 6284 jobs; today's (2026-11-16) Toronto SN/SF postings present | 0 new | Board current through ~18:10 EST |
| GitHub Pages | eltonaguiar.github.io/BESTIEJOB/ + jobs.json | — | HTTP 200 both |

## Seen but not added (off-target / stale)
- **Scotiabank** — "ServiceNow Administrator Specialist", Toronto, Oct 20 2026. Platform Admin targeting but ~4 weeks old — outside the 30-day window. Not added.
- **CGI** — "ServiceNow Administrator/Developer", Toronto, ~2 weeks old. Stale; not added.
- **Smart IT Frame** — "Salesforce Technical Architect - Strong CPQ and Revenue Cloud Advanced", Toronto (from prior run). Architect level, not Platform Admin/Dev I. Not added.
- **Raas Infotek** — ServiceNow Architect roles, Remote Canada contract. Senior/remote, off-target. Not added.
- Various Senior/Lead/Architect Salesforce & ServiceNow roles (PwC, OSI Digital, CGI, Deloitte, Accenture, BDO, Altus Group, Medcan, Intelli-CloudWare) — mid/senior level, not entry-level Platform Admin / Platform Developer I targeting. Not added.

## Rate limits and caveats
- Workday CXS search endpoint is burst-limited: repeated POSTs return HTTP 422. Space calls ≥5s; a single spaced call still works. Noon harvest is the freshest Workday data available this hour.
- LinkedIn guest: `seeMoreJobPostings` API 429s after ~4 rapid queries — read `status` + body digest, not just `len`, and sleep ~25s between batches of four. List and detail pages are readable as guest via DOM.
- Workday `postedOn: "Posted Today"` is not a Canada signal — always read the `externalPath` slug/country before counting a hit.
- Entry-level targeting = Platform Administrator / Platform Developer I. Architect, contract, remote-Canada, and senior SN/SF hits go in lessons, not the board.

## Recommendation for next hourly run
- Re-probe Workday tenants after the rate-limit window; prioritize entry-level **Platform Administrator / Platform Developer I** titles.
- Keep Rogers weekly (not hourly) and public-sector via Job Bank only; Bell and other telco career pages are low-yield for SN/SF.
- Do not re-add stale (~2+ week) off-board candidates — they were already scanned and correctly excluded.

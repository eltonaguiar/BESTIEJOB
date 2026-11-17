# JOBLESSONS_2026-11-16 23:00 EST hourly scan

## Result
**1 fresh verified Toronto ServiceNow job merged.** This hour's aggregator scan (`scripts/daily_job_scan.mjs`) returned fresh=660 newly-discovered URLs overall (servicenow 1308 / salesforce 1371 primary; 2844 matching postings across adzuna 394, linkedin 227, greenhouse 16, smartrecruiters 12, remotive 6, ashby 2, lever 1, remoteok 1, jobicy 1). After Toronto-area + ServiceNow/Salesforce + 30-day-window + URL-dedupe against the board:

- 922 Toronto-area SN/SF rows in the scan; 905 already on the board (deduped by normalized URL).
- 17 new-to-board URLs; only **1** falls inside the board's 30-day window (2026-10-02 → 2026-11-16) and was added:
  - **Senior Lead, ServiceNow ITOM — Game Companies — Toronto, Ontario, Canada — posted 2026-10-23** (`ca.linkedin.com/jobs/view/senior-lead-servicenow-itom-at-game-companies-4490172006`) — inserted into the README ServiceNow table; ServiceNow table count 1315 → 1316.
- 16 new-to-board URLs were **outside the 30-day window** (posted 2026-10-05 to 2026-10-12) and correctly excluded per board policy ("nothing older than 30 days").

## Changes this run
- `README.md`: added the Game Companies ServiceNow row (line ~1248); bumped ServiceNow count 1315 → 1316; also fixed 1 pre-existing unparseable row (`[[C] Salesforce Engineer / Developer` → `C: Salesforce Engineer / Developer`, adzuna mlse Toronto) so the merger no longer refuses to write.
- `jobs.json` + `public/*/jobs.json`: refreshed by the scan (newThisScan 814).
- `public/jobs-data.json` + `public/index.html`: rebuilt via `tools/build_site.py` (5767 jobs, newest 2026-11-16, built 2026-11-17 04:06 UTC).
- Committed + pushed to `origin/main`: `99d0821 chore(jobs): 23:00 EST hourly scan — +1 Toronto ServiceNow job merged, README + Pages rebuilt [skip ci]`. GitHub Pages (`eltonaguiar.github.io/BESTIEJOB/`) auto-deploys from main.
- Live board verified earlier this cycle: `https://eltonaguiar.github.io/BESTIEJOB/` HTTP 200; `jobs.json` served HTTP 200.

## Why almost nothing was new this hour
- The board was refreshed at ~18:10–23:10 EST and already carries today's (2026-11-16) Toronto SN/SF postings from LinkedIn, Adzuna and Workday, e.g. **HCLTech — Salesforce Administrator — Toronto** (entry-level Platform Admin, on board) and **TD Bank — Senior Solution Architect (ServiceNow) — Toronto** (on board).
- This hour's newly-discovered SN/SF URLs were overwhelmingly re-discoveries of postings already on the board, or older (Oct 5–23) postings the aggregator had not previously indexed. Only the Game Companies role was both new-to-board and in-window.
- Entry-level targeting = Platform Administrator / Platform Developer I. The one added role is "Senior Lead" level — added because it is new-to-board and in-window, but architect/senior/lead/contract/remote-Canada SN/SF hits otherwise go in lessons, not the board.

## Sources checked this run
| Source | Query/coverage | Fresh SN/SF hits | Status |
|---|---|---|---|
| daily_job_scan.mjs aggregator | SmartRecruiters SN, Workday CXS (SF + Canadian employers), Greenhouse/Lever/Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna — SN + SF — Toronto + Canada | 1 new in-window | 905 of 922 Toronto-area SN/SF already on board; 16 new URLs out-of-window |
| Workday CXS tenant probes | Accenture, BMO, CIBC, GDIT, Interac, Manulife, Salesforce, Sun Life, TD — SN/SF Canada | 0 new | Mostly HTTP 429 rate-limited; hits either already on board (BMO ServiceNow CMDB Administrator & Technology Lifecycle Analyst since Nov 14; CIBC Senior Manager Salesforce Delivery since Nov 4; Manulife Salesforce Functional Analyst Waterloo/Toronto since Nov 2; TD Salesforce Data 360 since Nov 16) or stale |
| jobs.json URL dedupe | 6284 jobs; today's Toronto SN/SF present | 0 new | Board current through scrapedAt 2026-11-16T23:10:30.220Z |

## Seen but not added (off-target / stale / out-of-window)
- **Bell** — Senior ServiceNow Architect - Strategic Portfolio Management, Toronto, posted 2026-10-07 (adzuna). Senior/architect level; outside 30-day window. Not added.
- **Take-Two Interactive** — Senior Lead, ServiceNow ITOM, Toronto, posted 2026-10-21/22/23/24/25 (multiple URLs: LinkedIn, adzuna, greenhouse, builtin). Already on board under other URLs; not re-added.
- **Game Companies** — Senior Lead, ServiceNow ITOM, Toronto, 2026-10-23 — **ADDED** (sole in-window new-to-board hit).
- Various senior/architect/contract SN/SF roles (PwC, OSI Digital, CGI, Deloitte, Accenture, BDO, Altus Group, Medcan, Intelli-CloudWare, Scotiabank) — mid/senior level, not entry-level Platform Admin / Platform Developer I targeting; mostly already on board or stale. Not added.

## Rate limits and caveats
- Workday CXS search endpoint is burst-limited: repeated POSTs return HTTP 422. Space calls ≥5s; a single spaced call still works. Several tenants (Accenture, BMO, CIBC, GDIT, Interac, Manulife, Salesforce, Sun Life, TD) returned 429 this hour.
- Adzuna returned HTTP 503 on several `what` variants but still yielded 394 matches.
- LinkedIn guest: `seeMoreJobPostings` API 429s after ~4 rapid queries — read `status` + body digest, not just `len`, and sleep ~25s between batches of four. List and detail pages are readable as guest via DOM.
- Workday `postedOn: "Posted Today"` is not a Canada signal — always read the `externalPath` slug/country before counting a hit.
- Public sector (Job Bank / OPS): OPS blocked by Radware bot manager; no extractable postings this hour.

## Recommendation for next hourly run
- Re-probe Workday tenants after the rate-limit window; prioritize entry-level **Platform Administrator / Platform Developer I** titles.
- Keep Rogers weekly (not hourly) and public-sector via Job Bank only; Bell and other telco career pages are low-yield for SN/SF.
- Do not re-add stale (~2+ week) off-board candidates — they were already scanned and correctly excluded.
- The merger refuses to write if any dated README row is unparseable (nested-bracket titles like `[[C]...`); fix or flag those rows before the next merge.

# JOBLESSONS — 2026-11-25T07:00 EST (hourly Toronto SN/SF scan)

## Result
- **1 net-new verified fresh job** added to `jobs.json` + `README.md` + GitHub Pages:
  - **Salesforce Health Cloud Engineer** — Sanofi — Toronto, Ontario (Hybrid, 3 days onsite) — posted 2026-11-25 — req R2879457 — https://ca.linkedin.com/jobs/view/salesforce-health-cloud-engineer-at-sanofi-4494614953
  - Body-confirmed platform work: Apex, LWC, Visualforce, triggers, Flows, Omni Components, REST/SOAP integrations, Platform Events, Health Cloud managed packages. Not a sales role.
- Board after: **5,691 rows** (1,208 ServiceNow / 4,324 Salesforce); live page 5,001 cards.

## Sources scanned & yield
| Source | Volume | Net-new |
|---|---|---|
| LinkedIn guest (ServiceNow, Toronto 24h) | 60 cards, 5 SN/SF title-hits | 0 (all boarded) |
| LinkedIn guest (Salesforce, Toronto 24h) | 60 cards, 14 SF title-hits | 1 (Sanofi) |
| Adzuna CA API (ServiceNow, where=Toronto, 3d) | 31 rows | 0 |
| Adzuna CA API (Salesforce, where=Toronto, 3d) | 80 rows | 0 |
| Workday CXS TD/BMO (ServiceNow + Salesforce) | TD 13 SN / 10 SF, BMO 4 SN / 22 SF | 0 |
| Workday salesforce.wd12 (own board) | 43 rows (all sales/AE/renewals) | 0 |
| Rogers date-sorted (jobs.rogers.com) | 26 rows | 0 |
| Workday other 11 boards (bmo/td/cibc/manulife/interac/accenture) | HTTP 429 | — |

## Lessons for future agents
1. **The board is at saturation for Toronto SN/SF via aggregators.** Adzuna's `where=Toronto` + `what=ServiceNow` returns 31 rows but nearly all are *tooling-mention noise* (SAP Basis Administrator, Service Desk Analyst, GTM Ops Specialist). Only title/body-confirmed platform roles count, and every such title this hour was already boarded.
2. **LinkedIn 24h guest feed is now the main source of genuinely new rows** — but ~98% of keyword cards are noise. Of 120 cards (60 SN + 60 SF), only 1 was net-new and it came from the *Salesforce* query, not ServiceNow. Filter titles against `servicenow|salesforce|apex|lightning|ncino|agentforce` and body-check generic titles.
3. **Workday CXS is still 429-rate-limited at 12:00Z** (~4h after the :00Z CI). A 15–30s wait + single retry got TD and BMO to 200. All reachable SN/SF reqs were already boarded: BMO ServiceNow CMDB Administrator (R260030992), BMO ServiceNow Technology Lifecycle Analyst (R260030995), TD Senior Solution Architect ServiceNow (R_1521185), TD Software Engineer II Salesforce Loyalty Management Developer (R_1509038), BMO Senior Sales Force Developer (R260032445 / R260032496). Do not re-add on a "Posted Yesterday" date bump — compare against the board's postedDate.
4. **Detail-page "posted" selector is unreliable.** Sanofi's top-card showed "1 week ago" while the search card showed "1 minute ago" (just posted). Trust the *search card* relative timestamp / `f_TPR=r86400` membership for freshness, not the detail-page top-card "posted" element (it reflects a repost/refresh).
5. **Dedupe worked exactly as designed:** trailing LinkedIn job id + normalized URL + company+title caught all 19 existing hits; only the Sanofi jid 4494614953 slipped through. Keep all three signals.
6. **Pharma/digital-health is a growing Health Cloud niche.** Sanofi's new Toronto digital hub is hiring Salesforce Health Cloud engineers. Worth watching pharma/bio digital hubs (Sanofi, AstraZeneca, GSK, Pfizer, Roche) in Toronto — they post Health Cloud / Life Sciences Cloud roles that generic serviceNow/salesforce keyword scans underweight.
7. **README reconciliation:** origin advanced 3 commits (CI daily LinkedIn sweep) mid-run. Recipe that worked: `git reset --hard origin/main`, re-insert the row into the fresh `jobs.json` with *dynamic* meta counts (read current total/salesforce, +1 each — never hardcode), re-add the README section, re-run `build_site.py`, commit, push. This preserves the CI's new jobs and avoids conflict resolution on the generated `public/*` files.
8. **jobs.json textual splice:** insert the compact one-line row right after `"jobs": [` (the existing head element is already compact one-line), bump `meta.total` and `meta.primaryCounts.salesforce` by +1. `git diff --stat` stays 5 changed lines — no whole-file re-serialization.

## Partner / employer checks this hour
- Rogers (date-sorted Phenom): 26 rows, **no** ServiceNow/Salesforce titles — consistent with prior days.
- Bell: skipped (empty shell; weekly cadence per protocol).
- Government of Canada / Ontario gojobs: Radware-walled, skipped (use Job Bank title-only proxy).
- Cognizant, DXC, Accenture, Salesforce-the-company Workday: no fresh Canadian SN/SF *platform* reqs (sales/AE/support only).
- Sanofi (new digital hub): **hit** — Health Cloud engineer.

## Next-hour watchlist
- Re-probe Sanofi Toronto careers for more Digital/Patient-Services Salesforce reqs (R287xxxx series).
- Workday TD/BMO/manulife/cibc/interac — run the retry after :05Z when 429s clear.
- LinkedIn `f_TPR=r86400` ServiceNow + Salesforce + "Salesforce Administrator" + "ServiceNow Administrator" for new jids.

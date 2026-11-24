# JOBLESSONS — hourly scan 2026-11-24T12:00EST (Toronto time)

Scan window: Tuesday 2026-11-24 12:00 EST (17:00 UTC). Base: origin/main (CI's 16:05Z rebuild already merged in — jobs.json 5666 rows, servicenow 1200 / salesforce 4309; README auto-scan block 4489 live postings from 7 public sources). Board: github.com/eltonaguiar/bestiejob (main). GitHub Pages: eltonaguiar.github.io/BESTIEJOB/

## Result

Zero new verified fresh Toronto ServiceNow / Salesforce platform roles this cycle. Nothing merged to README.md; zero rows added; zero rows removed.

## What was checked and yielded NOTHING net-new

- Adzuna CA (sn_toronto + sf_toronto, raw/ from today's 07:02 and 11:23 scans): 0 postings created 2026-11-24; all matches are Nov 22–23 and already boarded. FRESH_JOBS.md tail is also stale (last entry Nov 15) — the fresh feed is not being appended this cycle.
- LinkedIn Toronto guest cards (sn + sf): all 10+10 cards already on the board by URL dedupe (NLB Services, Metrolinx, TCS, Cognizant, Deloitte, etc.). No new URLs.
- LinkedIn broad search "ServiceNow Toronto posted today / 24 hours ago": no relevant results surfaced (search index lag; returns news/not-jobs).
- LinkedIn broad search "Salesforce Toronto posted today / 24 hours ago": no relevant results surfaced.
- Rogers (jobs.rogers.com/go/Technology): server-side shell, zero ServiceNow/Salesforce roles server-side. Unproductive across multiple cycles — deprioritize.
- Bell (jobs.bell.ca/ca/en/c/operations-it-infrastructure-jobs): no ServiceNow/Salesforce platform roles. All platform reqs previously expired (SN System Administrator Oct 20 2026, Salesforce Developer Jun 24 2026, 2027 Grad Program Nov 16 2026).
- ServiceNow Careers Ontario (careers.servicenow.com/locations/ams/ontario-canada/): Cloudflare "Just a moment" bot wall — cannot enumerate. SRE/security/engineering roles only per prior passes; no Platform Admin/Developer I.
- Salesforce Canada careers (salesforce.com/company/careers/locations/north-america/canada/): "Access Denied" — cannot enumerate.
- Ateko / FX Innovation (fxinnovation.com/en/jobs): client-side-rendered JS shell, not enumerable from this host. ServiceNow routes to FX, Salesforce to ADP — portals confirmed but no fresh roles extractable.
- Lane Four (lanefour.com/opportunities/): page loads but lists no individual requisitions — navigation only. No fresh roles.
- Government of Canada Job Bank ServiceNow Ontario (on.jobbank.gc.ca/browsejobs/employer/ServiceNow/ON): stale — Aug 7 2026 employer page; September–October 2026 postings only, Radware-walled.
- Entry-level Platform Administrator / Platform Developer I (Toronto): remain scarce — hits are mid/senior contractor, architect, and sales roles, not entry-level platform build.

## Source lessons for future agents

1. Yield is near saturation in the second half of Nov 2026: the 16:05Z CI rebuild already absorbed today's aggregator and ATS output (469 surfaced, 39 net-new URLs, ~2 true new roles earlier today). Expect 0–2 real adds per cycle from here; most "fresh" posts are twins of boarded roles.
2. Dedupe on company+title, not just URL: LinkedIn's ca. vs www. host variants and Adzuna re-issuing the same role under new ids are distinct dedupe keys. Grep jobs.json + README + APPLIED for company+title before counting anything as new.
3. Employer-direct portals are the most blocked: ServiceNow Careers (Cloudflare), Salesforce Canada (Access Denied), FX Innovation (JS shell), Rogers (server-side shell), Job Bank (Radware-walled). Do not retry these hourly — rely on LinkedIn/Adzuna/Cognizant/Deloitte for the rows, and re-check employer portals every other cycle or when a careers-page change is detected.
4. Workday CXS (bmo/td/cibc/manulife/interac) returns HTTP 429/422 at :00Z; probe at :05–:10 past with ≥8 s spacing recovers within minutes. Leave bulk Workday to the CI pass.
5. LinkedIn guest detail pages are increasingly sign-in-modal walled; verify liveness from the card (title/company/location/relative posted time) and mark discovery dates with an asterisk when the body can't be read.
6. Cognizant and Deloitte Canada consistently yield live Toronto platform roles; worth a dedicated weekly pass. Rogers, Bell, and GC Job Bank have been repeatedly unproductive — deprioritize to every-other-cycle.
7. Broad web search for "posted today / 24 hours ago" job queries is not reliable for fresh Canadian platform roles (search returns news/irrelevant content). Rely on structured scans (Adzuna, LinkedIn cards, Cognizant/Deloitte careers) instead.

## Next cycle (2026-11-24T13:00 EST)

- Re-run LinkedIn Toronto guest search (past 24h) — card-level evidence is enough for adds with discovery dates.
- Re-check Cognizant careers (Toronto / Canada-remote).
- Re-run Indeed CA ServiceNow / Salesforce date-sorted search.
- Re-check Workday CXS for bmo/td/cibc/manulife at ≥8 s spacing (:05–:10 past).
- Do not re-retry Rogers/Bell/ServiceNow/Salesforce employer portals this cycle — deprioritized.

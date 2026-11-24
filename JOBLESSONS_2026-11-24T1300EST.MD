# JOBLESSONS — hourly scan 2026-11-24T13:00EST (Toronto time)

Scan window: Tuesday 2026-11-24 13:00 EST (18:00 UTC). Base: origin/main (jobs.json 5672 rows, servicenow 1203 / salesforce 4311; README auto-scan block 4489 live postings from 7 public sources). Board: github.com/eltonaguiar/bestiejob (main). GitHub Pages: eltonaguiar.github.io/BESTIEJOB/

## Result

Thirteen fresh postings verified live this cycle; merged to README.md under "Verified fresh additions — hourly scan 2026-11-24T13:00EST". All deduped by URL against jobs.json, README.md and APPLIED.md. Zero roles removed. 3 ServiceNow, 10 Salesforce.

## What was verified live (added)

ServiceNow (3):
- Galactic Minds INC — ServiceNow Specialist / Lead — Toronto, Ontario, Canada — LinkedIn card (posted 2026-11-24), detail page confirmed live via browser (guest details page loads, "ServiceNow Specialist / Lead at Galactic Minds INC — Toronto, Ontario, Canada | LinkedIn Jobs").
- OnX — ServiceNow Tech Lead — Greater Toronto Area, Canada — LinkedIn card (posted 2026-11-24), detail page loads live.
- Systematix — ServiceNow ITSM Development Lead — Canada — LinkedIn card (posted 2026-11-24), detail page loads live.

Salesforce (10):
- Highspring — Salesforce Developer — Toronto, Ontario, Canada — LinkedIn card (posted 2026-11-23), detail page confirmed live ("Salesforce Developer at Highspring — Toronto, Ontario, Canad…").
- Cognizant — Salesforce Business Analyst manager — Toronto, Ontario, Canada — LinkedIn card (posted 2026-11-23), detail page loads live.
- Highspring — Salesforce Program Manager — Quebec, Canada — LinkedIn card (posted 2026-11-24), detail page loads live.
- iA Financial Group (Industrial Alliance) — Lead technique Salesforce — Québec, Quebec, Canada — LinkedIn card (posted 2026-11-24), detail page loads live.
- Campus4Tech — Salesforce Business Analyst — Canada — LinkedIn card (posted 2026-11-23), detail page loads live.
- CGI — Sr. Salesforce Business Analyst (FSC) — Toronto, Ontario, Canada — LinkedIn card (posted 2026-11-23), detail page loads live.
- Avanciers Inc. — Salesforce Marketing Cloud Senior Developer — Toronto, Ontario, Canada — LinkedIn card (posted 2026-11-23), detail page loads live.
- Brainhunter Systems Ltd — Salesforce Business Analyst — Toronto, Ontario, Canada — LinkedIn card (posted 2026-11-23), detail page loads live.
- Intact Financial — Senior Back-End Email Developer (Salesforce Marketing Cloud) — Toronto, Ontario — Adzuna CA (created 2026-11-22); liveness via Adzuna API `created` date + title/platform match (detail page behind CloudFront 403).
- Cognizant — Salesforce Tech Lead (Remote) — Toronto, Ontario — Adzuna CA (created 2026-11-22); liveness via Adzuna API `created` date + title/platform match.

## What was checked and yielded NOTHING net-new

- Rogers (jobs.rogers.com): server-side shell, zero ServiceNow/Salesforce platform roles server-side. Unproductive across multiple cycles — deprioritize.
- Bell (jobs.bell.ca / LinkedIn cards): ServiceNow System Administrator req 4476350097 and Salesforce Developer req 4417352458 are older postings; no fresh live platform role.
- ServiceNow Careers Ontario (careers.servicenow.com/locations/ams/ontario-canada/): Cloudflare "Just a moment" bot wall — cannot enumerate. SRE/security/engineering only per prior passes; no Platform Admin/Developer I.
- Salesforce Canada careers: "Access Denied" — cannot enumerate.
- Atego / FX Innovation (fxinnovation.com): client-side-rendered JS shell, not enumerable from this host.
- Government of Canada Job Bank / canada.ca: ServiceNow/Toronto surfaced September–October 2026 postings only, stale; Radware-walled.
- Indeed CA ServiceNow / Salesforce date-sorted search: all matches already on the board by URL dedupe (NLB Services, Metrolinx, TCS, Cognizant, Deloitte, etc.). No new URLs.
- Entry-level Platform Administrator / Platform Developer I (Toronto): remain scarce — hits are mid/senior contractor, architect, and sales roles, not entry-level platform build.

## Source lessons for future agents

1. Yield remains low in late Nov 2026: this cycle added 13 rows, nearly all LinkedIn-card-level. Expect 0–15 real adds per cycle from here; most "fresh" posts are twins of boarded roles — always URL-dedupe against jobs.json + README + APPLIED.md first.
2. LinkedIn guest detail pages now load via browser (domcontentloaded) but render title/meta via JS — confirm liveness by page load + URL, not body text. Mark discovery dates with an asterisk when no absolute posted date exists.
3. Adzuna CA detail pages return CloudFront 403 from this host — treat a 403 as a bot-wall on a live posting, not dead; establish liveness via the Adzuna API `created` date plus title/platform/company match.
4. Cognizant and Deloitte Canada consistently yield live Toronto platform roles; Highspring, CGI, Avanciers, Brainhunter, iA Financial Group, Campus4Tech are also producing. Worth a dedicated weekly pass.
5. Rogers, Bell, Government of Canada Job Bank, ServiceNow Careers, Salesforce Careers have been repeatedly unproductive (nothing fresh, expired, already on board, or bot-walled) — deprioritize to every-other-cycle unless a careers-page change is detected.
6. Dedup by URL is effective: none of the 13 added rows were already on the board despite similar titles being present (e.g. iA Financial "Lead technique Salesforce" 4494150998 vs boarded "Salesforce Technical Lead" 4494149845 — different req IDs, distinct roles).

## Next cycle (2026-11-24T14:00 EST)

- Re-run LinkedIn Toronto guest search (past 24h) — card-level evidence is enough for adds with discovery dates.
- Re-check Cognizant careers (Toronto / Canada-remote).
- Re-run Indeed CA ServiceNow / Salesforce date-sorted search.
- Re-check Workday CXS for bmo/td/cibc/manulife at ≥8 s spacing (:05–:10 past).
- Do not re-retry Rogers/Bell/ServiceNow/Salesforce employer portals this cycle — deprioritized.

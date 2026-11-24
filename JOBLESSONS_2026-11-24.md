# JOBLESSONS — hourly scan 2026-11-24 (Toronto time)

Scan window: Tuesday 2026-11-24 00:01 EST (05:01 UTC). BestieJob hourly cron run.
Board: github.com/eltonaguiar/bestiejob (main). GitHub Pages: eltonaguiar.github.io/BESTIEJOB/

## Result
7 fresh postings verified live and added to README.md under "Verified fresh additions — hourly scan 2026-11-24T05:01EST". All deduped by URL against jobs.json, README and APPLIED.md. Zero roles removed. 3 ServiceNow, 4 Salesforce.

## What was verified live (added)

ServiceNow:
- Deloitte — Lead Specialist, ServiceNow CMDB Solution Architect — Remote in Toronto, ON (Ottawa also) — $85,000–$156,000 — Indeed jk=8481424a81ab3122 (Reference 135342). CSDM, Discovery, Service Mapping, IntegrationHub ETL. Deloitte = ServiceNow Global Elite partner.
- Deloitte — Senior Consultant, ServiceNow Platform (DTC) — Hybrid Toronto (Bay Adelaide East) — $69,000–$114,000 — Indeed jk=159ae9b051d0cc56 (Reference 133759). Flow Designer, scripting, integrations, ITSM/HRSD/WSD/CMDB/IRM.
- CGI — ServiceNow Administrator/Developer — Hybrid Toronto (250 Yonge St) — $80,000–$130,000 — Indeed jk=cf4ffdcf78006e60. CSA+CAD+CIS mandatory; Business Rules, Script Includes, UI Policies, Client Scripts.

Salesforce:
- Cognizant — Salesforce QA Automation Engineer (Salesforce QE) — Canada Remote, Ontario preferred — $74,000–$98,000 — Posted 2026-11-23, applies until 12/20/2026 — careers.cognizant.com/.../00071207741. LWC, Apex triggers, Flows, test automation. VERY fresh (posted yesterday).
- Cognizant — Salesforce nCino Developer — Hybrid Toronto — $100,000–$130,000 — Posted 2026-11-13, applies until 12/15/2026 — careers.cognizant.com/.../00070679681. Apex, LWC, OmniStudio, nCino banking.
- Dentalcorp — Salesforce Administrator/Developer — Toronto (181 Bay St), hybrid Mon–Thu onsite — CA$87,000–CA$103,000 — Listed ~7 days ago (≈2026-11-17) — Workday JR26988 (found via revopsroles mirror). Requires Salesforce Apex development = build role.
- Deloitte — Senior Consultant, Salesforce Platform (DTC) — Hybrid Toronto — $69,000–$114,000 — Indeed jk=ed77066feb39f0cc (Reference 133770). Flows, Apex, Lightning components, API/event integrations.

## What was checked and yielded NOTHING net-new
- Scotiabank Salesforce Developer (Req 265131 / 603559617) and Sr Dev/Architect (Req 265640 / 604373417): careers page says "not accepting any further applicants" — CLOSED. Do not add.
- Cognizant Salesforce nCino Developer is new to board; the Sr Dev/Architect Scotiabank req was already on board.
- Indeed ServiceNow Administrator Ontario and Salesforce Administrator Toronto search pages: several listings surfaced but all either already on the board (KPMG Manager SN Technical Lead jk=8c270c710f6166a5; Intact SFMC jk=...) or are the Deloitte/CGI roles added above.
- Rogers, Bell, Atego/FX Innovation, Canada Life: no fresh live platform roles (Bell's open SN roles are Oct 28–30 postings already on board).
- TD Bank: JobBank Salesforce Software Engineer II advertised until 2026-02-22 (expired).
- BMO/TD/CIBC/Manulife Workday CXS probes: HTTP 422/429 (site names need re-discovery via careers pages).
- Government of Canada / Ontario public-sector portals: nothing fresh.
- LifeLabs ITSM Practice Lead (adzuna 5974915847): truncated API description, no platform-build evidence — held as lead, not added.

## Source lessons for future agents
1. Indeed `viewjob?jk=...` detail pages ARE fetchable and show full duties + location + pay, but usually NO posted date. Mark those rows with the discovery date and an asterisk; never fabricate an issuer posted date.
2. Cognizant careers pages are fully fetchable, show `Date published` and `Applications accepted until` — a strong, dateable source. Re-check Cognizant Toronto/Canada remote listings frequently.
3. RevOps Roles mirrors Workday jobs with full descriptions; use the Workday apply URL as the canonical posting URL (employer/ATS evidence beats a mirror), credit RevOps Roles as discovery source.
4. Scotiabank careers returns an explicit closed message ("not accepting any further applicants") — always fetch the detail URL before adding; a search hit is not liveness evidence.
5. Indeed search pages are fetchable but individual `jk` values change per session; capture the `jk` from the search-result link, not a guessed viewjob ID.
6. Deloitte (ServiceNow Global Elite partner) and Cognizant consistently yield live Toronto platform roles; worth a dedicated weekly pass.
7. Rogers / Bell / Government of Canada portals have been repeatedly unproductive across multiple cycles (nothing fresh, expired, or already on board) — deprioritize to every-other-cycle unless a careers-page change is detected.
8. Dedup by URL remains effective; the Deloitte ServiceNow Platform Consultant and Cognizant nCino roles were NOT on the board despite similar titles already present (different req IDs).

## Next cycle (2026-11-24T06:00 EST)
- Re-check Cognizant careers (new Salesforce QE posted Nov 23 suggests active posting).
- Re-run Indeed ServiceNow/Salesforce Toronto with `sort=date` to catch same-day postings.
- Re-discover Workday CXS site names for bmo/td/cibc/manulife via their careers pages.
- Re-check Deloitte Canada platform openings (CMDB/Platform/Salesforce tracks).

# Four named employers, their associates, and ServiceNow — 2026-11-10

Requested by name: Canada Life, UNC Health, Air Force Research Laboratory (AFRL),
AIT Worldwide Logistics. Each sits on a different ATS, and none of the four was
in our 455-board registry. Method: hit each employer's own board directly
(curl, then headless Chrome where the site blocks curl), read the posting list,
and search every board — including associate boards — for "servicenow".

## Canada Life — SAP SuccessFactors, `jobs.canadalife.com`

Board reports 86 postings; 64 distinct rows parsed across the four list pages
(the rest fall outside the paged markup). Canada's largest insurer, so this is
the one employer here with genuinely Canadian supply: Toronto, London,
Mississauga, Winnipeg, Montreal, Calgary, Halifax, Kitchener.

IT-relevant live postings:

| Role | Location | Path |
|---|---|---|
| Solutions Architect — App Enablement Lead | Toronto | `/job/Toronto-Ontario-Solutions-Architect-App-Enablement-Lead…` |
| Solutions Architect — Enterprise Content Management | Toronto | `/job/Toronto-Solutions-Architect-Enterprise-Content-Manageme…` |
| Manager, Application Security | Toronto | `/job/Toronto-Ontario-Manager%2C-Application-Security-ON-M5T-…` |
| Senior Data Platform Engineer | London | `/job/London-Senior-Data-Platform-Engineer-ON/1452685333/` |
| Intermediate Data Analyst (12-month term) | Winnipeg | `/job/Winnipeg-Manitoba-Intermediate-Data-Analyst-Value-Partn…` |
| Finance Data Analyst | Kitchener | `/job/Kitchener-Ontario-Finance-Data-Analyst-ON-N2P-2G5/…` |
| Bilingual Data Integrity Specialist (6-month) | London | `/job/London-Bilingual-Data-Integrity-Specialist…` |

**ServiceNow: none live.** `jobs.canadalife.com/search/?q=servicenow` returns the
search shell with the "no results" marker and a single `/job/` link (the
template's own), so the count is zero, not unread. Two expired postings show the
platform is used in-house, both from London ON and both closed: *IT Business
Systems Analyst* (posted 2026-09-09, required ServiceNow ITSM + Salesforce) and
*Senior Disaster Recovery Analyst* (posted 2026-10-05, ServiceNow BCM/SNOW).

## UNC Health — Phenom-style board, `jobs.unchealthcare.org`

~1,580 openings, overwhelmingly clinical. The board answers curl with 403 and
needs a real browser, which is why it has never shown up in our sweeps.

**ServiceNow: no platform roles, but ServiceNow is the operational backbone of
their shared-services HR group in Morrisville NC.** Three live postings name it
as a daily tool rather than a build target:

- *HR Service Delivery Advisor I* — `/jobs/18390985-hr-service-delivery-advisor-i`
- *HR Data Analyst — HR Systems Operations* — `/jobs/18030985-hr-data-analyst-hr-systems-operations` (ServiceNow + iNFOR preferred)
- *HR Operations Specialist* — `/jobs/17843077-human-resources-operations-specialist`

The board also carries an explicit *Information Technology* category
(`/search/information-technology/jobs`), whose visible listing included
*Information System Specialist — Credentialing* (Job ID 214795, Morrisville).

## Air Force Research Laboratory — Yello, `airforcestem.yellogov.com`

41 postings on the board (25 parsed from the first page). US-citizenship roles at
Dayton OH (Wright-Patt), Albuquerque NM, Rome NY, Rosamond/Edwards CA.

**ServiceNow: none.** Zero occurrences of "servicenow" on the board; two
"salesforce" mentions. Computing-adjacent live roles read as research and
program management, not platform administration: *Digital/IT Platform Product
Owner for Classified Systems*, *AI Agentics Scientist / Computer Engineer*
(Rome NY), *Associate Computer Engineer*, *Laboratory Development Engineer*.

## AIT Worldwide Logistics — iCIMS, `careers-aitworldwide.icims.com`

83 open roles, 8 posted in the last 7 days, every US location (IL, TX, GA, NJ,
CA, MA, MI, MN, MO, KY, IN, PA, NY, AZ, FL). iCIMS answers curl's search with
405 and renders results from embedded data, so the row list here comes from
search-engine captures of the same board: *Business Systems Analyst* (ID
2026-8155), *Manager, Global Change Management* (2026-8213, Itasca IL),
*Sr. Pricing Analyst* (Fairburn GA), plus the operations/warehouse bulk.

**ServiceNow: none found** — the IT category on the US board and the EMEA board
were both searched, zero hits.

## Known associates, and what each one returned

| Employer | Associates checked | Result |
|---|---|---|
| Canada Life | Great-West Lifeco group: **Irish Life** (`life-careers.com/canadalife`), Canada Life UK, Empower, Putnam | Irish Life: 0 ServiceNow (same empty-result marker). Group requisitions surface on Canada Life's own board, branded "\\| Great West" (e.g. *VP, Chief Internal Auditor \\| Great West*, *Assistant Manager, Corporate Financial Reporting \\| Great West*). Empower's board did not render — **unverified**. |
| UNC Health | 15 member entities: UNC Medical Center, Hillsborough, Rex, Rex Holly Springs, Rockingham, Pardee, Nash, Wayne, Johnston, Caldwell, Chatham, Southeastern, Lenoir, Blue Ridge, Appalachian Regional, plus UNC Faculty Physicians, UNC Health Alliance, Shared Services | All share the one board, so the ServiceNow verdict above covers them. Note *NC Health (Rex Healthcare, Inc.)* is the private subsidiary that employs the Morrisville shared-services staff. |
| AFRL | Air Force Civilian Service (`afciviliancareers.com`), AFMC/AFOSR, HJF (contractor running AFRL's CHEERS program), DAGSI | AFCS: 0 ServiceNow. HJF: page rendered without job rows — **unverified**. DAGSI/AFOSR are fellowship programmes, not standing requisitions. |
| AIT | EMEA iCIMS board (`emea-external-aitworldwide.icims.com`), AIT Truckload Solutions category, station network | EMEA: 0 ServiceNow, 18 roles (Amsterdam, Zurich, Berlin, London, Tel Aviv). Truckload Solutions is a category on the US board, no SN. |

## Bottom line

No live ServiceNow requisition at any of the four or their checked associates
today. Canada Life is the only one whose roles a Canadian-based candidate can
take without US work authorisation, and its IT openings are architect/analyst
work on Azure, ECM and data platforms rather than ServiceNow; the SN-adjacent
history there is real but both postings have closed. UNC Health and AIT are
worth watching for the pattern "ServiceNow as a tool inside HR/IT operations"
rather than "ServiceNow developer" — that phrasing is what their boards actually
carry.

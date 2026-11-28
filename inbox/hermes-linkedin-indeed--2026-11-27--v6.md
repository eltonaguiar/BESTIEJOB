<!-- merged: pending -->
---
model: hermes-desktop (cdp, user's logged-in Chrome :9223)
scanned_at: 2026-11-27T18:40:00Z
task: servicenow-linkedin-indeed-crawl
---

# ServiceNow crawl — LinkedIn + Indeed, 2026-11-27

Authenticated crawl of the user's own Chrome (CDP 9223). 77 unique postings collected
(54 LinkedIn / 23 Indeed, 51 companies); **71 were already on the board**, so only the
rows below are new. Every date is the ISO date the page itself published — no row here
was backfilled or inferred.

On-topic filter: the posting BODY was fetched in-page for each ambiguous row and checked
for "ServiceNow". Three candidates were dropped on that evidence — `BMC Consultant`
(Flexstaf) is BMC Remedy/Helix, `Senior OT SOC & Systems Integration` (Quantum) is
security-operations, and one Indeed row returned 401 with no readable body.

| Posted | Role | Company | Location | Source |
|---|---|---|---|---|
| 2026-11-27 | [ServeiceNow Developer-PSDS](https://ca.linkedin.com/jobs/view/serveicenow-developer-psds-at-accion-labs-4493884979) | Accion Labs | Canada | LinkedIn, query "ServiceNow developer" |
| 2026-11-26 | [Platform Architect](https://ca.linkedin.com/jobs/view/platform-architect-at-tata-consultancy-services-4495032427) | Tata Consultancy Services | Toronto, ON | LinkedIn, body confirms ServiceNow |
| 2026-11-18 | [Access Management Automation Analyst - Information Technologies](https://ca.linkedin.com/jobs/view/access-management-automation-analyst-information-technologies-at-university-of-calgary-4491535560) | University of Calgary | Calgary, AB | LinkedIn, body confirms ServiceNow |
| 2026-11-27 | [ServiceNow Developer](https://ca.linkedin.com/jobs/view/servicenow-developer-at-tekstaff-it-solutions-4495855206) | TekStaff IT Solutions | Toronto, ON | LinkedIn, query "ServiceNow developer" |

Note on the first row: the "ServeiceNow" spelling is the posting's own typo, kept verbatim
rather than corrected, so it stays matchable against the source.

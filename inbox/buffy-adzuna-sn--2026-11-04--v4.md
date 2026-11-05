<!-- merged 2026-11-05T014508Z: +2 new, 9 duplicate, version 2 -->
---
model: buffy
scanned_at: 2026-11-04T22:52:00Z
task: adzuna servicenow capacity probe + paced SN pass
api_calls: 28
---

# Adzuna ServiceNow pass — 2026-11-04

Capacity first: 28 paced calls (2.5 s apart, ~24/min) returned **28× HTTP 200, zero 429s**.
Earlier scans in `logs/job_scan.log` hit 429s under burst fan-out, so the ceiling is a
per-minute/burst limit, not an exhausted daily quota.

Queries: 19 ServiceNow angles × Toronto/Canada + `servicenow` in Mississauga, Ottawa,
Vancouver, Calgary, `servicenow platform|lead|remote` across Canada, `service now`,
`itsm analyst`. 152 results were already on the board; 12 were outside Canada/GTA.

Rows below are dated because Adzuna's `created` field is absolute. Every one was checked
against the ad text for ServiceNow/ITSM scope — the two mislabelled ones are flagged in
the note column.

| Posted | Role | Company | Location | Source |
|---|---|---|---|---|
| 2026-10-29 | [ServiceNow IRM Architect (CA$100–150/hr)](https://www.adzuna.ca/details/5946009468) | Dacaro Services | Toronto, ON | adzuna — posted as "Software Engineering Consultant", ad text is SN IRM architect |
| 2026-10-21 | [RQ00793 — Project Manager/Leader, Senior (ITSM operating models, CMDB, SPM)](https://www.adzuna.ca/details/5936605736) | Flexstaf IT | Toronto, ON | adzuna — Ontario public-sector req, SN APIs + DPRM integration |
| 2026-10-31 | [RQ00727 — Business Analyst, Intermediate (GRC/IRM, CMDB, APM)](https://www.adzuna.ca/details/5948023941) | Source Code | Toronto, ON | adzuna — SN GRC/IRM requirements |
| 2026-10-31 | [IT Operations & CMDB Analyst](https://www.adzuna.ca/details/5948258787) | Purolator | Mississauga, ON | adzuna |
| 2026-10-24 | [ServiceNow Manager](https://www.adzuna.ca/details/5940716920) | Ledcor | Calgary, AB | adzuna |
| 2026-11-04 | [Manager, IT Service Management (ITSM)](https://www.adzuna.ca/details/5953261357) | Workplace Safety and Insurance Board | Canada | adzuna — WSIB req mirrored across 4 regions |
| 2026-11-02 | [Manager, IT Service Management (ITSM)](https://www.adzuna.ca/details/5950814153) | Workplace Safety and Insurance Board | Mississauga, ON | adzuna — same WSIB req, Peel listing |
| 2026-11-02 | [Manager, IT Service Management (ITSM)](https://www.adzuna.ca/details/5950814284) | Workplace Safety and Insurance Board | Hamilton, ON | adzuna — same WSIB req, Hamilton listing |
| 2026-11-02 | [Manager, IT Service Management (ITSM)](https://www.adzuna.ca/details/5950814023) | Workplace Safety and Insurance Board | London, ON | adzuna — same WSIB req, London listing |
| 2026-10-29 | [ITAM Governance Analyst](https://www.adzuna.ca/details/5946008454) | Insight Global | Toronto, ON | adzuna — repost of the 10-25 ad below |
| 2026-10-25 | [ITAM Governance Analyst](https://www.adzuna.ca/details/5941206005) | Insight Global | Toronto, ON | adzuna |

## Checked and left out on purpose

- **ServiceNow (the vendor) engineering roles** — Senior ML Engineer, Staff Incident Response
  Engineer, two Senior Staff Cloud Security Engineers, Staff Information Security Analyst,
  Staff Compliance Analyst. Real postings at ServiceNow Canada, but they hire engineers for
  the product, not people to administer the platform. Kept out of the ServiceNow table.
- **Sr. Consultant, Value Excellence** (ServiceNow, 3 listings: 10-29, 10-31, 11-01) — vendor
  professional-services consulting, no platform scope in the ad text.
- **Implementation Specialist (English/Spanish)** (SysAid, 10-30) — ITSM, but SysAid's product.

Raw snapshot with all 28 responses' matches: `raw/adzuna_sn_2026-11-04.json`.

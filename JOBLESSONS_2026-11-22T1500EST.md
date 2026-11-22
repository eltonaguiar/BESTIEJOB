# JOBLESSONS_2026-11-22T1500EST — hourly Toronto ServiceNow / Salesforce scan

Run: Sunday 2026-11-22 15:00 EST (20:02Z). Cron job, no user present.
Repo: eltonaguiar/BESTIEJOB, branch main (synced with origin before starting).

## Scan results

Sources run (node scripts/daily_job_scan.mjs):
- Adzuna CA API — 35 queries (servicenow/salesforce variants × Toronto, Ottawa, Mississauga, Canada; ITAM/CMDB/ITSM reporting variants): 196 cards
- LinkedIn guest search — 14 queries × Toronto/Canada (+24h fresh pass): 160 cards
- SmartRecruiters (ServiceNow): 12; Greenhouse (8 boards): 12; Lever (3 boards): 1; Ashby (3 boards): 2
- RemoteOK/Jobicy/Remotive: 6
- Workday CXS (10 tenants × servicenow/salesforce): HTTP 429 on every board during the scan (the :00Z rate-limit window; see note below)

Scan merge: fresh=389 URLs seen, merged=5632 rows in jobs.json (SN 1,193 / SF 4,282).

## Dedup outcome — 0 net-new roles

Diffed the scan's new URLs against origin/main:jobs.json: 36 newly-seen URLs, but company+title comparison shows every one is a twin of a role already on the board:

- 35 are Adzuna/LinkedIn mirror re-issues of tracked roles (Adzuna re-issues the same req under a new details id — e.g. Amicis "ServiceNow Business Analyst" 5972002660 → 5972983023 pattern seen before). Board already carries these roles under other URLs; they render on the live page under the surviving card, so no new card results.
- Manual post-:00Z Workday retry (bash curl loop, 10 known tenant|site pairs, 9s spacing, Content-Type+Accept+Origin only, --compressed): all 20 calls HTTP 200, but every Canada-relevant hit was a company+title twin already on board:
  - BMO ServiceNow CMDB Administrator (Toronto) — already tracked via BuiltIn Toronto + LinkedIn + Adzuna (Bank of Montreal)
  - Interac Senior Business Systems Analyst (ServiceNow) — already tracked (adzuna 5970622713 / 5953261445)
  - Interac Quality Engineering Senior Specialist (ServiceNow Platform) — already tracked (LinkedIn 4465182167)
  - Everything else returned was US (Chicago, Mount Laurel, AFB bases), Philippines (Quezon City/Makati), or India — out of scope.

Net new Toronto SN/SF roles this scan: **0**. Nothing merged into jobs.json, README.md tables, or jobs-data.json; no GitHub Pages deploy required. This matches the 14:00 EST lessons-only precedent (commit c470418).

## Partner / Elite Partner / sponsor / government check (this run)

- Rogers: jobs.rogers.com Phenom board = server-side shell, zero job rows (raw/rogers_1900_sn.html, raw/rogers_1900_sf.html). Rely on LinkedIn/Adzuna for Rogers rows; do not retry hourly.
- Bell: jobs.bell.ca = 0 reqs for servicenow/salesforce (browser shows (0)); re-check weekly, not hourly. Bell-backed SN hiring appears under Ateko / FX Innovation — ateko.com/en/careers is a JS WordPress shell with no server-side job rows (only a link to fxinnovation.com/en/jobs).
- Canadian government portals (jobs.gc.ca, gojobs.gov.on.ca): Radware-walled; Job Bank used as proxy. Today's fresh_ca sweep: Job Bank 12 pages, Eluta 6 pages, 0 rows. Only trust Job Bank hits whose title names the platform.
- Already on the board from government/public-sector work: RBC "Senior ServiceNow Discovery & Service Mapping Engineer" (Toronto, LinkedIn 11-20 + Adzuna 11-14), Deloitte "Salesforce Consultant, GoC focus" (Ottawa, in README Salesforce table), Salesforce Careers "Technical Architect / Senior Technical Architect - PubSec (Canada)" JR353468 (README 11-04). Salesforce.com careers JR355276 (Senior Technical Consultant - PubSec) is the same role family — covered by JR353468 row.
- Partner/Elite Partner coverage already inside the scan: Accenture (Workday wd103 AccentureCareers), NeuraFlash (Greenhouse), Benevity/Loopio (Ashby), EQ Bank/Alimentiv/Versapay (Lever), GDIT/BMO/TD/CIBC/Manulife/Interac/CAAT Pension/Salesforce (Workday CXS).

## Working tree

jobs.json, README.md, FRESH_JOBS.md and public/jobs.json copies reverted to origin/main (scan churn was mirror URLs only — no role additions). Untracked raw/ and inbox artifacts left untouched. Only JOBLESSONS_2026-11-22T1500EST.md is committed ([skip ci]).

## Guidance for the next hourly run

- Workday CXS is rate-limited around :00Z; a manual retry 3–4 minutes after :00Z at 8–9s spacing returns 200 on all known Canadian tenants (bmo, td, cibc, manulife, interac, caatpension, gdit, salesforce, accenture, bdo).
- Do not re-add company+title twins just because the URL is new; the role already renders under the surviving card.
- Hourly value at :00 EST comes from Adzuna (date-sorted, max_days_old=14) and LinkedIn fresh pass (f_TPR=r86400); Workday freshness is carried by the CI hourly pass.

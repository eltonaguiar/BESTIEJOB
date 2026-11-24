# JOBLESSONS_2026-11-24T1500EST

Hourly cron scan, Toronto ServiceNow / Salesforce, 2026-11-24 15:00 EST (Toronto, UTC-05).

## What ran
- LinkedIn guest search (past 24 h): "ServiceNow Salesforce" Toronto (381 cards) and ServiceNow-only Toronto (292 cards).
- Dedup baseline: jobs.json holds 5,637 rows; combined with README links = 6,286 known URLs.
- Employer-direct: Rogers jobs.rogers.com Technology; Bell jobs.bell.ca Technology; Lane Four opportunities; NewRocket careers; Government of Canada Job Bank + Eluta.

## Verified fresh (added to README.md)
1. Senior Salesforce Developer — BMO — Scarborough, Ontario, Canada — LinkedIn req 4494172759 — "2 hours ago" at scan time; hybrid, 2 days onsite downtown Toronto; 3–5 years on the Salesforce Lightning platform (Apex, LWC, Flows, Aura, declarative/metadata-driven development); Risk Management portfolio. Genuine platform build work.
2. Senior Salesforce Developer — BMO — Toronto, Ontario, Canada — LinkedIn req 4494175406 — same profile, downtown Toronto.
Both are discovery-date rows (2026-11-24, asterisked per board policy) because the listings state no absolute posted date. Neither was in jobs.json — the feed scrape at 14:10 EST preceded them.

## Checked, not added
- S M Software Solutions RQ10997 "Software Developer – CRM – Intermediate" (Toronto, onsite, started 2026-05-01) — Oracle Siebel CRM (IP18, Siebel Tools), not the Salesforce/ServiceNow platform → out of scope.
- Agility IT Senior ServiceNow Technical Consultant – ITSM/IRM, "14 minutes ago" — LinkedIn sign-up wall, body unreadable from this host → unverifiable lead, deliberately not added.
- Lane Four Salesforce Consultant / Administrator postings — pages carry no job body server-side → leads only.
- National Consultants Professionals "Service Management (MSP Governance & ITIL Operations Lead)" — no platform keyword in title; not scoped without a body check (deferred).

## Employer-direct results this cycle
- Rogers: no platform roles (sales/ops cards only).
- Bell / Ateko: ServiceNow and Salesforce reqs expired or filled.
- Lane Four / NewRocket: no verifiable open platform reqs from this host.
- Job Bank / Eluta: radware-walled; surfaced postings were September–October 2026 (stale).
- ServiceNow Careers: Cloudflare bot wall.

## Patterns / lessons for future scans
1. LinkedIn guest search is the freshest Toronto signal (relative ages down to "14 minutes ago"); the jobs.json feed scrape (14:10 EST today) misses postings appearing right after it — re-run LinkedIn every hour even after the feed refresh.
2. Most LinkedIn detail pages are readable without sign-in; when one walls (Agility IT), record it as a lead and never add unverified.
3. Entry-level Platform Administrator / Platform Developer I (Toronto) remain scarce — another hour with zero junior surfaced; only mid/senior/lead reqs.
4. Scarborough is in the City of Toronto (in scope); Markham, Mississauga, Vaughan are not.
5. "CRM Developer" ≠ Salesforce platform — Oracle Siebel postings recur under CRM keywords; reject by body, not title.
6. Same title + distinct req IDs + distinct cities (BMO Scarborough / Toronto) = separate rows; keep both.

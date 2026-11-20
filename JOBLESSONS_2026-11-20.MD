# JOBLESSONS_2026-11-20

## Cycle summary
Hermes hourly cron, 2026-11-19 23:00 EST (2026-11-20T04:00Z). Base: eltonaguiar/bestiejob `main` at f6a45cf (README ServiceNow 1152 / Salesforce 1048 / Other 4089 = 6291 live postings, fresh window 2026-10-20 → 2026-11-19).

**Merged 0 jobs.** Every candidate was either already on the board (dedupe by normalized URL against README.md + jobs.json + APPLIED.md), undated (Lever public lists carry no posting date — merger skips undated rows by design), outside Toronto/Canada, older than the 30-day window, or not platform-build duties. Zero net-new verified jobs is a valid result; an unavailable source is not a zero.

## Sources scanned this cycle
- **scan_boards.py --read** on configured Lever ATS tenants: alimentiv (50 list entries, 3 keyword leads), eqbank (81 entries, 11 leads), versapay (28 entries, 18 leads). Output staged to `leads-live-2026-11-20.jsonl`. Lever public list payloads carry no `datePosted`, so none of these leads can carry a fresh-feed date; a detail page would be needed per role. Detail re-checks were not repeated this cycle because prior cycles already dated/rejected them (see below).
- **web_search**: "ServiceNow / Salesforce Toronto November 2026" queries plus ATS-site queries (lever/greenhouse/ashby) and employer checks for Rogers, Bell and Government of Canada.

## Duplicates / already boarded (correctly excluded)
- Procom — Salesforce Developer, Toronto, hybrid 2-month contract — https://myprocom-portal.procomservices.com/jobs/salesforce-developer-toronto-73f5a6b2 — already on README (added 2026-11-11 via cron scan 2026-11-18).
- OSI Digital — already has multiple boarded rows in jobs.json (Salesforce Lead Toronto; Salesforce Technical Business Analyst; etc.).
- Alimentiv — ServiceNow Platform Specialist, Toronto — already boarded (lever row, 2026-10-29).

## Candidates checked but NOT added
- EQ Bank — Senior ServiceNow Engineer, Toronto, hybrid — live via jobs.lever.co/eqbank/1af36346… JSON-LD datePosted 2026-09-22, outside the 30-day window.
- EQ Bank — Manager, Technology Workplace Services, Toronto — people-management duties, no ServiceNow platform build.
- EQ Bank — AI Solutions Engineer, Toronto — datePosted 2026-10-15, outside window.
- Versapay — Salesforce Developer, Canada (Remote) — jobs.lever.co/versapay/7906bc29… — live but undated on the Lever list; merger skips undated rows. US twin exists; keep the CA requisition when a date is obtainable.
- Versapay sales/account/GTM/recruiting roles keyword-flagged "Salesforce" — these *use* Salesforce, they do not *build on* it; rejected under the sales/marketing function exclusion (runbook: "Use Salesforce to manage your pipeline ⇒ reject").
- Web-search leads without an obtainable canonical employer page (OSI Digital Salesforce Developer Toronto ~7d; Konrad Salesforce Architect Toronto; Salesforce DevOps Architect Toronto/Remote Nov 11) — employer detail pages gated/JS shells this cycle; not added without an employer-verifiable date + build duties.

## Employer / partner checks (Rogers, Bell, government, Elite/select partners)
- **Rogers** jobs.rogers.com: HTTP 404 / 9-byte body (Phenom board) — known dead end; re-check weekly, not hourly.
- **Bell** jobs.bell.ca / jobs.bce.ca: Phenom client-side shells, no server-rendered datePosted; freshness unverifiable. ServiceNow Senior Technical Advisor surfaced in search but no dated posting.
- **Government of Canada** Job Bank / GC Jobs (emploisfp-psjobs.cfp-psc.gc.ca): keyword search is noise; trust only postings whose title names the platform. GC Jobs portal was under a scheduled service interruption 2026-11-15.
- **Ateko** (ServiceNow → FX Innovation careers; Salesforce → ADP career centre): both portals confirmed; no dated Toronto SN/SF vacancy captured this cycle.
- **Pentio** (Toronto Select ServiceNow partner), **Lane Four** (Salesforce), **NewRocket** (ServiceNow), **Fujitsu** (ServiceNow Elite implementation): partner profiles / sponsor showcase reviewed; no fresh Toronto req dated within window.
- **Deloitte** (Elite partner) postings via web search dated Sept–Oct 2026, outside window.

## Why nothing was added (pattern, not a failure)
Toronto SN/SF hourly scans routinely yield 0–1 net-new verified jobs. Blockers this cycle: Lever lists undated; Indeed.ca Cloudflare 403 (direct Indeed scraping dead — rely on the daily scan's Indeed/Adzuna harvest); LinkedIn guest detail sign-in-gated; Workday CXS HTTP 429 at :00Z during the concurrent CI scan; employer detail pages JS-shell/gated with no verifiable datePosted.

## Counts after this cycle (unchanged)
ServiceNow 1152 / Salesforce 1048 / Other 4089 = 6291 live postings. README.md unchanged — no rows inserted, none removed. No GitHub Pages content change this cycle beyond this lessons record committed to main.

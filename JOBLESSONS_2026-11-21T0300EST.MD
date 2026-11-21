# JOBLESSONS_2026-11-21T0300EST — Toronto ServiceNow / Salesforce hourly scan

**Run time:** 2026-11-21 03:00 EST (08:00 UTC). Cron run of the BESTIEJOB hourly scan.
**Scope:** Fresh Toronto / remote-Ontario ServiceNow and Salesforce (dev + admin) roles, plus the adjacent "Other" track. Canada-focused; known partners/Elite partners, sponsors, banks, telcos and government employers in scope.

## What this run did

1. Web-search scan: Indeed Canada (ca.indeed.com), LinkedIn guest, jobs.ca, Workday/ATS employer pages, plus employer-targeted probes for ServiceNow and Salesforce keywords × Toronto / Ontario / Canada.
   Employers probed: Rogers, Bell (incl. Ateko, backed by Bell Canada, which routes SN to FX Innovation and SF to ADP), Scotiabank, TD, BMO, CIBC, Interac, CGI, BDO, Compugen, SS&C, Lane Four, Accenture, Deloitte, TCS, Moneris, Altus, ServiceNow Inc. careers (Canada Protected B), Salesforce public-sector (jobs.ca).
2. Candidate list: 21 leads → deduped by `title||company||city` fingerprint and URL against jobs.json (5,602 jobs on origin/main, scraped 2026-11-21T06:18Z) and README.md tables (5,594 rows) → 16 not previously on the board.
3. Liveness + date verification of the strongest leads:
   - **TCS — Senior Salesforce Developer, Toronto** (jobs.ca, search snippet said "Posted Nov 19, 2026"): page now returns "This posting is no longer available". Dropped — a snippet date is not a live posting.
   - **Scotiabank — ServiceNow Developer, Toronto** (jobs.scotiabank.com .../603030017/, Req 260518): "We are currently not accepting any further applicants for this role." Closed — do not add; archive the req.
   - **BMO — ServiceNow SAM Administrator - ITAM, Toronto** (Indeed, application deadline 11/22/2026, 250 Yonge St): Indeed viewjob behind sign-in wall to headless fetch; only relative "New" label, no absolute posted date → not merged (runbook: no backfill of relative dates).
   - **BDO — ServiceNow Functional Consultant** (Workday JR6421): Workday tenant returned "service interruption" → unverified, retry next cycle rather than mark closed.
   - **Lane Four — Salesforce Consultant, Toronto**: no posting date on the page; mirror indicates 30+ days ago → outside the 30-day fresh window.
   - CGI SN Administrator/Developer, Compugen SN Developer contract, Recutify SN Lead Developer, Spectra Group SN Developer, Moneris/iVedha/Pyramid×2/Accenture SF roles: search-listing URLs or relative freshness only ("6d", "5 days ago"); no issuer absolute date obtainable → not merged.
   - **ServiceNow Inc. Canada Protected B roles** (careers.servicenow.com, posted Nov 5–17): infrastructure/SRE/security roles supporting Government of Canada workloads — not ServiceNow platform build/admin → out of the platform track per AGENT-RUNBOOK.md.
   - **Dentalcorp — Salesforce Administrator/Developer, Toronto** (181 Bay St): carryover undated lead from the 01:00/02:00 EST passes; still no absolute issuer date → stays undated, not merged.

## Result

**+0 new verified jobs merged.** Zero new verified jobs is a valid result per AGENT-RUNBOOK.md; an unavailable source is not a zero, and all sources answered.

## Patterns / lessons for future agents

- **Snippet date ≠ live posting.** TCS's jobs.ca page was removed between the search index and this verification. Verify the issuer detail page before counting any posting, and re-check shortlisted ads within 24–48 hours.
- **Roles close fast.** Scotiabank req 260518 was open in search results this cycle and closed by verification time — treat every req as perishable and archive closed/filled reqs instead of leaving them live.
- **Indeed viewjob is a sign-in wall headless.** "New" labels and application deadlines are not absolute posted dates and cannot populate the dated README tables; keep Indeed-only leads as undated inbox/watchlist rows.
- **Workday tenants can be down mid-scan.** BDO's Workday returned a service interruption — retry on the next cadence, don't mark the req closed on a 5xx/unavailable.
- **Dedupe fingerprint works.** `title||company||city` + URL caught re-advertised mirrors (e.g. Scotiabank SN Admin Specialist, Procom SF Developer, Altus SF Platform Developer already on board); Avanciers SN Implementation Architect (deadline today, Nov 21) was already on the board — don't re-post under a new scan date.
- **Named employers this cycle, no new dated Toronto SN/SF vacancy:** Rogers (SN: 0 open; SF: sales-function roles only), Bell (SN demand funnels via Ateko/FX Innovation portals, no direct req), City of Toronto / federal GC (no new SN/SF req surfaced), WSIB ServiceNow IRM manager already carried from Nov 19.

## Disposition

- README.md: unchanged — no new verified dated rows to add.
- jobs.json / public/ (GitHub Pages): unchanged; no data changed so no Pages rebuild is required for this run (Pages re-deploys on the next push to `main` touching README.md or `public/`, plus the scheduled :35 Pages workflow).
- Nothing new merged to `main`; this lessons file is the run's commit.

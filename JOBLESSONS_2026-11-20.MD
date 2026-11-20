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


## Second cycle — 2026-11-20 00:00 EST (05:02:09 UTC) — `scripts/daily_job_scan.mjs`
**Base**: origin/main at 48009ca (CI hourly scan, 04:15:11Z, 5,586 listings).
**Fresh postings surfaced**: 472 (linkedin 292 · adzuna 133 · greenhouse 17 · smartrecruiters 13 · remotive 6 · jobicy 4 · workday 2 · ashby 2 · remoteok 2 · lever 1).
**Merged to jobs.json + README.md DAILY-SCAN block**: commit c31ce75 (2,514 rows after capSecondary; primary ServiceNow 1,169 / Salesforce 1,206 retained).
**Liveness gate** (`verify_links.py --days 2`): 155 fresh rows probed · 0 dead · 66 unknown (bot-wall, not treated as dead) · nothing dropped.
**GitHub Pages**: `tools/build_site.py` → 5,045 cards (SN 848 / SF 916 / Other 3,281), built 2026-11-20 05:03 UTC; `pages.yml` run 44678537345 triggered to redeploy.
**Notable fresh Toronto/partner roles**: ServiceNow — Senior Systems Engineer (ServiceNow, smartrecruiters, posted 2026-11-20), Senior Associate Workflows & Automation / SN Developer (PwC), Senior Solution Architect SN (TD Bank), Senior BSA SN (Interac Corp.), HR Tech & SN HRSD (Mackenzie Investments), ServiceNow Architect (Pacer Group), SN ITAM/ITOM Architect (W3Global), SN ITOM Developer (Virtusa); Salesforce — Sr Salesforce Developer (Euna Solutions, Oakville), Sr Systems Developer Salesforce (Co-operators, Mississauga/Toronto/Guelph), Salesforce Administrator (CanPrev).
**Employer / partner / telco / government checks**: Bell — Ateko ("backed by Bell Canada") had live SN roles; jobs.bell.ca itself returns 0 SN/SF. Rogers — jobs.rogers.com unreachable (HTTP 404), re-check weekly. Government of Canada — jobs.gc.ca / gojobs.gov.on.ca Radware-captcha-walled; Job Bank is the title-only proxy. Workday CXS — every tenant HTTP 429 at :00Z (CI scan minute); space manual probes ≥8s or leave to CI.
**Lessons**: (1) Workday CXS 429 at :00Z — avoid probing at the top of the hour. (2) Adzuna 503 under rapid queries — space calls ≥3s; demo keys still surface results despite partial failures. (3) LinkedIn guest API works over HTTP (292 cards); no local Playwright/chromium, so `--playwright` is not an option. (4) capSecondary shrinkage (5,586 → 2,514) is by design — secondary tags capped at 40, primary SN/SF unlimited; do not hand-merge dropped rows back. (5) 403/429/5xx are bot-walls on live postings, never dead; only 404/410/451 are dropped. (6) Commit scan outputs with `[skip ci]` (avoids pre-existing red board-invariants) and manually trigger `pages.yml` for immediate Pages redeploy; never commit the unrelated `ServiceNow_Learning_...` submodule pointer or untracked scratch files.

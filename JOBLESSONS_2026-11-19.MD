# JOBLESSONS_2026-11-19

## Cycle summary
Hermes hourly cron, 2026-11-19 00:00 EST (05:00Z). Base: eltonaguiar/bestiejob `main` at a511db8 (GitHub Actions hourly scan, 05:13Z, 5481 listings).

**Merged +12 verified Toronto/Canada ServiceNow/Salesforce jobs from Dice.com** (server-rendered, scrapeable via axios+cheerio; ~31 cards/page; selectors `[data-testid="job-card"]`, title `[data-testid="job-search-job-detail-link"]`, company `[data-testid="job-card-company-name"]`, location+date `p.mb-0.text-sm.font-normal.text-foreground-light`). Queries: servicenow × salesforce × Toronto, Canada × 3 pages each. All 12 within the 30-day window (2026-10-27 → 2026-11-19), direct Dice job-detail URLs, deduped by normalized URL against jobs.json + APPLIED.md, added at head of jobs.json; meta totals recomputed (SN 1150, SF 1170, total 5493). README ServiceNow + Salesforce tables gained one row each (newest first); `tools/build_site.py` regenerated public/jobs-data.json + public/index.html; commit fc2c05f pushed to main; `pages.yml` dispatched and succeeded; live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` verified HTTP 200 carrying the new dice.com/job-detail URLs.

ServiceNow added (5):
- Sr Specialist - ServiceNow Developer — Energy Transfer — Calgary, Alberta — 2026-11-19
- ServiceNow Lead, Business Analyst — Cayuse Holdings — Remote, Canada — 2026-11-19
- ServiceNow Developer - Specialized Developer – Expert — Spectra Group — Hybrid in Toronto, Ontario — 2026-11-12
- CAM ServiceNow CAD CSA — Boston Associate Software Systems — Remote, Canada — 2026-11-13
- ServiceNow CSM/OMT Architect – 12-Month Contract — Alldus International Consulting Limited — Remote, Canada — 2026-10-27

Salesforce added (7):
- Salesforce Marketing Cloud Architect — MAVLRA CORPORATION — Remote, Canada — 2026-11-17
- salesforce cpq developer — Spiceorb — Remote, Canada — 2026-11-17 (detail JSON-LD: datePosted 2026-11-16, Location: Canada)
- Salesforce Marketing Cloud Architect (Remote) — SSV Technologies Inc — Remote, Canada — 2026-11-17
- Salesforce CPQ & Billing Developer — Spiceorb — Remote — 2026-11-12
- Salesforce Ops Consultant — JConnect Inc — Hybrid in Vancouver, British Columbia — 2026-11-12
- Salesforce CPQ Solution Engineer — Sagarsoft — Hybrid in Bolton, Ontario — 2026-11-07
- Salesforce CPQ Lead Developer - Canada — SRA Staffing Solutions LTD — Remote, Canada — 2026-11-07

## Source notes this cycle
- **Dice works.** Raw HTML via axios returns real cards; cheerio is CJS-only in ESM — `const cheerio = (await import("cheerio")).default || ...`. Most Dice "Remote" cards are US-only; verify Canada on the detail page (JSON-LD datePosted/location) before adding. Dice date strings: "Today", "Nd ago".
- **Workday CXS 429s at :00Z** during the concurrent CI hourly scan — all 14 tenant×query pairs returned HTTP 429 (bmo, td, salesforce, etc.). Confirmed again; leave Workday to the CI pass or retry 3–4 tenants at ≥8 s spacing off-peak.
- **LinkedIn guest** HTTP 429 initially, then 277 postings; healthy card HTML is ~31 KB and differs per query — test length + digest, not just status (authwall returns 200 with a static 337 KB body).
- **NoDesk is now Algolia-driven** — raw HTML fetch returns nav/promo blocks, zero job cards; the saved `li` + `h2`/`h3` selector is stale. Do not retry hourly; revisit via the Algolia API if needed.
- **Bell** `jobs.bce.ca/bell/search/?q=servicenow` renders over HTTP, but job detail pages are Phenom client-side shells with no server-rendered `datePosted` → freshness unverifiable; skipped (ServiceNow Senior Technical Advisor, Toronto, seen in search).
- **Rogers** `jobs.rogers.com` Phenom board returns HTTP 404 (9-byte body) to curl — known dead end; check weekly, not hourly.
- **Canadian government:** Job Bank full-text search is noise; trust only postings whose *title* names the platform. GC Jobs portal (emploisfp-psjobs.cfp-psc.gc.ca) was under a scheduled service interruption 2026-11-15.
- **Deloitte (Elite partner)** postings surfaced via web search are dated Sept–Oct 2026, outside the 30-day window — not added.

## Push / merge note
Origin advanced mid-run (a511db8, actions hourly scan). Resolved by branching `hermes-cron-2026-11-19` from origin/main, merging job sets programmatically (remote jobs.json + Dice adds, dedupe by normalized URL), taking README row inserts, rebuilding the site, then fast-forward `push origin hermes-cron-2026-11-19:main`. Do not force-push over the actions scan; merge instead.

## What was deliberately NOT added
- US-only Dice remote cards (East Hanover NJ, Madison WI, New York/Charlotte/Orlando/Chicago/Minneapolis, Phoenix/St. Louis/Nashville/Kansas City/Denver, Minneapolis/Detroit/Madison/Columbus/Chicago).
- EverCommerce "EverHealth — Sr Salesforce Administrator / Architect (Remote, US)" — title says US.
- Symphony "Salesforce Architect/Tech Lead — W2 Only" — W2 = US.
- Bell ServiceNow Senior Technical Advisor — no verifiable posting date.

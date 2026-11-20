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
## Cycle 2 — Hermes hourly cron, 2026-11-19 01:00 EST (06:00Z)
Base: eltonaguiar/bestiejob `main` at e7c0845 (cycle 1 Dice merge, commit fc2c05f at 05:13Z; jobs.json refreshed 05:22Z).

**Merged +5 verified Toronto/GTA ServiceNow/Salesforce jobs into README tables** (jobs.json already carried them from the 05:22Z harvest; README tables were out of sync with jobs.json — tables now synced; dedupe by URL against existing ~8,000 board URLs, all clear).

ServiceNow added (2):
- Senior Solution Architect (ServiceNow) — TD Bank — Toronto, Ontario — 2026-11-18 — adzuna.ca/details/5970077372
- ServiceNow Developer cum Architect — W3Global — Mississauga, Peel region — 2026-11-16 — adzuna.ca/details/5968012906

Salesforce added (3):
- [C] Salesforce Engineer / Developer — mlse — Toronto, Ontario — 2026-11-15 — adzuna.ca/details/5967040864
- Software Engineer III - Salesforce Data 360 — TD Bank — Toronto, Ontario — 2026-11-15 — adzuna.ca/details/5966715213
- Salesforce Senior Developer — IKO — Mississauga, ON — 2026-10-20 — iko.wd3.myworkdayjobs.com/en-US/IKO_Careers/job/Mississauga-ON/Salesforce-Senior-Developer_REQ-14036 (Workday detail shell has no server-rendered datePosted; date taken from FRESH_JOBS.md daily-scan row, inside the 30-day window)

Deliberately skipped:
- IKO Cloud Architect (Mississauga, 2026-11-13) — no ServiceNow/Salesforce evidence in title or scan row; out of scope for the SN/SF board.

Source notes this cycle:
- FRESH_JOBS.md (daily scan output, regenerated each run) is the fertile layer when direct scraping is blocked: 6 URLs absent from the board; 5 added as above, 1 skipped for relevance.
- Indeed.ca returns HTTP 403 to curl — direct Indeed scraping is dead; rely on the daily scan's Indeed/Adzuna harvest instead.
- Dice.com page-1 "Toronto" query returns mostly US remote cards; both Ontario hits (Spectra Group 11-12, Sagarsoft Bolton 11-06) were already in the board — zero new Dice adds this cycle.
- nodesk.co / jobs.canada.ca / careers.rogers.com: DNS failures or JS shells with no server-rendered cards; Bell jobs.bce.ca is a Phenom shell with no verifiable datePosted.
- Workday detail pages (e.g. IKO) render a client shell with no datePosted — pair Workday adds with the daily-scan row for the posted date.

README counts: ServiceNow 1130, Salesforce 1031, total 6190 live postings. Committed on branch hermes-cron-2026-11-19, merged with origin/main, pushed to main (no force-push); pages.yml redeploys eltonaguiar.github.io/BESTIEJOB on push to main.

## Cycle 3 — Hermes hourly cron, 2026-11-19 03:00 EST (08:00Z)
Base: eltonaguiar/bestiejob `main` at 63c0384 (README ServiceNow 1133 / Salesforce 1032 / 6206 live postings, window 2026-10-20 → 2026-11-19).

**Merged zero jobs.** Every candidate was either already on the board (dedupe by normalized URL against README + jobs.json), outside Toronto (Montréal/Québec or US-remote), undated (Lever public lists carry no date; detail JSON-LD required), older than the 30-day window, or not a platform-build duty:

- EQ Bank — Senior ServiceNow Engineer, Toronto, hybrid, datePosted 2026-09-22 (live, verified via jobs.lever.co/eqbank/1af36346… JSON-LD; predates window — not added).
- EQ Bank — AI Solutions Engineer, Technology Workplace Services, Toronto, datePosted 2026-10-15 (live, verified; predates window — not added).
- EQ Bank — Manager, Technology Workplace Services, Toronto (people-management duties, no ServiceNow build — not added).
- Versapay — Salesforce Developer, Canada (Remote), live but undated — merger skips undated rows.
- Alimentiv SN Platform Specialist Toronto — already on board (lever row, 2026-10-29).
- Ensiti two Salesforce leads — released 2026-10-05 / 2026-09-21, Montréal/Ottawa, outside window.
- Levio leads — all Montréal/Québec or undated/old.
- ServiceNow SmartRecruiters company feed page 1 — 3 Toronto hits (full-stack Experience Team, sales CPQ, cloud security); none are ServiceNow platform build/admin.
- Web-search leads (HCLTech Salesforce Administrator Nov 17; Pacer Group Salesforce FSC Developer Nov 11; Procom Salesforce Developer Nov 11; Nityo Infotech ServiceNow Architect) — all already boarded under other URLs.

Sources scanned: Dice Toronto (servicenow + salesforce, server-rendered cards — the one Toronto card, Spectra Group, was already boarded 2026-11-12; rest US-remote), Job Bank Canada keyword search (noise: indeed/Talent.com/CareerBeacon mirrors, no genuine SN/SF Toronto roles), Bell careers jobs.bell.ca (embedded `eagerLoadRefineSearch.data.jobs` JSON — keyword filter does not apply server-side; no dedicated SN/SF openings), ATS public APIs (Alimentiv, EQ Bank, Versapay, Ensiti via SmartRecruiters, Levio via Greenhouse), ServiceNow SmartRecruiters feed page 1 of 835, web-search dedupe.

Source notes this cycle:
- Indeed.ca still returns HTTP 403 to direct fetch; rely on the daily scan's Indeed/Adzuna harvest.
- Workday CXS returned HTTP 429 at :00Z during the concurrent CI hourly scan (bmo, td, salesforce tenants) — leave Workday to the CI pass or retry ≥8 s spacing off-peak.
- Bell detail pages carry no server-rendered datePosted; freshness unverifiable.

`tools/build_site.py` re-ran cleanly against the unchanged README (4971 jobs: SN 832, SF 895, Other 3244); `public/` content is unchanged, so nothing to commit for the site this cycle.

## Cycle 4 — Hermes hourly cron, 2026-11-19 22:00 EST (2026-11-20T03:00Z)
Base: eltonaguiar/bestiejob `main` at 88f3af9 (README ServiceNow 1152 / Salesforce 1047 / Other 4089 = 6290 live postings, window 2026-10-20 → 2026-11-19).

**Merged +1 verified Toronto/GTA Salesforce job into the README Salesforce table** (dedupe by normalized URL against README + jobs.json — clean).

Salesforce added (1):
- Salesforce Developer — Apex Systems — Mississauga, Ontario, Canada — 2026-11-10 — https://www.apexsystems.com/job/3058976_usa/salesforce-developer — 6-month hybrid contract, Salesforce Platform Developer I preferred; corroborated by LinkedIn guest snippet (job 4489664187, "Nov 10, 2026") and the Apex posting page.

Counts after merge: ServiceNow 1152 / Salesforce 1048 / Other 4089 = 6291 live postings. README.md committed to main; `pages.yml` redeploys https://eltonaguiar.github.io/BESTIEJOB/ on push to main.

Candidates verified but NOT added:
- Zaelab — ServiceNow FSM Architect (LinkedIn 4434135469) — expired posting (Posted 2026-07-22 / expired 2026-08-05 per earlier runs); search engines re-surface expired postings.
- EQ Bank / Equitable Bank — Senior ServiceNow CMDB Consultant (6-month contract), Toronto (LinkedIn 4144379061) — not on board but unverifiable this cycle: LinkedIn detail gated, exact-title search did not resurface it, no employer canonical page (EQ Bank Lever ATS shows other SN roles, not this one). Held as unverified lead.
- Altus Group — Salesforce Platform Developer R0014087 — already on board ×2 (2026-10-30/31).
- MLSE — Senior Salesforce Loyalty Cloud Administrator/Developer — canonical Workday Published 2026-09-30, outside the 30-day window.

Source notes this cycle:
- Indeed.ca: Cloudflare 403 (browser + curl) — direct Indeed scraping dead; rely on the daily scan's Indeed/Adzuna harvest.
- LinkedIn guest: detail pages sign-in-gated; verify via search snippets + corroborating employer/mirror pages.
- Rogers jobs.rogers.com: HTTP 404 / 9-byte body; Bell jobs.bell.ca: zero SN/SF reqs; GC Jobs / Job Bank portals Radware-walled or title-noise — re-check weekly, not hourly.
- Entry-level / Platform Developer I emphasis: Apex row matches (PD1 preferred, GTA). MLSE Built In Toronto "Entry level" tag was stale (canonical publish 2026-09-30).



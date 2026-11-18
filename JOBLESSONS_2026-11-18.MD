# JOBLESSONS_2026-11-18 — BESTIEJOB hourly cron scan (01:00 EST)

## Scan scope
- Target: fresh Toronto / Canada ServiceNow and Salesforce postings (Platform Admin / Platform Developer I emphasis for Salesforce; ServiceNow platform, CSA/CAD/CIS certs for SN).
- Freshness window: posted today / yesterday preferred (`f_TPR=r86400` equivalent where supported); hourly ATS sweep carries sub-daily freshness.
- Sources scanned: public ATS feeds — SmartRecruiters, Workday (CXS), Greenhouse, Lever, Ashby, LinkedIn (guest), remote boards, Adzuna — plus partner/employer career pages.

## Result
- Fresh Canada SN/SF postings surfaced this hour: 40 (21 ServiceNow, 19 Salesforce), posted 2026-11-16 through 2026-11-18.
- New to the board from this scan: 0 — all 40 were already present (dedupe against jobs.json + README.md held). Staged as `inbox/hermes-cron--2026-11-18--v1.md`; `check_inbox.py` OK (40 dated rows); merger reported `+0 new, 40 duplicate`.
- Board net change this run: +2 rows (from concurrent `fresh-ca--2026-11-18--v1.md` IG Wealth HRSD row and `ats-sweep--2026-11-18--v1.md` TD nCino/Salesforce row). README counts: ServiceNow 1154→1155, Salesforce 1477→1478.
- `tools/build_site.py`: OK — 5006 jobs indexed (SN 808 · SF 934 · Other 3264), 863 duplicate mirrors collapsed, 35 applied hidden, newest 2026-11-18. `public/jobs-data.json` + `public/index.html` rebuilt.

## Partner / employer look (Rogers, Bell, Canadian government, Elite/SN-SF partners)
- Rogers: `jobs.rogers.com` Phenom board unreachable (HTTP 404, 9-byte body to curl; error page in browser). Check weekly, not hourly.
- Bell: `jobs.bell.ca` renders an empty shell / shows (0) for both `servicenow` and `salesforce` in a browser — zero reqs, not a scrape failure. Re-check weekly.
- Canadian government: `gojobs.gov.on.ca` (Ontario) and `jobs.gc.ca` are Radware-walled (captcha) — do not retry. Use Job Bank as proxy; trust only postings whose TITLE names the platform (Job Bank full-text search is noise: "searchstring=servicenow" returns shipping coordinators, agronomy engineers).
- Salesforce-the-company: Toronto/Canada careers page exists, but per market shape Salesforce posts nothing below 4 days old and no Platform Admin/Dev I in Toronto — nothing fresh to add this hour.
- ServiceNow-the-company: Toronto postings are sales/SRE/security only — no platform roles this hour.
- Fresh platform work this hour came from banks (BMO/TD/CIBC Workday), DXC, and GRC/IRM consultancies (PwC ServiceNow IRM practice). Accenture Workday has 1,600+ SN reqs but effectively none Canadian on page 1.

## Source / API notes (reusable next hour)
- Workday CXS IS reachable from this host — use the `wdN` host and `curl --compressed` (without `--compressed` the gzipped body decodes as nothing). Known 200 Canadian pairs: `bmo.wd3/External`, `td.wd3/TD_Bank_Careers`, `cibc.wd3/search`, `manulife.wd3/MFCJH_Jobs`, `interac.wd3/interac`, `accenture.wd103/AccentureCareers`, `salesforce.wd12/External_Career_Site`. Dead ends this cycle: `canadalife/telus/desjardins/loblaw/kpmg/deloitte/cgi` (.wd3 → 422), `sunlife/rbc.wd3` (→ 404), `dxctechnology.wd1/dxcjobs` and `cognizant.wd1` (→ 521). Workday `postedOn: "Posted Today"` is NOT a Canada signal — read the `/job/<City>/…` slug and country before counting a hit.
- LinkedIn guest `seeMoreJobPostings` 429s after ~4 rapid queries. Use `new_tab` on the guest search URL, then same-origin `fetch('/jobs-guest/...')` from that page (no CORS, HTTP 200, full card HTML with absolute `datetime`). Always test length + md5 digest distinctness, not just HTTP 200 (authwall returns 200 with a stale 337 KB body). Sleep ~25 s between batches of four; `f_TPR=r3600` is near-empty pre-dawn EST — use `r86400`.
- Adzuna 503s after ~4 rapid queries — space calls ≥3 s. Adzuna recycles IDs: use the detail page's JSON-LD (`datePosted`/`validThrough`), not the API `created` date. Dedupe by fuzzy company (strip Inc/Ltd/Corp/Limited, compare 10-char prefix) + title tokens — plain URL/company matching misses `MLSE` vs `Maple Leaf Sports & Entertainment Partnership`.
- Dedupe rules: normalize URL (strip query string + trailing slash); LinkedIn job-id equality is a hard dedupe signal even when titles differ; vendor twins (different staffing firms advertising the same client req under the same title) are DISTINCT postings — keep both, dedupe on URL only.
- `jobs.rogers.com` / `jobs.scotiabank.com` Phenom boards unreachable this cycle. `jobs.bell.ca` = zero reqs. Gov portals Radware-walled.

## What did not change
- `jobs.json` untouched (scan rows go to README via the inbox merger; `build_site.py` unions jobs.json + README, so the page reflects both).
- `inbox/hermes-cron--2026-11-18--v1.md` left untracked (merger run without `--bump-inbox`; all 40 rows were duplicates).

### 06:00 EST run (later the same day) — 4 fresh verified jobs merged
- Diffed the 09:12 UTC `FRESH_JOBS.md` feed (2617 postings) against README.md + jobs.json by normalized URL; 7 rows posted >= 2026-11-17 were absent from both; verified each survivor on the employer canonical page or ≥2 mirrors; 4 were genuine, live, platform-track roles and were merged via `inbox/hermes-cron--2026-11-18--v2.md` (`check_inbox.py` OK; merger `+4 new, 0 duplicate`):
  - 2026-11-18 | Sr. Software Engineer (Salesforce), Specialty Health Technology | Loblaw Companies Limited | Brampton, Ontario, Canada | careers.loblaw.ca .../sr-software-engineer-salesforce-specialty-health-technology/job/PAF-LCL-D6E814FF-FBEA-41E6-8CF9-562A2B21717E_4479_1791569521_0
  - 2026-11-17 | Salesforce Techno-Functional Support Lead / AMS Lead | Accenture | Mississauga, Ontario, Canada (hybrid, 3d/wk) | accenture.com/ca-en/careers/jobdetails?id=R00364526_en
  - 2026-11-17 | Salesforce FSC Solution Architect | Maarut | Montréal, Québec, Canada | ca.talent.com/view?id=645321517787778374 (also adzuna.ca/details/5969279913)
  - 2026-11-17 | Software Engineering MTS | Salesforce | Toronto, Ontario | ca.linkedin.com/jobs/view/software-engineering-mts-at-salesforce-4490679676
- Skipped as already-covered or stale: Interac "Technical Service Now, Lead" (already on board as posted 2026-10-28 — LinkedIn "20 hours ago" is stale); Avanciers ServiceNow Implementation Architect (on board 2026-11-11); Maarut Salesforce Configuration Developer (on board 2026-11-10); Bell ServiceNow System Administrator / Senior Technical Advisor (deadlines 10/20–11/02/2026, expired) and Salesforce Developer (05/20/2026); Rogers surface hits were sales/pre-sales, not platform build; Traction Rec "Product Developer (Remote) - Ontario" is genuine Salesforce build work but BambooHR publishes no posted date, so it cannot enter the dated tables; Take-Two ServiceNow ITOM already covered; GC/CSIS Stream 10 closed 06-25-2026; CDS roles are general development, not SN/SF platform.
- Board after merge + normalize: 6601 live postings (normalize removed 3 vendor-sales rows); `board-invariants` PASS (errors=0, no ratchet kind grew); header count synced; `jobs.json` feed superset synced to README (5638 rows); `build_site.py` rebuilt, newest 2026-11-18.
- Pushed to `main` as `3b0d896` (rebased onto the 10:00 UTC hourly scan `ccae40f`); GitHub Pages deploys from `main` automatically.
- Channel updates vs 01:00 run: **Indeed.ca is blocked** (Cloudflare 403, browser and curl); LinkedIn job detail pages require sign-in — verify via search snippets + employer canonical pages; **Adzuna detail pages return CloudFront 403** — corroborate via mirrors (talent.com, lmiafinder.ca, jobrapido, workopolis). Employer canonical pages that verified cleanly today: careers.loblaw.ca, accenture.com/ca-en/careers.
- **Script fix:** `scripts/sync_readme_to_jobs.mjs` failed to parse section headings because the blurb is glued to the heading line (`### ServiceNow jobs (1159)_developer … roles_`), so it read 0 README rows and the feed missed every curated row. Patched to prefix-match `^(servicenow jobs|salesforce jobs|other jobs)/`; committed with the run.

## Next run (07:00 EST)
Re-check Traction Rec Product Developer (Ontario) for a publishable date; re-scan Accenture for sister Salesforce AMS requisitions; re-poll Rogers/Bell/GC careers portals; confirm the 4 merged roles are still live before anyone applies.

### 07:00 EST run (this run) — zero new verified jobs

- Scan method: diffed the 11:24 UTC `FRESH_JOBS.md` feed (2638 postings across Adzuna, LinkedIn, Workday, Greenhouse, SmartRecruiters, Ashby, Lever, Jobicy, Remotive, RemoteOK) against `README.md` + `jobs.json` by normalized URL and `title|company|city` fingerprint. Fresh window: posted >= 2026-11-17, Canada, ServiceNow/Salesforce track.
- Result: **0 new candidates** — every fresh Canada SN/SF row in the feed was already on the board; dedupe held. No inbox file staged, no README merge.
- `scripts/fresh_ca_scan.py` (Adzuna / Job Bank / Eluta + optional LinkedIn guest) could not complete on this host: ran twice, both timed out, no output written. Known blockers (from prior runs): Adzuna 503s under rapid queries (needs >=3s spacing), LinkedIn guest 429s after ~4 fast queries.
- Targeted web checks for today/yesterday Toronto SN/SF postings returned only aged roles (17d / 30d+ / 6 days ago); nothing fresh and unboarded.
- Partner / employer look:
  - Rogers: `jobs.rogers.com` Phenom board unreachable (HTTP 404 / 9-byte body); search hits were sales/pre-sales, not platform build. Re-check weekly, not hourly.
  - Bell: `jobs.bell.ca` empty shell / (0) reqs for servicenow and salesforce; previously found ServiceNow SysAdmin / Senior Technical Advisor and Salesforce Developer reqs had expired deadlines (10/20–11/02/2026 and 05/20/2026). Re-check weekly.
  - Canadian government: `jobs.gc.ca` / `gojobs.gov.on.ca` Radware-walled (captcha) — do not retry. Job Bank used as proxy; full-text "servicenow" search is noise. Trust only postings whose TITLE names the platform.
  - Ateko (Bell-backed SN/SF partner): careers page routes SN to FX Innovation and SF to an ADP career centre; no fresh Toronto platform posting surfaced. NewRocket / Lane Four careers pages loaded but list no fresh requisition.
  - Salesforce-the-company: no Platform Admin / Developer I in Toronto under 4 days old. ServiceNow-the-company: Toronto postings are sales/SRE/security only.
- Net board change: 0. Counts unchanged (~6601 live; ServiceNow ~1155, Salesforce ~1478). `jobs.json`, README, and `public/` already current on `main`; GitHub Pages deploys from `main` automatically, so no redeploy needed.
- Limitation: the feed covers up to ~11:24 UTC (06:24 EST); postings between then and this 07:00 run were not re-scanned because the aggregator scanner is unreliable on this host. Next run should retry `fresh_ca_scan.py` with the LinkedIn pass dropped and wider Adzuna spacing, or rely on the next scheduled daily scan.

### 08:00 EST run (this run)

- Scan method: ran `node scripts/daily_job_scan.mjs` (aggregator: Adzuna 483, LinkedIn 253, SmartRecruiters 12, Lever 1, Workday 0 — HTTP 429 on BMO/TD/Moneris/CAAT Pension/BDO/Medcan/Altus Group/IKO/Huron/Irving Oil/McKesson/Brookfield/GDIT/Resolve Tech). Regenerated `FRESH_JOBS.md` (2637 postings, SN 1154 / SF 1318), `jobs.json`, and the README `DAILY-SCAN` block (scan stamp 2026-11-18T13:02:16Z).
- Dedupe vs `README.md` + `jobs.json` (normalized URL + title\|company\|city fingerprint; posted >= 2026-11-17; Canada; ServiceNow/Salesforce track): **0 new candidates** — every fresh Canada SN/SF row already on the board. No inbox file staged, no curated-table merge.
- Curated tables unchanged: ServiceNow 1155, Salesforce 1478, Other 4039 (~6601 live). `board_invariants` not re-run (no table change).
- Commit `3f53b01` pushed to `origin/main`; `tools/build_site.py` rebuilt `public/` (4997 jobs indexed: SN 811 · SF 939 · Other 3247 · 867 duplicate mirrors collapsed · 35 applied hidden · newest 2026-11-18). GitHub Pages deploys from `main` automatically, so the live board reflects this scan.
- Partner / employer look (Rogers, Bell, Government of Canada, Elite SN/SF partners):
  - Bell (`jobs.bce.ca` Phenom): ServiceNow System Administrator / Senior Technical Advisor (Req 432824/432829, Toronto) exist but Posted Oct 6 2026, apply-by Nov 3 2026 — expired; already on board from prior runs. Not fresh.
  - Zaelab: ServiceNow FSM Architect — expired (Posted Jul 22, expired Aug 5 2026). Digital Consulting Architect CPQ — Posted Oct 2 2026, outside the 30-day window. Nothing fresh.
  - OSI Digital / PwC / Docebo / Lane Four / NewRocket / Ateko (FX Innovation): sampled roles already on board (posted Nov 2–16). No new unboarded partner requisition.
  - Rogers: `jobs.rogers.com` Phenom board unreachable (HTTP 404 / 9-byte body); search hits were sales/pre-sales, not platform build.
  - Canadian government: `jobs.gc.ca` / `gojobs.gov.on.ca` Radware-walled (captcha) — not retried; Job Bank used as proxy but full-text "servicenow" search is title-noise.
- Net board change this run: 0 new verified jobs (feed refresh only).
- Limitation: Workday Canadian hosts 429'd on this host; known dead-ends this cycle incl. canadalife/telus/desjardins/loblaw/kpmg/deloitte/cgi (.wd3 → 422), sunlife/rbc.wd3 (→ 404), dxctechnology/cognizant (.wd1 → 521). LinkedIn detail pages require sign-in — verification via search snippets + employer canonical pages where available.

### 09:00 EST run (this run)
- Scan method: LinkedIn guest search (ServiceNow + Salesforce, Toronto, f_TPR=r86400, 60 cards per query, full title+ID list captured); Workday CXS (BMO + TD after ~20s cooldown cleared the earlier 422s; other tenants 422'd earlier this cycle); Adzuna API demo keys (ServiceNow page 1, Salesforce Administrator page 1, max_days_old=3, sort_by=date, ≥3s spacing); Rogers jobs.rogers.com RSS feed; Bell jobs.bell.ca guest page.
- Result: **1 new verified job** — Senior Salesforce Developer, Tata Consultancy Services (Salesforce partner), Toronto, Ontario, Canada, LinkedIn 4491845382, posted ~59 minutes ago. Body verified on the guest detail page: Salesforce platform mentions (Apex 3, SOQL 1, Visualforce 2, LWC 1). Added to README.md Salesforce table (top, newest first) and jobs.json head (source=linkedin, tags=[salesforce], postedDate 2026-11-18T13:00:00.000Z).
- Already on board (dedupe held, skipped): IG Wealth HRSD ×3, BMO ServiceNow CMDB Administrator, Envision ITOM Developer, NTT DATA BA–ServiceNow SPM, ServiceNow Principal Solution Architect, ServiceNow Staff Cloud Security; Loblaw Sr Software Engineer (Salesforce), Accenture Techno-Functional Support Lead, Citco Salesforce Solution Architect, Munvo SFMC Consultant, Cognizant Data Cloud Developer, TD nCino/Salesforce Associate, Celestica Salesforce Developer Intern, Tru QA SFMC. Adzuna hits: TD Senior Solution Architect (ServiceNow) refresh already on board; Salesforce Administrator query returned sales/non-platform roles only.
- Dropped after verification: Deloitte "Software Asset Management (SAM) Analyst" (Adzuna 5969569891) — canonical careers.deloitte.ca shows Posting Start Date 9/16/26 (~2 months old, outside the 30-day window; anitab.org "Posted Nov 3" corroborates aged); not fresh, not added.
- Partner/employer look: Rogers jobs.rogers.com reachable via RSS this cycle — servicenow search = "No jobs currently available"; salesforce search = sales roles only, nothing platform. Bell jobs.bell.ca = zero reqs for servicenow/salesforce. Salesforce-the-company and ServiceNow-the-company Toronto careers pages: nothing fresh platform-track (postings are sales/SRE/security or 4+ days old). Canadian government portals (jobs.gc.ca, gojobs.gov.on.ca) remain Radware-walled — Job Bank used as proxy, trust only title-named platform postings.
- Merge/rebase note: origin/main advanced 2 commits mid-run (08:13 hourly scan + 09:00 agency scan). Rebased onto origin/main; jobs.json/public/* resolved to upstream (--ours during rebase = upstream wins). Upstream's jobs.json independently already contains the TCS role (2 rows: id + url) — the CI scan ingested it independently, confirming it is a genuine fresh posting. Local feed differences absorbed; build_site.py re-run: 4997 jobs indexed (SN 810 · SF 941 · Other 3246), 865 mirrors collapsed, 35 applied hidden, newest 2026-11-18. README counts bumped: TOC/summary 1461→1462, heading 1492→1493.
- Pushed 3c3aadf to origin/main; triggered pages.yml (run 44322454096); live https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json verified carrying the TCS URL (verified: Aggregator, match 60, match reasons Salesforce / Role fit / Toronto area).
- Limitation: Indeed.ca blocked (Cloudflare 403, browser and curl); LinkedIn detail pages need the guest-browser read (.jobs-description selector); Adzuna detail pages return CloudFront 403 to curl — corroborate via mirrors (talent.com, lmiafinder.ca, jobrapido, workopolis, anitab.org).


### 10:00 EST run (this run) — 4 fresh verified jobs merged
- Scan method: targeted web search for Toronto / Canada ServiceNow & Salesforce postings dated 2026-11-11 to 2026-11-18; dedupe against README.md + jobs.json by normalized URL + title\|company fingerprint. Checked Rogers, Bell, Canadian government (jobs.gc.ca / gojobs.gov.on.ca Radware-walled), ServiceNow & Salesforce careers Canada, and SN/SF partners (Ateko/NewRocket/Lane Four).
- Result: 4 fresh verified Salesforce jobs merged to the Salesforce table (newest first):
  - 2026-11-16 | Software Engineering MTS | Salesforce | Toronto, Canada | scoutify.com/companies/salesforce/jobs/3499409/ (Salesforce careers)
  - 2026-11-13 | Salesforce Business Analyst, Senior Associate | PwC Canada | Toronto, Ontario, CA | LinkedIn 4490536839 (~CA$88K-138K)
  - 2026-11-11 | Salesforce Developer | OSI Digital | Toronto, ON | jobs.ca/osi-digital/.../71730b7f3a5b3 (on-site, full-time)
  - 2026-11-11 | Salesforce Developer | Procom | Toronto, ON, Canada | myprocom-portal .../salesforce-developer-toronto-73f5a6b2 (hybrid, contract 2 months, posted 11/11/2026)
- ServiceNow: no newly-dated Toronto platform/dev/admin posting verified after 2026-11-10 this cycle.
- Skipped (dup/stale): Lyft Salesforce Architect (10/20), Make-A-Wish Sr SA (11/6), Procom Sr SN Dev (11/4, different role), Bell ServiceNow SysAdmin (deadline passed 10/20), OPS Solution Manager ServiceNow (date unconfirmed).
- Fix: synced stale README header counts after rebase onto active main to actual table rows — ServiceNow 1108, Salesforce 915 (incl. the 4 new), Other 4096; total 6119 live postings; window 2026-10-19 to 2026-11-18.
- jobs.json + public/ regenerated (sync_readme_to_jobs.mjs + build_site.py); committed to main and pushed; GitHub Pages rebuilds from main automatically.


### 11:00 EST run (this run)

- Scan method: targeted web search for Toronto / Canada ServiceNow & Salesforce postings dated 2026-11-11 to 2026-11-18; dedupe against README.md + jobs.json by normalized URL. Checked Rogers (jobs.rogers.com reachable, no servicenow/salesforce platform postings), Bell (jobs.bell.ca zero reqs), Canadian government (jobs.gc.ca / gojobs.gov.on.ca Radware-walled — not retried; Job Bank full-text proxy, title-noise only), ServiceNow & Salesforce careers Canada, SN/SF partners (Ateko / FX Innovation, NewRocket, Lane Four, Pentio, Fujitsu), and martechjobs.io Canada Salesforce list.
- Result: 2 fresh verified ServiceNow jobs merged to the ServiceNow table (newest first):
  - 2026-11-12 | ServiceNow Developer | SPECTRAFORCE | Toronto, ON, Canada | https://www.jobs.ca/spectraforce/jobs/servicenow-developer-toronto-on-54256a3e5345 — via jobs.ca — posted 2026-11-12 · Hybrid · Contract · ServiceNow CMDB/HAM/SAM/discovery/inventory build
  - 2026-11-13 | ServiceNow Developer | Dexian | Toronto, ON, Canada | https://www.jobs.ca/dexian/jobs/servicenow-developer-toronto-on-42da4c496cfe — via jobs.ca — posted 2026-11-13 · Hybrid · Contract 6 months · $90–$100/hr · Blue Rewards – IPS line of business (distinct staffing-vendor posting from the already-boarded Procom 2026-11-04 Blue Rewards requisition)
- Salesforce: no fresh unboarded Toronto Platform Admin / Developer I postings this hour.
- Dedupe vs README.md + jobs.json: +2 new, 0 duplicate (check_inbox OK; merger +2 new, 0 duplicate). Direct jobs.ca fetch returns Cloudflare 403 — listings verified via search-indexed content (posted date, duties, location, employment type). Both rows dedupe onto existing adzuna.ca Spectraforce/Dexian Toronto cards in jobs.json (vendor-twin URLs stay distinct README rows per the URL-only dedupe rule).
- Counts after merge: ServiceNow 1112, Salesforce 1071, Other 4061, total 6244 live postings — TOC, headings, "Show N postings" summaries and headline all agree; window 2026-10-19 → 2026-11-18.
- Publish: jobs.json 5,438 rows; public/ rebuilt: 4,926 jobs (SN 812 · SF 876 · Other 3238), 814 mirrors collapsed, link check OK; commit 4fd1f9e rebased onto upstream hourly scan 5a129f4 and pushed to origin/main; GitHub Pages deploys from main automatically.
- inbox/hermes-cron--2026-11-18--v5.md left as submitted untracked (upstream main already carries hermes-cron--2026-11-18--v4.md, their scan submission — not overwritten).
- Blockers this cycle: jobs.ca / Indeed.ca Cloudflare 403 to direct fetch; LinkedIn guest detail pages need sign-in; Adzuna detail pages CloudFront 403; Jobs Bank / GC portals walled or noisy.

### 12:00 EST run (this run)
- Scan method: targeted web search for Toronto / Canada ServiceNow & Salesforce postings dated 2026-11-17 to 2026-11-18; dedupe against README.md + jobs.json by normalized URL + title|company fingerprint. Checked Indeed.ca, Workopolis, CareerBeacon, LinkedIn guest, Built In Toronto, whatjobs aggregator mirrors, plus Rogers, Bell, Canadian government (jobs.gc.ca / gojobs.gov.on.ca Radware-walled), ServiceNow & Salesforce careers Canada, and SN/SF partners (SS&C, NewRocket, Lane Four, Ateko/FX Innovation, Pentio, Fujitsu).
- Result: **0 new verified jobs** — every surfaced Canada SN/SF row was already on the board or not fresh/platform-track:
  - City of Toronto RQ00757 Specialized IT Consultant (ServiceNow SPM, CareerBeacon 4060430, posted 2026-11-13) — already on board via CareerBeacon 3954299 / Job Bank 50492172 (posted 2026-11-03); company+title dedupe collapsed the re-surface.
  - SS&C Salesforce Implementation Consultant & Platform Administrator (LinkedIn 4487007282) — already on board ×5 rows (Nov 3–11).
  - whatjobs "posted today" mirrors (Insight Global Health Cloud, Maarut FSC, CYNET Scarborough, CorGTA, Virtusa Backend/API) — resolve to already-boarded companies/roles or non-platform tracks; CorGTA already on board (2026-11-03); Maarut roles Montreal.
- ServiceNow: no newly-dated Toronto platform/dev/admin posting verified after 2026-11-10 this cycle beyond boarded rows.
- Salesforce: no fresh unboarded Toronto Platform Admin / Developer I posting this hour.
- Partner / employer look (Rogers, Bell, Government of Canada, Elite SN/SF partners):
  - Rogers: jobs.rogers.com Phenom board unreachable (HTTP 404 / 9-byte body); search hits sales/pre-sales only. Re-check weekly.
  - Bell: jobs.bell.ca zero reqs for servicenow/salesforce. Re-check weekly.
  - Canadian government: jobs.gc.ca / gojobs.gov.on.ca Radware-walled (captcha) — not retried; Job Bank used as proxy, full-text "servicenow" search is title-noise. City of Toronto RQ00757 already boarded.
  - SS&C / NewRocket / Lane Four / Ateko (FX Innovation): sampled roles already on board (posted Nov 3–16). No new unboarded partner requisition.
  - Salesforce-the-company / ServiceNow-the-company Toronto careers: nothing fresh platform-track.
- Net board change this run: 0 new verified jobs. Counts unchanged: ServiceNow 1112, Salesforce 1071, Other 4061, total 6244 live postings; window 2026-10-19 → 2026-11-18.
- No README merge, no inbox file staged, no jobs.json/public change required; GitHub Pages already current from the 11:00 EST push (4fd1f9e).
- Blockers this cycle: jobs.ca / Indeed.ca Cloudflare 403 to direct fetch; LinkedIn guest detail pages need sign-in; Adzuna detail pages CloudFront 403; Jobs Bank / GC portals walled or noisy; whatjobs/careerbeacon detail dates are aggregator mirrors, resolved to boarded primary URLs.


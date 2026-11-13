# JOBLESSONS_2026-11-13 — hourly BESTIEJOB scan (2026-11-13 03:00 EST / 08:00 UTC)

## Scope
Toronto/Canada-first ServiceNow / Salesforce / IT-platform job board (`eltonaguiar/bestiejob`, main). Hourly cron scan: find fresh postings dated ~today/yesterday, dedupe against the board, merge verified rows into `README.md`'s three tables + `jobs.json` feed, rebuild GitHub Pages (`public/jobs-data.json` + `public/index.html`), push to `main` (auto-deploys to https://eltonaguiar.github.io/BESTIEJOB/).

## What ran this hour
This run used a **browser/search-based sweep** (web_search + web_extract) rather than the repo's `daily_job_scan.mjs` API scan, because the Adzuna/LinkedIn secrets are only present inside the GitHub Action. Queries covered:
- ServiceNow Toronto/GTA/Canada (LinkedIn guest, Indeed CA/FR, ZipRecruiter, BuiltIn, iHire)
- Salesforce "Platform Administrator" / "Platform Developer I" Toronto, entry-level/junior
- Telco targets: Rogers, Bell (jobs.bce.ca)
- Canadian government: Job Bank (`jobbank.gc.ca`, `mb.jobbank.gc.ca`)
- ServiceNow/Salesforce partners: Accenture, Deloitte, KPMG, CGI, Capgemini (Global Elite / sponsors)

The GitHub Action's `daily_job_scan.mjs` refreshed `jobs.json` earlier today (`scrapedAt 2026-11-13T07:12:51Z`, **2,610 listings**) and rebuilt the site to 5,088 cards. This web-based sweep is a supplementary pass and **added 3 verified rows** the API feed had not surfaced.

## Result this run
**3 verified fresh rows added.**

| Metric | Value |
|---|---|
| Scan start | 2026-11-13T08:00Z (03:00 EST) |
| jobs.json total (Action feed) | 2,610 (feed meta) |
| Live page indexed (this build) | **5,091 cards** (built 2026-11-13 08:07 UTC) |
| README rows after merge | **6,827** (was 6,824; +3) |
| New rows merged this run | **3** (0 duplicates against README + jobs.json) |

## Candidates found and disposition (all checked against jobs.json + README)

| Candidate | Source | Disposition |
|---|---|---|
| Cognizant — ServiceNow SAM Developer (job 00070949051, Toronto 199 Bay St / hybrid, published 2026-11-11, $92K-$105K CAD, applies until 11/30/2026) | careers.cognizant.com (page extracted) | **MERGED — ServiceNow table** |
| Cognizant — Salesforce Developer (job 00071305431, Remote in Canada, hiring location Toronto, published 2026-11-12, $80K-$95K CAD, applies until 11/20/2026) | careers.cognizant.com (page extracted) | **MERGED — Salesforce table** |
| TekStaff (end client) — Sr. ServiceNow Developer (jobs.ca 1955e5a41d93, Toronto ON hybrid, posted 2026-11-12, 5.5-month contract, CMDB/HAM/SAM/Discovery/MID Server/IntegrationHub) | jobs.ca (page extracted) | **MERGED — ServiceNow table** |
| Scotiabank — ServiceNow Developer (req 603030017) | jobs.scotiabank.com | Already on board — duplicate, skipped |
| BDO Canada — ServiceNow Senior Developer (Indeed jk=c956b22cc281049c) | Indeed.ca | Already on board — duplicate, skipped |
| Celestica — Senior Salesforce Developer / Admin (req 137318) | careers.celestica.com | Already on board — duplicate, skipped |
| Moneris — Principal Salesforce Software Developer (Workday JR106006) | jobs.moneris.com | Already on board — duplicate, skipped |
| Deloitte — Salesforce Developer, Digital Customer (135279, posted 9/29/2026) | careers.deloitte.ca | Outside 30-day window — stale, skipped |
| Accenture — ServiceNow Technical Architect (Job Bank R00356209, Toronto) | Job Bank | Early-October posting, outside fresh window — backfill candidate |
| Rogers — Lead Management Operations (req 343961, posted ~04 Nov 2026, Ottawa work location) | jobs.rogers.com | Salesforce-adjacent but not a dev/admin/architect title — excluded by title rule |
| Bell — ServiceNow Developer/Integrator (431695), System Administrator (432824), Sr. Manager Platform Delivery (432892) | jobs.bell.ca | All return "has been filled" — filled roles never enter the board |
| Government of Canada (jobs.gc.ca / GC Jobs) | jobbank.gc.ca | No ServiceNow/Salesforce technical postings found |
| Capgemini — Salesforce Toronto (1425744133, 1441205933, others) | careers.capgemini.com | Cookie wall, no verifiable posting date — not added |

## Patterns / lessons for future agents

1. **Cognizant posts fresh Toronto SN/SF roles directly on careers.cognizant.com with absolute "Date published" fields** — both Nov 11 and Nov 12 postings appeared this run. Prioritize it each cycle.
2. **Run the repo's own merger, not hand-edits:** `python3 tools/jobs_merge_inbox.py --max-per-table 5000 --bump-inbox` (5000 prevents the 150-row default from truncating the tables). The merger preserves existing rows verbatim and additively appends new ones; it dedupes on normalised URL against README + jobs.json.
3. **Blocker encountered:** the merger refused to write because a documentation example row in README.md's "How to add jobs" section was not a parsable `[title](url)` row (`extract_rows` counted it as an unreadable dated row and aborted to prevent silent data loss). Fixed by converting it to link format. Future runs should not hit this unless another example row lands in the tables.
4. **LinkedIn pages remain a login wall (HTTP 422).** Never add a LinkedIn-sourced role without a verifiable posting date.
5. **Telco/employer career sites beat aggregators for freshness, but titles mislead.** Rogers' Salesforce work is posted as "Lead Management Operations" (marketing operations); Bell's SN roles are filled. Scan named employers' ATS directly; reject filled/expired pages immediately.
6. **Dedupe against both README.md table URLs and jobs.json; normalize by stripping query strings and trailing slashes.** jobs.json feed keys: `readme:<url>`, `jobs.ca:<...>`, `workday:<...>` etc.; the Cognizant SN job landed under `readme:careers.cognizant.com/uki-en/jobs/00070949051/...` (locale-normalized).
7. **Publish chain:** `node scripts/sync_readme_to_jobs.mjs` → `python3 tools/build_site.py` → `python3 scripts/check_site_links.py`, then commit README.md, jobs.json, public/ and the inbox/ submission; push to main without `[skip ci]` so `pages.yml` redeploys https://eltonaguiar.github.io/BESTIEJOB/ (hourly-scan commits use `[skip ci]`, so the page is otherwise redeployed by the pages.yml `:35` schedule).

## Recommended next scans

- Target employer ATS deep-links directly: `site:*.myworkdayjobs.com` ServiceNow Toronto, `site:*.greenhouse.io` / `site:*.lever.co` Salesforce Toronto.
- Re-check Accenture R00356209 (relisted or expired after 09 Nov 2026 closing).
- Re-check Capgemini Salesforce Toronto postings once direct ATS URLs with dates are available.
- Re-check Rogers Lead Management Operations (Salesforce, posted 04 Nov 2026) on the next in-window cycle.

## Files touched

- `README.md` — fixed the unparseable documentation example row in the How-to section; merger added 3 new rows (2 ServiceNow, 1 Salesforce); board now 6,827 rows
- `inbox/hermes--2026-11-13--v2.md` — submission, version-stamped by the merger (+3 new, 0 duplicate)
- `jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json` — synced from README
- `public/jobs-data.json`, `public/index.html` — GitHub Pages site rebuilt (5,091 jobs, stamped 2026-11-13 08:07 UTC)
- `JOBLESSONS_2026-11-13.MD` — this file


## 09:00 EST run (2026-11-13 14:00 UTC) — supplementary hourly scan
**Result: 0 new fresh rows merged. Board already current.**

| Metric | Value |
|---|---|
| Scan start | 2026-11-13T14:00Z (09:00 EST) |
| jobs.json total (latest Action feed) | 2,615 (scrapedAt 2026-11-13T13:11:30Z; newThisScan 844; primaryCounts servicenow 1,228 / salesforce 1,269) |
| README rows | 6,827 (window 2026-10-13 → 2026-11-12) |
| New rows merged this run | **0** |

Candidates reviewed and disposition (all checked against jobs.json + README.md tables):
| Candidate | Source | Disposition |
|---|---|---|
| Adzuna — Cyber StrategiX, ServiceNow Platform Specialist, Canada, posted 2026-11-12 | adzuna.ca/details/5963510756 | NOT ADDED — detail page blocked by CloudFront (403); Adzuna API posted/created dates recycle ids (prior runs saw ~47 kept rows collapse to ~23 genuinely new), so API date alone is not proof of freshness. Flagged for next run; verify via direct employer/ATS page or once the Adzuna detail is reachable. |
| Adzuna — Salesforce, Software Engineering LMTS, Toronto, posted 2026-11-13 | adzuna.ca/details/5964479115 | EXCLUDED — not a Platform Administrator / Platform Developer I role (Salesforce-company engineering LMTS; title does not name the platform). Board title rule: title must name ServiceNow/Salesforce or a platform module/cert. |
| fresh-ca inbox v3 — Raas Infotek ServiceNow CTA (4490365820), lululemon Senior Solution Architect Agentforce/Salesforce (4488575656) | LinkedIn | Already on README (merged via fresh-ca--2026-11-13--v1.md) — DUPLICATE, skipped. |

Lessons this run:
1. The hourly GitHub Action (`daily_job_scan.mjs`, ADZUNA credentials) already refreshed `jobs.json` at 13:11 UTC (2,615 jobs; 844 new this scan) and republished `public/` to `main` — the live page https://eltonaguiar.github.io/BESTIEJOB/ is current. A local re-scan shortly after the Action adds little.
2. Local browser cannot reach Adzuna detail pages (CloudFront 403) and Cognizant pages render an authwall shell, so `postedDate` from the Adzuna API cannot be independently corroborated locally. Do not add Adzuna-sourced rows on API date alone given the known id-recycling issue.
3. Inbox submissions were already merged under an earlier inbox version (`fresh-ca--2026-11-13--v1.md`) — always grep the exact URL in README before treating an inbox row as new.
4. Title rule holds: Salesforce "Software Engineering LMTS" (company engineering role, not Platform Admin/Dev I) excluded; board rule is title must name ServiceNow/Salesforce or a platform module/cert.

Files touched:
- `JOBLESSONS_2026-11-13.MD` — appended this 09:00 EST section
- No changes to `README.md`, `jobs.json`, or `public/` (0 new verified jobs; board already current from the Action).

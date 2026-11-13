# JOBLESSONS_2026-11-13 — hourly BESTIEJOB scan (2026-11-13 01:00 EST / 06:00 UTC)

## Scope
Toronto/Canada-first ServiceNow / Salesforce / IT-platform job board (`eltonaguiar/bestiejob`, main). Hourly cron scan: find fresh postings dated ~today/yesterday, dedupe against the board, merge verified rows into `README.md`'s three tables + `jobs.json` feed, rebuild GitHub Pages (`public/jobs-data.json` + `public/index.html`), push to `main` (auto-deploys to https://eltonaguiar.github.io/BESTIEJOB/). `jobs.json` is the system of record.

## What ran this hour
This run used a **browser/search-based sweep** (web_search + web_extract) rather than the repo's `daily_job_scan.mjs` API scan, because the Adzuna/LinkedIn secrets are only present inside the GitHub Action. Queries covered:
- ServiceNow Toronto/GTA/Canada (LinkedIn guest, Indeed CA/FR, ZipRecruiter, BuiltIn, iHire)
- Salesforce "Platform Administrator" / "Platform Developer I" Toronto, entry-level/junior
- Telco targets: Rogers, Bell (jobs.bce.ca)
- Canadian government: Job Bank (`jobbank.gc.ca`, `mb.jobbank.gc.ca`)
- ServiceNow/Salesforce partners: Accenture, Deloitte, KPMG, CGI, Capgemini (Global Elite / sponsors)

The GitHub Action's `daily_job_scan.mjs` refreshed `jobs.json` at 05:12Z (`scrapedAt 2026-11-13T05:12:11Z`, **2,609 listings**, SN 1,224 · SF 1,264) and rebuilt the site to 5,088 cards at 05:13:54Z (commit `e1c9de4`). This run's web-based sweep is a supplementary pass and added 0 rows.

## Result this run
**0 verified fresh rows added.** Null web sweep — every fresh surfacing was already on the board, dead (HTTP 410), expired, or behind a login wall with no verifiable posting date. Null hourly runs are the norm, not a failure.

| Metric | Value |
|---|---|
| Scan start | 2026-11-13T06:00Z (01:00 EST) |
| jobs.json total (05:12Z Action feed) | 2,609 (SN 1,224 · SF 1,264) |
| Live page indexed (Action build, 05:13:54Z) | **5,088 cards** |
| Mirror duplicates collapsed | 778 |
| Applied roles hidden | 43 |
| New rows merged this hour | **0** |
| Newest posting on site | 2026-11-13 |

## Candidates found and disposition (all checked against jobs.json + README)
| Candidate | Source | Disposition |
|---|---|---|
| Canada Life — ServiceNow Software Developer (Toronto) | LinkedIn 4117805118 | **Already on board** (2026-11-08 row) |
| Interac — ServiceNow Developer (Toronto) | LinkedIn 4187027175 | **Already on board** (2026-11-08 row) |
| Scotiabank — ServiceNow Solutions Architect, Platform Integration | LinkedIn 4221477571 | Not on board, but **login wall + id 422M ≈ Oct 2026** (board's fresh LinkedIn ids are 448M–449M) — stale/unverifiable, skipped |
| Job Bank — ServiceNow SPM developer (CSA+CAD mandatory, Toronto) | mb.jobbank.gc.ca 50108003 | **HTTP 410 Gone** — removed/expired |
| Job Bank — RBC Senior HR ServiceNow Developer (Toronto) | jobbank.gc.ca 48904398 | **HTTP 410 Gone** — removed/expired |
| Bell — ServiceNow Senior Technical Advisor (Toronto/Montreal) | jobs.bce.ca 1437314500 | **Application deadline 11/02/2026 — expired** |
| KPMG — Functional Consultant/Senior Consultant ServiceNow (34113) | careers.kpmg.ca 34113 | **Already on board** (icims URL, posted 2026-10-15) |
| KPMG — Senior Consultant ServiceNow (ITAM/ITOM) (33527) | careers.kpmg.ca 33527 | Role **already tracked** under many LinkedIn/eluta rows (posted 2026-11-10/09) |
| KPMG — Solution Developer (33919) · Senior Consultant (31517) | careers.kpmg.ca | **Already on board** |
| Deloitte — Senior Consultant ServiceNow Platform (133759) | careers.deloitte.ca 133759 | **Already on board** (req 133759, posted 2026-11-01) |
| CGI — ServiceNow Business System Architect (Toronto) | LinkedIn/eluta/njoyn | **Already on board** (latest 2026-10-31) |
| Accenture — ServiceNow Business Process Consultant (R00299365) | accenture.com | **"This job is no longer available"** — expired |
| Slalom — ServiceNow Technical Consultant HRSD (Toronto) | LinkedIn 4149977399 | **Closed** (accepting applications until April 30, 2025) |
| BFG Enterprise Services — SN Admin/Developer (Intermediate, Markham) | Indeed CA | **Already on board** (readme row) |
| BMO — ServiceNow SAM Administrator (Toronto) | Indeed/ZipRecruiter | **Already on board** (deadline 11/22/2026) |

## Dedupe outcome
- Normalized-URL set from `jobs.json` (2,609 unique, 0 bad date/url/title) was the primary gate; fuzzy company+title checked as a backstop (KPMG/CGI/Deloitte/BMO roles re-surface under LinkedIn/eluta/njoyn/icims/Workday URLs — company+title catches them even when the URL differs).
- Every candidate either matched an existing URL, matched an existing company+title row, or failed liveness/deadline. Nothing met the "genuinely fresh + verifiable + not already tracked" bar.

## `import_fresh_rows.py` check — do NOT run it blind this hour
A `--dry-run --days 2` reported **431 fresh rows, 22 "genuinely new"**. Cross-checking each against the full README text showed **every one was already on the board under a mirror URL**, e.g.:
- BMO ServiceNow CMDB Administrator (Workday `R260030992`, live HTTP 200) ≡ README row via LinkedIn `...cmdb-administrator-at-bmo-4490380189`
- BMO ServiceNow Technology Lifecycle Analyst (Workday `R260030995`, live HTTP 200) ≡ README via LinkedIn `...technology-lifecycle-analyst-at-bmo-4490364941`
- Cognizant / CAAT / OSI Digital / TForce Freight / Deloitte (2026-11-12) rows — already added to README by the 22:00 EST run.
`import_fresh_rows.py` only diffs against its own scan-output URLs, so it cannot see the README's LinkedIn/aggregator mirrors and would have **duplicated ~22 existing roles**. Dry-run it, then confirm each "new" row by company+title against the whole README before importing — or better, skip it and let `build_site.py` union jobs.json + README.

## Target-company checks (Rogers / Bell / partners / Government of Canada)
- **Rogers:** no fresh SN/SF *platform* role surfaced; Rogers Salesforce hits are sales/marketing-ops (already tracked in Other), not Platform Admin/Dev I.
- **Bell:** ServiceNow Senior Technical Advisor (432829) deadline was 11/02/2026 → expired; the Senior Forward Deployed AI Engineer role mentions Salesforce/ServiceNow only as preferred skills (AI role, not SN/SF platform) — excluded by title rule.
- **Partners (KPMG Global Elite, Deloitte, CGI, Accenture):** all live SN roles already on the board or expired (Accenture R00299365 no longer available; KPMG 34113/33919/31517/33527 tracked; Deloitte 133759 tracked; CGI Business System Architect tracked).
- **Government of Canada / Job Bank:** servicenow keyword hits were either HTTP 410 (removed) or unrelated roles whose body text merely lists ServiceNow among tools — Job Bank full-text search is noise; trust only title-named platform roles.

## Patterns / lessons for future agents
1. **Web search is a weak freshness oracle.** Google/Indeed snippets lag by days–weeks: most ServiceNow LinkedIn hits carried 401M–422M job ids (Oct 2026) while the board's genuinely fresh LinkedIn entries are 448M–449M. Always confirm a candidate's real date (ATS `startDate`, `datePosted` JSON-LD, or "Application Deadline") before treating search output as "fresh".
2. **HTTP 410 on a Job Bank posting id = removed.** Both CSA/CAD SPM and RBC HRSD hits were 410; do not re-add them.
3. **LinkedIn detail pages are behind a login wall for `web_extract`** (HTTP 422 target_paywalled) and the browser harness may fail with a locked Chrome profile. Dedupe by URL/id from search snippets instead; don't burn calls re-extracting walled pages.
4. **`postedDate` on ATS/Workday rows is the scan timestamp, not the real posting date.** The 15 "2026-11-13" rows in `jobs.json` are mostly jobs *scanned* today (Workday/BMO/GDIT), not genuinely new postings. Never insert them into README as "Posted today" — freshness must come from the source, not the scan clock.
5. **Rebuild after any `jobs.json` change.** `public/jobs-data.json` can lag the feed (this hour my local 2,657 feed built to 5,086 cards, but origin's newer 2,609 feed already built 5,088 at 05:13:54Z — trust the newer feed). `tools/build_site.py` re-unions `jobs.json` (leads) + README rows; editing `jobs.json` alone never reaches the page, so always run `build_site.py` and commit `public/jobs-data.json` + `public/index.html`.
6. **The board is already dense (5,088 unique cards; 2,609 fresh feed).** Sustained null hours mean coverage is good, not that scanning stopped. Keep the liveness/verification gate, but don't manufacture rows to "hit a number".
7. **Partner portals rarely publish dates and rarely have entry-level Platform Admin / Dev I.** GC platform work reaches the market through prime vendors on their own ATS; check those boards, not `jobs.gc.ca` (Radware-blocked).
8. **`import_fresh_rows.py` over-reports "new" rows by mirror URL.** It reported 22 "genuinely new" this hour, but all 22 were already in README under LinkedIn/aggregator URLs (its dedupe only sees its own scan-output URLs). Never import its output without a company+title cross-check against the full README first.
9. **Workday↔LinkedIn mirror pairs share one requisition.** BMO `R260030992`/`R260030995` live on Workday *and* as LinkedIn `4489…` rows; either URL is valid, but adding both double-lists one job. Prefer the employer-board URL when adding a genuinely new row; keep the LinkedIn mirror as an alternate.

## Files touched
- `JOBLESSONS_2026-11-13.MD` (this file)
- `jobs.json` (Action scan feed: 2,609 listings, 05:12Z) — already committed on origin (`e1c9de4`); not touched by this run
- `public/jobs-data.json`, `public/index.html` (fresh via the Action's `tools/build_site.py`: 5,088 cards, built 2026-11-13 05:13:54Z — no rebuild needed this run; my own 5,086-card build from the older local 2,657 feed was discarded in favour of origin's newer scan)
- `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json` (feed mirrors)
- `FRESH_JOBS.md` (scan output)

## Next scan TODO
- Re-run `daily_job_scan.mjs` inside the GitHub Action (Adzuna/LinkedIn secrets) for the next full API sweep — this run's web sweep is a supplement, not a replacement.
- Re-check Scotiabank ServiceNow Solutions Architect (4221477571) once it is reachable without login to get a real posted date.
- Watch Bell 432829 / Accenture R00299365 for reposts under new req ids.
- Keep prioritising entry-level **Platform Administrator** and **Platform Developer I** roles; senior/architect roles dominate current surfaces.

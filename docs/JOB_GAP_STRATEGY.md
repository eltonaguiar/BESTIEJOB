# BESTIEJOB — Gap Strategy: Jobs NOT on the Board

**Goal:** Find ServiceNow / Salesforce / "other" resume-relevant IT jobs in Canada that are NOT already reflected in
`README.md` (and the live site at eltonaguiar.github.io/BESTIEJOB/), then get them onto the board under the same
verification rules the board already uses.

**Board baseline (as of 2026-11-11):** 6,427 live postings, window 2026-10-12 → 2026-11-11 — ServiceNow 1,056, Salesforce
1,212, Other 4,159. Source mix is dominated by Adzuna API rounds, Indeed cache (`round11-cached`), Greenhouse/Lever/Ashby
ATS slugs, and four date-verified feeds (CareerBeacon, Dice, Procom, Built In Toronto). `jobbank.gc.ca` has 13 rows,
`himalayas.app` 3 rows, `themuse.com` 1 row, `builtin.com` 30 rows.

## 1. Gap sources — verified by live search (not on board, or under-harvested)

| # | Source | Why it's missing / under-covered | Evidence found (live search) | Est. yield | Effort | First action |
|---|--------|----------------------------------|------------------------------|------------|--------|--------------|
| 1 | **Indeed Canada** (ca.indeed.com + emplois.ca.indeed.com) | Blocked from scraping (403/CAPTCHA); only `round11-cached` Indeed rows made it onto the board. Largest raw volume for contract/staffing roles. | Probe: 434 ServiceNow + 400 Salesforce hits for Toronto. French Québec market surfaces via search: iA Financial Group "Salesforce Developer" Québec City; Procom "Administrateur / Développeur Salesforce" Québec City (contract); TEHORA "Spécialiste / Développeur ServiceNow" Montréal; BNP Paribas "ServiceNow Platform Developer" Montréal; CGI "ITOM ServiceNow Developer" Montréal; BFG Enterprise Services "ServiceNow Administrator / Developer (Intermediate)" Markham $70–85K. | High | High (blocked) | Web-search sweeps in French + English; open each hit, capture `datePosted` JSON-LD if reachable, else mark undated → inbox. |
| 2 | **Himalayas** (himalayas.app) | Only 3 rows on board (Valiantys, Ensiti, an ITSM listing page — all `via readme`, 2026-11-04). Remote-focused aggregator; carries Canada-only Salesforce/ServiceNow roles. | Salesforce "Solution Consultant / Senior Solution Consultant (PubSec)", Remote Canada, CA$75K–125K, posted 2026-08-14, apply before 2026-10-13 → **expired** (outside board window, correctly not on board) but proves the source yields Canada-only SF roles. CloudMasonry "Principal Consultant, Data 360 (Data Cloud)" is US-only → out of scope. | Medium | Low | Add Himalayas Canada pages (`/jobs/countries/canada/...`, `/companies/{salesforce,servicenow}/jobs/...`) as a scrape target; keep only postings with absolute dates inside the 30-day window. |
| 3 | **The Muse** (themuse.com) | 1 row on board (Infosys ITSM Sr Developer, `via readme`). Company-profile job board with direct employer postings. | Equinix Toronto: "Principal Architect - ServiceNow People and Legal Tech" (posted Apr 17) and "ServiceNow Platform Developer/Engineer" (posted Apr 17) — both stale/expired. Kyndryl "ServiceNow Developer - ITOM" (Bangalore, India — out of scope). TJX Mississauga "Senior Architect - ServiceNow" marked "no longer available". | Low/Medium | Low | Search `site:themuse.com servicenow salesforce Canada Toronto` weekly; accept only postings with an absolute posted date within window. |
| 4 | **Job Bank** (jobbank.gc.ca) | 13 rows on board, all via buffy-round16/readme. Federal board — public-sector and Crown SN/SF requisitions (SSC, CRA, DND, Ontario Health, Metrolinx, TTC) post here per procurement rules and may never hit aggregators. | Search returned generic pages, no SN/SF hit on first page — needs direct advanced-search queries by skill/keyword, not just `site:`. | Medium | Medium | Run Job Bank advanced search for ServiceNow/Salesforce/CMDB/ITAM in ON/QC/BC; capture `datePosted`; disable jobs without absolute dates. |
| 5 | **Wellfound / AngelList** | Blocked (Cloudflare "Checking if the site connection is secure"). Startup-heavy → Salesforce-heavy roles. Board's existing `research_sources_scraper.js` only does basic HTML of `angel.co/jobs` (dead). | Role pages still render in search snippets (Genesis10 "Senior ServiceNow Developer / Architect" $166–187K, US-based). | Medium (startups/SF) | High | Try Wellfound no-login search API or Apify actors ("only new jobs since last run" mode); Canada + ServiceNow/Salesforce filter. |
| 6 | **Staffing firm career pages** (client-side) | `config/agency_boards.json` has Randstad, TEKsystems (Phenom), Eluta **disabled** — search pages render links client-side. S.i. Systems, Altis, Experis, Hays, Insight Global, Robert Walters, Aquent, etc. never probed for harvestability. | TEKsystems careers page loads but job search is client-side; `careers.teksystems.com/ca/fr/job/JP-006394899` exists (filled roles). | Medium | High | Headless-browser probe (Playwright) or find sitemap/RSS/job-feed endpoints per firm; enable only feeds that expose absolute posting dates. |
| 7 | **More ATS APIs** | Board has ~45 Greenhouse + ~20 Lever slugs; Ashby partially. Riley-Dorrington aggregator pattern shows Ashby, BambooHR, iCIMs, Paylocity are directly queryable via JSON. | `tools/ats_board_slugs_ca.txt` exists but short; Greenhouse `boards-api.greenhouse.io/v1/boards/{slug}/jobs`, Lever `api.lever.co/v0/postings/{slug}?mode=json`. | Medium | Low | Expand `ats_board_slugs_ca.txt` with Canadian end-users (banks, telcos, retailers, consultancies); add Ashby/BambooHR/iCIMs/Paylocity adapters. |
| 8 | **Company career-page discovery** | End-user enterprises (RBC, TD, BMO, CIBC, Scotiabank, National Bank, Desjardins, Manulife, Sun Life, Bell, Rogers, Telus, Loblaw, CN, CPKC, Air Canada) post on their own portals ahead of aggregators. | NewRocket/GlideFast (Everforth) ServiceNow careers pages found; roles mostly US-remote. Traction on Demand (acquired by Salesforce), CloudKettle, Slalom, Diabsolut, Lane Four, CloudJunction, Altus Group, Docebo in partner list. | Medium | Medium | Crawl careers pages of top-30 Canadian SN/SF end-users + partners; detect ATS (Greenhouse/Lever/Ashby/Workday) and add slugs. |
| 9 | **French-language Québec** | Most sweeps use English keywords; Montréal/Québec City SN/SF market (CGI, BNP Paribas, iA Financial, TEHORA, Desjardins, Pomerleau, Exo, CMHC) posts in French. | `emplois.ca.indeed.com` search shows French titles: "Administrateur(trice) ServiceNow", "Développeur ServiceNow Senior", "Spécialiste / Développeur ServiceNow", "Développeur de plateforme ServiceNow". | Medium | Low | Add French queries: `administrateur ServiceNow`, `développeur Salesforce`, `analyste ITSM ServiceNow`, Québec/Montréal. |
| 10 | **Human / referral channel** | Not a scraper source, but most Canadian SN/SF contracts route to recruiters before public posting. | JOB_SITES_CANADA doc: S.i. Systems, Procom, TEKsystems, Apex, Robert Half, Randstad, Experis, Hays, Robert Walters, Altis, Eagle, Akkodis, Raise, CorGTA, Insight Global hold bank requisitions. | High (contracts) | Human effort | Register with 3 recruiters (S.i. Systems, Procom, TEKsystems); attend SNUG Toronto + Trailblazer Community Toronto + Salesforce Saturday. |

## 2. Verified leads found (not on board — date status shown)

| Role | Company | Location | Source | Date evidence | On board? |
|------|---------|----------|--------|---------------|-----------|
| Solution Consultant / Senior Solution Consultant (PubSec) | Salesforce | Remote, Canada | Himalayas | Posted 2026-08-14; apply before 2026-10-13 → **expired** | No (outside window) |
| Principal Consultant, Data 360 (Data Cloud) | CloudMasonry | United States only | Himalayas | n/a → **out of scope** | No (not Canada) |
| Senior Salesforce Administrator | Desjardins / Collabria | Montréal/Remote | Built In | Removed 2026-10-31 → **expired** | No |
| Salesforce Developer | iA Financial Group | Québec City, QC | emplois.ca.indeed.com | date not visible in snippet → **pending** | No |
| Administrateur / Développeur Salesforce (senior) | Procom | Québec City, QC (contract) | emplois.ca.indeed.com | date not visible → **pending** | No |
| Spécialiste / Développeur ServiceNow | TEHORA | Montréal, QC | emplois.ca.indeed.com | date not visible → **pending** | No |
| ServiceNow Platform Developer | BNP Paribas | Montréal, QC | emplois.ca.indeed.com | date not visible → **pending** | No |
| ITOM ServiceNow Developer | CGI | Montréal, QC | emplois.ca.indeed.com | date not visible → **pending** | No |
| ServiceNow Administrator / Developer (Intermediate) | BFG Enterprise Services | Markham, ON | ca.indeed.com | date not visible → **pending** | No |

**Rule applied:** none of the above is added to README until a posting page shows an absolute `datePosted` within the board window and the URL passes dedupe. That is deliberate — the board's rule is "absolute date on the posting only; no relative ages, no fabricated dates."

## 3. Execution plan (phased)

### Phase 0 — this week (zero new tooling)
1. Run the 10 web-search query sets below (English + French, all Canadian geo) once per weekday.
2. For every hit: open the posting, confirm an absolute posted date within 2026-10-12 → 2026-11-11, confirm employer from the posting itself, normalize URL (strip `utm_*`, query strings, trailing slashes), dedupe against `README.md`, then file to `inbox/<source>--<date>--v<N>.md` for the merger.
3. Re-scan the four enabled feeds (CareerBeacon, Dice, Procom, Built In Toronto) — they are date-verified and cheap to re-run.

### Phase 1 — week 2 (low effort, high yield)
1. Himalayas: add Canada SN/SF pages as scrape targets; require absolute date.
2. Expand `tools/ats_board_slugs_ca.txt`; add Ashby, BambooHR, iCIMs, Paylocity API scrapers.
3. French-language Québec sweeps on Indeed/web search.

### Phase 2 — month 1 (medium effort)
1. Wellfound workaround (no-login API / Apify actor, "new since last run").
2. Staffing firm sitemap/RSS probes (Randstad, TEKsystems Phenom, Eluta, Talent.com) — enable only if absolute dates are present.
3. Company career-page discovery for top-30 Canadian end-users + consulting partners; add discovered ATS slugs.

### Phase 3 — ongoing (human channel)
1. Weekly: Job Bank advanced search (public sector).
2. Monthly: SNUG Toronto / Trailblazer Toronto / Salesforce Saturday attendance; recruiter check-ins with S.i. Systems, Procom, TEKsystems.
3. Per round: dedupe by URL, validate liveness (HTTP 200 on employer-ATS posting), sort newest-first, commit, push, verify live site.

## 4. Weekly search query set (copy-paste ready)

ServiceNow:
- `ServiceNow developer administrator jobs Toronto Canada site:ca.indeed.com OR site:ca.linkedin.com OR site:jobbank.gc.ca`
- `ServiceNow ITOM ITAM CMDB Discovery HR SPM jobs Canada site:jobbank.gc.ca OR site:jobs.gc.ca`
- `administrateur ServiceNow développeur Québec Montréal emploi`
- `ServiceNow jobs site:himalayas.app Canada`
- `ServiceNow jobs site:themuse.com Canada Toronto`

Salesforce:
- `Salesforce developer administrator architect jobs Toronto Canada site:ca.indeed.com OR site:ca.linkedin.com`
- `développeur Salesforce administrateur Salesforce Québec emploi`
- `Salesforce jobs site:himalayas.app Canada`
- `Salesforce jobs site:themuse.com Canada Toronto`

Other (resume keywords):
- `PowerShell VBA Alteryx Python SQL Tableau Power BI jobs Toronto Canada site:ca.indeed.com`
- `ITAM CMDB ITOM ServiceNow jobs Ottawa Gatineau site:jobbank.gc.ca`

## 5. Board rules carried over (do not relax)

- **Absolute date only** — `datePosted` JSON-LD / `article:published_time` / literal `Posted YYYY-MM-DD` on the posting itself. No "3 days ago", no footer dates, no invented dates.
- **Employer from the posting** — never the board name.
- **Location from the posting** — ambiguous city names need province or "Canada"; `USA`/`United States` rejected.
- **Dedupe by URL** — normalize (strip `utm_*`, query strings, trailing slash); skip if already in README.
- **Canada scope only** — enforce Canada/remote-Canada; reject US-only (CloudMasonry Data 360 role is an example of a reject).
- **No vendor sales titles; no job at the product vendor counted as a platform role** (ServiceNow/Salesforce hiring for their own sales is out of scope for this board).
- **Never fabricate** dates, salaries, or company names → "Not disclosed" or undated → inbox, not README.

## 6. Success metrics

- New sources added to `config/agency_boards.json` / `tools/ats_board_slugs_ca.txt` with `enabled: true` only after a dated, in-scope row is produced.
- Weekly delta: N new rows in README that were NOT in the previous week's commit, each with a verifiable `Posted` date and source tag.
- Zero rows added without an absolute date; zero duplicates by normalized URL.

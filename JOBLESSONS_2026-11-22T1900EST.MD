# JOBLESSONS 2026-11-22 19:00 EST scan

**Run:** hourly Toronto ServiceNow / Salesforce job scan, 2026-11-22T19:00 EST (commit `6f22ce7`, repo `eltonaguiar/BESTIEJOB`, branch `main`).
**Goal:** find fresh Toronto SN/SF postings, dedupe against `jobs.json`, merge verified new rows into `README.md` + GitHub Pages, record lessons.

## What the scan returned
- Script: `scripts/daily_job_scan.mjs` (public ATS/job feeds only; no logins, no paid APIs).
- Fresh postings this scan: **399** (after URL-based dedupe against the existing board).
- Merged board total: **5,632** postings (ServiceNow 1,192 / Salesforce 4,283).
- Stale rows pruned: 1. `normalize_board.py --apply`: **0 rows dropped** — every fresh row passed board rules.
- Writes: `jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`, `FRESH_JOBS.md`, README `<!-- DAILY-SCAN -->` block.
- Site rebuilt via `tools/build_site.py`: 4,930 display jobs (851 SN / 922 SF / 3,157 Other), 436 duplicate mirrors collapsed, 27 applied hidden.
- Committed and pushed to `main`; GitHub Pages (`eltonaguiar.github.io/BESTIEJOB/`) redeploys via `pages.yml` on push to `public/**` + `README.md`.

## Source mix this scan
| Source | Postings | Notes |
|---|---|---|
| Adzuna | 190 | Largest contributor; Canada-wide + Toronto queries |
| LinkedIn | 176 | Guest endpoint HTTP 429 on first attempt, recovered on retry |
| SmartRecruiters | 12 | ServiceNow board only |
| Greenhouse | 12 | 9 board slugs (NeuraFlash, D2L, LightFeather, etc.) |
| Ashby | 2 | Benevity, Loopio |
| Lever | 1 | EQ Bank |
| Remote (RemoteOK/Jobicy/Remotive) | 6 | |
| Workday (14 boards incl. Salesforce, BMO, TD, GDIT, CIBC, Scotiabank, Manulife) | 0 | **All HTTP 429 — rate-limited** |

## What worked / what didn't
- **Adzuna is the workhorse** for Toronto SN/SF — consistently the largest fresh yield. Keep the broad query list (SN/SF + ITSM/ITAM/CMDB/agentforce/apex variants, Toronto + Ottawa + Mississauga + Canada-wide remote).
- **LinkedIn guest search is throttled** (HTTP 429). The script retries once; a Playwright fallback exists but wasn't needed here. Don't rely on LinkedIn as a primary fresh signal.
- **Workday is rate-limited hard** — every board returned HTTP 429 this scan, including Salesforce/BMO/TD/GDIT/CIBC/Scotiabank/Manulife. Workday-heavy employers (banks, telcos, GDIT) are under-represented until the 429 clears; probe them individually later with longer delays.
- **SmartRecruiters/Greenhouse/Ashby/Lever** return small but clean, employer-direct postings (good for verified, non-aggregator rows).
- Dedupe key = hostname + pathname (query/strip stripped). Adzuna/LinkedIn "id-recycle twin URLs" were suppressed — this is a recurring dedupe pattern (see 18:00 EST run suppressing 36 twins).

## Fresh verified Toronto / Ontario SN/SF postings dated 2026-11-22 (newest)
ServiceNow:
- Cyber Advisory Solution Consultant — ServiceNow, Inc. — Toronto, ON (Adzuna)
- Conseiller principal, ITOM, ServiceNow — Deloitte — Toronto, ON, Canada (LinkedIn)
- Conseiller(ère) principal(e), ServiceNow — Deloitte — Brossard, QC, Canada (LinkedIn)
- Manager, ServiceNow Platform — iA Financial Group — Canada (Adzuna)
- GDIT ServiceNow Developer — Any Location / Remote (Workday)

Salesforce:
- Senior Back-End Email Developer (Salesforce Marketing Cloud) — Intact Financial — Toronto, ON (Adzuna, EN + FR duplicate pair)
- Salesforce Tech Lead (Remote) — Cognizant — Toronto, ON (Adzuna)
- Salesforce Specialist — INNOVA — Toronto, ON, Canada (LinkedIn)
- Salesforce BSA — Apex Systems — Mississauga, ON, Canada (LinkedIn)
- Director, Salesforce Delivery and Architecture — Deloitte — Toronto, ON, Canada (LinkedIn)
- Salesforce Administrator (Remote) — Hired — Canada (LinkedIn)
- Senior Salesforce Technical Lead — UST — Montreal, QC, Canada (LinkedIn)

## Partner / Elite Partner / sponsor companies to target next scan
The scan's Workday board list and SmartRecruiters pull do NOT include Rogers, Bell, or Canadian government — these must be searched explicitly:
- **Rogers** — careers at jobs.rogers.com; no ServiceNow/Salesforce posting surfaced in this scan (raw/rogers_1700/1900 html captured earlier but unparsed).
- **Bell** — jobs.bell.ca; Indeed surface Salesforce Admin/Bell Mobility leads but no verified Toronto SN/SF row merged this scan.
- **Canadian government** — GCjobs / Canada.ca; not in any configured board; public-sector SN/SF roles appear under Deloitte "GoC focus" and similar integrator postings instead.
- Known partners already appearing: Deloitte, Cognizant, Slalom, INNOVA, UST, Blue Mantis, NeuraFlash (Greenhouse), Accenture (Workday probe captured raw/wd_live_accenture_* but not merged).

## Partner / government leads found this scan (web-verified — not in the ATS scan)
These surfaced via targeted search, not the configured board sources; none are in the current Workday/Greenhouse/Lever/Ashby allowlists, so they must be added as explicit sources next scan.
- **CMHC — Bilingual Senior Specialist, ServiceNow ITSM Developer** (Req 12379), Montreal / Ottawa / Toronto, hybrid, Secret clearance, $104,180–$130,225. careers.cmhc-schl.gc.ca — active ServiceNow government role.
- **Government of Canada — Senior Salesforce Developer** (LinkedIn), Ontario, contract, posted 2026-11-09, requires SECRET clearance + Salesforce Platform Developer cert. linkedin.com/jobs/view/4481939757.
- **ServiceNow — Senior Systems Engineer**, Canadian sovereign cloud (GCP), requires GoC Reliability Status (citizen/PR). careers.servicenow.com/jobs/744000162621080.
- **House of Commons — Full-Stack Developer (Digital Product Developer)**, Ottawa, leverages ServiceNow platform — closed 2026-11-15 (stale; do not re-add).
- **Rogers** (jobs.rogers.com Technology category) and **Bell** (jobs.bell.ca/technology, Toronto(1)) careers pages exist but returned no specific ServiceNow/Salesforce row this scan.

## Recommendations for future agents
1. When Workday returns HTTP 429, flag "bank/telco under-represented" and retry those boards individually with longer delays rather than treating the scan as complete.
2. Add Rogers (jobs.rogers.com), Bell (jobs.bell.ca), and GCjobs/Canada.ca as explicit sources — none are in the current Workday/Greenhouse/Lever/Ashby allowlists.
3. Dedup Adzuna+LinkedIn+jobs.ca clusters under employer+title (build_site.py already collapses 436 mirrors) — don't count mirrored aggregator rows as distinct fresh jobs.
4. README header count ("5628 live postings") is the deduped/filtered count; FRESH_JOBS.md total (5,632) includes pre-existing rows. They intentionally differ; don't "fix" by overwriting the scan header.
5. Commit + push to `main`, then confirm `pages.yml` deploy run concludes `success` before reporting the live page as updated (two runs already confirmed success; the run for `6f22ce7` was still queued at write time).

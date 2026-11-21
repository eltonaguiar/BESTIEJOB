# BESTIEJOB Hourly Scan — Job Search Lessons

**Date**: 2026-11-21
**Run time**: 2026-11-21 10:00 EST (15:02 UTC) — scheduled cron run
**Scope**: Fresh Toronto / GTA ServiceNow and Salesforce postings (Platform Admin / Platform Developer I / partner & employer focus); adjacent Other tags per board policy
**Repo**: github.com/eltonaguiar/BESTIEJOB (branch: main)
**Live board**: https://eltonaguiar.github.io/BESTIEJOB/

## Scan summary

| Metric | Value |
|---|---|
| Scan command | `node scripts/daily_job_scan.mjs` (no `--no-readme`, so README `<!-- DAILY-SCAN -->` block was rewritten) |
| Scan started | 2026-11-21T15:02:21Z |
| Fresh postings this scan | 466 |
| Merged board total (jobs.json) | 5,584 |
| Primary counts | servicenow 1,189 · salesforce 4,259 |
| Sources | adzuna 200 · linkedin 229 · smartrecruiters 12 · greenhouse 14 · remote 8 · ashby 2 · lever 1 · workday 0 |
| Liveness gate (`verify_links.py --days 2 --workers 16`) | 85 fresh rows probed · live=25 · dead=0 · unknown=60 (bot-walls kept) · nothing dropped |
| Site build (`tools/build_site.py`) | 5,060 jobs (servicenow 871 · salesforce 931 · other 3,258) · 779 mirror clusters collapsed · built 2026-11-21 15:07 UTC |
| README counts | header already correct: 5,487 live postings |

## Per-source notes

- **Adzuna CA API** (`max_days_old=14`, `sort_by=date`, demo keys): 200 matching postings — the freshness workhorse again; ~43% of fresh rows. Geos: Toronto, Ottawa, Mississauga, Canada-wide; queries incl. `servicenow`, `salesforce`, `apex`, `agentforce`, `salesforce cpq`, `it asset management`, `cmdb`, `itsm reporting`.
- **LinkedIn guest search**: 229 cards across 42 query×location tasks (7 general + 14 fresh/f_TPR=r86400 queries × Toronto and Canada). Two calls hit HTTP 429; the source still returned cards overall. No Playwright fallback needed.
- **SmartRecruiters ServiceNow**: 12 matches (ServiceNow's own Canadian engineering/admin roles force-tagged servicenow).
- **Greenhouse 14 / Lever 1 / Ashby 2**: small verified board APIs (NeuraFlash, D2L, Benevity, Loopio, EQ Bank, Alimentiv, etc.).
- **Workday CXS**: all 15 boards × 2 queries returned HTTP 429 on the scheduled pass (rate-limited at :00Z, persisting past it). Manual retry with corrected host/path split (`{tenant}.wd{N}.myworkdayjobs.com` host, bare `{tenant}` in the CXS path tenant slot, 8 s spacing) returned HTTP 200 on all 10 calls — but no Today/Yesterday Canada ServiceNow/Salesforce platform requisitions (newest Canada SN hit was BMO "ServiceNow CMDB Administrator", 9 days old; TD "Software Engineer III - Salesforce Data 360", 8 days old). Nothing fresh to add from Workday this hour; CI's 11:00 EST pass carries Workday.

## Companies checked (partners / telcos / banks / public sector)

- **Rogers**: `jobs.rogers.com` Phenom search returns a ~56 KB shell with zero server-side job rows — not scrapeable hourly; rely on LinkedIn/Adzuna for Rogers rows.
- **Bell**: `jobs.bell.ca` shows (0) for both servicenow and salesforce — zero reqs, not a scrape failure. Bell's real SN hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn; covered by the LinkedIn guest queries.
- **Canadian banks (Workday)**: BMO, TD, CIBC, Manulife, Interac — re-probed successfully post-429; no Today/Yesterday platform roles this cycle.
- **Canadian government / provincial portals**: `jobs.gc.ca` and `gojobs.gov.on.ca` are Radware-walled (captcha) — do not retry hourly; Job Bank is the proxy, and only title-named platform postings are trustworthy.
- **Partners scanned via board APIs**: NeuraFlash (Accenture), D2L, Benevity, Loopio, EQ Bank, Alimentiv — small board APIs; no fresh SN/SF platform roles this pass.

## Dedupe detail

- Scan-time dedupe: `jobs.json` URL keys (normalized: query string + trailing slash stripped) — the scan script merges fresh into existing before capping.
- README block: written against existing README URLs so already-listed postings are not repeated in the `<!-- DAILY-SCAN -->` tables.
- Site render: `build_site.py` unions jobs.json (leads) with README-only rows whose URL key is absent from JSON; mirrors collapsed by canonical title + employer + requisition id.
- Nothing was merged that already existed under a different URL (Adzuna re-issues the same role under new ids; company+title fingerprinting handles those).

## Lessons

1. Adzuna's dated API is the only source consistently returning same-week Toronto ServiceNow/Salesforce postings; keep it first in the hourly path. Job Bank/Eluta hang without timeouts — keep out of the hourly path.
2. Workday CXS 429s every hour at :00Z and persist for several minutes afterward; a manual retry ~4 minutes after :00Z with 8 s spacing recovers 200s. Use the correct host/path split (host includes `.wd{N}`, path tenant is bare). This hour's retry had 200s but no fresh Today/Yesterday Canada platform requisitions.
3. `verify_links.py --days 2` probes only fresh rows (85 probed, 0 dead) — fast enough for the hourly run; the full-board `--all` sweep stays daily.
4. Rogers' Phenom board and Bell's portal return zero rows server-side; public-sector portals are Radware-walled — record them as weekly (not hourly) checks and rely on LinkedIn/Adzuna/Ateko for that coverage.
5. Do not commit stray run artifacts (`raw/`, `leads-*.jsonl`, `README.BAK_*`) — stage only `jobs.json`, `README.md`, `FRESH_JOBS.md`, `public/*`, and the lessons file.

## Decision

466 fresh postings merged; 0 dropped by liveness gate; README.md and `public/` (jobs-data.json, index.html) rebuilt and pushed to main; GitHub Pages redeployed via `pages.yml`. Nothing new from Workday/Rogers/Bell/gov this cycle — recorded as a partial scan with full Adzuna/LinkedIn/ATS coverage.

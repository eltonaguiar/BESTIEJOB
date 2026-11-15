# JOBLESSONS_2026-11-15

BESTIEJOB hourly cron scan — 2026-11-15 00:00 EST (UTC-05). Target: fresh Toronto/GTA ServiceNow + Salesforce postings.

## Fresh verified job added this run (1)

| Posted | Role | Company | Location | Source | Notes |
|--------|------|---------|----------|--------|-------|
| 2026-11-15 | Lead Management Operations | Rogers Communications | Markham, Ontario, Canada | LinkedIn guest (job id 4490212417) | Salesforce lead management / Salesforce administration — business lead & SME for Lead Management within Salesforce; campaign structures, lead routing, automation workflows, Salesforce enhancements/releases/testing/adoption. In-office 5 days/week. Posted ~31 minutes ago. Added to jobs.json (tags: salesforce) and README (Other table). Commit 4e262e7, public/ rebuilt. |

## Sources checked this hour

- **LinkedIn guest search** (`jobs/search?keywords=&location=&f_TPR=r86400`, browser, no auth, ~6 s/query, 60 cards/page, absolute `datetime`):
  - ServiceNow Toronto: 60 cards; the 2 ServiceNow titles (Deloitte CMDB/GRC Solution Architect, job ids 4474558762 / 4474570325) were already on the board — dedupe working.
  - Salesforce Platform Administrator Toronto: 6 roles; only new match was the Rogers role above. Salesforce Solution Architect ×2 (4457034728 / 4457039647) already in README; Salesforce Manager comp + Kinaxis co-op + Bell grad program = non-matching.
  - Salesforce Platform Developer Toronto: 8 roles; all already on board or non-matching (senior "Software Developer – CRM" at S-M Software is generic CRM, not Salesforce Platform Dev I).
- **Workday CXS** (manual curl `--compressed`, single call): BMO `bmo.wd3/External` ServiceNow = 12 postings, none titled ServiceNow (search matches body text); TD `td.wd3/TD_Bank_Careers` ServiceNow = 12 postings, none titled ServiceNow. Scripted burst of 14 calls returned HTTP 422 across the board — Workday rate-limits/422s on rapid repeated calls; retry one call at a time with gaps.
- **Rogers careers** (date-sorted `sortColumn=referencedate&sortDirection=desc`): first page (Nov 11–14) = all sales/retail roles, no SN/SF titles. Rogers keyword search returns sales roles that merely mention SN/SF in the body (noise).
- **Bell** (`jobs.bell.ca`): confirmed zero reqs for servicenow/salesforce (skill: re-check weekly, not hourly).
- **Canadian government / public sector** (`jobs.gc.ca`, `gojobs.gov.on.ca`): Radware-walled — do not retry; Job Bank is the proxy but full-text search is noise (only trust title-named platform postings).

## Patterns / lessons for future agents

1. **LinkedIn guest search is the best hourly freshness oracle** — `f_TPR=r86400` via browser returns real cards with absolute dates; page 2 (`start=25`) re-serves page 1, don't bother. The guest API (`seeMoreJobPostings`) 429s after ~4 rapid calls and can return an authwall page with HTTP 200 + huge identical body — test length + digest distinctness, not just status.
2. **Dedupe on normalised URL + LinkedIn job id**: strip query strings/trailing slashes; LinkedIn job-id equality is a hard dedupe signal even when titles differ (e.g. two renamed titles sharing one job id = one posting). Check against `jobs.json` + `README.md` + `APPLIED.md` before adding. Vendor twins (two staffing firms, same client req, same title) are DISTINCT — keep both, dedupe on URL only.
3. **Workday CXS works but is flaky**: verified 200 pairs (bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site). Use `--compressed` (without it the gzip body decodes as nothing), send Origin + Referer + UA, one call at a time (bursts → 422). `bmo.myworkdayjobs.com` is NXDOMAIN — use the `wdN` host (`bmo.wd3...`). Dead ends: telus/rogers/kpmg/deloitte/cgi/sunlife/rbc `.wd3` → 404/422.
4. **Market shape (late 2026)**: ServiceNow-the-company posts only sales/SRE/security in Toronto; Salesforce-the-company posts nothing below 4 days and no Platform Admin/Dev I. Fresh platform work comes from banks (BMO/TD Workday), DXC, and GRC/IRM consultancies. Expect sparse hours — 1 fresh job this hour is normal, not a failure.
5. **README tables are pre-existing one-line mangled blocks** with stale heading counts (heading↔`<details>` mismatch is the baseline; `board_invariants` is red at ~136 errors regardless). `jobs_merge_inbox.py` additive insert is safe (read-safety check refuses row loss) and keeps counts via `_bump_counts`, but don't chase a perfect count reconciliation — it's pre-existing debt.
6. **Build & publish**: `jobs.json` is the system of record; `tools/build_site.py` unions `jobs.json` + README-only rows into `public/jobs-data.json` + `public/index.html`. The page only changes when `public/*` + `jobs.json` + `README.md` are committed to main. Always use `[skip ci]` (non-`[skip ci]` pushes run the chronic red audits). `pages.yml` redeploys eltonaguiar.github.io/BESTIEJOB/ on main push.
7. **Liveness gate**: `tools/verify_links.py --days 2 --workers 16 --blocklist dead_urls.txt` probed 74 fresh rows, 0 dead, nothing dropped. Only 404/410/451 mean dead; 403/429/5xx/transport errors are bot-walls on LIVE postings — keep them.

## Commit
`4e262e7 chore(jobs): merge 1 fresh Toronto Salesforce posting (Rogers) — 2026-11-15 00:00 EST scan [skip ci]` — pushed to origin/main.

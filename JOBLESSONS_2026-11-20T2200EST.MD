# JOBLESSONS_2026-11-20T2200EST

Hourly BESTIEJOB scan run: 2026-11-21T03:01Z (2026-11-20 22:00 EST). Cron job.

## What ran
`node scripts/daily_job_scan.mjs` (no --no-readme), then `python3 tools/build_site.py` + `scripts/sync_readme_counts.py`.

## Scan results by source
| Source | Matching postings |
|---|---|
| LinkedIn guest | 239 |
| Adzuna CA API | 177 |
| SmartRecruiters (ServiceNow) | 12 |
| Greenhouse | 14 |
| Lever (eqbank) | 1 |
| Ashby | 2 |
| Remote boards (RemoteOK/Jobicy/Remotive) | 9 |
| Workday CXS | 0 (all HTTP 422/429) |

## Dedupe verdict
- Scan: fresh=454, merged=5611 (was 5587 on origin/main).
- Diff against origin/main: +24 URLs, **all 24 are company+title twins** of rows already on the board (Adzuna re-issuing the same role under a new redirect_url id, e.g. TD/Amicis/OSI Digital repeats). **0 net-new distinct roles** this cycle — nothing false-duplicated, nothing dropped.
- Site build: 5,052 jobs (servicenow 867, salesforce 930, other 3,255), 805 duplicate mirrors collapsed, 30 applied hidden. Built 2026-11-21 03:22 UTC. README header already correct at 5,880 live postings.

## Pipeline bug found and fixed
Workday CXS search API returned HTTP 422 (`{"errorCode":"HTTP_422",...}`, empty message) for **every** board (BMO, TD, Salesforce, CIBC, Manulife, Interac, CAAT, Accenture, BDO, GDIT) in both the scan and a manual curl probe.
- Root cause: `scripts/daily_job_scan.mjs` `scanWorkday()` sent only `content-type` + `accept`. Workday requires `Origin: https://{tenant}.{wd}.myworkdayjobs.com`.
- Fix: added `origin` header to the Workday fetch in `scripts/daily_job_scan.mjs` (6 lines changed, committed).
- Verification: with `Origin`, `bmo.wd3/External` + "servicenow" returned HTTP 200 with 5 Toronto postings (CMDB Administrator, Technology Lifecycle Analyst, etc.), all 5–15 days old and already tracked via LinkedIn. So no fresh Workday rows were lost — just not collected this hour.
- Note: post-:00Z Workday 429s persist for several minutes; a manual retry probe 4+ minutes after the CI hour works (per prior runs). Leave Workday collection to the next CI hourly pass or retry the probe later.

## LinkedIn / Adzuna notes (re-confirmed this run)
- LinkedIn guest intermittently 429s yet still returns cards; healthy card HTML is ~31 KB and differs per query. Authwall returns HTTP 200 with constant ~337,822-byte body — test length + digest, never status alone.
- Adzuna demo keys (`54ce986e` / `db851...`) work; 503s after ~4 rapid queries — space calls ≥3 s.

## Employer/partner sweep (Rogers, Bell, GC, Elite partners)
- Rogers: `jobs.rogers.com` Phenom search renders a zero-row shell server-side — rely on LinkedIn/Adzuna; do not retry hourly.
- Bell: `jobs.bell.ca` shows (0) for both servicenow and salesforce — zero reqs; re-check weekly. Bell's real SN hiring surfaces via Ateko / FX Innovation (Bell-backed) on LinkedIn (already in scope of LinkedIn scan).
- Canadian government portals (jobs.gc.ca, gojobs.gov.on.ca) are Radware-captcha walled — do not retry; Job Bank is the proxy, trust only postings whose *title* names the platform.
- Web search for Rogers / Bell / Ateko / GC ServiceNow-Salesforce Toronto roles returned only LinkedIn profile pages and generic content — no verifiable fresh posting URLs. Dropped unverifiable aggregator leads rather than adding them.

## Files changed (this commit)
- `jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json` — refreshed feed (5,611 rows).
- `README.md` — `<!-- DAILY-SCAN -->` block rewritten.
- `public/jobs-data.json`, `public/index.html` — rebuilt GitHub Pages site (5,052 cards).
- `scripts/daily_job_scan.mjs` — Workday `Origin` header fix.
- `JOBLESSONS_2026-11-20T2200EST.MD` — this file.

## Next run (next hour)
Re-run `node scripts/daily_job_scan.mjs`; Workday boards should answer now that `Origin` is sent, barring :00Z+ 429s — retry the probe after a few minutes if they 429 again.

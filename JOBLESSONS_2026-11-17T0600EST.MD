# JOBLESSONS_2026-11-17T0600EST — BESTIEJOB hourly scan (Toronto SN/SF)

**Run:** 2026-11-17 06:00 EST (cron). **Repo:** eltonaguiar/bestiejob `main`. Local clone: `C:\Users\zerou\bestiejob`.
**Board state before run:** 2,825 jobs in `jobs.json`; 7,530 dedup URLs (jobs.json + README). **Result: 0 fresh mergeable Toronto ServiceNow/Salesforce jobs; board already current.**

## Channels scanned this run

| Channel | Query / scope | Result |
|---|---|---|
| Workday CXS (curl) | 8 tenants × {ServiceNow Toronto, Salesforce Toronto}: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site | All HTTP 200. SN/SF Toronto hits (e.g. TD Senior Solution Architect ServiceNow "Posted Yesterday", BMO ServiceNow CMDB Administrator) — every one already on board |
| LinkedIn guest (browser) | keywords ServiceNow + Salesforce, location Toronto, f_TPR=r86400; 60 cards each = 120 cards | Every SN/SF-relevant card already on board. Standout: Salesforce Administrator, HCLTech, Toronto (18h ago) — already on board |
| Gap scan / Adzuna | raw/gap_scan_2026-11-17.json (04:04 EST), ~53 items all Nov-16 postings | All 8 spot-checked Toronto SN/SF adzuna URLs already on board |
| Rogers careers | jobs.rogers.com date-sortable re-fetch (HTTP 200, dates Nov 13–17) | Zero ServiceNow/Salesforce mentions |
| Bell | jobs.bell.ca | Known zero reqs (skipped per prior finding) |
| Public sector (Ontario/GC) | gojobs.gov.on.ca / jobs.gc.ca | Radware-walled; Job Bank only, title must name platform |

## Dedupe
- All candidate URLs normalized (strip query string + trailing slash) and checked against the combined dedup set (jobs.json + README). 0 new URLs passed.
- No README/table changes, no `jobs.json` changes, no `public/` rebuild needed this run.

## Lessons for future agents
- **Workday CXS is reachable from this host via `curl --compressed`** with `Origin`/`Referer` headers; only known-good `tenant|site` pairs answer (200). Guessing tenants (capgemini, kyndryl, ibm, cgi, cognizant, telus, rogers, kpmg, scotiabank, intact, loblaw, cprail) returns 422; rbc/pwc/sunlife return 404. Do not waste calls guessing.
- **LinkedIn guest search page is readable as a guest** (`new_tab` on `linkedin.com/jobs/search?...&f_TPR=r86400`, ~6 s/query, 60 cards/page, no auth). The `seeMoreJobPostings` API 429s after ~4 rapid queries — space batches ≥25 s, and always test length+digest distinctness, not just HTTP 200 (authwall returns 200 with a stale 337 KB body).
- **Adzuna 503s after ~4 rapid queries** — space calls ≥3 s. Adzuna recycles IDs; dedupe by the detail page's JSON-LD `datePosted`, not the API `created` date.
- **Rogers careers is date-sortable and reachable; Bell is zero.** Re-check Rogers weekly, not hourly.
- **Freshness convergence:** all past-24h Toronto SN/SF LinkedIn cards converge to the same ~20 postings that earlier hourly scans already boarded. Re-running LinkedIn + Workday the same day yields diminishing returns; rotate sources instead (partner portals, Job Bank proxy, Greenhouse/Lever/Ashby `ats_board_sweep.py --days 2`, public-sector proxy).
- **Commit hygiene:** lessons-only pushes use `[skip ci]` to avoid triggering the chronic red board-invariants audits. A non-[skip ci] push runs Job Source Truth Check + board invariants (pre-existing ~136 errors on main, not a regression).

## Recommended next run
Rotate to sources not hit today: ServiceNow/Salesforce partner & Elite Partner career pages, Greenhouse/Lever/Ashby ATS sweep (`--days 2`), Job Bank title-anchored proxy, and the public-sector portal check. Re-run LinkedIn + Workday no sooner than the next cadence cycle.

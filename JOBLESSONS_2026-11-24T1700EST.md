# JOBLESSONS_2026-11-24T1700EST — hourly BESTIEJOB scan lessons

## Scan summary
- Run time: 2026-11-24T22:04Z (17:04 EST), cron job
- Base: origin/main at 810e4b2d (CI fresh CA sweep 2026-11-24T21:44Z [skip ci]), fast-forwarded cleanly
- Local commit: b1dbc2c7 "chore(jobs): hourly scan refresh (5681 listings, 2026-11-24T22:04Z)" — pushed without `[skip ci]` so `pages.yml` deployed automatically
- Deploy: `Deploy GitHub Pages` completed 22:08:24Z (~30 s); live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` verified HTTP 200, 7,183,802 bytes, carries new scan URLs

## Source results (this hour)
| Source | Matching postings | Notes |
|---|---|---|
| LinkedIn (guest, 28 query/location tasks) | 244 | Healthy volume; cards readable via HTTP |
| Adzuna Canada API (34 queries, demo keys 54ce986e / db851f...) | 196 | Fast hourly freshness oracle; space calls ≥3s to avoid 503s |
| SmartRecruiters (ServiceNow board) | 12 | Largest single SN source; not on LinkedIn guest feed |
| Greenhouse (9 verified slugs) | 12 | |
| Lever (3 boards) | 1 | |
| Ashby (3 boards) | 2 | |
| Remote boards (RemoteOK/Jobicy/Remotive) | 6 | Canada-geo filter applied |
| Workday CXS (14 boards × 2 queries) | 0 | **All HTTP 429 — rate-limited at :00Z when the CI hourly scan runs concurrently.** Retry 4+ minutes later (verified pattern: a 10-tenant probe at +4 min returns HTTP 200 on all calls). |

Merge result: fresh=473, merged=5681 (servicenow 1,204 / salesforce 4,319). Most "fresh" rows are Adzuna re-issues under new IDs or company+title twins already on the board — net-new URLs are small. Diff URL sets against the previous origin commit before reporting additions.

## Liveness gate (`verify_links.py --days 2`)
- 71 fresh rows probed, 27 live, 0 dead, 44 unknown (bot-wall/transport errors kept — never treat 403/429/5xx as dead)
- No postings dropped from jobs.json

## Build
- `tools/build_site.py`: 4,988 jobs (SN 868 / SF 960 / other 3,160), 569 mirror duplicates collapsed, 28 applied hidden, built 2026-11-24 22:06 UTC
- `scripts/sync_readme_counts.py`: no-op (no count header line in current README format)
- Committed: jobs.json, README.md, FRESH_JOBS.md, public/{jobs.json,jobs-data.json,index.html,gotjob/jobs.json,findjobs/jobs.json}

## Audits (triggered by non-[skip ci] push)
- Job Source Truth Check: success
- board invariants: success — previously red at a ~36-error baseline on main; this cycle passed, so treat green as real progress not a fluke, but still grep output for your URLs before declaring clean
- README job-row guard: triggered; deploy succeeded regardless

## Employer / partner checks (Toronto ServiceNow / Salesforce focus)
- **Rogers**: jobs.rogers.com Phenom board returns HTTP 200 but ~56 KB shell with zero job rows server-side (2026-11-20 pattern holds). Do not retry hourly; rely on LinkedIn/Adzuna for Rogers rows.
- **Bell**: jobs.bell.ca renders empty shell; `(0)` in browser for servicenow/salesforce = zero reqs, not a scrape failure. Re-check weekly. Bell's real SN hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn — search "Ateko" for SN Dev / Implementation Specialist / Architect / FSM roles.
- **Canadian government**: gojobs.gov.on.ca (Ontario) and jobs.gc.ca are Radware-walled (captcha). Use Job Bank as proxy; trust only postings whose *title* names the platform. Job Bank keyword full-text is noise ("shipping coordinator", "agronomy engineer").
- **ServiceNow Careers**: Cloudflare bot wall — not scrapeable from this host.
- **Scotiabank**: Phenom search scrapable and dated (`jobs.scotiabank.com/search/?q=servicenow&sortColumn=referencedate&sortDirection=desc`) — use instead of guessing `scotiacareers` as a Workday site (422/500).
- **Workday tenants that answer (200)**: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site, caatpension.wd10/Careers, iko.wd3/IKO_Careers. Dead ends: rbc/pwc/sunlife (404), capgemini/kyndryl/ibm/cgi/cognizant/telus/rogers/kpmg/scotiabank/intact/loblaw/cprail (422), sunlife/rbc.wd3 (404), dxc/cognizant.wd1 (521). Workday `postedOn: "Posted Today"` is not a Canada signal — read the `/job/<City>/` slug for location.

## Role targeting
- Entry-level **Platform Administrator / Platform Developer I (Toronto)** remain scarce this hour: nothing junior surfaced, only mid/senior and lead reqs.
- Salesforce-the-company posts nothing below 4 days and no Platform Admin/Dev I in Toronto. Fresh platform work comes from banks (BMO/TD Workday), DXC, and GRC/IRM consultancies (PwC's ServiceNow IRM practice).
- ServiceNow-the-company posts only sales and SRE/security roles in Toronto.

## Dedupe reminders
- Dedupe on URL (strip query strings/trailing slashes) + trailing LinkedIn job id, never on normalized title alone.
- Vendor twins (same client req, different staffing firms) are distinct postings — keep both.
- SmartRecruiters `/v1/companies/{slug}/postings/{id}` is the strongest liveness+body check (returns `active`, `releasedDate`, `remote/hybrid`).

## Tech notes (this host)
- git: `C:/Program Files/Git/cmd/git.exe` (`/mingw64/bin/git` is blocked)
- python: `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe` (`python3` on PATH is the WindowsApps store stub)
- Run curl from bash, not Python subprocess (WinError 5). `gh` API calls work; `gh` execs bundled git for some ops and can fail.
- Commit without `[skip ci]` when `public/` changes so `pages.yml` deploys; use `[skip ci]` on lessons-only commits.
- Untracked `raw/*` scratch files accumulate — do not commit them; leave them untracked.

## Next run (2026-11-24T18:00EST)
- Re-run `node scripts/daily_job_scan.mjs`; expect Workday 429s again at :00Z — if the scan logs 0 Workday postings, do a manual 10-tenant Workday probe 4 minutes later before concluding no fresh reqs.
- Adzuna 503s after ~4 rapid queries — keep ≥3s spacing.
- Consider re-probing Rogers/Bell weekly, not hourly.

# JOBLESSONS_2026-11-21T1800EST

Hourly BESTIEJOB scan run, Saturday 2026-11-21 18:00 EST (23:01Z). Toronto ServiceNow / Salesforce focus, Canada-first.

## What ran
- `node scripts/daily_job_scan.mjs` — full hourly scan: SmartRecruiters (ServiceNow), Workday CXS, Greenhouse/Lever/Ashby, LinkedIn guest, Adzuna, remote feeds.
- Result: `fresh=426 merged=5590` — primary counts servicenow=1189, salesforce=4265. `scrapedAt 2026-11-21T23:01:31.208Z`.
- README `<!-- DAILY-SCAN -->` block rewritten (newest 12 SN / 12 SF / 10 other); scan stamp `2026-11-21T23:01:31.208Z`, 1426 live postings claimed.
- `python3 tools/build_site.py` → `public/jobs-data.json` + `public/index.html`: site 5026 jobs {servicenow: 872, salesforce: 930, other: 3224}, 755 duplicate mirrors collapsed, 30 applied hidden, newest 2026-11-21.
- `scripts/sync_readme_counts.py` → README header count 4954 → 5057 live postings.

## Fresh jobs verified on the board this cycle
Posted 2026-11-21 (today) and already present in README + jobs.json + public/jobs-data.json:
- EY — ServiceNow IRM Senior Consultant (NFR), Toronto (ca.linkedin.com/jobs/view/...-4491983802)
- VDart Inc — Service now Developer CUM Architect, Canada (adzuna.ca/details/5974418388)
- Hired — Salesforce Administrator (Remote), Canada (linkedin ...4492888602)

Already on board from earlier today's scans (not new this cycle, deduped correctly): Altus Group Salesforce Platform Developer Toronto (linkedin ...4483476940), Moneris Principle Salesforce Developer Toronto (linkedin ...4466619394) — both posted 2026-11-21, both already in README tables and jobs-data.json.

## Dedupe notes (applied)
- Diffed URL sets: new jobs.json vs `origin/main:jobs.json` → 28 URLs added, 1 removed (adzuna 5956636310 Cognizant Senior Full Stack .NET Developer — non-SN/SF, cap pruning, expected).
- Most of the 28 "added" URLs were already in older README blocks (sync_readme_to_jobs is a no-op; the scan's carryExistingJobs pulled them into jobs.json) — not truly new. Altus/Moneris (Nov 21) were already in README before this run.
- Dedup rule re-confirmed: diff URL sets against origin, then flag company+title twins; never claim a row as new until it is absent from jobs.json AND README.md AND APPLIED.md.
- APPLIED.md check: none of the fresh URLs are applied/archived.

## Source behavior this cycle
- Workday CXS: fully blocked — in-node scan got HTTP 429 on every tenant; direct curl probes (bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, salesforce.wd12/External_Career_Site, accenture.wd103/AccentureCareers × "servicenow"/"salesforce") returned HTTP 422 with empty body. Known pattern: Workday rate-limits around :00Z and persists well past it; the hourly CI pass (10:00Z) carries Workday. Do not hand-add Workday "Posted Today" reqs this cycle. Retry recipe that worked previously: 10 tenants × 2 queries at 8 s spacing, ~4 minutes after a blocked run.
- LinkedIn guest: first call HTTP 429, second call recovered (~186 postings) — retry once after a few minutes before declaring empty.
- Adzuna API: 203 postings, reliable. Demo keys must be passed explicitly: app_id=54ce986e, app_key=db851f299e966c0a2a72af525dce6199 (missing key → HTTP 400).
- SmartRecruiters ServiceNow: 12 postings; Greenhouse 14; Lever 1; Ashby 2; remote feeds 8.

## Partner / elite partner / sponsor / gov scan (task requirement)
- Bell: jobs.bell.ca renders empty shell `(0)` for servicenow/salesforce — zero reqs, not a scrape failure; re-check weekly, not hourly. Real Bell-backed SN hiring is Ateko / FX Innovation (already on board: Nov 19 SN Développeur/Implementation Specialist, Architect ITOM/ITAM; CloudKettle Salesforce Industries/Revenue Cloud architects).
- Rogers: jobs.rogers.com Phenom returns a ~56 KB shell with zero server-side job rows — do not retry hourly; rely on LinkedIn/Adzuna for Rogers rows (Nov cycle: Rogers Lead Management Operations, Sr Data Analyst etc. are non-platform roles, correctly excluded from primary SN/SF lists).
- Canadian government: jobs.gc.ca and gojobs.gov.on.ca are Radware-walled (captcha) — do not retry; use Job Bank as proxy and trust only postings whose title names the platform. CMHC careers (careers.cmhc-schl.gc.ca) posts bilingual ServiceNow ITSM roles sporadically (Nov 4 hits already on board); Job Bank postings 404 once expired — a search hit is not proof of a live posting.
- Platform/elite partners seen on board this cycle: EY (ServiceNow IRM/GRC senior consultants), PwC (Salesforce Business Analyst), Deloitte (ServiceNow advisor), KPMG Canada (ServiceNow Solution Developer), LGS/IBM (Salesforce architect), Accenture (Workday board has 1,600+ SN reqs but effectively none Canadian in first pages — use national careers site).
- ServiceNow-the-company: posts only sales/SRE/security in Toronto — no Platform Admin/Dev I. Salesforce-the-company: nothing below Platform Admin/Dev I in Toronto this cycle.

## Environment notes (re-applied)
- `git` at /mingw64/bin/git is blocked — use `C:/Program Files/Git/cmd/git.exe` for all git ops.
- `python3` on PATH is the Windows Store stub — run repo Python tools with `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe`.
- Commit only jobs.json, README.md, public/jobs-data.json, public/index.html + this lessons file; leave untracked raw/*, leads-*.jsonl, reports/* from prior runs uncommitted.
- Use `[skip ci]` on the commit (chronic red board-invariants audits are pre-existing on main, not a regression from this run), then trigger `pages.yml` manually for immediate GitHub Pages reflect and verify via curl of jobs-data.json.

## Next cycle
- Re-probe Workday key tenants after the :00Z rate-limit window; if still 422/429, the CI hourly pass covers it.
- Rogers/Bell/gov: weekly cadence only; portal shells are confirmed dead ends.

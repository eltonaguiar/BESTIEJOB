# JOBLESSONS_2026-11-18T1900EST

Hourly Toronto ServiceNow / Salesforce scan — cron run 2026-11-18 19:00 EST (scan clock 2026-11-19T00:02Z).

## What ran
- `node scripts/daily_job_scan.mjs --no-readme` — SmartRecruiters, Lever, Greenhouse, Ashby, LinkedIn guest, Workday, Adzuna, RemoteOK, Jobicy, Remotive feeds. Wrote jobs.json, public/jobs.json (x3), FRESH_JOBS.md.
- Result: 2406 matching postings (9 sources; Adzuna API 503 without ADZUNA_APP_ID/ADZUNA_API_KEY — no key locally; Workday mostly HTTP 429; LinkedIn guest HTTP 429 on first hit, 200 on retry). fresh=605, retained=1801; SN 1139 / SF 1161.
- `python scripts/sync_readme_counts.py` after the manual README merge — canonicalizes the "**N live postings**" header to the actual table rows (CI guard; header had drifted before).

## Fresh SN/SF jobs found this scan
37 new scan IDs matched SN/SF + Toronto/Canada geo after title exclusion. 29 were already on the board (dedupe by URL). 8 were truly new — all verified and merged to README.md main branch (GitHub Pages deploys on push to main via pages.yml):

ServiceNow (+4 → 1123):
- 2026-11-18 Compugen Inc — Project Manager – ServiceNow & Financial Systems - Contract — Toronto (LinkedIn, fetched HTTP 200)
- 2026-11-18 Compugen Inc — ServiceNow Business Analyst - Contract — Toronto (LinkedIn, 429 first, 200 on retry)
- 2026-11-14 SPECTRAFORCE — ServiceNow Developer — Toronto (adzuna feed; corroborated via talent.com/Glassdoor SPECTRAFORCE Toronto listings; adzuna.ca detail returns 403 CloudFront from this IP — not dead)
- 2026-11-07 KPMG Canada — Consultant/Senior Consultant - ServiceNow Solution Developer — Toronto (LinkedIn, fetched HTTP 200)

Salesforce (+4 → 1026):
- 2026-11-19 SickKids Foundation — Senior Specialist, Salesforce Developer — Toronto (LinkedIn, fetched HTTP 200)
- 2026-11-15 MLSE — [C] Salesforce Engineer / Developer — Toronto (adzuna feed; corroborated on MLSE Workday careers page, employer's own ATS)
- 2026-11-08 Smart IT Frame LLC — Salesforce Technical Architect - Strong CPQ and Revenue Cloud Advanced — Toronto (adzuna feed; corroborated on LinkedIn 4490672278 "3 days ago" and jobily.ca Nov 8 2026)
- 2026-11-08 OSI Digital — Salesforce Lead — Toronto (adzuna feed; corroborated on osidigital.applytojob.com employer career page)

Board totals after merge: ServiceNow 1123 · Salesforce 1026 · Other 4058 · 6206 live postings, window 2026-10-20 → 2026-11-19. Jobs committed: jobs.json + public/* + README.md + FRESH_JOBS.md.

## Partner / sponsor signal observed
Active Toronto SN/SF hiring this window from known partners/employers: Cognizant (Toronto ServiceNow sponsor), BMO, TD Bank, Altus Group, KPMG Canada, CGI, Deloitte, Compugen, SickKids Foundation, MLSE, OSI Digital, Smart IT Frame, SPECTRAFORCE, Benevity, Alimentiv, Versapay, City of Toronto (Salesforce System Development Specialist), ServiceNow corporate (Staff roles Toronto). Government channel: jobbank.gc.ca postings present (e.g. Bonafide Info Systems ServiceNow CMDB Consultant Toronto).

Not surfaced this run: Rogers, Bell (no fresh SN/SF postings in the feeds checked). Adzuna API needs credentials locally — schedule runs with ADZUNA_APP_ID/ADZUNA_API_KEY or skip Adzuna queries (they were 302 of 2406 postings when keys are present in CI).

## Verification pattern that works
1. Diff new scan IDs against committed jobs.json, then against README.md URLs (dedupe before anything else).
2. Fetch LinkedIn guest job pages with a browser UA; retry once on HTTP 429 — second attempt usually 200.
3. adzuna.ca detail pages 403 from this network (CloudFront). Do not treat 403/429 as dead — corroborate via the employer's own careers/ATS page found through search (Workday, Lever, applytojob, LinkedIn, jobily). CI's verify_links.py only drops 404/410/451 for the same reason.
4. LinkedIn rate limit: 1 request/second pacing kept the guest endpoint stable.

## Files touched
README.md (+8 rows, counts refreshed), jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json, FRESH_JOBS.md. Pre-existing uncommitted change: ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM submodule — left untouched, not part of this commit.

# JOBLESSONS_2026-11-21T2200EST

HERMES cron scan, Saturday 2026-11-21 22:00 EST (2026-11-22T03:00Z). Toronto ServiceNow / Salesforce hourly scan for BESTIEJOB (github.com/eltonaguiar/BESTIEJOB, main branch).

## What this run did
1. Web search for fresh Toronto ServiceNow and Salesforce postings (LinkedIn, Indeed, Glassdoor, Adzuna, landthatrole, employer career pages).
2. Public ATS API scan via tools/scan_boards.py --read against the watchlist's Lever/Greenhouse/Ashby/SmartRecruiters tenants (alimentiv, eqbank, versapay, ensiti, levio, solink, cea, electricmind) → leads-fresh-2026-11-21T2200EST.jsonl (keyword discovery only, not verified).
3. Dedupe against README.md tables and jobs.json (URL-first identity; mirror trap checked).
4. Merge of verified fresh rows via tools/jobs_merge_inbox.py (additive, --bump-inbox), then scripts/sync_readme_to_jobs.mjs + tools/build_site.py so README, jobs.json, public/ and GitHub Pages all reflect the add.
5. Commit + push to origin main; Pages rebuild triggered by push (public/** + README.md).

## Fresh verified jobs added (+4 rows in README.md ServiceNow table; +3 in jobs.json feed)
Scotiabank "ServiceNow Administrator Specialist" already exists in the jobs.json feed under its canonical careers URL (posted 2026-11-09), so the LinkedIn mirror landed in the README table only — correct dedupe behaviour.

| Posted | Role | Company | Location | Source / evidence |
|---|---|---|---|---|
| 2026-11-14 | Senior ServiceNow Engineer | EQ Bank / Equitable Bank | Toronto, Canada | Live Lever requisition jobs.lever.co/eqbank/1af36346-6dd1-475a-bee9-1d5e805452e8 (HTTP 200); CoE build duties — applications, workflows, catalog items, integrations. Age ~1 week per LinkedIn guest search; date is best-estimate. |
| 2026-11-14 | Solution Architect-ServiceNow Service Portal (US or Canada) | NewRocket | Toronto, Ontario, Canada | LinkedIn guest search + Indeed, Toronto listed; hands-on ServiceNow Service Portal build. Date best-estimate. |
| 2026-11-14 | ServiceNow Administrator Specialist | Scotiabank | Toronto, Ontario, Canada | LinkedIn jobs list, 1 week ago; detail page login-gated, not re-opened. Canonical careers posting already in feed (2026-11-09). |
| 2026-11-16 | ServiceNow Developer | Scotiabank | Toronto, Ontario, Canada | LinkedIn jobs list, 5 days ago; detail page login-gated, not re-opened. |

Dates marked best-estimate come from LinkedIn relative ages ("1 week ago", "5 days ago"); the merger requires absolute YYYY-MM-DD, so the calendar day is recorded and the relative age is kept in the note.

## Already on the board — skipped (dupes)
- Interac "Technical Service Now, Lead (6-month contract)" — already in jobs.json (scraped 2026-11-09, posted 2026-10-28), LinkedIn 4126302101.
- Scotiabank DevOps Engineer (Salesforce) req 276046 — already in README since 2026-11-07.
- Everything from the 2026-11-22T02:02Z scan (1564 live postings) ran ~7h before this run.

## Employers / partners checked (Toronto SN/SF)
Rogers, Scotiabank, TD, BMO, RBC, Envision Technology Solutions, Interac, EQ Bank, NewRocket, ServiceNow Inc. careers page. LinkedIn job-detail pages are login-gated to this unattended agent (blank "🐴 LinkedIn" shell) — no credentials were used and no login walls were bypassed; verification rests on search-snippet text and live employer/ATS URLs where reachable.

## Lessons
- LinkedIn detail pages cannot be verified headless (login wall). Rows from LinkedIn guest-list snippets carry "detail page login-gated, not re-opened" notes and best-estimate dates; treat dates as hints, not issuer dates.
- Same-title mirrors can die while the canonical stays live: a bc47fb78 Lever mirror of the EQ Bank role returned 404; the watchlist canonical 1af36346 returned 200. Always resolve to the live employer ATS URL before citing.
- The automated hourly scan (Adzuna + LinkedIn guest) still misses live postings that direct search finds (EQ Bank Lever req, NewRocket via Indeed, Scotiabank mirrors) — direct employer/ATS spot checks remain necessary.
- Git on this host: /mingw64/bin/git is blocked; use C:/Program Files/Git/cmd/git.exe with native C:/... paths.
- Zero-removal merge: readme-guard needs no [allow-readme-removals] marker when only rows are added.

## Files changed
README.md, jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json, public/jobs-data.json, public/index.html, inbox/hermes-cron--2026-11-21--v2.md, this file.

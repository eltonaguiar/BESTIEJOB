# JOBLESSONS_2026-11-16 — hourly cron scan (00:00 EST / 05:00 UTC)

## Result this run
- Fresh Toronto ServiceNow/Salesforce scan performed: Workday ATS todayfeeds inbox (04:01Z), gap_scan (adzuna/workday/greenhouse/lever/ashby/jobbank, 01:03Z), LinkedIn guest, plus review of jobs.json.
- **0 brand-new on-target discoveries this hour** beyond what jobs.json already held.
- **2 verified fresh ServiceNow roles merged into README.md** (top of the ServiceNow table, newest first; both posted 2026-11-16, LinkedIn guest search, last 24h):
  - ServiceNow ITOM Developer — TechNeptune Consulting Inc. — Toronto, Ontario, Canada — https://ca.linkedin.com/jobs/view/servicenow-itom-developer-at-techneptune-consulting-inc-4489717217
  - ServiceNow CMDB Consultant — TechNeptune Consulting Inc. — Toronto, Ontario, Canada — https://ca.linkedin.com/jobs/view/servicenow-cmdb-consultant-at-techneptune-consulting-inc-4489716220
- Both were already present in jobs.json (ingested by the 03:49Z fresh CA sweep / retained by the 05:16Z hourly scan: jobs.json 2766 listings, techneptune count = 2), not in APPLIED.md, not duplicates. This run's contribution: adding them to the README table (ServiceNow jobs 1272 -> 1308; "as of" -> 2026-11-16) and rebuilding public/.
- Live page verified: both TechNeptune URLs present in jobs-data.json; check_site_links.py OK (5746 jobs, newest 2026-11-16).

## Off-target roles skipped (do not merge)
- Salesforce "Technical Architect Director - PubSec - Mulesoft Canada", "Salesforce Technical Architect with Revenue Cloud (RCA)", "Senior Lead Solutions Architect, Salesforce Migrations", generic "Salesforce Developer"/"Salesforce Engineer/Developer"/"Technical Salesforce Senior Associate"/"Sr. Salesforce CRM Development Lead" — the board targets Platform Administrator / Platform Developer I (esp. entry-level/junior); generic Salesforce Dev is secondary, architect/migration/Revenue Cloud are not Platform Dev I.
- ServiceNow "Staff Site Reliability Engineer" (ServiceNow Inc.) — vendor product SRE/security, not platform admin/dev; market shape note: ServiceNow-the-company posts only sales/SRE/security in Toronto.
- Non-Toronto / explicitly US or offshore (Vancouver, Montréal, Québec, Calgary, Any Location/Remote where not Toronto-first) — board is Toronto-first / Canada.
- Lane Four "Salesforce Consultant" / "Salesforce Administrator" — undated (no postedDate); the merger skips undated rows, and freshness can't be confirmed.

## Dedup & verification procedure (followed this run)
1. Read jobs.json (system of record) + README tables + APPLIED.md.
2. Normalize URLs (strip query strings/trailing slashes); exclude anything already in jobs.json, README, or APPLIED.md.
3. Confirm freshness (posted today/yesterday), direct posting deep-link (is_listing_url() rejects hubs/search pages), and platform targeting (ServiceNow in title/description/certs; Salesforce = Platform Admin/Platform Dev I).
4. Write to jobs.json first; README is a capped rendered view. build_site.py unions jobs.json (leads) + README rows whose URL key is absent from JSON — so a row only in jobs.json still renders on the page; a row only in README renders only if not in jobs.json.
5. Rebuild: python3 tools/build_site.py → public/jobs-data.json + public/index.html; then python3 scripts/check_site_links.py (pages.yml guard; must pass before push).
6. Commit README.md + public/ + jobs.json; push WITHOUT [skip ci] so pages.yml redeploys live board. [skip ci] only for docs-only commits.

## Recurring collision pattern (hit this run)
- The automated hourly scan (`chore(jobs): hourly scan refresh ... [skip ci]`) pushed to origin/main twice during this run (04:16Z → 2762 listings, 05:16Z → 2766 listings), causing non-fast-forward rejections.
- Fix each time: `git fetch origin`, `git rebase origin/main`, `git checkout --ours public/*` (upstream wins on generated files), keep my README change, `python3 tools/build_site.py`, amend, push. Never `--force` — that would destroy the scan's jobs.json/public work.

## Market-shape notes (late 2026, stable)
- ServiceNow-the-company: Toronto postings are sales/SRE/security only; no Platform Admin/Dev I.
- Salesforce-the-company: nothing below 4 days old, no Platform Admin/Dev I in Toronto.
- Fresh platform work comes from banks (BMO/TD/CIBC Workday), DXC, and GRC/IRM consultancies (PwC ServiceNow IRM practice). Accenture Workday has 1,600+ ServiceNow reqs but effectively none Canadian on page 1 — use its national careers site.
- Rogers careers is date-sortable and has SN/SF reqs; Bell returns zero for both platforms (re-check weekly, not hourly). Workday CXS known 200 tenants: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, salesforce.wd12/External_Career_Site, accenture.wd103/AccentureCareers, gdit.wd5/External_Career_Site, caatpension.wd10/Careers, iko.wd3/IKO_Careers — POST /wday/cxs/{tenant}/{site}/jobs with curl --compressed, wdN host.

## Extractor quirk
- `jobs_consolidate.extract_rows` skips any README table line that doesn't start with `|` — the glued `<details><summary>...|| first-row` line is never parsed, so README heading counts and extractor counts diverge (baseline debt; count-disagreement is a warning, not an error). Do not chase a perfect heading count; protect that jobs-data.json carries the new URLs and check_site_links passes.


## 2026-11-16 07:00 EST run — null result (0 fresh jobs merged)

Window: 2026-11-15 → 2026-11-16, Toronto-first ServiceNow / Salesforce; Canada scope (banks, government, partners, Rogers, Bell).

Board state: local main == origin/main 00f00e3 after rebase; README already carries the two TechNeptune ServiceNow roles from the 00:00 EST run (ServiceNow jobs 1308, "as of" 2026-11-16).

Sources checked, all zero new merged:

- **Workday CXS** (`curl -s --compressed`, POST `/wday/cxs/{tenant}/{site}/jobs`, body `{"appliedFacets":{},"limit":20,"offset":0,"searchText":q}`, one call at a time, ~6 s gaps): 18 probes × {ServiceNow, Salesforce} — bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, sunlife.wd3/Experienced-Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site — all HTTP 200. Canada SN/SF hits: BMO Applications Support Analyst (Posted Yesterday, R260028077 — already aboard from the 2026-11-15 21:00 EST run), BMO ServiceNow CMDB Administrator R260030992 / Technology Lifecycle Analyst R260030995 / SAM Administrator–ITAM R260030096 (4–13 days, recurring requisitions aboard), TD Software Engineer III–Salesforce Data 360 R_1515074 (3 days, aboard), Manulife Salesforce Functional Analyst Waterloo (14 days, aboard). Interac Senior BSA (ServiceNow) + QE Senior Specialist (ServiceNow Platform), Toronto — 30+ days, outside fresh window. All other hits non-Canada (Accenture/GDIT/Salesforce corporate offshore + US). **0 fresh.**
- **LinkedIn** (web-search cross-check; guest pass unavailable — Chrome profile locked, direct LinkedIn 301/403): six "1 day ago" (2026-11-15) Toronto ServiceNow leads — Brookfield contract dev 4481508851 (already aboard), Lightspeed 4466234344 (in APPLIED.md — hard exclude), Cloud Resourcing 4397607517, Brainhunter 4474956448, ThoughtStorm 4480281328, iPartner/Cognizant 4480455968 (none in jobs.json/README.md/APPLIED.md). Not merged: cannot re-fetch live guest-detail pages this run to confirm freshness and that the posting is live. Deferred to next run.
- **gap_scan** (`raw/gap_scan_2026-11-16.json`, 01:03Z): partner/Elite-sponsor career sites (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) — Lane Four "Salesforce Consultant" undated (merger skips undated rows); all other sites returned 0 postings. **0 fresh.**
- **Public sector**: gojobs.gov.on.ca Radware-walled; jobs.gc.ca NXDOMAIN; Job Bank OPS feed 0 platform-titled postings; City of Toronto 0 SN/SF cards; inbox todayfeed (Workday, 04:01Z) = data-engineering roles only, no SN/SF.
- **Rogers / Bell**: Rogers careers = sales/retail only, no SN/SF platform titles; Bell JS-rendered 303, not curl-scrapeable.

Dedupe: URL + title|company|city fingerprint held against jobs.json + README.md + APPLIED.md; nothing new survived.

Outcome: no board-data commit — README.md, jobs.json, and public/ unchanged; live page (https://eltonaguiar.github.io/BESTIEJOB/) remains current from the 00:00 EST push. Only this lessons entry committed ([skip ci]).

New lessons:

1. **Workday CXS `searchText` matches body text, not just titles** — BMO's "ServiceNow" probe returned "Applications Support Analyst" etc.; read the title before counting a hit. Recurring BMO requisitions reappear under the same job IDs (R260030992, R260030995) — check postedOn before treating as fresh.
2. **LinkedIn guest re-fetch stayed unavailable** (Chrome profile locked; direct LinkedIn 301/403; ddgs cannot extract URLs). Web-search snippets give "1 day ago" freshness but not liveness — do not merge unverified leads; re-fetch via LinkedIn guest next run before merging the Cloud Resourcing / Brainhunter / ThoughtStorm / iPartner leads.
3. **Late-2026 hourly supply stays near zero** — 0 fresh merged hours are normal; don't re-run the merge "just to have a commit".

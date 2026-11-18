# JOBLESSONS_2026-11-17T2000EST

Hourly BESTIEJOB scan for Toronto ServiceNow / Salesforce jobs, run 2026-11-17 20:00 EST.

## Result

1 verified fresh job merged to the board (README.md row only — jobs.json/public already contained it via the scheduled Actions scan at 2026-11-18T00:32Z):

| Posted | Role | Company | Location | Source | Note |
|---|---|---|---|---|---|
| 2026-11-17 | Student Intern, Salesforce Developer 1 | Celestica | Toronto, Ontario, Canada | LinkedIn guest | Hybrid, 16-month internship, Req ID 141238, posted "1 hour ago" at verification time. Verified live via LinkedIn guest detail page (innerText). Entry-level Platform Developer I-adjacent — matches the user's Platform Admin/Dev I + entry-level focus. URL: https://ca.linkedin.com/jobs/view/student-intern-salesforce-developer-1-at-celestica-4491444461 |

Live page verified: https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json serves the Celestica row (jobs-data 5997 rows).

## What was checked and excluded

- **ServiceNow — Staff Cloud Security Engineer – Financial Services, Office of the CISO, ServiceNow Inc., Toronto** (LinkedIn, posted "2 hours ago"). EXCLUDED: security engineering role at ServiceNow the company, no ServiceNow platform administration/development content. Per targeting rules, only platform roles (CMDB/ITOM/ITAM/CSM, CSA/CAD/CIS certs) or Salesforce Platform Administrator/Developer I count.
- **All other LinkedIn 24h hits** (60 ServiceNow + 60 Salesforce cards): every relevant title (BMO ServiceNow CMDB Administrator 4490380189, Envision ServiceNow ITOM Developer 4491166743, W3Global ServiceNow Developer cum Architect 4488382344, TD Associate Software Engineer nCino/Salesforce 4491757623, White Bay Salesforce Administrator SFMC 4491195862, Nuvei Salesforce Business Process Analyst 4491413880, etc.) was already on the board — dedupe by normalized URL against jobs.json + README: 0 additional new rows.
- **Adzuna morning hits** (ServiceNow CMDB Administrator Bank N.A. 5968011526, Astra-North SPM Developer 5968012935, FSC leads/architects): all already on board.
- **Workday CXS** (known-good tenants: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site): only bmo.wd3 answered cleanly this hour; the rest returned HTTP 422 (burst rate limit — space calls ≥5s). Morning raw files (06:04 EST, raw/wd20261117/*) showed no "Posted Today" ServiceNow/Salesforce postings at any tenant; freshest were 2 days old (BMO Applications Support Analyst) / 5 days (ServiceNow CMDB Administrator, ServiceNow Technology Lifecycle Analyst).
- **Rogers**: date-sortable Phenom page (jobs.rogers.com/search/?sortColumn=referencedate&sortDirection=desc) — checked weekly, not hourly (board lesson); not re-scraped this hour.

## Technical notes

- LinkedIn guest search page works in the browser (new_tab + wait_for_load, no login wall): ~60 cards/page with f_TPR=r86400. web_extract times out on LinkedIn; use the browser. The `js()` helper mangles `\` escapes (`\"` becomes `"` and breaks JS strings; `\/` triggers SyntaxWarning). Reliable pattern: write selector JS to a file with write_file, base64-encode it in the terminal, evaluate `js("eval(atob('BASE64'))")`. No top-level `await` — the harness runs code at module top level.
- Dedupe: normalize URLs by stripping query strings/tracking params (utm_*, refId, trackingId, position, pageNum, trk) before comparing against jobs.json + README. Compare against README too — it carries ~8k normalized URLs.
- Push conflict: remote advanced while I worked (Actions commits 6c21857 at 00:32Z and 742611b at 01:00Z; remote jobs.json already at 2858 rows including the Celestica row). Rebased onto origin/main; for generated files (jobs.json, public/*) upstream wins (`git checkout --ours`), then push only the README change. Never `git add -A` mid-rebase — it staged all untracked raw/reports/inbox files into the commit this run (recovered via `git reset --hard origin/main`).
- README.md tables are mangled one-line blocks inside `<details>`; sync_readme_to_jobs.mjs is a no-op. jobs.json is the system of record; build_site.py unions jobs.json + README rows. The scheduled scan owns jobs.json/public; manual edits should touch README only when jobs.json already has the row.
- Commit hygiene: all board commits use `[skip ci]`; lessons-only commits do not trigger pages.yml.

## Commit

`089ecb4 chore(jobs): add verified fresh Toronto Salesforce posting to README (2026-11-17T20:00EST) [skip ci]` — 1 file, README.md row appended to the Salesforce table (newest first).

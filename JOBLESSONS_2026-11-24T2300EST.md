# JOBLESSONS_2026-11-24T2300EST

Hourly BESTIEJOB cron scan, Toronto ServiceNow / Salesforce, run 2026-11-24 23:00 EST (2026-11-25T04:03Z scan start). Commit b6c93a65, then CI hourly scan committed cb3a6588 on top; both on main. GitHub Pages live feed verified at generatedAt 2026-11-25T04:13:12Z, 4,992 jobs.

## What the scan found

`node scripts/daily_job_scan.mjs` (no --no-readme, so it also rewrote the README `<!-- DAILY-SCAN -->` block):
- LinkedIn guest 232 cards (HTTP 429 twice, then success on retry — retry matters; test length/digest distinctness, not just status=200, since the authwall also returns 200).
- Adzuna CA API 189; SmartRecruiters ServiceNow 12; Greenhouse 12; Lever 1; Ashby 2; remote feeds 6.
- All Workday CXS boards returned HTTP 429 (past the :00Z window) and were skipped — the CI hourly pass carries Workday; don't re-probe Workday manually at this hour.

Result: fresh=454, merged=5,681 (servicenow 1,205 / salesforce 4,318). **36 net-new Canada-geo SN/SF rows by URL** added to jobs.json. Diff URL sets against the previous origin commit before reporting additions — most "fresh" rows are company+title twins or already boarded.

## Dedupe lessons this cycle

- Deduped by normalized URL against jobs.json + README.md + APPLIED.md. No new URLs collided with APPLIED.md.
- TCS Salesforce Developer Toronto (LinkedIn 4494376362), Konrad Salesforce Architect (Loyalty & Data 360) Toronto (4491325080), Altus Group Salesforce Platform Developer Toronto (4483476940), Alithya Analyste d'affaires Salesforce Montreal (4464669300) were README-only rows from earlier scans; they are now synchronized into jobs.json so they render as page cards.
- Adzuna id-recycling: Cognizant "Salesforce Tech Lead (Remote)" Toronto (Adzuna 5973912092) and Celestica "Student Intern, Salesforce Developer 1" Toronto (Adzuna 5971440660) are twins of rows already on the board (LinkedIn 4494074582 / Adzuna 5974890709; careers.celestica.com employer-direct). Not double-listed — dedupe by fuzzy company + title tokens, not URL alone.
- Render-time mirror collapse: the live page shows these roles by company+title even though the exact URL collapsed onto a mirror card (Konrad → konrad.com careers employer-direct; Altus → simplyhired.ca card; Celestica → careers.celestica.com). Verify roles reached the page by company+title in jobs-data.json, not by URL.

## Employer / partner checks this cycle (Toronto SN/SF)

- Rogers jobs.rogers.com date-sorted: 26 dated rows, no ServiceNow/Salesforce titles.
- Bell / Ateko (FX Innovation): no fresh platform reqs.
- Government of Canada Job Bank / Ontario gojobs: Radware-walled — do not retry hourly.
- ServiceNow Careers: Cloudflare bot wall.
- Cognizant careers search: JS shell, not enumerable.
- Salesforce-the-company Workday: Toronto rows are sales/AE/renewals only, no Platform Admin/Developer I.
- Accenture Workday: Toronto hits are CCaaS/AI, not SN/SF platform.
- Result: no other fresh live ServiceNow or Salesforce platform roles this hour. Entry-level Platform Administrator / Platform Developer I (Toronto) remain scarce — closest junior hit is the Celestica student intern (already boarded).

## Pipeline mechanics

- Build: `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe tools/build_site.py` (plain `python3` is the Windows Store stub and will not run the script). Then `scripts/sync_readme_counts.py` (silent no-op on this README — its headings are glued one-line blocks; expected).
- Push: `git` at /c/Program Files/Git/cmd/git works; remote `bestiejob.git` redirects to `BESTIEJOB.git`. `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB` works from this host for an immediate redeploy; the Deploy GitHub Pages workflow triggers on `public/**` pushes too.
- The CI hourly scan overwrites manual pushes: it committed cb3a6588 after my push. My README edit survived (CI runs `daily_job_scan.mjs --no-readme`). Always `git merge --ff-only origin/main` before editing; verify board totals after the scan completes before declaring the board updated.
- Live verification: `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` — confirmed generatedAt 2026-11-25T04:13:12Z, count 4,992, and all four freshest roles present (TCS, Konrad, Altus Group, Celestica).
- Do NOT add cron jobs from recurring-schedule language; this was an existing scheduled run.

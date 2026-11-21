# JOBLESSONS_2026-11-21T0600EST — hourly ServiceNow / Salesforce Canada scan

## Run summary (2026-11-21 06:00 EST / 11:00Z)

- `node scripts/daily_job_scan.mjs` ran against 9 public sources: SmartRecruiters (ServiceNow), Workday CXS (13 boards), Greenhouse/Lever/Ashby boards, LinkedIn guest search, RemoteOK/Jobicy/Remotive, Adzuna Canada API (29 queries).
- fresh=460 candidates, merged=5,631 rows in jobs.json (servicenow 1,202 / salesforce 4,296).
- Net-new URLs actually added to jobs.json vs origin/main: **2**. The other 458 fresh hits were duplicates/twins already on the board — `fresh=N` is not net new; always diff URL sets against `origin/main:jobs.json` before claiming additions.
- Site rebuilt: 5,060 jobs (servicenow 873 / salesforce 930 / other 3,257); README header count 5,531 -> 5,586 via `sync_readme_counts.py`.

## Verified additions this cycle

| Posted | Role | Company | Location | Source | URL |
|---|---|---|---|---|---|
| 2026-11-19 | Associate Software Engineer (nCino/Salesforce) | TD Bank | Toronto, Ontario | adzuna | https://www.adzuna.ca/details/5971441048 |
| 2026-11-12 | Sr Specialist – ServiceNow Developer | Parkland Corporation | Calgary, Alberta, Canada | linkedin | https://ca.linkedin.com/jobs/view/sr-specialist-%E2%80%93-servicenow-developer-at-parkland-corporation-4488573852 |

Neither URL appears in APPLIED.md. Both passed the freshness/direct-deep-link/platform-content filters.

## Source behavior this hour (lessons for future runs)

- **Workday CXS rate-limited:** HTTP 429 on all 13 boards x 2 queries at this hour. Not empty postings — the CI hourly pass carries Workday. A manual re-probe ~4+ minutes later with >=8 s spacing between tenants recovers (verified pattern on earlier runs). Do not conclude zero postings from 429s.
- **Adzuna 503s:** ~5 of 29 queries failed with HTTP 503 (rapid-call rate limit), yet the source still returned 176 matches. Space Adzuna calls >=3 s.
- **LinkedIn guest:** first attempt HTTP 429, retry returned 247 cards. Always retry once; detect the authwall by body length + digest distinctness, not status alone (healthy card HTML ~31 KB and differs per query).
- **Build order:** jobs.json must be written before `tools/build_site.py`; then `scripts/sync_readme_counts.py`; then commit jobs.json + README.md + public/* together — the live page serves only committed files.
- **Commit/push:** do not use [skip ci] on data commits so `pages.yml` auto-deploys on the public/ push. If push is rejected non-fast-forward (CI committed first): copy the lessons file aside, `git reset --hard origin/main`, re-run scan + build on the fresh base, recommit, push. Never hand-merge the six generated-file conflicts.

## Partner/target-company notes

- Rogers (`jobs.rogers.com` Phenom) and Scotiabank Phenom boards were not reliable this hour — rely on LinkedIn/Adzuna for Rogers rows; check Phenom boards weekly, not hourly.
- Bell (`jobs.bell.ca`) returns zero rows for servicenow/salesforce — re-check weekly, not hourly. Bell's real ServiceNow hiring surfaces under Ateko/FX Innovation on LinkedIn.
- Public-sector portals (gojobs.gov.on.ca, jobs.gc.ca) are Radware-walled; use Job Bank as proxy and trust only postings whose title names the platform.
- Salesforce's own Workday board (`salesforce.wd12/External_Career_Site`) posted nothing below 4 days and no Platform Admin/Dev I this cycle; fresh platform work came from banks (TD via Adzuna) and consultancies.

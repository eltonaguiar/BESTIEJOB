# JOBLESSONS_2026-11-25

Hourly Toronto ServiceNow / Salesforce job scan — 2026-11-25T00:00EST (ran 05:06Z). Cron run of the BESTIEJOB hourly scan.

Note on ordering: the CI hourly scan ran at 05:14:44Z (commit `7d954c27`, 5646 listings) and pushed `jobs.json` + `public/` before this run's data push, so the CI scan's build superseded this run's data push to origin/main. This lessons file documents this run's scan analysis on top of CI's build.

## Scan summary

`node scripts/daily_job_scan.mjs` (no flags; full pipeline, no Workday manual probe — see below)

- fresh=465, merged=5684 rows in jobs.json (SN 1206 / SF 4320)
- Sources: LinkedIn guest 241, Adzuna CA API 191, SmartRecruiters ServiceNow 12, Greenhouse 12, Remotive/Jobicy/RemoteOK 6, Ashby 2, Lever 1
- Workday CXS: all 14 boards × 2 queries returned HTTP 429 → 0 postings, skipped this hour. The CI :03:00EST / :08:00Z hourly pass carries Workday. Do not manual-probe at :00Z/:05Z — 429s persist; retry 3–4 tenants at ≥8 s spacing past the window if needed (verified pattern: 10-tenant probe at :06Z returned HTTP 200 on all calls).
- LinkedIn guest: first call HTTP 429, retry succeeded (241 cards). Fresh pass (`f_TPR=r86400`) stamps scan time as postedDate when `<time>` is absent — treat those dates as discovery dates, not posted dates.
- Liveness gate `tools/verify_links.py --days 2`: 50 rows probed, live=28, dead=0, unknown=22 (bot-wall/transport, kept). Nothing dropped.

## Dedupe vs board (jobs.json, README.md, APPLIED.md)

- 40 URLs new vs `origin/main:jobs.json`
- 29 of those URLs already present in README.md (earlier scans) — synchronized into jobs.json so they render as page cards; not double-listed
- 0 duplicates vs APPLIED.md
- Company+title twin check against the board: all 40 URL-new rows have an existing same-company+same-title twin on the board (Adzuna re-issues ids for the same ad — e.g. Cognizant "Salesforce Tech Lead (Remote)" adzuna 5973912092 is a twin of 5974890709; TD "Senior Solution Architect (ServiceNow)" 5970077372 twins Workday R_1521185; Deloitte DTC Platform twins on LinkedIn; Celestica student intern twins the careers.celestica.com row). Per board policy these are NOT re-added as new roles — the role stays represented under its original URL, `build_site.py` collapses company+title mirrors into one card.
- 1 URL-new row without a board twin: Instacart "Senior Salesforce Developer", LinkedIn 4494476452, location "Canada", postedDate = scan time (card-level only, body not confirmed). Kept as an unverified lead; not a Toronto-verified platform role. Body-check via browser before counting it.
- Net new verified roles this cycle: 0. Entry-level Platform Administrator / Platform Developer I (Toronto): none surfaced — mid/senior/lead and program-BA roles only. Junior scarcity persists.

## What was merged (by this run's scan; superseded at push time by CI's 05:14Z build)

- jobs.json + public copies + FRESH_JOBS.md rewritten; README `<!-- DAILY-SCAN -->` block refreshed (Scan: 2026-11-25T05:06:41.334Z · 4519 live postings from 7 public sources · 164 dated 2026-11-01)
- `tools/build_site.py`: public/jobs-data.json + public/index.html rebuilt — 4993 jobs (SN 868, SF 965, other 3160), 568 duplicate mirrors collapsed, 28 applied rows hidden, built 2026-11-25 05:09 UTC
- `scripts/sync_readme_counts.py`: no standalone header count claim remains (DAILY-SCAN block carries the count now) — "nothing rewritten" is the expected by-design result; exit 0
- `scripts/check_readme_sort.mjs`: 23 ordering problems, ALL in pre-existing "Verified fresh additions — cron/hourly scan ..." mangled sections (`||||| Posted | ... ||` 7-column tables). None in the new DAILY-SCAN block. Pre-existing debt, left untouched per policy

## Employer-direct / partner checks this cycle

- Rogers: Phenom board not server-rendering job rows (prior date-sorted checks: 26 dated rows, no SN/SF titles on 11-24; zero-row shell on 11-20). No fresh Rogers ServiceNow/Salesforce postings in this cycle's LinkedIn guest or Adzuna results; rely on mirrors rather than retrying jobs.rogers.com hourly.
- Bell: jobs.bell.ca renders an empty shell / (0) — zero reqs, not a scrape failure. Bell's real ServiceNow hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn; Ateko careers page (ateko.com/en/careers/) lists ServiceNow/Salesforce/Cloud Data & AI teams. No fresh Ateko platform reqs in this cycle's cards (sampled older ids 4360496360 / 4413567740 only).
- Government of Canada Job Bank / Ontario gojobs.gov.on.ca: Radware-walled; do not retry. Job Bank body search is noise ("shipping coordinator", "agronomy" matches) — trust only postings whose TITLE names the platform; even title hits need a body check (partner/sales titles naming the product are not build/admin work).
- ServiceNow Careers: Cloudflare bot wall. Cognizant careers: JS shell search. Salesforce-the-company Workday: Toronto rows are sales/AE/renewals only. Accenture Workday: 1,600+ SN reqs globally, effectively none Canadian in first pages; Toronto hits are CCaaS/AI, not platform.

## Next verification

- Push this lessons commit on top of CI's build, trigger `pages.yml`, then curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json and confirm the live build stamp is 2026-11-25 05:14 UTC (CI build) and fresh URLs render (verify by company+title, not URL — twins collapse at render).

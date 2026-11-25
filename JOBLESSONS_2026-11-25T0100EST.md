# JOBLESSONS_2026-11-25T0100EST

Hourly Toronto ServiceNow / Salesforce targeted scan — 2026-11-25 01:00 EST (06:00 UTC). Cron run of the BESTIEJOB hourly scan, supplementary to the CI hourly scan that ran at 05:14:44Z (commit `7d954c27`, 5646 listings) and already pushed `jobs.json` + `public/`.

Board: github.com/eltonaguiar/bestiejob (main). GitHub Pages: eltonaguiar.github.io/BESTIEJOB/

## Result

Net new verified fresh Toronto ServiceNow / Salesforce platform roles this cycle: **0**.
`jobs.json` and `README.md` unchanged — nothing to merge. Zero roles added, zero roles removed, zero duplicates created.

## Scan summary

Targeted employer-direct + public-API scan (the CI hourly pass already covered LinkedIn guest 253 cards, Adzuna CA API 191, SmartRecruiters ServiceNow 12, Greenhouse 12, Lever 1, Ashby 2, Remotive 6, Workday 17):

- **Workday CXS** (curl `--compressed`, reachable from this host, no 429 this hour):
  - BMO `bmo.wd3/External` ServiceNow: 4 postings, all 9–19 days old (incl. `ServiceNow CMDB Administrator` R260030992, 12 days — already boarded).
  - BMO `bmo.wd3/External` Salesforce: 22 postings; "Posted Today" rows are `Senior Sales Force Developer` R260032445 (Toronto, already boarded via LinkedIn twin) and `Senior Salesforce Developer` R260032496 (Chicago — out of GTA scope).
  - TD `td.wd3/TD_Bank_Careers` ServiceNow: freshest is `Senior Solution Architect (ServiceNow)` R_1521185, 8 days old — already boarded.
  - TD `td.wd3/TD_Bank_Careers` Salesforce: `Software Engineer II (Salesforce Loyalty Management Developer)` R_1509038, Posted Today — already present in `jobs.json` (onboard).
  - Interac `interac.wd3/interac` ServiceNow/Salesforce: nothing fresh (30+ days old or CRM/sales-enablement, not platform).
  - Workday lesson re-confirmed: `postedOn: "Posted Today"` is not a new-posting signal — always diff against the board row's `postedDate` before treating a date bump as new.
- **Adzuna CA API** (`app_id=54ce986e`, `max_days_old=3`, `where=Toronto`): ServiceNow query returned a Deloitte "SAP Basis Consultant" (false positive — SAP, not ServiceNow); Salesforce query returned "Margin Analyst" (Univar, accounting) and "Account Executive" (Rogers, sales) — both non-platform. Adzuna `servicenow`/`salesforce` keyword queries remain false-positive magnets (sales, gamedev, non-platform tooling); title+body check required before adding.
- **Rogers** `jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc`: zero server-side ServiceNow/Salesforce/platform rows this hour. (Prior date-sorted checks found 26 dated rows but no SN/SF titles.) Deprioritize to every-other-cycle.
- **Salesforce-the-company Workday** `salesforce.wd12/External_Career_Site`: 1610 postings, global; page 1 is all non-Canada (India/Taiwan/Australia). Toronto fresh hits are sales/AE/renewals only — no Platform Admin/Developer I. Append city to `searchText` if re-probing.
- **Web search** (Indeed/Glassdoor/LinkedIn Canada): all candidates surfaced (Jolera Senior ServiceNow Consultant 11-24, ServiceNow Staff/Senior SRE Canada Protected B Toronto 11-05) verified already onboard.

## Dedupe vs board (jobs.json + README.md + APPLIED.md)

- jobs.json URLs: 5,646; README URLs: 1,486; APPLIED URLs: 7; **union: 5,992 board URLs** (normalized: query strings stripped, trailing slashes removed).
- Every candidate URL checked (Jolera LinkedIn 4494431156, ServiceNow SRE JB0076847/JB0076846, BMO CMDB Admin R260030992, TD Salesforce R_1509038): **ONBOARD** — all already present in jobs.json and/or README.
- 0 duplicates vs APPLIED.md.
- Company+title twin check: all URL-new candidates (none) would be checked for twins before adding; none found this cycle.

## Employer-direct / partner checks this cycle

- Rogers (Phenom): no server-side SN/SF platform rows; rely on LinkedIn/Adzuna mirrors rather than retrying `jobs.rogers.com` hourly.
- Bell: `jobs.bell.ca` empty shell / (0) — zero reqs, not a scrape failure. Bell's real ServiceNow hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn; no fresh Ateko platform reqs this cycle.
- ServiceNow Careers: Cloudflare bot wall (not scrapeable). Cognizant careers: JS shell search. Salesforce-the-company Workday: sales/AE/renewals only in Toronto. Accenture Workday: 1,600+ SN reqs globally, effectively none Canadian in first pages.
- Government of Canada Job Bank / Ontario gojobs: Radware-walled; do not retry. Job Bank body search is noise — trust only postings whose TITLE names the platform, then body-check for admin/build context.

## Source lessons for future agents

1. **Workday CXS is reachable from this host via bash `curl --compressed`** (no `Referer` header, `Content-Type`/`Accept`/`Origin` only). Do NOT drive curl from Python `subprocess` (WinError 5). Avoid probing at the :00Z window (CI hourly run causes HTTP 429); retry 3–4 tenants at ≥8 s spacing past the window.
2. **Workday `"Posted Today"` is a date bump, not a new posting** — always cross-check against the board row's `postedDate` and `alternates` before adding (BMO R260032445/R260032496 and Manulife JR26101237 all read "Today" while already boarded).
3. **Adzuna `servicenow`/`salesforce` keyword queries are false-positive magnets** — reject `sales executive|solution sales|account executive` and non-platform tooling (SAP Basis, BMC Helix, ticketing-tool users) before treating a hit as a platform role. Use the detail page's JSON-LD (`datePosted`), not the API `created` date.
4. **Rogers' Phenom date-sorted route is intermittent** — sometimes 26 dated rows, sometimes a zero-row marketing shell. "Zero rows" is not "zero jobs"; re-check weekly, not hourly.
5. **Salesforce-the-company Workday is a global board; page 1 is relevance-sorted and non-Canada** — append the city to `searchText` or expect only sales/AE/renewals Toronto hits.
6. **0-net-new hours are real** after several board refreshes in a day — always diff candidate URLs/IDs against the 5,992-URL board union before any body check.
7. **Entry-level Platform Administrator / Platform Developer I (Toronto) remain scarce** — this cycle yielded only mid/senior/lead and program-BA roles; no junior platform roles surfaced. Keep the weekly partner/Elite-partner pass (Deloitte, Cognizant, CGI, Wipro).

## Next verification

- Live page is current via CI's 05:14Z build; confirm with `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` (build stamp ~2026-11-25 05:14 UTC) and grep a fresh SN/SF company+title (verify by company+title, not URL — twins collapse at render).
- No `pages.yml` trigger needed this cycle since `jobs.json`/`README.md`/`public/` did not change.

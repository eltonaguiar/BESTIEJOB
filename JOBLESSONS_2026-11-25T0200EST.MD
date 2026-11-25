# JOBLESSONS_2026-11-25T0200EST — hourly Toronto ServiceNow / Salesforce scan

## Scope
Hourly cron scan for fresh Toronto/GTA ServiceNow and Salesforce Platform Administrator / Platform Developer I roles, deduped against jobs.json + README.md + APPLIED.md, with employer-direct partner/Elite-Partner/sponsor checks (Rogers, Bell/Ateko, Government of Canada Job Bank / Ontario gojobs, bank Workday boards).

## Result: 0 net-new fresh platform roles this cycle

No verified fresh ServiceNow or Salesforce platform build/admin roles were added to jobs.json, README.md, or the live page. Entry-level Platform Administrator / Platform Developer I (Toronto) remain scarce this hour — only mid/senior/lead and sales/partner-adjacent reqs surfaced.

## Sources checked

| Source | Query / target | Fresh platform hits | Disposition |
|---|---|---|---|
| Adzuna CA API | servicenow, salesforce, platform administrator — Toronto, max_days_old=2 | 0 | All noise (SAP Basis, cyber risk, margin analyst, LMS specialist, IT sysadmin). `content-type=application/json` param required; space calls ≥3s to avoid 503. |
| Workday CXS | bmo/External, td/TD_Bank_Careers, cibc/search, manulife/MFCJH_Jobs, interac/interac, salesforce/External_Career_Site, accenture/AccentureCareers × {ServiceNow, Salesforce (+Toronto for global boards)} | 0 net-new | Requires `User-Agent` header or returns HTTP 422; use `--compressed`. Fresh hits excluded: TD `Software Engineer II (Salesforce Loyalty Management Developer)` R_1509038 = already in jobs.json (scraped 05:12Z); Manulife `Salesforce Functional Analyst` JR26101237 = date-bump of existing 2026-11-02 row (skip per board policy); BMO `Senior Sales Force Developer` R260032445 = sales role, not Salesforce platform. All other hits 4–30+ days old, non-platform (CCaaS/SAP/sales), or non-Toronto. |
| Rogers jobs.rogers.com | date-sorted `sortColumn=referencedate&sortDirection=desc` | 0 | 26 dated rows, 0 ServiceNow/Salesforce/platform titles. Recovered from earlier zero-row shell; run each cycle but expect none. |
| LinkedIn guest (browser) | keywords ServiceNow / Salesforce, Toronto, f_TPR=r86400 | 0 (walled) | Search cards wall/rate-limit on repeat calls (0 cards on retry after ServiceNow returned empty once and Salesforce cards on first pass). Detail pages behind authwall — never infer platform content from card title alone. Do not add unverified. |
| Bell / Ateko | — | 0 | No fresh platform reqs (re-check weekly, not hourly). |
| Gov't Job Bank / Ontario gojobs / ServiceNow Careers / Salesforce Careers | — | 0 | Radware-walled / Cloudflare bot wall / no Platform Admin/Dev I below 4 days. |

## Fresh Workday hits excluded (for future reference)

- `td.wd3/TD_Bank_Careers` `Software Engineer II (Salesforce Loyalty Management Developer)` Toronto, Posted Today, R_1509038 — already boarded (first row of jobs.json, scrapedAt 2026-11-25T05:12Z). Duplicate.
- `manulife.wd3/MFCJH_Jobs` `Salesforce Functional Analyst` Waterloo, Posted Today, JR26101237 — already boarded with postedDate 2026-11-02; this is a Workday `startDate` bump, not a new posting. Skip.
- `bmo.wd3/External` `Senior Sales Force Developer` Toronto, Posted Today, R260032445 — sales ("Sales Force") role, not Salesforce platform build/admin. Exclude.
- `cibc.wd3/search` `Sr. Consultant, Infrastructure Management` Toronto, Posted Today, 2623517 — not SN/SF platform. Exclude.

## Recurring patterns (lessons for future scans)

1. **Workday CXS 429s at :00Z** when the CI hourly scan runs concurrently (03:00 EST / 08:00Z). A manual probe at that minute gets HTTP 429 on BMO/TD/CIBC/Manulife/Interac/Salesforce/Accenture. Probe 3–4 tenants at ≥8s spacing outside the :00Z window, or leave Workday to the CI pass. A `User-Agent` header + `--compressed` are mandatory (422 without UA).
2. **Adzuna demo keys** `app_id=54ce986e` / `app_key=db851f299e966c0a2a72af525dce6199` must be passed explicitly; 503s after ~4 rapid queries — space calls ≥3s.
3. **"Sales Force" (two words) ≠ Salesforce platform.** BMO's "Senior Sales Force Developer" reqs are sales roles; do not board.
4. **Workday "Posted Today" is not a Canada or freshness signal.** Salesforce.com and Sunlife post non-Canada reqs "Posted Today"; always read the location slug before counting a hit.
5. **LinkedIn guest search is intermittently walled.** ServiceNow returns 0 cards while Salesforce returns results on the same page — retry once after a few minutes. Detail pages serve the authwall; body-check via browser `.jobs-description` when accessible, else skip.
6. **Rogers date-sorted page** is the reliable Rogers check (keyword search returns sales roles that merely mention the platforms). Expect no SN/SF titles; re-check per cycle, not hourly.
7. **Entry-level Platform Administrator / Platform Developer I (Toronto) remain scarce.** The closest junior signal this cycle (Celestica student intern) is already boarded via its careers-page twin; no fresh Platform Admin/Dev I roles surfaced from any oracle.

## Board state
jobs.json: 5,646 rows (1,208 ServiceNow / 4,321 Salesforce) per CI scan 2026-11-25T05:14Z. No changes this cycle — nothing to merge into readme.md or public/, no pages deploy triggered. Commit is `[skip ci]` (lessons only).

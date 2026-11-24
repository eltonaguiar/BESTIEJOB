# JOBLESSONS_2026-11-24T0500EST — hourly scan 2026-11-24 05:00 EST (10:00Z)

## Result

**0 net-new verified fresh Toronto ServiceNow / Salesforce platform jobs this cycle.** Cross-checked the live page (`https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json`, deployed from origin/main == local main): all 12 SN/SF roles posted 2026-11-24 are already represented on the board — Indeed/Tri-global/Compugen/CGI/Deloitte mirrors as README rows, Konrad/CoreKloud/Adzuna in jobs.json. No changes to jobs.json, README.md, or public/ — lessons-only commit, `[skip ci]`, no Pages redeploy required.

Today's live SN/SF posts already on the board:
- ServiceNow: Lead Specialist CMDB Solution Architect (Deloitte, jk=8481424a81ab3122), ServiceNow Business Analyst - Contract (Compugen, jk=51dd9612200e90ef), Project Manager – ServiceNow & Financial Systems (Compugen, jk=653bb0c2cc9bc020), ServiceNow Administrator/Developer (CGI, jk=cf4ffdcf78006e60), Senior Consultant ServiceNow Platform (Deloitte, jk=159ae9b051d0cc56), ServiceNow Project Manager (Tri-global, jk=83990275ef12d929)
- Salesforce: Salesforce Architect Loyalty & Data 360 (Konrad), Salesforce Developer FSC (CoreKloud), Senior Consultant Salesforce Platform (Deloitte, jk=ed77066feb39f0cc), Analyste d'affaires Salesforce (Alithya, Montreal), Salesforce Developer (Harbor, Remote Canada)

## What was checked and rejected

- **Adzuna CA API** (`app_id=54ce986e`, `what=ServiceNow|Salesforce`, `where=Toronto|Ontario`, `max_days_old=3`, `sort_by=date`) — freshest hits dated 2026-11-22: Deloitte Technical Delivery Mgr ServiceNow IRM/Sec Ops (remote, not Toronto platform), ServiceNow Inc Cyber Advisory Solution Consultant / Sr Mgr Sales Cyber (sales), Novartis SFMC Manager (band 4 manager), Flexstaf Revenue Cloud Architect. Nothing posted 2026-11-24, nothing Platform Administrator / Platform Developer I.
- **SmartRecruiters ServiceNow public API** (`/v1/companies/servicenow/postings?limit=100`, totalFound=997) — page 1: sole Canada role is "Solution Sales Executive - Moveworks" (Toronto, released 2026-11-20) — sales, not platform build. Consistent with market shape: ServiceNow-the-company Toronto = sales/SRE/security, not platform Admin/Dev.
- **Scotiabank Phenom** (`jobs.scotiabank.com/search/?q=servicenow` and `q=salesforce`, date-sorted) — Toronto rows returned (Incident Management, Employee Technology, InfoSec, CIAM, Identity Lifecycle, Technology Risk) but zero SN/SF platform roles; one "ServiceNow Developer" in Bogota, Colombia — out of scope.
- **LinkedIn guest search** (Toronto, `f_TPR=r86400`) — signup wall (~61 KB "Sign Up" page) from this host this cycle; search cards unreadable. Guest API path blocked without an established session.
- **Indeed ca.indeed.com** — CloudFront 403 / blocked from this host; SERPs and detail pages unfetchable; web_search snippets carry no posting dates, so freshness cannot be established and nothing was added from snippets alone.
- **Workday CXS** (TD/BMO/CIBC/Manulife/Interac/Accenture/Salesforce) — 05:00 EST = 10:00Z is the CI hourly scan window; Workday returns HTTP 429 at :00Z and 429s persist past it. Left Workday to the CI pass.
- **Employer-direct partners**: Rogers `jobs.rogers.com` (Phenom shell, zero server-side rows — weekly, not hourly); Bell `jobs.bell.ca` (empty shell, 0 reqs — weekly); Government of Canada direct portals (Radware-walled); Job Bank keyword search (boilerplate noise — trust only titles naming the platform).

## Duplicate check

All live-today candidates deduped by URL (query strings stripped) against jobs.json (5,635 rows), README.md tables, and APPLIED.md. Every candidate was already on the board by URL or mirror — no net-new rows.

## Patterns / lessons for future scans

1. **Live-page cross-check is a fast completeness oracle:** query `jobs-data.json` for `family` = servicenow/salesforce with `posted` = today; if every role appears in README/jobs.json by URL or alternate mirror, close the hour with 0 net-new — never force rows to look productive.
2. **Adzuna `what=ServiceNow` matches GRC/cyber/risk consulting that names the platform as tooling** — reject unless the body shows admin/config/build context. Its `max_days_old=3` bucket still serves Nov 22 hits at off-peak hours; Adzuna freshness lags real-time freshness.
3. **LinkedIn guest search can serve a signup wall mid-session** even when it worked in prior cycles — treat as a temporary wall, retry after ~4–25 min; never treat the wall as zero results or as a real 404.
4. **Phenom boards (Scotiabank/Rogers) are browser-enumerable but keyword-noisy** — filter by title, trust absolute posted dates, never relative labels ("3 days ago").
5. **SmartRecruiters ServiceNow page 1 is relevance-sorted (997 total)** — the only Canada role was a sales req. Fresh Canada platform reqs need deeper paging or a date sort.
6. **05:00 EST / 10:00Z coincides with the CI hourly scan** — Workday probes get 429; leave Workday to CI and verify its ~10:15Z commit landed before the next manual push.
7. **0 net-new hours are normal.** A lessons-only `[skip ci]` commit leaves the deployed page unchanged and correct when jobs.json/README/public are untouched.

## Files touched

- `JOBLESSONS_2026-11-24T0500EST.md` only (docs; `[skip ci]`)

# JOBLESSONS_2026-11-23T1100EST — Hourly BESTIEJOB scan (11:00 EST / 16:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,610 after sync) + README.md + APPLIED.md. This run's own web/ATS scan found **0 net-new platform roles**. The 15:44Z CI fresh-CA sweep had already added four rows, two of which were appended inline on the `### ... jobs (N)` header lines and therefore never parsed into the feed or page. I split those two rows onto their own lines (AceStack Technical Lead – Senior ServiceNow, Vancouver; GLOBAL CONSULTING COMPANY Techno-Functional BA – Salesforce & AI, Toronto), synced, rebuilt the page, and pushed.

## Scan sources
| Source | Query / target | Result |
|--------|----------------|--------|
| LinkedIn guest search | ServiceNow + Salesforce, Toronto, past 24h / past 7d, date-sorted | Works without login (~60 cards/search). Every relevant SN/SF platform role was already on board: Deloitte ITOM/Now Assist/Salesforce Platform, INNOVA Salesforce Specialist, Altus, Benevity, Scotiabank, Konrad, PwC, OSI Digital, CGI, HCLTech, Konrad, SickKids, CanPrev, Acronym, RBC, TD, BMO, EY, Pacer, Blue Mantis, Apptoza, Compugen, SPECTRAFORCE. |
| jobs.ca | ServiceNow / Salesforce Toronto, employer pages | G-Force "Information Technology Service Management Consultant" was a mirror of LinkedIn 4490140539 already on board (Nov 16) — reverted. Intelli-CloudWare SA/BA removed ("no longer available"). Infoya Sep 2, Zodiac Oct 16 (closed), Astek Oct 16 (closed), Canadian Cancer Society Oct 11 (closed) — all outside window. Avanciers Nov 20, Citco Nov 17, Realtek Nov 18, White Bay Nov 18 already on board. |
| Indeed / Workopolis / Glassdoor / gojobs | Toronto SN/SF | Cloudflare/CAPTCHA blocked from this host. Do not spend calls. |
| Lever / Greenhouse / Ashby APIs | Alimentiv, EQ Bank, Versapay, Electric Mind, Levio, Solink, CAE, Konrad, CloudKettle, OSI Digital | Alimentiv, Versapay, Electric Mind, Levio hits all already on board; Konrad/CloudKettle/OSI tokens 404; no fresh Toronto SN/SF. |
| ServiceNow careers / JobsByCountry | 22 Toronto roles | All sales, security, SRE, product, or generic engineering; Principal Solution Architect Oct 29 already on board. Excluded by board rules. |
| Rogers careers | servicenow / salesforce | 0 ServiceNow positions; 18 "Salesforce" hits are all sales/ops (Lead Management Ops, Delivery Specialist, Client Relationship, Field Sales). Nothing platform. |
| Bell careers | servicenow / salesforce | Search page is JS-gated (no server-rendered rows). LinkedIn Bell "ServiceNow Developer / Integrator" 4471150580 is not on board but its application deadline is 10/07/2026 — treat as expired. |
| Government | Job Bank, OPS, City of Toronto, EDC, Wirehead, CAS | Source Code RQ00757 (ServiceNow SPM, Nov 8) and OPS RQ11686 (ServiceNow Senior Developer, Nov 3) already on board. City of Toronto Salesforce/ServiceNow expired. EDC ServiceNow CSM expired Sep 16. Wirehead Salesforce Developers x2 posted 83 days ago. Courts Administration Service (Ottawa) is internal-GoC only. |
| Partners / sponsors | Deloitte, EY, KPMG, Accenture, CGI, IBM, Coforge, RSM, Cognizant, Konrad, Paralucent, BDO, Acronym, Rexall | All current Toronto/GTA postings already on board. |

## Dedupe result
- **G-Force IT Services Inc** jobs.ca row → duplicate of LinkedIn 4490140539 (posted 2026-11-16, "Information Technology Service Management Consultant"). Reverted before commit. This is the key near-miss of the hour.
- **Highspring "(DEV) Saleforces Developer"** (Nov 23) → actually a Salesforce Marketing Cloud landing-page developer; duplicates Highspring Salesforce Developer (Nov 19).
- **Smart IT Frame LLC "Salesforce Data 360 Consultant"** (Nov 23) → duplicate of Salesforce Data Cloud Consultant (Nov 5); CI added it anyway.
- **Deloitte "Senior Consultant, Salesforce Platform"** (Nov 23 repost) → same title already on board via Adzuna Nov 11.
- **Net new from this run's own scan: 0.** After fixing the two inline CI rows, the board gained **2 parseable rows** (AceStack Vancouver Technical Lead; GLOBAL CONSULTING Toronto Salesforce BA).

## Board state after run
- jobs.json: 5,610 (was 5,608 at pull).
- public/jobs-data.json: 4,948 (live page was 4,945; deploy pending).
- ServiceNow table header 566 (565 parseable rows); Salesforce header 899 (896 parseable rows). The 1/3 header drift pre-dates this run and is not gated.
- `python scripts/board_invariants.py`: **PASS** (errors=2 warnings=108; no kind grew against baseline).

## Lessons for future agents
1. **LinkedIn guest search is the best fresh source from this host.** `ca.linkedin.com/jobs/search?keywords=...&location=Toronto%2C%20Ontario%2C%20Canada&f_TPR=r86400&sortBy=DD` renders ~60 cards without login. Extract `a[href*="/jobs/view/"]` plus the card text; Indeed, Workopolis, Glassdoor and gojobs are Cloudflare/CAPTCHA-blocked.
2. **Dedupe by LinkedIn numeric ID AND normalized company + title before adding.** A ServiceNow developer role can be titled "Information Technology Service Management Consultant" (G-Force) with no "ServiceNow" in the title. A title-only regex for "ServiceNow" misses it and produces a duplicate mirror.
3. **jobs.ca is a mirror farm with good metadata.** It shows reliable posted dates and status ("This posting is no longer available" = removed; "Applications are currently unavailable" = closed), but most rows mirror LinkedIn/Adzuna. Always check the LinkedIn ID and company+title against jobs.json before adding.
4. **CI fresh-ca-scan sometimes appends rows inline on the `### ... jobs (N)` header line.** Both `sync_readme_to_jobs.mjs` and `tools/build_site.py` skip inline rows. Symptom: a row appears added in the diff but is absent from jobs.json/jobs-data.json. Fix: move each inline row to its own line, then re-run `node scripts/sync_readme_to_jobs.mjs` and `python tools/build_site.py`.
5. **ServiceNow's own Toronto roles are sales/security/SRE/product**, excluded by the board. Rogers has 0 ServiceNow and only sales/ops "Salesforce" hits. Bell's search page is JS-gated; its LinkedIn SN role is past its application deadline.
6. **Government leads:** OPS RQ11686 (ServiceNow Senior Developer, $95–103/hr) and RQ00757 (ServiceNow SPM) are on board; City of Toronto Salesforce/ServiceNow expired; EDC ServiceNow CSM expired Sep 16; Wirehead's government Salesforce contract is 83 days old. Courts Administration Service (Ottawa) is internal-GoC only.
7. **Respect the 31-day freshness window.** Wirehead (83 days), Randstad Senior Salesforce Development Specialist (Aug 13), Infoya (Sep 2), Salvation Army (Aug) are live but outside the window; do not add them.

## Leads for next run
- **S M Software Solutions RQ10997 Software Developer – CRM – Intermediate** (LinkedIn 4493659215, ~2h old) — login-walled; verify whether it is Salesforce/ServiceNow before adding.
- **Bell ServiceNow Developer / Integrator** (LinkedIn 4471150580) — application deadline 10/07/2026; confirm if relisted.
- **TalentZone / GLOBAL CONSULTING COMPANY Salesforce BA** — now parsed and on board; watch for a direct-employer version.

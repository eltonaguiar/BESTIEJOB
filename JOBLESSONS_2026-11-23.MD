# JOBLESSONS_2026-11-23 — hourly Toronto ServiceNow / Salesforce scan (BESTIEJOB cron)

## What ran (2026-11-23 00:00 EST)
Hourly scan for fresh Toronto ServiceNow/Salesforce postings, deduped against jobs.json + README + APPLIED.md, merged into jobs.json/README, site rebuilt via tools/build_site.py, deployed to GitHub Pages.

## Fresh additions (2 verified)
| Role | Company | Location | Source | Posted |
|------|---------|----------|--------|--------|
| Technical Delivery Mgr, ServiceNow IRM/Sec Ops, Deloitte Global Technology | Deloitte | Toronto, Ontario | adzuna.ca/details/5975652935 | 2026-11-22 |
| SFMC Manager | Novartis AG | Toronto, Ontario | adzuna.ca/details/5975287815 | 2026-11-22 |

Both dated 2026-11-22 via the live Adzuna CA API; inserted at head of jobs.json (servicenow 1193→1194, salesforce 4284→4285, total 5634→5636).

## Sources checked this hour
- **Adzuna CA API** (app_id=54ce986e/app_key=db851f299e966c0a2a72af525dce6199, `what=servicenow|salesforce`, `max_days_old=3`, `sort_by=date`, `where=Toronto|Ontario`, `content-type=application/json`): 4 queries, 2 fresh rows after dedupe. Detail pages (www.adzuna.ca/details/<id>) return CloudFront **403** from this host — treat as bot-wall on a live posting, never as dead; rely on API `created` + title + redirect_url.
- **LinkedIn guest search** (ca.linkedin.com/jobs/search, keywords ServiceNow / Salesforce, location Toronto, f_TPR=r86400, sortBy=R): 4 + 4 cards, all already on the board (04:06Z CI sweep had them). Cards readable without login via `li a[href*="/jobs/view/"]` + `li.innerText` (title/company/location/posted).
- **Workday CXS** (POST /wday/cxs/{tenant}/{site}/jobs, `--compressed`, Content-Type/Accept/Origin only): bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs all returned **HTTP 422** — previously "verified" tenants have rotted; don't retry hourly, re-discover site slugs via careers pages/search engines.
- **Web search** for partner/employer-direct leads: Ateko (Bell-backed) ServiceNow Platform Administrator 4475476505 → LinkedIn 404 (expired); Canada Life Platform Administrator 4490436505 → posted 5 days ago (2026-11-08), no servicenow/salesforce in body (not a platform role); US Tech Solutions ServiceNow System Administrator 4478298486 → LinkedIn 404 (expired). 2iSolutions ITOM Consultant 4486429594 already on board.

## Patterns / lessons
- Adzuna API remains the fast hourly freshness oracle; Job Bank/Eluta sweeps are slow (>300s) and only needed for specific coverage gaps.
- LinkedIn job-id (trailing numeric id) is the hard dedupe signal — titles can be renamed for reposts (e.g. ...-5816 twins).
- Direct detail links from search engines age fast: verify liveness (HTTP/status + body platform check) before adding; 404/expired reqs are dropped, not parked.
- ServiceNow-the-company posts only sales/SRE/security in Toronto; Salesforce-the-company posts nothing below 4 days / no Platform Admin/Dev I. Fresh platform work comes from banks (BMO/TD/CIBC/Manulife Workday) and GRC/IRM consultancies (PwC, Deloitte, EY).
- Bell's own jobs.bell.ca shows zero SN/SF reqs; Bell's real ServiceNow hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn.
- Rogers Phenom board (jobs.rogers.com) returns a zero-row shell; rely on LinkedIn/Adzuna for Rogers rows.
- Public-sector portals (jobs.gc.ca, gojobs.gov.on.ca) are Radware-walled; Job Bank is the proxy — trust only title-named platform postings.
- Dedupe: normalize URLs (strip query strings/trailing slashes) against jobs.json + README + APPLIED.md; also check company+title twins (Adzuna re-issues same role under new ids).
- Salary rows use object schema {min, max, currency: "CAD", display}; never strings.

## Negative space (searched, nothing fresh)
- LinkedIn Salesforce "Platform Administrator"/"Platform Developer I" Toronto: no fresh postings (market note: no Platform Dev I roles this hour).
- Workday Canadian tenants: all 422 — no employer-direct bank reqs surfaced this hour.
- Job Bank site:search returned no usable title-named platform postings.

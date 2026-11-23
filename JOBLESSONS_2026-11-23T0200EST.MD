# JOBLESSONS_2026-11-23T0200EST — hourly Toronto ServiceNow / Salesforce scan (BESTIEJOB cron)

## What ran (2026-11-23 02:00 EST / 07:00Z)
Hourly scan for fresh Toronto ServiceNow/Salesforce postings via `node scripts/daily_job_scan.mjs` (no `--no-readme`): SmartRecruiters ServiceNow board, Workday CXS (Salesforce + Canadian employers), Greenhouse/Lever/Ashby public board APIs, LinkedIn guest search (ServiceNow/Salesforce × Toronto/Canada, f_TPR=r86400), remote feeds (RemoteOK/Jobicy/Remotive), Adzuna CA API. Dedupe against jobs.json + README.md + APPLIED.md (normalized URLs: strip query strings/trailing slashes; trailing LinkedIn job id; company+title fuzzy twins).

## Result: 0 net-new verified jobs this hour
- fresh=374 postings surfaced; merged=5,637 total in jobs.json (servicenow 1,194 / salesforce 4,286) — nearly all re-fetches of rows already on the board. Two raw net-new URLs:
  - RSM "Salesforce Supervisor CPQ Solution Architect" — Toronto, adzuna.ca/details/5974913547, posted 2026-11-22 — **already tracked on the board** (README row), not new.
  - Shore Consulting "Lead Platform Engineer (DevOps & MLOps)" — Toronto, adzuna.ca/details/5974229824, posted 2026-11-21, tags devops — **EXCLUDED**: off brief (not ServiceNow/Salesforce; not in the other-category spec: ITAM/CMDB/Discovery/MID Server/ITOM/Event Mgmt/GRC-IRM/SPM/FSM/HRSD/Data-integration).
- Board unchanged at 5,636 rows. No jobs.json/README.md/FRESH_JOBS.md/public/ changes committed. No GitHub Pages deploy required — the live page already reflects HEAD.

## Sources checked this hour
- **Adzuna CA API** (`api.adzuna.com/v1/api/jobs/ca/search/1`, demo keys app_id=54ce986e / app_key=db851f299e966c0a2a72af525dce6199, `sort_by=date`, `max_days_old=14`, `content-type=application/json`, `where=Toronto|Ontario|Canada`): 190 matching postings across servicenow/salesforce variants. `www.adzuna.ca/details/<id>` returns CloudFront **403** from this host — treat as bot-wall on a live posting, never as dead; never probe detail pages via curl from this host; rely on API `created` + title + redirect_url.
- **LinkedIn guest search**: 151 cards after one 429 retry — 0 net-new (every card already on the board). Validate health by body length (~31 KB) + md5 distinctness, not HTTP 200 alone (the authwall also returns 200, ~3.4 KB, identical body across queries).
- **Workday CXS** (POST /wday/cxs/{tenant}/{site}/jobs, `--compressed`, Content-Type/Accept/Origin headers only): all 14 boards (bmo/td/cibc/manulife/interac/accenture/salesforce/altusgroup/iko/huron/irvingoil/mckesson/brookfield/gdit/resolvetech × servicenow+salesforce) returned **HTTP 429** — rate-limited at this hour; the CI hourly pass at 08:00Z carries Workday. Do not manual-probe during the 429 window; a spaced retry (≥8 s between calls) pays off within ~4 minutes after the window clears (verified pattern: 16:02Z all-429 → 16:06Z all-200).
- SmartRecruiters ServiceNow 12, Greenhouse 12, Lever 1, Ashby 2, remote feeds 6 — all already tracked.

## Patterns / lessons re-confirmed
- Adzuna API is the fast hourly freshness oracle; Job Bank/Eluta sweeps are slow (>300 s) and only needed for specific coverage gaps.
- LinkedIn job-id (trailing numeric id) is the hard dedupe signal — reposts rename titles (e.g. "...-5816" twins are one posting).
- Adzuna re-issues the same role under new detail ids (e.g. Amicis BA 5972002660 → 5972983023; TechNeptune CMDB Consultant 4491354155 → 4491940243); dedupe on company+title fuzzy + title substrings (rows with company "Unknown" carry the employer inside the title), not URL alone.
- "Platform Engineer" in a title ≠ ServiceNow/Salesforce platform role; gate on tags (servicenow/salesforce) and body context, not the word platform.
- ServiceNow-the-company posts only sales/SRE/security in Toronto; Salesforce-the-company posts nothing below 4 days / no Platform Admin/Dev I. Fresh platform work comes from banks (BMO/TD/CIBC/Manulife Workday) and GRC/IRM consultancies (PwC/Deloitte/EY).
- jobs.bell.ca shows zero SN/SF reqs; Bell's real ServiceNow hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation. Rogers Phenom board (jobs.rogers.com) returns a zero-row shell — use LinkedIn/Adzuna for Rogers rows.
- Public-sector portals (jobs.gc.ca, gojobs.gov.on.ca) are Radware-walled; Job Bank is the proxy — trust only title-named platform postings.
- Salary schema: `{min, max, currency: "CAD", display}` objects, never strings.
- Working-tree hygiene: this run reverted its own scan artifacts because 0 net-new jobs — do not commit churn for an empty hour.

## Negative space (searched, nothing fresh)
- LinkedIn Salesforce "Platform Administrator" / "Platform Developer I", Toronto: no fresh postings this hour.
- Workday Canadian tenants: 429'd; no employer-direct bank reqs surfaced this hour.

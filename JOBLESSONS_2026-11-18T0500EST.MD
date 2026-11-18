# JOBLESSONS_2026-11-18T0500EST — hourly BESTIEJOB scan (Toronto SN/SF)

Run: 2026-11-18 05:00 EST (10:00Z), cron. Repo: eltonaguiar/BESTIEJOB @ main, commit 99bb84d (origin/main synced, clean tree).

## Sources scanned this hour
- `FRESH_JOBS.md` — output of the :00Z hourly scan (`scripts/daily_job_scan.mjs --no-readme`), 2617 postings across 10 sources (adzuna 490, linkedin 261, workday 20, greenhouse 16, smartrecruiters 12, remotive 6, ashby 2, lever 1, remoteok 1, jobicy 1), generated 2026-11-18T09:12Z (04:12 EST).
- Targeted partner/company searches: Rogers (`jobs.rogers.com`), Bell (`jobs.bell.ca` / `jobs.bce.ca`), CGI, Deloitte, Accenture, ServiceNow careers (`careers.servicenow.com`), Salesforce careers (Toronto hub), Government of Canada (GC Jobs / Job Bank). One web_search per partner + ServiceNow/Salesforce + Toronto.

## Dedupe against board (jobs.json 2575 rows, README tables)
- `FRESH_JOBS.md` parsed: 2566 unique rows (by URL), 2177 Canada-located, **0 not already on board** (dedupe key = `company.lower()|title.lower()`, plus URL). The automated :00Z scan already merged everything feed-relevant by the 04:00 EST run.
- Partner-search candidates: all either already on board, older (September LinkedIn ids), no confirmable posted date, or closed.

## Verified new jobs added (0)
- No new job met the board gate this hour: Canada location + ServiceNow/Salesforce + absolute posted date within ~30 days + resolvable job URL + not already on board + not closed.

## Excluded this hour
- Accenture — ServiceNow Solution Architect (job no. r00306880, Toronto/Ontario, full-time, $99,450–$209,900): real partner posting confirmed via search index, but **no confirmable posted date** and the direct URL renders a React search shell rather than the job body — excluded (gate requires an absolute postedDate and a resolvable job URL).
- Accenture — ServiceNow Implementation Architect – Hybrid, Toronto (`jobs.ca/acestack/jobs/servicenow-implementation-architect-toronto-on-84515bdff33a`): posted 2026-11-14, $130,000–$135,000, body-verified, but **"Applications are currently unavailable for this posting"** — closed, excluded.
- S-M Software "…CRM…Senior" — Siebel, not Salesforce (body-check required; "CRM" ≠ Salesforce).
- Generic titles without the platform in title or body (business analyst, IT support, sales/marketing, PMO, recruiting) — excluded per board remit.

## Patterns / lessons for future agents
1. The :00Z hourly GitHub Actions scan already merges the full Adzuna/LinkedIn/Workday/ATS feed into jobs.json + README by ~04:00 EST; a manual 05:00 EST re-scan surfaces 0 new feed jobs. Don't expect additions on consecutive hourly runs.
2. Partner direct searches (Rogers/Bell/CGI/Deloitte/Accenture/GC) are worth running once per day, not every hour: Rogers careers under maintenance, Bell zero reqs, CGI/Deloitte surface only older (September) LinkedIn ids already on board, GC portals captcha-walled.
3. Gate strictly: a posting needs (a) an absolute posted date, (b) a URL that resolves to the job body (not a JS search shell), (c) not "applications unavailable"/closed. Accenture r00306880 failed (a)+(b); Accenture Implementation Architect failed (c).
4. Dedup key = normalized URL + `company.lower()|title.lower()`; same title with a different LinkedIn job id = a different posting (keep location-distinct rows).
5. "CRM" titles must be body-checked for Siebel vs Salesforce before adding.
6. Files changed: `JOBLESSONS_2026-11-18T0500EST.MD` only (no README/jobs.json/public changes this hour — nothing verified to merge).

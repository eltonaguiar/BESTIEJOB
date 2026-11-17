# JOBLESSONS_2026-11-17T1500EST — 15:00 EST hourly scan (Nov 17, 2026)

## Scope
Fresh Toronto/GTA ServiceNow + Salesforce jobs, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Canada-focused (Toronto/GTA + Remote Canada accepted). Dedupe against jobs.json, README.md tables, and APPLIED.md (URL normalization: strip query strings/trailing slashes). Merge verified fresh jobs to jobs.json + README + public/ (GitHub Pages).

## What ran this hour
1. **LinkedIn guest browser** (Toronto, f_TPR=r86400, past 24h) × ServiceNow and × Salesforce — 60 cards each, healthy ~317–320 KB HTML (authwall is ~337 KB and repeats the same md5; length+digest distinctness is the health test, not status).
2. **Workday CXS** re-probe of bmo/td/cibc/interac/manulife/accenture/salesforce/gdit tenants — all HTTP 200 this hour (no 429), but every SN/SF title was 4+ days old ("Posted 5 Days Ago", "Posted 14 Days Ago", "Posted 30+ Days Ago"); newest was TD Senior Solution Architect (ServiceNow) "Posted Yesterday" — architect tier, already on board. Workday stays useful but mostly stale for Toronto platform roles.
3. **Rogers** `jobs.rogers.com` date-sort page 1 — 0 ServiceNow/Salesforce mentions (rogers_today.html).
4. **Bell** — skipped (jobs.bell.ca shows (0) for servicenow/salesforce; weekly re-check only).
5. **Job Bank** title search for ServiceNow/Salesforce Toronto — noise/stale (hits from March–August 2026; posting 404s once expired, so search hits are not proof of live). Public-sector portals (jobs.gc.ca, gojobs.gov.on.ca) remain Radware-walled.
6. **Partner/Elite Partner gap scan** — FX Innovation, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze; mostly 0 anchors. Recent partner checks (Deloitte Jul 9 stale; Cognizant Nov 4 architect tier; Cognizant Jr SN Sep 10 stale) hold — no entry-level Platform Administrator / Platform Developer I from partners this hour.

## Fresh verified Toronto SN/SF jobs merged this run: 1 net-new to jobs.json

| Role | Company | Location | Posted | URL | Status |
|---|---|---|---|---|---|
| Salesforce Administrator (Remote) | Hired | Toronto, ON · Remote, Canada | 2026-11-17 (8h ago) | ca.linkedin.com/jobs/view/salesforce-administrator-remote-at-hired-4491158151 | Added to jobs.json (was in README only — README row source linkedin-guest--2026-11-17--v1.md); liveness gate kept it (LinkedIn 403 = live, not dead); site rebuilt to public/ (5,987 jobs) |

Every other platform-titled candidate from today's LinkedIn and Workday sweeps was already on the board:
- ServiceNow: 4484026843 (ServiceNow Principal Solution Architect), 4490380189 (BMO CMDB Administrator), 4491166743 (Envision ITOM Developer), 4491539817 (TD Senior Solution Architect), 4488382344 (W3Global Developer cum Architect)
- Salesforce: 4491195862 (White Bay), 4490484571 (Citco Solution Architect), 4490945616 (Smart IT Frame CPQ Architect — off-target), Co-operators Manager roles ×3

Skipped/off-target: 4490950459 PwC Brasil IRM/GRC (not Canada), 4490686438 Astra-North ITSM Zendesk→OpenText migration (not SN/SF platform).

## Merge mechanics this run
- Prepended row to jobs.json (schema: id `source:url`, salary object null, postedDate ISO 8601, workArrangement `remote`, tags `[salesforce]`); meta.total 2845→2846.
- `python3 tools/verify_links.py --days 2`: 127 fresh rows probed, live=30, dead=0, unknown=97, nothing dropped.
- `python3 tools/build_site.py`: public/jobs-data.json + public/index.html rebuilt — 5,987 jobs (SN 966 / SF 1,020 / Other 4,000), built 2026-11-17 20:04 UTC.
- **Race:** `git push origin main` rejected (Actions hourly scan landed first: 3113ee0 "hourly scan refresh 2846 listings"). Rebased with upstream wins on jobs.json/public/* (`git checkout --theirs`); upstream commit already contained the 4491158151 row (same 2846 total), so my commit was skipped as redundant. main == origin/main == 3113ee0. No separate push needed.
- Live page verified: `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` HTTP 200, 5,987 jobs, contains 4491158151; index.html HTTP 200.

## Recurring pattern
4th consecutive hour with ~zero net-new Toronto Platform Admin/Dev I postings (12:00/13:00: 0 fresh; 14:00: 1 SN job already committed; 15:00: this run). Market shape unchanged: fresh platform work = senior/architect roles at banks (BMO/TD Workday) and GRC/IRM consultancies; ServiceNow-the-company and Salesforce-the-company post nothing below 4 days and no Platform Admin/Dev I in Toronto.

## Recommended next-hour focus
- Re-probe Workday CXS tenants after cooldown only if they previously 429'd (they returned 200 this hour, so hourly Workday is viable again — but hits are aging).
- Keep LinkedIn guest browser (not the API — 429s after ~4 rapid queries) for Toronto f_TPR=r86400 sweeps.
- Rogers page 1 clear; re-check weekly unless a platform title appears. Bell weekly. Job Bank title-filtered only as public-sector proxy.

## Files changed
- jobs.json (+1 row: Hired Salesforce Administrator) — already contained in upstream commit 3113ee0
- public/jobs-data.json, public/index.html (rebuilt) — already contained in upstream commit 3113ee0
- This lessons file (JOBLESSONS_2026-11-17T1500EST.MD), commit [skip ci]

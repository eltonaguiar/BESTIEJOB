# JOBLESSONS_2026-11-18T2200EST

Hourly Toronto ServiceNow / Salesforce scan — cron run 2026-11-18 22:00 EST (America/Toronto).

## What ran

Fresh CA sweep (today + yesterday window: 2026-11-18 → 2026-11-19):

- Adzuna — dated API, `max_days_old=2` + `sort_by=date`, 68 calls, geos: national, Toronto Ontario, Ontario
- Job Bank — 12 keyword pages (servicenow / salesforce variants)
- Eluta — 6 keyword pages
- LinkedIn guest pass — SKIPPED: the 19:00 EST daily_job_scan already covered the past-24h LinkedIn guest window (~3 h ago); re-running the same window returns the same already-evaluated requisitions.

Every kept URL was live-checked (HTTP 2xx/3xx) before submission.

## Dedupe result

Raw 84 → unique 9 → kept **0** after date window, liveness, URL dedupe and title+company+city fingerprint dedupe against README.md + jobs.json:

- 9 rows already on the board (URL duplicates) — dropped, not re-added.
- No genuinely new Toronto ServiceNow or Salesforce posting this hour.

## What changed

- README.md: **unchanged** — still 6,209 live postings (0 added this run).
- jobs.json / public/*: **unchanged** — no new rows to sync.
- Site (GitHub Pages): no rebuild required since README/jobs.json did not change; last built by the 21:00 EST run remains current.
- inbox/fresh-ca--2026-11-19--v1.md (new, empty table — 0 kept rows) and reports/fresh_ca_2026-11-19.json (refreshed) recorded as scan artifacts.
- JOBLESSONS_2026-11-18T2200EST.MD (this file) committed.

## Lessons

- Zero net-new is a real finding, not a failed scan: the board is refreshed hourly by parallel sweeps, so a quiet hour means the aggregators (Adzuna/Job Bank/Eluta) have nothing dated today-yesterday that isn't already published.
- Adzuna's dated API remains the freshest Canadian SN/SF source; Job Bank keyword matching stays noisy (most "servicenow"/"salesforce" hits are non-platform roles) — verify platform-build duties before counting a req.
- Indeed.ca (Cloudflare) and dice.com (US-only) remain unusable for Toronto SN/SF from this network; employer Workday/Lever/Greenhouse boards and Job Bank are the reliable Canadian channels.
- Rogers / Bell / Canadian government: covered indirectly — Rogers surfaces only Salesforce-using sales/marketing-ops roles (Ottawa/Brampton/Vancouver, not Toronto platform roles), Bell's ServiceNow reqs are expired or already scanned, and Government of Canada postings arrive via the Job Bank feed already in the sweep. No direct Rogers/Bell/GC careers-board SN/SF dev/admin hits in this window.

## Files touched

JOBLESSONS_2026-11-18T2200EST.MD (new); inbox/fresh-ca--2026-11-19--v1.md (new); reports/fresh_ca_2026-11-19.json (refreshed, untracked). README.md, jobs.json, public/ unchanged.

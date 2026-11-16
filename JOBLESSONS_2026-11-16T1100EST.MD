# JOBLESSONS_2026-11-16T1100EST — hourly cron scan (11:00 EST / 16:00 UTC)

## Result this run
- Fresh Toronto ServiceNow / Salesforce scan performed: Workday CXS tenant probes (BMO/TD/CIBC/Manulife/Sun Life/Interac/Rogers × ServiceNow & Salesforce) plus the 10:02 EST `extracted_fresh_jobs.json` extraction, `gap_scan_2026-11-16.json`, and todayfeeds inbox (04:01Z).
- **0 brand-new on-target discoveries this hour.** Nothing merged to README.md / jobs.json / public/.
- Live page unchanged: https://eltonaguiar.github.io/BESTIEJOB/ remains current from the 10:00 EST push (ServiceNow 1295 / Salesforce 1504 / Other 4777 = 7,541 live postings, "as of 2026-11-16").

## What was checked and why each source yielded nothing mergeable

- **Workday CXS extraction (`raw/extracted_fresh_jobs.json`, 10:02 EST)** — 11 surfaced rows, none mergeable:
  - BMO ServiceNow CMDB Administrator (Posted 4 Days Ago) — already aboard, recurring requisition.
  - BMO ServiceNow Technology Lifecycle Analyst (Posted 4 Days Ago) — already aboard.
  - BMO ServiceNow SAM Administrator–ITAM (Posted 13 Days Ago) — already aboard, outside fresh window.
  - GDIT ServiceNow Developer / System Administrator / Sr Principal (Any Location / Remote, 3–14 days) — not Toronto-first, skipped.
  - Interac Senior BSA (ServiceNow) / QE Senior Specialist (ServiceNow Platform) — Posted 30+ Days Ago, outside fresh window.
  - TD Software Engineer III–Salesforce Data 360 (Posted 3 Days Ago) — already aboard.
  - Deloitte Lead Specialist ServiceNow CMDB Solution Architect — architect/vendor role, excluded (board targets Platform Admin / Platform Dev I; a job *at* a consultancy as an architect is not a platform role).
- **Workday CXS re-probe at 11:00 EST** — HTTP 429/422 on every tenant (rate-limited); could not pull fresher pages. Relied on the 10:02 extraction instead.
- **gap_scan (`raw/gap_scan_2026-11-16.json`, 01:03Z)** — partner/Elite-sponsor career sites (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze): `dated: []`. Lane Four "Salesforce Consultant" / "Salesforce Administrator" are undated — the merger skips undated rows, so nothing mergeable.
- **todayfeeds inbox (`raw/inbox/todayfeeds--2026-11-16--v1.md`, 04:01Z)** — Workday "Posted Today" roles were all data engineering (Altus Group, Brookfield, Moneris, OMERS) plus a Salesforce "Technical Architect Director – PubSec – Mulesoft Canada" (architect, 4 locations, not Platform Dev I). No ServiceNow / Salesforce Platform Admin/Dev I.
- **Web cross-check (Glassdoor/Indeed/LinkedIn/Simplify/jobs.ca)** — closest candidates: PwC Technical Salesforce Associate (posted Nov 12, ~4 days old, outside strict fresh window), Scotiabank ServiceNow Administrator Specialist (Oct 20, stale), Celestica Salesforce Developer Intern (student-only, not entry-level hire). No posting verified as posted today/yesterday with a live Toronto deep-link absent from jobs.json/README/APPLIED.md.

## Dedup & verification procedure (followed this run)
1. Read jobs.json (system of record) + README tables + APPLIED.md.
2. Normalize URLs (strip tracking params/trailing slashes); exclude anything already in jobs.json, README, or APPLIED.md (APPLIED.md is a hard exclude).
3. Confirm freshness (posted today/yesterday), direct posting deep-link (rejects hubs/search pages), Toronto-first / Canada scope, and platform targeting (ServiceNow in title/description/certs; Salesforce = Platform Administrator / Platform Developer I, esp. entry-level/junior).
4. Only merge after a live detail re-fetch confirms the posting is still open — LinkedIn guest re-fetch stayed unavailable this run (Chrome profile locked; direct LinkedIn 301/403), so LinkedIn leads could not be confirmed live and were deferred, not merged.

## Recurring collision pattern
- The automated hourly scan (`chore(jobs): hourly scan refresh ... [skip ci]`) can push to origin/main mid-run causing non-fast-forward rejections. Fix each time: `git fetch origin`, `git rebase origin/main`, `git checkout --ours public/*` (upstream wins on generated files), keep the README change, `python3 tools/build_site.py`, amend, push. Never `--force`.

## New lessons this run
1. **Workday CXS rate-limits hard after repeated probes** (429/422 on all tenants at 11:00 EST). Space probes ~6s apart and cache the last good extraction; do not re-probe the same tenants within the hour when 429 arrives.
2. **Relative "Posted N Days Ago" is not publishable** — BMO's 4-day and 13-day requisitions recur under the same job IDs (R260030992, R260030995, R260030096); only `postedOn` absolute dates convert to published rows.
3. **Architect/vendor roles are a steady noise source** — Deloitte/GDIT/ServiceNow-inc architect/SRE/sales surface in every SN/SF scan; the board rule ("a job at ServiceNow/Salesforce is not a ServiceNow/Salesforce platform role") keeps rejecting them. Document once, re-apply silently.
4. **LinkedIn leads without guest re-fetch stay deferred** — web-search "1 day ago" snippets give freshness hints but not liveness; merging unverified leads pollutes the board. Defer to next run rather than merge-and-retract.

## Board state after this run
- README.md, jobs.json, public/ unchanged.
- Only this lessons file committed ([skip ci]); no pages.yml redeploy needed since no board data changed.

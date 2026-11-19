# JOBLESSONS_2026-11-18T2000EST

Hourly Toronto ServiceNow / Salesforce scan — cron run 2026-11-18 20:00 EST (America/Toronto).

## What ran

Confirmation re-scan after the 19:00 EST merge (HEAD 2ecdbe6, committed 19:09 EST, +8 fresh jobs). Board state at run start: ServiceNow 1123, Salesforce 1026, Other 4058, 6206 live postings, window 2026-10-20 → 2026-11-19.

Sources checked this cycle:
- Job Bank (jobbank.gc.ca) — ServiceNow Toronto: 26 keyword results, mostly non-platform roles; the two platform matches (Bonafide Info Systems CMDB Consultant 50740661, Source Code RQ7 SPM 50698289) were already merged from the 18:00 EST scan.
- Job Bank — Salesforce Toronto: 110 keyword results, mostly non-platform roles; nothing new.
- dice.com — ServiceNow Toronto: 0 results; Salesforce Toronto: 0 results (dice is US-focused).
- nodesk.co Canada remote: 2 results, neither SN/SF (commerce marketing, CircleCI engineering).
- Indeed.ca — Cloudflare blocked (Ray ID a5cb4a04cc45ac5a), not usable from this network.
- LinkedIn guest — not re-run: the 19:00 EST daily_job_scan already covered the past-24h LinkedIn guest window (f_TPR=r86400) one hour ago; re-running the same window would surface the same already-evaluated requisitions.

## Dedupe result

Fresh SN/SF jobs found this cycle: **0 new verified jobs** — a valid result per the runbook. Spot-checked recent 2026-11-18 leads (SPECTRAFORCE 4492200627, TD Senior Solution Architect R_1521185, TechNeptune ITOM Developer 4491345268, Raas Infotek 4492046880, NTT DATA SPM BA 4490843088, 2iSolutions 4492201395) are all already present in jobs.json / README.md (dedupe by URL + company+title+city).

No inbox/ submissions pending (hermes-cron--2026-11-18--v9.md was merged at 18:13 EST in commit 5da0175).

## What changed

Nothing merged to README.md this cycle. Only this JOBLESSONS record is being committed. Pre-existing uncommitted change (ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM nested repo) left untouched, not part of this commit.

## Lessons

- The board is refreshed at least hourly by parallel scans; a single hour (19:00→20:00 EST) produced zero new Toronto SN/SF postings this cycle. Zero is a real finding, not a failed scan.
- Indeed.ca and dice.com are not viable Toronto SN/SF sources from this network (Cloudflare block / US-only index). Rely on Job Bank, employer Workday/Lever/Greenhouse pages, and the daily_job_scan.mjs feed aggregation.
- Job Bank keyword matching is noisy ("servicenow"/"salesforce" match unrelated postings); always verify platform-build duties before counting a req.
- GitHub Pages deploys on push to main via pages.yml; committing this lessons record redeploys the board site.

## Files touched

JOBLESSONS_2026-11-18T2000EST.MD (new). README.md, jobs.json, public/* unchanged this cycle.

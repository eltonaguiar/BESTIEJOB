# JOBLESSONS_2026-11-17T1900EST.MD

19:00 EST scan, Tuesday 2026-11-17. BestieJob board: eltonaguiar/BESTIEJOB (main), live page eltonaguiar.github.io/BESTIEJOB.

## What this run did
1. Ran the freshness-first Canadian sweep (`scripts/fresh_ca_scan.py --days 2`, Adzuna + Job Bank + Eluta, ServiceNow/Salesforce titles, postings dated today/yesterday). The local run did not complete in this session — no new `inbox/fresh-ca--2026-11-17--v*.md` artifact was written, so no new rows were surfaced by this run itself.
2. Relied on the most recent complete sweep (07:00 UTC / 02:00 EST today, 105 boards, liveness-verified): ServiceNow — 0 net-new; Salesforce — 4 net-new, all already merged into `readme.md` by earlier runs (Jobgether ×3 via Lever, Docebo ×1 via Ashby, all dated 2026-11-10/2026-11-13). Hourly scans at 17:00 EST and 18:00 EST also returned 0 fresh.
3. Dedupe check: all 4 fresh Salesforce postings confirmed present in `readme.md` (URL and fingerprint match), 0 ServiceNow postings missing. Nothing new to merge — `readme.md` and `jobs.json` already current; no readme/jobs commit this run.
4. GitHub Pages: no board change, so no README/public push; the scheduled Pages redeploy (`35 * * * *`) keeps eltonaguiar.github.io/BESTIEJOB current with main (next at 19:35 EST). Live page last known HTTP 200, ~5.7k jobs serving.

## Fresh jobs this cycle (all already on the board, deduped against jobs.json + readme.md)
| Posted | Title | Company | Location | Source |
|---|---|---|---|---|
| 2026-11-13 | Associate Vice President, Salesforce Engineering & Development | Jobgether | Canada | Lever |
| 2026-11-13 | Solution Architect, Salesforce Voice | Jobgether | Canada | Lever |
| 2026-11-10 | Associate Salesforce Administrator | Jobgether | Canada | Lever |
| 2026-11-10 | Senior Salesforce Developer | Docebo | Toronto, Ontario | Ashby |

ServiceNow: 0 fresh this cycle.

## Patterns / lessons
- Freshness-first (≤2 days, Adzuna/Job Bank/Eluta) and breadth-first 7-day hourly scans catch different jobs: the 07:00 UTC sweep fetched ~13,100 SN and ~13,200 SF postings across 105 boards but only 4 were net-new and ≤7 days old. Fresh Toronto SN/SF roles arrive in bursts, not steadily — most hours yield 0.
- Dedupe by fingerprint (title|company|city), not URL only: the same requisition is advertised under multiple mirrors (Adzuna, LinkedIn, Lever, direct ATS) with different URLs and dates. `scripts/fresh_ca_scan.py` gates on both fingerprint vs readme.md and URL vs jobs.json.
- Workday CXS rate-limits bursts at HTTP 422 — space calls ≥5s. LinkedIn `seeMoreJobPostings` 429s after ~4 rapid queries; LinkedIn guest detail pages remain readable.
- Known SN/SF partners and consultancies covered in the sweep: Accenture, DXC, RSM, NeuraFlash, Levio, Highmetric, 9th Way Insignia, CGI, TELUS Digital, etc. Public-sector source covered: Job Bank (jobbank.gc.ca). No fresh Canadian-government SN/SF roles this cycle; Rogers/Bell/TD/BMO/CIBC/Sun Life/Manulife boards were queried with no fresh SN/SF hits.
- Local `fresh_ca_scan.py` can exceed a 7-minute run budget (URL liveness check per kept row). Future runs: keep the merge step decoupled from the scan so a slow scan never blocks publishing what's already verified.

## Board state after this run
- readme.md: 7,588 live postings, window 2026-10-02 → 2026-11-17; ServiceNow 1,331 / Salesforce 1,531 / Other 4,777; 30-day window, Toronto-first, newest first.
- No changes to readme.md, jobs.json, or public/ this run; nothing to commit for jobs.
- This file committed to main under [skip ci]; Pages redeploys on its hourly schedule regardless.

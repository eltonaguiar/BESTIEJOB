# JOBLESSONS_2026-11-12 — hourly BESTIEJOB scan (2026-11-12 00:00 EST / 05:00 UTC)

## Scope
Toronto-first ServiceNow / Salesforce / IT-platform job board (`eltonaguiar/bestiejob`, main). Hourly cron scan: find fresh postings dated ~today/yesterday, dedupe against the board, merge verified rows into README.md's three tables, rebuild GitHub Pages (`public/`), push to main. Pages redeploy on push via `.github/workflows/pages.yml`.

## Result this run
**0 verified fresh rows added to the live tables.** The scan ran and the site was rebuilt, but no new row passed all three gates (fresh + direct posting URL + not already on the board).

| Metric | Value |
|---|---|
| Scan start | 2026-11-12T05:02:17Z |
| Fresh postings surfaced by scan | 783 across 10 public sources |
| jobs.json total after sync | 2,888 |
| Live page indexed | 2,442 jobs (SN 876 / SF 915 / Other 651) |
| Duplicate mirrors collapsed | 314 |
| Applied roles hidden | 35 |
| Board tables | ServiceNow 595 / Salesforce 612 / Other 583 — **unchanged** |
| Dead links dropped | 1 (appended to dead_urls.txt) |

## Source breakdown (this scan)
- SmartRecruiters (ServiceNow): 13 · Workday (BMO/TD/Altus/BDP/CAAT/etc.): 14 · LinkedIn guest: 307 · Adzuna: 422 · Greenhouse: 16 · Lever: 1 · Ashby: 2 · RemoteOK/Jobicy/Remotive: 8
- 4 Adzuna queries returned HTTP 503/429 (rate-limited): `servicenow administrator/Toronto`, `servicenow lead/Toronto`, `salesforce remote/Canada`, `it asset management/Toronto` — re-try next hour, those keywords are not lost (other Adzuna queries cover them).
- LinkedIn guest: 307 cards; endpoint 429s after ~4 rapid queries — the script already paces at 1.8s/query with 2 workers; do not increase concurrency.

## Dedupe outcome
- Every URL from this scan's fresh set was already on the board (Adzuna/LinkedIn/Workday re-surface the same requisitions hourly) or fell outside the 30-day window → skipped, 0 added.
- Verify-links gate probed 154 rows posted within 2 days: 30 live, **1 dead**, 123 unknown (bot-walled/403). Dropped: ivari Canada "Salesforce Manager, Sales & Marketing Clouds" (LinkedIn 4093448492, now 404) → dead_urls.txt.
- `scripts/sync_readme_to_jobs.mjs` added 367 README-only rows into jobs.json (feed now a superset of README); `tools/build_site.py` rebuilt `public/jobs-data.json` + `public/index.html` from README tables + jobs.json.

## Target-company checks (Rogers / Bell / partners / GC) — nothing fresh addable
- **Rogers (jobs.rogers.com):** "Technical Specialist, Markham" (req 343759) mentions ServiceNow/Salesforce only as comparable preferred tools — not an SN/SF role, skipped. Rogers "Lead Management Operations" req 343961 was already added to the board in the previous run.
- **Bell (jobs.bell.ca):** ServiceNow Developer / Integrator (job id 431695, Ottawa/Toronto/Montreal/Quebec City) looked fresh on Indeed (~6h ago) but the canonical page returns **HTTP 410 "the job ... has been filled"** — verified closed, skipped. Earlier Bell SN roles (432824 System Administrator, 432829 Senior Technical Advisor) are already on the board.
- **Canadian government / Job Bank:** hits were Aug–Sept 2026 (e.g. Upstaff ServiceNow CSA/CAD consultant for Ontario, posted Sept 29) — outside the 30-day window. Nothing fresh.
- **ServiceNow Careers Ontario page:** 16 jobs listed; dated Toronto hits are sales/security/SRE roles (Nov 5–9), no fresh SN dev/admin/postings for Nov 11–12.
- **Salesforce careers Canada:** no fresh Toronto Platform Admin / Platform Developer I postings surfaced.
- **Partner career-site gap scan:** 7 sites (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) — 0 dateable postings; Lane Four's 2 Salesforce anchors publish no date → logged to `inbox/gap-scan--2026-11-12--v1.md` as undated (merger deliberately skips undated rows).

## Adzuna note
Adzuna detail pages return HTTP 405 to extractors — trust the dated sweep files (`inbox/fresh-ca--2026-11-11--v*.md`) for title/company/location/date, then diff the URL set against the board before adding. Adzuna emits one URL per city for the same requisition — dedupe by URL first, then company+title+date for near-dupes (vendor twins like Pacer/Nityo advertising the same req are distinct rows and both stay).

## Files changed
`README.md` (daily-scan block refreshed), `jobs.json` (+367 feed rows from sync), `dead_urls.txt` (+1), `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`, `public/jobs-data.json`, `public/index.html`, `JOBLESSONS_2026-11-12.MD`

## Left as-is (untracked working queue, per repo convention)
`inbox/*` (incl. new `inbox/gap-scan--2026-11-12--v1.md`), `raw/*`, `docs/JOB_GAP_STRATEGY.md`, `README.BAK_*` backups.

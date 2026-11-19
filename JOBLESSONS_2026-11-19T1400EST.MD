# JOBLESSONS_2026-11-19T1400EST — hourly Toronto ServiceNow / Salesforce scan

**Run:** 2026-11-19 14:00 EST (2026-11-19T19:03Z)
**Repo:** eltonaguiar/BESTIEJOB (main) · Live site: https://eltonaguiar.github.io/BESTIEJOB/

## What this run did
1. `git pull --rebase origin main` — fast-forwarded to cf67ba5 (the GH Actions hourly scan that ran 2026-11-19T18:16Z).
2. `node scripts/daily_job_scan.mjs` — this hour's scan: fresh=528 merged=2490 rows in jobs.json (servicenow 1159, salesforce 1194). Sources: adzuna 199, linkedin 284, smartrecruiters 13, greenhouse 17, lever 1, ashby 2, remotive 6, jobicy 4, remoteok 2.
3. `python3 tools/verify_links.py --days 2` — probed 184 fresh rows: live=96, dead=0, unknown=88. No rows dropped.
4. `python3 tools/build_site.py` — rebuilt public/jobs-data.json + public/index.html: 5,043 jobs (SN 841, SF 911, other 3,291), 838 duplicate mirrors collapsed, built 2026-11-19T19:04Z.
5. Committed jobs.json, README.md (DAILY-SCAN block), FRESH_JOBS.md, public/*. Pushed to origin/main. Triggered `pages.yml` for immediate GitHub Pages reflect (the data commit carries [skip ci]).

## Dedupe result
The 3 LinkedIn ServiceNow leads from the 05:00 EST cron scan (TechNeptune ITOM Developer 4491345268, SPECTRAFORCE Developer 4492200627, TechNeptune CMDB 4491354155) were already on the board — merge recorded +0 new, 3 duplicate. URL-based dedupe held.

## Source notes (this cycle)
- **Workday CXS:** HTTP 429 on every Canadian tenant (BMO, TD, Moneris, Altus Group, CAAT, Medcan, IKO, Huron, Irving Oil, McKesson, Brookfield, GDIT, Resolve Tech) for both `servicenow` and `salesforce`. Known pattern: the CI hourly at :00Z 429s Workday — leave Workday to the CI pass; manual probes retry max 3-4 tenants at ≥8s spacing.
- **LinkedIn guest API:** first call HTTP 429; retry returned 284 cards (healthy card HTML ~31 KB, differs per query). Always retry once before concluding empty; test length + digest distinctness, not just status.
- **Adzuna:** 199 postings; adzuna.ca/details detail URLs return CloudFront 403 via browser and HTTP — employer page/duties unverifiable for Adzuna leads this cycle. Do not probe Adzuna details as liveness.
- **LinkedIn detail pages:** signed-in wall for unsigned agents — posted date/title/company/location come from the committed scan only; duties not re-verified.

## Partner / employer / public-sector check (per task scope)
- **Rogers (jobs.rogers.com):** date-sorted listing `?q=&sortColumn=referencedate&sortDirection=desc` IS scrapeable via browser — 196 results, page 1 covers postings dated Nov 18–19, 2026. Zero ServiceNow/Salesforce titles on page 1 → no fresh Rogers SN/SF platform posting this cycle. Re-check weekly; deeper paging only when a keyword hit appears.
- **Bell (jobs.bell.ca):** returns empty shell / (0) for servicenow and salesforce — zero reqs, not a scrape failure. Re-check weekly.
- **Government of Canada / Ontario:** Job Bank search surfaces stale/undated postings (Mar–Aug 2026); jobbank.gc.ca/jobposting/<id> 404s once expired, so a search hit is not proof of a live posting; gojobs.gov.on.ca is Radware-walled (captcha) — do not retry. Use Job Bank only as proxy, trust only postings whose *title* names the platform.
- **Lane Four (Salesforce Select partner, Toronto):** Salesforce Administrator posting exists — entry-level (0–2 yrs SF experience), $50–75K, hybrid, downtown Toronto. BUT the posting page carries no postedDate (no JSON-LD, no date in body) → per protocol undated rows are skipped by the merger. Not added to the board this cycle; flagged for inbox/manual review.
- **Diabsolut / CloudJunction:** no dated Toronto SN/SF posting surfaced this cycle.

## What did NOT change
- Unrelated working-tree file `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` (submodule pointer) and untracked `leads-2026-11-18.jsonl` were left uncommitted.
- `jobs_merge_inbox.py` not run — no new inbox submissions this cycle; the scan writes jobs.json/README directly.

## Next cycle
- Re-run the hourly scan; retry Workday for 3–4 Canadian tenants at ≥8s spacing outside the :00Z window.
- Re-check Rogers page 2–8 and Bell/government portals on the weekly cadence.
- Lane Four Salesforce Administrator: obtain a verifiable posted date (employer page or ATS feed) before adding.
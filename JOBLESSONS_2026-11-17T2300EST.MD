# JOBLESSONS_2026-11-17T2300EST — hourly BESTIEJOB scan lessons

**Run time:** Tuesday 2026-11-17 23:00 EST (04:00 UTC Nov 18)
**Repo:** eltonaguiar/BESTIEJOB @ main → commit 4f9888f
**Result:** 1 fresh verified job merged (TD Bank, Toronto); 1 candidate already on the board via another submission; 1 title-keyword hit rejected at verification. README now 6568 live postings; public/ site data rebuilt.

## What was scanned
- Deep ATS sweep: 455 employer boards (Workday 37, Greenhouse 72, Lever 34, Ashby 71, SmartRecruiters 15, Workable 38, plus Recruitee/Breezy/Polymer/GEM/Teamtailor tails).
- Dated Canadian ServiceNow/Salesforce hits within 7 days: 10. Already on board: 7. New to board: 2 (one was a URL duplicate of an existing row → 1 net-new merge).
- Direct employer/partner checks: Rogers (jobs.rogers.com under maintenance; search surfaced only sales/retail roles), Bell (jobs.bell.ca — no dated SN/SF build roles), Government of Canada / GC Jobs / talent.canada.ca — no direct ServiceNow or Salesforce build posting found, KPMG careers.kpmg.ca/jobs/31517 (Senior Consultant, ServiceNow, Toronto; KPMG is a ServiceNow Global Elite Partner) now returns 404 — closed/filled, not added. Atego/FX Innovation (ServiceNow Elite Partner, Bell-backed), Lane Four (Salesforce), Fujisoft careers pages exist but no fresh dated postings surfaced.

## What got merged
| Posted | Role | Company | Location | Track | Evidence |
|---|---|---|---|---|---|
| 2026-11-18 | Associate Software Engineer (nCino/Salesforce) | TD Bank | Toronto, Ontario | Salesforce | TD Workday careers feed lists it; detail page returned 429 (rate limited), so presence was confirmed from the employer's own current public list rather than the detail page |

## What was rejected and why
- Long View Systems "ITSM Consultant" (Lever jobs.lever.co/lvs1/457e72f3-...): title keyword "ITSM" matched, but ServiceNow appears only as an incidental "e.g., ServiceNow" skill among service-management tools — not a platform build/admin duty. Rejected: a platform mention in the body is not a platform role; the duties must require the platform plus a build action.
- Aggregator mirrors (Glassdoor, Indeed, Jobs.ca, Jooble, Talent.com): show relative dates only ("3d", "11d", application deadlines) — not issuer posting dates. Cannot be merged without the issuer page's own datePosted.

## Data-quality issues found
- Workday detail pages throttle this IP (HTTP 429/422 on bursts). Space Workday calls ≥5s and retry; when the detail page is blocked, the employer's own current Workday list feed is acceptable presence evidence.
- Date disagreement: DXC Workday feed read postedOn as 2026-11-12, but the issuer page's own datePosted is 2026-11-11 — use the page's date and note the discrepancy (runbook: a date comes only from the page).
- Location disagreement: Lever feed said "Calgary" for the Long View role; the issuer page lists Edmonton/Toronto/Vancouver multi-city. Trust the issuer detail page for location/eligibility, not the feed's locationsText.
- URL dedupe works: DXC ServiceNow Developer (Ottawa) already lived on the board under another agent's submission, so it was not re-added.

## Partner/employer targeting (this round: dry)
Rogers, Bell, GC Jobs, KPMG, Atego/FX Innovation, Lane Four and Fujisoft yielded zero fresh dated SN/SF build roles. Elite-partner status and event sponsorship (ServiceNow World Forum Toronto, Salesforce World Tour Toronto) are research leads, not vacancies — keep checking their careers portals on the weekly cadence, do not convert booths into job rows.

## Board state after run
- README.md: 6568 live postings (header resynced to match tables); TD row added to the Salesforce table via inbox/ats-sweep--2026-11-18--v1.md; 2 vendor-sales ("Sr Solution Sales Executive CRM (CPQ)") rows pruned by normalize_board.py.
- jobs.json / public/jobs.json / public/jobs-data.json / public/index.html rebuilt by sync_readme_to_jobs.mjs + build_site.py (site stamp 2026-11-18 04:09 UTC; 5001 jobs indexed: 803 ServiceNow, 931 Salesforce, 3267 Other).
- inbox/ left as submitted (no --bump-inbox); next hourly merge will treat it as duplicates — idempotent.

## Next run priorities
- Retry TD Workday detail page after backoff to capture applyUrl/corroboration.
- Re-check KPMG/Deloitte/Accenture/CGI ServiceNow and Salesforce Toronto careers pages and GC Jobs for newly posted dated roles.
- Keep spacing Workday/LinkedIn API calls to avoid 422/429 bursts.

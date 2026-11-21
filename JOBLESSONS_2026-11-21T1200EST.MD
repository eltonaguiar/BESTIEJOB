# JOBLESSONS_2026-11-21T1200EST

**Run:** 2026-11-21 12:00 EST (17:00 UTC) — scheduled cron scan
**Scope:** Fresh Toronto ServiceNow / Salesforce jobs, deduped against github.com/eltonaguiar/bestiejob main branch
**Outcome:** Scan ran; 24 Toronto SN/SF jobs surfaced, all 24 already on the board (0 new merges). Board and GitHub Pages already current from the 16:13 UTC hourly scan.

---

## What was scanned

Sources queried (no-login, structured feeds):

| Source | Matching postings | Notes |
|---|---|---|
| LinkedIn (guest) | 239 | ca.linkedin.com job listings |
| Adzuna CA | 205 | adzuna.ca API; created date from ad |
| Greenhouse | 14 | Public board APIs |
| SmartRecruiters | 12 | ServiceNow board |
| Remotive | 6 | Remote feed |
| Ashby | 2 | Public posting API |
| Lever | 1 | Public board API |
| RemoteOK / Jobicy | 1 each | Remote feeds |

Workday lookups (BMO, TD, Altus, BDO, IKO, GDIT, Moneris, Brookfield, ResolveTech, Irving Oil, McKesson) returned HTTP 429 (rate limited) — no data from those employers this run.

Focused search (ITAM/CMDB/ITSM/other keywords) ran after the primary scan and added 742 rows to jobs.json across non-SN/SF tracks.

## Dedupe results

- 28 net-new rows added to jobs.json by the scan (5557 → 5585 before focused search pushed it to 6327)
- Of those, **24 are Toronto/Ontario SN/SF jobs** — all 24 already present in README.md tables (0 new merges needed)
- 4 other net-new rows (non-Toronto or Other-track) also already reflected on the board
- The remote main branch had already absorbed the 16:13 UTC hourly scan (5559 listings), so this run's data was subsumed; no push was required

Confirmed duplicate URLs were not re-added. The merger correctly rejected all 24 as duplicates.

## Verification notes

Verification is by structured ATS feed, not page scraping:
- SmartRecruiters, Greenhouse, Lever, Ashby: public board APIs — canonical employer postings
- LinkedIn guest endpoint: employer-syndicated listings
- Adzuna: aggregator, redirect_url to source; not a truth source on its own
- Direct page verification (browser) was not possible this run — Chrome profile locked; web-extract backend (DDG) search-only

Jobs flagged for follow-up verification (visit the canonical ATS detail before applying):
- Blue Mantis — Sr ServiceNow Business Process Consultant, Toronto (remote, adzuna 5974233718)
- Altus Group — Salesforce Platform Developer, Toronto (linkedin 4483476940)
- TD Bank — Associate Software Engineer (nCino/Salesforce), Toronto (adzuna 5971441048) — entry-level candidate
- CIBC — ServiceNow CMDB Administrator / Technology Lifecycle Analyst, Toronto (linkedin 4490380189 / 4490364941)
- OSI Digital — multiple Salesforce roles, Toronto (adzuna 5962506342/5962506340/5962506362)

## Partner / sponsor / target-employer findings

**ServiceNow partners with Toronto/Canada presence:**
- Fujitsu — Elite Consulting & Implementation partner, Toronto office (Build track is Premier, not Elite)
- Pentio — Toronto-based Select implementation boutique (Elite-only filters miss it)
- Ateko — Toronto World Forum sponsor; ServiceNow candidates routed to FX Innovation (fxinnovation.com/en/jobs), Salesforce to a separate ADP career centre
- NewRocket — ServiceNow Toronto sponsor (newrocket.com/careers)
- ServiceNow Inc. — direct hiring in Toronto (careers.servicenow.com/locations/ams/ontario-canada/)

**Salesforce partners / publishers:**
- Salesforce Canada careers — salesforce.com/company/careers/locations/north-america/canada/
- AppExchange Consulting — appexchange.salesforce.com/consulting
- Lane Four — Toronto Agentforce World Tour sponsor (lanefour.com/opportunities)
- Slalom, CloudFulcrum, NeuraFlash (Accenture) — Salesforce sponsors/partners
- Traction Rec — Canadian Salesforce product company (tractionrec.bamboohr.com/careers); search "Product Developer" not just "Salesforce"

**Telcos / banks / technical employers (already in employer-watchlist.csv):**
- Rogers — jobs.rogers.com
- Bell — jobs.bell.ca; Bell backs Ateko (CloudKettle); Bell Canada has ServiceNow Developer/Integrator and Salesforce Developer roles in Toronto
- CIBC, TD, BMO, RBC, Scotiabank — Workday/Lever/Adzuna hits; all in watchlist with daily cadence

**Canadian government / public sector:**
- Government of Canada — Senior Salesforce Developer, requires Secret clearance + Platform Developer cert (linkedin 4481939757)
- House of Commons — Full-Stack Developer (Digital Product Developer), ServiceNow exposure, Ottawa, via gJobs.ca; closes 2026-11-15
- CMHC — Bilingual Senior Specialist, ServiceNow ITSM Developer, Ottawa/Montreal/Toronto, hybrid, Secret clearance (careers.cmhc-schl.gc.ca)
- City of Toronto — Systems Integrator 1 (ServiceNow Developer), Toronto Court Services, CSA or CAD cert, hybrid (govjobsgta.com; posting period ended 2026-10-20 — monitor for re-post)
- Federal contract roles via Randstad/Myticas/Systematix — Government of Canada Reliability/Secret clearance, often Ottawa, sometimes remote

## Patterns worth reusing next run

1. **Employer-first, not keyword-first:** The watchlist (24 entries) is the productive loop. Re-check due sources before generic keyword searches. Adzuna + LinkedIn together surface most Toronto SN/SF; Workday employers (banks) need throttle-respecting retries on 429.
2. **Partner portals diverge:** Ateko splits ServiceNow → FX Innovation and Salesforce → ADP. Always save both portal records; never assume one careers page covers both practices.
3. **Entry-level signal:** "Associate Software Engineer" (TD, nCino/Salesforce), "ServiceNow Platform Specialist" (Alimentiv), "Salesforce Administrator" (CanPrev, Benevity, HCLTech) are the closest matches to Platform Admin / Platform Developer I. Junior roles rarely carry "Senior" in the title; filter out "Senior/Lead/Architect/Manager" when hunting entry-level.
4. **Government roles carry clearance:** Federal and City of Toronto ServiceNow/Salesforce roles routinely require Secret or Reliability clearance and sometimes bilingualism — tag these, don't count them as open-to-anyone.
5. **Date discipline:** Only absolute `YYYY-MM-DD` posting dates count as "fresh." Relative "3 days ago" and scan-clock dates are excluded from the fresh feed. The merger already drops non-absolute dates.
6. **Mississauga/Markham ≠ Toronto:** Per board scope, an office in Markham or Mississauga alone is not Toronto. Wipro (Mississauga) and Alimentiv (London) hits were excluded from the Toronto count this run.

## Next run (2026-11-21 13:00 EST or next cadence)

- Re-check due watchlist sources (Alimentiv, EQ Bank, Versapay, Cognizant, TD, Altus — daily cadence)
- Retry rate-limited Workday employers (BMO, TD, Altus, BDO) with backoff
- Check ServiceNow Partner Finder Elite/Global Elite filter for new Canadian firms
- Check Salesforce AppExchange Consulting partners by location for Toronto firms not yet in watchlist
- Monitor govjobsgta.com and GC Jobs for re-posted City of Toronto / federal ServiceNow roles
- Write any genuinely new rows to inbox/hermes-cron--2026-11-21--vN.md and run jobs_merge_inbox.py

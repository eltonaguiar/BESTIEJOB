# JOBLESSONS_2026-11-17T1600EST.MD

# BESTIEJOB Hourly Scan — Job Search Lessons

**Date**: 2026-11-17
**Run time**: 2026-11-17 16:00 EST (21:00 UTC) — scheduled cron run
**Scope**: Fresh Toronto / Canada ServiceNow and Salesforce postings (entry-level / Platform Admin / Platform Developer I emphasis)
**Repo**: github.com/eltonaguiar/BESTIEJOB (branch: main)
**Live board**: https://eltonaguiar.github.io/BESTIEJOB/

## Scan summary

| Metric | Value |
|---|---|
| Sources queried | inbox/adzuna-autonomous--2026-11-17--v1.md (Adzuna dated API, scanned 2026-11-17T14:03Z), raw/linkedin_guest_2026-11-17.json (LinkedIn guest, scanned 2026-11-17T11:39Z), raw/wd20261117/* (BMO, GDIT, TD, CIBC, Interac, Manulife, Accenture, salesforce.com Workday tenants, scanned 2026-11-17T06:03Z), raw/rogers_today.html (Rogers careers, crawled 2026-11-17T06:05Z), raw/gap_scan_2026-11-17.json (partner/sponsor boards: FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) |
| Dedupe baseline (README.md tables + jobs.json on main) | README 7,898 table rows; jobs.json 2,846 listings; 7,997 unique normalised URLs |
| Fresh Toronto/Canada ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no README change → no redeploy required; board already current as of 2026-11-17) |

## Candidates reviewed

- **Adzuna autonomous scan 2026-11-17T14:03Z** (inbox/adzuna-autonomous--2026-11-17--v1.md): 505 rows parsed (84 ServiceNow-classified, 152 Salesforce-classified). 0 unmerged — every URL already present in README (e.g. Astra-North SPM Developer Toronto 5968012935, BMO CMDB Administrator 5968011526, Pacer FSC Developer 5968012602, TD Salesforce Data 360 5968012143).
- **LinkedIn guest fresh 2026-11-17T11:39Z** (raw/linkedin_guest_2026-11-17.json): 7 fresh-dated roles (Co-operators "Manager, Systems Development - Agentic Salesforce Delivery" ×3 Toronto/Mississauga/Guelph posted 2026-11-17; Hired "Salesforce Administrator (Remote)" posted 2026-11-17; Alldus "ServiceNow ITOM Technical Consultant" posted 2026-11-16; PwC Brasil "IRM/GRC Technologies Senior Associate" Toronto posted 2026-11-16; Astra-North ITSM migration lead Waterloo posted 2026-11-16). 0 unmerged — all added by the 13:00–15:00 EST merges earlier today.
- **Workday tenant scans 2026-11-17T06:03Z** (raw/wd20261117/*): SN/SF-titled reqs found (e.g. BMO ServiceNow CMDB Administrator, TD Senior Solution Architect ServiceNow), but `postedOn` is relative ("Posted 2 Days Ago") with no absolute date — the merger refuses undated/relative rows rather than inventing a date. Already represented in jobs.json from the 19:12Z refresh.
- **Rogers careers** (raw/rogers_today.html): 0 ServiceNow/Salesforce mentions; the page is a JS shell linking to jobs.rogers.com/search (date-sorted), nothing server-rendered to harvest.
- **Partner/sponsor gap scan** (raw/gap_scan_2026-11-17.json): 7 partner career pages crawled; Lane Four "Salesforce Consultant" and "Salesforce Administrator" remain **undated** (no posted date on the page) → merger skips them; re-check next cycle if dates appear. Other partners (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Crossfuze) returned 0 anchors.
- **Canadian government portals** (jobs.gc.ca / gojobs.gov.on.ca): Radware-walled ("ops_gojobs_status: blocked"); Job Bank feed returned `found: []` for OPS platform roles.

## Already on the board (context)

README tables are current through 2026-11-17 ("Current jobs — as of 2026-11-17", window 2026-10-02 → 2026-11-17, 7,588 live postings; SN 1,328 / SF 1,531 / Other 4,777 per header). jobs.json at 2,846 listings, last refreshed 2026-11-17T19:12:47Z. Earlier today's runs already merged the day's fresh hits: 11:00 EST +250 Canada postings, 14:00 EST +1 Toronto SN (Hydro One/Acronym contract), 15:00 EST +1 Toronto SF (Hired Salesforce Administrator remote). The 10:00, 12:00, 13:00 and now 16:00 EST runs found 0 fresh — an empty merge is a valid hourly outcome.

## Patterns / lessons for future agents

1. **Hourly runs frequently yield 0 fresh.** By mid-day the board has already been swept by the 03:00 EST cron, the adzuna autonomous scan, the fresh-ca sweep, and linkedin guest scans; later hours re-surface the same population. Expect empty merges; do not force rows.
2. **Dedupe on normalised URL + classify on title.** Combined baseline this run: 7,997 unique URLs (README 7,898 + jobs.json 2,846). All 505 rows of today's adzuna scan and all 7 linkedin-guest fresh roles were already covered — 0 unmerged after normalisation.
3. **Undated ≠ addable.** Workday `postedOn` relative strings ("Posted 2 Days Ago") and Lane Four postings with no `datePosted` are skipped by the merger; never fabricate a posted date to force a row onto the board.
4. **Telco/government portals are poor hourly sources.** Rogers careers renders a JS shell with no server-side job rows; jobs.gc.ca/gojobs are Radware-walled; Job Bank full-text search is noisy (only title-named platform hits are trustworthy). Reserve these for the 3-hour fresh-ca cadence.
5. **Commit discipline.** Lessons-only commits carry `[skip ci]` (no README/public change → no Pages redeploy). Before pushing, `git fetch --prune && git rebase origin/main` — the hourly GitHub Action pushes independently and non-fast-forward rejects occur if you skip this.

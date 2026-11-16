# JOBLESSONS_2026-11-16T1800EST

Hourly BESTIEJOB scan — Toronto ServiceNow / Salesforce — Monday 2026-11-16 18:00 EST (UTC-05).

## Result: 0 fresh net-new jobs merged

No verified fresh Toronto ServiceNow/Salesforce postings were added to README.md this run. Every candidate surfaced by today's scan was either already on the board or not mergeable (see below).

## Scan sources run today (2026-11-16)

| Source | Scope | Fresh SN/SF candidates | Mergeable |
|---|---|---|---|
| Workday CXS | BMO, TD, CIBC, Interac, Manulife, SunLife, Accenture, GDIT, Salesforce (tenant scan `wd_*20261116`) | ~11 Canadian/Toronto SN/SF | 0 (all already in board) |
| LinkedIn (guest + verified) | ca.linkedin.com SN/SF search | 5 verified | 0 (present in jobs.json but undated; not in README.md) |
| Public sector (Job Bank / OPS) | canada.ca / ops.gojobs | 0 | 0 |
| Workday fresh probe | `raw/wd_fresh_2026-11-16.json` | 0 | 0 |

## Candidates checked and dedupe outcome

All workday-sourced Canadian Toronto SN/SF jobs found today are already present in both `jobs.json` and `README.md`:

- BMO — ServiceNow CMDB Administrator (Toronto) — posted ~2026-11-12 — README line 109
- BMO — ServiceNow Technology Lifecycle Analyst (Toronto) — posted ~2026-11-12 — README line 110
- BMO — ServiceNow SAM Administrator - ITAM (Toronto) — posted ~2026-11-03 — README line 324
- TD — Software Engineer III - Salesforce Data 360 (Toronto) — posted ~2026-11-13 — README line 6797

5 LinkedIn-verified SN/SF jobs (Smart IT Frame, HRConnects, Yochana, Cognizant, NLB Services) exist in `jobs.json` but are **not in README.md** and carry no absolute posted date (`posted_hint: null`). README.md rows require a `YYYY-MM-DD` Posted cell, and the merger drops undated rows, so these cannot be added without a date source. LinkedIn guest detail returns HTTP 422, so posted dates are not recoverable by scraping.

Liveness gate: the 4 workday candidate URLs were re-verified with `curl --compressed` + UA header — all return HTTP 200 on the full Workday path (`/en-US/External/...` and `/en-US/TD_Bank_Careers/...`). Short-form Workday URLs (no `/en-US/...`) return 404; the board stores the full form.

## Partner / Elite Partner / sponsor scan (Rogers, Bell, Government, etc.)

The task asked to check known ServiceNow/Salesforce partners, Elite Partners, sponsors, and technical companies such as Rogers, Bell, and Canadian government jobs.

- **Configured Workday board inventory** (`scripts/ats_board_sweep.py` WORKDAY list) covers: Accenture, AGF, Altus Group, BDO, BMO, Brookfield, CAAT Pension, Canadian Tire, CIBC, Cloudera, Danaher, Desjardins, DXC, GDIT, Harris Computer, Huron, ICF, IKO, Interac, Irving Oil, Manulife, McKesson, Medcan, MLSE, Moneris, OMERS, Resolve Tech, RSM, **Salesforce**, Salvation Army Canada, SOTI, Sun Life, TD, Thomson Reuters, TJX, TMX Group.
- **Greenhouse** list: NeuraFlash, Geotab, Varicent, Levio, Take-Two, iCapital, Movable Ink, Toast, Okta, nCino, LightFeather, Accenture Federal, GuidePoint, CCLFG, Dscout, Airbnb, SpaceX, Brex, MongoDB, Bloomerang, D2L.
- **Rogers** (`jobs.rogers.com`), **Bell** (`jobs.bell.ca`), and **Government of Canada** (`canada.ca` jobs) are **NOT** in the configured Workday/Greenhouse/Lever board inventory and were not scanned today. Web search returned only their career-site homepages, no extractable fresh postings.
- **Gap:** partner/Elite Partner career sites (Rogers, Bell, Deloitte, CGI, IBM Canada, GC Jobs) need dedicated scrapers or manual checks; they are currently outside the automated hourly scan.

## Lessons / patterns for future agents

1. **Dedupe is by canonical URL.** `jobs.json` holds 6,283 unique URLs. Always normalize (`strip query, trailing slash, lower`) before comparing; short-form vs full-form Workday URLs (`/job/...` vs `/en-US/External/job/...`) are different strings and caused a false "absent" reading on the first pass.
2. **README.md requires absolute posted dates.** `import_fresh_rows.py` skips any row without `posted` in `YYYY-MM-DD`; undated postings are reported separately, never merged. Workday CXS exposes only relative "Posted X Days Ago", so dates must be computed back from scan date (scan 2026-11-16 → "4 Days Ago" = 2026-11-12).
3. **Workday CXS is reachable via `wdN.myworkdayjobs.com` + `curl --compressed` + browser UA.** Bare tenant host NXDOUN; short job path 404s; full `/en-US/External/job/...` path returns 200.
4. **LinkedIn guest detail is blocked (HTTP 422); urllib blocked by Workday CXS.** Use `curl --compressed` with UA, or the Workday search JSON endpoint, not `urllib`.
5. **Concurrent pushes to main.** Peer agents push constantly; a bare `git push` is rejected. Always `git pull --rebase --autostash origin main` then retry push; verify with `git merge-base --is-ancestor`.
6. **`APPLIED.md` is a hard exclude** — never re-add roles already applied to.
7. **Board window is ~30 days (README states `nothing older than 30 days`, window shown as 2026-10-02 → 2026-11-16).** "Posted 30+ Days Ago" (Interac SN roles today) falls outside the window and is correctly excluded.
8. **GDIT "Any Location / Remote" roles are US-centric (defense contractor)** and do not pass the Canada scope check (`is_canadian`); exclude unless location confirms Canada.
9. **README.md and jobs.json counts diverge** (README: SN 1,297 / SF 1,505; jobs.json: SN 1,305 / SF 1,372) — pre-existing sync gap, not caused by this run; do not force counts.
10. **Previous hourly scans (16:00, 17:00 EST) also merged 0 fresh jobs** — today's Toronto SN/SF market is thin; scans surface mostly re-listings of roles already on the board.

## Recommended next steps

- Add Rogers, Bell, and GC Jobs career-site scrapers (or their Workday tenants) to the board inventory so partner/Elite Partner postings are covered hourly.
- Recover posted dates for the 5 undated LinkedIn-verified SN/SF jobs so they can be promoted from `jobs.json` into README.md.
- Keep the hourly cadence; the market is thin but BMO/TD/Interac re-list regularly.

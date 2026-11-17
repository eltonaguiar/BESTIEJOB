# JOBLESSONS — BESTIEJOB hourly SN/SF scan — 2026-11-17T0500EST

## Scope (this run)
- Families: ServiceNow + Salesforce (Platform Admin / Platform Developer I emphasis, entry-level preferred)
- Location: Toronto / GTA / Canada-first (Remote Canada accepted)
- Freshness window: postings ≤ 7 days old (cutoff 2026-11-10)
- Sources scanned: 105 employer/ATS boards (Workday, Greenhouse, Lever, Ashby, SmartRecruiters, Workable) including Rogers, Bell, Canadian banks, consultancies

## Results
- ServiceNow: 0 net-new fresh postings
- Salesforce: 4 net-new fresh postings found in prior cycle — ALL already merged to README.md before this run:
  - 2026-11-13 Associate Vice President, Salesforce Engineering & Development — Jobgether — Canada (lever)
  - 2026-11-13 Solution Architect, Salesforce Voice — Jobgether — Canada (lever)
  - 2026-11-10 Associate Salesforce Administrator — Jobgether — Canada (lever)
  - 2026-11-10 Senior Salesforce Developer — Docebo — Toronto, Ontario (ashby)
- Dedupe vs jobs.json + README.md: 0 new merges required this cycle; board already current.
- jobs.json note: Docebo ashby row present in README.md but absent from jobs.json — acceptable (build unions jobs.json + README; README-only rows render as their own card).

## Verification performed this run
- Workday CXS re-check (BMO ServiceNow): HTTP 200, 7 jobs all "Posted 2–15 Days Ago", none "Posted Today" — all already on board.
- Rogers date-sortable careers page: 0 ServiceNow / Salesforce hits.
- Bell careers: zero reqs for both families (re-check weekly, not hourly).

## Partner/company landscape (Toronto SN/SF)
- Fresh Canadian platform work comes mainly from banks via Workday (BMO, TD, Interac, Manulife, CIBC) and GRC/IRM consultancies (PwC ServiceNow IRM practice).
- Salesforce-the-company: posts nothing below 4 days old and no Platform Admin / Platform Developer I in Toronto.
- Rogers: date-sortable, parse `<tr>` rows with absolute dates; keyword search returns noise (sales roles mentioning SN in body).
- Bell: genuinely nothing — `(0)` in browser for both families.

## Rate limits / pitfalls (observed)
- Workday CXS: reachable from this host with `curl --compressed` + `Origin`/`Referer`/`User-Agent` headers. Verified 200 pairs: `bmo.wd3/External`, `td.wd3/TD_Bank_Careers`, `interac.wd3/interac`, `manulife.wd3/MFCJH_Jobs`, `cibc.wd3/search`. Space calls ≥ 6 s — repeated rapid calls return empty body (rate limit), retry after backoff. HTTP 422 = wrong `{site}` name, not an empty board.
- Adzuna: 503s after ~4 rapid queries; space calls ≥ 3 s.
- LinkedIn guest `seeMoreJobPostings`: 429s after ~4 rapid queries; space ~25 s between batches of 4. Guest detail pages readable in browser via `new_tab` + `innerText`; `web_extract` times out.
- Canadian gov / public sector: Radware-walled (`gojobs.gov.on.ca`, `jobs.gc.ca`) — do not retry; use Job Bank as proxy, trust only postings whose *title* names the platform.
- `postedOn: "Posted Today"` is not a Canada signal — always read the `externalPath` slug/country before counting a fresh hit.
- All commits for lessons-only changes use `[skip ci]` (pages.yml not triggered; live page stays on previous successful deploy).

## Action taken
- No jobs.json / README.md changes (nothing new to merge).
- This lessons file committed to `main` with `[skip ci]`.

# JOBLESSONS — 2026-11-25T09:00 EST (hourly Toronto SN/SF scan)

## Result
- **2 net-new verified fresh jobs** added to `jobs.json` + `README.md` + GitHub Pages:
  1. **Senior Sales Force Developer** — BMO — Toronto, ON (hybrid) — posted 2026-11-24 — Workday req **R260032445** — 3–5 yrs Salesforce Lightning (LWC, Apex, Aura, Flows, APIs), 2–3 yrs SF admin + SQL/SOQL/SOSL — closes 2026-12-24 — https://bmo.wd3.myworkdayjobs.com/External/job/Toronto-ON-CAN/Senior-Sales-Force-Developer_R260032445
  2. **Salesforce Developer** (body: Senior Salesforce Developer) — Dawn InfoTek Inc. — Toronto ON — posted 2026-11-24 — agency posting for a bank client, 6-month contract, CAD 80–100/hr — Apex/Visualforce/LWC/Aura, REST/SOAP integrations, Sales/Service Cloud — https://www.eluta.ca/spl/salesforce-developer-35e9676587de87fc4dc1919ec62a4d2a
- Board after: **5,654 rows** (1,208 ServiceNow / 4,328 Salesforce).

## Sources scanned & yield
| Source | Volume | Net-new |
|---|---|---|
| Eluta Toronto — `q=servicenow`, `q=salesforce` | 28 cards / 21 unique leads | 0 (Dawn SF was listed under q=salesforce; CGI/EY/IGM/Wipro/TD/BMO rows all boarded) |
| Eluta Toronto — `q=salesforce administrator` | 14 cards | 0 (Survalent, Lane Four, Benevity boarded; Merrithew older-than-fresh) |
| Eluta Toronto — `q=servicenow administrator` | 14 cards | 0 (CGI, BMO CMDB, TD, RSM Architect, Alimentiv all boarded) |
| Workday CXS — TD, BMO, CIBC, RBC, Manulife | ~40 SN/SF-titled reqs | 1 (BMO R260032445) |
| Workday CXS — Sun Life, Rogers, TELUS, Metrolinx, WSIB, Desjardins, Canada Life, CPPIB, OTPP, OMERS, NBC, Loblaw, Intact, UHN | 0 Toronto-metro SN/SF titles returned | 0 |
| ServiceNow official SmartRecruiters API | 973 postings / 26 Canada | 0 (Senior Systems Engineer JB0078172 + Principal Solution Architect JB0076386 already boarded; rest are sales/security) |
| Salesforce official Workday (wd12 External_Career_Site) | 13 ServiceNow reqs, no Toronto | 0 |
| Rogers careers RSS | 406 blocked this hour | 0 |
| LinkedIn guest — Toronto 24h ServiceNow | 429 rate-limited | covered by CI sweep |
| Ontario gojobs + federal jobs.gc.ca | no live dated Toronto SN/SF build req | 0 |
| Merrithew careers / Dawn InfoTek own site | cross-check | Merrithew not fresh; Dawn role not on own site (Eluta-only) |

## Lessons for future agents
1. **BMO's Workday title splits "Sales Force"** — R260032445 is *Senior Sales Force Developer*. A title regex on `salesforce`/`sales force` will find it, but Adzuna/LinkedIn mirrors were not yet indexing it and the 13:15Z CI snapshot missed it. Query `bmo.wd3.myworkdayjobs.com/wday/cxs/bmo/External/jobs` with `searchText=Salesforce` **and** `searchText=Servicenow` every hour; BMO publishes Toronto reqs at 00:00Z and they can take a day to reach aggregators.
2. **Eluta detail pages carry JSON-LD dates.** The `d_*.html` files have `"datePosted":"2026-11-24T…"` and sometimes `"validThrough"`; use those for an absolute posted date instead of the "1 day ago" label. Dawn's own site never listed the role, so Eluta was the only public route — fine for an agency-of-record posting, but label it as agency.
3. **Scarborough counts as Toronto.** Merrithew's SFMC Admin is Scarborough (a Toronto district), $75–85k hybrid, but posted **2026-11-05** (meta `Posted content`), i.e. 20 days old — held back from the fresh merge; add later only if the board needs backfill.
4. **LinkedIn guest API is 429 for this host most mornings.** One attempt is enough; the :15Z CI LinkedIn sweep already covers 24h Toronto. Don't burn retries on a shared IP.
5. **Bank Workday boards are current and small.** TD/BMO/CIBC/RBC/Manulife returned only boarded rows; the one new BMO req was a same-day publish. Sweep the remaining Canadian tenants once per hour but expect ~0.
6. **Interac's Workday now shows** `Senior Business Systems Analyst (ServiceNow)` (REQ-2351, already boarded via Adzuna 2026-11-18) and `Quality Engineering, Senior Specialist (ServiceNow Platform)` (REQ-2346, 30+ days, QE not build). Do not add QE/BA as fresh dev rows.
7. **Duplicate mirrors to keep ignoring:** RSM Canada "ServiceNow Architect" (5 Adzuna mirrors), MLSE "[C] Salesforce Engineer / Developer" (Workday JR000058 + 3 Adzuna mirrors), TCS "Salesforce Senior Developer" (jobs.ca + LinkedIn + Adzuna), CGI's 4 Toronto Salesforce rows. All boarded.
8. **Government channels still not automatable.** gojobs.gov.on.ca and jobs.gc.ca return stale/undated index pages; the only SN hit (House of Commons, gjobs.ca/2414863) closed April 2026. Keep checking weekly by hand, not hourly.
9. **Splice recipe verified again:** pull → insert compact one-line JSON row(s) after `"jobs": [` → bump `meta.total` and `meta.primaryCounts.<family>` from current values → `python tools/build_site.py` (reported 5,003 public rows, newest 2026-11-25) → README additions section under `<!-- DAILY-SCAN:END -->` → commit/push with `pull --rebase` retry.

## Partner / employer checks this hour
- BMO: **hit** — Senior Sales Force Developer R260032445 (Toronto hybrid, deadline 2026-12-24); R260032496 is the Chicago twin, do not add to Canada.
- Dawn InfoTek: **hit** — Salesforce Developer (agency, bank client); their ServiceNow Engineer/Technical Analyst remains boarded from Oct 23.
- CGI / EY / IGM-Mackenzie / Wipro / TD / Cognizant / Deloitte: all rows already boarded.
- RSM Canada (ServiceNow Architect), MLSE (Salesforce Engineer/Developer), Survalent, Lane Four, Benevity: boarded.
- Merrithew: older (Nov 5); Winobell ServiceNow Developer: Toronto but undated — check its own careers page next hour.
- Rogers: no ServiceNow; Bell: JS shell (Enterprise Solutions Architect II is an architect role, not build).

## Next-hour watchlist
- Winobell — ServiceNow Developer (Toronto, hybrid) — needs an absolute date + canonical apply URL from winobell.com.
- Merrithew — SFMC Administrator (Scarborough, Nov 5) — backfill candidate, not fresh.
- BMO External Workday straight after :05Z; also watch for the Toronto twin of any US-published SF req.
- Eluta `l=toronto` for `salesforce`/`servicenow` with 1-day filter remains the best residual agency channel; also try `l=mississauga` for GTA-hybrid roles whose body names Toronto.

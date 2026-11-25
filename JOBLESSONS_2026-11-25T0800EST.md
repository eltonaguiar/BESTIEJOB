# JOBLESSONS — 2026-11-25T08:00 EST (hourly Toronto SN/SF scan)

## Result
- **1 net-new verified fresh job** added to `jobs.json` + `README.md` + GitHub Pages:
  - **Salesforce Data Cloud Developer** — Wipro Limited — Toronto, Ontario — posting start 2026-11-18 — req 220407 — CAD 77,000–120,000 — 5–8 yrs — https://careers.wipro.com/job/Salesforce-Data-cloud-Developer/220407-en_US
  - Mandatory skill Salesforce Data 360 (Data Cloud); role is design/test/maintain client Salesforce solutions. Consultancy delivery role, so client-site expectations are unstated — flag for the applicant.
- Board after: **5,651 rows** (1,208 ServiceNow / 4,325 Salesforce).

## Sources scanned & yield
| Source | Volume | Net-new |
|---|---|---|
| LinkedIn guest — Toronto 24h, keywords ServiceNow + Salesforce (6 pages each) | 96 unique cards, 11 SN/SF title-hits | 0 (all boarded) |
| LinkedIn guest — Toronto 48h, "ServiceNow Developer", "Salesforce Developer", "ServiceNow Administrator", "Salesforce Administrator" | 36 unique cards, 23 title-hits | 0 |
| LinkedIn guest — Canada-wide 24h, ServiceNow + Salesforce | 40 unique cards, 19 hits | 0 |
| Eluta Toronto searches (servicenow, salesforce) | 20 leads | 1 (Wipro; 17 already boarded, 2 employer aliases) |
| Wipro careers direct (Phenom search + detail) | 2 ServiceNow rows, 1 Salesforce row | 1 (Data Cloud Developer) |
| Workday CXS — TD, BMO, CIBC, RBC, Moneris, Medcan, SSCTech, Interac, Manulife | ~150 reqs across 2 keywords each | 0 |
| Workday CXS — Sanofi (follow-up from 07:00 hit) | 32 Salesforce reqs, 10 ServiceNow | 0 (only the already-boarded Health Cloud Engineer is Canadian) |
| Rogers careers RSS (jobs.rogers.com/services/rss/job) | 0 ServiceNow, 17 Salesforce-keyword rows | 0 (all sales/AE roles) |
| Bell careers | JS shell, no listings | skipped |
| Job Bank HTML search | keyword ignored, random national results | unusable |
| CareerBeacon | Cloudflare challenge | skipped |

## Lessons for future agents
1. **LinkedIn Toronto is fully saturated at the 24h window.** 132 unique cards this hour produced 23 platform title-hits and every single one was already on the board (by URL, job id, or company+title). Do not spend more than two queries per track on LinkedIn before moving to direct employers.
2. **Eluta is the best residual discovery channel for agency/partner postings.** Its result page is a plain server-rendered HTML list (`div.organic-job`, `data-url="spl/..."`, employer + location + "N day(s) ago"). It surfaced the Wipro role that LinkedIn and the Workday sweep both missed. Treat it as a lead: resolve the issuer before publishing.
3. **Eluta detail pages do not expose the canonical apply URL to curl** (Apply is JS-gated; only the employer's homepage is in the HTML). Use the title + employer to find the role on the employer's own ATS. Wipro's Phenom site is JS-rendered for curl but works fine in a real browser: `https://careers.wipro.com/search/?q=<kw>&locationsearch=Toronto`, then `a[href*="/job/"]`.
4. **Workday `searchText` matches description bodies, not titles.** Searches return bankers, insurance advisors and sales managers that merely mention the platform. Always filter on `jobPostings[].title` with a strict regex before judging yield.
5. **Employer-family aliases are the main false "new" signal.** Edgewood Health Network = EHN Canada (same Toronto role); IGM Financial "Manager, HR Technology ServiceNow HRSD (14374)" = the Mackenzie Investments row already boarded. Check parent/subsidiary names before adding.
6. **Rogers' RSS is clean and reliable:** `https://jobs.rogers.com/services/rss/job/?locale=en_US&keywords=<kw>` returns items with `pubDate`; ServiceNow returns literally zero rows, and "salesforce" only matches sales roles. Two prior runs agree — Rogers is not a platform-hiring source right now.
7. **Bank Workday boards (TD/BMO/CIBC/RBC) are current and small.** Every ServiceNow/Salesforce req reachable at 13:00Z was already boarded (TD R_1521185, R_1509038, R_1515074; BMO R260030992/95, R260032445/96; RBC nCino + ServiceNow Discovery). No 429s this hour — the :00Z traffic window had cleared.
8. **CIBC's Workday tenant does not list its Salesforce "Consultant, Salesforce Development" rows** even though search engines index URL slugs for them (2621590, 2619703, last published Oct). Likely closed or on a different site — do not add from a search snippet alone.
9. **Sanofi follow-up paid off as a negative result:** all 32 Salesforce reqs are non-Canadian except the Health Cloud Engineer already added. Their Toronto digital hub posts through Workday (sanofi.wd3 / SanofiCareers) and is worth a weekly re-check, not hourly.
10. **Splice recipe still works on a CI-refreshed board:** `git reset --hard origin/main` (CI had advanced 2 commits and pruned ~41 "other" rows), insert the compact one-line row after `"jobs": [`, bump `meta.total` and `meta.primaryCounts.salesforce` from the *current* values, then rebuild.

## Partner / employer checks this hour
- Wipro (Global Elite SN partner, large SF practice): **hit** — Salesforce Data Cloud Developer, Toronto.
- CGI: 4 Salesforce + 2 ServiceNow Toronto rows on Eluta — all already boarded.
- EY: ServiceNow IRM Senior Consultant + bilingual GRC lead — already boarded.
- Cognizant: Data Cloud Developer, Senior SF Tech Lead, SF BA Manager — already boarded.
- Deloitte: ServiceNow/Salesforce Platform Senior Consultant — already boarded (LinkedIn).
- Rogers: 0 platform roles. Bell: JS shell. Government of Canada / Ontario: not reachable via simple search; Job Bank keyword search is broken for automation.
- Sanofi: no additional Canadian platform reqs.

## Next-hour watchlist
- Dawn InfoTek — "Salesforce Developer" (Toronto, Eluta 1 day ago): agency posting, canonical URL not yet found — try dawninfotek.com job board or LinkedIn company page.
- Wipro careers: re-query `salesforce` + `servicenow` with `locationsearch=Toronto` weekly; their requisitions post on their own Phenom board days before aggregators.
- Eluta `l=toronto` for salesforce/servicenow with a 1-day filter is now a standing source; also try `l=mississauga` for GTA-hybrid roles whose body names Toronto.
- Workday TD/BMO/CIBC/RBC straight after :05Z when the hourly CI has finished.

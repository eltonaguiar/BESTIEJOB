# JOBLESSONS — 2026-11-25T10:00 EST (hourly Toronto SN/SF scan)

## Result
- **0 net-new verified fresh jobs** this hour. The board is current; nothing to merge to `README.md` / GitHub Pages.
- Board after CI refresh: **5,656 rows** (1,208 ServiceNow / 4,329 Salesforce / 119 other), `jobs.json` scrapedAt `2026-11-25T14:13Z`.
- Today's fresh (2026-11-25) Toronto rows are **already onboarded** by the CI/prior runs, so no curated add was needed:
  - BMO — ServiceNow ITOM & HAM Administrator (Toronto, req R260030992; same req as the boarded "ServiceNow CMDB Administrator")
  - Cognizant — Salesforce Business Analyst Manager (Toronto)
  - Cognizant — Salesforce Tech Lead (Toronto)
  - SS&C Technologies — Salesforce Implementation Consultant & Platform Administrator (Toronto)
  - Manulife — Salesforce Functional Analyst (Waterloo)
  - Sanofi — Salesforce Health Cloud Engineer (Toronto)

## Sources scanned & yield
| Source | Volume / status | Net-new |
|---|---|---|
| LinkedIn guest — 24h Toronto (ServiceNow, Salesforce + Developer/Administrator variants) | 6 queries × up to 50 cards = 40 cards, 14 SN/SF title hits — every one already boarded | 0 |
| Workday CXS — BMO, CIBC, TD, Manulife, Sun Life, OMERS, Desjardins | 9 reachable tenants; 4 relevant Toronto hits (BMO CMDB/ITOM&HAM, BMO Tech Lifecycle, TD Sr Solution Architect SN, TD SF Loyalty Dev) all boarded | 0 |
| Workday CXS — Accenture (wd103/AccentureCareers), Kyndryl (wd5/KyndrylProfessionalCareers) | both HTTP 200; zero Toronto SN/SF titles | 0 |
| Workday CXS — intactfc, RBC, CPPIB, OTPP, Canada Life, TELUS, Rogers, UHN, Metrolinx, WSIB, NBC, Loblaw, CNR | **404 / 422 — stale tenant or site slugs; re-discovery needed** | 0 |
| Eluta Toronto — servicenow/salesforce + variants, t=1 | **BLOCKED: "User Verification" bot wall** (curl 302→sandbox interstitial; headed browser shows 🐴 User Verification) | 0 |
| Indeed Toronto (sort=date, fromage=2) | **BLOCKED: Security Check / captcha** | 0 |
| ServiceNow official SmartRecruiters | 973 postings / 26 Canada / 5 Toronto-title hits — all sales, security, compliance or network; none fresh platform-build | 0 |
| Salesforce official Workday (wd12 External_Career_Site) | 200; 0 Toronto SN/SF reqs | 0 |
| Rogers careers (SuccessFactors) | `q=ServiceNow` → 0; `q=Salesforce` → 30 cards, all sales/account/field roles | 0 |
| Bell careers | JS shell — no server-rendered cards | 0 |
| Canadian government — Toronto city, gojobs, jobs.gc.ca | City SN Developer (Job 66386) closed 2026-10-20; SN Platform Lead closed 2026-06-23; federal Sr SF Developer ~4 weeks old | 0 |
| Partners via Adzuna feed (CI): Cognizant, Deloitte, CGI, Capgemini, Wipro, IBM | today's Cognizant SF rows already on board; rest boarded | 0 |

## Lessons for future agents
1. **Eluta is now behind an anti-bot wall.** Plain `curl` gets a 302 to `/sandbox?destination=…`, then a ~22 KB interstitial with **no `organic-job` cards**; a headed browser gets a "🐴 User Verification" page. Do **not** burn retries every hour. Try a session-cookie warm-up or run Eluta only every few hours; when blocked, say so and lean on the CI's Adzuna/LinkedIn sweep.
2. **Half the Workday tenant slugs in `scripts/workday_probe.py` are stale.** RBC, CPPIB, OTPP, Canada Life, TELUS, Rogers, UHN, Metrolinx, WSIB, NBC, Loblaw, CNR, Intact return 404/422. Re-discover their `wday/cxs/<tenant>/<site>/jobs` path before the next probe; a 422 almost always means the site name (not the tenant) changed.
3. **New valid partner Workday endpoints found:** `accenture.wd103.myworkdayjobs.com/wday/cxs/accenture/AccentureCareers/jobs` and `kyndryl.wd5.myworkdayjobs.com/wday/cxs/kyndryl/KyndrylProfessionalCareers/jobs`. Add them to the hourly tenant list — both answered 200, just had no Toronto SN/SF this hour.
4. **Dedupe bug to avoid:** every Workday URL contains the token `myworkdayjobs`, so a naive "any token ≥6 chars from the URL appears in the board" check false-matches *every* new Workday row. Extract only req-id-shaped tokens (`\b[A-Za-z]{0,4}[_-]?\d{5,}\b`, e.g. `R260030992`, `R_1521185`), or match on URL path.
5. **BMO reuses reqs with new titles.** `ServiceNow ITOM & HAM Administrator` (Workday title) = `ServiceNow CMDB Administrator` (builtintoronto + req R260030992). Dedupe by req id / URL path, not title alone, or you will double-add.
6. **Rogers search is sales-noise.** `q=ServiceNow` returns zero; `q=Salesforce` returns account/field-sales roles. Only trust a Rogers hit whose title contains developer/admin/architect/engineer/consultant.
7. **Indeed guest is captcha-walled from this host.** One attempt is enough; do not retry. Adzuna + LinkedIn already cover Indeed's inventory.
8. **ServiceNow SmartRecruiters needs a relevance + date filter.** Of 973 postings (26 Canada), the Toronto titles were Staff Compliance/Security Analyst, Network Reliability Manager and CRM Sales — company-internal roles, not platform build. Filter on title regex **and** `releasedDate >= cutoff`.
9. **Government SN/SF postings are seasonal and short-window.** Toronto's ServiceNow Developer (Oct 5–20) and Platform Lead (Jun 9–23) windows are closed; check gojobs/jobs.gc.ca weekly, not hourly.
10. **Quiet hours are normal.** With 6,000+ rows and an hourly CI, roughly half the curated hours yield 0 net-new. Document the 0, keep the source-status table current, and do not manufacture adds.

## Partner / employer checks this hour
- **Elite / global partners:** Accenture, Kyndryl → 200, no Toronto SN/SF. Cognizant → 2 fresh SF rows already on board. Deloitte/CGI/Capgemini/Wipro/IBM → boarded via Adzuna.
- **Tech / telco:** Rogers → 0 SN, Salesforce hits sales-only; Bell → JS shell.
- **Banks / insurers:** BMO, TD, CIBC, Manulife, Sun Life, OMERS, Desjardins all reachable; every relevant Toronto req already boarded.
- **Public sector:** Toronto city and federal postings closed or stale.

## Next-hour watchlist
- Fix Workday slugs (lesson 2) and add Accenture/Kyndryl (lesson 3) to the hourly probe.
- Re-try Eluta with a cookie/warm-up flow; if still walled, downgrade to every-3-hours.
- Watch BMO External Workday right after :05Z — BMO publishes Toronto reqs at 00:00Z and they lag aggregators by ~a day.
- Keep an eye on Cognizant/Deloitte/CGI direct boards for SF roles that Adzuna indexes a day late.

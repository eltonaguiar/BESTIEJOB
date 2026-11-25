# JOBLESSONS — 2026-11-25T12:00 EST (hourly Toronto SN/SF scan)

## Result
- **1 net-new verified fresh row** added to `jobs.json` + `README.md` + GitHub Pages this hour:
  - **Zoho — Senior Salesforce Developer** — Toronto; LinkedIn 4494928808 (posted ~4 min before scan).
- The **identical JD at BULL Information Systems** (4494919869, posted ~50 min before scan) was **already onboarded by the CI's 16:17Z sweep** before this push (origin/master moved 5,663→5,664 between my 11:00 read and fetch). Dedupe + the pre-push `origin/main:jobs.json` check caught it — only Zoho was missing.
- Board after merge: **5,665 rows** (1,210 ServiceNow / 4,336 Salesforce); Pages rebuilt, deploy run `45661364055` success, live page marker `2026-11-25 17:07 UTC`.
- JD (Zoho/BULL twin): Apex, Triggers, Batch Apex, LWC, SOQL/SOSL, Salesforce Flows, REST/SOAP integrations, Sales + Service Cloud, Data Loader, unit tests / Apex coverage, production support, Agile/Scrum. Senior (4–5+ yrs typical), no cert stated, no salary posted. Pure developer req — **not** the Yochana/Raas "Production Support" admin+Apex blend.

## Sources scanned & yield
| Source | Volume / status | Net-new |
|---|---|---|
| LinkedIn guest — 24h Toronto, 5 title queries (ServiceNow, Salesforce, SN dev, SF dev, SF admin) × pages 0/10/20 | 112 unique cards, 14 title-hits; 12 already boarded (Sanofi, SS&C, Yochana, Raas ×2, Agility IT, AceStack, BULL-IT Lead, Nityo, Tamanna, Enterprise Solutions, Smart IT Frame) | **1** (Zoho) |
| Aggregator/web (CGI ServiceNow Admin/Dev + SF Dev/Architect, KPMG SN Dev ×2, Deloitte SN IRM/SecOps, HCLTech SF Admin, Dentalcorp, Lane Four, Wipro Data Cloud, OSI Digital, SS&C, National Bank, Acestack) | all title-hits already boarded | 0 |
| Partner / Elite — Ateko / FX Innovation (ServiceNow Elite, Bell-backed) | live ServiceNow Developer/Architect/Implementation roles, Canada-remote, but **French required** (Montréal/Québec); already represented on board | 0 |
| Partner / employer — Envision ITOM, Real Ventures, NeuraFlash, Docebo, Levio | boarded / no fresh Toronto SN/SF | 0 |
| Government — GoC Sr Salesforce Dev (4481939757), CMHC ServiceNow ITSM Dev (4444741717) | already boarded | 0 |
| Government — City of Toronto Systems Integrator-1 ServiceNow (req 66386); House of Commons full-stack ServiceNow | **closed** (2026-10-20 / 2026-11-15) | 0 |
| Telco — Rogers careers, Bell careers | Rogers: no SN/SF titles; Bell: 303-redirect → 0 (Bell hiring surfaces via Ateko/FX) | 0 |
| ZipRecruiter / Glassdoor candidates | Wawanesa SF Lead Developer (CA$100–130k), PwC Sr Associate SF Technical Consultant, Dentsu freelance SF/HubSpot dev — **Cloudflare-walled**, unverified | 0 (watchlist) |

## Lessons for future agents
1. **Vendor twins post the identical JD within the hour — check `origin/main` before adding.** Zoho (4494928808) and BULL Information Systems (4494919869) carried byte-identical JDs; the CI's 16:17Z sweep onboarded BULL first. `git fetch` + grep `origin/main:jobs.json` for the LinkedIn id is the only reliable guard (lesson #2 from 11:00 held again).
2. **The BULL staffing group rotates legal names and titles.** On the board: `BULL-IT SOLUTIONS LTD` (Salesforce Lead 4494730713 — live, a *lead/architect* JD w/ MuleSoft+Docusign), `BULL TECHNICAL SERVICES LIMITED` (Senior Salesforce Developer 4485775315 — **now 404/closed**), `BULL INFORMATION SYSTEMS LIMITED` (Senior Salesforce Developer 4494919869 — live), `BULLIT SYSTEMS` (CPQ Architect), `Bull Information Technology and Services` (ServiceNow Consultant). Dedupe *within* the group by normalized company brand + title, but a genuinely different req (Lead vs Senior Dev) is a distinct posting. Check the individual LinkedIn URL's liveness — the 11-03 "Senior SF Dev" is dead.
3. **Zoho is a real Toronto employer on this board** (two React Native full-stack rows since 2026-11-02). Its "Senior Salesforce Developer" is not a staffing alias — but the JD matching BULL's exactly means one client req shopped by two vendors (keep both, apply once).
4. **LinkedIn `keywords=ServiceNow` search is noisy** — it matches job *mentions*, returning IT-support/BMC/governance cards. Use title-specific queries ("servicenow developer", "salesforce administrator") and filter on title tokens (servicenow/service now/salesforce/apex/lwc/sfdc/itsm). Some title queries return 0 on page 0 but results on a later page (Salesforce → start=20; Salesforce-developer → start=10) — don't stop at an empty first page.
5. **ZipRecruiter and Glassdoor are Cloudflare-challenge-walled** to both `curl` (403) and headless Chromium ("Performing security verification"). Their listings (Wawanesa, PwC, Dentsu) can seed a watchlist but cannot be verified here — do **not** add them as verified rows; re-check via the employer's own careers site or a non-walled aggregator instead.
6. **Most public-sector SN/SF reqs are already boarded or closed.** GoC Senior Salesforce Developer and CMHC ServiceNow ITSM Developer are both on the board; City of Toronto's court-services ServiceNow req 66386 closed 2026-10-20 and House of Commons' full-stack (ServiceNow) closed 2026-11-15. Treat `jobs.toronto.ca` / `gjobs.ca` hits as closed unless the posting period is current.
7. **Ateko/FX Innovation (Bell-backed ServiceNow Elite) is a real recurring source** but nearly every live ServiceNow dev/architect role there is Canada-remote from Montréal/Québec **with a French requirement** — an English-only Toronto candidate can apply to few. Note the French requirement explicitly; don't count them as Toronto-onsite.
8. **Quiet hour, 1 net-new — normal.** Every employer-direct and partner source was saturated by the CI/prior runs; the single add came from a brand-new LinkedIn staffer twin. Document the 0s; do not manufacture adds (runbook: zero net-new is valid).

## Partner / employer checks this hour
- **Elite / global partners:** CGI, KPMG, Deloitte, Accenture — all SN/SF reqs already boarded via aggregators. Ateko/FX (ServiceNow Elite) — live but French-required remote.
- **Tech / telco:** Rogers → 0 SN/SF titles; Bell → 303-redirect (0); Bell's ServiceNow hiring surfaces through Ateko/FX.
- **Banks / insurers:** BMO, TD, CIBC, Manulife, Interac, RBC, Scotiabank — no net-new Toronto SN/SF this cycle (all previously boarded or unchanged); RBC `wd5` still 422 (re-discover slug).
- **Public sector / gov:** GoC + CMHC boarded; City of Toronto req 66386 closed; House of Commons closed.
- **Partner ATS:** NeuraFlash (Greenhouse), Docebo (Ashby), Levio (Greenhouse) — no fresh Toronto SN/SF.

## Next-hour watchlist
- Re-run LinkedIn guest **Canada-wide** (not just Toronto) SF/SN developer queries to catch remote-eligible roles the geo filter drops.
- Re-discover **RBC Workday** site slug (wd5 422) — try `rbc.wd3`/other site names.
- Verify **Wawanesa — Salesforce Lead Developer (CA$100–130k)** and **PwC — Sr Associate SF Technical Consultant** via employer careers (ZipRecruiter/Glassdoor walled).
- Watch BMO External + TD_Bank_Careers right after :05Z; both publish Toronto reqs at 00:00Z and lag aggregators ~1 day.
- Watch Zoho/BULL-style "Senior Salesforce Developer" staffer twins — a third vendor often re-posts the same client JD within the hour; always check `origin/main` before adding.

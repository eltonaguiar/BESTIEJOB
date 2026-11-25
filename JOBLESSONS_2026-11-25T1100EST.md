# JOBLESSONS — 2026-11-25T11:00 EST (hourly Toronto SN/SF scan)

## Result
- **1 net-new verified fresh row** added to `jobs.json` + `README.md` + GitHub Pages this hour:
  - **Yochana — Salesforce Production Support (Platform Admin + Apex/LWC)** — Toronto; LinkedIn 4494915808.
- The **twin of the same client req at Raas Infotek** (4494644519 + 4494643540) was **already onboarded by the CI's 15:44Z fresh-CA sweep**, so it was NOT re-added (dedupe caught it).
- Board after merge: **5,663 rows** (1,210 ServiceNow / 4,335 Salesforce); site rebuilt to ~5,000 rendered cards, newest 2026-11-25.
- The req is a genuine **Salesforce Admin + Developer** role despite the "Production Support" title: administer users/profiles/permission sets/sharing; objects/fields/Flow/reports; Data Loader/Workbench/SOQL; production support; **Apex classes/triggers/LWC/Apex test classes**; deployments. SF Admin cert preferred; **Platform Developer I an asset**. Sales Cloud + FSC. 4–5 yrs, mid-senior.

## Sources scanned & yield
| Source | Volume / status | Net-new |
|---|---|---|
| Adzuna CA — ServiceNow/Salesforce + both admin variants, Toronto, `max_days_old=3` | 35 / 89 / 6 / 4 rows; 15 platform hits — 5 ServiceNow-Inc. sales/pre-sales (exclude), Cognizant SF BA/Tech Lead + RSM CPQ Architect + ServiceNow Cyber Consultant all boarded | 0 |
| Adzuna CA — ServiceNow/Salesforce Developer, Canada-wide, `max_days_old=2` | 1 / 14 rows; the 5 real SF rows boarded; rest sales/SailPoint/Marketing-Cloud noise | 0 |
| Workday CXS — BMO, TD, CIBC, Manulife, Interac (ServiceNow + Salesforce, "Toronto") | **all 200 (no 429 at 16:00Z)**; fresh hits (BMO ServiceNow ITOM&HAM R260030992, TD SF Loyalty R_1509038, Manulife SF Functional Analyst) all already boarded by the 09:13Z scan | 0 |
| Workday CXS — RBC (`rbc.wd5`) | HTTP **422** — wrong site slug; re-discover | 0 |
| ServiceNow official SmartRecruiters (`country=ca`) | 973 postings / 26 Canada — all sales, SRE, security, staff-eng; no fresh platform build | 0 |
| Salesforce official Workday wd12 | 43 Toronto rows, all Account Exec / GTM / CSM / product — zero Platform Admin/Dev I | 0 |
| Accenture Workday wd103 | 200; contact-centre/AI/CCaaS sellers only — no SN/SF build | 0 |
| Rogers careers (date-sorted) | 26 `<tr>` rows, zero SN/SF titles | 0 |
| Scotiabank Phenom (servicenow + salesforce, date-sorted) | 11 / 25 rows; only "ServiceNow Developer" is **Bogotá**; SF rows are generic banking | 0 |
| Bell careers | HTTP **303** redirect, empty body — treat as 0 | 0 |
| Job Bank (servicenow/salesforce, Toronto) | 25 title spans each, all generic (LAN admin, food-delivery driver…) | 0 |
| Partner ATS — NeuraFlash (Greenhouse), Docebo (Ashby), Levio (Greenhouse) | NeuraFlash 21 Canada roles all boarded (new = AWS architect); Docebo "Senior Salesforce Developer" boarded; Levio no fresh Toronto SN/SF | 0 |
| LinkedIn guest — 24h Toronto (ServiceNow, Salesforce, SN Developer, SF Administrator) | 87 unique cards, 18 boarded; 3 platform-titled new → **1 kept (Yochana)**, 1 vendor twin already boarded (Raas), 1 typo-mirror (BULL-IT) excluded | **1** |
| Government — gojobs / jobs.gc.ca | Radware-walled (known); none surfaced | 0 |

## Lessons for future agents
1. **LinkedIn guest via the browser DOM still works — extract the id from `data-entity-urn`.** `goto_url` on `jobs-guest/jobs/api/seeMoreJobPostings/search?…&f_TPR=r86400&start=N` returns `li` cards; read `data-entity-urn="urn:li:jobPosting:<id>"` (clean) plus `a[href*="/jobs/view/"]`. **Do not** build the id regex inside a plain (non-raw) Python triple-quoted string — `\b` becomes a backspace char and silently corrupts the JS so `querySelectorAll` yields 0 cards. Use `data-entity-urn` or a raw string. `start=0,10,20,30` genuinely pages here (unlike `/jobs/search` page-2 re-serve).
2. **The CI fresh-CA sweep runs ~15:44Z and can onboard your candidates before you push.** Both Raas rows were already in `origin/main` when I went to push. **Always `git fetch` + check `origin/main:jobs.json` for your candidate ids BEFORE adding**, then rebuild on top of origin (`git reset --hard origin/main` + re-splice only the truly missing rows). Do not fight a rebase on generated JSON.
3. **Workday 429s are not guaranteed at :00Z.** At 16:00Z all five Canadian tenants (BMO/TD/CIBC/Manulife/Interac) answered 200 with 1 s spacing — the "429 every board" note is intermittent; a post-:00Z probe is worth one attempt.
4. **"Posted Today/Yesterday" Workday hits are almost always already boarded by the CI's earlier :13Z scan.** BMO R260030992 and TD R_1509038 read "Posted Today/Yesterday" but were in `jobs.json` (added 09:13Z). Match by **req id / URL path** before treating a fresh `postedOn` as net-new.
5. **Generic "Production Support" titles hide real Salesforce Admin + Developer roles.** The Yochana/Raas JD is squarely admin config + Apex/LWC + test classes + deployments. Body-check every support-titled card before discarding.
6. **Vendor twins from different firms are distinct postings — keep both.** Yochana and Raas Infotek posted the identical client JD; the user applies separately. But dedupe **within** one firm's two near-identical posts (Raas 4494644519 vs 4494643540) to one.
7. **A repost with a typo is still a mirror.** BULL-IT "Saleforce Lead" (4494929271, misspelled) = the already-boarded "Salesforce Lead" (4494730713). Dedupe by company + normalized title even when the vendor re-posts under a typo'd title.
8. **BMC Helix/Remedy is NOT ServiceNow.** "Specialized IT Consultant" at Russell Tobin and Akkodis are BMC Helix ITSM build roles (Rev ARS, Smart IT, DWP) — exclude. And an "ITSM consultant" that uses ServiceNow *operationally* (Collabera → CPP Investments, incident/problem/change) is a process analyst, not platform admin/build — exclude per the protocol's "operational capacity" rule.
9. **Salesforce's own board (wd12) hires no Platform Admin/Dev in Toronto** — all sales/GTM/CSM. ServiceNow's own board is all sales/SRE/security. Platform build work lives at banks, integrators and staffing firms, not the vendors.
10. **Bell careers 303-redirects** (empty body) — treat as 0. Bell's real ServiceNow hiring surfaces as **Ateko (backed by Bell Canada) / FX Innovation** on LinkedIn, not `jobs.bell.ca`.
11. **Adzuna Canada-wide developer queries are dominated by noise** ("Outside Sales (Design Consultant)", SailPoint, Marketing-Cloud email devs). Filter hard on title tokens (salesforce/servicenow/apex/lwc/cpq/admin/dev) before treating a row as a candidate.
12. **Quiet hours remain normal (~half).** One net-new came from a LinkedIn staffer twin; every employer-direct and vendor-direct source was already saturated by the CI/prior runs. Document the 0s, keep this table current, don't manufacture adds.

## Partner / employer checks this hour
- **Elite / global partners:** Accenture (wd103) → 200, no SN/SF build; NeuraFlash → Salesforce architect roles all boarded. Cognizant/Deloitte/CGI/Wipro → boarded via Adzuna.
- **Tech / telco:** Rogers → 0 SN/SF; Bell → 303; Scotiabank → only Bogotá SN Dev; ServiceNow/Salesforce vendors → sales-only.
- **Banks / insurers:** BMO, TD, CIBC, Manulife, Interac reachable — every relevant Toronto req already boarded by 09:13Z; RBC `wd5` slug is wrong (422) — re-discover.
- **Public sector / gov:** Ontario gojobs + jobs.gc.ca Radware-walled; Job Bank pure title noise.

## Next-hour watchlist
- Re-discover RBC Workday site slug (try `rbc.wd3`/other site names) — `wd5` is dead (422).
- Re-run LinkedIn guest on **Canada-wide** remote SN/SF developer queries (not just Toronto) to catch remote-eligible roles the geo filter drops.
- Keep watching BMO External + TD_Bank_Careers right after :05Z; both publish Toronto reqs at 00:00Z and lag aggregators ~1 day.
- Watch Raas/Yochana-style "Production Support" staffer twins — if the client req is real, a third vendor often posts it within the hour; check `origin/main` before adding.

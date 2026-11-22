# JOBLESSONS_2026-11-22T0600EST

Hourly Toronto ServiceNow / Salesforce scan — Sunday 2026-11-22 06:00 EST (UTC-05).
Board: github.com/eltonaguiar/BESTIEJOB (main) · pages: eltonaguiar.github.io/BESTIEJOB/

## Result this run
- Fresh verified jobs merged: **0** (none qualified)
- Board state unchanged: 5,596 jobs (1,173 ServiceNow / 4,266 Salesforce), last hourly scan 2026-11-22T09:11Z (04:11 EST) — success.
- GitHub Pages: last deploy **success** at 2026-11-22T10:37Z (05:37 EST), run 45013312745 — live site is current. No redeploy needed (nothing new to publish).
- Commit: none (nothing to merge).

## Sources scanned
| Source | Query/scope | Postings found | New vs board | Verdict |
|---|---|---|---|---|
| ServiceNow Inc careers (SmartRecruiters API) | country == ca, all pages | 26 | 0 | All already on board (incl. Senior Site Reliability Engineer, Toronto, JB0076846 — already present at jobs.json index ~1848). Mostly sales/exec/security; not platform build/admin. |
| Salesforce careers (Workday cxs API) | searchText=Toronto, offsets 0/20/40 | 44 | 26 new | 18 already on board. The 26 new are sales/corporate (Account Executive, AE Tableau/MuleSoft/Informatica, Partner Sales, BDR, recruiters, product/manager) — none are Salesforce Platform Administrator / Platform Developer I / platform-build titles. Skipped per board focus. |
| Web search (Indeed/LinkedIn/Glassdoor) | "ServiceNow jobs Toronto", "Salesforce jobs Toronto", Rogers/Bell/govt variants | ~10 candidates | ~10 not on dedupe key | Could not individually verify (Indeed/Glassdoor/LinkedIn behind bot protection/clickthrough; Glassdoor Cloudflare "Just a moment"). Several were near-dupes of existing entries under spelling variants (e.g. Moneris "Principle" vs "Principal" Salesforce Developer). Per quality gate, unverified postings are NOT added. |

## Dedupe method
Key = `company.lower() | title.lower()` (case-insensitive), compared against jobs.json and README.md. Near-dupe spelling variants are NOT caught by exact-key dedupe — reviewed manually.

## Partner / Elite / sponsor / target-employer sweep
No fresh Toronto ServiceNow/Salesforce platform vacancies beyond what's already on the board:
- Ateko (Bell-backed ServiceNow partner): careers route to FX Innovation / ADP; no current vacancy listed.
- Pentio (Toronto Select partner): partner profile only, no careers path / vacancy.
- Fujitsu (Elite implementation): partner profile only — no vacancy.
- NewRocket / Lane Four / Slalom: no fresh Toronto platform requisition this run.
- ServiceNow Inc own careers (Ontario): 22 open Toronto roles but almost all sales executives, security engineers, Canada Protected B SREs — not platform build/admin. Board rule: skip vendor sales/exec roles.
- Rogers (jobs.rogers.com, SuccessFactors): surface roles were retail/sales, no ServiceNow/Salesforce platform posting.
- Bell (jobs.bell.ca): ignores ?q= search; no direct ServiceNow/Salesforce platform vacancy surfaced. (Bell-backed platform arm Ateko covered above.)

## Observed failure
- Hourly Job Scan run 45001849967 (2026-11-22T08:14Z) concluded **failure**. Adjacent scans (09:11Z) and pages deploys succeeded. Worth re-checking next hour if the 08:14Z scan's feed gap matters.

## Pattern / lesson for future agents
1. ServiceNow Inc and Salesforce Inc career sites mostly publish sales/corporate requisitions, not platform admin/dev roles — the useful "ServiceNow/Salesforce jobs" for this board come via LinkedIn/Adzuna/Indeed feeds, which the automated hourly scan already covers.
2. ServiceNow/Salesforce partners and Elite partners in Canada (Ateko, Pentio, Fujitsu, NewRocket, Lane Four, Slalom) rarely list public platform vacancies; record the partner portal, not a job, unless a requisition is live.
3. Canadian government / Rogers / Bell surface few-to-no ServiceNow/Salesforce platform postings through their public career search; go through partner staffing (Ateko/FX Innovation for Bell) instead of direct career pages.
4. Always re-dedupe against the live jobs.json right before inserting (a stale dedupe_keys snapshot caused a near-duplicate insert this run — caught and reverted, board stayed at 5,596).
5. Indeed/Glassdoor/LinkedIn job pages are bot-protected in this environment; treat search snippets as leads only, not verified postings.

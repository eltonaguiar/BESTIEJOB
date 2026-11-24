# JOBLESSONS_2026-11-24T0900EST

Hourly Toronto ServiceNow / Salesforce platform job scan, 2026-11-24 09:00 EST (America/Toronto). Cron run against github.com/eltonaguiar/BESTIEJOB main branch.

## Result: 1 net-new verified job merged

| Posted | Role | Company | Location | Source |
|---|---|---|---|---|
| 2026-11-24* | Salesforce Developer | Scotiabank | Toronto, Ontario, Canada | linkedin |

Requisition 265640, Salesforce GWMT Centre of Excellence: Apex, Visualforce, Lightning components, CI/CD (Azure DevOps, Metadata API) — genuine platform build work, in scope. LinkedIn page confirmed live (134 applicants; listing states "3 weeks ago", no absolute date, so discovery date 2026-11-24 is shown asterisked per board policy). Deduped by URL against jobs.json, README.md and APPLIED.md — req 265640 not previously on the board (3 other Scotiabank Salesforce rows exist under different reqs).

Merged as section "Verified fresh additions — hourly scan 2026-11-24T09:00EST" in README.md, commit ac548631, pushed to origin/main. GitHub Pages redeployed (workflow run 45413383347, success); live board at eltonaguiar.github.io/BESTIEJOB/ shows 4974 postings, data stamped 2026-11-24 14:24 UTC, and jobs-data.json contains the new row.

## Liveness conflict to reconcile

An earlier board entry recorded Scotiabank Salesforce Developer JR265640 as closed ("not accepting any further applicants") from an employer-direct check. This cycle's LinkedIn check shows the req live with 134 applicants. Conflicting evidence — retained with a note in the section; the user should reconcile against careers.scotiabank.com before applying.

## Search coverage this cycle

Employer-direct checks returned NO other fresh live ServiceNow or Salesforce roles:

- Rogers (jobs.rogers.com Technology): no platform roles
- Bell (ServiceNow System Administrator req considered only): no fresh live platform role; Atego/FX Innovation portals not enumerable from this host
- TD / BMO / CIBC / Manulife Workday CXS: no fresh platform roles
- ServiceNow Careers (careers.servicenow.com): Cloudflare bot verification blocked this host
- Cognizant Careers: Cloudflare bot verification blocked this host
- CGI Careers: homepage loads, job listing is JS-driven, not enumerable
- Government of Canada Job Bank "ServiceNow" + Toronto: 27 results — keyword noise only (cloud developer, cybersecurity consultant, business consultant); no fresh ServiceNow platform roles. Blue Mantis (Nov 20) and Source Code (Nov 8) already on the board.

LinkedIn guest access from this host: roughly half of candidate posting URLs soft-404 ("Page not found" after a language-selection wall) or hit a language wall with no job content. Only the Scotiabank page rendered full detail. Search snippets (title/employer/location/relative age) are NOT sufficient evidence under the runbook's verification rules, so ~9 Toronto-linked LinkedIn leads (GlobalVariable, EQ Bank x2, Robertson, CGI, Hays, Insight Global x2, iVedha) were found via search but NOT verified and NOT merged.

## Patterns / lessons for future agents

1. **Dedup by URL catches exact duplicates, not mirror requisitions.** The same requisition under a LinkedIn URL and an employer ATS URL are different keys — check company + title + req id before treating a "NEW" URL as a genuinely new vacancy (e.g. Cognizant nCino Developer already on the board via careers.cognizant.com surfaced again under a LinkedIn URL this cycle).
2. **Employer careers pages are increasingly blocked from unattended hosts.** ServiceNow, Cognizant and Workday CXS tenants returned Cloudflare bot walls; Job Bank and LinkedIn guest pages are the most reliable public surfaces, but LinkedIn guest job detail is flaky (language wall / soft-404 on ~50% of posting URLs). Plan verification around what actually loads, not what search snippets promise.
3. **Job Bank keyword searches are noisy for "ServiceNow"** — "service now" as two words matches non-platform roles (cloud/cybersecurity/business consulting). Always read duties before merging; platform + build action required (Script Includes / Flow Designer / Apex / LWC etc.).
4. **Relative posting dates ("3 weeks ago", "2 days ago") conflict across mirrors.** Search snippets and LinkedIn pages disagreed on the Scotiabank req age (2 days ago vs 3 weeks ago). Never back-calculate; record the literal source clock and flag conflicts (runbook §5).
5. **Commit hygiene:** README.md edits trigger the Pages deploy (pages.yml watches README.md) — do NOT add [skip ci] when the page must refresh. Pushes to main collide with the hourly CI scan (concurrency group bestiejob-main-write); rebase + retry on rejection. jobs.json showed a UU rebase conflict this cycle even though this run only touched README.md — resolve by checking out HEAD's jobs.json (CI feed is authoritative).
6. **One verified job is still a valid run.** Zero new verified jobs is a valid result; an unavailable source is not a zero. Don't pad the board with search-lead-only rows.

## Next cycle suggestions

- Retry employer-direct portals from a different egress (or via the browser with cookies) for Rogers/Bell/TD/BMO/CIBC/Manulife/ServiceNow/Cognizant — these are the named Elite Partners / technical employers and keep yielding roles when accessible.
- Re-check the ~9 LinkedIn search leads that couldn't be verified this cycle; try their employer ATS mirrors directly.
- Watch for ServiceNow World Forum Toronto 2026 sponsor follow-ups (Ateko, Cognizant, NewRocket, Pentio) and Salesforce World Tour Toronto sponsors (Lane Four, Slalom, Ateko, CloudFulcrum) for partner-derived requisitions.

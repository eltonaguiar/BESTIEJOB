# JOBLESSONS_2026-11-22T2200EST

Hourly Toronto ServiceNow / Salesforce job scan — Sunday 2026-11-22, run 22:00 EST (03:00 UTC 2026-11-23).

## Result this cycle
+1 verified fresh job added to the board (commit c40a731, main):
- ServiceNow Administrator/Developer — Leading Talent — Toronto, ON (hybrid) — posted 2026-11-19, expires 2026-12-19 — CSA + CAD mandatory — employer-direct via leadingtalent.ca/jobs/servicenow-administratordeveloper-in-toronto-ontario-ca-2/

jobs.json: 5600 → 5601 rows (servicenow 1192 → 1193). Site rebuilt: public/jobs-data.json 4,932 jobs (SN 852 / SF 923). Live page verified via curl to https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json — the Leading Talent row is present (source leadingtalent.ca, verified "Employer board", toronto: true).
Deploy: pages.yml run 45105224864 → success; live page matches repo.

## Sources checked this cycle
| Source | Query | Fresh genuine SN/SF found | Notes |
|---|---|---|---|
| Adzuna API (ca) | servicenow × Toronto/Ontario, salesforce × Toronto/Ontario, max_days_old=3 | 0 net-new | 44/53/88/145 results; every platform-title hit already on board (URL + company+title dedupe). Feed saturated this cycle. |
| LinkedIn guest (browser, f_TPR=r86400) | Salesforce Toronto | 0 net-new | 60 cards, mostly sales roles; INNOVA Specialist, Deloitte Director, Apex Systems BSA already on board. |
| LinkedIn guest (browser, f_TPR=r86400) | ServiceNow Toronto | 0 | Returned 0 cards twice incl. after 3 scroll steps — known intermittent wall, query walled not empty; retry later. |
| Workday CXS (curl --compressed + UA) | bmo/td/cibc/manulife/interac/salesforce/accenture × SN & SF | 0 fresh | Needs browser User-Agent or returns HTTP 400. BMO freshest req 7 days old (ServiceNow CMDB Administrator). CI hourly pass carries Workday; manual probe low yield this hour. |
| Rogers (jobs.rogers.com) | Phenom board | 0 | Server-side shell, zero job rows; rely on LinkedIn/Adzuna for Rogers. |
| Bell (jobs.bell.ca) | servicenow/salesforce | 0 | Zero reqs (shows (0) in browser); re-check weekly, not hourly. |
| Government (gojobs.gc.on.ca / jobs.gc.ca) | — | 0 | Radware captcha wall; Job Bank is the proxy — trust only postings whose *title* names the platform. |

## Dedupe dispositions (verified, not added)
- Interac "Technical Service Now, Lead" (4126302101) — already on board.
- Cognizant "ServiceNow Solution Architect" (4212847006) — LinkedIn page 404, treat as closed.
- KPMG "Service Now Developer" Vaughan (4381942370) — 1 week old, outside today/yesterday freshness window.
- iCapital "Salesforce Administrator AVP" (4472203067) — LinkedIn detail served login-wall shell; unverifiable, skip (never infer platform from card title alone).
- KORT Payments "Salesforce Administrator" (4461535381) — LinkedIn page 404, closed.
- SS&C "Salesforce Implementation Consultant & Platform Administrator" — already on board.
- Rogers "Lead Management Operations" (4486372328) — already on board (matched SF keyword only).

## Patterns / lessons for future agents
1. Adzuna demo keys (app_id=54ce986e, app_key=db851f299e966c0a2a72af525dce6199) still work; param is `content-type` not `content_type`; results cap at 50/page; sort_by=date + max_days_old=3 is the freshness oracle. When the feed is saturated (0 net-new URLs), new rows come only from generic-titled roles needing body checks — expensive, low yield.
2. LinkedIn guest search cards are readable without login (new_tab → read `li a[href*="/jobs/view/"]`). ServiceNow queries intermittently return 0/walled — retry once after several minutes with scroll steps. Detail pages intermittently wall (`h1: Join LinkedIn` / shell) — skip those candidates rather than infer.
3. Workday CXS direct POST needs a browser User-Agent header, else HTTP 400 with empty message; `postedOn: "Posted Today"` is not a Canada signal — read the /job/<City>/ slug. Don't probe at :00Z (CI concurrent → 429s persist past :00Z).
4. Dedupe on normalized URL (strip query/trailing slash) + company+title fuzzy; vendor twins (staffing firms advertising same req) are distinct and both kept. Rogers/Bell/gov portals are not reliable hourly sources.
5. Commit discipline: jobs.json + README.md + public/* together (page serves only committed public files); push without [skip ci] so pages.yml deploys; poll the run and verify live jobs-data.json carries the URL. Lessons-only commits: [skip ci].

## What to try next cycle
- Retry LinkedIn ServiceNow Toronto guest search (was walled this cycle).
- Body-check generic-titled hits from Adzuna/LinkedIn (e.g., "Business Analyst", "Project Manager") where the search matched servicenow/salesforce — platform roles hide under generic titles.
- Check builtin.com Toronto ServiceNow/Salesforce (server-rendered, flags removed postings in snippet).
- Re-check Rogers/Bell weekly, not hourly.

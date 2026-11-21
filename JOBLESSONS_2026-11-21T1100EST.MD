# JOBLESSONS_2026-11-21T1100EST — BESTIEJOB hourly scan (Toronto ServiceNow / Salesforce)

**Run:** 2026-11-21 11:00 EST (UTC-05) · cron hourly job · repo: eltonaguiar/BESTIEJOB (main) · no changes committed (0 net-new)

## Result
- **0 net-new verified jobs merged.** 14 candidates surfaced → 2 URL-new vs jobs.json → both collapsed to company+title twins of rows already tracked under LinkedIn URLs → skipped. No jobs.json/README/public changes, no push, no Pages redeploy needed.

## Candidates checked (all deduped, none added)

| Source | Candidate | Status | Reason |
|---|---|---|---|
| Adzuna `servicenow` Toronto p1 | Blue Mantis — Sr ServiceNow Business Process Consultant — Toronto (adzuna 5974233718, posted 2026-11-21T10:20Z) | SKIPPED | Twin of `linkedin:...sr-servicenow-business-process-consultant-at-blue-mantis-4492804605` already in jobs.json (postedDate 2026-11-20, Toronto) |
| Adzuna `salesforce` Toronto p1 | Novartis — SFMC Manager — Toronto (adzuna 5973939535, posted 2026-11-21T05:09Z) | SKIPPED | Twin of `linkedin:...sfmc-manager-at-novartis-4491648837` already in jobs.json (postedDate 2026-11-19, Toronto) |
| LinkedIn guest `ServiceNow` Toronto past-24h | Envision Technology — ServiceNow ITOM Developer (4492816283) | ALREADY ON BOARD | Captured by today's earlier scan (scrapedAt 2026-11-21T14:10Z) |
| Adzuna p1/p2 | vTech PM ServiceNow, Amicis SN BA twin, Mackenzie HR Tech & ServiceNow HRSD, TD Senior SA ServiceNow | ALREADY ON BOARD | Exact URLs in jobs.json |
| Adzuna p1/p2 | Flexstaf SF Revenue Cloud Architect, CGI SF BA, CGI SF Dev, Serefin SF DevOps, TD nCino/SF SWE, Celestica Intern SF Dev 1 | ALREADY ON BOARD | Exact URLs in jobs.json |
| Workday CXS | BMO (ServiceNow CMDB Administrator, Tech Lifecycle Analyst — 9 days old), TD (SF Data 360 — 8 days old) | NOT FRESH | Outside today/yesterday window; likely already tracked |
| Scotiabank Phenom | ServiceNow Developer hit = Bogota, Colombia; Salesforce = banking roles | OUT OF SCOPE | Not Toronto/Canada platform roles |
| Dice | 30 cards/query but US-only (clearances, W2, no location field) despite `location=Toronto` | NOT CANADA-RELEVANT | Dice ignores the Toronto geo param |

## Sources scanned this run
- Adzuna API (app_id 54ce986e): `servicenow` + `salesforce`, `where=Toronto`, `max_days_old=3`, `sort_by=date`, pages 1–2 (59 SN / 119 SF)
- Workday CXS via `curl --compressed`: bmo.wd3/External, td.wd3/TD_Bank_Careers, searchText ServiceNow & salesforce (HTTP 200 on all; spaced 9s to avoid :00Z 429s)
- LinkedIn guest search via browser (`new_tab`, `f_TPR=r86400`, `sortBy=DD`): 60 ServiceNow cards, Toronto
- Dice.com (curl): 30 cards/query, US roles only
- Scotiabank Phenom date-sortable search: servicenow + salesforce
- Known-dead/weekly-only (not retried hourly): Rogers Phenom (shell), Bell (0 reqs), gojobs.gov.on.ca / jobs.gc.ca (Radware-walled)

## Lessons for future agents
1. **Adzuna URL-new is not role-new.** Adzuna re-issues the same role under a new `details/<id>` (e.g. Amicis 5972002660 → 5972983023). Always grep `jobs.json` for company+title and check `alternates` before adding; skip if the role is already tracked under any URL (LinkedIn twin included).
2. **LinkedIn guest search works from the browser, not `fetch`.** `new_tab` on `linkedin.com/jobs/search?keywords=...&f_TPR=r86400` returns ~60 cards/query; read `li a[href*="/jobs/view/"]`. Detail pages intermittently serve the authwall — retry once, else skip as unverified.
3. **Workday CXS is reachable from this host** with `Content-Type`/`Accept`/`Origin` headers, `--compressed`, and the full `{tenant}.wd{N}.myworkdayjobs.com` host. Do NOT send `Referer` (empties the body). 429s hit at :00Z — space calls ≥8s and retry 3–4 minutes later; "Posted Today" still needs the `/job/<City>/` slug read for country.
4. **Dice is not a Canada source** — it ignores the Toronto param and returns US clearance/W2 roles; cards carry no location. Skip for the Toronto board.
5. **0 net-new is a normal hourly outcome.** The CI scan (10:00Z/~05:00 EST) and today's earlier local scan already captured today's fresh roles (EY IRM ×4, Envision ITOM, Blue Mantis via LinkedIn). Do not force rows into the board to "have something to add."
6. **Rogers / Bell / Canadian government portals are weekly, not hourly:** Rogers Phenom = shell; Bell = genuinely zero; gojobs.gov.on.ca/jobs.gc.ca = Radware-walled. Use Job Bank as proxy, trusting only title-named-platform hits.

## Verification
- Live site health: `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` HTTP 200, 5,059 jobs (matches repo feed scale); sample row carries today's EY ServiceNow IRM role — the deployed page is current.
- jobs.json: 5,556 rows (SN 1,190 / SF 4,260), scrapedAt 2026-11-21T14:10Z — no deltas this run.

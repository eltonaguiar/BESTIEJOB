# JOBLESSONS_2026-11-23T0900EST

Hourly Toronto ServiceNow / Salesforce job scan — Monday 2026-11-23 09:00 EST (14:00 UTC). BESTIEJOB board: github.com/eltonaguiar/BESTIEJOB.

## Result

1 net-new verified job added to the board; 0 new ServiceNow jobs.

| Posted | Role | Company | Location | Source |
|---|---|---|---|---|
| 2026-11-18 | Salesforce Administrator / SFMC / Natural Health / Hybrid in Toronto | White Bay | Toronto, ON | jobs.ca search index |

Added to README.md `### Salesforce jobs` table (893 -> 894 rows) and to jobs.json (5639 -> 5640 jobs). Public site rebuilt via `tools/build_site.py` (4944 deduped jobs; built 2026-11-23 14:11 UTC).

## What was scanned

- ServiceNow SmartRecruiters API (all pages, country=ca, releasedDate >= 2026-11-16): every Canada tech requisition already on the board; sales requisitions (Moveworks / Cyber / CPQ account execs) excluded by board's sales-role filter. No new ServiceNow adds.
- Web search: ServiceNow + Salesforce, Toronto / Canada, November 2026. Nearly every candidate URL was already on the board (dedupe key: normalised URL; title+company cross-check).
- Near-dupes skipped (same role already on board under a different URL/date):
  - Dentalcorp Salesforce Administrator/Developer — on board since 2026-11-16 (direct dentalcorp.com URL); surfaced again via revopsroles aggregator ("listed about 8 hours ago"). Skipped.
  - HCLTech Salesforce Administrator — on board since 2026-11-16 (LinkedIn 4490676918); jobs.ca URL is a duplicate listing. Skipped.
  - EQ Bank / Sun Life / J&M Group / Payments Canada — same roles already on board (older dates).
- Zaelab ServiceNow FSM Architect (linkedin 4434135469, "2 days ago"): LinkedIn returned HTTP 404 — posting expired/removed. Skipped. Do not re-add without a live detail.
- Rogers careers: 0 platform roles (only management/financial/data). Bell / Ateko (backed by Bell): ServiceNow and Salesforce roles already on board (2026-11-19 to 11-20). Canadian government / Payments Canada / Job Bank: already covered, nothing fresh.
- Salesforce Workday CXS: unreachable (HTTP 000 / 422 on bmo/td/cibc/manulife probes) — not usable from this host.
- Adzuna CA API: no app key in the local cron environment, so no Adzuna pull this cycle.

## Partner / Elite Partner check

Checked ServiceNow and Salesforce partners/Elite Partners with Canadian operations: Genpact, Hexaware, CDW Canada (Elite), Devoteam, inMorphis, plus Deloitte / Accenture / CGI / Cognizant. No fresh Canadian ServiceNow/Salesforce technical requisitions surfaced this cycle beyond what is already on the board.

## Entry-level / Platform Admin focus

User target: entry-level / Platform Admin / Platform Developer I. The one genuinely entry-level Salesforce surface this cycle (Generis "Sales Operations Coordinator / Junior Salesforce Admin", posted ~2026-11-21, Downtown Toronto) is already on the board. White Bay (Salesforce Administrator, $60-75k, hybrid) is the nearest platform-admin match and was not previously on the board.

## Verification notes / constraints

- LinkedIn job detail pages are not directly fetchable from this host (bot wall / redirect to linkedin.com); Liveness established via search-index snippet date + title/company/platform match. Per board policy, a bot-wall/403 is treated as a live posting, not dead — but a LinkedIn HTTP 404 (Zaelab) is treated as expired.
- jobs.ca direct page is Cloudflare-blocked to this host ("Just a moment" challenge); liveness established via the search-index "Posted Nov 18, 2026" snippet. Direct fetch not possible.
- jobs.json meta (total/newThisScan) left for the next automated hourly scan to refresh; jobs array now includes the new row.
- The spontaneous working-tree regeneration seen at 2026-11-23T14:03:46Z (jobs.json/FRESH_JOBS.md timestamps + README DAILY-SCAN header) was reverted to HEAD; this commit carries only the manual White Bay merge.

## Files changed

- README.md — Salesforce table +1 row (White Bay), count 893 -> 894
- jobs.json — +1 job (5640 total)
- public/jobs.json, public/findjobs/jobs.json, public/gotjob/jobs.json — synced from jobs.json
- public/jobs-data.json, public/index.html — rebuilt by tools/build_site.py

## Next scan (10:00 EST)

Retry Adzuna if an API key becomes available; re-probe Workday CXS site-name re-discovery; check ServiceNow careers Ontario page and Salesforce Canada careers for requisitions not in SmartRecruiters/Workday feeds.

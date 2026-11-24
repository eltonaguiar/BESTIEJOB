<!-- merged 2026-11-24T124909Z: +0 new, 1 duplicate, version 2 -->
# BESTIEJOB hourly scan provenance — 2026-11-24T07:00EST

Scan sources this cycle:
- Adzuna CA API (ServiceNow + Salesforce, Toronto, max_days_old=7, sort_by=date): 91 ServiceNow / 205 Salesforce results; all 17 platform-relevant rows already on the board (deduped by URL and company+title).
- Workday CXS probes (BMO, TD, CIBC, Manulife, Interac, Salesforce, Accenture — full `{tenant}.wd{N}.myworkdayjobs.com` hosts, `--compressed`, `Origin` header): HTTP 200 on all reachable boards; no fresh Toronto ServiceNow/Platform Admin/Developer I reqs (BMO SN roles are 12 days old and already on the board via mirrors).
- Targeted web searches: ServiceNow Toronto, Salesforce Toronto, "Platform Developer I" Toronto, government/Job Bank ServiceNow.
- Employer-direct checks: Rogers (jobs.rogers.com — zero server-side job rows, Phenom shell), Bell (no reqs), Atego/FX Innovation (not enumerable from this host), ServiceNow Careers Ontario (sales/SRE/security only this cycle), Government of Canada Job Bank (stale Sept–Oct postings).

| Posted | Role | Company | Location | Note |
|---|---|---|---|---|
| 2026-11-23 | [Salesforce Marketing Cloud Senior Developer](https://careers.wipro.com/job/Salesforce-Marketing-Cloud-Senior-Developer/220984-en_US/) | Wipro Limited | Toronto, Ontario, Canada | Verified live on employer careers page (HTTP 200). Posted 2026-11-23 ("1 day ago"). Added to jobs.json (row 1) + README. URL + company+title dedupe negative against jobs.json, README.md, APPLIED.md. |

Net-new this cycle: 1 row (0 ServiceNow, 1 Salesforce).

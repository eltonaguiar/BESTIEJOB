# JOBLESSONS_2026-11-09

Hourly ServiceNow / Salesforce job scan for Toronto/GTA/Canada — {NOW.date()}.

## What ran
- `scripts/daily_job_scan.mjs`: SmartRecruiters (ServiceNow), Workday CXS (Salesforce/BMO/TD/BDO/CAAT/...), Greenhouse, Lever, Ashby, LinkedIn guest (`f_TPR=r86400` fresh pass), RemoteOK, Jobicy, Remotive, Adzuna Canada (24 Toronto/Canada queries incl. Ottawa, Mississauga).
- `tools/verify_links.py --days 2`: liveness gate, 404/410/451 = dead; 403/429/5xx = kept (bot walls).
- `tools/build_site.py`: regenerated `public/jobs-data.json` + `public/index.html`.

## Results this hour
- Fresh postings discovered: {len(fresh)}
- Verified-dead postings dropped: {len(DEAD_DROP)}
- Board on main: {len(remote_jobs)} -> {len(merged_jobs)} listings (non-destructive union; nothing already listed was removed)
- ServiceNow: {payload['meta']['primaryCounts']['servicenow']} | Salesforce: {payload['meta']['primaryCounts']['salesforce']}

## Notable fresh Toronto / partner / public-sector hits
- ServiceNow: TD (Sr. IT Developer), BMO (SAM Administrator - ITAM), CIBC (ServiceNow Developer), 407 ETR (System Developer Contract), Interac Corp., Tech Mahindra, KPMG Canada (Consultant / Senior Technical Consultant across Toronto/Ottawa/Halifax/Calgary/Vancouver), Accenture (ServiceNow Technical Architect, Toronto), CGI (Lead ServiceNow Architecture Consultant, Calgary), MNP (Senior SN Developer & Administrator, Calgary), UST (ITSM Service/Process Owner, Remote Canada), GDIT (ServiceNow Developer SME, Remote), TELUS Digital (Remote Canada), Brookfield Properties (Contract, Toronto), BDO Canada (Senior Developer, Toronto), CAAT Pension Plan (ServiceNow Developer Hybrid, Toronto).
- Salesforce: CGI (Senior Salesforce Developer, Toronto), Smart IT Frame LLC (Technical Architect CPQ/RCA x2, Ontario), Enterprise Solutions Inc. (Data Cloud Architect, Technical Architect, Toronto), Altus Group (Platform Developer), Webflow (Senior SF Developer, LaSalle), WPP/Map (Marketing Cloud Developer, Toronto), Winobell (Salesforce Dealer Services), City of Toronto (Corporate Application Technical Leader, Senior Systems Integrator), TD (Salesforce & nCino Solutions Design IT Specialist), iA Financial Group, Salesforce careers (Customer Success Manager MuleSoft Public Sector, Toronto), Deloitte (Senior Consultant SF Platform DTC), CloudKettle (Revenue Cloud Architect), OSI Digital (Salesforce Lead), PwC (Senior Associate SF BA).
- Partners/Elite Partners seen: Accenture, Deloitte, KPMG, CGI, Crossfuze, NewRocket, Slalom, NeuraFlash, OSI Digital, CloudKettle.
- Public sector / crown: City of Toronto, University of Toronto, CAAT Pension Plan, OMERS, CMHC (gc.ca careers), Export Development Canada, Trillium Health Partners.

## Gaps / watch items
- Rogers: no ServiceNow/Salesforce hits this hour (careers.rogers.com not surfaced by Adzuna/LinkedIn guest) — try site:rogers.com / careers.rogers.com directly next run.
- Bell: confirmed hits via Adzuna/LinkedIn (Conseiller technique principal ServiceNow Toronto; Senior ServiceNow Architect Toronto) — Ateko (backed by Bell Canada) also recurring.
- jobs.ca / Eluta / Indeed links frequently resolve to employer hub pages rather than postings — `is_listing_url()` filter must apply at render time, not just at sync time.
- LinkedIn guest endpoint returned 256 cards this run (previously 403-walled); the `f_TPR=r86400` 24h pass is the most reliable freshness filter.
- GitHub's own `hourly-scan.yml` Action commits directly to `main` at :00 UTC and races this cron — all writes here use Contents-API `sha` + retry-on-409; the Action rebases on reject, so no data loss expected.
- `dead_urls.txt` now lists {len(merged_dead)} blocked URLs; build honors `dead_url_keys()` so dead rows never render even if present in jobs.json.

## Files touched
jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json, public/jobs-data.json, public/index.html, README.md (DAILY-SCAN block), dead_urls.txt, FRESH_JOBS.md.

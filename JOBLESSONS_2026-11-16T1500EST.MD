# JOBLESSONS_2026-11-16 — hourly cron scan (15:00 EST / 20:00 UTC)

## Result this run
- Fresh Toronto ServiceNow / Salesforce scan at 15:00 EST: LinkedIn guest search (ServiceNow Toronto / Salesforce Toronto / Platform Administrator / Platform Developer I, past 24h, f_TPR=r86400), Workday CXS tenant probes, Rogers / Bell / public-sector checks.
- **2 brand-new verified merges this hour:** both body-verified via LinkedIn guest detail pages:
  1. ServiceNow CMDB Consultant — Envision Technology Solutions — Toronto, ON, Canada — posted 46 minutes ago (2026-11-16) — ca.linkedin.com/jobs/view/servicenow-cmdb-consultant-at-envision-technology-solutions-4490926514
  2. ServiceNow CMDB Consultant — IMR Soft LLC — Toronto, Canada (Hybrid), contract, 8+ yrs — posted 22 minutes ago (2026-11-16) — ca.linkedin.com/jobs/view/servicenow-cmdb-consultant-at-imr-soft-llc-4490936151
- README.md: ServiceNow table 1295 → 1297 rows; board total 7542 → 7544 live postings. jobs.json: 6279 → 6281 (SN 1304 → 1306). public/ rebuilt with tools/build_site.py (public/jobs-data.json + public/index.html). Committed and pushed to main → GitHub Pages redeploy (pages.yml).

## Sources checked — 15:00 EST
- **LinkedIn guest** (browser, fresh non-profile session, ca.linkedin.com/jobs/search, f_TPR=r86400): ServiceNow page 1 = past-24h cards. New on-target: Envision 4490926514 + IMR Soft 4490936151 (both merged). Burgeon IRM Sr Dev 4489774223 and HCLTech Salesforce Administrator 4490676918 already aboard (LinkedIn job-id equality = hard dedupe). Remaining cards off-target: generic QA, Salesforce Marketing Cloud/CPQ/Revenue Cloud, architect-only titles, US/DC roles ("Any nearest DC Office in Canada").
- **Workday CXS** (POST /wday/cxs/{tenant}/{site}/jobs, curl --compressed): rate-limited this hour — HTTP 000/429 across bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site. No usable data. Earlier 12Z page-1 cache: only Canada-hit was BMO "Applications Support Analyst" (posted yesterday, generic title, not platform-confirmed — deferred); every other fresh hit was India / US / Germany / Norway / Sweden / Israel / Thailand / Gurugram — excluded (postedOn "Today" is not a Canada signal).
- **Rogers** (jobs.rogers.com/search/?q=servicenow&sortColumn=referencedate&sortDirection=desc): 0 open positions matching "servicenow". **Bell** (jobs.bell.ca): (0) — no reqs; re-check weekly.
- **Public sector/government**: jobs.gc.ca NXDOMAIN; gojobs.gov.on.ca Radware-walled; Job Bank full-text is noise — trust only title-named platform postings.
- **Partners / Elite sponsors**: Accenture Workday (no Canada page-1); Deloitte/KPMG/Capgemini/PwC/CGI — no new Toronto SN/SF hits this hour. Earlier gap scan: Lane Four undated (merger skips undated), FX Innovation/Ateko/Cofomo/Everforth/Coaxxion/CloudKettle/Crossfuze = 0.

## Dedup & verification procedure followed
- Candidate key = normalized URL + LinkedIn job id, checked against jobs.json + README.md + APPLIED.md (APPLIED.md is a hard exclude).
- Merge bar: posted today/yesterday; direct posting deep-link (no hubs/search pages); Toronto/GTA/Canada location; title shows ServiceNow or Salesforce platform work. Salesforce emphasis: Platform Administrator / Platform Developer I (entry-level/junior). ServiceNow: developer/administrator/architect/analyst.
- Title-only leads without body/location confirmation are deferred, not merged.

## Market-shape notes (2026-11-16, stable)
- Hourly supply near zero: 2 fresh merges this hour after 0-merge runs at 13:00/14:00 EST. Normal late-2026 pattern — commit what's verified, skip empty hours.
- Fresh platform work comes via consultancies/staffing and banks' Workday tenants (BMO, TD, CIBC); vendor twins (different staffing firms, same client req) are kept as distinct postings.

## New lessons
1. LinkedIn guest search works via a fresh non-profile browser session; job-detail pages were readable this hour (14:00 run hit a wall) — verify bodies same-hour before the wall returns.
2. Workday CXS rate-limited again this hour across all 8 Canadian tenants — back off, sleep ≥6s between probes, retry next hour; don't conclude boards are empty from 429/000.
3. Dedupe by LinkedIn job id *before* writing up lessons: Burgeon 4489774223 was already aboard from an earlier run.

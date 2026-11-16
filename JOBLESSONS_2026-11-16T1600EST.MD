# JOBLESSONS_2026-11-16T1600EST — BESTIEJOB hourly scan

**Run:** 2026-11-16 16:00 EST (21:00 UTC), scheduled hourly pass
**Repo:** eltonaguiar/BESTIEJOB (main), local clone C:\Users\zerou\bestiejob
**Board state:** jobs.json = 6281 listings, scrapedAt 2026-11-16T19:10:38Z (last commit f5b9ae4, 15:13 EST)
**Result:** 0 fresh ServiceNow / Salesforce jobs merged this hour — board unchanged, no jobs.json/public commit required.

## Scope (per user request)
Fresh Toronto ServiceNow / Salesforce jobs; emphasis on Platform Administrator / Platform Developer I (entry-level/junior). Also scanning known partners/elite partners, sponsors, and technical employers: Rogers, Bell, Canadian government (Job Bank / public-sector portals).

## Sources checked this hour

| Source | Query | Result |
|---|---|---|
| LinkedIn guest search (browser, f_TPR=r86400) | ServiceNow, Toronto, past 24h | 60 cards; 9 postings with ServiceNow in title — all already on jobs.json |
| LinkedIn guest search (browser, f_TPR=r86400) | Salesforce Platform Administrator / Platform Developer I, Toronto, past 24h | 13 + 6 cards; 1 Platform Administrator (HCLTech) — already on jobs.json |
| Workday CXS | bmo.wd3, td.wd3, cibc.wd3, manulife.wd3, interac.wd3, accenture.wd103, salesforce.wd12, gdit.wd5 × ServiceNow/Salesforce | BLOCKED — HTTP 000 / 0 bytes on every pair from 13:02 EST onward |
| Rogers careers date-sort (jobs.rogers.com/search/?sortColumn=referencedate&sortDirection=desc) | all roles, newest first | ~2KB shell, no job rows rendered — walled this hour |
| Job Bank (public-sector proxy) | jobbank.gc.ca/jobsearch/jobposting/50698289 | LIVE but DUPED (see below) |
| Bell (jobs.bell.ca) | — | 0 reqs per prior runs; skipped this hour |

## Candidates evaluated

**Already on jobs.json (deduped by normalized URL):**
- LinkedIn 4490660430 NLB Services ServiceNow CSM/HRSD (Toronto/Mississauga, 6h ago)
- LinkedIn 4490602725 AllianceIT Inc ServiceNow ITOM/CMDB Developer (Toronto, 8h ago)
- LinkedIn 4489717217 TechNeptune Consulting Inc ServiceNow ITOM Developer (Toronto, 18h ago)
- LinkedIn 4489770670 Burgeon IT Services ServiceNow IRM Sr. Developer (6h ago)
- LinkedIn 4490663180 NLB Services ServiceNow HRSD (6h ago)
- LinkedIn 4489774223 Burgeon IT Services ServiceNow IRM Senior Developer (6h ago)
- LinkedIn 4489780092 Resource Logistics Inc ServiceNow Developer (6h ago)
- LinkedIn 4490140539 G Force IT Services Inc IT Service Management Consultant (34m ago — body walled, title ambiguous; kept out)
- LinkedIn 4490676918 HCLTech Salesforce Administrator (4h ago — exact Platform Administrator match)
- Job Bank 50698289 Source Code RQ00757 Specialized IT Consultant - Intermediate (Toronto, CSA+CAD mandatory, $81.20/hr, posted 2026-11-08, advertised until 2026-11-23) — **LIVE but not new**: identical company+title to existing careerbeacon row (postedDate 2026-11-03, careersbeacon URL …/rq00757-specialized-it-consultant-intermediate/toronto-on). Per company+title dedupe rule, not double-listed.

**Aged out (surfaced by the 10:02 EST Workday scrape, raw/extracted_fresh_jobs.json; not on jobs.json, but posted 4–30+ days ago — failed today/yesterday freshness rule):**
- BMO ServiceNow CMDB Administrator / Technology Lifecycle Analyst / SAM Administrator - ITAM (Toronto, 4–13 days)
- GDIT ServiceNow Developer / System Administrator / Sr Principal / Senior EHR (Remote, 3–14 days)
- Interac Senior BSA (ServiceNow) / QE Senior Specialist (ServiceNow Platform) (Toronto, 30+ days)
- TD Software Engineer III - Salesforce Data 360 (Toronto, 3 days)
- LinkedIn 4474558762 Deloitte ServiceNow CMDB Solution Architect — already on board

**inbox/todayfeeds--2026-11-16--v1.md:** 0 SN/SF rows (data-engineering/finance postings only).

## Patterns / guidance for the next run (17:00 EST)

1. **LinkedIn guest search page works via browser** (~6 s/query, 60 cards/page, no auth). Detail pages return a 378-byte authwall after ~3 rapid fetches — rely on card title/datetime/URL; space out any detail reads.
2. **Dedupe by normalized URL (strip query) AND company+title fuzzy.** Vendor twins (two agencies, same client req) are kept; the same role resurfacing on a different board (Job Bank vs careerbeacon here) is collapsed — do not double-list.
3. **Workday CXS is blocked from this host since 13:02 EST** (104-byte error stubs / HTTP 000). Known-good tenant×site pairs: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, accenture.wd103/AccentureCareers, salesforce.wd12/External_Career_Site, gdit.wd5/External_Career_Site. The 14:10–16:00 EST Workday window is NOT covered this hour — retry it first at the next run; the 14:10Z scrape did include Workday rows (19 workday jobs in jobs.json).
4. **Rogers date-sort board was walled (~2KB shell, no rows).** Standing guidance: check Rogers weekly, not hourly; when reachable, parse `<tr>` rows with absolute dates from `?sortColumn=referencedate&sortDirection=desc` — keyword search returns noise.
5. **Job Bank is a live proxy for government-adjacent SN roles** (page readable as guest; gojobs.gov.on.ca and jobs.gc.ca are Radware-walled — do not retry). Job Bank rows expire to 404 — a search hit is not proof of life; verify the page before trusting a date.
6. **Targeting rules applied:** SN = title/description mentions ServiceNow or CSA/CAD/CIS certs. SF = exact Platform Administrator / Platform Developer I titles; Technical Architect and Marketing Cloud roles are secondary and not merged unless entry-level.

## Files touched
- JOBLESSONS_2026-11-16T1600EST.MD (this file) — committed to main with [skip ci]; no jobs.json/public change, so GitHub Pages is not re-deployed by this run (next scheduled pages deploy at :35 UTC).
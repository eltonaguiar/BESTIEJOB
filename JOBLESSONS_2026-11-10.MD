# BESTIEJOB Hourly Scan — Job Search Lessons

**Date**: 2026-11-10
**Run time**: 2026-11-10 07:00 EST (12:00 UTC)
**Scope**: Fresh Toronto / GTA ServiceNow and Salesforce postings
**Repo**: github.com/eltonaguiar/BESTIEJOB (branch: main)
**Live board**: https://eltonaguiar.github.io/BESTIEJOB/

## Scan summary

| Metric | Value |
|---|---|
| Sources queried | LinkedIn guest API (ca.linkedin.com), ServiceNow Careers (careers.servicenow.com), Salesforce Careers (careers.salesforce.com), Rogers (jobs.rogers.com), Bell (jobs.bell.ca), Government of Canada (jobs.gc.ca / canada.ca); partner/employer sites: Accenture, Deloitte, KPMG, CGI, Scotiabank, RBC, TD, BMO, CIBC |
| Dedupe baseline (README.md tables + jobs.json on main) | ~7,783+ unique URLs; README carries 5,658 live postings (ServiceNow 741 · Salesforce 943 · Other 3,974); window 2026-10-10 → 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required) |

## Candidates reviewed

**LinkedIn guest API — Salesforce, Toronto, last 24h (f_TPR=r86400):** 10 postings returned.
- 8 already on the board (deduped by URL): CGI Senior Salesforce Developer (4408542861), Genesys Sr. Salesforce Developer (4487960730), Smart IT Frame Salesforce Technical Architect ×2 (4487909642, 4486765411), Apptoza Senior Salesforce Developer (4487409717), Apptoza Salesforce Revenue Cloud Architect (4487173874), Diligente Senior/Lead Salesforce Marketing Cloud Engineer Mississauga (4477699547), Tekgence Salesforce Revenue Cloud Developer (4487949008). Skipped as duplicates.
- 2 not on the board, both excluded by role rule:
  - Salesforce — Partner Sales - Canada (4481519206, posted ~2h ago): sales/account role, rejected per title rule (sales/marketing roles excluded unless platform/analytics).
  - Salesforce — Principal Applied AI Architect (4487978961, posted ~7h ago): AI architecture, not a ServiceNow/Salesforce Platform Admin or Platform Developer I role; not entry-level. Rejected.
- LinkedIn ServiceNow query returned no extractable results (keyless extraction not supported for this site). LinkedIn detail pages sit behind a login wall, so posting dates cannot be independently verified — no LinkedIn-sourced role added without a verifiable absolute date.

**ServiceNow Careers (Ontario, 16 jobs):** Staff Systems Engineer (JB0073788, 11-06), Senior Staff Security Engineer \| Systems Engineering (JB0076457, 11-06), Staff Security Engineer \| Security Engineering (JB0076454, 11-06), Staff Site Reliability Engineer Canada Protected B (JB0076847, 11-05), Senior SRE Canada Protected B (JB0076846, 11-05) — all already on the board. Today's (11-09) postings are sales roles (Sales Director - CRM Sales; Senior CRM Account Executive) → rejected by title rule. Nothing fresh and platform-relevant.

**Salesforce Careers:** careers hub returned no extractable fresh Platform Admin / Platform Developer I postings for Toronto today.

**Partners / employers:**
- Deloitte — Senior Manager, ServiceNow - Operate (posting start 10/21/26, Toronto): outside freshness window; senior manager role.
- KPMG — Consultant/Senior Consultant ServiceNow Solution Developer (33919) and Functional Consultant (34113): existing vacancies, already captured on board (KPMG ×8). Not fresh.
- Accenture — careers hub only, no extractable fresh posting.
- CGI — Senior Salesforce Developer / Salesforce Architect in Toronto appear on Indeed aggregator but no extractable fresh direct posting date; CGI Senior Salesforce Developer (4408542861) already on board via LinkedIn.

**Rogers (jobs.rogers.com):** Lead Management Operations (Salesforce, Req 343961, posted 2026-10-28) — outside freshness window; already flagged. No fresh SN/SF technical roles.
**Bell (jobs.bell.ca):** no fresh ServiceNow/Salesforce technical roles surfaced; prior Bell SN roles were filled/expired.
**Government of Canada (jobs.gc.ca):** zero ServiceNow/Salesforce Toronto hits; GC platform work arrives via prime vendors on their own ATS.

**Banks:** Scotiabank ServiceNow Administrator Specialist (Req 261367 / 602949717) already on README (via hermes scan 2026-11-09). Scotiabank ServiceNow Developer (260518) and Salesforce Developer (265640) are senior/architect roles with no fresh extractable date; not entry-level Platform Admin/Dev I.

## Already on the board (context)

README.md on main is current through 2026-11-09 (5,658 live postings; ServiceNow 741 · Salesforce 943 · Other 3,974). Today's scan adds no verified fresh rows.

## Patterns / lessons for future agents

1. **LinkedIn guest API works for Salesforce but not ServiceNow.** The `seeMoreJobPostings` guest endpoint returned 10 Salesforce Toronto postings for `f_TPR=r86400`; the identical ServiceNow request was rejected (keyless extraction not supported / HTTP 403). ServiceNow hits must come from careers.servicenow.com or aggregators instead.
2. **LinkedIn gives relative ages only ("X hours ago"); detail pages are a login wall.** Absolute `datePosted` can't be verified by extraction, so no LinkedIn-sourced role enters the board without a verifiable date. The 8 already-boarded LinkedIn Salesforce roles came from prior scans with verified dates.
3. **Dedupe catches most fresh aggregator hits.** 8 of 10 fresh LinkedIn Salesforce postings were already on the board under the same LinkedIn URL. Always dedupe by normalized URL before judging.
4. **Role rule excludes the non-duplicate LinkedIn hits.** The two not-yet-boarded LinkedIn roles are a sales role (Partner Sales) and a principal AI architect — neither is a ServiceNow/Salesforce Platform Admin or Platform Developer I. Target titles stay: Platform Administrator, Platform Developer I, ServiceNow Administrator/Developer, plus CSA/CAD/CIS certs.
5. **Employer/partner career sites surface senior roles, not entry-level.** Deloitte (Senior Manager), KPMG (3+ yrs), Scotiabank (5+ yrs Administrator Specialist) are all mid/senior. Entry-level Platform Admin / Developer I Toronto postings remain scarce; the board's value is in capturing them when they appear, not forcing a merge every hour.
6. **Zero fresh merges on most hourly runs is the norm.** jobs.json/README are refreshed multiple times daily; today's board already carries postings through 2026-11-09. An hour scan that finds nothing verified-fresh is a clean run, not a failure.

## Recommended next scans

- Retry LinkedIn guest API for ServiceNow Toronto in a later hour (endpoint may be intermittently available); if still blocked, use `site:ca.linkedin.com/jobs/view servicenow toronto` web search to surface indexable deep links.
- Re-check KPMG careers (33919 / 34113) and Scotiabank ServiceNow Developer (260518) for a verified absolute posted date; add if fresh and not already boarded.
- Keep scanning named employer ATS deep-links (careers.servicenow.com, careers.kpmg.ca, jobs.scotiabank.com, careers.deloitte.ca) for Toronto SN/SF — aggregator mirrors lag employer sites.

## Files touched

- `JOBLESSONS_2026-11-10.MD` — this file, added to repo root on main.
- `README.md` — no changes (zero verified fresh jobs this hour).
- `public/` (GitHub Pages) — no changes; no redeploy required.

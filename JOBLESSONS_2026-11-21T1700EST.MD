# JOBLESSONS_2026-11-21T1700EST — Toronto ServiceNow / Salesforce hourly scan

**Run time:** 2026-11-21 17:00 EST (22:00 UTC). Cron run of the BESTIEJOB hourly scan.
**Scope:** Fresh Toronto / remote-Ontario ServiceNow and Salesforce (dev + admin) roles, plus adjacent "Other" track. Canada-focused; known partners/Elite partners, sponsors, banks, telcos and government employers in scope.
**Result:** +0 new verified jobs merged. All candidates were either already on the board, outside the freshness window (today/yesterday), not genuine platform roles, or from blocked sources.

---

## What this run did

1. **LinkedIn keyword sweep** (web_search, site:ca.linkedin.com/jobs/view):
   - ServiceNow Toronto: 8 leads found — all already on board (Brookfield 4481508851, Alldus 4483056086, Avanciers 4488236748/4491961105, Pacer Group 4492515163, Agility IT 4485353819, Sheridan College 4486264240, Cognizant 4489032943).
   - 2 additional leads NOT on board but outside freshness window: RBC Salesforce Platform Engineer (4454047088, ~1 week ago, mid-level nCino focus, not Platform Admin/Dev I), Sentrex Health Solutions Salesforce Developer (4419351664, ~2 weeks ago, Markham, 2+ yrs exp).
   - Salesforce Platform Developer I / Administrator Toronto: results were senior-level (3–10+ yrs), 1–4 weeks old, no entry-level Platform Admin/Dev I surfaced.

2. **Adzuna Canada API** (app_id=54ce986e, app_key=db851f299e966c0a2a72af525dce6199, max_days_old=2–3, sort_by=date):
   - Queries: ServiceNow, Salesforce, "ServiceNow Administrator", "ServiceNow Developer", "Salesforce Administrator", "Salesforce Developer" × where=Toronto/Ontario, pages 1–3.
   - All genuine SN/SF platform hits already on board (Blue Mantis, Flexstaf IT, Innosystech, ServiceNow Inc., NTT America, SickKids Foundation, Konrad, Medcan, Cloud Resourcing, Amicis Global, CGI, Serefin, Celestica).
   - Non-platform matches excluded per board rules: ServiceNow sales roles (Solution Sales Executive, Cyber Advisory, Sr Mgr Sales), marketing/automation roles (Marketing Cloud, Demand Generation, Revenue Ops), "ServiceNow or Jira" ITSM roles (TMX Group Manager Incident/Problem/Event Management — ticketing-tool user, not Admin/Dev).
   - Note: Adzuna `description` capped at ~500 chars; corroborate via mirrors/employer pages before merging.

3. **Workday CXS API** (curl --compressed, known Canadian tenants):
   - BMO (bmo.wd3/External): ServiceNow CMDB Administrator (R260030992) and ServiceNow Technology Lifecycle Analyst (R260030995) — both already on board (merged 2026-11-12).
   - TD (td.wd3/TD_Bank_Careers): Senior Solution Architect (ServiceNow) R_1521185, 5 days ago — already on board.
   - CIBC, Manulife, Interac, Salesforce: no fresh SN/SF platform roles (Interac had 2 SN roles but both 30+ days old).
   - Known-working tenants: bmo, td, cibc, manulife, interac, caatpension, iko, gdit, salesforce, accenture. Guesses (capgemini, kyndryl, ibm, cgi, cognizant, telus, rogers, kpmg, scotiabank, intact, loblaw, cprail) return 422/404/521.

4. **Partner / telco / government employers:**
   - Rogers (jobs.rogers.com): Phenom board returns HTTP 404 shell / zero rows server-side — do not retry hourly; rely on LinkedIn/Adzuna for Rogers rows.
   - Bell (jobs.bell.ca / jobs.bce.ca): renders empty shell, shows (0) for both servicenow and salesforce — zero reqs, re-check weekly.
   - Government of Canada (jobs.gc.ca) / Ontario (gojobs.gov.on.ca): Radware-walled — do not retry; use Job Bank as proxy, trust only title-named platform postings.
   - Scotiabank Phenom: previously unreachable; use jobs.scotiabank.com date-sortable search instead.
   - Real Bell SN hiring surfaces under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn.

---

## Patterns / lessons for future agents

- **Freshness window ≠ new roles.** Repeat hirers' Toronto SN/SF reqs (Cognizant, LGS/IBM, ServiceNow Inc., NeuraFlash/Accenture, PwC, RSM, Avanciers, Akkodis, EQ Bank, Versapay, TD/BMO Workday roles) reappear under the same req IDs; the board already carries them. Don't re-post the same requisition under a new scan date.
- **Dedupe must be fingerprint-based, not URL-based.** The same requisition is advertised across Adzuna, LinkedIn, Eluta and Job Bank mirrors with different URLs and dates. Normalize URLs (strip query strings/trailing slashes) AND diff against jobs.json + README.md + APPLIED.md.
- **Workday CXS 429s at :00Z** when the CI hourly scan runs concurrently. Manual probes at that minute get HTTP 429 on BMO/TD/Manulife/CIBC/Interac. Retry 3–4 tenants at ≥8s spacing or leave Workday to the CI pass. A post-:00Z retry pays off within ~4 minutes (10 tenants × 2 queries at 8s spacing returned HTTP 200 on all calls).
- **"Posted Today" is not a Canada signal.** Workday `postedOn: "Posted Today"` can be Gurugram/Bangalore reqs. Read the `/job/<City>/…` slug and country before counting a fresh hit.
- **LinkedIn guest search intermittently returns 0 cards for ServiceNow while Salesforce returns 40.** The query is walled, not empty — retry once after ~4 minutes (with scroll steps).
- **LinkedIn detail pages intermittently serve the authwall** (`h1: Join LinkedIn`) even mid-session. Skip that candidate as unverified; never infer platform content from the card title alone.
- **"ServiceNow" in body as tooling is not a platform role.** Body-check context: ITSM process managers listing "ServiceNow, or an equivalent ITSM tool" are ticketing-tool users, not Admin/Dev. Match "ServiceNow" or "Service Now" in title/description, or CSA/CAD/CIS certs in requirements.
- **CRM is not Salesforce.** "RQ… Software Developer – CRM" can be Siebel, not Salesforce. Read the duties text before accepting a body match; the LinkedIn "Similar jobs" sidebar injects unrelated keyword hits.
- **Entry-level Platform Admin / Developer I is scarce.** No entry-level Salesforce Platform Administrator or Platform Developer I surfaced this cycle in Toronto. Generic-titled BA/analyst/consultant roles may hide platform work — body-check before discarding (e.g., NTT DATA "Business Analyst" was actually ServiceNow SPM).
- **Vendor twins are distinct postings.** Two staffing firms advertising the same client req under the same title must both be kept — dedupe on URL, never title+company for agency rows.
- **Case-only duplicate filenames block git.** Avoid creating files differing only in case (e.g., foo.MD vs foo.md) — wedges git on case-insensitive filesystems.
- **`[skip ci]` commits do not trigger pages.yml.** Lessons-only pushes leave the deployed page on the previous deploy — correct when jobs.json/README/public did not change.

---

## Disposition

- **README.md:** unchanged (no new verified rows to add).
- **jobs.json:** unchanged.
- **public/ (GitHub Pages):** unchanged — no data changed; no rebuild needed.
- **New lessons file:** this document (JOBLESSONS_2026-11-21T1700EST.MD).
- **Next run:** re-scan known partner/proxy career pages directly (TD Workday, BMO Workday, Interac Workday) rather than re-running the same aggregator window; consider a manual telco/gov sweep on alternate cycles.

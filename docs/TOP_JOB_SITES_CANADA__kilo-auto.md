# Top job sites & employer targets in Canada — ServiceNow / Salesforce developer

**Advisory recorded:** 2026-11-02T16:45 UTC
**Agent / model:** kilo-auto (Hermes Agent, kilocode provider)
**Scope:** Canada (Toronto-first), ServiceNow & Salesforce developer/admin jobs

---

## 1. Job boards that actually work (verified by live scan)

These sources return real, current postings through public endpoints (no login, no paid API). The bestiejob hourly scan (`scripts/daily_job_scan.mjs`) pulls from all of them.

| Source | Type | Notes |
|--------|------|-------|
| **Adzuna Canada API** | Aggregator API | Largest volume (~327 postings in last scan). Use `app_id=54ce986e` demo key or set `ADZUNA_APP_ID`/`ADZUNA_API_KEY`. Queries: servicenow, salesforce, it reporting, it asset management, cmdb, itsm reporting — Toronto + Canada. |
| **LinkedIn guest API** | Jobs board | ~88 postings. `jobs-guest/jobs/api/seeMoreJobPostings/search`. Throttled hard; scan uses 1.8s pauses, 2 workers. Playwright fallback available but LinkedIn is increasingly blocked. |
| **Workday CXS API** | ATS (employer careers) | ~24 postings. Verified boards: Salesforce, BMO, TD Bank, Altus Group, Benevity, Moneris, BDO Canada, CAAT Pension, Medcan, Huron, GDIT, Resolve Tech, Irving Oil, McKesson, Brookfield, IKO. |
| **Greenhouse API** | ATS (employer careers) | ~18 postings. Verified boards: D2L, NeuraFlash, iCapital, Bloomerang, Movable Ink, LightFeather, 9th Way Insignia, Accenture Federal, Dscout. |
| **SmartRecruiters API** | ATS | ~7 postings. ServiceNow careers board (`api.smartrecruiters.com/v1/companies/ServiceNow/postings`). |
| **Ashby API** | ATS | ~4 postings. Verified: Benevity, Loopio, MoeGo. |
| **Lever API** | ATS | ~2 postings. Verified: EQ Bank, Alimentiv, Versapay. |
| **RemoteOK API** | Remote board | Remote-only feed; filter for Canada/Toronto. |
| **Jobicy API** | Remote board | `geo=canada`; ~20 postings. |
| **Remotive API** | Remote board | Search terms: servicenow, salesforce. |

**Bottom line:** Start with Adzuna (volume) + LinkedIn (freshness) + Workday/Greenhouse (employer careers). These four cover the bulk of Canadian SN/SF postings.

---

## 2. Job sites that are BLOCKED via HTTP (do not waste time scraping directly)

These return 403 Cloudflare / anti-bot / captcha when fetched anonymously:

- **Indeed.ca / Indeed.com** — Cloudflare "Just a moment..." / "Request Blocked"
- **ZipRecruiter** — Cloudflare 403
- **Jooble** — Cloudflare 403
- **Glassdoor** — Strong anti-bot; stealth + Playwright both failed (per `scrapers/backup_scrapers/README.md`, Feb 2026)
- **Workopolis** — 403 Forbidden
- **Wellfound (AngelList)** — 403 + captcha
- **Monster** — Structure changed; returns 0

**Recommendation:** Do not build primary scrapers against these. Use Playwright only as a last resort for individual company careers pages, or rely on aggregators (Adzuna) that already index them.

---

## 3. Top Canadian job boards (general, to check manually)

Even if not in the automated scan, these are worth a weekly manual look for SN/SF roles:

1. **Job Bank Canada** (jobbank.gc.ca) — Government of Canada, free, no login. Good for Ontario/Toronto postings from employers who post to the national exchange.
2. **LinkedIn Jobs** (linkedin.com/jobs) — Requires sign-in to see full list, but the guest API works for a sample.
3. **Indeed.ca** — High volume but blocked to anonymous scrapers; use via browser manually.
4. **Workopolis.ca** — Canadian incumbent; mostly 403 to scrapers, use manually.
5. **Monster.ca** — Use manually.
6. **SimplyHired.ca** — Aggregator.
7. **Canada's Top 100 Employers / Glassdoor.ca** — For employer research, not job pulling.

---

## 4. Company careers pages to target directly (ServiceNow & Salesforce partners & customers in Canada)

These employers are known ServiceNow and/or Salesforce partners or customers and actively hire SN/SF developers/admins in Canada (confirmed appearing in the live scan as hiring companies):

### Global consultancies (heavy SN + SF practice in Canada)
- **Deloitte** (CA) — 15 SN/SF postings in scan; Workday board `deloitte`
- **Accenture** — Major SN/SF implementation partner; check Accenture careers CA
- **KPMG Canada** — 9 postings in scan; SN/SF practice
- **CGI** — 11 postings; major Canadian IT services, SN/ITSM practice
- **Cognizant** — 3 postings; SN/SF practice
- **TCS (Tata Consultancy Services)** — 4 postings; SN/SF practice in Toronto
- **Slalom** — 3 postings; SN/SF consulting
- **Slalom / NeuraFlash** — NeuraFlash: 16 postings (top SN/SF hiring partner); NeuraFlash is a dedicated Salesforce + ServiceNow consultancy

### Pure-play / specialist SN & SF consultancies
- **NeuraFlash** — 16 postings; Salesforce + ServiceNow partner (Greenhouse board `neuraflash`)
- **CloudKettle Inc** — 2 postings; Salesforce consultancy (Toronto)
- **Benevity** — 6 postings; Workday + Ashby board; Salesforce/ServiceNow user
- **Altium Solutions** — ServiceNow partner; check careers
- **Appirio / Wipro / Infosys / HCL / Tech Mahindra** — SN/SF outsourcing practices; check Canada careers

### End-user employers (customers of ServiceNow & Salesforce, hiring in-house)
From the live scan, these Canadian employers had active SN/SF postings:
- **ServiceNow** itself — 10 postings (SmartRecruiters board); Canadian engineering/admin roles
- **Salesforce** — Workday board `salesforce`; Canadian roles
- **BMO (Bank of Montreal)** — Workday board `bmo`; Elton's former employer
- **TD Bank** — Workday board `td`; 3 postings
- **Bell** — 8 postings
- **Harris Computer** — 9 postings
- **McKesson** — 9 postings (Workday board `mckesson`)
- **Altus Group** — 4 postings (Workday board `altusgroup`)
- **Moneris** — Workday board `moneris`
- **BDO Canada** — Workday board `bdo`
- **CAAT Pension Plan** — Workday board `caatpension`
- **Medcan** — Workday board `medcan`
- **Huron** — Workday board `huron`
- **GDIT** — Workday board `gdit`
- **Resolve Tech Solutions** — Workday board `resolvetech`
- **Irving Oil** — Workday board `irvingoil`
- **Brookfield** — Workday board `brookfield`

**How to find more:** Search each company's careers site for "ServiceNow" or "Salesforce". Most use Workday, Greenhouse, Lever, Ashby, or SmartRecruiters — all of which have public APIs the scan already hits.

---

## 5. Recommended weekly search protocol (for a human)

1. **Adzuna API** — Run the scan queries: `servicenow`, `servicenow administrator`, `servicenow architect`, `salesforce`, `salesforce developer`, `salesforce administrator`, `salesforce architect`, `it reporting`, `it asset management`, `cmdb`, `itsm reporting` — Toronto + Canada, sort by date, max 14 days.
2. **LinkedIn Jobs** — Manual: "ServiceNow developer Toronto", "Salesforce administrator Toronto", "ServiceNow consultant Canada". Sort by "Date posted".
3. **Company careers (Workday/Greenhouse)** — Check the boards above directly; many post there before hitting aggregators.
4. **Job Bank Canada** — jobbank.gc.ca, search "ServiceNow" / "Salesforce", location Toronto/Ontario.
5. **Track applications** — Log company, role, URL, date applied, source in a spreadsheet.

---

## 6. Notes

- All postings are deduplicated by URL; nothing older than 45 days is kept; cert-targeted Adzuna queries use `maxDaysOld=3`.
- The bestiejob site (`https://eltonaguiar.github.io/BESTIEJOB/`) refreshes hourly via GitHub Actions (`hourly-scan.yml`) and pushes to `main` with `[skip ci]`.
- Anonymous scraping of Indeed/ZipRecruiter/Glassdoor is not viable without residential proxies or authenticated sessions — do not build production scrapers against them.

# Job Aggregator Reverse-Engineering Findings — BESTIEJOB

**Date:** 2026-11-09  
**Subject:** Techniques and sources for finding more fresh Canadian ServiceNow/Salesforce jobs  
**Repo:** https://github.com/eltonaguiar/BESTIEJOB

---

## 1. What BESTIEJOB Already Does

### Active branches (may hold additional techniques)
| Branch | Updated |
|--------|---------|
| restore-truncated-board-2026-11-03 | Nov 9, 2026 |
| kilo-2026-11-05-sam-modules | Nov 8, 2026 |
| hermes/scan-refresh-2026-11-05 | Nov 8, 2026 |
| job-hunt-sn-sf-2026-11-06 | Nov 6, 2026 |
| arlo/success-pack-2026-11-05 | Nov 5, 2026 |

### Scrapers already in `scrapers/`
- `recruiting_firms_scraper.js` — covers **TekSystems, Procom, S.i. Systems, Robert Half, Randstad, Hays, Altis, Experis, Insight Global, Kforce**. Each uses axios GET to the firm's job-search URL, cheerio parse of `.job-card` / `article` / JSON-LD, with `parseSalaryFromText` (hourly + annual + K notation) and `parseEmploymentType` helpers.
- `research_sources_scraper.js` — Jooble, USAJobs API, Authentic Jobs RSS, AngelList/Wellfound (basic HTML scrape of `angel.co/jobs`)
- `indeed_scraper.js`, `linkedin_scraper.js`, `simplyhired_scraper.js`, `remote_boards_scraper.js`, `easy_remote_scrapers.js`, `ats_api_scraper.js`, `company_careers_scraper.js`, `aggregator_scrapers.js`, `hr_platform_scraper.js`, `rss_feed_scraper.js`, `stealth_scraper.js`, `workingnomads_scraper.js`, `alternative_scraper.js`, `advanced_extraction.js`

### ATS board slugs (`tools/ats_board_slugs_ca.txt`)
~45 Greenhouse slugs and ~20 Lever slugs for Canadian companies (d2l, flipp, geotab, hootsuite, leagueinc, poka, workleap, etc.).
Direct API pattern:
- Greenhouse: `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs`
- Lever: `https://api.lever.co/v0/postings/{slug}?mode=json`

### Top keyword patterns (`keyword-patterns-nov2.md`)
**ServiceNow:** Developer (75), IRE/CMDB/Discovery (53/7/8), ITOM (18), ITAM/HAM/SAM Pro (15/22/5), GRC/IRM (14/12), SPM, CSM, HRSD  
**Salesforce:** Developer (56), Admin (25), Marketing Cloud (18), MuleSoft (15), Data Cloud/Agentforce (12/11), FSC/OmniStudio (10/8), LWC/Apex  
**Hidden titles:** Platform Engineer, CRM Analyst, ITSM Analyst, Configuration Manager, Asset Management Analyst, Business Systems Analyst (CRM)

### Best current source by volume
Adzuna — 11,712 jobs via public API, Canada-focused.  
`jobs_from_gh.json` meta source breakdown: LinkedIn 255, Adzuna 363, Greenhouse 19, SmartRecruiters 12, Workday 1, Lever 1, Ashby 2, RemoteOK 3, Remotive 4 — total 3,302 across 9 keywords.

### Confirmed Canadian SN/SF job sources (from `jobs_past_7_days_sn_sf.json` + `jobs_from_gh.json`)
- **Workday:** Altus Group (Toronto Salesforce BA), GDIT (ServiceNow Senior, remote)
- **Greenhouse:** NeuraFlash (Salesforce Consultant)
- **LinkedIn (ca.linkedin.com):** AceStack (ServiceNow Specialist, Montreal), Poly Tech Talent (ITSM, Toronto), SS&C Technologies (Salesforce Implementation, Toronto), Parkland Corporation (Salesforce Architect, Calgary)
- **SmartRecruiters:** ServiceNow (Staff Security Engineer, Toronto)
- **Adzuna:** TD (DevOps, Toronto)
- **Readme/LinkedIn guest:** various ITSM/ServiceNow roles in Toronto/Montreal

---

## 2. Techniques Other GitHub Job Aggregators Have That BESTIEJOB May Have Overlooked

### A. Riley-Dorrington/job-board-aggregator
- **Direct ATS API scraping** (not HTML): Greenhouse, Lever, Ashby, BambooHR, iCIMs, Paylocity, Workday — all hit via their public JSON APIs in parallel with `concurrent.futures`
- **20,000+ companies, 1M+ positions** — indexes by company slug, not just keyword search
- **Daily GitHub Actions refresh** with force-push to a separate `job-board-data` repo, tagged releases, chunked gzip data served via Web Workers for fast client-side filtering
- **Client-side filtering:** title, company, location, ATS platform, experience level, exclude keywords, remote-only toggle, hide recruiter postings, hide already-applied jobs
- **Takeaway:** Add Ashby, BambooHR, iCIMs, Paylocity as direct API scrapers alongside Greenhouse/Lever/Workday. Expand `ats_board_slugs_ca.txt` by crawling GitHub job-radar repos for more Canadian company slugs.

### B. OpenTechnology14/Job-Hunter (11 free scrapers, no API keys)
Sources BESTIEJOB doesn't appear to have:
- **Himalayas** (remote jobs aggregator)
- **RemoteOK** (remote jobs) — partially covered
- **Arbeitnow** (EU/US/remote aggregator)
- **The Muse** (company profiles + jobs)
- **Google Jobs** via SerpAPI (~$100/mo)
- **Company career-page discovery** (`scraper_web.py`) — finds a company's own ATS board by crawling their careers page
- **DuckDuckGo internet-wide search** (free) as fallback when SerpAPI unavailable
- **Spreadsheet tracking** + auto-apply browser automation

### C. Wellfound/AngelList scrapers
- `jwc20/wellfound-scraper` — logs in, makes POST requests to the Wellfound API
- `2scraper/wellfound-scraper` — Playwright/Selenium/Puppeteer or 2Captcha Scraping Browser API; gets salary + equity ranges
- Apify actors (`orgupdate/Apify-Wellfound-Jobs-Scraper`, `scrapeunblocker/wellfound-jobs-scraper`) — no login, search by role+location, export JSON/CSV, **only-new-jobs-since-last-run** mode
- BESTIEJOB's `research_sources_scraper.js` has a basic AngelList fetch but it's HTML-scraping `angel.co/jobs` which is likely blocked now (Wellfound moved to a heavy JS app). The Apify approach or direct Wellfound API would be more reliable.

---

## 3. The "Referred By" Job Board Technique

**Pattern:** Many job postings (especially from aggregators like Adzuna, SimplyHired, Indeed) include a "source" or "referral" field indicating which board originally posted the job. When scraping a job from Adzuna/Indeed/LinkedIn, look for:
- `source` or `provider` field in the job JSON
- "Originally posted on [BoardName]" text in the description
- Referral URL parameters in the job link (e.g., `?source=boardname`)
- Canonical URL pointing back to the original ATS board

**Action:** When you find a job via Adzuna/Indeed/LinkedIn, follow the `url` to the original posting. The original posting page often says "Posted on [BoardName] [X days ago]" or links back to the board. Collect those board names, then add them as new scraper targets. This is how you discover niche boards you don't already know about.

**Files to watch:** `jobs_from_gh.json` already has a `source` field per job — analyze which sources produce the most Canadian SN/SF jobs and deepen those, while hunting "referred by" text in job descriptions to find unknown boards.

---

## 4. IT Recruiting Companies — TekSystems, Procom, S.i. Systems

BESTIEJOB **already has scrapers for all three** in `recruiting_firms_scraper.js`:

| Firm | URL pattern | Status |
|------|-------------|--------|
| TEKsystems | `teksystems.com/en-ca/jobs?keywords=...&location=Toronto, ON` | Implemented (cheerio parse of `article`, `.job-card`, `.job-listing`) |
| Procom | `procom.ca/job-search/?search=...&location=Toronto` | Implemented (cheerio parse of `.job-listing`, `.job-card`, `article`) |
| S.i. Systems | `sisystems.com/it-jobs/?search=...&location=Toronto` | Implemented (cheerio parse of `.job-card`, `.job-listing`, `article`) |

Also already covered: Robert Half, Randstad, Hays, Altis, Experis, Insight Global, Kforce.

**What to add next** (Canadian IT staffing firms not in the scraper):
- Aerotek, Modis, SCI, Talent Inc., Randstad Technologies (separate from Randstad Digital), Computer Futures
- Ottawa-focused: Public Service Commission (jobs.gc.ca), GC Jobs for federal SN/SF roles
- Vancouver/BC: Robert Half Vancouver, Procom Vancouver, TEKsystems Vancouver

**Salary/rate parsing:** The `parseSalaryFromText` function handles hourly ($50/hr, $50-75/hour), annual ($80K-120K), and simple dollar amounts — good for contract roles which dominate staffing firm postings.

---

## 5. Specific Gaps & Recommendations for More Fresh Canadian SN/SF Jobs

### Immediate additions (low effort, high yield):

1. **Add Ashby, BambooHR, iCIMs, Paylocity APIs** — Riley-Dorrington's aggregator shows these are directly queryable via JSON. Expand `ats_board_slugs_ca.txt` with more Canadian company slugs from GitHub job-radar repos.

2. **Wellfound via no-login API** — BESTIEJOB's current AngelList scrape is basic HTML. Use an Apify Wellfound actor or the direct Wellfound search API to get startup SN/SF roles (startups use Salesforce heavily). The "only new jobs since last run" mode is ideal for fresh postings.

3. **Himalayas + Arbeitnow + The Muse** — from Job-Hunter's 11 scraper list. These are remote-focused and may have Canadian SN/SF roles not on LinkedIn/Indeed.

4. **"Referred by" harvesting** — when scraping from Adzuna (your #1 source by volume), extract the original board from each job's `source` field or follow the URL to find "Posted on [BoardName]" text. Add newly discovered boards as scrapers.

5. **Company career-page discovery** — Job-Hunter's `scraper_web.py` finds a company's own ATS board by crawling their careers page. For Canadian SN/SF end-users (banks, telecoms, retailers), their careers pages often use Greenhouse/Workday/ASHBY directly.

6. **Google Jobs via SerpAPI** — if budget allows, gives broadest coverage across all boards including ones you haven't scraped individually.

---

## 6. Summary of Priority Actions

| Priority | Action | Effort | Expected Yield |
|----------|--------|--------|----------------|
| 1 | Add Ashby/BambooHR/iCIMs/Paylocity API scrapers | Low | Medium |
| 2 | Wellfound no-login scraper with "new since last run" | Medium | High (startups use SF heavily) |
| 3 | Add Himalayas, Arbeitnow, The Muse scrapers | Low | Medium |
| 4 | "Referred by" board discovery from Adzuna job data | Low | Medium (ongoing discovery) |
| 5 | Company career-page discovery for Canadian SN/SF end-users | Medium | High (direct ATS boards) |
| 6 | Add missing Canadian staffing firms (Aerotek, Modis, SCI, etc.) | Low | Medium |

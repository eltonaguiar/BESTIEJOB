# Staffing Agency Portals — ServiceNow/Salesforce Developer Jobs (Canada)

**Purpose:** Reference list of staffing/recruiting agency career portals that feed ServiceNow/Salesforce contract and permanent roles in Canada. Maintained for other AIs to scrape/scan. Contains portal URLs, search URL patterns, notes on scrapeability, and known recent finds.

**Status:** All portals below verified reachable (HTTP 200) at scan time. Geo-validation required before adding any row to bestiejob (see `scripts/geo_validate_jobs.py`).

**Companion docs:** `docs/CANADIAN_JOB_SITES__nemotron.MD`, `docs/JOB_SEARCH_PLAYBOOK.md`, `docs/JOB_SEARCH_PROTOCOL_2026-11-02.md`

---

## 1. Staffing agency portals (Canada-focused)

| Agency | Portal URL | Search URL pattern | Scrapeable? | Notes |
|--------|-----------|-------------------|-------------|-------|
| **Procom** (procom.ca / procomservices.com) | `https://portal.procomservices.com/jobs?loginType=contractor&lang=en` | `.../jobs?loginType=contractor&lang=en&q=<kw>` | YES (JS-rendered HTML, direct hrefs) | Toronto-founded, Canada HQ; 300+ live jobs; 219 count on page; categories page `https://www.procom.ca/app/jobs?keywords=servicenow` works |
| **TEKsystems** | `https://careers.teksystems.com/ca/en/search-results` | `.../ca/en/search-results?keywords=ServiceNow` | YES (Phenom ATS, PhenomPeople CDN) | Allegis Group company; heavy ServiceNow practice; Job IDs `JP-006xxxxx`; example: `JP-006214349` ServiceNow Developer Ottawa 75-85 CAD/hr |
| **Apex Systems** (Everforth Apex) | `https://www.apexsystems.com/careers` | `.../careers?k=ServiceNow` | YES (Drupal, JS-rendered) | Everforth Inc (NYSE: EFOR); Big Five Bank Tier 1/2 support; Technical Writer ServiceNow/Virtual Agent 12-month remote Canada-wide; AI/ML Platform Developer Vancouver; HR Operations Advisor Vancouver hybrid |
| **Altis** | `https://jobportal.altis.com/search?b=altisrecruitment` | `.../search?b=altisrecruitment&k=ServiceNow` | YES (jobportal.altis.com) | Toronto staffing; job portal at `jobportal.altis.com`; categories include ERP Implementation, IT - Application & Software Development |
| **Experis Canada** (ManpowerGroup) | `https://www.experis.ca/en/search` | `.../en/search?keywords=ServiceNow` | YES (JS-rendered, ManpowerGroup site) | ManpowerGroup Canada; IT staffing; search page renders keywords |
| **Randstad Canada** | `https://www.randstad.ca/jobs/` | `.../jobs?search=<kw>` | PARTIAL (JS-rendered; job detail pages exist but listing needs JS) | Randstad Canada staffing; portal loads but results are JS-injected; direct job detail URLs like `/job/<slug>` found in page HTML |
| **Adecco Canada** | `https://www.adecco.ca/en-CA/jobs/` | `.../en-CA/job-seekers/find-a-job` | PARTIAL (JS-rendered; uses `candidate.adecco.com` portal) | Adecco Canada; candidate portal at `candidate.adecco.com/application/job-description/{jobId}`; needs JS or portal API |
| **Robert Half Canada** | `https://www.roberthalf.ca/en/jobs` | `.../ca/en/job/<city>-<province>/<title>/<id>-caen` | YES (server-rendered job detail pages) | Robert Half Canada; individual job pages server-rendered; keyword search returns accounting/admin not IT — need direct URL probing |
| **Manpower Canada** | `https://www.manpower.ca/en/jobs` | — | PARTIAL (JS-rendered) | Manpower Canada staffing; portal loads but results JS-injected |
| **Kelly Services Canada** | `https://kellyservices.ca/en/jobs/` | — | PARTIAL (JS-rendered) | Kelly Services Canada staffing; portal loads but results JS-injected |
| **Insight Global** | `https://www.insightglobal.com/careers/` | — | PARTIAL (JS-rendered) | Insight Global staffing; portal loads but results JS-injected |
| **Epsilon Solutions** | `https://www.epsilonsolutions.ca/careers/` | `https://www1.jobdiva.com/portal/?a=...` | YES (JobDiva portal) | Epsilon Solutions; JobDiva ATS portal linked from careers page |

---

## 2. Known recent finds from these portals

| Portal | Role | Location | Posted | Source URL | Status |
|--------|------|----------|--------|------------|--------|
| TEKsystems | ServiceNow Developer | Ottawa, ON | Aug 11 2026 | `careers.teksystems.com/ca/en/job/JP-006214349` | Live, 75-85 CAD/hr |
| TEKsystems | Mid-Senior ServiceNow Developer | DISN contract | Oct 27 2026 | `careers.teksystems.com/ca/en/job/JP-006381588` | Live |
| TEKsystems | Engagement Manager/Project Manager-ServiceNow | Remote | Nov 6 2026 close | `careers.teksystems.com/ca/en/job/JP-006374689` | Live |
| Apex Systems | Technical Writer (ServiceNow/Virtual Agent) | Remote Canada-wide | Recent | `apexsystems.com/job/3046124_usa/technical-writer` | Live, Big Five Bank client, 12-month |
| Apex Systems | AI/ML Platform Developer (CAN) | Vancouver, BC | Jul 9 2026 | `itcareersapply.apexsystems.com/application?id=OBtfjuniRZA%3D` | Live, hybrid 3x/week |
| Apex Systems | HR Operations Advisor | Vancouver, BC | Recent | `apexsystems.com/job/3041758_usa/hr-operations-advisor-1` | Live, hybrid 3x/week |
| Apex Systems | Solutions Architect (FAAS/Ads) | Toronto, ON (hybrid) | Recent | `apexsystems.com/job/3054928_usa/solution-architect-faasads` | Live, ecommerce/grocer |
| Apex Systems | Digital Cloud Solution Architect L2 | Remote Canada | Recent | `apexsystems.com/job/3058252_usa/digital-cloud-solution-architect-l2` | Live |
| Apex Systems | Applications Support Specialist | Barrie/Scarborough ON | Recent | `apexsystems.com/job/3045453_usa/applications-support-specialist` | Live, Big Five Bank, 6-month |
| Apex Systems | Technical Service Specialist | Southwestern ON | Recent | `apexsystems.com/job/3037173_usa/technical-service-specialist` | Live, field Ontario |
| Apex Systems | Technical Service Specialist | Southwestern ON | Recent | `apexsystems.com/job/3037173_usa/technical-service-specialist` | Live, field Ontario |
| Apex Systems | Manager of Sales | Montreal/Toronto remote | Recent | `apexsystems.com/job/3057071_usa/manager-of-sales` | Live, SaaS healthcare tech |

---

## 2b. Recent finds — staffing agencies via LinkedIn guest API

| Agency | Role | Company | Location | Posted | Source URL | Notes |
|--------|------|---------|----------|--------|------------|-------|
| TEKsystems | Software Engineer (Salesforce) | Motorola Solutions | Greater Vancouver, BC | 2026-11-10 | `ca.linkedin.com/jobs/view/software-engineer-salesforce-canada-remote-at-motorola-solutions` | Canada remote |
| TEKsystems | Salesforce Technical Architect | Smart IT Frame LLC | Toronto, ON | 2026-11-10 | `ca.linkedin.com/jobs/view/salesforce-technical-architect-strong-cpq-and-revenue-cloud-advanc` | CPQ + Revenue Cloud |
| TEKsystems | Développeur Salesforce | LGS, an IBM Company | Ville-Marie, QC | 2026-11-11 | `ca.linkedin.com/jobs/view/d%C3%A9veloppeur-salesforce-at-lgs-an-ibm-company-4487871160` | French-language role |
| TEKsystems | Senior Salesforce Developer | Zodiac Solutions, Inc | Toronto, ON | 2026-11-10 | `ca.linkedin.com/jobs/view/senior-salesforce-developer-at-zodiac-solutions-inc-4487827104` | |
| Procom | Specialist- Salesforce Architect | Parkland Corporation | Calgary, AB | 2026-11-11 | `ca.linkedin.com/jobs/view/specialist-salesforce-architect-at-parkland-corporation-4487861359` | Duplicate posting seen twice |
| Altis | Salesforce Configuration Developer (FSC) | Avanciers Inc. | Montreal, QC | 2026-11-10 | `ca.linkedin.com/jobs/view/salesforce-configuration-developer-salesforce-fsc-at-avanciers-inc` | Financial Services Cloud |
| Altis | Associate, Salesforce Support | Apex Systems | Toronto, ON | 2026-11-10 | `ca.linkedin.com/jobs/view/associate-salesforce-support-at-apex-systems-4489652732` | Support tier role |
| Experis | Salesforce Technical Architect - Service Cloud Voice | Experis | Canada | 2026-11-10 | `ca.linkedin.com/jobs/view/salesforce-technical-architect-service-cloud-v` | Service Cloud Voice specialty |
| Experis | Salesforce FSC Developer | Quantum World Technologies Inc. | Toronto, ON | 2026-11-10 | `ca.linkedin.com/jobs/view/salesforce-fsc-developer-at-quantum-world-technologies-inc-4489612` | Financial Services Cloud |
| Insight Global | Business Systems Analyst | Lane Four | Toronto, ON | 2026-11-06 | `ca.linkedin.com/jobs/view/business-systems-analyst-at-lane-four-44873454` | Salesforce partner consulting |
| Randstad | IT Help Desk Analyst | Bay Street Staffing | Greater Toronto Area | 2026-11-10 | `ca.linkedin.com/jobs/view/information-technology-help-desk-analyst-at-ba` | IT help desk |
| Randstad Canada | Technical Help Desk - Senior | Raise | Toronto, ON | 2026-11-10 | `ca.linkedin.com/jobs/view/technical-help-desk-senior-at-raise-4489497645` | Senior help desk |
| Kelly Canada | Directeur | Deloitte | Montreal, QC | 2026-11-10 | `ca.linkedin.com/jobs/view/25-directeur-at-deloitte-4488645258` | French-language "Directeur" role |

---

## 3. Scrape notes per portal

### Procom (`portal.procomservices.com`)
- Fully server-side rendered HTML; direct `<a href="/jobs/slug-hash">` links
- Each job page shows date posted, salary range, workplace type, location
- Search: try `?loginType=contractor&lang=en&q=ServiceNow` or `&keywords=ServiceNow`
- Pagination shows 15 pages (~300 jobs)
- Categories: `https://www.procom.ca/app/jobs?keywords=servicenow`

### TEKsystems (`careers.teksystems.com`)
- Phenom ATS (PhenomPeople CDN assets)
- Canada site: `careers.teksystems.com/ca/en/`
- Job URL pattern: `/ca/en/job/JP-006xxxxx/<slug>`
- Search: `?keywords=ServiceNow`
- Heavy ServiceNow practice (CMDB, SecOps, ITOM, AppEngine, CSM, HRSD roles seen)

### Apex Systems (`apexsystems.com`)
- Drupal CMS
- Job URL pattern: `/job/\d+_[a-z]+/[a-z-]+`
- Individual job pages need separate fetch for title/location
- Everforth Inc (NYSE: EFOR); Commercial Segment
- Canadian locations: Vancouver BC, Toronto ON, Montreal QC, Barrie/Scarborough ON, Southwestern ON

### Altis (`jobportal.altis.com`)
- Job portal at `jobportal.altis.com` (separate from marketing site `altisrecruitment.com`)
- Search: `?b=altisrecruitment&k=ServiceNow`
- Categories: IT - Application & Software Development, ERP Implementation

### Experis Canada (`experis.ca`)
- ManpowerGroup site; JS-rendered
- Search: `?keywords=ServiceNow`
- May require JS execution for results

---

## 4. Geo-validation requirement

Before adding any row from these portals to bestiejob README:
1. Fetch the individual job URL
2. Confirm HTTP 200 (active, not closed/filled/expired)
3. Confirm location is Canada (Toronto/GTA, Ontario, remote-Canada, or another Canadian province)
4. Confirm role matches ServiceNow/Salesforce developer/admin/architect (not sales, AE, BDR, etc.)

See `scripts/geo_validate_jobs.py` for the validation script.

---

*Prepared by Kilo (opencode fork, nvidia/nemotron-3.5-super-vl:free), 2026-11-11. Agency portals discovered through search engine queries, direct URL probing, and LinkedIn guest API harvests. Portals verified reachable at scan time; verify each portal directly before scraping as site structures may change. Staffing agencies covered: Procom, TEKsystems, Apex Systems, Altis, Experis Canada, Randstad Canada, Adecco Canada, Robert Half Canada, Manpower Canada, Kelly Services Canada, Insight Global, Epsilon Solutions.*

# JOBLESSONS_2026-11-08.MD
**Date:** 2026-11-08 (Sunday)  
**Run time:** 06:00 EST / 11:00 UTC  
**Agent:** Hermes cron job (hourly scan for Toronto ServiceNow/Salesforce jobs)

---

## Scan Summary
- **Daily scan executed:** `npm run scan:daily` (via `scripts/daily_job_scan.mjs`)
- **Sources queried:** 50+ employer ATS feeds, job boards (LinkedIn, Indeed, Adzuna, Glassdoor, etc.), partner portals
- **Live postings found:** 1,665 total (938 ServiceNow + 931 Salesforce + other)
- **Curated tables updated:** 150 ServiceNow + 150 Salesforce + 150 Other = 450 live postings (30-day window)
- **Merge completed:** All inbox files merged into README.md curated tables via `tools/jobs_merge_inbox.py`

---

## Key Lessons Learned

### 1. **ServiceNow Partner / Elite Partner Signals**
The most reliable Toronto ServiceNow postings come from **partner companies** that are official ServiceNow Elite/Platinum/Gold partners:
| Partner | Tier | Toronto Postings (today) | Signal Strength |
|---------|------|--------------------------|-----------------|
| **Deloitte** | Elite | 6+ | ⭐⭐⭐⭐⭐ - Always posts on careers.deloitte.ca + LinkedIn |
| **KPMG** | Elite | 5+ | ⭐⭐⭐⭐ - careers.kpmg.ca + LinkedIn, consistent volume |
| **Accenture** | Elite | 3+ | ⭐⭐⭐⭐ - Multiple ATS (Workday, jobs.ca) |
| **CGI** | Elite | 2+ | ⭐⭐⭐ - LinkedIn guest posts, French/English |
| **Bell Canada / Ateko** | Strategic | 1 | ⭐⭐⭐ - "backed by Bell Canada" tag = high confidence |
| **Slalom** | Elite | 3+ | ⭐⭐⭐ - jobs.slalom.com multi-locale |
| **ServiceNow Inc.** | Vendor | 4 | ⭐⭐⭐⭐⭐ - SmartRecruiters ATS, direct hiring |

**Pattern:** Elite partners post 3-10x more roles than non-partners. Filter by partner tier first.

### 2. **Salesforce Partner / ISV Signals**
Top Toronto Salesforce sources:
| Company | Type | Today's Postings | Signal |
|---------|------|------------------|--------|
| **Salesforce (vendor)** | Vendor | 2 | ⭐⭐⭐⭐⭐ - Direct LinkedIn, migration architect roles |
| **Cognizant** | GS/Platinum | 1 | ⭐⭐⭐⭐ - B2B Commerce Architect, Mississauga |
| **McKesson / Medicine Shoppe** | Enterprise | 2 | ⭐⭐⭐⭐ - Healthcare vertical, Mississauga cluster |
| **LTM (Larsen & Toubro)** | GS | 1 | ⭐⭐⭐ - Data Cloud focus |
| **IKO North America** | End-user | 1 | ⭐⭐⭐ - Manufacturing vertical |
| **nesto** | FinTech | 1 | ⭐⭐⭐ - QA Automation Salesforce |

**Pattern:** Vertical-specific (healthcare, fintech, manufacturing) Salesforce roles cluster in Mississauga/Toronto corridor.

### 3. **Telco & Crown Corporation Hiring**
- **Rogers / Bell / Telus / Bell Canada (Ateko):** Consistent ServiceNow hiring
- **Bell Canada** posts via Ateko subsidiary - watch for "backed by Bell Canada"
- **TELUS Digital** posts ServiceNow dev roles on jobs.ca (Remote Canada)
- **Interac Corp** (crown-adjacent): ServiceNow Developer on LinkedIn today
- **Canada Post / Purolator / 407 ETR** - periodic ServiceNow contracts

### 4. **Big Five Banks - Core Toronto Employers**
| Bank | Today's SN/SF Postings | ATS / Board |
|------|------------------------|-------------|
| **TD** | Sr IT Developer (ServiceNow) | LinkedIn |
| **CIBC** | ServiceNow Developer | LinkedIn |
| **BMO** | Senior ServiceNow Solutions Engineer | Indeed |
| **RBC** | (periodic) | Workday / careers.rbc.com |
| **Scotiabank** | (periodic) | Workday |

**Pattern:** Banks post on LinkedIn guest + own Workday. Use "site:linkedin.com/jobs (TD|CIBC|BMO|RBC|Scotiabank) ServiceNow" for monitoring.

### 5. **Federal / Provincial Government**
- **GC Jobs (jobs.gc.ca):** ServiceNow roles under "ITS" classification
- **Ontario Public Service (gojobs.gov.on.ca):** Periodic ServiceNow architects
- **City of Toronto:** ITSM Analyst roles (Salvation Army Canada posting today via Workday)
- **Shared Services Canada:** Bulk hiring for ServiceNow platform team

### 6. **Best ATS / Feed Sources for Toronto**
| Source | Coverage | Reliability | Notes |
|--------|----------|-------------|-------|
| **LinkedIn Guest** | High | ⭐⭐⭐⭐ | Most partner/consulting posts; deduplicate by URL |
| **jobs.ca** | High | ⭐⭐⭐⭐ | Canadian aggregator, good for Brookfield, TELUS, Accenture |
| **Adzuna API** | Med | ⭐⭐⭐ | Duplicates LinkedIn; good for salary estimates |
| **Workday (direct)** | High | ⭐⭐⭐⭐⭐ | Banks, Deloitte, KPMG, CGI, ServiceNow Inc. |
| **SmartRecruiters** | High | ⭐⭐⭐⭐ | ServiceNow Inc., Slalom |
| **Greenhouse / Lever / Ashby** | Med | ⭐⭐⭐ | Tech companies (Lightspeed, Anthropic, etc.) |
| **Indeed (ca.indeed.com)** | Med | ⭐⭐⭐ | Salesforce architect roles, some duplicates |

### 7. **Deduplication Patterns**
- **URL-based dedup** works best: LinkedIn guest URLs (`ca.linkedin.com/jobs/view/...`) are canonical
- **Same role, multiple boards:** e.g., Deloitte ServiceNow Cyber Sales Executive appears on LinkedIn + Adzuna + rounds1-8
- **Partner rebranding:** "Ateko backed by Bell Canada" = Bell Canada posting
- **Locale variants:** Slalom posts same role on jobs.slalom.com/en_US, /de_DE, /es_ES, /ja_JP → dedupe by jobId

### 8. **Search Keywords That Surface Toronto SN/SF**
```
ServiceNow: "ServiceNow Developer Toronto", "ServiceNow Architect Toronto", "ITSM Analyst Toronto", "ITOM ServiceNow Toronto", "ServiceNow CSA Toronto"
Salesforce: "Salesforce Architect Toronto", "Salesforce Developer Mississauga", "Marketing Cloud Toronto", "Salesforce CPQ Toronto", "Revenue Cloud Architect Toronto"
```
**Pro tip:** Add `"Remote Canada"` + `"Toronto"` to catch hybrid roles.

### 9. **Today's High-Value Toronto Finds (2026-11-08)**
| Role | Company | Location | Source | Why Notable |
|------|---------|----------|--------|-------------|
| ServiceNow Developer (Contract) | Brookfield Asset Management | Toronto, ON | jobs.ca | Large asset manager, direct posting |
| ServiceNow Developer | Lightspeed Commerce | Toronto, ON | Ashby | Fast-growing Canadian tech unicorn |
| Senior Consultant, Developer, ServiceNow | KPMG Canada | Toronto | LinkedIn Guest | Elite partner, multiple openings |
| Senior ServiceNow HR Developer | Quantum Technology (QTR) | Toronto | jobs.ca | Recruiting firm placing at banks |
| Solutions Architect, Salesforce Migrations | Salesforce | Toronto | LinkedIn Guest | Vendor direct, Data360/Revenue Cloud |
| Salesforce Technical Architect | McKesson | Mississauga | LinkedIn Guest | Healthcare vertical, enterprise scale |
| Salesforce B2B Commerce Architect | Cognizant | Mississauga | LinkedIn Guest | Platinum partner, commerce specialization |

---

## Action Items for Next Hourly Run
1. [ ] Re-run `npm run scan:daily` at top of next hour
2. [ ] Check for new postings from **Deloitte, KPMG, Accenture, CGI, Bell/Ateko** Workday feeds
3. [ ] Monitor **GC Jobs** and **gojobs.gov.on.ca** for federal/provincial ServiceNow roles
4. [ ] Watch **ServiceNow Inc. SmartRecruiters** for new Toronto engineering roles
5. [ ] Cross-reference **indeed-monitor** for Salesforce Marketing Cloud / Revenue Cloud postings
6. [ ] Validate any new URLs against existing README.md (grep by URL) before adding to inbox

---

## Technical Notes
- **Git push blocked on Windows** → Use `gh api` Contents API for commits (base64 encode files)
- **Submodule `ServiceNow_Learning...`** shows modified - may need separate handling
- **Inbox files auto-bumped** on merge - old versions deleted, new versioned files created
- **README.BAK_*** auto-created on each merge for rollback
- **public/*.json** updated for GitHub Pages (eltonaguiar.github.io/BESTIEJOB/)

---

## Pattern for Future Agents
> **When searching for Toronto ServiceNow/Salesforce jobs:**
> 1. Start with Elite Partner career sites (Deloitte, KPMG, Accenture, CGI, Slalom)
> 2. Check vendor direct (ServiceNow Inc., Salesforce)
> 3. Scan Big Five banks' Workday + LinkedIn
> 4. Add telco (Bell/Ateko, Rogers, TELUS, Interac)
> 5. Check GC Jobs / Ontario Public Service
> 6. Deduplicate by canonical URL (LinkedIn guest > Adzuna > Indeed)
> 7. Cap curated tables at 150/category, 30-day window
> 8. Save lessons to `JOBLESSONS_YYYY-MM-DD.MD` each run
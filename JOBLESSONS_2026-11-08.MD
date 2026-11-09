# JOBLESSONS_2026-11-08.MD
**Date:** 2026-11-08 (Sunday)  
**Run time:** 09:00 EST / 14:00 UTC  
**Agent:** Hermes cron job (hourly scan for Toronto ServiceNow/Salesforce jobs)

---

## Scan Summary
- **Hourly scan executed:** `npm run scan:daily` (via `scripts/daily_job_scan.mjs`)
- **Sources queried:** 9 sources (LinkedIn Guest, Greenhouse, Workday, SmartRecruiters, Adzuna, Remotive, Jobicy, Lever, RemoteOK)
- **Live postings found:** 2,030 total (942 ServiceNow + 931 Salesforce + 157 Other)
- **Curated tables updated:** 150 ServiceNow + 150 Salesforce + 150 Other = 450 live postings (30-day window)
- **Merge completed:** All inbox files merged into README.md curated tables via `tools/jobs_merge_inbox.py`
- **Git commit:** `91941d1` — pushed to main branch; GitHub Pages site https://eltonaguiar.github.io/BESTIEJOB/ updated

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

## Additional Scan: 2026-11-08 (Hourly Cron Run — Post-Merge Update)

### Technical Notes — Adzuna API Rate Limiting
- Adzuna API returned HTTP 429 (Too Many Requests) for all 50+ queries in this hourly run
- All Adzuna searches were rate-limited; SmartRecruiters, Workday, LinkedIn, and other sources provided the fresh data instead
- Recommended back-off: wait 60+ seconds between Adzuna API calls, or reduce concurrent queries from 3 to 1

### Scan Results — Fresh Jobs Found (Hourly Run vs. 06:00 EST Run)
- **Adzuna:** 0 matching postings (rate-limited); 0 in prior 06:00 EST run
- **SmartRecruiters:** 12 matching postings (new source this run)
- **Workday:** 16 matching postings (same count as 06:00 EST run: 16)
- **Lever:** 1 matching posting (new source this run; 0 in 06:00 EST)
- **LinkedIn:** 205 matching postings (same scale as 06:00 EST: 205 via LinkedIn Guest API)
- **Total fresh:** 264 new jobs identified before dedup

### Merge Results
- After dedup and secondary capping: 450 curated rows in 30-day window
- Breakdown: 150 ServiceNow + 150 Salesforce + 150 Other (same as prior run's cap)
- Archived 4848+ expired rows to README.BAK_2026-11-08T130449Z.md
- Applied roles excluded (per APPLIED.md guard)

### Site Build Output
- Total jobs in built site: 1830 (735 ServiceNow + 761 Salesforce + 334 Other)
- Down from 2030 in raw scanned set — dedup and per-category capping applied
- Newest posting: 2026-11-08; built: 2026-11-08 13:04 UTC
- 35 applied roles hidden; 222 duplicate mirrors collapsed

### Key Patterns Confirmed (repeated from prior runs)
- Elite partners (Deloitte, KPMG, Accenture, CGI, Slalom) remain the most reliable source for Toronto ServiceNow roles
- Partner rebranding pattern persists: "Ateko backed by Bell Canada" = Bell Canada posting
- URL dedup by canonical URL (stripping query params, www., lowercasing) is essential
- LinkedIn Guest API is the highest-volume source for partner/consulting postings

### New Action Items
1. [ ] Implement Adzuna API back-off/retry logic (60s minimum between calls, reduce concurrency)
2. [ ] Monitor LinkedIn API rate limits (429 observed in this run)
3. [ ] Consider SmartRecruiters and Lever as high-priority sources for hourly scans
4. [ ] Verify deduplication pipeline handles the same role appearing on multiple boards


## 21:00 EST hourly run — 2026-11-08 (second run today)

**Scan executed:** `node scripts/daily_job_scan.mjs --no-readme` + `node scripts/gap_scan.mjs`
**Sources:** SmartRecruiters, Workday, Greenhouse, Lever, Ashby, LinkedIn Guest, Adzuna, RemoteOK, Jobicy, Remotive + partner career sites (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze)
**Fresh postings this run:** 622 new across SN/SF feeds; gap scan +6 feed entries; 2 undated roles to `inbox/gap-scan--2026-11-09--v1.md`
**Feed total:** 2,169 postings in `jobs.json`; 2,072 matching in `FRESH_JOBS.md`
**Curated tables merged into README.md:** ServiceNow 595 + Salesforce 535 + Other 102 = 1,232 rows (932 genuinely new, 3 date-refreshed; deduped by canonical URL against README.md + APPLIED.md)
**Site rebuilt:** `public/jobs-data.json` + `public/index.html` — 1,833 jobs (SN 736, SF 759, Other 338), newest 2026-11-09, built 2026-11-09 02:04 UTC
**Duplicate check:** no doubled rows within the managed ServiceNow/Salesforce/Other tables; every fresh URL verified absent from README/APPLIED before insert. (25 pre-existing legacy-tail duplicates remain untouched outside the managed tables.)

### Lessons — 21:00 run
- Adzuna returned 367 postings this run (no HTTP 429 rate-limiting, unlike the 09:00 EST run); best volume pairing is Adzuna + LinkedIn Guest (199) + Workday (16).
- SmartRecruiters ServiceNow (12) and Workday (16) remain strong for vendor-direct Toronto roles (ServiceNow Inc., GDIT).
- Gap-scan partner career pages returned 0 dated roles — Ateko/FX Innovation, Cofomo, Everforth render little JobPosting JSON-LD; LinkedIn Guest + Workday remain the reliable Toronto signal.
- Toronto employer signals this run: **Bell/Ateko** (ServiceNow ITOM/ITAM Architect, Quebec), **TD/CIBC/BMO/KPMG/Interac/407 ETR** (GTA ServiceNow), **Salesforce vendor** (Solutions Architect Migrations, Data360/Revenue Cloud), **Salvation Army Canada** (ITSM Analyst, Toronto via Workday).


## 23:00 EST hourly run — 2026-11-08 (third run today)

**Scan executed:** web search (LinkedIn guest snippets, Indeed CA snippets) + direct source fetches (careers.servicenow.com, careers.salesforce.com, ateko.com careers). Adzuna/Indeed APIs unavailable keyless this cycle; LinkedIn job pages are behind a login wall so posted dates could not be confirmed by direct fetch.

**Fresh postings verified (dated, live, URL absent from README.md) and merged into the ServiceNow table:**
| Posted | Role | Company | Location | Source / note |
|---|---|---|---|---|
| 2026-11-06 | [Staff Security Engineer \| Security Engineering](https://careers.servicenow.com/jobs/744000160294642/staff-security-engineer-security-engineering/) | ServiceNow | Toronto, ON | ServiceNow Careers (vendor direct); verified live Nov 08 2026 |
| 2026-11-05 | [Senior Site Reliability Engineer, Canada Protected B](https://careers.servicenow.com/jobs/744000159911194/senior-site-reliability-engineer-canada-protected-b/) | ServiceNow | Toronto, ON | ServiceNow Careers (vendor direct); supports Government of Canada Protected B; verified live Nov 08 2026 |

**Duplicates skipped (already on the board from the 19:00 EST run):**
- Staff Systems Engineer — ServiceNow — Toronto, ON — 2026-11-06 (careers.servicenow.com)
- Senior Staff Security Engineer \| Systems Engineering — ServiceNow — Toronto, ON — 2026-11-06 (careers.servicenow.com)
- Salesforce Developer Lead – Data Cloud — Epsilon Solutions Ltd. — LinkedIn (already on board)

**New but undated — deferred to next run (board rule: no absolute YYYY-MM-DD, no table row):**
- Sr. IT Developer (ServiceNow) — TD — Toronto (ca.linkedin.com/jobs/view/sr-it-developer-servicenow-at-td-4177846836)
- ServiceNow Solutions Engineer — Manulife — Toronto (…at-manulife-4181837609)
- ServiceNow Solutions Architect – APM & Service Mapping — Scotiabank — Toronto (…at-scotiabank-4092080311)
- ServiceNow Administrator & Developer (Hybrid) — Central 1 — Toronto (…at-central-1-4215919730)
- Technical Specialist – ServiceNow Platform — BMO — Toronto (…at-bmo-4179502423)
- Service Now Consultant — Compunnel Inc. — Toronto (…at-compunnel-inc-4203121945)
- Associate, Salesforce (1-yr contract) — MaRS Discovery District — Toronto (…at-mars-discovery-district-4189742431)
- Senior Salesforce Engineer — Scotiabank — Toronto (…at-scotiabank-4105474889)
- Account Executive – Data Cloud — Salesforce — Toronto (…at-salesforce-4231733063)

**Salesforce:** vendor careers page showed sales/operations postings dated September–October 2026 (outside the fresh window); no new dated technical Salesforce Toronto roles this cycle.

**Partners / telco / sponsors / government checked:**
- Ateko (ServiceNow + Salesforce partner, backed by Bell Canada): careers page live; its jobs.ca postings dated Oct 3–16 2026 — known, not fresh.
- Rogers / Bell / TELUS direct careers: no fresh ServiceNow/Salesforce Toronto hits this cycle.
- Canadian government: ServiceNow Canada "Protected B" federal roles are the two senior security/SRE roles merged above (both support Government of Canada Protected B workloads).

**Merge result:** ServiceNow table 709 → 711 rows; board total 5395 → 5397 live postings. Commit 403320eb942e… pushed to main; `pages.yml` rebuilds https://eltonaguiar.github.io/BESTIEJOB/ on the push.


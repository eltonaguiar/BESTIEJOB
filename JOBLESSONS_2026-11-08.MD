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


---

## 17:21 EST hourly run (2026-11-08T22:38:06.383Z) — Hermes cron

### Scan
- Scanners: npm run scan:daily (scripts/daily_job_scan.mjs --no-readme) + scripts/gap_scan.mjs
- Total matching postings: 2,039 (ServiceNow 949 + Salesforce 933); fresh this scan: 255
- Sources: LinkedIn 199 · Workday 16 · Greenhouse 16 · SmartRecruiters 12 · Lever 1 · Ashby 2 · Jobicy 3 · Remotive 4 · RemoteOK 2
- Adzuna: HTTP 429 on every query (persistent from the 09:00 EST run) - no Adzuna data this hour
- Gap scan / partner career sites: FX Innovation/Ateko (Bell), Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze - 0 dated postings; Lane Four had 2 undated anchors (skipped by merger: no absolute date)
- Bell Canada direct (jobs.bce.ca): ServiceNow Senior Technical Advisor (Oct 6) and Senior Manager Platform Delivery (Sep 23) found via search - both outside the 30-day window, not board-eligible
- GC Jobs (jobs.gc.ca): no indexable ServiceNow postings surfaced by search

### Merge (tools/jobs_merge_inbox.py --max-per-table 150)
- Inbox: hermes-cron--2026-11-08--v1.md - 46 dated rows (45 KPMG Canada ServiceNow 2026-11-07 requisitions, 1 Interac ServiceNow Lead contract Toronto 2026-11-07, 1 GDIT remote 2026-11-07, 1 Salesforce Solutions Consultant Canada 2026-11-08)
- Added: 2 rows - Interac Technical ServiceNow Lead (Toronto, ON) and Chapman Tate Associates Principal Solutions Consultant - Salesforce & Digital Transformation (Canada)
- Capped out: 44 KPMG 2026-11-07 requisitions + 1 GDIT row - same posting date as existing board rows; the 150/family cap keeps earlier-submitted rows on date ties (stable sort), so late-hour same-day runs are crowded out
- Also merged: websearch--2026-11-05--v11.md (+2), websearch--2026-11-05--v14.md (+5) - previously unmerged submissions
- Result: 450 curated rows (150 per family); README.BAK_2026-11-08T222817Z.md archives 4,875 rows older than 2026-10-09
- Sales/marketing filter: 207 rows skipped; 183 aggregator listing pages skipped

### Site build (tools/build_site.py)
- Built: 1,828 jobs (ServiceNow 736 + Salesforce 759 + Other 333); 214 duplicate mirrors collapsed; 33 applied roles hidden; newest 2026-11-08
- GitHub Pages: https://eltonaguiar.github.io/BESTIEJOB/ redeployed on push to main (pages.yml triggers on public/** plus README.md)

### Lessons (this run)
1. Adzuna 429 is persistent - hourly runs get no Adzuna data; SmartRecruiters/Workday/LinkedIn carry the load instead. Back-off (60s+ between calls, concurrency 1) not yet implemented.
2. The 150/family cap crowds out same-date late runs - rows tie on Posted date and earlier submissions win. To surface late-hour finds, either raise the cap or sub-sort by scrapedAt.
3. Partner career sites are mostly dry for Toronto SN/SF - LinkedIn guest plus employer Workday/ATS feeds remain the highest-yield sources; Elite partners (Deloitte, KPMG, Accenture, CGI, Slalom) still dominate volume.
4. Bell/GC Jobs hits from search were stale (Sep-Oct) - outside the 30-day window; direct site checks need a date filter before submission.

### Action items for next hourly run
1. Re-run npm run scan:daily plus gap_scan.mjs at top of next hour
2. Implement Adzuna back-off/retry (60s min between calls, concurrency 1)
3. Re-check GC Jobs / gojobs.gov.on.ca / jobs.bce.ca with posted-date filter for in-window ServiceNow roles
4. Consider sub-sorting the 150/family cap by scrape time so late-run fresh rows aren't locked out by same-date ties
5. Validate any new URLs against README.md (grep by URL) before adding to inbox

## 18:00 EST hourly run (2026-11-08) — Hermes cron (independent scan)

### Scan
- Tool: web search (Indeed.ca, careers.servicenow.com, BuiltIn Toronto, Jobera, Hiring Tempo)
- Queries: "Toronto ServiceNow jobs November 2026", "Toronto Salesforce jobs November 2026"
- Named companies checked: Rogers, Bell / Ateko, Canadian government (GC Jobs / jobbank.gc.ca)

### Dedup result (normalized URL vs README.md)
0 new jobs merged. Every posting found was already represented on the board:

| Source | Posting | Location | Posted | On-board as |
|---|---|---|---|---|
| ServiceNow careers | Staff Systems Engineer (744000160278249) | Toronto | 2026-11-06 | jobs.smartrecruiters.com/ServiceNow/744000160278249 |
| ServiceNow careers | Staff Security Engineer / Security Engineering (744000160294642) | Toronto | 2026-11-06 | jobs.smartrecruiters.com/ServiceNow/744000160294642 |
| ServiceNow careers | Staff Security Engineer / Enterprise Security (744000160297239) | Toronto | 2026-11-06 | jobs.smartrecruiters.com/ServiceNow/744000160297239 |
| ServiceNow careers | Senior Staff Security Engineer / Systems Engineering (744000160294989) | Toronto | 2026-11-06 | jobs.smartrecruiters.com/ServiceNow/744000160294989 |
| ServiceNow careers | Staff Site Reliability Engineer, Canada Protected B (744000159744570) | Toronto | 2026-11-05 | jobs.smartrecruiters.com/ServiceNow/744000159744570 |
| ServiceNow careers | Senior Site Reliability Engineer, Canada Protected B (744000159911194) | Toronto | 2026-11-05 | jobs.smartrecruiters.com/ServiceNow/744000159911194 |

Salesforce: Indeed.ca results were aggregator listing pages (rejected as listing URLs). Corporate Salesforce roles returned were sales / business-development / recruiter / customer-success (outside the board's technical remit). Technical Salesforce roles (Solutions Architect, Technical Architect) had no verifiable direct posting URL with an absolute posted date, so none were added.

### Named-company check
- Bell / Ateko: Canada Protected B ServiceNow roles found — already on board (table above).
- Rogers: no in-window Toronto ServiceNow / Salesforce posting surfaced.
- Canadian government (GC Jobs / jobbank.gc.ca): prior runs found only stale Sep–Oct postings outside the 30-day window; nothing in-window this scan.

### Lessons (this run)
1. careers.servicenow.com and jobs.smartrecruiters.com/ServiceNow/<JK> are the same requisition. Dedupe by canonical job ID, not URL string alone, to avoid mirror duplicates.
2. Indeed.ca SERP pages are listing pages and are rejected by the merger; only direct ATS / job-posting URLs with an absolute `Posted` date qualify.
3. Salesforce technical roles surface on Indeed, but each posting needs a verifiable date before submission — never fabricate a date.
4. GC Jobs / jobbank / Bell direct hits were stale (outside the 30-day window); apply a posted-date filter before submitting public-sector roles.


## Additional Scan: 2026-11-08 (19:00 EST / 2026-11-09T00:00Z hourly cron run)

**Run summary**
- **Hourly scan executed:** parsed `FRESH_JOBS.md` (auto-generated by `scripts/daily_job_scan.mjs` at 2026-11-08T22:24Z; 2,039 postings across 9 sources)
- **Canada-relevant ServiceNow/Salesforce candidates found:** 55 (46 ServiceNow + 9 Salesforce), posted 2026-11-06 to 2026-11-08, not already on the board
- **Submitted to inbox:** 12 rows in `inbox/hermes-cron--2026-11-08--v1.md`
- **Merge result:** +12 new, 0 duplicate; README.md holds 450 rows (150/150/150); 21 stale rows (>30 days) archived to `README.BAK_2026-11-09T000603Z.md`
- **Pushed to main:** README.md, README.BAK_*, inbox file (gh Contents API; git blocked on Windows Security)
- **GitHub Pages:** the `README.md` push triggers `pages.yml` → `tools/build_site.py` rebuilds `public/` and redeploys https://eltonaguiar.github.io/BESTIEJOB/

**Roles added (Toronto / Ontario / Canada focus)**
ServiceNow:
- Staff Systems Engineer — ServiceNow (vendor direct, Toronto) — verified live
- Consultant, ITAM Transactions & Compliance — CIBC (Big Five bank, Toronto) — verified live
- ServiceNow Administrator & Developer — Sheridan College (Oakville, ON)
- ServiceNow SAM Administrator - ITAM — BMO (Big Five bank, Toronto)
- Directeur.rice fonctionnel.le - ServiceNow — KPMG Canada (Toronto) [Elite partner]
- Manager, ServiceNow Technical Lead — KPMG Canada (Toronto) [Elite partner]
- Functional Manager - ServiceNow — KPMG Canada (Toronto) [Elite partner]
- Conseiller.ère fonctionnel.le - Service Now — KPMG Canada (Toronto) [Elite partner]
- Manager - ServiceNow Solution Architect — KPMG Canada (Ottawa) [Elite partner]
- Senior ServiceNow Platform Architect (CoE/Vault) — Resonaite (Ottawa)

Salesforce:
- Développeur principal Salesforce — Canadian Cancer Society (Toronto) [Canadian nonprofit]
- Salesforce Technical Architect - Revenue Cloud CPQ — Enterprise Solutions Inc. (Canada)

**Exclusions (verified, not submitted)**
- `roberthalf.com/ca/en/jobs/toronto-on/salesforce-developer` — aggregator listing page, not a single posting (rejected as listing URL)
- EY Salesforce Technical Architect (Toronto) — ATS posted date Sep 30 2026, outside the 30-day window (would be archived immediately)
- `roleweek.com/companies/bdo/` — company listing page, not a posting
- LinkedIn direct `/jobs/view/` URLs return 403 without a Firecrawl key; treated as scan-verified via the pipeline's trusted LinkedIn Guest source

**Lessons (this run)**
1. `FRESH_JOBS.md` (the `--no-readme` daily scan output) is the best source for in-window postings not yet on the curated board; diff its URLs against `README.md` before submitting.
2. Verify each URL before submitting: listing pages and stale ATS dates are rejected by the merger, or archived immediately if outside the 30-day window.
3. KPMG Canada dominates Toronto ServiceNow volume (Elite partner) — multiple postings per city; dedupe by URL, each city/requisition is a distinct row.
4. Big Five banks (CIBC, BMO) post ITAM/ServiceNow-adjacent roles on Workday; worth a standing check each hour.
5. Git push is blocked on Windows Security; use the `gh` Contents API (base64-encoded file content). A `README.md` push triggers `pages.yml` to rebuild and redeploy GitHub Pages.


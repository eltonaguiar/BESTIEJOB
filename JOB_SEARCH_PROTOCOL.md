# BESTIEJOB — Job Search Protocol

**Generated:** 2026-11-02T15:30:00Z  
**Agent:** Kilo (nvidia/nemotron-3.5-super-vl:free via Kilo Gateway)  
**Repository:** eltonaguiar/BESTIEJOB (main branch)  
**Live site:** https://eltonaguiar.github.io/BESTIEJOB/

---

## Purpose

A repeatable, auditable protocol for finding ServiceNow, Salesforce, and "other" resume-relevant IT jobs in Toronto/Canada, tracking them in BESTIEJOB's README, and keeping the live site current. Designed for a human operator to execute manually or with light automation.

---

## Target roles (by category)

### ServiceNow
Developer, Administrator, Architect, Business Analyst, Technical Lead, Implementation Consultant, ITOM/ITSM/ITAM/CMDB/Discovery/HR/SPM/CSM/GRC/SecOps/Now Assist specialist.

Keywords: ServiceNow, CSA, CAD, CIS, ITOM, ITAM, CMDB, Discovery, Service Mapping, Flow Designer, Business Rules, Script Includes, UI Policy, Integration Hub, MID Server, Now Assist, Virtual Agent, Agentforce, CSDM.

### Salesforce
Developer, Administrator, Architect, Consultant, Technical Lead, Platform Engineer, FSC/CPQ/Marketing Cloud/Service Cloud/Data Cloud/Agentforce specialist.

Keywords: Salesforce, Apex, SOQL, LWC, Visualforce, Flow, Process Builder, CPQ, Revenue Cloud, FSC, Marketing Cloud, Service Cloud, Data Cloud, Agentforce, Einstein, MuleSoft, Copado, GitLab, DevOps Center.

### Other (resume-relevant keywords)
PowerShell, VBA/Excel, Alteryx, Python, SQL Server, Tableau, Power BI, JIRA, Confluence, ITAM, ITOM, GitHub/CI-CD, Data Analyst, BI Engineer, Data Engineer, Systems Administrator.

---

## Protocol phases

### Phase 0 — Preparation (once, then as needed)

1. **Confirm API keys** are available in the path set by `DBPASSES_FILE` (default: `$HOME/dbpasses.txt`):
   - OpenRouter key (`sk-or-v1-...`) — used to generate search queries and scrutinize results
   - DeepSeek key (`sk-0a01...`) — alternate model for query generation / second opinion
   - No dedicated search API keys (Brave/Tavily/Serper/Google CSE) found; rely on websearch tool + direct site scraping
2. **Verify aliveness** of each key with a minimal chat completion before starting a scan round.
3. **Checkout `main`** and pull latest: `git checkout main && git pull origin main`
4. **Review the live site** at https://eltonaguiar.github.io/BESTIEJOB/ to confirm data freshness.

### Phase 1 — Scan (per round)

#### 1a. Automated scan (Adzuna CA API)
Run `scripts/daily_job_scan.mjs` (or equivalent) against Adzuna CA:
- Keywords: ServiceNow, Salesforce + secondary tags (vba, alteryx, full-stack, data, devops, python)
- Geo: Toronto, Ontario, Canada + remote
- `max_days_old=14`, `sort_by=date`, `results_per_page=25`
- Output: `jobs.json` + `public/jobs-data.json` + `FRESH_JOBS.md`

#### 1a-bis. Free-AI keyword proposals (`tools/ai_panel.py`)
`scripts/daily_scan.sh` runs this automatically right before `gap_scan.mjs`:

```bash
python3 tools/ai_panel.py ping                       # which free peers answer today
python3 tools/ai_panel.py queries --count 12 \
  --out raw/ai_queries.json                          # new Adzuna `what` variants
python3 tools/ai_panel.py triage --input <jobs>.json  # second-opinion on ambiguous rows
```

Peers are tried local (`:8000`/`:11434`/`:4000`) → keyless (Kilo, Pollinations, LLM7, OVH)
→ keyed free tiers (Groq, Gemini, Cohere, Mistral, SiliconFlow, …). Keys come from
`~/dbpasses.txt` and are never printed. **Proposals are hypotheses only:** the panel and
`gap_scan.mjs` both drop anything that isn't a 2–4 word keyword, and no date, salary, or
company ever comes from a model. A failed panel is non-fatal — the static list still runs.

The same script reviews the inbox:

```bash
python3 tools/ai_panel.py triage-inbox --limit 20
```

It reads `inbox/*.md`, takes the rows whose Posted cell is an undated marker, and writes
`inbox/_ai-triage--<date>--v<N>.md` — a verdict table (`servicenow` / `salesforce` /
`other` / `reject` plus the peers' reasons). The leading underscore makes the merger and
`check_inbox.py` ignore it, so a review report can never become a submission or acquire a
date. Read it before opening the raw inbox files.

#### 1a-ter. Web search (`scripts/web_search_scan.py`)

Real search, not aggregator scraping: Tavily (×2 keys), Exa and Firecrawl, 8 job-focused
queries each, results filtered against board **category** pages ("ServiceNow Developer
Jobs in Toronto (500 Open Roles)" is not a posting), then keyword + geo + dedupe.

**A date comes only from the page** (`datePosted` JSON-LD, `article:published_time`,
`itemprop=datePosted`). No date means an em dash and an `inbox/` row the merger skips.
Most web-search hits are undated — treat this source as a review queue, not a feed.

#### 1b. Web search (per category)
Run 3-6 targeted web searches per category using the websearch tool:

**ServiceNow queries:**
- `ServiceNow developer administrator jobs Toronto Canada November 2026 site:ca.indeed.com OR site:ca.linkedin.com OR site:workopolis.com OR site:jobbank.gc.ca`
- `ServiceNow ITOM ITAM CMDB Discovery HR SPM jobs Toronto Canada November 2026`
- `ServiceNow jobs site:careers.bmo.com OR site:jobs.td.com OR site:careers.scotiabank.com OR site:careers.cibc.com OR site:jobs.rbc.com`
- `ServiceNow jobs site:jobs.bell.ca OR site:jobs.rogers.com OR site:jobs.bell.ca OR site:careers.bell.ca`
- `ServiceNow jobs site:dayforce.com OR site:shopify.com OR site:lightspeed.com OR site:kinaxis.com`
- `ServiceNow jobs site:manulife.com OR site:sunlife.com OR site:canadalife.com OR site:intact.ca`
- `ServiceNow jobs site:careers.microsoft.com OR site:amazon.jobs OR site:careers.google.com` — Big Tech Toronto presence (added post-scrutiny)

**Salesforce queries:**
- `Salesforce developer administrator architect jobs Toronto Canada November 2026 site:ca.indeed.com OR site:ca.linkedin.com OR site:workopolis.com OR site:jobbank.gc.ca`
- `Salesforce CPQ Marketing Cloud Service Cloud jobs Toronto Canada November 2026`
- `Salesforce jobs site:careers.bmo.com OR site:jobs.td.com OR site:careers.scotiabank.com OR site:careers.cibc.com OR site:jobs.rbc.com`
- `Salesforce jobs site:jobs.bell.ca OR site:jobs.rogers.com OR site:jobs.bell.ca`
- `Salesforce jobs site:docebo.com OR site:altusgroup.com OR site:benevity.com`
- `Salesforce jobs site:careers.microsoft.com OR site:amazon.jobs OR site:careers.google.com` — Big Tech Toronto presence (added post-scrutiny)

**Other keyword queries:**
- `VBA PowerShell Alteryx Python SQL Tableau Power BI jobs Toronto Canada November 2026 site:ca.indeed.com OR site:ca.linkedin.com OR site:workopolis.com`
- `Jira Confluence ITAM ITOM GitHub CI CD jobs Toronto Canada November 2026`
- `Data Analyst BI Engineer Tableau Power BI jobs Toronto Canada November 2026`

#### 1c. Partner ecosystem scan
Check careers pages of Salesforce/ServiceNow consulting partners:
- Lane Four (lanefour.com/opportunities) — Salesforce boutique, Toronto
- CloudJunction / CloudJunction Advisors (cloudjunction.cloud/careers) — Salesforce Select partner, Toronto
- Diabsolut (diabsolut.com/careers) — Salesforce Summit Partner, Montreal/Toronto
- Altus Group (altusgroup.wd3.myworkdayjobs.com) — Salesforce Platform, Toronto
- Docebo (jobs.ashbyhq.com/docebo) — Salesforce, 55 York St near Eaton Centre

#### 1d. Downtown Toronto / Eaton Centre area scan
Focus on M5G 2H5 / 55 Centre Avenue and Eaton Centre vicinity:
- Companies near downtown Toronto core: Docebo (55 York St), Bell, Rogers, banks, consulting firms
- Search: `ServiceNow Salesforce jobs downtown Toronto Eaton Centre M5G 2H5 November 2026`
- Search: `IT Reporting IT Asset Management jobs downtown Toronto November 2026`

### Phase 2 — Dedupe & validate

1. **Dedupe by URL** — normalize URLs (strip query strings, `utm_*`, trailing slashes). Skip if URL already in README.
2. **Validate liveness** — for employer-ATS postings (careers.bmo.com, jobs.rbc.com, etc.), confirm HTTP 200 on the posting URL. Mark unverified aggregator mirrors.
3. **Date assignment** — use explicit posted date (YYYY-MM-DD) where available; mark "Not disclosed" if absent. Relative ages ("2 days ago") are NOT accepted without conversion to a date.
4. **Category assignment** — ServiceNow / Salesforce / Other based on keywords in title + description.

### Phase 3 — Update README

1. **Edit `README.md`** — add new rows to the appropriate table (ServiceNow / Salesforce / Other), sorted newest-first within each table.
2. **Update "Last updated" timestamp** in header (P0 enhancement — see docs/SUGGESTED_ENHANCEMENTS.md).
3. **Run merge script** if using the inbox workflow: `python3 tools/jobs_merge_inbox.py`
4. **Commit** with descriptive message: `docs(README): add <N> new <category> jobs from <source>`
5. **Push to main**: `git push origin main` (note: remote is `git@github.com:eltonaguiar/BESTIEJOB.git`)

### Phase 4 — Verify live site

1. **Confirm** https://eltonaguiar.github.io/BESTIEJOB/ reflects new jobs (GitHub Pages may have a brief delay).
2. **Check** that the "Last updated" timestamp is present and correct.
3. **Spot-check** 2-3 job URLs open correctly.

---

## Frequency

| Cadence | Action |
|---------|--------|
| Daily (weekdays) | Phase 1a automated scan + Phase 1b web search (3 queries per category) |
| Weekly | Full Phase 1 (all queries) + Phase 1c partner ecosystem + Phase 1d downtown Toronto |
| Per round | Phase 2-4 (dedupe, validate, update README, push, verify) |

---

## Quality rules

- **Never fabricate** posting dates, salaries, or company names. If unknown, mark "Not disclosed."
- **Never commit secrets** — API keys in dbpasses.txt are never committed to the repo.
- **Always verify employer-ATS URLs** return HTTP 200 before adding.
- **Always dedupe by URL** — normalized (strip query strings, utm_*, trailing slash).
- **Always sort newest-first** within each category table.
- **Prefer employer-ATS sources** over aggregator mirrors for reliability.

---

## Files touched per round

- `README.md` — job tables + last-updated timestamp
- `public/jobs-data.json` — rebuilt from README (via merge script)
- `jobs.json` — raw scan output
- `FRESH_JOBS.md` — human-readable fresh jobs summary
- `docs/SUGGESTED_ENHANCEMENTS.md` — update if new feature ideas emerge
- This protocol (`JOB_SEARCH_PROTOCOL.md`) — update after scrutiny review

---

## Scrutiny log

| Date | Reviewer | Finding | Action |
|------|----------|---------|--------|
| 2026-11-02 | Kilo (self) | Initial draft | Pending external scrutiny |
| | | | |

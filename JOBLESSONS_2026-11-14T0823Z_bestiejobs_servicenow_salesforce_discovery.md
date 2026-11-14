# BESTIEJOB ServiceNow / Salesforce Discovery and Pattern Audit

**Worktree:** `bestiejobs`
**Generated:** 2026-11-14T08:23Z
**Scope:** ServiceNow and Salesforce developer, administrator, architect, consultant, and analyst roles in Toronto, the surrounding GTA, Ontario, and Canada-remote.
**Primary data:** live board feed `public/jobs-data.json` (5,133 cards, generated 2026-11-14T07:36Z), `jobs.json` (2,650 rows, 07:11Z), current `README.md` tables (6,782 rows), and a fresh Adzuna / Job Bank / Eluta scan. SubQ Snap 1.2 was used for document comparison and structured decisions.

---

## 1. Executive summary

- The board is not one dataset. Four stores disagree materially: README current tables have **6,782 rows**, `jobs.json` has **2,650**, and the live site renders **5,133 cards**. README headings still say **2,700 live postings** and **Other jobs (169)** while the Other table has **4,201 rows**.
- ServiceNow supply is developer-heavy and ranked high: **907** live ServiceNow cards, **328** developer-titled rows, median resume-fit **84**, **793** rows at or above 70.
- Salesforce supply is comparable (**962** cards, **383** developer-titled rows) but is suppressed by the profile: median fit **56**, only **23** rows at or above 70, and **0** at or above 85. For developer-only Toronto/GTA/remote rows: ServiceNow median **88** vs Salesforce **60**.
- The cause is visible in `tools/build_site.py`: ServiceNow gets 34 points; ITSM, ITAM, CMDB, ITOM add 50 more; Salesforce gets a single 20-point line and no cloud/Apex/LWC weights. The site's Best Match view (≥70) contains **816 rows: 793 ServiceNow and only 23 Salesforce (97.2% / 2.8%)**. SubQ puts the probability of a systematic Salesforce under-score at **0.999** and recommends a separate Salesforce lens (**0.89**).
- Aggregators are the freshness channel, not the verification channel. ServiceNow rows posted in the last 3 days: **138** aggregator vs **37** employer-board. Salesforce: **173** vs **18**. Employer boards are more trustworthy but often stale (Greenhouse: 1 of 42 ServiceNow rows and 4 of 46 Salesforce rows were 7 days old or newer).
- The keyword classifier has measurable false positives: **67** ServiceNow-family rows are generic ITSM/ITAM roles with no explicit ServiceNow token; **35** are ServiceNow-vendor SRE/security/DevOps/sales roles; Salesforce-family rows include Oracle APEX, Apex Systems, and Apex Legends matches.
- The fresh scan found many rows but almost no genuinely new roles. After canonical employer+title dedupe, **0 of 23** primary-geo fresh candidates were new to the board; they were mirrors of existing employer rows. Across the completed lanes and the fresh scan, **63** unique candidates collapsed to **9** new candidates, several of which are still caveated.
- Liveness is perishable. Of **48** current employer roles re-checked, **13 (27.1%)** were dead, expired, or origin-down, and **9 (18.8%)** were definitively dead (404/410/dead-text). The `verified` badge on the board means "employer vs aggregator", not "live now".
- The strongest methodology combination is **P4 freshness scan + P1 verification protocol + P3 weekly untried-source expansion** (SubQ 0.76). Daily mode should be freshness-first (0.72), direct ATS weekly (0.59), staffing as a separate lane (0.93), with explicit developer (0.94) and Canada-remote (0.96) filters.
- The highest-value fixes are: a Salesforce lens, count reconciliation with a CI assertion, classifier guards, unknown-row quarantine, and a re-verification loop. These are user-facing correctness issues, not cosmetic ones.

---

## 2. How the current board is fed

| Stage | Script / artifact | What it contributes |
|---|---|---|
| Freshness scan | `scripts/fresh_ca_scan.py` (Adzuna + Job Bank + Eluta) | Today/yesterday rows, absolute dates, drops URLs that do not answer |
| Breadth scan | `scripts/daily_job_scan.mjs` (SmartRecruiters, Workday, Greenhouse, Lever, Ashby, LinkedIn, RemoteOK, Jobicy, Remotive, Adzuna) | Fills 7–45 day windows |
| Agency lane | `scripts/agency_board_scan.py`, `config/agency_boards.json` | Staffing portals and contract roles |
| ATS sweep | `scripts/ats_board_sweep.py` and related probes | Dated public feeds per employer |
| Stores | `jobs.json`, `README.md`, `public/jobs-data.json` | Scan system of record, rendered view, site feed |
| Site build | `tools/build_site.py` | Union of `jobs.json` + README, URL dedupe, employer+title clustering, APPLIED hidden, dead-URL blocklist, per-row match score |

The site build is the right architecture: `jobs.json` leads and README rows survive only where the JSON does not know them. The weakness is that the three outputs are produced at different times, with different windows and classifiers, and nothing asserts that their counts agree.

---

## 3. Pattern analysis

### 3.1 Volume and role mix

| Metric | ServiceNow | Salesforce |
|---|---:|---:|
| Live cards | 907 | 962 |
| Developer-titled | 328 | 383 |
| Architect | 156 | 187 |
| Consultant | 102 | 68 |
| Analyst | 88 | 59 |
| Manager / lead | 76 | 85 |
| Administrator | 38 | 71 |
| Specialist / SME | 44 | 22 |
| Sales / alliance / marketing | 7 | 15 |
| Unspecified seniority | 550 | 657 |
| Senior / lead in title | 336 | 269 |
| Junior / mid in title | 12 | 18 |
| Director+ in title | 9 | 18 |

ServiceNow is a developer and architect market. Salesforce is more balanced across developer, architect, administrator, and manager titles, with a much larger staffing-agency component.

### 3.2 Geography

| Geography bucket | ServiceNow | Salesforce |
|---|---:|---:|
| Toronto / GTA | 279 (31%) | 409 (43%) |
| Canada, no city | 216 (24%) | 209 (22%) |
| Other Canada | 129 (14%) | 144 (15%) |
| Remote stated | 51 (6%) | 66 (7%) |
| Unknown / blank | 64 (7%) | 40 (4%) |
| Other / unparsed | 151 (17%) | 61 (6%) |
| US / other | 17 (2%) | 33 (3%) |

Developer-only rows sharpen the picture:

| Developer geography | ServiceNow | Salesforce |
|---|---:|---:|
| Toronto / GTA | 107 | 176 |
| Canada, no city | 56 | 81 |
| Remote stated | 28 | 19 |
| Other Canada | 29 | 32 |
| Unknown / other / US | 108 | 75 |

"Canada" without a city is a quarter of the board. It is usually country-wide, but remote eligibility is not verified. Only 6–7% of rows explicitly say remote.

### 3.3 Sources and freshness

| Source | SN rows | SN ≤7 days | SF rows | SF ≤7 days | Interpretation |
|---|---:|---:|---:|---:|---|
| LinkedIn | 208 | 87 | 299 | 117 | Broad and fresh; rate-limits after ~4 rapid calls |
| Adzuna | 132 | 66 | 230 | 95 | Fresh, but mirrors employer rows |
| Workopolis | 43 | 41 | 29 | 29 | Unexpectedly fresh; under-promoted |
| Workday ATS | 47 | 15 | 42 | 8 | Verifiable but often stale |
| Greenhouse | 42 | 1 | 46 | 4 | Very stale for these employers |
| jobs.ca | 35 | 2 | 45 | 0 | Stale mirrors |
| careers.servicenow.com | 31 | 23 | — | — | Vendor engineering/sales, not all practitioner |
| SmartRecruiters | 24 | 7 | — | — | ServiceNow vendor roles |

By verification class:

| Family / class | Rows | Posted ≤3 days | 4–7 days | 8–14 days | >14 days |
|---|---:|---:|---:|---:|---:|
| ServiceNow aggregator | 480 | 138 | 60 | 192 | 90 |
| ServiceNow employer board | 427 | 37 | 32 | 239 | 119 |
| Salesforce aggregator | 661 | 173 | 73 | 254 | 161 |
| Salesforce employer board | 301 | 18 | 24 | 169 | 90 |

The practical rule: **use aggregators to discover, use employer ATS to confirm**. A daily freshness scan that only reads employer boards will miss most same-day rows; a scan that only reads aggregators will surface mirrors and expired postings.

### 3.4 Employer and channel mix

Practitioner rows in Toronto/GTA, Ontario, or Canada-remote:

| Bucket | ServiceNow | Salesforce |
|---|---:|---:|
| Other / long-tail employer | 174 (33%) | 273 (42%) |
| Unknown company | 126 (24%) | 97 (15%) |
| Consultancy / partner | 83 (16%) | 97 (15%) |
| End employer | 58 (11%) | 55 (8%) |
| Staffing / agency | 50 (10%) | 116 (18%) |
| Vendor (platform) | 33 (6%) | 18 (3%) |
| Total | 524 | 656 |

Developer-only staffing share is higher for Salesforce (**52 of 273, 19%**) than ServiceNow (**20 of 190, 11%**). The Salesforce contract market runs through agencies more than the ServiceNow market does.

Concentration is high at the top:

- ServiceNow: Unknown 127, ServiceNow 31, Deloitte 23, CGI 19, KPMG Canada 17, Accenture Federal 17, jobgether 11, Alldus 10, Cognizant 9, BMO 7, GDIT 7, TCS 7, NewRocket 7, BDO 6, Scotiabank 6.
- Salesforce: Unknown 103, Salesforce 25, Cognizant 18, NeuraFlash 16, jobgether 11, Epsilon Solutions 11, Smart IT Frame 10, Pacer Group 9, Deloitte 9, TCS 8, Acestack 8, LTM 7, Capgemini 7, CGI 7, J&M Group 7.

### 3.5 Demand signals in titles and notes

| ServiceNow signal | Mentions | Salesforce signal | Mentions |
|---|---:|---|---:|
| ITSM | 89 | Marketing Cloud | 55 |
| ITAM | 40 | Revenue Cloud | 39 |
| ITOM | 35 | CPQ | 30 |
| CMDB | 22 | Agentforce | 23 |
| GRC | 21 | Data Cloud | 22 |
| SAM | 21 | FSC | 18 |
| CSM | 19 | Apex | 12 |
| HRSD | 14 | nCino | 9 |
| HAM | 13 | LWC | 8 |
| SecOps | 10 | OmniStudio | 4 |
| SPM | 10 | | |

Caveat: these are title+note mentions, not full-job-description counts. They are directional, not a skills census.

### 3.6 Match-score bias

| Metric | ServiceNow | Salesforce |
|---|---:|---:|
| All rows, median fit | 84 | 56 |
| All rows ≥70 | 793 | 23 |
| All rows ≥85 | 386 | 0 |
| Developer rows (TO/GTA/remote/Canada unique) | 190 | 274 |
| Developer median fit | 88 | 60 |
| Developer ≥70 | 172 | 4 |
| Developer ≥85 | 105 | 0 |

`tools/build_site.py` weights:

| Signal | Points |
|---|---:|
| ServiceNow | 34 |
| ITSM | 13 |
| ITAM | 13 |
| CMDB | 13 |
| ITOM | 11 |
| Flow Designer | 9 |
| ServiceNow scripting | 9 |
| Integration | 9 |
| Salesforce | 20 |
| ITIL | 8 |
| JavaScript | 7 |
| Data / reporting | 6 |

There is no Salesforce cloud, Apex, LWC, CPQ, Marketing Cloud, Data Cloud, Agentforce, or FSC weight beyond the single 20-point Salesforce line. A Salesforce-only developer cannot reach the ServiceNow band.

The user-facing consequence is the Best Match view:

| Best Match composition (match ≥70) | Rows | Share |
|---|---:|---:|
| ServiceNow | 793 | 97.2% |
| Salesforce | 23 | 2.8% |
| Total | 816 | 100% |

Of the 23 Salesforce rows, most are business analysts, consultants, or integration architects. Only a handful are developer-titled. The Best Match tab is effectively a ServiceNow tab.

SubQ decision on this evidence: **scoring bias exists 0.999**, best fix is a **separate Salesforce lens 0.89**, and the top action is **fix the Salesforce profile 0.83**.

### 3.7 Classification and data-quality errors

| Issue | Evidence | Impact |
|---|---|---|
| Generic ITSM/ITAM tagged ServiceNow | 67 rows with no explicit ServiceNow token, e.g. "ITSM Reporting Specialist", "ITAM Transactions & Compliance", "Expert Freshservice ITSM / ITAM" | Cannot be confirmed as ServiceNow from the title; some are other ITSM tools (Freshservice) or generic ITAM |
| ServiceNow vendor engineering tagged ServiceNow | 35 rows: SRE, security, DevOps, database, ML, sales director at ServiceNow | Mostly not end-user platform-practitioner work; a few platform-architect roles are relevant exceptions |
| Oracle APEX tagged Salesforce | "Senior Oracle APEX & Database Administrator" at Stantec | Clear false positive |
| Apex Systems / Apex Legends tagged Salesforce | 5 rows | Wrong family |
| Unknown company | 127 SN (14.0%), 103 SF (10.7%) | Cannot dedupe or verify employer |
| Duplicate identity | 4.7% SN, 6.8% SF by canonical employer+title (URL dedupe already works) | Modest inflation; site clusters alternates |
| Dead / expired rows | 13 of 48 re-checked (27.1%) were dead, expired, or origin-down | User clicks dead apply links |

### 3.8 Count drift across stores

| Store | Timestamp | Total | ServiceNow | Salesforce | Other |
|---|---|---:|---:|---:|---:|
| README current tables | window 2026-10-15..11-14 | 6,782 rows | 1,190 | 1,391 | 4,201 |
| README headings | same | says 2,700 | 1,238 | 1,293 | 169 |
| `jobs.json` | 2026-11-14T07:11Z | 2,650 | 1,114* | 1,201* | 335* |
| live `jobs-data.json` | 2026-11-14T07:36Z | 5,133 cards | 907 | 962 | 3,264 |

\* Family counts computed by applying the board's own classifier to `jobs.json`; `meta.primaryCounts` says 1,238 / 1,293.

The README's "Window: 2700 live postings" line is arithmetically wrong for its own tables. The live site is a clustered card view, so it will be smaller than row counts, but 907 ServiceNow cards vs 1,190 README ServiceNow rows is a 24% gap that is not explained by clustering alone. Part of the gap is timing: the live build at 07:36Z predates later 08:00Z commits. That timing explanation does not cover the internal README heading/table mismatch.

SubQ: counts are inconsistent at **0.999**.

---

## 4. Discovery swarm methodology applied

### 4.1 Isolation and sequence

Three lanes ran independently under `/tmp/kilo/discovery/<lane>/`. No lane wrote to the repository and no lane read another lane's draft before producing its own candidate file. All three returned candidate sets; the lead then deduped and re-verified them. The lead supplied only shared context: the live board snapshot, the methodology docs, the role definition, and the SubQ key.

Each lane followed the same sequence:

- **00 PREREQ** — can the lane reach public sources without login? Blocked sources logged.
- **01 PLAN** — window, geography, role definition, exclusions, success criteria.
- **02 CLARIFY** — what needs another source or is blocked (Workday outage, Cloudflare, SPAs).
- **03 PHASES** — source-by-source scan, one phase at a time.
- **04 QA** — liveness, absolute date, geography, role type, dedupe, SubQ classification.
- **05 FINAL** — candidate JSON plus notes, branchless and repo-safe.

### 4.2 Lanes

| Lane | Scope | Result |
|---|---|---|
| A — ServiceNow employer/partner | ServiceNow careers, banks, telcos, consultancies, partners, public sector | 2 new verified; 18 sources succeeded, 17 blocked |
| B — Salesforce employer/partner | Salesforce careers, partners, banks, insurers, product companies | 5 candidates, all already on the board; 0 new. Employer-date/work-model corrections for TD, NeuraFlash, McKesson, and PointClickCare, plus an out-of-scope Salesforce DevOps row. |
| C — Aggregators/remote/staffing | Adzuna, Job Bank, LinkedIn, Jobicy, Remotive, RemoteOK, WWR, Himalayas, Working Nomads, staffing | 33 candidates, 32 verified, 0 dead; 1,750 rejected as already on board |

### 4.3 QA gates

Every candidate had to pass:

1. **Liveness** — HTTP 200 (202 accepted for JS-rendered IBM); 403/429 kept only as botwall with a note; 404/410 rejected; 521 treated as origin-down, not proof of life.
2. **Absolute date** — YYYY-MM-DD only. Relative dates quarantined, not silently accepted.
3. **Geography** — Toronto/GTA/Ontario, or explicit Canada-remote. US-only remote rejected. Bare "Canada" kept with a country-wide caveat.
4. **Role type** — platform practitioner only; sales, marketing, recruiting, customer success, pre-sales, project/product management, QA/support excluded from developer counts.
5. **Dedupe** — normalized URL, then canonical employer + title, then SubQ title classification.
6. **Anti-fabrication** — no row without a URL and an absolute date; dates cross-checked against the employer ATS where available.

### 4.4 SubQ decisions

| Question | SubQ answer | Confidence |
|---|---|---|
| Best methodology doc for developer roles | P1 Protocol (tiered sources + ATS verification) | 0.56 |
| Biggest coverage gap | Direct employer/partner ATS | 0.36 (top) |
| Date policy | Quarantine relative dates and re-verify | 0.95 |
| First-priority source | Employer ATS | 0.65 |
| Scoring bias exists | Yes | 0.999 |
| Best fix | Separate Salesforce lens | 0.89 |
| Counts inconsistent | Yes | 0.999 |
| Top action | Fix Salesforce profile | 0.83 |
| Quarantine unknown-company rows | Yes | 0.98 |
| Salesforce developer under-coverage | Yes | 0.999 |
| Best methodology combination | P4 daily freshness + P1 verification + P3 weekly expansion | 0.76 |
| Daily mode | Freshness-first | 0.72 |
| Direct ATS cadence | Weekly | 0.59 |
| Staffing separate lane | Yes | 0.93 |
| Developer-only view | Yes | 0.94 |
| Canada-remote filter | Yes | 0.96 |

### 4.5 What worked, what did not

- **Worked:** Adzuna deep pagination (15 queries × 3 geos × 5 pages) produced the only real same-day volume; Workopolis was unexpectedly fresh; employer Workday detail endpoints gave exact `startDate`; Greenhouse `first_published` was reliable; lane isolation made blocked-source reporting clean.
- **Did not work:** Job Bank Canada silently ignored `locationstring` and returned loose full-text matches; Robert Half, Randstad, Insight Global, TEKsystems, S.i. Systems, Apex Systems, Altis, Experis, and Motion Recruitment were SPA/404/bot-walled; ServiceNow's own Workday/Phenom surfaces were intermittent; LinkedIn guest search rate-limits after ~4 rapid calls; Deloitte Canada was in maintenance; Cognizant/Thirdera/Crossfuze were Cloudflare 403.
- **Lane B result:** 5 candidates, all already on the live board. The useful output was date/work-model correction, not new rows.
- **Important:** the fresh scan's 40 kept rows looked impressive, but canonical employer+title dedupe showed all 23 primary-geo rows were mirrors of roles already on the board. Freshness is not the same as novelty.

---

## 5. Fresh and verified roles (2026-11-14)

### 5.1 Candidates that survived URL + employer/title dedupe (9)

These are the only rows from the three lanes that did not match the live board after canonical dedupe. They are candidates, not a guarantee of employer identity or remote eligibility.

| Posted | Role type | Title | Company | Location | Source | URL |
|---|---|---|---|---|---|---|
| 2026-11-11 | architect | Sr. Salesforce System Architect (CPQ) | TechDigital Group | Oakville, Halton | Adzuna | https://www.adzuna.ca/details/5961952728 |
| 2026-11-11 | developer | Salesforce Marketing Cloud Developer | Sumeru Inc | Canada | Adzuna | https://www.adzuna.ca/details/5961938966 |
| 2026-11-11 | developer | Salesforce Platform Developer | Reonomy | Toronto, Ontario | Adzuna | https://www.adzuna.ca/details/5961955838 |
| 2026-11-11 | specialist | ServiceNow SAM Specialist | Princeton IT Services | Canada | Adzuna | https://www.adzuna.ca/details/5961953431 |
| 2026-11-11 | consultant | Salesforce Consultant, Nonprofit | Passion Fruit Partners | Canada | Adzuna | https://www.adzuna.ca/details/5961942885 |
| 2026-11-11 | consultant | Managed Services - Salesforce Consultant, Nonprofit | Passion Fruit Partners | Canada | Adzuna | https://www.adzuna.ca/details/5961954188 |
| 2026-11-07 | administrator | Senior Salesforce Administrator | Make-A-Wish Foundation Canada | Toronto, Ontario | Adzuna | https://www.adzuna.ca/details/5956791140 |
| 2026-11-07 | administrator | Senior Salesforce Administrator | Equest | Toronto, Ontario | Adzuna | https://www.adzuna.ca/details/5957587771 |
| 2026-11-02 | administrator | Salesforce Business Systems Administrator | Salesloft | Anywhere in the World | We Work Remotely | https://weworkremotely.com/remote-jobs/salesloft-salesforce-business-systems-administrator |

Caveats:

- **Reonomy** is an Altus Group company; this may be the same product org as the Altus Group "Salesforce Platform Developer" already on the board. Treat as a possible duplicate.
- **Equest** is a job board; the underlying employer is not proven. Treat the employer as unverified.
- **Salesloft** is "Anywhere in the World", not Canada-specific. It is listed for completeness but excluded from the Canada-remote count.
- The two **Passion Fruit Partners** rows may be the same role posted under two titles; keep both only if the URLs resolve to distinct reqs.
- All Adzuna URLs are detail pages, not employer ATS pages. Resolve to the employer before applying.

Two additional employer-verified rows were found but are already on the board:

| Posted | Title | Company | Location | Employer URL |
|---|---|---|---|---|
| 2026-11-12 | Solution Architect ServiceNow Service Portal, Moveworks | NewRocket | US or Canada - Remote | https://www.newrocket.com/careers/job?gh_jid=6260728004 |
| 2026-11-11 | IRM/GRC Technologies Senior Associate | PwC Canada | Toronto, ON | https://pwc.wd3.myworkdayjobs.com/Global_Experienced_Careers/job/Toronto/IRM-GRC-Technologies-Senior-Associate_729518WD-1 |

### 5.2 ServiceNow roles verified live on 2026-11-14

These are already on the board but passed a fresh HTTP check (200 or 202) and contained no dead/expired text.

| Posted | Role type | Title | Company | Location | URL |
|---|---|---|---|---|---|
| 2026-11-13 | administrator | ServiceNow CMDB Administrator | BMO | Toronto, ON | https://bmo.wd3.myworkdayjobs.com/en-US/External/job/Toronto-ON-CAN/ServiceNow-CMDB-Administrator_R260030992 |
| 2026-11-13 | developer | ServiceNow Software Asset Management Developer | Cognizant | Toronto, ON (hybrid) | https://careers.cognizant.com/us-en/jobs/00070949051/servicenow-software-asset-management-developer/ |
| 2026-11-12 | developer | Hybrid! ServiceNow Developer - Senior, 6 Month Contract | Dimensional Tech Inc. | Toronto, ON | https://jobs.crelate.com/portal/dimensionaltechinc/job/1yjera61fx68yoqg3o8brt46ny |
| 2026-11-12 | architect | ServiceNow Architect - Canada | Ondaro | Canada | https://ondarowave.com/job-listing?gh_jid=5271251007 |
| 2026-11-11 | developer | ServiceNow Developer | Triunity Software | Toronto, ON | https://103.careerplug.com/jobs/3524732/apps/new |
| 2026-11-11 | developer | ServiceNow Developer | Rexall | Toronto, ON | https://careers.rexall.ca/servicenow-developer/job/37B80470AD0A44355A6D3D8E2EF2E593 |
| 2026-11-10 | consultant | ServiceNow Hardware Asset Management (HAM) Consultant | Accenture | Canada | https://www.accenture.com/us-en/careers/jobdetails?id=14379035_en |
| 2026-11-09 | administrator | ServiceNow SAM Administrator - ITAM | BMO | Toronto, ON | https://bmo.wd3.myworkdayjobs.com/en-US/External/job/Toronto-ON-CAN/ServiceNow--SAM-Administrator---ITAM_R260030096 |
| 2026-11-09 | administrator | ServiceNow Administrator Specialist | Scotiabank | Toronto, ON | https://jobs.scotiabank.com/job/Toronto-ServiceNow-Administrator-Specialist-ON-M5H-1H1/602949717/ |
| 2026-11-09 | developer | ServiceNow Developer | Lightspeed | Remote, Canada | https://www.remotejobs.place/job/lightspeed-servicenow-developer-d4deadf1 |
| 2026-11-09 | consultant | Application Consultant-ServiceNow | IBM | Canada | https://careers.ibm.com/fr_CA/careers/JobDetail/Application-Consultant-ServiceNow/81142 |
| 2026-11-09 | developer | Application Developer-ServiceNow | IBM | Canada | https://careers.ibm.com/fr_CA/careers/JobDetail/Application-Developer-ServiceNow/69291 |
| 2026-11-08 | architect | ServiceNow Architect | RSM | Toronto | https://rsm.wd1.myworkdayjobs.com/en-US/RSMCareers/job/Toronto/ServiceNow-Architect_JR122225 |

### 5.3 Salesforce roles verified live on 2026-11-14

| Posted | Role type | Title | Company | Location | URL |
|---|---|---|---|---|---|
| 2026-11-14 | developer | Software Engineer III - Salesforce Data 360 | TD Bank | Toronto, ON | https://td.wd3.myworkdayjobs.com/en-US/TD_Bank_Careers/job/Toronto-Ontario/Software-Engineer-III---Salesforce-Data-360_R_1515074 |
| 2026-11-13 | architect | Marketing Cloud Next Solution Architect | NeuraFlash | Remote - Canada (AB, BC, ON only) | https://job-boards.greenhouse.io/neuraflash/jobs/6253608004 |
| 2026-11-13 | developer | Salesforce Marketing Cloud Developer | McKesson | Mississauga, ON | https://mckesson.wd3.myworkdayjobs.com/en-US/External_Careers/job/CAN-ON-Mississauga/Job-Description-Salesforce-Marketing-Cloud-Developer_JR0147159 |
| 2026-11-12 | developer | Salesforce Developer | Cognizant | Remote in Canada (Toronto hiring location) | https://careers.cognizant.com/us-en/jobs/00071305431/salesforce-developer/ |
| 2026-11-11 | developer | Salesforce Platform Developer | Altus Group | Toronto, ON | https://altusgroup.wd3.myworkdayjobs.com/en-US/AltusGroup/job/Toronto-Ontario/Salesforce-Platform-Developer_R0014087 |
| 2026-11-11 | developer | Salesforce Data Cloud Developer | Cognizant | Toronto, ON | https://careers.cognizant.com/us-en/jobs/00070828311/salesforce-datacloud-developer/ |
| 2026-11-11 | developer | Salesforce Developer (Dealer Services) | Winobell | Toronto, ON | https://www.winobell.com/jobs/job-opportunity-salesforce-developer-dealer-services |
| 2026-11-11 | developer | Salesforce Developer 1014 | Veracity Ventures Inc. | Toronto, ON | https://veracity-ventures-inc.careerplug.com/jobs/3563242/apps/new |
| 2026-11-11 | architect | Lead Salesforce Solution Architect | McKesson | Mississauga, ON | https://mckesson.wd3.myworkdayjobs.com/en-US/External_Careers/job/CAN-ON-Mississauga/Lead-Salesforce-Solution-Architect_JR0154441 |
| 2026-11-11 | architect | Salesforce Solution Architect, Service Cloud | NeuraFlash (Accenture) | Remote - Canada (AB, BC, ON only) | https://job-boards.greenhouse.io/neuraflash/jobs/5730028004 |
| 2026-11-10 | architect | Salesforce Solution Architect | Cognizant | Toronto, ON | https://careers.cognizant.com/ca-en/jobs/00070590911/salesforce-solution-architect/ |
| 2026-11-10 | developer | Salesforce Developer | Robert Half | Toronto, ON (remote) | https://www.roberthalf.com/ca/en/job/toronto-on/salesforce-developer/000954410-caen |
| 2026-11-10 | developer | Senior Salesforce Developer | Docebo | Toronto, ON | https://jobs.ashbyhq.com/docebo/0bbdde71-476f-4f46-bfdc-d4536cdcf7ad |
| 2026-11-09 | developer | Senior Full Stack Developer - Salesforce (Contract) | Electric Mind | Downtown Toronto, ON | https://jobs.lever.co/electricmind/0c786409-1f69-43a8-82ee-878377e247eb |
| 2026-11-09 | developer | Senior Salesforce Marketing Cloud Developer | WPP (Map) | Toronto, ON | https://job-boards.greenhouse.io/map/jobs/8396722002 |
| 2026-11-09 | administrator | Salesforce Administrator | Lane Four | Toronto, ON | https://lanefour.com/job-posting/salesforce-administrator/ |
| 2026-11-09 | developer | Salesforce Senior Developer | IKO | Mississauga, ON | https://iko.wd3.myworkdayjobs.com/en-US/IKO_Careers/job/Mississauga-ON/Salesforce-Senior-Developer_REQ-12533 |
| 2026-11-09 | developer | Senior Salesforce Developer @ Webflow | Webflow | Remote, Canada | https://jobs.ashbyhq.com/webflow/a35a4d60-319f-441e-89d7-3a0ef6cd7421 |
| 2026-11-08 | developer | Principal Application Engineer (Salesforce) | PointClickCare | Mississauga, ON | https://jobs.lever.co/pointclickcare/230b8d92-f07c-4f44-b888-7f862314af15 |
| 2026-11-07 | developer | DevOps Engineer (Salesforce) | Scotiabank | Toronto, ON | https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/ |

### 5.3.1 Lane B employer-date corrections

Lane B's five candidates were all already on the board, but the employer ATS exposed dates and work models that differ from the board card.

| Role | Board date | Employer ATS date | Work model | Source |
|---|---|---|---|---|
| Software Engineer III - Salesforce Data 360 (TD Bank) | 2026-11-14 | **2026-11-13** | **Onsite** (`remoteType=Onsite`) | Workday CXS `startDate` |
| Marketing Cloud Next Solution Architect (NeuraFlash) | 2026-11-13 | **2026-11-09** | Remote, Canada (AB/BC/ON only) | Greenhouse `first_published` |
| Lead Salesforce Solution Architect (McKesson) | 2026-11-11 | **2026-11-10** | **Hybrid** | Workday CXS `startDate` |
| Principal Application Engineer (Salesforce) (PointClickCare) | 2026-11-08 | **2026-11-05** | Not specified; separate Remote-US req exists | Lever `createdAt` |
| DevOps Architect (CAN) (Salesforce) | 2026-11-12 | 2026-11-11 | Remote customer-based | Workday CXS `startDate` |

The TD row matters: the board presents it as a Toronto Salesforce Data 360 role, but the employer says onsite. The NeuraFlash row is six days older than the board card. This is the empirical case for storing the employer date and a work-model flag beside every aggregator date.

### 5.4 Liveness exclusions

These rows are on the board but failed the 2026-11-14 re-check. They should be removed or quarantined until re-confirmed.

| Status | Title | Company | URL |
|---|---|---|---|
| 200 + dead text | Senior ServiceNow Developer | BMO via Procom | https://myprocom-portal.procomservices.com/jobs/senior-servicenow-developer-toronto-0fe02eb9 |
| 200 + dead text | Consultant/Senior Consultant - ServiceNow Solution Developer | KPMG Canada | https://careers.kpmg.ca/jobs/33919?lang=en-us |
| 200 + dead text | Salesforce Developer | Nityo Infotech | https://dontapply.club/jobs/310746-salesforce-developer |
| 410 | Senior Salesforce Developer / Admin | Celestica | https://confidential.careers/job-detail/senior-salesforce-developer-admin-celestica-toronto |
| 410 | Salesforce Revenue Cloud Architect (Remote) | CloudKettle Inc | https://www.jobbank.gc.ca/jobsearch/jobposting/50631252 |
| 404 | Salesforce FSC Developer | Cognizant | https://careers.cognizant.com/us-en/jobs/00070907531/salesforce-fsc-developer/ |
| 404 | Salesforce Developer | Procom | https://myprocom-portal.procomservices.com/jobs/salesforce-developer-toronto-73f5a6b2 |
| 404 | Senior Consultant, ServiceNow | KPMG | https://careers.kpmg.ca/jobs/31517?lang=en-us |
| 404 | Senior Technical Consultant, ServiceNow Developer | KPMG Canada | https://careers.kpmg.ca/jobs/33533?lang=en-us |
| 403 botwall | Senior Salesforce Developer | Synechron | https://jobsca.org/senior-salesforce_toronto-c117072/2026-10-synechron_i4248473031 |
| 403 botwall | Salesforce Industries Cloud Architect (Remote) | CloudKettle | https://www.simplyhired.ca/job/zB_R8fQYap01hyQv9CNPqFq8kDc60329tJOZgPfdQFE3OvVt0Ykneg |
| 521 origin down | ServiceNow System Administrator | GDIT | https://gdit.wd5.myworkdayjobs.com/en-US/External_Career_Site/job/Any-Location--Remote/ServiceNow-System-Administrator_RQ230636 |
| 521 origin down | ServiceNow Developer Sr Principal | GDIT | https://gdit.wd5.myworkdayjobs.com/en-US/External_Career_Site/job/Any-Location--Remote/ServiceNow-Developer-Sr-Principal_RQ232247-1 |
| 521 origin down | ServiceNow Developer SME | GDIT | https://gdit.wd5.myworkdayjobs.com/en-US/External_Career_Site/job/Any-Location--Remote/ServiceNow-Developer-SME_RQ231819-1 |
| 521 origin down | ServiceNow Developer Senior - EHR | GDIT | https://gdit.wd5.myworkdayjobs.com/en-US/External_Career_Site/job/Any-Location--Remote/ServiceNow-Developer-Senior---Electronic-Health-Records---Remote-_RQ231413 |

Liveness tally: 34 HTTP 200, 2 HTTP 202, 4 HTTP 404, 2 HTTP 410, 2 HTTP 403, 4 HTTP 521. Nine rows were definitively dead; four were origin-down; two were botwalled. The board should not treat the 521/403 rows as live without a retry.

---

## 6. Blockers and source reliability

| Source | Status on 2026-11-14 | Workaround |
|---|---|---|
| Job Bank Canada | `locationstring` ignored; loose full-text matches; 0 usable rows from 441 parsed | Use as a date/source cross-check, not a keyword search |
| LinkedIn guest | 200 but rate-limits after ~4 rapid calls; detail returns 422 | Sleep ~25s between batches; use email alerts as primary |
| Workday CXS | Intermittent 5xx/outage on many tenants; needs `wdN` host + `curl --compressed`; urllib blocked | Retry later; use employer-specific `wdN` host |
| Greenhouse | API reliable, but many boards have old `first_published` dates | Use for verification, not freshness |
| Workopolis | Fresh and parseable | Promote to daily/weekly lane |
| Eluta | Server-rendered, relative "last seen" dates | Convert to absolute at capture; quarantine |
| Indeed | 403 Cloudflare | Email alerts or browser only |
| Robert Half / Randstad / Insight Global / TEKsystems / S.i. Systems / Apex / Altis / Experis / Motion | SPA, 404, or bot-wall | Use Adzuna/LinkedIn mirrors; do not burn daily cycles |
| Deloitte Canada | Site maintenance | Retry weekly |
| Cognizant / Thirdera / Crossfuze | Cloudflare 403 | Use their ATS/aggregator mirrors |
| KPMG Canada | iCIMS redirect shell | Use Workday/aggregator mirrors; re-check weekly |
| Bell / Rogers / TELUS / RBC / BMO Phenom | Widget JSON works for some; keyword counts often 0 | Use Workday/Phenom detail endpoints where reachable |
| ServiceNow vendor | SmartRecruiters 200, 818 postings, 24 Canada, no in-window platform role | Keep as vendor-engineering lane, not practitioner |

---

## 7. Recommendations

Priority order, with evidence and SubQ confidence where available:

1. **Add a Salesforce lens (SubQ 0.89).** Keep the ServiceNow profile for the ServiceNow tab; add a second profile with Salesforce 30, Apex/LWC 10, CPQ/Revenue Cloud 8, Marketing Cloud 8, Data Cloud 8, Agentforce 8, FSC 6, Integration/MuleSoft 6. Show a family-relative percentile, not a single cross-family score. Do not merely reweight the one profile (SubQ 0.01).
2. **Reconcile counts with a CI assertion (SubQ 0.999).** Make `jobs.json` the single source of truth. Generate README headings from actual table rows and assert `sum(sections) == total`. Assert live family counts are within a documented window of the JSON. The current README says 2,700 while its own tables have 6,782 rows.
3. **Fix classifier false positives.** Remove bare `\bsn\b` and generic `itsm|itam|cmdb|itom` as sole triggers. Require an explicit platform token in the title or a known platform ATS family. Add negative guards for Oracle APEX, Apex Systems/Apex Legends, Freshservice, and ServiceNow-vendor SRE/security/DevOps/sales. Add a `vendor_engineering` sub-bucket.
4. **Quarantine unknown-company and noisy rows (SubQ 0.98).** 127 ServiceNow (14.0%) and 103 Salesforce (10.7%) rows have no usable employer. Do not show them as live cards until resolved.
5. **Use two passes: daily freshness, weekly direct ATS.** Aggregators found 138 ServiceNow and 173 Salesforce rows aged ≤3 days; employer boards found 37 and 18. Use aggregators to detect, employer ATS to confirm. Run the direct ATS crawl weekly (SubQ 0.59), not daily.
6. **Add an explicit Canada-remote filter with a verification flag (SubQ 0.96).** Only 51 ServiceNow and 66 Salesforce rows mention remote. "Canada" and "Any Location / Remote" are not proof of Canada eligibility.
7. **Add a developer-only view and separate admin/consultant/architect views (SubQ 0.94).** The current family tabs mix 328 ServiceNow developers with 156 architects, 102 consultants, and 88 analysts. A developer view is the user's primary workflow.
8. **Promote Workopolis and Adzuna; demote stale Greenhouse/jobs.ca for these employers.** Workopolis had 41 of 43 ServiceNow rows and 29 of 29 Salesforce rows at ≤7 days. Greenhouse had 1 of 42 and 4 of 46. Keep LinkedIn with backoff.
9. **Re-verify liveness on a schedule.** 13 of 48 current roles (27.1%) were dead, expired, or origin-down on re-check. Add a retry/quarantine state; do not equate a 200 with a live posting when the page says "no longer accepting".
10. **Keep staffing as a labeled lane (SubQ 0.93).** Salesforce developer staffing share is 19% vs 11% for ServiceNow. Label agency rows so users can separate contract work from direct employer roles.
11. **Apply the date-quarantine rule (SubQ 0.95).** Convert relative dates at capture, store the capture timestamp, and re-verify on the employer ATS. Do not silently drop or silently trust relative dates.
12. **Promote the P4+P1+P3 methodology (SubQ 0.76).** P4 is the daily automated front end; P1 is the verification and anti-fabrication rulebook; P3 is the weekly untried-source expansion. Keep P2 as the human weekly routine.

---

## 8. Verification log

- **Board snapshot:** `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json`, HTTP 200, 3,811,119 bytes, `generatedAt` 2026-11-14T07:36:29+00:00, count 5,133.
- **README/jobs.json:** `git show origin/main:README.md` and `git show origin/main:jobs.json` from `github.com/eltonaguiar/BESTIEJOB`.
- **Freshness scan:** `python3 scripts/fresh_ca_scan.py --days 3` → raw 649, unique 124, kept 40 (25 Salesforce, 15 ServiceNow), unverified dropped 33, already on board 9 by URL / 16 by title, cross-source dup 7.
- **Fresh candidate liveness:** 23 primary-geo URLs checked; all HTTP 200; 0 dead-text; 6 employer dates were 1–2 days older than the aggregator's posted date (e.g., S.I. Systems 2026-11-11 vs 2026-11-13; Altis 2026-11-11 vs 2026-11-13).
- **Canonical dedupe:** 23 fresh candidates → 0 new after employer+title canonicalization. 63 unique candidates across the three lanes plus the fresh scan → 9 new.
- **Current-role liveness:** 48 curated employer roles checked with browser UA and `Accept-Language: en-CA`; 34 × 200, 2 × 202, 4 × 404, 2 × 410, 2 × 403, 4 × 521; 3 rows had dead/expired text inside a 200.
- **Lane B Salesforce:** 5 candidates, all HTTP 200, all already in the live board. Employer ATS dates differed from board dates for TD (11-13 vs 11-14), NeuraFlash (11-09 vs 11-13), McKesson (11-10 vs 11-11), and PointClickCare (11-05 vs 11-08).
- **SubQ:** Snap 1.2 via `POST https://api.subq.ai/v1/systemone`; methodology comparison (13,879 input tokens), pattern decisions (1,541 input tokens), title classification (23 questions), methodology-combination decisions (829 input tokens). All decisions and confidences are reproduced in §4.4.
- **No fabricated rows:** every row in §5 has a URL and an absolute posted date. Aggregator dates are labeled as such; employer ATS dates are preferred where available.

---

## 9. Open items

| Item | Why it remains open | Suggested owner / next action |
|---|---|---|
| Employer resolution for the 9 new candidates | Adzuna/WWR URLs are detail pages, not employer ATS pages | Resolve each to the employer board; drop any that are mirrors or unverifiable |
| Reonomy / Altus Group duplicate check | Reonomy is an Altus Group company; the two "Salesforce Platform Developer" rows may be the same product org | Compare req IDs on the Altus Workday board |
| Equest employer identity | Equest is a job board, not necessarily the employer | Resolve to the underlying employer before treating as a direct role |
| Salesforce lens implementation | Report recommends it; no code change was made | Add a second profile in `tools/build_site.py` and a family-relative percentile |
| Classifier guards | Report quantifies the false positives; no code change was made | Add negative guards for Oracle APEX, Apex Systems/Apex Legends, Freshservice, vendor SRE/security/DevOps/sales |
| Count reconciliation CI | README, `jobs.json`, and live feed still disagree | Add a CI assertion for section sums and cross-store counts |
| Liveness re-check loop | 27.1% of sampled current roles were dead/expired/origin-down | Add a retry/quarantine state and re-check stale rows |

## 10. Provenance

- **Worktree:** `bestiejobs` (`/home/eaguiar2015/findtorontoevents_antigravity.ca/.kilo/worktrees/bestiejobs`).
- **BESTIEJOB repo:** `github.com/eltonaguiar/BESTIEJOB`, `origin/main`.
- **Methodology docs read:** `docs/JOB_SEARCH_PROTOCOL_2026-11-02.md`, `docs/JOB_SEARCH_PLAYBOOK.md`, `docs/SERVICENOW_EXHAUSTIVE_HUNT_PLAN.md`, `docs/superpowers/specs/2026-11-11-exhaustive-sn-sf-scan-design.md`, `scripts/fresh_ca_scan.py`, `scripts/daily_job_scan.mjs`, `tools/build_site.py`, `tools/jobs_consolidate.py`.
- **Lane artifacts:** `/tmp/kilo/discovery/servicenow/`, `/tmp/kilo/discovery/salesforce/`, `/tmp/kilo/discovery/aggregators/`.
- **SubQ artifacts:** `/tmp/kilo/subq_methodology.json`, `/tmp/kilo/subq_patterns.json`, `/tmp/kilo/subq_method_combo.json`, `/tmp/kilo/subq_title_classes.json`.

---

*This audit is read-only with respect to the job data. The only file committed is this report.*

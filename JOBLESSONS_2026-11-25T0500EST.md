# JOBLESSONS_2026-11-25T0500EST — hourly Toronto ServiceNow / Salesforce scan

## Cycle
Cron run Wednesday 2026-11-25 05:00 EST (UTC-05, ran ~10:00Z). Repo `eltonaguiar/BESTIEJOB` (`main`). Local clone `/c/Users/zerou/bestiejob_repo`, reset to `origin/main` at `6b6bbea4` (the 04:00 EST lessons commit on top of the 09:15Z CI scan build) before scanning, so the URL diff is against the live board.

## What ran
1. `node scripts/daily_job_scan.mjs` (no flags — full pipeline incl. README `<!-- DAILY-SCAN -->` refresh, which the CI never does). Result: `fresh=491 merged=5686 {servicenow:1205, salesforce:4322}`. Sources: LinkedIn guest 253, Adzuna CA 203, SmartRecruiters ServiceNow 12, Greenhouse 12, remote 8, Lever 1.
   - Workday inside the scan: **all 15 boards HTTP 429** at scan time (:00-:05Z window), `[workday] 0 matching postings` — rate-limit, not zero postings (see manual probe below).
2. Workday manual probe (7 tenants × 2 queries, 8 s spacing) **past the 429 window** — all HTTP 200:
   `bmo/External`, `td/TD_Bank_Careers`, `cibc/search`, `manulife/MFCJH_Jobs`, `interac/interac`, `salesforce.wd12/External_Career_Site`, `gdit.wd5/External_Career_Site`. 166 postings, 47 Canada-located.
3. Employer-direct: Rogers (date-sorted Phenom), Bell (jobs.bell.ca), Ateko/FX Innovation, Accenture Workday (`accenture.wd103/AccentureCareers`).
4. `tools/verify_links.py --days 2` → 57 probed, live=33, dead=0, unknown=24 (bot-wall/transport, kept). Nothing dropped.
5. `tools/build_site.py` → 4998 cards (SN 868 / SF **966** / other 3164), 560 mirrors collapsed, 28 applied hidden, built 2026-11-25 10:11 UTC.

## Dedupe vs board
- 40 URL-new rows vs `origin/main:jobs.json`. **39 of 40 were company+title twins** already on the board (Adzuna/LinkedIn re-issues: Cognizant "Salesforce Tech Lead" 5978174028 twin of 5973912092/5974890709; TCS "Salesforce Developer" 4494376362 twin; Jolera "Senior ServiceNow Consultant" 4494431156 twin; TD "Senior Solution Architect (ServiceNow)" 5970077372 twins Workday R_1521185; Deloitte DTC twins; etc.). 1 non-twin: Tanium "Senior Software Engineer - Full-stack Cloud Operations" (not SN/SF core, already in README).
- **0 genuinely-new fresh SN/SF roles from the automated scan** (all 4 "today/yesterday" URL-new SN/SF rows were twins already in README). Same outcome as the 03:00 and 04:00 EST runs — board is at saturation; new rows come from employer-direct/Workday body checks, not aggregators.

## Employer-direct results
- **Rogers** `jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc`: 26 dated `<tr>` rows, **0 ServiceNow/Salesforce titles** (matches 11-24).
- **Bell** `jobs.bell.ca` both queries: 0-byte shell = zero reqs (not a scrape failure). Real Bell SN hiring is Ateko/FX Innovation.
- **Ateko / FX Innovation** careers pages are JS/marketing shells; their reqs live on ADP WorkforceNow + LinkedIn (covered by the LinkedIn guest pass).
- **Accenture** `accenture.wd103/AccentureCareers` HTTP 200 but **0 Canada-located** SN/SF rows in first page (global board, relevance-sorted) — consistent with prior runs.
- **Banks Workday fresh "Posted Today/Yesterday" SN/SF rows were all twins or non-platform:**
  - BMO R260032445 "Senior Sales Force Developer" (Toronto) + R260032496 (Chicago) = employer-direct twin of the board row **"Bank of Montreal (via Procom) Senior Salesforce Developer"** (2026-11-09). Same role; not re-added.
  - TD R_1509038 "Software Engineer II (Salesforce Loyalty Management Developer)" — already on board.
  - GDIT RQ232563 "ServiceNow Developer" (Remote) — already on board; GDIT ARCHITECT is USA Offutt AFB (US-only).
  - CIBC 2623517 "Sr. Consultant, Infrastructure Management" — ServiceNow appears only as *"It's an asset if you have experience with ServiceNow and OpenShift/Ansible"* → infra/DevOps role, not a platform role. Skip.
  - Manulife JR26100922 "Manager, Technology Governance & Controls" — *"Familiarity with tools such as Archer, Jira, Confluence, and ServiceNow. Hands-on platform administration is not required."* → GRC governance, ServiceNow is just a tool. Skip.
  - All Salesforce-the-company "Posted Today" rows = India/Mexico/Japan/Australia/UK sales/CS/legal — none Toronto platform.

## What was merged (1 verified fresh role)
- **TD Bank — Bus Sys Analysis Specialist (Salesforce/nCino)**, Toronto, Ontario, `2026-11-23`, $96,900–$136,800 CAD, Office Focused (onsite, full-time).
  Workday `R_1522988` direct deep link. Body: *"Work with cross-functional teams (business, developers, QA) to design and implement Salesforce or nCino-based solutions."* Genuinely absent from the board (no URL/company+title twin; the earlier "TD Salesforce Business Analyst 2026-11-23" hit was **Brainhunter Systems Ltd**, not TD).
  - Added to `jobs.json` at head (tags `["salesforce"]`, salary object, excerpt) → `meta.total 5686→5687`, `primaryCounts.salesforce 4322→4323`.
  - Added to README `<!-- DAILY-SCAN -->` Salesforce table (heading 12→13) in date order.
  - `build_site.py`: rendered as family **salesforce**, SF card count 965→**966**, present in `public/jobs-data.json` by company+title.
- Entry-level **Platform Administrator / Platform Developer I (Toronto, 0–2 yrs): none surfaced** this hour. Junior scarcity persists.

## Patterns for future agents
- **Workday CXS opens up ~4–6 min after a scan's 429 burst.** A manual probe at :00-:05Z gets 429 on every board; the same 7 tenants answered HTTP 200 at ~:06Z with 8 s spacing. Always `--compressed` + `Content-Type/Accept/Origin` (no Referer).
- **`"td"` / `"ltd"` substring traps.** Filtering `company` with `'td' in company.lower()` matches `Ltd` (Atlantic Packaging, Brainhunter). Use word-boundary regex (`\btd\b`) or startswith, or you will mis-attribute staffer rows to TD Bank.
- **BMO "Senior Sales Force Developer" (with a space) is the employer twin of the Procom board row**, not a new posting. The board keeps "Bank of Montreal (via Procom) Senior Salesforce Developer"; `norm_co` won't match "BMO"↔"Bank of Montreal (via Procom)" — match on the role + employer relationship, not the string.
- **"Infrastructure Management" / "Technology Governance" titles are tooling, not platform.** Read the body: "ServiceNow is an asset" and "platform administration is not required" both mean skip.
- **Hidden SN/SF titles worth a Workday body-check each cycle:** "Bus Sys Analysis Specialist" (TD → Salesforce/nCino BA), "Business System Analyst" (BMO), "CRM Business Analyst". These don't carry "Salesforce" in the title and the automated `matchTags` rejects them — only a manual Workday/CXS body read catches them.
- **Accenture `wd103/AccentureCareers` answers but yields no Canadian rows** in the first relevance-sorted page — don't spend more than 2 queries on it per hour.
- **At saturation the automated scan is net-zero; value is in employer-direct Workday body checks.** Budget the hourly run: scan (~4 min) → Workday 7-tenant probe (~2 min) → Rogers/Bell (~10 s) → dedupe → build → commit.
- **`sync_readme_counts.py` prints "header count line not found — nothing rewritten"** — this is expected: the DAILY-SCAN block carries the live count now, not a standalone header.

## Changes committed
- `jobs.json` (+1 TD row; scan refresh), `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`, `public/jobs-data.json`, `public/index.html`, `FRESH_JOBS.md`, `README.md`, this lessons file.

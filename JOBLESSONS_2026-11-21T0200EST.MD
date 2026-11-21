# JOBLESSONS_2026-11-21T0200EST

Hourly BESTIEJOB scan for Toronto/Canada ServiceNow + Salesforce jobs, run 2026-11-21 02:00 EST (07:01 UTC).
Board: github.com/eltonaguiar/BESTIEJOB (jobs.json = system of record; GitHub Pages at eltonaguiar.github.io/BESTIEJOB).

## Result this run
- `node scripts/daily_job_scan.mjs` (no --no-readme): fresh=499 source results, merged=5627 (SN 1198 / SF 4295).
- 29 net-new URLs vs. prior board (diff against `origin/main:jobs.json`).
- CI's concurrent sweep (`c6b1cc5`, fresh CA sweep 06:50Z) had already integrated this cycle's jobs; local commit `6d8aa3b` was redundant — reset `--hard origin/main`. No push required; board already on `main`.
- `tools/verify_links.py --days 2`: live=27 dead=0 unknown=44 (403/429/transport kept as live), nothing dropped.
- `tools/build_site.py`: 5059 jobs (SN 872 / SF 930), built 2026-11-21 07:08 UTC. `scripts/sync_readme_counts.py`: 5602 live postings.
- `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB` → success (run 44878972108, ~35 s). Live `jobs-data.json` verified to carry new URLs (e.g. `4490380189` BMO SN CMDB Admin, `5971441048` TD nCino/Salesforce, `744000158575719` ServiceNow Principal Solution Architect, Toronto).

## What worked (sources / patterns)
- **Adzuna Canada API** (`api.adzuna.com/v1/api/jobs/ca/search/1`, demo keys `54ce986e`/`db851f299e966c0a2a72af525dce6199`, param `content-type`, `sort_by=date&max_days_old=14`, `where=Toronto/Ottawa/Mississauga/Canada`): best freshness oracle for Toronto SN/SF. Queries: servicenow/salesforce + administrator/architect/developer/consultant/specialist/lead, plus ITSM/ITOM/ITAM/CMDB/"service now"/"platform developer"/"crm developer"/"apex"/"agentforce".
- **LinkedIn guest search** (`linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search`, keywords + `f_TPR=r86400` for 24h, locations Toronto + Canada): returned cards as HTML; queries ServiceNow/Salesforce developer/administrator/architect/consultant. Retry once after ~4 min if a query returns 0. Throttles hard — 2 workers + 1.8s spacing; 429s after ~4 rapid queries. Test length + digest distinctness, not just HTTP 200 (authwall returns 200 with a static ~337 KB body).
- **SmartRecruiters public API** (`api.smartrecruiters.com/v1/companies/ServiceNow/postings`): ServiceNow's own Toronto reqs (e.g. Principal Solution Architect).
- **Greenhouse / Lever / Ashby board APIs** — caught partner/ecosystem roles: NeuraFlash (Salesforce partner, Senior Salesforce Architect), Benevity (Senior Salesforce Administrator), D2L, EQ Bank, Alimentiv, Versapay, Loopio, MoeGo.
- **Workday CXS** (`{tenant}.wd{N}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs`, POST `{"appliedFacets":{},"limit":20,"offset":0,"searchText":"servicenow|salesforce"}`): verified 200 tenants — bmo.wd3/External, td.wd3/TD_Bank_Careers, salesforce.wd12/External_Career_Site, cibc.wd3/search, manulife.wd3/MFCJH_Jobs, interac.wd3/interac, caatpension.wd10/Careers, gdit.wd5/External_Career_Site, accenture.wd103/AccentureCareers, bdo.wd3/BDO. BMO/TD/Salesforce surfaced SN/SF roles. **Caveat:** Workday "Posted Today" is NOT a Canada signal — read the `/job/<City>/` slug and country before counting.
- **Company/partner names that reliably surface Toronto SN/SF:** BMO, TD Bank, CIBC, KPMG Canada, Deloitte, Accenture, NeuraFlash, Konrad, OSI Digital, Altus Group, Benevity, Alimentiv, Cognizant, Pacer Group, Avanciers, Wipro, ServiceNow (itself).
- **GTA satellite cities** (Markham, Mississauga, Vaughan, Ottawa) surface listings that avoid "Toronto".

## What did NOT work / pitfalls
- **Workday rate limits:** all boards HTTP 429 during this scan (CI hourly runs at :00Z / 03:00 EST; 429s persist past :00Z). `curl` returned HTTP 000 (connect failure) to Workday hosts from this environment even though Node `fetch` reached them (429). Manual retry: key tenants × servicenow/salesforce with 8s spacing, `Content-Type`+`Accept`+`Origin` headers only (no Referer — Referer empties responses), `--compressed`, write probe JSON under repo `raw/` with `curl -sS`. Post-:00Z retry pays off within ~4 min.
- **Rogers:** `jobs.rogers.com` Phenom board returns a ~56 KB shell with zero server-side rows; rely on LinkedIn/Adzuna for Rogers. Re-check weekly, not hourly.
- **Bell:** `jobs.bell.ca` renders an empty shell / shows (0) for servicenow and salesforce = zero reqs, not a scrape failure. Bell's real SN hiring is under "Ateko (backed by Bell Canada)" / FX Innovation on LinkedIn — search "Ateko", not just "Bell".
- **Canadian government:** `gojobs.gov.on.ca` (Ontario) and `jobs.gc.ca` are Radware-walled (captcha). Do not retry; use Job Bank as proxy and trust only postings whose *title* names the platform.
- **Indeed / www.adzuna.ca:** walled from this host (CloudFront 403 / "Blocked"). Use the Adzuna API, not the website.
- **Job Bank keyword search** (`searchstring=servicenow`) is noise (matches unrelated NOC postings); trust only title-named platform hits. `jobbank.gc.ca/jobsearch/jobposting/<id>` 404s once expired.
- **LinkedIn detail pages:** intermittently serve the "Join LinkedIn" authwall even mid-session — skip as unverified, never infer platform from card title. On readable pages, extract `.jobs-description`/`.jobs-box__html-content` (not `body.innerText`, which includes "People also viewed" sidebar false hits).
- **Generic titles hide platform roles:** body-check before discarding (e.g. "Business Analyst" was actually SN SPM; "CRM developer" can be Siebel, not Salesforce).
- **Adzuna `Apex`/`CPQ`** are false-positive magnets — exclude `sales executive|solution sales Account Executive` and `Apex Legends`.
- **"ServiceNow" in body as tooling ≠ platform role** (e.g. ticketing-tool user, ITSM process manager). Require the platform/certs in context.
- **Dedupe:** normalize URL (strip query/trailing slash/hostname www) + trailing numeric job ID for LinkedIn (e.g. `-5816` twins). Also company+title fuzzy check (strip Inc/Ltd/Corp/Limited) to catch `MLSE` vs `Maple Leaf Sports…`, `Interac Corp.` vs `Interac`. Vendor twins (two staffing firms on same client req) are DISTINCT — keep both, dedupe on URL only.
- **Job ids recycle** (Adzuna) — use detail-page JSON-LD `datePosted`, not API `created`.
- **Never prune existing dead links** (user instruction); `verify_links --days 2` only probes fresh rows. Full prune daily, not hourly.
- **`jobs.json` rewrite:** `JSON.stringify(..., indent=2)` re-formats the whole file (huge diffs). For 1–3 row batches, insert textually at the `"jobs": [` marker, preserve newline style, verify with `git diff --stat`.
- **gh CLI:** bundled-git exec raises WinError 5 on this host — use `git` directly for clone/push/reset. `gh workflow run <workflow> --repo <repo>` works for triggering deploys; `gh run list --json …` for polling.
- **[skip ci] commits** don't trigger `pages.yml`; after a data push, manually run `gh workflow run pages.yml` and verify live `jobs-data.json` carries the URL.

## Partners / Elite Partners / sponsors / technical companies to target next run
ServiceNow & Salesforce partners & consultancies: NeuraFlash, Konrad, OSI Digital, KPMG, Deloitte, Accenture, PwC (ServiceNow IRM practice), Altus Group, Benevity, Alimentiv, Cognizant, Pacer Group, Avanciers, Wipro, D2L, Loopio, EQ Bank, Versapay.
Technical companies / banks / telcos: BMO, TD Bank, CIBC, Manulife, Interac, Rogers, Bell (via Ateko/FX Innovation), GDIT, Moneris, BDO Canada, CAAT Pension, Medcan, Huron, Irving Oil, McKesson, Brookfield, Resolve Tech.
Canadian government: probe Job Bank only (titles naming ServiceNow/Salesforce); gojobs.gov.on.ca / jobs.gc.ca are Radware-walled.

## Files touched this run
`jobs.json`, `README.md` (DAILY-SCAN block), `FRESH_JOBS.md`, `public/jobs-data.json`, `public/index.html`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`.

# JOBLESSONS — 2026-11-20 05:00 EST (10:00Z) hourly ServiceNow / Salesforce scan

Run context: Hermes cron hourly scan. Board at start `origin/main` 849d7f7 (5,584 rows). CI hourly scan also fires at :00Z, so its 10:00Z commit landed at 10:15Z mid-run; I fast-forwarded onto it before editing (`git merge --ff-only origin/main`).

Outcome: 23 candidates surfaced → 22 already on the board → **1 genuinely new** (Compugen Inc — Business Process Consultant – ServiceNow, Ontario, posted 2026-11-19). Added to `jobs.json` head (5,585 rows, SN 1,178), README DAILY-SCAN ServiceNow table (newest 12 kept), rebuilt `public/jobs-data.json` + `public/index.html` (5,031 cards after mirror collapse: SN 853 / SF 919 / other 3,259).

## What worked

- **LinkedIn guest search via browser is still the freshest oracle.** `https://www.linkedin.com/jobs/search?keywords=…&location=Toronto%2C%20Ontario%2C%20Canada&f_TPR=r86400`, then scroll 3× and read `li a[href*="/jobs/view/"]`. Salesforce returned 40 cards first try; ServiceNow returned **0 on the first call** (empty body, the known intermittent wall) and returned 50 cards on a retry ~4 minutes later. Always retry a 0-card ServiceNow query once before concluding the market is empty.
- **Adzuna API with `where=Toronto`/`where=Ontario` is a cheap freshness oracle, but `what=salesforce` is ~90% marketing/sales noise.** Filter titles hard: keep only salesforce|apex|lightning|sfdc|platform (admin|developer)|administrator|architect|nCino|Data Cloud. ServiceNow results were mostly rows already on the board plus tooling-user roles (Scotiabank incident mgmt, TMX event mgmt) that the board correctly treats as non-platform.
- **Workday CXS probes are quick when driven correctly.** POST `https://{tenant}.wd{N}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` with `{"appliedFacets":{},"limit":20,"offset":0,"searchText":"<q> Toronto"}`. TD (13 SN hits), BMO (4), CIBC (3), Interac (8), Accenture (5 SN / 19 SF), Salesforce (44 SF) all answered 200 this hour with **no 429s**, so the 10:00Z CI concurrency warning did not bite today.

## What failed / traps

- **`curl -o` into the Hermes scratch dir silently fails** (file never created; `-s` hides the error). Write probe JSON into the repo (`raw/…`) instead, and always use `curl -sS` so resolution/write errors surface.
- **Workday loop bug to avoid:** the host column in a `tenant|site` pair must be the full `{tenant}.wd{N}.myworkdayjobs.com`; using just `td.wd3` yields "Could not resolve host: td.wd3". Also omit the `Referer` header — with it, responses came back empty; with only `Origin` + `Content-Type` they parsed fine.
- **`.jobs-description` is empty on current LinkedIn detail pages.** Use `document.body.innerText` and slice from "Job Description"/"About the job". But the **"Similar jobs" sidebar pollutes keyword hits**: City of Hamilton's "CRM Administrator" matched `salesforce` only because a similar-jobs card was named "Salesforce Administrator". Body-checking the *duties* section showed it is Microsoft Dynamics 365 — rejected. Endress+Hauser "Business Applications Specialist" names Salesforce only as an example platform ("e.g., SAP, Salesforce") — rejected as a generic app-support role.
- **Indeed-backed Job Bank ads mirror each other.** Job Bank 50740706 (Bonafide "cloud developer") is the same ad as the ServiceNow ITOM Developer on Indeed; both the Bonafide ITOM Developer and the City-of-Toronto SPM consultant (50698289, Talent.com) were already on the board. Job Bank full-text search still returns "shipping coordinator"/"physician assistant" for `servicenow` — title-only trust remains correct.
- **`meta.primaryCounts.salesforce` jumped to 4,302** after the CI's `sync_readme_to_jobs` widened the feed from README rows; that is a feed count, not the card count. Judge health by `jobs.length` (5,585) + `build_site` cards (5,031), not by primaryCounts alone.

## Source yields this hour (for future agents)

- LinkedIn guest 24h (SN Toronto, SN Canada, SF Toronto, SF Admin 7d): ~140 cards → 1 new.
- Adzuna API (SN/SF × Toronto/Ontario, 2-day window): ~80 rows → 0 new (all board-covered).
- Workday CXS (9 tenants): 0 new. Newest relevant: TD Senior Solution Architect (ServiceNow) 4d, BMO CMDB Administrator 8d, Interac Product Manager 1d (not a platform role).
- Job Bank (full-text + 2 known deep links): 0 new.
- ServiceNow careers: Toronto postings this cycle are engineering/security (Staff Full-Stack, Senior Systems Engineer, Cloud Security) — **not** SN platform admin/dev; only "Senior Systems Engineer" was board-worthy and it was already captured at 03:00 EST.
- Rogers (`jobs.rogers.com`) still serves the Phenom shell only; Bell SN hiring still surfaces as **Ateko, backed by Bell Canada** on LinkedIn; gojobs/jobs.gc.ca remain Radware-walled.

## Market pattern (Nov 20, 2026)

The board is saturated for LinkedIn/Adzuna-sourced Toronto SN/SF work: 22 of 23 fresh candidates were already tracked (1,783 LinkedIn job ids indexed). Net-new rows now come almost exclusively from (a) employer ATS boards not yet in the sweep, (b) agency twins of the same req under new titles, and (c) francophone/Quebec postings from LGS/La Caisse/Ateko. Expect 0–1 net-new per hourly pass during business hours; investigate only when a pass returns 0 **and** LinkedIn returned fewer than ~25 cards (that signals a wall, not a quiet market).

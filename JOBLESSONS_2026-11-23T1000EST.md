# JOBLESSONS_2026-11-23T1000EST — Hourly BESTIEJOB scan (10:00 EST / 15:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,640 entries) + README.md + APPLIED.md. Two verified fresh jobs merged to README.md tables and jobs.json; both pushed to origin/main.

## Scan sources
| Source | Query | Result |
|--------|-------|--------|
| Web search | ServiceNow Toronto postings Nov 22–23 2026 (Indeed, LinkedIn, Glassdoor, JobBeacon) | ServiceNow's own Toronto postings are Nov 6 (Staff/Senior Staff Systems/Security Engineer — infrastructure, not platform); the Nov 22 Toronto hits are sales roles (Solution Sales Executive Moveworks, Cyber Account Exec) — excluded by board's no-sales rule |
| Web search | Salesforce Toronto postings Nov 22–23 2026 | LANDTHATROLE Toronto list (Nov 23): Paraluxent (4d), Konrad (4d), OSI Digital (11d), Docebo/Benevity (3w). Konrad Salesforce Architect Loyalty & Data 360 already on board (LinkedIn 4491325080). Paraluxent Sr Manager/Advisory not on board — added |
| jobs.ca mirror | HCLTech Salesforce Administrator Toronto | Posted Nov 17 — already on board (LinkedIn 4490676918 ×2 in jobs.json) |
| Web search | TD Bank Salesforce Developer Toronto | confidential.careers mirror shows posting dated Nov 20 but returns HTTP 403 (AEO bot policy); TD Workday req R_1486443 returns "page doesn't exist". Not verified live — dropped per board policy |
| Web search | Compugen ServiceNow Developer contract Toronto | datePosted 2026-10-25, validThrough 2026-11-10 — expired |
| Web search | Pacer Group ServiceNow Implementation Architect Toronto | Posted Nov 12, application deadline Nov 20 — expired |
| Web search | Alimentiv ServiceNow Platform Specialist Toronto | Posted Nov 18, remote, full-time, CSA required. jobs.ca + employer careers site verified live (HTTP 200). Not on board — added |
| Employer direct | Ateko / FX Innovation careers (fxinnovation.com/en/jobs) | JS-filtered listings panel; no server-rendered job rows — nothing actionable. Ateko SN roles already covered from LinkedIn (4492170001, 4492156434) |
| Employer direct | NewRocket careers | Marketing page only; offices listed are Vista CA, New York, London, Pune — no Toronto |
| Workday CXS | bmo/td/cibc/manulife/interac/caatpension tenants | Not reachable from this host (HTTP 000 / 422). CI hourly scan at :00Z carries Workday freshness; do not retry hourly |
| Canadian government | Job Bank / gojobs.gov.on.ca / City of Toronto | City of Toronto Systems Integration Specialist (AMANDA + Salesforce as asset) — Salesforce is only an asset, not a platform role; not added |

## Dedup result
- HCLTech Salesforce Administrator (LinkedIn 4490676918 / jobs.ca 1cbaba4e1749): already in jobs.json ×2 — skipped
- SS&C Technologies Salesforce Implementation Consultant & Platform Administrator (LinkedIn 4487007282): already in jobs.json + README — skipped
- Compugen Project Manager – ServiceNow & Financial Systems (LinkedIn 4492108232): already in jobs.json ×2 — skipped
- Konrad Salesforce Architect Loyalty & Data 360 (landthatrole mirror gh-konradgroup-8208217003): already on board via LinkedIn 4491325080 — skipped
- **Net new verified: 2**
  1. Alimentiv — ServiceNow Platform Specialist — Toronto, ON (remote) — posted 2026-11-18 — jobs.ca mirror + employer careers page verified live (HTTP 200) → added to `### ServiceNow jobs (565)` and jobs.json
  2. Paralucent — Salesforce Architect, Senior Manager / Advisory — Toronto/GTA (hybrid, contract 3–4 wks, Salesforce Data 360 + Agentforce) — posted ~2026-11-19 → added to `### Salesforce jobs (895)` and jobs.json
- Nothing in APPLIED.md matches these URLs

## GitHub Pages verification
Pending: push to origin/main triggers the `pages` workflow (push on public/** or README.md). Verify `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` count = 4,946 and both new entries present after the deploy run completes.

## Lessons for future agents
1. **No ADZUNA keys on this host** (CI-only secrets). When the hourly Adzuna sweep can't run locally, fall back to web search + employer-direct verification, but expect 0–2 net-new per hour rather than 0–5.
2. **jobs.ca mirrors render fully** (job summary, duties, posted date) and are an acceptable source when the employer page is Cloudflare/LinkedIn-gated — verify the mirror shows a real posting, not a listing page (jobs.ca `/<company>` hub pages are listing pages, not postings — blocked by sync_readme_to_jobs listing rules).
3. **Workday tenant pages and confidential.careers are blocked from this host** (HTTP 000/422/403). A Workday req that 404s ("page doesn't exist") or a mirror behind a bot wall cannot be verified live — drop it rather than guess.
4. **landthatrole mirrors are recruiter-mirrored (Recruitee/Greenhouse/Zapier prefixes)** — always dedupe by URL first (Konrad was already on board via LinkedIn), then prefer the employer-direct URL (careers.paralucent.com/...) found by clicking through.
5. **Sales roles keep appearing under "ServiceNow" queries** (Solution Sales Executive, Cyber Account Exec, Sr Mgr Sales) — the board's EXCL filter drops them at ingest; don't add them manually either.
6. **Always verify live page vs repo before declaring a deploy:** `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` count must equal `git show origin/main:public/jobs-data.json | python -c "import json,sys;print(json.load(sys.stdin)['count'])"` after the Pages deploy run succeeds.

# JOBLESSONS — Hermes cron scan — 2026-11-20 16:00 EST (21:00Z)

Run: 2026-11-20 16:00 EST / 21:00Z. Repo: `eltonaguiar/BESTIEJOB`. Scope: fresh Toronto/GTA + Canada-remote **ServiceNow** and **Salesforce** platform-build roles, deduped against `origin/main` (README tables + `jobs.json`), plus a partner / Elite-partner / telco / government sweep.

## Outcome

- **Net-new verified this hour: 1** — Kumaran Systems, *Salesforce Consultant*, Greater Toronto Area, posted 2026-11-20T20:08Z, 5+ yrs hands-on Salesforce dev/consulting (Sales/Service/Marketing), live LinkedIn detail page, expires 2026-12-20. Staged in `inbox/hermes-cron--2026-11-20--v13.md`, merged to README (Salesforce table 1200→1201), jobs.json + public mirrored, site rebuilt (5047 cards, SF 923→924).
- **Board health:** `board_invariants.py` → PASS ("no kind grew" vs baseline). Header count 6091 live.
- **Everything else surfaced was already on the board.** The board is saturated with 2026-11-19/11-20 postings from the automated hourly scan + earlier hermes runs; finding net-new requires looking *past* the obvious aggregator pages.

## What was checked, and why each lead was a duplicate

| Candidate (fresh-looking) | Where found | Resolution |
|---|---|---|
| CGI *ServiceNow Administrator/Developer* (Toronto) via Leading Talent re-list 2026-11-19 | leadingtalent.ca (JSON-LD `hiringOrganization=CGI`) | Already on board — LinkedIn 4462044907, 2026-11-06. The Leading Talent page is a re-aggregation of the CGI req. |
| BFG Enterprise Services *ServiceNow Administrator/Developer (Intermediate)* (Markham) | Glassdoor / CareerBeacon "posted yesterday" / careers.bfg.ca | Already on board — careers.bfg.ca/jobs/707075, 2026-11-03. Date conflict: CareerBeacon "yesterday" vs Talent.com "30+ days" → original is old, do not treat as fresh. |
| Bonafide Info Systems *ServiceNow ITOM Developer* (Toronto) | Glassdoor "24h" | Already on board — Job Bank 50740706, 2026-11-16. |
| SPECTRAFORCE *ServiceNow Developer* (Toronto) | LinkedIn 4492200627 | Already on board — 2026-11-18. |
| Konrad *Salesforce Architect (Loyalty & Data 360)* | landthatrole "New" | Already on board — LinkedIn, 2026-11-18. |
| OSI Digital *Salesforce Developer / BA* (Toronto) | landthatrole "7d" | Already on board — adzuna 5963223318 / 5963222927, 2026-11-12. |
| PwC *Salesforce BA Associate / Senior Associate* (Toronto) | landthatrole "7d" | Already on board — LinkedIn + adzuna, 2026-11-13/18. |
| Paralucent *Salesforce Agentic Developer* (Toronto) | FRESH_JOBS readme | Already on board — BuiltIn Toronto, 2026-11-19. |
| Recutify *ServiceNow Lead Developer* (Toronto) | Glassdoor | Already on board — adzuna 5961942687, 2026-11-11. |
| Resource Logistics *ServiceNow Developer* (Toronto) | snpro.jobs | Already on board — LinkedIn, 2026-11-16. |
| Spectra Group *ServiceNow Developer* (Toronto, $100–110/hr) | Glassdoor | Already on board — dice 731ebf90, 2026-11-12 (same "Specialized Developer – Expert" req). |
| Rexall, Veracity, Panasonic, Cognizant SAM Developer | Glassdoor / Adzuna | All already on board (Nov 2–13). |
| City of Toronto *Systems Integrator 1 (ServiceNow Developer)* Job ID 66386 | jobs.toronto.ca | **Closed** — posting period 05-Oct → 20-Oct-2026. Not fresh; skip. |
| Lightspeed *ServiceNow Developer* (Toronto, $85–105K) | jobs.ca / Real Ventures board | Old — posted Sep 18-2026 (30+ days); also already on board as Ottawa/Remote. |
| Cognizant *Salesforce Developer* 00071305431 (Toronto, remote-in-Canada) | careers.cognizant.com | Already on board — 2026-11-12 (us-en locale). |

## Partner / Elite-partner sweep (ServiceNow + Salesforce)

All current Toronto/GTA partner postings were already on the board; no net-new this hour.
- **Cognizant** — ServiceNow Technical Consultant (Oct 21) + ServiceNow SAM Developer (Nov 13) + Salesforce Technical Architect (4467116032) + SF Developer 00071305431 — all tracked.
- **Deloitte / KPMG / Accenture / TCS / PwC / Fujitsu / NewRocket / Pentio** — no *new* Toronto SN/SF platform req this hour beyond what the board holds (Deloitte SN consultant 2026-11-01, KPMG SN solution dev 2026-11-07, TCS SF dev 2026-11-18, PwC multiple, Accenture Data Cloud MarTech 2026-11-20, NewRocket gap scan clean).
- **Ateko (backed by Bell)** — SN hiring still routes through FX Innovation; SF through the ADP tenant. Already tracked; the two LinkedIn Ateko roles (2026-11-19) are on the board.

## Telco sweep

- **Rogers** — careers.rogers.com returned no ServiceNow/Salesforce platform req this hour (sales/marketing roles only).
- **Bell** — jobs.bell.ca zero for both platforms; Bell's SN hiring surfaces via Ateko/FX Innovation (already tracked).

## Government sweep

- **City of Toronto** — only SN posting (Systems Integrator 1, Job ID 66386) closed 2026-10-20. No open SN/SF dev.
- **Ontario Public Service (gojobs.gov.on.ca)** — no ServiceNow/Salesforce developer posting surfaced.
- **Federal (canada.ca / Job Bank)** — Job Bank servicenow/salesforce hits remain template noise; no titled SN/SF dev posting new this hour.

## Lessons & patterns for future agents

1. **Workday is the recurring blind spot.** The automated hourly scan hits 429 on TD/BMO/CIBC/Manulife Workday tenants almost every :01Z; those roles get recovered via Adzuna/LinkedIn mirrors. This run's Workday-derived leads (TD, CIBC, BMO) were all already covered by mirrors. When doing a manual pass, hit Workday directly at ~:05–:10Z after the throttle clears, or rely on the Adzuna/LinkedIn mirror of the same req.
2. **Aggregator "fresh" dates lie.** CareerBeacon/Talent/SimplyHired relist old reqs with "posted yesterday/24h". Always resolve the employer's own ATS date (JSON-LD `datePosted` or ATS API `first_published`) before calling something fresh. Two this run (BFG, Leading Talent→CGI) were old reqs re-listed.
3. **Lead-gen pages hide the real employer in JSON-LD.** `leadingtalent.ca` and similar registrar pages carry `hiringOrganization` in JSON-LD — reading it revealed the real issuer was CGI. Fastest way to convert an aggregator lead into a real employer+req.
4. **The board is genuinely saturated for Toronto SN/SF.** With 5047 rendered cards and hourly scanning, zero/low net-new per hourly run is normal and correct. Cross-checking `jobs.json` (feed) against README (curated) is the highest-yield way to find the handful of feed-only gaps (this run: Kumaran was the only one of 6k+).
5. **Gap analysis recipe that worked:** parse README URLs into a normalized set; scan `jobs.json` for postedDate in the last 2 days + Canada location + SN/SF in title/tags; diff. It surfaced exactly the 1 feed-only row.
6. **Do not blanket-run the inbox merger.** The accumulated 405-file inbox holds a backlog (≈15–267 stale Oct 22–27 rows incl. "Director, Marketing"). Running it unqualified pollutes the board with non-fresh, out-of-scope rows. Isolate your one file (`mv` the rest aside), merge, restore — the canonical merger then adds exactly your rows.

## Files touched this run

- `inbox/hermes-cron--2026-11-20--v13.md` (new — dated record + Kumaran row)
- `README.md` (Salesforce table +1 row, count 1200→1201)
- `jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`, `public/jobs-data.json`, `public/index.html` (synced/rebuilt)
- `JOBLESSONS_2026-11-20T1600EST.MD` (this file)

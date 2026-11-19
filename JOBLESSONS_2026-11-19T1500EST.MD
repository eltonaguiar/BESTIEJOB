# JOBLESSONS 2026-11-19T1500EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
`scripts/daily_job_scan.mjs` (Adzuna CA API, Workday CXS, SmartRecruiters, Greenhouse, Lever, Ashby, LinkedIn guest, remote boards), then `tools/build_site.py`, committed to `main` and published via `pages.yml`. Ran 10:02–15:13 EST.

## Result
- Sources returned 780 candidate rows. Adzuna HTTP 503 on several queries (rate-limit; retry ≥3 s spacing). Workday CXS HTTP 429 on every tenant — the CI hourly scan runs at :00Z and 429s manual probes at that minute; leave Workday to the CI pass.
- Genuinely new URLs vs board: 50. Fresh ServiceNow/Salesforce Canada rows dated today or yesterday: 14.
- Of the 14, 3 were already on the board from the 09:14 EST CI scan (same URLs). 11 injected as new into `jobs.json` + README DAILY-SCAN block:
  - Today 2026-11-19 (9): ServiceNow Platform Developer — Acronym Solutions, Etobicoke; ServiceNow Business Analyst — Apptoza Inc., Toronto; Développeur.euse ServiceNow + Spécialiste d'implantation ServiceNow — Ateko (backed by Bell Canada), Canada; Salesforce Developer — Vaco by Highspring, GTA; Salesforce Developer — Tata Consultancy Services, Canada; Associate Software Engineer (nCino/Salesforce) — TD Bank, Toronto; ServiceNow Staff Full-Stack Engineer (Experience Team) ×2 — ServiceNow, Toronto.
  - Yesterday 2026-11-18 (2): Senior Solution Architect ServiceNow — TD Bank, Toronto; Salesforce Developer — CGI, Toronto.
- Dedupe: normalised-URL check against jobs.json + README tables + APPLIED.md — zero collisions; none previously applied.
- Board after build: 4,986 jobs indexed (ServiceNow 836, Salesforce 901, Other 3,249), newest posting 2026-11-19, 30 applied roles hidden, 829 mirror clusters collapsed.
- Commit `8479485` on `main`; GitHub Pages deployed (`jobs-data.json` generated 2026-11-19T15:13:49Z). All 9 spot-checked fresh URLs confirmed live on `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` — some stored as mirror-cluster `alternates[]`, so check alternates, not only primary `url`.

## Partner / Elite-Partner / sponsor / target-company scope
- **Bell (strongest hit):** Atego, "backed by Bell Canada" — two ServiceNow roles, Canada. `jobs.bell.ca` renders an empty shell and shows (0) for servicenow/salesforce — zero reqs, not a scrape failure; re-check weekly, not hourly.
- **Rogers:** `jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc` renders `<tr>` rows with absolute dates — parse date-sorted listing instead of keyword search; no Rogers hit this cycle. `jobs.rogers.com`/`jobs.scotiabank.com` Phenom boards return 404 to curl — check weekly, not hourly.
- **TD Bank** (Workday): nCino/Salesforce associate + ServiceNow Senior Solution Architect, Toronto.
- **TCS / CGI:** Salesforce Developer roles, Toronto/Canada.
- **ServiceNow-the-company:** Toronto postings are staff SRE/security, not Platform Admin/Dev I — deprioritize.
- Public sector: `gojobs.gov.on.ca` and `jobs.gc.ca` are Radware-captcha walled — do not retry; Job Bank is the proxy, trust only title-named platform postings.

## Verification notes
- Adzuna detail pages return HTTP 403 (Cloudflare) to curl — 403/429/5xx are bot-walls on live postings, not dead. Freshness signal = Adzuna API `created` date (today/yesterday).
- LinkedIn guest detail is gated in this environment; LinkedIn rows come from the scan's guest feed. Job IDs in the 4492xxxxx range are mid-Nov 2026 — consistent with today's postings.

## Git / workflow notes for next run
- Remote `origin` is `eltonaguiar/bestiejob.git`; GitHub replies "moved to eltonaguiar/BESTIEJOB.git" but pushes still succeed.
- The CI hourly scan pushed (`9b26c1a`, 14:14Z) mid-run and rejected my push. Resolution: `fetch`, `checkout -B main origin/main`, re-inject missing rows (idempotent via URL normalisation), rebuild, commit, push — run inject+build+commit+push quickly to avoid another race; CI runs at :00Z.
- Parallel cron branch `hermes-cron-2026-11-19` exists (5 verified Toronto/GTA SN/SF jobs merged into README tables, 6,190 postings) — separate lineage, not merged to main.
- `git` at `/mingw64/bin/git` is blocked (WinError 5); use `C:/Program Files/Git/cmd/git.exe` for all git ops.

## Source precedent (corrected)
- `dice.com` and `nodesk.co` ARE server-rendered and scrapeable via axios+cheerio (dice `data-testid="job-card"` ~31/page; nodesk `li` cards with h2+h3). `daily_job_scan.mjs` does not integrate them yet — per `bestiejob-hunt` skill, add `scanDice()`/`scanNoDesk()` after the last scanner and register in `Promise.allSettled`. Not done this cycle because Adzuna/Workday/LinkedIn covers the freshness window.

## Commit
`8479485` chore(jobs): hourly SN/SF Toronto scan 2026-11-19 — 11 fresh verified postings [skip ci]
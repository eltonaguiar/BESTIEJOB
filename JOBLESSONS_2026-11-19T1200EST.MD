# JOBLESSONS 2026-11-19T1200EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
`scripts/daily_job_scan.mjs` full hourly pass at 2026-11-19T17:02:56Z (12:02 EST), then `tools/build_site.py`, committed to `main` and published via `pages.yml`.

Sources queried: SmartRecruiters (ServiceNow board), Workday CXS (altusgroup, iko, huron, irvingoil, mckesson, brookfield, gdit, resolvetech, medcan — all HTTP 429 at the :00Z CI hour), Greenhouse, Lever, Ashby, LinkedIn guest (HTTP 429 first attempt, 274 postings on retry), Adzuna CA API (485 postings), RemoteOK/Jobicy/Remotive.

## Result — this cycle
- Fresh candidates surfaced: 804. Genuinely new URLs vs the board (HEAD jobs.json had 5,570 rows): exactly **1**.
- Merged 1 fresh verified posting into `jobs.json` (inserted at head), the README `<!-- DAILY-SCAN -->` block, and `public/`:
  - **Senior ServiceNow Consultant — Flexstaf I.T. Inc., Toronto, Ontario, Canada — LinkedIn, posted 2026-11-19** — https://ca.linkedin.com/jobs/view/senior-servicenow-consultant-at-flexstaf-i-t-inc-4492170849
- Already on board (deduped, not re-added):
  - Shodh Consultancy "Salesforce Architect [Sales Cloud Service Cloud]" Mississauga (adzuna.ca/details/5970383356, from `inbox/fresh-ca--2026-11-19--v1.md`) — present in jobs.json + README.
  - Wipro "ServiceNow Implementation Architect" Mississauga (linkedin 4486514927) — present in README main table.
  - Every other DAILY-SCAN block row (ServiceNow Business Analyst Apptoza, Staff Full-Stack Engineer ServiceNow ×2, Flexstaf Revenue Cloud Architect ×4, PwC Technical Salesforce Associate, CGI Salesforce Developer ×3, Serefin Salesforce DevOps ×3, TD nCino Associate Software Engineer, plus Salesforce/Other keyword matches) — already in HEAD jobs.json or README tables.
- Board state after merge: `jobs.json` = 5,571 jobs; `build_site.py` indexed 4,993 (ServiceNow 839 · Salesforce 903 · Other 3,251), newest posting 2026-11-19, 832 mirror clusters collapsed, 30 applied roles hidden.

## Git / Pages
- Commit `41e5ec8` on `main`; pushed `origin/main` (b694ebf..41e5ec8). Remote suggests `eltonaguiar/BESTIEJOB.git` but pushes still succeed.
- `pages.yml` run 44573880151 started 17:08:20Z, concluded **success**.
- Live page verified: `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` returns 4,993 jobs and carries the Flexstaf URL. `https://eltonaguiar.github.io/BESTIEJOB/` tracks `main`.

## Lessons for future agents
1. **Workday CXS returns HTTP 429 on every tenant at the :00Z CI hour** — manual probes collide with the hourly scan; leave Workday to the CI pass or retry ≥8 s apart off-hour.
2. **`daily_job_scan.mjs` replaces `jobs.json` with its own scan cache** (this cycle: 5,570 → 2,467 rows, dropping ~3,105 readme-sourced rows). Always `git checkout HEAD -- jobs.json` after the scan, then insert only genuinely new rows (delta via normalized-URL diff), so the master board is never shrunk.
3. **LinkedIn guest endpoint rate-limits (HTTP 429)** — retry the same URL after a short wait; a healthy response differs in body/digest per query, don't trust status=200 alone.
4. **Dedupe by normalized URL** (strip query string + trailing slash, lowercase) against `jobs.json` + `README.md` + `APPLIED.md`; vendor twins (different staffing firms, same client req) are kept.
5. **`tools/build_site.py` unions `jobs.json` + README rows whose URL key is absent from JSON** — a row present only in README still renders as a card, so a README-only hit (e.g. Wipro via linkedin-guest inbox) doesn't need a `jobs.json` row.
6. **Commit `public/jobs-data.json` and `public/index.html` alongside `jobs.json`** — the live page serves only committed files; do NOT skip CI when `public/` changes if you want the Pages deploy this cycle (`[skip ci]` only for docs/lessons-only commits).
7. **`gh` workflow commands work for triggering/polling; `git push` over HTTPS works** — bash `/mingw64/bin/git` handled fetch/checkout/push fine in this run.

## Commit
`41e5ec8` chore(jobs): hourly SN/SF Toronto scan 2026-11-19T1700EST — 1 fresh verified posting [no skip ci — pages deploy]

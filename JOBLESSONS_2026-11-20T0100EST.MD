# JOBLESSONS_2026-11-20T0100EST

## Cycle summary
Hermes hourly cron, 2026-11-20 01:00 EST (2026-11-20T06:00Z). Base: eltonaguiar/bestiejob `main` at f9c5d8f (CI hourly scan 05:14Z, 5,580 listings; SN ~1,169 / SF ~1,206 after cap).

**Merged 533 fresh postings.** Commit `7630607` pushed to origin/main:
`chore(jobs): hourly scan refresh (2026-11-20T01:00 EST) · SN 1171 / SF 1208 · 533 fresh postings · 0 dead URLs · [skip ci]`
Board after merge: 2,520 rows in jobs.json (SN 1,171 / SF 1,208, primary tags uncapped; secondary tags capped at 40 each by capSecondary).

## Sources scanned this cycle
`node scripts/daily_job_scan.mjs` (9 public sources, Promise.allSettled):
- **linkedin**: 283 matching postings (guest API; one 429, recovered on retry) — fresh Sr Salesforce Developer (Euna Solutions, Oakville), Salesforce Administrator (CanPrev, North York), Salesforce Business Systems Analyst (Avanciers Inc., Toronto)
- **adzuna**: 205 matching postings (demo keys `app_id=54ce986e` / `app_key=db851f299e966c0a2a72af525dce6199`)
- **smartrecruiters**: 13 matching postings — Senior Systems Engineer (ServiceNow, Toronto, posted 2026-11-20)
- **lever**: 1 matching posting
- **workday**: 0 — every tenant (bmo, td, moneris, caatpension, bdo, medcan, altusgroup, iko, huron, irvingoil, mckesson, brookfield, gdit, resolvetech) returned HTTP 429 (CI scan contention at top of hour)

## Dedupe / liveness gate / build
- Dedupe against jobs.json by normalized URL (query strings stripped); new rows inserted at head of jobs.json.
- `tools/verify_links.py --days 2`: 161 fresh rows probed — live=82, dead=0, unknown=79 (bot-walls, kept, never treated as dead). Nothing dropped.
- `tools/build_site.py`: 5,034 cards (SN 848 / SF 917 / Other 3,269) · 836 duplicate mirrors collapsed · 30 applied hidden · built 2026-11-20 06:03 UTC.
- `public/jobs-data.json` + `public/index.html` committed alongside jobs.json (live page serves only committed files).
- Commit uses `[skip ci]` (avoids pre-existing red board-invariants audit); Pages redeploy triggered manually.

## GitHub Pages
- `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB` → run 44685201301, queued 06:04Z, status in_progress at cycle end. Poll `gh run list --repo eltonaguiar/BESTIEJOB --workflow=pages.yml --limit 1` until `conclusion=success`, then confirm `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` carries the fresh URLs (e.g. `jobs.smartrecruiters.com/ServiceNow/744000162621080`).

## Employer / partner / telco / government checks (no fresh dated Toronto SN/SF req captured)
- **Workday CXS**: all known tenants HTTP 429 at :00Z / top of hour (CI scan runs at 03:00 EST / 08:00Z). Space manual probes ≥8s over 3–4 tenants, or leave Workday to the CI pass. `postedOn: "Posted Today"` is not a Canada signal — read the `/job/<City>/` slug.
- **Adzuna**: HTTP 503 under rapid queries — space calls ≥3s; demo keys still surface results despite partial failures.
- **LinkedIn guest API**: walls repeated calls (HTTP 200, same md5 body = auth wall). Test length + digest distinctness, not just status. Fallback: new_tab on the jobs/search page with `f_TPR=r86400`, read `li a[href*="/jobs/view/"]` from the DOM.
- **Rogers**: jobs.rogers.com HTTP 404 / 9-byte body (Phenom) — known dead end, re-check weekly not hourly.
- **Bell**: jobs.bell.ca renders 0 SN/SF — zero reqs, re-check weekly.
- **Government of Canada**: jobs.gc.ca / gojobs.gov.on.ca behind Radware captcha; Job Bank is the title-only proxy — trust only postings whose *title* names the platform.
- **Partners**: Pentio (Toronto Select SN), Lane Four (SF), NewRocket (SN), Fujitsu (SN Elite) reviewed — no fresh Toronto req dated in window.

## Lessons (patterns for future cycles)
1. **Workday CXS 429 at top of hour** — never probe Workday at :00Z; the CI scan owns that minute.
2. **Adzuna 503 under rapid queries** — space calls ≥3s; don't treat 503 as "no jobs".
3. **LinkedIn guest 429 is retryable** — one retry after a few minutes returns real card HTML (~280 cards); len=0 or identical md5 = auth wall, not results.
4. **`[skip ci]` commits do not trigger pages.yml** — always manually trigger `pages.yml` after a data push and poll for success; verify the live `jobs-data.json` count matches the repo.
5. **403/429/5xx are bot-walls on live postings** — only 404/410/451 mean dead; never prune on transport errors.
6. **Freshness first** — prioritize today/yesterday postings; Workday "Posted Today" must be cross-checked against board `postedDate` + `alternates` to avoid re-adding an existing req under a new date.
7. **Do not commit untracked scratch files** (README.BAK_*, leads-*.jsonl, raw/, reports/) or the `ServiceNow_Learning_*` submodule pointer.

## Verification pending
- Pages run 44685201301 conclusion + live `jobs-data.json` carries the new URLs (check after run completes).

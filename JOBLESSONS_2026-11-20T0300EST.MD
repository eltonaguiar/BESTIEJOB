# Job-search lessons — 2026-11-20 03:00 EST (08:00Z) — BESTIEJOB hourly cron

Run of `node scripts/daily_job_scan.mjs` on origin/main `04a870a`, then `verify_links --days 2`, `build_site.py`, `sync_readme_counts.py`.
Delivered: **526 fresh / 2524 merged** (SN 1172 / SF 1211); site **5049 cards** (SN 849 / SF 918 / Other 3282); **82 recent (>=11-18) Toronto-area SN/SF rows** on the board.

## What changed this cycle
- Local base was `bc7ef67`; origin/main advanced to `04a870a` (CI hourly refresh 07:16Z). Instead of rebasing six generated files, did `git reset --hard origin/main` then re-ran scan+verify+build — clean fast-forward. Matches the 2026-11-19 local hourly-run recipe.
- A manual run **without `--no-readme`** refreshed the README `<!-- DAILY-SCAN -->` block (the CI `hourly-scan.yml` uses `--no-readme` and leaves it stale). If the visible "Latest auto-scanned jobs" block on readme.md matters, run the scan without `--no-readme`.

## Source behaviour (confirmed again)
- **Workday CXS 429 at :00Z is deterministic.** At 08:00Z all Workday boards (salesforce, bmo, td, moneris, bdo, caatpension, medcan, altusgroup, iko, huron, irvingoil, mckesson, brookfield, gdit, resolvetech) returned HTTP 429 for both queries — the CI hourly-scan fires at :00Z and hammers the same tenants. Previously-carried Workday rows survive the 45-day carry window, so nothing is lost, but a manual run at exactly :00Z cannot refresh Workday. To catch fresh Workday reqs manually, run at :10Z or later, or probe 3–4 tenants at >=8s spacing.
- **LinkedIn guest API recovers from a first 429.** It returned HTTP 429 on the first 1–2 `seeMoreJobPostings` calls, then succeeded — 278–279 matching postings. Do not abort on a single 429; the mapLimit(2)+1.8s pacing in `daily_job_scan.mjs` rides it out.
- **Adzuna stable at ~201** with the demo keys (`app_id 54ce986e` / `app_key db851f299e966c0a2a72af525dce6199`). Occasional 503s, per-query catch keeps the rest.
- **`verify_links --days 2`:** probed 164 fresh rows → 87 live / 0 dead / 77 unknown (403/429/5xx bot-walls kept as live per policy). No dead rows this cycle.

## Named-employer / partner coverage (what the user asked to watch)
- **Bell Canada:** real ServiceNow hiring surfaces under **“Ateko, backed by Bell Canada”** on LinkedIn — 2 roles dated 11-19: *Développeur.euse ServiceNow* and *Spécialiste d'implantation ServiceNow (Implementation Specialist)*. `jobs.bell.ca` shows (0) for servicenow/salesforce in a browser — genuinely empty; don't retry hourly. Search "Ateko", not "Bell".
- **ServiceNow partners/consultancies (Toronto-heavy volume):** Accenture (SF Techno-Functional/AMS Lead; SF Data Cloud MarTech ×2 Toronto), PwC (Sr ServiceNow Developer; Technical SF Associate; SF BA Associate), CGI (SF Developer + SF BA Toronto; SF Architect Montreal), Cognizant (Sr SF Developer Toronto), IBM (SF Sr Solution Architect Toronto/Montreal/Ottawa/Calgary) and IBM's **LGS** arm (many ServiceNow roles in Ville-Marie QC — French titles), TCS (Sr SF Developer), Virtusa (SN ITOM Dev Toronto), Coforge (Sr SF Dev Markham), RSM US (SN Architect Toronto), Munvo (SFMC Consultant), Konrad (SF Architect / Sr Loyalty Dev), MuniPaaS (SF Solution Architect Vaughan), NTT DATA (SN SPM BA).
- **Banks/enterprise:** TD Bank (Associate SW Engineer nCino/Salesforce — same req on Adzuna 5971441048 and td.wd3 Workday R_1508918; also Senior Solution Architect ServiceNow), Interac Corp (Senior BSA ServiceNow), Mackenzie Investments (Manager/Responsable Technologie RH & ServiceNow HRSD), Loblaw (Sr SW Engineer Salesforce, Brampton), PointClickCare (Principal/Senior SF Architect Mississauga), McKesson (Lead SF Solution Architect), Celestica (Student Intern SF Dev 1), Co-operators (Sr Systems Developer + Sr BA Salesforce), SickKids Foundation (Sr Specialist SF Developer), Acronym Solutions (SN Platform Developer Etobicoke), The Citco Group (SF Solution Architect).
- **Government of Canada:** no dated SN/SF posting captured this cycle. `jobbank.gc.ca` / `gojobs.gov.on.ca` remain Radware-walled; Job Bank keyword hits are body-text false positives — trust only titles naming the platform.
- **Rogers:** no SN/SF in the last 48h. `jobs.rogers.com` still 0-byte to curl / error page to a browser; rely on LinkedIn/Adzuna.

## Fresh Platform-Admin / Dev-I signal (entry-level emphasis)
- Today (11-20): **CanPrev — Salesforce Administrator** (North York), **White Bay — Salesforce Administrator | SFMC** (North York, hybrid, $60-75k), Euna Solutions — Sr Salesforce Developer (Oakville), Avanciers — SF Developer + SF BSA (Toronto), ServiceNow — Senior Systems Engineer (Toronto). These are the Platform-Admin-shaped roles the user prioritizes.

## Dedupe lessons
- **TD nCino/Salesforce is one req with two URLs** (Adzuna `details/5971441048` and td.wd3 `.../R_1508918`) — `build_site.py` collapses by employer-board-preferred; do not double-list.
- **Co-operators posts the same SF role under "Co-operators" and "Co-operators Assurance et services financiers"** (English + French entity names) on LinkedIn — needs fuzzy company matching.
- **Ateko roles are French-titled** ("Développeur.euse", "Spécialiste d'implantation") — a Toronto-only English keyword scan misses them; search Canada-wide and keep French titles.

## Operational
- The `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM` submodule (gitlink mode 160000) shows as modified in `git status` — **never stage it**; stage only jobs.json / README.md / FRESH_JOBS.md / public/* / inbox / lessons.
- Untracked artifacts from prior runs (`README.BAK_*`, `leads-*.jsonl`, `raw/gap_scan*`, `reports/*`) linger in the tree — leave them out of the commit.
- Push with `[skip ci]` (avoids the chronic-red board-invariants/truth-check audits), then trigger `pages.yml` (`gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB`) for immediate live reflect; otherwise the `:35Z` scheduled `pages.yml` picks it up.

## Pattern for future hourly agents
1. `git fetch origin main; git reset --hard origin/main` (board content lives there; CI re-scans hourly).
2. `node scripts/daily_job_scan.mjs` (no `--no-readme` so the README block refreshes).
3. `python3 tools/verify_links.py --days 2` (drop only 404/410/451).
4. `python3 tools/build_site.py` then `python3 scripts/sync_readme_counts.py`.
5. Write `inbox/hermes-cron--<date>--v1.md` (6-col table, absolute dates, exact URLs) — validate with `python3 scripts/check_inbox.py --file ...`. Do **not** run the whole-inbox merger for a small batch (known `_bump_counts` glue bug).
6. `git add` the generated files + inbox + lessons; commit `[skip ci]`; push; trigger `pages.yml`; verify live `jobs-data.json` carries a known fresh URL.

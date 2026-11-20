# JOBLESSONS_2026-11-20T0200EST

## Cycle summary
Hermes hourly cron, 2026-11-20 02:00 EST (2026-11-20T07:00Z). Base: origin/main `6db6493` (fresh CA sweep 06:51Z; CI hourly scan 06:22Z, 5,575 listings). Scanned → deduped → liveness-gated → built → pushed `a146cb4`.

Board after merge: **jobs.json 2,522 rows** (SN 1,172 / SF 1,209, primary tags uncapped; secondary tags capped at 40 each by `capSecondary`). **Site 5,063 cards** (SN 849 / SF 918 / Other 3,296). README header **6,276 live postings** (was 6,184).

## Sources scanned this cycle
`node scripts/daily_job_scan.mjs` (9 public sources, Promise.allSettled):
- **linkedin**: 290 matching postings (guest API; no 429 this cycle)
- **adzuna**: 204 matching postings (demo keys `app_id=54ce986e` / `app_key=db851f299e966c0a2a72af525dce6199`)
- **greenhouse**: 17 · **smartrecruiters**: 13 (incl. ServiceNow-company "Senior Systems Engineer", Toronto, posted 2026-11-20)
- **remotive**: 6 · **jobicy**: 3 · **ashby**: 2 · **remoteok**: 2 · **lever**: 1
- **workday**: ALL 15 tenants returned **HTTP 429** at 07:00Z top-of-hour (bmo, td, salesforce, moneris, caatpension, bdo, medcan, altusgroup, iko, huron, irvingoil, mckesson, brookfield, gdit, resolvetech). 1 posting attributed to workday in the merged feed (carried TD req).

`fresh=539 merged=2522` — note `fresh` means "within 45 days", NOT net-new. Net-new to jobs.json this cycle: **31 URLs (29 SN/SF)**, dominated by older resurfacing rows; genuinely dated today/yesterday fresh Toronto SN/SF: TD nCino SWE (11-19), Apptoza SN BA (11-19), Amicis SN BA Senior (11-19), Ateko/Bell SN Dev + Implementation Specialist (11-19), CanPrev SF Admin + Avanciers SF BSA + White Bay SFMC Admin (11-20), ServiceNow Sr Systems Engineer Toronto (11-20), W3Global SN ITAM/ITOM Architect (11-20).

## Partner / partner-Elite / telco / government checks
- **Bell Canada → Ateko (backed by Bell Canada / FX Innovation)**: **2 fresh ServiceNow roles posted 2026-11-19** — "Développeur.euse ServiceNow" and "Spécialiste d'implantation ServiceNow" — both LIVE on the board. This is the notable fresh find this cycle. Ateko is Bell's ServiceNow unit; search **"Ateko"** on LinkedIn, not just "Bell" (jobs.bell.ca itself shows 0 SN/SF).
- **Rogers**: `jobs.rogers.com` returned **HTTP 200 with a 0-byte body** to curl (empty JS shell) — unusable for direct scraping. 1 fresh Rogers row captured via aggregator (Lead Management Operations, Ottawa — not SN/SF). Phenom board remains a dead end.
- **Government of Canada / Ontario**: **0 fresh SN/SF titles** in the last 3 days. `jobs.gc.ca` / `gojobs.gov.on.ca` still behind Radware captcha.
- **Elite partners / consultancies**: 189 fresh partner-keyword rows. Notable: ServiceNow-company Sr Systems Engineer (Toronto 11-20), Accenture SF Techno-Functional AMS Lead, PwC SN Developer + SF Associate, CGI SF BA (Toronto 11-19), Cognizant, KPMG SN Solution Developer (11-07), Deloitte SN Platform Sr Consultant (11-01). Agency mirrors (Pacer, Apptoza, Avanciers, Flexstaf) reflect TCS/BMO/TD client reqs — keep as distinct postings.

## Dedupe / liveness gate / build
- Dedupe by normalized URL (query strings stripped). Net-new 31 URLs (29 SN/SF); duplicate adzuna mirrors of TD "Senior Solution Architect (ServiceNow)" collapsed under the canonical Workday (`td.wd3…R_1521185`) + LinkedIn URLs — the role still renders.
- `tools/verify_links.py --days 2`: 162 fresh rows probed — **live=83, dead=0, unknown=79** (bot-walls; kept, never treated as dead). Nothing dropped.
- `tools/build_site.py`: 5,063 cards (SN 849 / SF 918 / Other 3,296) · 849 duplicate mirrors collapsed · 30 applied hidden · built 2026-11-20 07:03 UTC.
- `scripts/sync_readme_counts.py`: README header total 6,184 → **6,276** live postings.
- README `<!-- DAILY-SCAN -->` block auto-rewritten by the scan with newest 12 SN + 12 SF + 10 other.

## GitHub Pages
- Push `a146cb4` to `origin/main` (remote redirects `eltonaguiar/bestiejob.git` → `eltonaguiar/BESTIEJOB.git`).
- `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB` → run **44692215458**, queued 07:04:01Z, **conclusion=success**.
- Live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json`: **5,063 jobs**; verified fresh URLs PRESENT (Apptoza `4491626483`, CanPrev `4492535763`, Amicis `5972002660`, Acronym `4492159456`).

## Lessons (patterns for future cycles)
1. **Workday CXS still 429s on every tenant at the top of the hour (07:00Z).** Local hourly runs at :00Z cannot reach Workday; it is covered only by the CI 08:00Z pass. Space any manual probe ≥8s or skip Workday entirely on top-of-hour runs.
2. **`fresh=` in the scan summary is "within 45 days", not net-new.** Compute net-new by diffing normalized URLs against `origin/main:jobs.json`; report the genuinely dated-today/yesterday rows explicitly rather than the raw `fresh` number.
3. **Adzuna mirror URLs get collapsed by `build_site.ident_key`** onto a Workday/LinkedIn canonical row. A raw URL-subset check will report the adzuna mirror "NOT-LIVE" even though the role renders — verify by company+title on the live feed, not URL only.
4. **Bell Canada's ServiceNow work flows through "Ateko (backed by Bell Canada)"** (a.k.a. FX Innovation). Search "Ateko" on LinkedIn; `jobs.bell.ca` itself shows 0 SN/SF reqs.
5. **Rogers Phenom careers returns HTTP 200 with a 0-byte body** — treat as unparseable; rely on aggregators (a Rogers row surfaced via adzuna/linkedin).
6. **`[skip ci]` data push does not trigger pages.yml.** Always `gh workflow run pages.yml`, poll `gh run list --workflow=pages.yml --limit 1` to `conclusion=success`, then confirm the live `jobs-data.json` count matches the repo (5,063) before declaring done.
7. **`sync_readme_counts.py` edits only the README header total**; the DAILY-SCAN block is separate and is rewritten by `daily_job_scan.mjs`.
8. **Do not commit untracked scratch** (`README.BAK_*`, `leads-*.jsonl`, `raw/`, `reports/`) or the `ServiceNow_Learning_*` submodule pointer. Stage only the 8 generated files.

## Verification
- `origin/main` at `a146cb4`. Pages run 44692215458 success. Live `jobs-data.json` = 5,063 jobs, fresh Toronto SN/SF URLs present. jobs.json 2,522 (SN 1,172 / SF 1,209).

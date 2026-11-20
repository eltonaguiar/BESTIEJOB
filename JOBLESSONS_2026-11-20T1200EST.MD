# JOBLESSONS — 2026-11-20 12:00 EST (17:00Z) hourly ServiceNow / Salesforce scan

Run context: Hermes cron hourly scan. Start `origin/main` = 075493c (CI hourly scan, 16:15Z; `jobs.json` 5,586 rows, README header **6131 live postings**, SN 1226 / SF 1177 / Other ~4089). Local 1 commit behind; pulled ff-only first.

Outcome: **2 verified net-new** merged to README + `jobs.json` + GitHub Pages data.
- **iA Financial Group (Industrial Alliance)** — *Directeur(trice) adjoint(e), Plateforme ServiceNow* — Québec, QC. LinkedIn 4492965179. JSON-LD `datePosted 2026-11-20T16:44:08Z`, `validThrough 2026-12-20`, body + guest fragment verified ("20 minutes ago" at check).
- **IH** — *Salesforce Financial Services Cloud Architect - Contract to Hire - Montreal, Canada (Hybrid)* — Montréal, QC. LinkedIn 4491935347. Body + guest fragment verified ("1 hour ago"); FSC technical-architect duties, FR/EN.

Both were absent from README + `jobs.json` + APPLIED by job id **and** by company+title, and had no cross-source twin (checked `Financial Services Cloud Architect`, `Contract to Hire`, `plateforme ServiceNow`, `Industrial Alliance`). Board now **6133 live postings**; site **5054 cards (SN 864 / SF 924 / other 3266)**, built 17:10Z. Guards: `check_readme_sort` OK, `check_site_links` OK, `board_invariants` **PASS (31 errors, baseline 34, no kind grew)**.

## Source-by-source findings (reuse next hour)

| Source | Result this hour | Notes for next agent |
|---|---|---|
| Adzuna CA API (10 queries, `max_days_old=2`, sort_by=date) | ~204 rows; **0 net-new URLs** | Same-day id recycling again (Amicis BA re-issued yesterday under a fresh id). Detail pages still CloudFront-403 to curl; trust the API row, dedupe on company+title. |
| LinkedIn guest search (24 queries × Toronto+Canada, `f_TPR=r86400`) | 240 cards, 200 OK throughout, **no 429 this run** | Only 2 untracked. 10 cards/query cap means query breadth beats paging. The two adds came from "ServiceNow developer" and "Salesforce CPQ" passes. |
| LinkedIn guest — second pass (20 queries: nCino, FSC, ITAM, HRSD, CSM, Agentforce, CRM, platform dev, discovery, integration) | 200 cards, **0 net-new** | Saturation confirmed. Do not repeat the same 20 next hour; rotate title variants instead. |
| Workday CXS (Salesforce, Accenture, TD, BMO, CIBC, Manulife) | All tenants **200** at 17:10Z (no :00Z 429) | Zero fresh Canada SN/SF reqs. BMO "ServiceNow CMDB Administrator" (Toronto, 8d) is already on the board under an Adzuna/LinkedIn URL — **exact-URL dedupe misses cross-source twins**, so also compare company+title. |
| Workday dead slugs | Rogers `rogers.wd3` 422, TELUS 422, Canada Life 422, RBC 404 | Phenom/Workday host guesses are not reliable; treat as dead ends and don't re-probe hourly. |
| Greenhouse partners: NeuraFlash (70 jobs), NewRocket/highmetric (44) | 68 / 40 geo-matched, **0 net-new URLs** | All Canada listings already tracked. NewRocket's Director/IRM roles are old-vintage per 09:00 lessons. |
| Rogers / Bell (public careers sites) | Rogers Phenom shell / Bell Phenom client-side — no server-rendered dates | Unchanged; weekly recheck only. Bell SN hiring still surfaces as "Ateko, backed by Bell Canada" on LinkedIn. |
| Government / public sector | Not re-probed beyond scan (Job Bank full-text is noise; jobs.gc.ca Radware-walled) | Ontario VOR work keeps arriving as RQ##### agency rows (TWC/Cleo/Metrolinx, already on board). |

## Mechanics lessons (important)

1. **README carries a pre-existing glued-row defect on the two section-header lines.** The ServiceNow header line holds **9 dated rows glued after `</summary>`**, the Salesforce header **6** (rows separated by `||`, no newline). `extract_rows` parses only the first row per line, while `count_dated_rows` counts cells — the two errors cancel, so `board_invariants` reports OK and you won't notice. **Insert new rows as standalone lines after the header; never insert through the header line.**
2. **Do NOT run `tools/jobs_merge_inbox.py` globally on this repo.** A dry run wanted **+186 rows** from stale `twin-harvest--2026-11-03--v106.md` (83), `websearch--*` and October rows (including a "Director, Marketing" row the board would reject). CI may have merged-then-pruned these historically; a hand run would inject them. Merge only your own file: copy it to a temp dir, set `jobs_merge_inbox.INBOX = tempdir`, then `J.main()` with `sys.argv=['x','--today','2026-11-20','--max-per-table','4000']`. The merger's `insert_rows` still appends into glued lines, so after merging **verify** the rows are line-start rows (`grep -n '^| 2026-11-20 | \[…'`) and fix with a direct `lines.insert()` if not.
3. **Bump the visible counts manually when inserting by hand:** `(1226)→(1227)`, `Show 1155 postings→1156`, same for Salesforce, then run `scripts/sync_readme_counts.py` to recompute the `**N live postings**` claim with `board_invariants`' own parser (6131 → 6133).
4. **`sync_readme_to_jobs.mjs` is the bridge README→jobs.json** (and copies to `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json`). Run it before `tools/build_site.py`; the site reads README, the API/feeds read jobs.json, so both must be in sync.
5. **Python**: `python3` on PATH is the WindowsApps stub. Use `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe`. Node v26 runs the `.mjs` scripts fine.
6. **Commit data files only** — never `raw/`, `leads-*`, `reports/`, `README.BAK_*`, or the `ServiceNow_Learning…` submodule pointer. Push `[skip ci]` (matches CI pattern), then `gh workflow run pages.yml` for an immediate Pages redeploy (or wait for the :35 hourly deploy).
7. **Check `origin/main` right before pushing.** The 17:00Z CI hourly workflow races this job; on a rejected push, `git pull --rebase --autostash origin main` and push again.

## Dedupe keys that worked
- Normalized URL (strip query/hash/trailing slash; host lowercased, `www.` dropped) for exactness.
- `company.lower()|title.lower()` to catch reposts and cross-source twins — this is what classified 66/68 candidates as already tracked when their URLs differed.
- LinkedIn 10-digit job id as a tie-breaker; Adzuna detail id is **not** stable (recycled).
- Verify freshness from the posting's own JSON-LD `datePosted`, not the aggregator's "posted X hours ago".

# JOBLESSONS_2026-11-19T0500EST — BESTIEJOB hourly scan cycle 5

**Run:** 2026-11-19 05:00 EST (2026-11-19T10:00Z), cron job. **Board after run:** 6211 live postings (README header synced), ServiceNow + Salesforce tables, Toronto-first scope.
**Commit target:** main branch of github.com/eltonaguiar/bestiejob.git; GitHub Pages rebuilt via public/.

## What the scan found

Source: FRESH_JOBS.md, output of `scripts/daily_job_scan.mjs` (2026-11-19T09:13Z) — 2437 postings from 10 public sources: adzuna 491, linkedin 279, workday 19, greenhouse 17, smartrecruiters 13, remotive 6, jobicy 4, ashby 2, lever 1, remoteok 1.

Merged into README.md (3 rows, all ServiceNow, Toronto, dated 2026-11-18, deduplicated by URL against 6252 parsed link-rows — none were already present):

| Posted | Role | Company | Location | Source |
|---|---|---|---|---|
| 2026-11-18 | ServiceNow ITOM Developer | TechNeptune Consulting Inc. | Toronto, Ontario, Canada | LinkedIn (4491345268) |
| 2026-11-18 | ServiceNow Developer | SPECTRAFORCE | Toronto, Ontario, Canada | LinkedIn (4492200627) |
| 2026-11-18 | ServiceNow CMDB | TechNeptune Consulting Inc. | Toronto, Ontario, Canada | LinkedIn (4491354155) |

Submission file: `inbox/hermes-cron--2026-11-19--v1.md` (passed `scripts/check_inbox.py`; merged with `--allow-row-loss` because README holds 2 pre-existing unreadable glued lines — nothing was dropped).
Normalization (`scripts/normalize_board.py --apply`) removed 3 pre-existing vendor-sales rows ("Sr Solution Sales Executive CRM (CPQ)"). My rows were not affected.
Feed + pages rebuilt: `jobs.json` (5501 rows), `public/jobs-data.json`, `public/index.html`, `board.html`.

## What was found but NOT merged (verification barriers — record for next cycle)

1. **LinkedIn detail pages behind sign-in wall.** All five ca.linkedin.com detail URLs opened show the "Agree & Join / sign in" wall — no datePosted, no duties readable unsigned. Duties could not be re-verified on employer pages. Rows merged above rest on scan evidence (title + date + location from the committed daily scan) with the limitation disclosed in the row note. Same reason cycle 4 dropped PwC "Salesforce Business Analyst, Associate" 4492083143. Candidates left in review:
   - Accenture "Consultant MarTech spécialisé en Salesforce Data Cloud" ×2 (Toronto, 2026-11-19) — also "MarTech" title leans marketing-ops; runbook rejects sales/marketing by title unless platform/analytics work is clear.
   - PwC Canada "Salesforce Business Analyst, Associate" (Toronto, 2026-11-18) — cycle-4 precedent: drop.
2. **Adzuna detail URLs blocked (CloudFront 403)** via both `urllib` and the browser — employer page and duties unverifiable:
   - Nuvei "Salesforce Business Process Analyst" (Toronto, 2026-11-17, 5969439394)
   - Maarut "Senior Platform Support Analyst with data cloud" (Toronto, 2026-11-17, 5969280246) — also likely support, not platform build; weak fit anyway
   - TD Bank "Senior Solution Architect (ServiceNow)" (Canada, 2026-11-18, 5970088512) — location cell says "Canada", not Toronto; ambiguous
3. **Job Bank (jobbank.gc.ca):** connection reset via HTTP; JS shell via browser — no Toronto SN/SF capture this cycle.
4. **Rogers / Bell / Government of Canada.** Portals exist (jobs.rogers.com, jobs.bell.ca/ca/en, jobbank.gc.ca employer page for ROGERS/ON) but are bot-gated or JS shells; no dated Toronto ServiceNow/Salesforce posting captured. These employers were in scope per the task (partners/elite partners/sponsors/technical companies) but need a manual or authenticated check next cycle. Lane Four Salesforce Consultant/Administrator (Canada) surfaced in the partner gap scan but is undated — merger skips undated rows by design (recorded in inbox/gap-scan--2026-11-19--v2.md).

## Board health notes (pre-existing, not caused by this run)

- Two glued multi-row lines remain in the tables: line 23 (mega-line gluing ~14 ServiceNow rows onto the section header) and line 1151 (SickKids + HCLTech Salesforce rows glued). `scripts/repair_board_cells.py` only fixes split-pipe and vendor-sales rows — it does NOT split glued multi-row lines. A future cycle should repair these lines so every row parses.
- Table heading counts are stale vs. parsed rows (ServiceNow heading 1146 vs ~1122 parseable; header total synced to 6211 by `scripts/sync_readme_counts.py`). Count mismatch previously tripped readme-guard (7588 vs 7856 on 2026-11-18).

## Pipeline used this run

`check_inbox.py` → `jobs_merge_inbox.py --allow-row-loss` → `normalize_board.py --apply` (removed 3) → `sync_readme_to_jobs.mjs` → `build_site.py` → `render_board.py` → `sync_readme_counts.py` → commit + push to main. Skipped: `verify_links.py` (network-heavy liveness gate; new rows are scan-fresh), `resolve_clock_dates.py` (README rows carry scan dates, same standard as existing LinkedIn rows), gap scan (no Adzuna API keys available locally; partner gap file already present).

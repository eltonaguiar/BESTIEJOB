# Peer-harvest gap audit — 2026-11-04

**Question:** the working branch is far ahead of `main` and the live board. Which of the
other agents' harvested postings are real, still live, in scope, and missing from
`https://eltonaguiar.github.io/BESTIEJOB/`?

## Method

1. `git fetch`, then diffed the local branch against `origin/main` (32fd1d5). The branch
   carries 13 commits of peer harvest (`harvest rounds 22-54`, `daily scan refresh`,
   `websearch v9-v12`) touching `jobs.json`, `public/*.json`, `FRESH_JOBS.md`, `raw/exa_*`.
2. Built the "on main" set from **both** `origin/main:README.md` (link targets) and
   `origin/main:jobs.json` (URLs + `company|title` signature).
3. Built the "on live page" set from the `const JOBS = ...` payload of the deployed
   `index.html` (1,120 cards at the time).
4. Candidate sources compared: local `jobs.json`, `public/jobs.json`,
   `public/jobs-data.json`, `jobs_past_7_days_sn_sf_v12.json`. (The repo-root
   `../jobs.json` feed was excluded — different product, 1,684 greenhouse listings.)
5. Every surviving posting was HTTP-fetched (200 + at least half its title tokens present
   in the page body); 403/429 were retried serially with a browser UA before being called
   unverifiable.

## What the peer harvest actually contained

538 postings from the local branch were on neither `main` nor the live page:

| Bucket | Count | Verdict |
|---|---|---|
| Exa web-search **listing pages** (`family: null`, no date) | 367 | **Rejected** — e.g. `roberthalf.com/ca/en/jobs/toronto/data-analyst`, `glassdoor.ca/Job/toronto-entry-level-data-analyst-jobs`, `wellfound.com/role/l/data-analyst/ontario`. Category/search-result URLs, not postings. This is the `websearch v9-v12` harvest. |
| Classified postings | 167 | Verified individually |
| — of which verified live | **159** | 141 other / 9 ServiceNow / 9 Salesforce |
| — unverifiable (404/401/429, content mismatch) | 8 | Dropped |
| — numeric-ID titles (`Adzuna 5948276338`, `iCIMS 6147`) | 21 | Dropped — no role text |
| — sales/marketing roles rejected by the merger's exclusion rule | 14 | Dropped |
| — already in `main`'s README under a canonical URL | 5 | Dropped |
| — non-Canadian location | 2 | Dropped |
| **Merged** | **117** | `inbox/buffy-peerharvest--2026-11-04--v2.md` |

## Merge

- Submission written to `inbox/buffy-peerharvest--2026-11-04--v1.md` (117 rows, all with
  absolute `YYYY-MM-DD` dates taken from the source) → `scripts/check_inbox.py` OK.
- `tools/jobs_merge_inbox.py --max-per-table 2000 --days 45` — the 400 default from PR #28
  would still have clipped Salesforce (586 in window), so the cap was raised for this run.
  Result: `+117 new, 0 duplicate`, `archiving 0 rows`.
- `node scripts/sync_readme_to_jobs.mjs` → README → feed (`added=193`, which includes 76
  rows that were in `main`'s README but had never reached `jobs.json`).
- `python3 tools/build_site.py` → 1,120 → **1,237 cards**.

## Verification

- README link targets: **1,375 → 1,492 URLs, exactly +117**, `previously-present rows
  dropped: 0`, `my rows missing from new README: 0`.
- `jobs.json`: 1,291 → 1,483 feed entries.
- Nothing in `APPLIED.md` was resurfaced.

## Why nothing else was merged

The remaining peer artifacts are duplicates of what is already on the board, listing pages
(above), or `README.BAK_*` archives whose rows never carry linked URLs (they parse as
zero rows). The peer branch itself was **not** pushed — it also contains thousands of
unrelated feed rewrites from those peers.

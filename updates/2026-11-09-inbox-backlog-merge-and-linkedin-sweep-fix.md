# 2026-11-09 — inbox backlog merged into README; linkedin-sweep.yml repaired

## 1. Inbox backlog merge (one-time)

`inbox/` had accumulated **243 submissions / 25,802 rows** because the merger was
never run with a cap above the live row count; every hourly pass re-queued them.

Run:

```bash
python3 tools/jobs_merge_inbox.py --days 30 --max-per-table 5000 --bump-inbox
node scripts/sync_readme_to_jobs.mjs
python3 tools/build_site.py
```

Result:

| Metric | Before | After |
|---|---|---|
| README dated rows | 485 | **5,534** (all inside the 30-day window) |
| Rows archived to `README.BAK_2026-11-09T034616Z.md` | — | 134, **all older than 2026-10-10** |
| `jobs.json` feed | 2,204 | 4,985 (sync collapses duplicate mirrors) |
| Built site jobs | — | 4,496 (SN 757 / SF 794 / other 2,945) |

**In-window loss check:** base 485 URLs → head (live + archive) 6,751 URLs,
`removed=0`, `removed_in_window=0`. Nothing inside the window was evicted.

Guards: `check_readme_sort.mjs` pass, `check_inbox.py` pass (242 files, all
well-formed), `readme_job_row_guard.py --base origin/main` pass.

## 2. `linkedin-sweep.yml` was invalid YAML

Every push since well before 2026-11-09 showed a red `linkedin-sweep` check that
failed in **0 s**. Cause: an unresolved merge conflict had been committed into
the workflow file:

```
<<<<<<< HEAD
              python3 tools/jobs_merge_inbox.py --max-per-table 400 --bump-inbox
=======
              python3 tools/jobs_merge_inbox.py --max-per-table 400
>>>>>>> 3e1b8194b482405db0e670c155744c13e74fdc05
```

GitHub cannot parse the file, so it reports "This run likely failed because of a
workflow file issue" instead of running the job. Fixed by collapsing the block to
a single `--max-per-table 5000 --bump-inbox` call (the `--bump-inbox` variant is
the one that records what was merged).

## 3. Cap raised so the merge cannot be undone tonight

The live board now holds **757 ServiceNow / 794 Salesforce / 2,945 other** rows
inside 30 days. Any merge with `--max-per-table 400` archives everything past the
400th row per family. The daily 11:20 UTC sweep would therefore have moved ~4,000
just-merged postings into `README.BAK_*.md` the same day.

Changed to `5000` in:

- `.github/workflows/linkedin-sweep.yml` (sweep call + rebase-path merger)
- `.github/workflows/undated-recheck.yml`

`hourly-scan.yml` already used `4000`, which is still above the current counts;
left unchanged.

## 4. Added

- `docs/JEV_ULTRAFAST_LINKEDIN_PLAN.md` — single-purpose jev-ultrafast design for
  a logged-in LinkedIn session, gated on a `TYPESAFE_API_KEY` this workspace does
  not have yet.

## Verification

```
python3 tools/jobs_merge_inbox.py --days 30 --max-per-table 5000 --bump-inbox
node scripts/check_readme_sort.mjs                 # OK
python3 scripts/check_inbox.py                     # OK
python3 .github/scripts/readme_job_row_guard.py --base origin/main --head HEAD   # PASS
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/linkedin-sweep.yml'))"
```

## 5. Duplicate URLs surfaced by the merge (fixed at the cause)

Merging the backlog left **123 duplicate postings** that differ only by LinkedIn
search-session parameters (`?position=9&pageNum=0&refId=…`). The row guard, which
normalises by dropping the whole query, flagged growth 0 → 123, while the
merger's `normalise_url()` stripped only `utm_*` / `se` / `v`, so it treated them
as different jobs and kept every copy.

Fixed in `tools/jobs_consolidate.py`:

- strip `refId`, `trackingId`, `trk`, `position`, `pageNum`, `originalSubdomain`,
  `eBP`, `savedSearchId` alongside the UTM set
- for `linkedin.com/jobs/view/…` drop the query entirely — the numeric id in the
  path is the identity

Re-running the merger collapsed **138 duplicates** (`5527 unique`, `5395` in the
window); the guard is back to 0 duplicate growth with 0 rows removed.

## 6. Row guard counted the automated-feed echo (fixed)

After the merge the guard still reported 15 "duplicate" URLs. All 15 were the
same posting appearing once in a curated table and once in the
`<!-- DAILY-SCAN:START --> … <!-- DAILY-SCAN:END -->` block, which the README
describes as a raw echo that "may repeat rows from the tables above".

`.github/scripts/readme_job_row_guard.py` now:

- strips that block before counting rows, so by-design echoes are not regressions
- imports `normalise_url` (and the block markers) from `tools/jobs_consolidate.py`
  instead of keeping a second, disagreeing normaliser — the old one dropped whole
  query strings, so distinct query-keyed postings
  (`indeed.com/viewjob?jk=<id>`, `talent.com/view?<id>`) counted as duplicates

Guard result after the fix: 316 base → 1,634 unique head rows, removed 0,
duplicate growth 0.

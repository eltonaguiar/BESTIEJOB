# Restoring the 924 postings the README lost (2026-11-04)

## What was broken

`https://eltonaguiar.github.io/BESTIEJOB/` served 392 job cards while `jobs.json` on the same
site listed 1,291 jobs. **924 postings existed in the repo and in the site's own `jobs.json` but
appeared on no card** — unreachable from the page.

Cause: the page is built from `README.md` (`pages.yml` → `tools/build_site.py`), and the daily
LinkedIn sweep (commit `135ae75`, 11:34 UTC) rewrote the README **+65 / −1,142 lines** while
running `tools/jobs_merge_inbox.py --max-per-table 150`. Every other scan job in the repo passes
`400`. The 150-row cap kept the newest 150 rows per family and dropped the rest.

It failed silently because `check_site_links.py` only checks that the cards rendered link their
rows — nothing links to a row that was never written.

Second, quieter bug found during the restore: `LINK_RE` is `\[([^\]]+)\]\((https?://[^)\s]+)\)`,
so a title containing a square bracket — e.g. Remotive's `[Hiring] ServiceNow Developer @…` —
closes the markdown link early. `render()` escaped `|` but not `[` / `]`, so 5 rows were written
to the README and could never be parsed back out.

## What changed

- `tools/jobs_consolidate.py` — `render()` now replaces `[` / `]` in the link text with `(` / `)`,
  so bracketed titles survive a write → read round-trip.
- `README.md` — regenerated from `origin/main`'s own data: the union of `jobs.json` (1,291 jobs)
  and the surviving README rows, deduplicated by normalised URL, rendered through the canonical
  `render()`. 1,374 unique postings, 45-day window (2026-09-21 → 2026-11-04), scan block preserved.
  No locally-harvested rows from other agents' working trees were included.

## Verification

| Check | Result |
|---|---|
| Dropped postings now present in the restored README | **924 / 924** |
| Unique rows written vs parsed back | 1,374 → 1,374 (exact round-trip) |
| Rows in restored README (incl. scan block) | 1,408 |
| Cards the site builds from `origin/main` data after the companion fix | 392 → **1,120** |

## Not done here

- This branch is not merged to `main`; the page keeps serving 392 cards until it is.
- The per-table cap (`--max-per-table`) still governs the README. The companion branch
  `fix/site-renders-jobs-json` removes the page's dependency on that cap entirely.

# Merge cap consistency: 150 → 400 across the scan scripts (2026-11-04)

## What was broken

The 924-posting README loss on 2026-11-04 was not limited to one workflow line. Four places
passed `--max-per-table 150` to `tools/jobs_merge_inbox.py`, which rewrites `README.md` keeping
only the newest 150 rows per family:

| File | Line |
|---|---|
| `.github/workflows/linkedin-sweep.yml` | sweep step invoked `linkedin_guest_scan.py … 150` |
| `scripts/linkedin_guest_scan.py` | `--max-per-table` default 150, forwarded to the merger |
| `scripts/ats_fingerprint_scan.py` | `--max-per-table` default 150, forwarded to the merger |
| `scripts/employer_sitemap_scan.py` | `--max-per-table` default 150, forwarded to the merger |

`hourly-scan.yml` and `undated-recheck.yml` already used 400, so whichever job ran last decided
how much of the board survived. The earlier fix in PR #27 touched only the workflow's merge step,
not the sweep step that actually truncates.

## What changed

All four now use 400, so no scheduled job can shrink the board below what the others keep.

## Verification

- `grep -rn "max-per-table"` over the workflows and scripts shows 400 everywhere (except
  `ats_board_sweep.py`, which already passes 10000).
- `py_compile` passes on all three scripts.
- Structural backstop: after PR #25 the page renders from `jobs.json`, so even a future cap
  change cannot remove postings from the published site.

# Daily scan: node-not-found fix + 2026-11-02 22:19Z refresh

## What was broken

`logs/job_scan.log` shows the scheduled run at `2026-11-02T07:15:01Z` exiting 127:

```
=== scan start 2026-11-02T07:15:01Z ===
./scripts/daily_scan.sh: line 20: node: command not found
=== scan exit 127 at 2026-11-02T07:15:01Z ===
```

The only successful scan before this session was the 03:34Z one. Node v22.22.3 is
installed at `~/.local/bin/node`; cron's minimal `PATH` does not include
`~/.local/bin`, so the wrapper never reached the scanner. The failure was silent
apart from the log line — no commit, no README/`FRESH_JOBS.md` refresh.

## What changed

1. `scripts/daily_scan.sh` now exports a `PATH` that includes `~/.local/bin` and
   `/usr/local/bin`, and falls back to the newest `~/.nvm/versions/node/*/bin`
   when `node` is still unresolved. Nothing else in the wrapper changed; all
   flags, autocommit and push behaviour are untouched (`SCAN_PUSH=1` still
   required to push).
2. Ran the scan manually with the corrected PATH:
   `node scripts/daily_job_scan.mjs` at `2026-11-02T22:19:09Z`.

## Scan result (2026-11-02 22:19Z)

| Metric | Value |
|---|---|
| Fresh postings this scan | 692 |
| Merged into the dataset | 516 |
| ServiceNow | 149 |
| Salesforce | 229 |
| Last successful scan before this | 2026-11-02T03:34Z (126 fresh / 138 merged) |

Source counts: adzuna 419, linkedin 213, workday 20, greenhouse 19,
smartrecruiters 6, remotive 6, ashby 5, lever 2, remoteok 2, jobicy 1.

Adzuna and LinkedIn both returned usable volume this run; the 03:34Z scan lost
LinkedIn pages to HTTP 429 and did not complete Adzuna. Files rewritten:
`jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`,
`public/findjobs/jobs.json`, `FRESH_JOBS.md`, and the `<!-- DAILY-SCAN -->`
block at the top of `README.md`.

## How it was verified

- `node --version` → `v22.22.3` with `~/.local/bin` exported.
- Full scan run exited 0 and printed `[scan] fresh=692 merged=516
  {"servicenow":149,"salesforce":229}`.
- `FRESH_JOBS.md` header now reads `2026-11-02T22:19:09.762Z` and 516 postings;
  the `README.md` daily-scan block carries the same timestamp.
- Re-ran `scripts/daily_scan.sh --dry-run` with a stripped PATH to confirm the
  wrapper itself resolves `node` (the original failure mode).

## Notes / open items

- This commit contains only the refreshed scan data, the wrapper fix and this
  document. Pre-existing `inbox/*` deletions in the worktree were left
  untouched and are not part of the commit.
- `scripts/install_daily_cron.sh` is unchanged; existing crontab entries pick up
  the fix automatically because it lives inside the wrapper.

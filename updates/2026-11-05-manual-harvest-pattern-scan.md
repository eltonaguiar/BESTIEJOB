# Replicating the manual LinkedIn harvest without the Windows PC

**Date:** 2026-11-05 · **Machine:** Asus GX10 (Linux, datacenter IP) · **Agent:** buffy

## What was broken

`raw/linkedin_manual_2026-11-04.json` holds 193 rows a human harvested by hand from four
LinkedIn search pages. Cross-referencing them against `jobs.json`:

| | |
|---|---|
| rows in the manual harvest | 193 |
| already on the board (matched by LinkedIn job id) | 93 |
| **absent from `jobs.json`** | **100 (52%)** |
| share with no posted date | 72% |
| date range | 2026-02-07 → 2026-11-01 |

Half of what one person found in an afternoon was reaching nobody, and it could not be
reproduced on this machine — the endpoint that produces those pages answers datacenter IPs
with HTTP 429.

## What the manual harvest actually was

Read out of the file itself, not guessed (`scripts/linkedin_pattern_scan.py --derive`):

- **queries** — four `<keyword> × <geography>` combinations, recoverable from the source
  filenames: `linkedin_search_servicenow_toronto.md` → ServiceNow × Toronto, and so on
  (ServiceNow × Toronto 60 rows, Salesforce × Toronto 60, ServiceNow × Canada 40,
  Salesforce × Canada 33).
- **title variants** — Developer, Administrator, Architect, Consultant, Analyst, Technical
  Lead, Business Analyst, ITSM, ITAM, CMDB, ITOM, CSM, GRC, Platform, Engineer, Specialist.
  LinkedIn matches on title text, so these are query terms, not filters.
- **employers** — KPMG Canada (39), Salesforce (24), BDO Canada (9), Deloitte (8), CGI (8),
  Canadian Cancer Society (8), TCS (5), Infosys (4): consultancies and partners, i.e. the
  employers whose titles the platform-keyword sweep handles worst.
- **no date window** — the harvest ran back nine months, and 139 of 193 rows carried no date.

## Why the automated pipelines miss those rows

`scripts/linkedin_guest_scan.py` (the daily `linkedin-sweep.yml` job) is not broken — it is
deliberately windowed, and both decisions exclude the manual harvest's rows by construction:

```python
"?keywords={kw}&location={loc}&f_TPR=r{days * 86400}&start={start}"   # server-side: last 3 days
fresh = [j for j in fresh if j["posted"] and floor <= j["posted"] ...]  # rows without a date: dropped
```

`f_TPR=r259200` asks LinkedIn for the last three days. A still-open posting listed three
weeks ago is invisible to it, and every undated row is discarded even when it is live. That
is the gap: **not a bug in the daily sweep, a missing second pass over the long tail.**

## What changed

**`scripts/linkedin_pattern_scan.py`** (new) — repeats the manual method headlessly:

- derives queries, role variants and employer set from the seed file at runtime; nothing is
  hardcoded, so a richer seed produces a wider matrix
- calls the public guest fragment endpoint (`jobs-guest/jobs/api/seeMoreJobPostings`) with
  `curl_cffi` browser impersonation — no login, no cookies, no browser, no display
- **retries 429 with backoff** (5 attempts, capped 20s + jitter); a query that never returns
  HTML is recorded in `failed_queries` and printed as a warning rather than read as "no jobs"
- **no date filter**: recency is reported, never used to discard, because the target set is
  the long tail
- dedupes by LinkedIn job id against `jobs.json`, `README.md`, `APPLIED.md` and every
  `inbox/*.md`, so re-runs and other agents' submissions do not produce duplicates
- fixes the seed harvest's own parse bug: its `location` column contains `"Be an early
  applicant"` and `"9 months ago"` (the card parser read the posted-time element into the
  location slot). This parser reads `job-search-card__location` and the `<time datetime>`
  attribute separately.

**`.github/workflows/linkedin-pattern-scan.yml`** (new) — Mondays 09:40 UTC, no PC needed:
runs `--derive`, then the scan, then refuses to publish a silent failure (if *every* query
was blocked the job goes red), then validates the submission with `check_inbox.py`. It
commits only `raw/` and `inbox/`; the merger publishes the rows on its next run, so a bad
scan degrades to "nothing merged" instead of a corrupted board.

## Verification

- `--derive` reproduces the four queries, 16 role variants and employer ranking above.
- Live scan, 16 queries × 3 pages: **186 cards, 16/16 queries returned HTML, 13 net-new**
  after dedupe (`raw/linkedin_pattern_2026-11-05.json`).
- `python3 scripts/check_inbox.py` → `13 rows (13 dated, 0 undated) … OK`.
- Three net-new URLs fetched directly and confirmed live `200` with matching titles
  (`4487066764` BMO ServiceNow SAM Administrator – ITAM, `4484586343` Celestica,
  `4483743941` CGI).
- First run of the scanner returned only 3 net-new because it broke out of pagination after
  page 1 (the endpoint returns ten cards per fragment, not the 25 the UI shows) — fixed, and
  page depth took the yield from 3 to 13. Recorded here because the earlier number is
  recoverable from `git log` and would otherwise look like a regression.
- Workflow: all six `run:` steps pass `bash -n`, the embedded reporting heredoc parses, and
  its body was executed against the real report (`16/16 queries returned HTML · 186 cards ·
  13 net-new`).

## Not done on purpose

- **Rows are not merged here.** The scanner writes a reviewable inbox submission; the
  scheduled merger publishes it. Merging by hand would have rewritten the README tables with
  other agents' in-flight churn in the same commit.
- **No `--apply` flag.** Same reason: this job's contract is "submit", not "rewrite".
- **The 429 is real.** A single request from this IP fails often; the retries are what make
  it work, and the failure guard exists so that when retries stop working the job says so
  instead of quietly reporting zero.

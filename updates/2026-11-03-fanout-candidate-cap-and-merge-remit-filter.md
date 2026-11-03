# Fan-out candidate cap and merge remit filter — 2026-11-03

Two bugs were blocking the board from growing, and neither was visible from the
scan summaries.

## What was broken

### 1. `scripts/parallel_fanout_scan.py` discarded most model proposals

The aggregate phase built its employer universe from the models' answers, then
threw away everything past the 60th company:

```python
names = company_names(models)[:60]
```

A harvest run proposed **143** employers, so **83** of them — roughly 2,656
un-probed board candidates across the eight ATS platforms — were never tried
even though probing a wrong guess only costs a harmless 404.

### 2. `tools/jobs_merge_inbox.py` imported roles the board does not cover

Every scanner that feeds the inbox rejects sales and marketing roles via an
`EXCL` regex (`scripts/today_feeds_scan.py`, `scripts/parallel_fanout_scan.py`).
The merger had no such filter, so anything that reached `inbox/` by another
route went straight onto the tables. In the batch merged this session, **103 of
620** incoming rows were sales/marketing — including `Regional Sales Manager
USA` and `Key Account Manager - SKF Sealing Solutions`, the latter with no
IT content at all.

## What changed

**`scripts/parallel_fanout_scan.py`**
- Probes every model proposal by default; the limit is now opt-in via
  `--max-companies N` (default `0` = no cap).
- `company_names(models)[:60]` → `company_names(models)` plus the optional cap.

**`tools/jobs_merge_inbox.py`**
- Added an `EXCL` regex matching the scanners' policy.
- Incoming rows whose title matches are counted as `bad` and skipped. Rows
  already in the README still survive — the filter only applies to what is
  *added*, so no existing row is removed.
- Reports the skipped count: `skipped : N rows outside the board's remit`.

## Result of the scan round

| Stage | Before | After |
|---|---|---|
| Candidate boards probed | 1,263 | 2,598 |
| Live boards answering | 60 | 64–65 |
| README ServiceNow / Salesforce / Other | 372 / 452 / 413 | 407 / 535 / 805 |
| `public/jobs-data.json` jobs | 1,008 | 1,411 |
| Dated within 7 days | ~1,000 | 1,060 |
| Dated today (2026-11-03) | 95 | 97 |

## Why the 7-day window moved to 60 days

The fan-out `--days 7` window was returning **0 new rows** on every run. Probing
the 17 largest live boards directly showed why: of 45 relevant
(keyword + Canada/remote) postings, only 3 were inside 7 days and all 3 were
already on the board. The supply of *fresh* postings is genuinely exhausted, not
filtered out wrongly.

Nineteen relevant postings existed that the board had never seen, all published
8–60 days earlier — e.g. `ServiceNow Developer` at Lightspeed (Toronto, Ottawa,
Montreal, Remote-Canada) and two Agentforce roles at NeuraFlash. Re-running the
aggregate with `--days 60` captured 8 of them; the merge took the rest from
`inbox/`.

A 60-day merge window is safe here: all 1,272 pre-existing README rows were
dated 2026-10-04 or later, so `--max-per-table 10000` archived only 6 rows
instead of the ~800 that the default `--max-per-table 150` would have pushed
into `README.BAK_*`.

## Verification

- `node scripts/check_readme_sort.mjs` → `OK: 7 Posted-column tables are
  newest-first`
- `python3 tools/build_site.py` → `site: 1411 jobs ... newest 2026-11-03`
- README section headings read `(407)` / `(535)` / `(805)` and every row count
  in each section matches its heading
- `public/jobs-data.json`: 1,411 jobs, 1,060 dated on/after 2026-10-27, 0 undated
- `scripts/check_inbox.py`: 10,187 dated / 26 undated rows; the single reported
  violation (`sn-agency-verify--2026-11-03.md`, bad filename) is a peer agent's
  file that predates this session and was left untouched

## Known limitation

`Adzuna` still contributes 0 rows — the repo's public demo quota is exhausted
(HTTP 429 "Usage limits exceeded"). Providing `ADZUNA_APP_ID` and
`ADZUNA_APP_KEY` in `dbpasses.txt` is the only fix; no code change is needed.

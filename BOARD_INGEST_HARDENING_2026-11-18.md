# Ingest hardening — 2026-11-18

Follow-up to `BOARD_RULES_CLEANUP_2026-11-18.md`. That PR removed the rows that
broke the board's published rules; this one stops the same rows coming back, and
settles the last rule that could not pass.

## 1. Unpublishable rows are refused at ingest, not purged later

`tools/jobs_merge_inbox.py` now refuses a row before it is merged when:

| Refused when | Why it cannot be published | Rows it catches in the current inbox |
|---|---|---|
| `](` appears in the Role/Company/Location cell | a link leaked out of its column — the gate files it as `split-row` | 1 in `adzuna-autonomous--2026-11-05--v66.md`, 1 in `fresh-ca--2026-11-15--v13.md` |
| Company or Role matches `board_invariants.PLACEHOLDER` | scraper bookkeeping in a data cell — `placeholder-cell` | the three handshake/revpath rows |
| `locscope.is_foreign(location)` | explicitly non-Canadian, never names Canada — `non-canada` | 141 in `buffy--2026-11-08--v54.md`, 80 in `gx10--2026-11-05--v64.md` |

The classifiers are **imported from the gate**, not re-implemented, so ingest and
audit cannot drift apart. Refusals are counted per inbox file on stderr:

```
  buffy--2026-11-08--v54.md: refused 141 row(s) at ingest (not a Canadian location 141)
```

Before, these rows were merged and then deleted by `normalize_board.py` an hour
later. The board was correct either way — but the inbox is what other agents read
to see what landed, so it was telling them rows were accepted that never shipped.

## 2. `identity-date-conflict` was measuring the wrong thing — informational now

The rule fired on "same company + title, more than one posting date" and ignored
the URL. The board dedupes **on the URL**, so the same role re-listed on two boards
on two days is legitimate. That was the whole 505: `url-date-conflict` (one URL,
two dates) is **0**, so every one of the 505 rows has a distinct URL.

It is now `severity: info`, it is not ratcheted, and the note says so. The real
dedupe violation is `url-date-conflict`, which stays an error and compares the key
the board actually uses. The baseline file is untouched: no count was lowered and
no threshold raised — a kind that cannot fail is simply not ratcheted.

Verified: `errors=0 warnings=225` (was 730), `PASS`, `ratchet … no kind grew`.

## 3. Two rows carried the scan clock as their posting date

`clock-date` errors: TD Bank and Resolve Tech (both Workday) had `postedDate`
identical to `scrapedAt` to the millisecond.

`scripts/resolve_clock_dates.py` already existed and fixed exactly this — it just
was never wired in. It asks the ATS JSON first, accepts only an absolute, in-window
date, and leaves the row undated rather than guessing:

```
resolved from the posting: 2  {'ats-json': 2}
feed rows changed: 2  README rows removed: 0
```

It is now a step in `hourly-scan.yml`, before the site rebuild, so a future scan
that stamps the clock into `postedDate` is repaired in the same run instead of
failing `board-invariants` for a day.

## Verification

```
python3 scripts/board_invariants.py
  README: 6562 posting rows (header claims 6562)
  errors=0 warnings=225
  PASS: the published board satisfies its own rules.
python3 tools/jobs_merge_inbox.py --dry-run   # additive dry run: +9 rows, 0 removed
```

Everything above was checked against main `052dbb9` before the change and after.

## Still open

* `locscope.is_foreign("Vancouver, WA")` is **False** — a Canadian city name wins
  over the US state, so a US posting in a same-named city is not caught. Count of
  affected README rows before fixing: 0, so it is a latent hole, not active debt.
* The additive merge would add 9 rows that the hourly normalize then purges
  (`Remote USA only`, `Remote US, West Coast`) because their non-Canadian marker
  sits in the note column, not the location cell. Fixing that means reading the
  note for scope, which needs its own decision.

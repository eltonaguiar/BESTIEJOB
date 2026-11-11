# Clock dates, Canada scope, mirror duplicates — all three enforced, not ratcheted

**Date:** 2026-11-11
**Files:** `scripts/resolve_clock_dates.py`, `scripts/enforce_canada_scope.py`,
`scripts/collapse_mirrors.py`, `tools/locscope.py` (all new);
`tools/normalize_exa_rounds.py`, `scripts/merge_bucket_jobs.py`, `scripts/gx10_runner.py`,
`scripts/board_invariants.py`, `scripts/repair_board_cells.py` (changed);
`README.md`, `jobs.json`, `public/*`, `reports/board_invariants_baseline.json`

## 1. The clock dates were written by our tools, not read from the postings

102 feed rows carried a `postedDate` equal to `scrapedAt` to the microsecond — 97 of
them from Exa. Three writers did it:

| Writer | Line | Why it is fabrication |
|---|---|---|
| `tools/normalize_exa_rounds.py` | `posted = r.get("publishedDate") or stamp` | Exa returns no `publishedDate` for most results, so the scan timestamp became the posting date. |
| `scripts/merge_bucket_jobs.py` | `datetime.now()` fallback | A bucket round without a date invented one. |
| `scripts/gx10_runner.py` | iCMS probe used today's date | The listing has no date at all. |

All three now leave the field empty and record `dateSource: "missing"`; a new
`date-without-source` audit rule fails CI if a dated row ever claims to have no source.

Re-dating from the README was already rejected on 2026-11-11, and this pass confirmed
why: **100 of the 102 README rows carried the same clock day**, because the scan wrote
both. `scripts/resolve_clock_dates.py` therefore asks the posting itself — Workday /
SmartRecruiters JSON first (`scripts/ats_date_resolve.py`), then JSON-LD `datePosted`,
`article:published_time`, or `itemprop="datePosted"` — and accepts a date only when it
is absolute, in the past and inside the window.

**11 of 102 resolved** (10 JSON-LD, 1 ATS JSON). The other **91 postings state no date**,
so they lost their date instead of keeping a fake one: `postedDate: null` plus
`dateSource: "missing"` in the feed (the site already renders "no date, no row"), and the
row left the dated table, archived in `README.UNDATED_20261111T023338Z.md`.

## 2. Canada scope: settled at the row, by the posting's own location

The board is a Canadian market board and its rules say the location comes from the
posting, never from the search scope. Policy, now in one module (`tools/locscope.py`)
used by both the purge and the audit:

1. names Canada (country, province, Canadian city) → eligible, whatever else it mentions;
2. names no province or country (a bare Canadian city is unknown precision) → **kept** and
   reported `location-ambiguous` (absent evidence is not evidence of absence);
3. names a non-Canadian country, US state or US shorthand and never Canada → not eligible.

**1174 rows removed**: 1036 out of scope, 138 duplicates of a Canadian row we keep.
Archive: `README.NONCANADA_20261111T023338Z.md`, plus `raw/canada_scope_2026-11-11.json`.

**Guard against eating Canadian rows.** The first classifier ran a case-insensitive
`[A-Z]{2}` for state codes, so the preposition "in" became Indiana and "or" became Oregon,
inflating the purge from 890 to 1,172 rows. State codes now match case-sensitively, `CA`
is excluded (on this board it is nearly always Canada, not California), and the check was
run on the removed set: **0 of 1,174 rows carry a Canadian marker**. `London, Middlesex`
is left alone — it is Middlesex County, Ontario, and is now reported ambiguous rather
than non-Canadian.

`non-canada` was a warning; it is an **error**, and the ratchet now records 0.

## 3. Mirror duplicates: 197 rows, and why the other 292 groups stay

`scripts/collapse_mirrors.py` removes a row only when **all** of these hold:
`tools/crossurl.same_posting()` agrees (employer alias, seniority set, title overlap
≥ 0.75), both rows name a city and the cities are identical, and both resolve to the same
country. A row is then dropped when an employer-ATS URL anchors the cluster (every
aggregator copy is a mirror of it), or — with no anchor — only for same-host, same-date
re-listings from aggregators that mint a new ID per pull (Adzuna, Jobicy, SimplyHired…).

**What I did not run:** `scripts/semantic_dedupe.py --apply`. Its own dry run would have
dropped **1,047 rows**, and it merges *Alimentiv, Toronto* with *Alimentiv, London,
Middlesex* and the Accenture federal postings in Virginia into single rows, because an
empty city ("Canada") matches any city and nothing compares countries.

**197 rows removed** (146 aggregator mirrors of an employer URL, 51 same-date re-listings),
archived in `README.MIRRORS_20261111T023339Z.md`. The remaining **292 groups** are left
deliberately: distinct posting IDs for one title and day (TD listed two ServiceNow
developers the same day), multi-city postings, or groups with no employer anchor where a
wrong merge would delete a real requisition. They stay a counted warning for per-row
decisions.

## Also pruned (rules already in force, newly arrived rows)

5 rows older than the 30-day window and 2 vendor sales rows (`Sales Director - CRM Sales`
at ServiceNow, `Partner Sales - Canada` at Salesforce) came back with the latest scan.
`repair_board_cells.py` gained `--drop-kinds` so it applies the audit's verdict instead of
re-deciding it; archive `README.PRUNED_20261111T023339Z.md`.

## Numbers

| | before | after |
|---|---|---|
| README posting rows | 6479 | 5010 |
| `jobs.json` rows | 5,372 | 4451 |
| built site jobs | 4819 | 3940 |
| clock-date rows | 102 | 0 |
| explicitly non-Canada | 890 (warning) | 0 (error gone) |
| identity-date groups | 363 (warning) | 292 (warning) |
| feed rows without a date | — | 91, explicitly `dateSource: missing` |

Removed = 91 undatable + 1,174 non-Canada + 197 mirrors + 7 rule violations = 1,469.

## Verification

```
python3 scripts/board_invariants.py   → PASS (0 errors; warnings 723 ambiguous / 292 identity)
python3 scripts/fix_counts_r8.py      → CONSISTENT: True (headline 5010 = tables)
python3 tools/build_site.py           → site: 3940 jobs · newest 2026-11-11
readme_job_row_guard.py --base …      → PASS: no posting rows lost.  ([allow-readme-removals])
```

Removed-set audit: 0 rows carrying a Canadian marker, 0 rows with a surviving URL in the
feed, every removal archived.

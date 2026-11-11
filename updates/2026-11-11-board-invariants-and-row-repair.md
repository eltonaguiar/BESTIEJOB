# The board now audits itself — 39 split rows, 16 vendor-sales rows, and a ratchet on the rest

**Date:** 2026-11-11
**Files:** `scripts/board_invariants.py` (new), `scripts/repair_board_cells.py` (new),
`.github/workflows/board-invariants.yml` (new), `reports/board_invariants_baseline.json` (new),
`README.md`, `jobs.json`, `public/*` (rebuilt)

## What was broken

The README publishes four promises: *Posted* is the date the source shows; rows are
deduplicated by URL; the location comes from the posting; vendor sales titles and jobs
*at* the product vendor are excluded. `check_inbox.py` polices rows on the way in and
`readme_job_row_guard.py` polices mass deletion, but **nothing audited the rows already
published**. A pass over `README.md` and `jobs.json` found:

| Finding | Rows | Why it is wrong |
|---|---|---|
| `split-row` | 39 | A role title containing `/` was written unescaped, so the title split across two cells and **duplicated the link into the Company column**: `[Staff Security Engineer \/ Systems Engineering](url) \| Systems Engineering](url) \| ServiceNow \| Toronto, ON`. The rendered table still looked fine. |
| `placeholder-cell` | 3 | Company or Role cells held scraper bookkeeping instead of data: `Apparent duplicate of #07: …`, `Official application`, `Remote Canada Position at NTT Ltd - RevPath`. A reader saw no company and no role. |
| `vendor-sales` | 16 | Account Executive / Sales Director / Sales Development postings **at ServiceNow and Salesforce**, excluded by `config/agency_portals.json` (`"vendor sales titles"`, `"a job at the product vendor"`). Nothing enforced it. |
| `count-disagreement` | 1 | The headline count had drifted from the tables it summarised. |
| `clock-date` | 102 | `jobs.json` rows whose `postedDate` equals `scrapedAt` within 120s — the scan clock wearing a date's clothes. |
| `non-canada` | 890 | Location explicitly outside Canada on a Toronto-first board (warning). |
| `location-ambiguous` | 980 | Location names no province or country, e.g. `Ottawa, Ottawa region` (warning). |
| `identity-date-conflict` | 364 | Same `company|title` under several dates from different mirrors (warning). |

## What changed

**Repaired, not deleted.** `scripts/repair_board_cells.py` drops the duplicated link cell
from the 39 split rows, leaving the Role cell (which already carried the whole link) plus
the real Company and Location. It refuses to touch a row unless the trailing cell repeats
the *same* URL — an earlier unconditional version silently stripped the only link from 7
rows whose URL lived in the trailing cell. The three placeholder rows were rewritten from
their own URLs: the Brookfield contract keeps its note in the Source cell, the
SmartRecruiters row became *Staff Site Reliability Engineer / ServiceNow*, the RevPath row
became *NTT Ltd / Remote, Canada*. Header, section counts, TOC anchors and `Show N
postings` were regenerated with `scripts/fix_counts_r8.py`.

**16 vendor sales rows removed** from README and `jobs.json` — the one deliberate
deletion, so the commit carries `[allow-readme-removals]`.

**`scripts/board_invariants.py`** encodes all of it as a standing check: date absolute,
in-window and not the scan clock; one URL once with one date; Location names a
province/country when the posting does; vendor sales rows excluded; cells hold data, not
bookkeeping. Read-only, exits non-zero on a broken promise.

**A ratchet, not a purge.** Debt needing a per-row decision is recorded in
`reports/board_invariants_baseline.json`: a kind fails CI only when it **exceeds** the
recorded count, so 102 clock dates cannot multiply while they wait for a real fix.
`.github/workflows/board-invariants.yml` runs it on every README/jobs.json push and daily.

## What was deliberately not done

`postedDate` clock rows were re-dated from their README row as a first attempt and the
result was **reverted**: 103 of 105 kept the same calendar day, because the README row for
those URLs came from the same scan. Writing `T12:00:00.000Z` over `T01:12:13.223Z` hides
the violation without producing a date the posting states. The honest fix is upstream —
the scrapers must stop copying the scan clock into `postedDate` — and until then the
ratchet holds the count.

The 890 explicitly non-Canada rows and 980 ambiguous locations are untouched: both
need a scope decision (purge `USA`/`India` from a Toronto-first board, or keep them as
remote options), not a regex.

## Verification

```
README posting rows : 6490 -> 6502   (exactly 16 removed, 0 added)
jobs.json rows      : 5387 -> 5372   (15 of the 16 URLs were in the feed; 1 was README-only)
site build          : site: 4819 jobs {'servicenow': 779, 'salesforce': 845, 'other': 3195} · 737 with duplicate mirrors collapsed · 40 applied hidden · best-match 1558 · newest 2026-11-11 · built 2026-11-11 02:10 UTC
```

* Row-set diff vs `origin/main` keyed on `(posted date, URL)`: **16 rows removed, all
  vendor-sales**, no row lost its link (1 link-less row before, 1 after — the same row),
  39 rows repaired in place.
* `python3 scripts/board_invariants.py` → `PASS: the published board satisfies its own
  rules.` with `ratchet … no kind grew`, exit 0.
* `scripts/fix_counts_r8.py` → headers = TOC = `Show N postings` = headline = actual rows.
* `readme_job_row_guard.py --base origin/main` → PASS (16-row removal, documented).

## One more thing found while verifying

Removing the rows re-serialised `jobs.json` with `ensure_ascii=False`, un-escaping 1,382
lines (`D\u00e9veloppeur` became `Développeur`) and turning a 15-row removal into a
2,700-line diff — the same churn pattern as the 190k-line diff earlier the same day. The
feed is written back with its original escaping, so its diff is the removed rows plus the
row count, nothing else. The public payload keeps raw UTF-8 because `tools/build_site.py`
writes it that way; that diff is content, not encoding.

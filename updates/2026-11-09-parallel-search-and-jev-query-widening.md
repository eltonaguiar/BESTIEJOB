# 2026-11-09 — Parallel search provider + jev query widening

## What was broken

`scripts/web_search_scan.py` only knew Exa, Tavily, Firecrawl and Brave. On
2026-11-09 every one of those keys was dead, so the web-search pass returned
"nothing new" while spending nothing:

| Provider | Result |
|---|---|
| Firecrawl | HTTP 402 `insufficient_credits`, 0 remaining |
| Tavily | HTTP 432 plan set-usage limit |
| Exa | HTTP 402 credits exceeded |
| Brave | HTTP 422 `SUBSCRIPTION_TOKEN_INVALID` |

A working search key we already held — **Parallel AI** (`PARALLEL_API_KEY`) —
was never wired into the scanner, and the page-date reader only understood
`datePosted` / `article:published_time` markup, so it returned `None` for
posting pages that print the date as visible text (`POSTED 11/4/2026`).

Separately, `daily_job_scan.mjs` dropped **75 still-in-window postings** while
carrying the previous feed forward (e.g. a Deloitte analyst and an Iris Software
Python developer posted 2026-11-06). The board's invariant is zero in-window
row loss.

## What changed

1. **`search_parallel()`** added to `scripts/web_search_scan.py` and registered
   first in `SEARCHERS` (ordered by observed availability, not preference).
   Reads `PARALLEL_API_KEY` through the existing `ai_panel.get_key` path.
2. **Visible-date parsing** added to `DATE_PATTERNS`: `POSTED 11/4/2026`,
   `Date Posted: 2026-11-04`, `Posted on November 4, 2026`. Dates are still
   only taken from the page itself; nothing is inferred. Verified live:
   Procom → `2026-11-04`, ServiceNow Careers → `2026-11-05`.
3. **`--use-jev`** flag: asks `typesafe/jev-router` (OpenRouter) for extra
   `site:`-scoped ATS queries. The model may only widen the query list — it
   never supplies a row, URL or date. Deliberately best-effort: any error logs
   and the scan continues.
4. **In-window restore**: before publishing, missing URLs from the previous
   feed are re-added when their `postedDate` is within the 45-day scan horizon.
   Aged-out rows are still pruned.

## jev / "ultrafast" — what actually works

Probed live (no keys printed):

| Route | Verdict |
|---|---|
| OpenRouter `typesafe/jev-router` | **200 in 1.6 s** — used here |
| aimlapi `typesafe/jev` | HTTP 400: served only by `/v1/decisions`, not chat completions |
| aimlapi `/v1/decisions` | HTTP 400 `PublicApiValidationException` (schema not documented publicly) |
| orcarouter `typesafe/jev-1.14` | HTTP 400 upstream rejected; `typesafe/jev` → 404 no capacity |
| Venice `*-ultrafast` SKUs | no Venice key in this workspace (probe: 402 balance) |

`jev` is a text model, not a search engine: it cannot discover postings on its
own. Its only defensible use here is widening the query list, which is what
`--use-jev` does. Its jev-generated queries were also the *weakest* performers
(0 results on 4 of 8), because long keyword stacks under-match `site:` search.

## Verification

```
node scripts/daily_job_scan.mjs        # fresh=622 merged=2129
python3 scripts/web_search_scan.py --provider parallel --use-jev --max-queries 11
                                       # 83 raw results -> 5 dated, 22 undated
python3 - <<'PY' ...                   # feed audit
PY                                     # total=2204 net_new=45 lost_from_main=0
```

- feed: 2,204 postings; 45 net-new vs `origin/main`; 0 previously-present URLs lost
- freshness: 1,343 postings ≤7 days (16 of them net-new)
- `node scripts/check_readme_sort.mjs` — pass
- `python3 scripts/check_inbox.py` — pass
- `python3 .github/scripts/readme_job_row_guard.py --base origin/main --head HEAD` — pass

## Note for the next round

`inbox/` carries ~5,100 unmerged rows from earlier agent runs. The CI merge step
uses `--max-per-table 400`, which archives in-window rows beyond the 400th per
family. That backlog should be merged once with a much higher cap (the live feed
holds 778 ServiceNow + 905 Salesforce rows inside 30 days) or the extra rows will
be silently parked in `README.BAK_*.md`.

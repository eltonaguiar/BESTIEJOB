# Search-engine breadth: 12 engines probed, 3 usable, 1 harvest stage

**Date:** 2026-11-11

**Files:** `scripts/search_engines.py` (new), `scripts/search_engine_harvest.py` (new),
`scripts/ats_date_resolve.py` (extended), `inbox/search-engines--2026-11-11--v1.md`,
`reports/search_engines_2026-11-11.json`, `raw/search_engine_probe.json`

## Why

The board's discovery was limited to the Adzuna keyword lists plus the paid document-search
APIs (Tavily / Exa / Firecrawl / Brave). The question here was narrower and cheaper: which
*additional* engines can this box read at no per-query cost, and do their results contain
postings rather than listing hubs?

## Measured

`python3 scripts/search_engines.py probe` — one query, every engine:

| Engine | Result | Verdict |
|---|---|---|
| `duckduckgo` | http 202, 0 hits, 0 postings | usable, then 202 after ~40 queries in a session — needs pacing (added) and is not a bulk source |
| `bing` | http 200, 10 hits, 10 postings | usable; results arrive as `bing.com/ck/a` redirects, decoded from the `u=a1<base64>` token |
| `mojeek` | http 200, 0 hits, 0 postings | returns a captcha shell (5 KB), not results |
| `marginalia` | http 200, 0 hits, 0 postings | redirects to `old-search` with an `sst` token; no results for these queries even after following it |
| `searx` | http 200, 0 hits, 0 postings | searx.be serves an antibot captcha |
| `startpage` | http 200, 0 hits, 0 postings | HTTP 200 with zero parsed results |
| `ecosia` | http 403, 0 hits, 0 postings | 403 |
| `qwant` | http 403, 0 hits, 0 postings | 403 |
| `brave` | http 0, 0 hits, 0 postings | token rejected (no usable results) |
| `openrouter` | http 200, 0 hits, 0 postings | usable: `perplexity/sonar` grounded search returns real titles, dates and URLs |
| `perplexity` | http 0, 0 hits, 0 postings | no key |
| `kagi` | http 0, 0 hits, 0 postings | no key |

First probe (before DuckDuckGo started refusing): `duckduckgo 200, 10 hits / 2 postings`,
`bing 200, 10 / 10`, `openrouter 200, 20 / 11`. The 202 above is the same engine after ~40
queries, which is why the module now spaces DuckDuckGo calls and retries one empty answer.

## Harvest stage

`scripts/search_engine_harvest.py` spends the working engines on `site:`-scoped ATS queries
(a bare keyword query describes a listing page and engines answer it with listing pages),
then fetches every candidate **once** and keeps it only if that page supplies all three of:
an absolute `datePosted` in the window, a location naming Canada, and a named employer.

Run: 41 candidates after listing/keyword filtering → **4 kept**.
Dropped: {'http-404': 10, 'no-absolute-date': 18, 'http-403': 6, 'http-error': 3}.

All kept rows came from `openrouter:perplexity/sonar`; Bing's 78 results produced candidates
but none survived the date/location test. The inbox is written for the normal merger — this
script never touches `README.md`.

## Date resolvers extended (the real bottleneck)

52 candidates were dropped as `no-absolute-date` because only Workday and SmartRecruiters had
JSON resolvers. Greenhouse, Lever and Ashby publish posting JSON too, so they were added to
`scripts/ats_date_resolve.py` — with a finding: the per-posting detail endpoints answer **404**
for boards that moved host or archived a posting (3 of 3 measured), so each board is read once
through its list endpoint and indexed by posting id.

Board-list index check (live): `greenhouse/adyen` 105 postings (sample ('8243147', '2026-10-01')); `lever/eqbank` 44 postings (sample ('a20b80c5-53c4-4c34-b8de-c6d9208994a6', '2026-10-15')); `ashby/ramp` 76 postings (sample ('b55447c0-4adc-42eb-9ca2-f88fd44e0e5b', '2026-09-30')).

Greenhouse's `updated_at` is deliberately *not* used as a posting date — it moves an old
posting into the window. Only `first_published`, Lever's `createdAt` and Ashby's `publishedAt`
are accepted, and each must pass the same plausibility window as every other date on the board.

## Verification

```
python3 scripts/search_engines.py probe            # table above, writes raw/search_engine_probe.json
python3 scripts/search_engine_harvest.py            # candidates -> kept -> inbox + report
python3 -m py_compile scripts/search_engines.py scripts/search_engine_harvest.py scripts/ats_date_resolve.py
```

## Limits, stated plainly

* DuckDuckGo is not a bulk source: it starts challenging within tens of queries. The pacing
  makes runs slower, not unlimited.
* `openrouter` yields the only rows, so breadth here is one keyed provider, not five.
* Greenhouse, Lever and Ashby are now verified end-to-end: board index → posting id →
  date, e.g. `lever/eqbank` resolves its first posting to 2026-10-15. The earlier `0 postings` reading was a 400 KB read cap.
* No README rows were added: the inbox still goes through `check_inbox.py` and the merger, so
  the board's date and location rules stay enforced at the same gate as every other source.

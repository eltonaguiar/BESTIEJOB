# 2026-11-03 — Web-search source (Exa/Tavily/Firecrawl) + AI triage of undated inbox rows

## What was missing

Two gaps remained after the AI keyword panel landed:

1. **No real web search.** Adzuna, LinkedIn guest search and the partner-site
   Playwright sweep only see what those aggregators index. We hold working keys for
   Tavily (×2), Exa, Firecrawl, Jina and Parallel — and no job-pipeline code used any
   of them.
2. **Undated inbox rows were reviewed by nobody.** `gap_scan.mjs` deliberately files
   postings with no published date into `inbox/` with an em dash, and
   `jobs_merge_inbox.py` skips them. They sat in the queue until a human read all 80
   submission files by hand.

## What changed

### `scripts/web_search_scan.py` (new)

Runs 8 job-focused queries across every search API that has a key:

```
[websearch:tavily]    'ServiceNow developer jobs Toronto' -> 10 results
[websearch:exa]       ... (8 queries × 3 providers)
[websearch:firecrawl] ...
```

Filters, in order: must be a job-ish URL, must not be a board **category** page
(`INDEX_URL` / `INDEX_TITLE` — "ServiceNow Developer Jobs in Toronto (500 Open
Roles)" is not a posting), keyword match, geo match, dedupe against README +
archives + inbox + jobs.json.

**Dates come only from the page.** `datePosted` JSON-LD, `article:published_time`,
or `itemprop=datePosted`. No date → the row keeps an em dash and lands in `inbox/`
where the merger skips it. A search snippet is never turned into a date.

Writes `inbox/websearch--<date>--v<N>.md`.

### `ai_panel.py triage-inbox` (new subcommand)

Reads `inbox/*.md`, extracts rows whose Posted cell is an undated marker, and asks
the panel whether each is worth a human re-check:

```
| verdict | votes | posted | role | source file | url |
| servicenow | servicenow:3 | — | ServiceNow Architect at Zodiac... | gap-scan--2026-11-02--v3.md | ... |
```

Writes `inbox/_ai-triage--<date>--v<N>.md` — the leading underscore makes both
`jobs_merge_inbox.py` and `check_inbox.py` ignore it, so a review report can never
become a submission or acquire a posting date.

### Key resolution fixed for the search APIs

The store spells these labels inconsistently (`EXA API KEY for serach`,
`TAVILY AI API KEY (SEARCH)`, `JINA READER API KEY(SEARCH)`), so the exact-label pass
never matched. Added a regex label pass with a per-provider lookahead (Exa's
credential sits ~20 lines below its label, behind a prose blurb and a docs block).
All six now resolve:

```
TAVILY_API_KEY resolved   TAVILY_API_KEY_ALT resolved   EXA_API_KEY resolved
FIRECRAWL_API_KEY resolved   JINA_API_KEY resolved   PARALLEL_API_KEY resolved
```

### Wired into `scripts/daily_scan.sh`

```
ai_panel.py queries      -> raw/ai_queries.json
gap_scan.mjs             -> uses those as extra Adzuna variants
web_search_scan.py       -> inbox/websearch--*.md
ai_panel.py triage-inbox -> inbox/_ai-triage--*.md
jobs_merge_inbox.py      -> README
sync_readme_to_jobs.mjs  -> jobs.json + public copies
build_site.py            -> public/jobs-data.json + public/index.html
```

Every AI/search step is non-fatal; a dead free tier cannot stop the scan.

## Verification — full `daily_scan.sh` run, 2026-11-03

```
SCAN_AUTOCOMMIT=0 ./scripts/daily_scan.sh   -> rc=0

[websearch:tavily]    8 queries x 10 results
[websearch:exa]       8 queries x 10 results
[websearch:firecrawl] 8 queries x 10 results
triaged 20 inbox rows with 3 peers (reject=2, salesforce=11, servicenow=7)

[sync] readme rows=966 already-in-feed=752 added=214 total=986
site: 818 jobs {'servicenow': 212, 'salesforce': 242, 'other': 364}
      · 92 duplicate mirrors collapsed · newest 2026-11-03
README dated rows: 1001   public/jobs-data.json rows: 818
```

Artefacts written: `raw/ai_queries.json`, `raw/ai_triage.json`,
`raw/websearch_last.json`, `inbox/websearch--2026-11-03--v2.md`,
`inbox/_ai-triage--2026-11-03--v2.md`.

## Known limitations

- **Search APIs return mostly board category pages.** Before `INDEX_URL`/`INDEX_TITLE`
  the first dry run kept 13 useless rows out of 20; after, 4 real postings out of 60
  results. The filter is aggressive on purpose — a category page costs a fetch and
  yields nothing.
- **Most search hits are undated.** Only pages that publish JSON-LD or an
  `article:published_time` get a date; aggregator postings usually don't. Expect the
  websearch submission to be mostly undated review rows, not feed rows.
- **The merge bumps every inbox file on every run**, so a scan after a gap produces a
  large inbox diff (74 deletions / 68 additions here). Pre-existing behaviour of
  `jobs_merge_inbox.py`, not introduced by this change.
- **Nothing was committed or pushed.** The working tree holds the refreshed data; the
  live page does not update until it is committed and pushed.

# Parallel AI + search fan-out scan; repaired the collapsed job tables

**Date:** 2026-11-03
**Scope:** `bestiejob` — `scripts/parallel_fanout_scan.py` (new), `tools/import_fresh_rows.py` (new), `README.md`

## What was broken

### 1. The README had no Salesforce section at all

`README.md` carried **813 posting rows under a single `### ServiceNow jobs` heading** —
333 ServiceNow rows and 460 Salesforce rows in one table. The `### Salesforce jobs`
heading was gone, although the contents list at the top still linked to
`#salesforce-jobs-400`.

`tools/build_site.py` builds the page from the README tables, so there was no Salesforce
section to render: everything collapsed into one list. The heading had been lost by the
2026-11-03 peer-branch merge, which rewrote rows in place without re-emitting headings.

### 2. Fresh postings never reached the page

The scanners write dated postings to `FRESH_JOBS.md` and `raw/*.json`; the site is built
from `README.md`. Those are separate stores. A posting dated today could sit in
`FRESH_JOBS.md` indefinitely without ever appearing on the site — `FRESH_JOBS.md` held
**984 dated rows, 177 of them not in the README at all**.

### 3. A reposted role kept its older date

Dedupe matched a fresh row to its existing README row by canonical URL and then kept the
*existing* date. When an employer re-listed a role, the fresh posting date was discarded,
so the row aged out of the 7-day window while still being live.

### 4. Job Bank contributes zero usable rows

Its quoted-phrase search (`searchstring="servicenow"&locationstring=Toronto, ON`) returns
`manager, computer system operations`, `shipping coordinator`, `counsel`. The quoted
phrase is not honoured, so every row fails the keyword filter. Unquoted `servicenow
developer` returns **0** job IDs. The source is therefore inert but harmless — its rows
are filtered out, not imported. Left in place, documented as dead until Job Bank's
search behaves.

### 5. Adzuna is disabled

`ADZUNA_APP_ID` / `ADZUNA_APP_KEY` are absent from `dbpasses.txt`. Adzuna is the richest
Canadian aggregator and it is skipped on every run (`daily_job_scan.mjs` logs the skip).

## What was added

### `scripts/parallel_fanout_scan.py`

The ATS boards were already exhausted: 2,083 Greenhouse postings yielded **2** rows dated
within 7 days, because the bottleneck is the *set of boards*, not the polling. This pass
grows that set.

**harvest** — fans out in parallel:
- local models: vLLM `:8000`, Ollama `:11434`, LiteLLM `:4000`, Open WebUI `:3000`
  (model id discovered from each `/v1/models`)
- cloud keys: Groq, Gemini, DeepInfra, Kilo, SiliconFlow, Mistral
- search APIs: Exa, Tavily (2 keys), Firecrawl, Jina, Parallel

Six divide-and-conquer prompts split the employer universe (banks/telco, agencies,
ServiceNow partners, Salesforce partners, GTA employers, ATS-native). Queries include
`site:`-scoped searches against the ATS domains themselves, which return individual
postings whose URL carries the board token.

Every worker writes its **own file** under `raw/fanout/` (`model-*.md`, `search-*.md`,
plus one combined `harvest-*.json`), so one dead provider cannot take the run down and
each contribution is auditable.

**aggregate** — extracts board slugs, then resolves company *names* to slugs by probing
the public board API of 8 platforms (Greenhouse, Lever, Ashby, SmartRecruiters, Workable,
Recruitee, BambooHR, Pinpoint). A wrong guess 404s harmlessly. A company name is a
hypothesis until its board answers 200 and returns a posting.

Result of the first run: **64 live boards** discovered out of 1,210 candidates, including
ServiceNow partners not previously polled (highmetric, levio, crossfuze, rapdev, nolio),
plus varicent, geotab, pointclickcare, achievers, sitetracker, vo2-group, cclfg.

### `tools/import_fresh_rows.py`

Repairs the table split and promotes fresh rows, surgically — it never re-renders the
whole file the way `jobs_merge_inbox.py` does (that path caps tables at
`--max-per-table 150` and would archive ~650 existing rows to `README.BAK_*`).

## Verification

```
before:  813 rows, one table (333 SN / 460 SF), no Salesforce heading
after :  820 rows — ServiceNow 340 · Salesforce 453 · other 27
         +85 genuinely new rows, 9 posting dates refreshed to the newer date
         headings, counts, <strong>Show N postings</strong> and contents links all rebuilt
```

Job Bank funnel (unchanged, confirms the source is inert rather than noisy):

```
raw 55 | keyword 0 | geo 0 | within 7 days 0 | new 0
```

## Known limits

- **Job Bank search is broken** for these queries (see above). Needs a different endpoint
  or a real API key before it can contribute.
- **Adzuna is unconfigured** — add `ADZUNA_APP_ID` + `ADZUNA_APP_KEY` to `dbpasses.txt`.
- Ollama answered nothing: `llama3.3:70b` timed out at 150 s cold-loading. The three
  other local endpoints answered fine.
- DeepInfra returned HTTP 401 for all calls; the key loads, so the model id or account
  tier is the issue.
- Firecrawl 429s after ~10 requests/min; the fan-out degrades to the other providers.
- The 85 new rows are the honest incremental yield: the existing sources are saturated,
  which is why the fan-out pivots to discovering *new employers* instead.

## Follow-up: inbox guard was red for everyone

`inbox/grokbot-hidden-title--2026-11-03--v13.md:10` had `2026-11` in the Posted cell.
`scripts/check_inbox.py` accepts only `YYYY-MM-DD` or an undated marker, so the
"Inbox submission guard" workflow failed on **every** push, including ones unrelated to
that file. The source page shows only a month, so the honest value is an em dash
(the merger skips undated rows). Guard now reports:
`OK: every submission is well-formed` — 89 files, 10,200 rows.

Verified live after the final push:

```
jobs-data.json   977 jobs · 61 dated 2026-11-03 · generatedAt 21:24:20Z
README (live)    ### ServiceNow jobs (353) · ### Salesforce jobs (440) · ### Other jobs (412)
Pages deploy     success on 2a7c08b
Inbox guard      success on 908948b
```

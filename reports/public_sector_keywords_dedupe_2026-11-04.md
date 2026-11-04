# Public-sector source, AI keywords, and feed dedupe — 2026-11-04

Follow-up to `reports/ai_search_harvest_2026-11-04.md`, which found the board is
~78% staffing-agency postings with near-zero public-sector employers, and that
the feed carried 133 company+title clusters.

## 1. Public-sector scanner (new source)

`scripts/public_sector_scan.py` (new), wired into `.github/workflows/hourly-scan.yml`
as *Public-sector scan (OPS + City of Toronto)* with `continue-on-error`.

| Board | Route | Status on 2026-11-04 |
|---|---|---|
| City of Toronto — `jobs.toronto.ca/jobsatcity` | SAP SuccessFactors. `/search/` renders job tiles with `data-url`; each detail page carries schema.org `JobPosting` microdata with `datePosted` + `validThrough`. | **works** — 1 open external posting (PARAMEDIC LEVEL 1, `datePosted` 2026-10-16). Internal-only competitions need an employee login and are not visible. |
| Ontario Public Service — `www.gojobs.gov.on.ca/Search.aspx` | Custom ASP.NET behind **Radware Bot Manager**. A plain GET returns `Radware Captcha Page` / "We apologize for the inconvenience"; `sitemap.xml`, `RSS.aspx` and `Preview.aspx` answer the same way. | **blocked** — recorded, never circumvented (same call as the 2026-10-31 public-sector review). |
| OPS fallback — `jobbank.gc.ca` employer feed | `?searchstring=ontario+public+service&sort=D` returns postings whose employer is verbatim `Ontario Public Service`; list and detail both carry a posted date (`Posted on November 03, 2026`). | **works** — 19 dated OPS competitions. |

Live run output:

```
City of Toronto   1 tiles, 0 undated/closed
OPS gojobs        blocked (Radware bot manager)
OPS Job Bank      19 articles, 0 non-OPS skipped, 0 unparsed
new postings: 0
```

`--all` (keyword filter off) produced 20 dated rows — 18 clinical/corrections/
administrative OPS roles plus the paramedic — confirming the parsers and dates
are real and that **the keyword filter, not a scraper bug, is what returns 0**.
None of the 19 OPS mirror rows are ServiceNow/Salesforce/IT, so the board's
coverage does not change today. OPS IT competitions live on the bot-walled
board and only reach this pipeline indirectly (LinkedIn / gap scan).

Undated or closed pages are always dropped, never dated by guesswork. Raw probe
output: `raw/public_sector_2026-11-04.json`.

## 2. AI-panel keywords wired into the passes

The 12 variants in `raw/ai_queries_60d.json` (`servicenow itom`, `cmdb specialist`,
`itam consultant`, `servicenow gsd`, `salesforce pardot`, `salesforce wave`,
`servicenow sysdev`, `salesforce apex`, `servicenow release`, `salesforce ahc`,
`servicenow table`, `salesforce flow`) are now consumed by every pass:

* **LinkedIn** — `scripts/linkedin_guest_scan.py`: added the variants the list
  still lacked (`CMDB specialist`, `ITAM consultant`, `ServiceNow GSD`,
  `ServiceNow sysdev`, `ServiceNow release`, `ServiceNow table`, `Salesforce Wave`,
  `Salesforce AHC`, `Salesforce Flow`, `Salesforce Apex`).
* **Adzuna** — `scripts/scrape_adzuna.js` had **no ServiceNow keyword at all** and
  only ever asked for `salesforce developer`. Added 21 platform keywords
  (servicenow{,developer,administrator,architect,consultant,itom,gsd,sysdev,release,table}
  salesforce{,administrator,consultant,pardot,wave,apex,ahc,flow}, itsm, itam).
* **CI gap scan** — `scripts/gap_scan.mjs` already merges AI proposals from
  `raw/ai_queries.json`; the five variants missing there (`itam consultant`,
  `servicenow sysdev`, `servicenow release`, `salesforce ahc`, `salesforce flow`)
  were appended to its `keywords` list, so the hourly job feeds them to Adzuna.

Verified on a dry run:

```
[gap:adzuna] +17 AI-suggested variants from .../raw/ai_queries.json
[gap:adzuna] variants=35 today-only matches=22
[gap] dry run: would add 7 of 22 (total 1587)
```

Many calls returned Adzuna `429`/`503` (throttling) during the probe, so that
7-row figure understates what the hourly job will see; nothing was merged from
the throttled run.

## 3. Feed dedupe + salary/work-arrangement backfill

Done in `scripts/sync_readme_to_jobs.mjs` (the generator that owns `jobs.json`),
so the hourly refresh cannot overwrite it:

* `dedupeRows()` — one row per company+title+city. Employer-board rows beat
  aggregator mirrors, then newest wins. Collapsed mirrors are preserved on the
  surviving row as `alternates` (same shape the cards use), capped at 6.
  Multi-city reposts are deliberately kept: different city = different listing.
* `inferSalary()` — extractive only: `$125,500 - $148,200 CAD`,
  `$111,700.00 to $149,000.00 annually`, `118,000–176,000 USD per year`. The text
  must signal money and the figure must be annual-scale (20k–400k), so an hourly
  rate or a headcount range can never become a salary.
* `inferArrangement()` — remote / hybrid / onsite from explicit wording, with a
  negation guard ("no remote option" is not remote).

Run log:

```
[sync] readme rows=1657 already-in-feed=1639 added=0 undated-dropped=0
listing-pages-skipped=8 listing-pages-purged=0 salary-filled=19
arrangement-filled=80 dupes-collapsed=91 total=1489
```

| | before | after |
|---|---|---|
| feed rows | 1580 | **1489** (−91) |
| rows carrying alternates | 0 | 74 (91 mirror links) |
| salary populated | 66 (4.2%) | 85 (5.7%) |
| workArrangement known | 390 (24.7%) | 470 (31.6%) |

Spot-checked extractions are genuine posting text, e.g.
`TD Site Reliability Engineer Lead → CAD 125,500–148,200`,
`Equinix DevOps Engineer → USD 118,000–176,000`,
`Job Bank ServiceNow Application Developer → CAD 115,812/year`.

## Verification

* `node scripts/sync_readme_to_jobs.mjs` → log above; `jobs.json` + 3 mirrors written.
* `python3 tools/build_site.py` → `site: 1329 jobs {servicenow 427, salesforce 479, other 423} · 177 with duplicate mirrors collapsed`.
* `node scripts/check_readme_sort.mjs` → `OK: 7 Posted-column tables are newest-first`.
* `python3 scripts/check_site_links.py` → `jobs=1329 applyLinks=1 tabs=True aria=True stamp=True fit=True blocked=0`.
* `node --check` on the two edited JS files, `ast.parse` on the LinkedIn scanner, `yaml.safe_load` on the workflow.

## Limitations

* OPS's own board remains unreachable without solving a Radware CAPTCHA, which
  this repo has declined to do in writing. The Job Bank mirror is a subset and,
  today, entirely non-IT.
* Page card count (1329) is unchanged by the feed dedupe: `build_site.py` already
  clusters more aggressively (rooted-company + related-title keys, 177 mirrors).
  The README tables still list every source row; only the feed is canonicalised.
* The 80 arrangement fills are heuristic. `unknown` remains on 1100 rows.

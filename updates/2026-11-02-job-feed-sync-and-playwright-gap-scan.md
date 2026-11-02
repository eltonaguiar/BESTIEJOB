# Feed sync + Playwright gap scan (2026-11-02)

## What was broken

The repo serves two different datasets, and nothing kept them in agreement:

| Consumer | File | Built from |
|---|---|---|
| Live page `public/index.html` ("Today" chip, tabs) | `public/jobs-data.json` | `README.md`, rebuilt by `tools/build_site.py` |
| API `/jobs.json`, `public/app.js` | `jobs.json` | `scripts/daily_job_scan.mjs` sources only |

Consequences found today:

1. **Curated rows never reached the feed.** Ateko/FX Innovation
   *ServiceNow Architect (526327)* is in `README.md` (row dated 2026-11-02) and in
   `jobs-data.json`, but was absent from `jobs.json` — so any consumer reading the
   API or `app.js` could not see it.
2. **The page was stale.** `jobs-data.json` was built at 15:36Z; the scan run at
   22:19Z rewrote only `jobs.json`, `FRESH_JOBS.md` and the README *daily-scan*
   block. The three curated tables the page is built from were untouched, so the
   page kept serving the 15:36Z picture.
3. **"Only 3 ServiceNow jobs today" is clustering, not data loss.** `build_site.py`
   collapses rows with the same normalised title+company into one card
   (Lightspeed Toronto+Ottawa, CGI Drummondville+Sherbrooke). Six dated rows →
   5 cards at 15:36Z; the count moves as rows arrive.
4. **One feed row had `postedDate: null`**, which makes date filtering and
   `.startsWith()` consumers throw.

## What changed

### `scripts/sync_readme_to_jobs.mjs` (new)

Parses the three README tables and appends every row missing from `jobs.json`
(matched on normalised URL first, then title+company), then writes all four feed
copies. Rows without a posted date are dropped and counted — dates are never
invented. `--dry-run` previews.

### `scripts/gap_scan.mjs` (new)

Playwright sweep of partner career pages that repeatedly carry roles the
aggregators miss or index a day late — FX Innovation/Ateko, Cofomo, Everforth,
Coaxxion, CloudKettle, Lane Four, Crossfuze — plus 18 extra Adzuna keyword
variants (`now platform`, `csdm`, `service mapping`, `omnistudio`, `revenue cloud`,
`data cloud`, `agentforce`, …) scoped to `max_days_old=1`.

For each site it reads `JobPosting` JSON-LD and keyword-matching anchors, opens
undated detail pages (cap 24, concurrency 4) to read `datePosted`, and merges
dated, Canada/remote-relevant rows into the feed. Undated candidates are recorded
in `raw/gap_scan_<date>.json` instead of being given a guessed date. Flags:
`--sites`, `--adzuna`, `--dry-run`.

### Recurring wiring

- `scripts/daily_scan.sh` now runs, after a successful scan: README→feed sync →
  gap scan (disable with `SCAN_GAP=0`) → `tools/build_site.py`; each step is
  non-fatal. It also commits `public/jobs-data.json` and `public/index.html` so
  the deployed page matches the feed.
- `.github/workflows/hourly-scan.yml` runs the sync and `build_site.py` before
  committing, and includes the two page files in the commit, so Pages data tracks
  the hourly scan instead of waiting for the next README edit.
- `package.json`: `scan:gap`, `sync:readme`, `build:site`.

## How it was verified

- `node scripts/sync_readme_to_jobs.mjs --dry-run` then the real run; both print
  rows read / already-in-feed / added / undated-dropped.
- `node scripts/gap_scan.mjs` run against the seven live partner sites; per-site
  JSON-LD and anchor counts are printed, and undated candidates are logged rather
  than dated by hand.
- `python3 tools/build_site.py` rebuilds `public/jobs-data.json` +
  `public/index.html`; the page timestamp and Today counts are read back from the
  rebuilt feed to confirm Ateko and the new rows are present.

## What the Playwright pass actually found (2026-11-02 22:24Z)

| Site | JSON-LD | keyword anchors | posted date exposed |
|---|---|---|---|
| FX Innovation / Ateko | 0 | 0 (16 links, none keyword-titled in DOM) | **no** — detail page has no `<time>`, no `meta[property*=published]`, no `datePosted` |
| Cofomo | 0 | 5 | no |
| Everforth | 0 | 0 | no |
| Coaxxion | 0 | 3 | no |
| CloudKettle | 0 | 22 | no |
| Lane Four | 0 | 26 | no |
| Crossfuze | 0 | 0 | no |

None of the seven partner sites publish a machine-readable posting date. They are
client-rendered listing pages with no `JobPosting` JSON-LD, so the run produced
zero dated rows and no invented dates.

**First run collected 24 false positives** — service/product pages such as
`cofomo.com/en/technologies/servicenow`, `coaxxion.com/itom` and
`ateko.com/en/services/salesforce/agentforce/`, which match the keyword filter but
are not postings. The anchor filter now requires a job-shaped URL
(`/jobs/<id>`, `/postings/`, `/apply`, or a known ATS host) and rejects
`/services|insights|technologies|products|solutions|…` paths, and the detail-page
fallback only accepts an explicit "posted"/"publication date" label.

Net effect: the partner pass currently contributes **no** dated rows — it is a
watchdog, not a volume source. Volume comes from the Adzuna today-only variants
and the existing hourly aggregator scan.

That is also the root cause of the Ateko surprise: the role is real and live
(`fxinnovation.com/en/jobs/526327`, "SERVICENOW ARCHITECT / Canada - Remote /
Architecture / Permanent") but has no date to sort on. It therefore only reaches
the page through the curated README row, which carries the date a human verified —
exactly the path the sync script now covers.

The net-new volume from this run came from the Adzuna today-only variant pass:
69 matches, 14 not already in the feed.

## Open items

- Detail-page date parsing for sites without JSON-LD is heuristic (regex over
  visible text); a site that formats dates unusually will land in `raw/…undated`
  rather than in the feed. Check that file when a known role is missing.
- `jobs.json` `source` is now `readme` for curated rows and
  `site:<partner>` for gap-scan rows, so the UI source filter can separate them.

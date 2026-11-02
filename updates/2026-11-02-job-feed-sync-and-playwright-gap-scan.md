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

## Follow-up: undated partner postings now go to the inbox

### The gap

`raw/gap_scan_<date>.json` was a dead end: the Playwright pass wrote undated
partner postings there and nothing downstream ever read the file, so a live role
on a partner site (Lane Four, Ateko, Cofomo) had no route to `README.md`, the
page or the feed.

### Change

`scripts/gap_scan.mjs` now writes `inbox/gap-scan--<date>--v<N>.md` — the same
queue every agent submits to — instead of stopping at `raw/`. Dated rows merge
normally; undated rows carry `—` in the Posted column, which
`tools/jobs_merge_inbox.py` skips by design, so "unknown" can never become an
invented date. The file follows the protocol's `<model>--<date>--v<N>.md`
convention and is skipped entirely when its URLs are already covered by today's
existing `gap-scan` submissions (`--no-inbox` disables it).

Because it is a normal submission, the merge step in `daily_scan.sh` and the new
`Merge inbox submissions into README` step in `hourly-scan.yml` pick it up with
everything else.

Verified: `node scripts/gap_scan.mjs --sites` wrote
`inbox/gap-scan--2026-11-02--v1.md` with 0 dated and 2 undated rows; the merger's
dry run parsed 529 incoming rows and left both em-dash rows untouched.

### Lane Four Salesforce postings — why they are not on the page

The two undated candidates are `lanefour.com/job-posting/salesforce-consultant/`
and `.../salesforce-administrator/`. Neither page shows a "Posted" line, and
their JSON-LD `datePublished` is **2021-08-03** and **2026-06-01** — both outside
the 30-day window, and the first is clearly a page-creation artefact rather than
a posting date. Adding them would mean asserting a date the employer does not
publish, and the merger would archive them on the next run anyway, so they stay in
the inbox submission for review instead of the live tables.

## Other agents' submissions that never surfaced

Checked after the report that other agents' work was missing from `main` / Pages:

1. **No CI step ran the merger.** `hourly-scan.yml` and `scrape_jobs.yml` both
   committed `README.md` but neither invoked `tools/jobs_merge_inbox.py`, so 78
   inbox submissions from 12+ models could only land when someone ran the merge
   locally.
2. **The per-table cap silently archived ~450 live rows.** Every pipeline call
   used the tool's `--max-per-table 150` default. With 933 unique rows inside the
   30-day window (251 ServiceNow / 282 Salesforce / 400 other), ~449 of them were
   written to `README.BAK_*` instead of `README.md` — and the page is built from
   `README.md`. Pipelines now pass `--max-per-table 400`; a merge at that cap
   produced a 968-row README, 813 cards, and a passing
   `scripts/check_site_links.py`.
3. **The feed/sync/scan fixes were never on `main`.** `HEAD` is
   `job-list-merged-inbox-2026-11-02`; `origin/main` kept taking hourly-scan
   commits (`9f49de2` …) with the pre-fix code, so `jobs.json` on `main` still
   lacked the curated rows even though they were in the README.
4. **Inbox version bumps were left uncommitted.** Running the merger renames every
   submission `vN → vN+1`; those renames were never committed, so the remote
   `inbox/` drifted from the local one. `hourly-scan.yml` now commits `inbox`
   together with the job data.

## Deploy to main + three new guards

- **README banner.** `tools/jobs_consolidate.py:render()` now emits a centred
  `<h2>` link to <https://eltonaguiar.github.io/BESTIEJOB/> plus a bold inline
  link, directly under the title. It lives in the renderer rather than in
  `README.md` because every merge rewrites that file and would erase a hand edit.
- **`scripts/check_inbox.py` + `.github/workflows/inbox-guard.yml`.** Validates
  every submission: filename `<slug>--<YYYY-MM-DD>--v<N>.md`, at least 5 cells per
  row, Posted either a real calendar date or an explicit undated marker, and an
  absolute URL on every dated row. A relative date ("2 days ago") or a split row
  now fails the build instead of being dropped by the merger without a word.
  `hourly-scan.yml` runs it before the merge step. Verified against the 53 live
  submissions on main: 9,237 rows, 0 violations.
- **`scripts/recheck_undated.mjs` + `.github/workflows/undated-recheck.yml`.**
  Monthly (1st, 09:00 UTC) re-fetch of every undated inbox row. A page that now
  publishes a `datePosted` inside the 31-day window is promoted into
  `inbox/undated-recheck--<date>--v<N>.md` and merged; stale dates (Lane Four's
  2021-08-03 and 2026-06-01) and pages that still publish nothing are reported,
  never promoted.
- **Deploy path.** The branch was rebuilt from `origin/main` carrying only these
  files, then merged at `--max-per-table 800` so no existing row was archived:
  `removed: 0, added: 21`, `check_site_links.py` OK, page 849 cards, then pushed
  to `main` to trigger the Pages deploy.

## Deploy #2: critical jobs, and the real reason nothing reflected

- **`critical_buffy_2026-11-02.MD`** records the 13 verified ServiceNow /
  Salesforce roles that were in `jobs.json` but in neither `README.md` nor
  `APPLIED.md` — the feed had them and the page did not. Every link returned HTTP
  200 at capture time, agency mirrors of the same requisition were collapsed
  (ATB/ATB Financial, four WSIB city variants, AIM's EN+FR pair), and the file
  carries a "deliberately excluded" table (Lane Four's undated pair, two 403
  pages, Salesforce-the-vendor GTM roles, French-gated Ateko roles). The same
  rows ship as `inbox/buffy-critical--2026-11-02--v1.md` so a peer can re-merge
  them with one command.
- **Root cause of the chronic "my work never reflects" reports.** The hourly run
  at 23:10Z failed on `git push`: `! [rejected] main -> main (fetch first)` —
  peer agents push to main mid-run, so the job's data was stranded locally. The
  same run also tried to commit a **104,208-line deletion** of `jobs.json`
  because it rebuilt the feed from scanner sources alone. `hourly-scan.yml` now
  rebases once and retries the push, and the README→feed sync step prevents the
  shrink.
- **Two rebases during this deploy conflicted** in `README.md` / `jobs.json` /
  `public/*`. Both were resolved by taking upstream's data files and re-running
  merge → build → sync, which regenerates every row from `inbox/`. That is why
  the inbox, not the README, is the source of truth.
- **Final state:** `main` = `17d0d8b` · README 1,021 rows with the Pages banner ·
  page 860 cards · Pages deploy success for `17d0d8b` · live
  `jobs-data.json` 860 cards, 71 posted today, with WSIB ITSM Manager, CloudKettle
  Industries architect, ProperExpression RevOps and NeuraFlash Agentforce all
  present on the deployed site.

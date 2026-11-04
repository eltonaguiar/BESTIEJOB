# Stranded branch rows + the hourly feed deletion — 2026-11-04

Two problems found while auditing unmerged branches, one of them actively
shrinking the live board every hour.

## 1. The hourly scan was deleting curated rows (root cause)

`scripts/daily_job_scan.mjs` rewrites `jobs.json` from scratch on every run. Its
`loadExistingJobs()` loaded the previous feed and then re-tested **every carried
row** against the keyword tag regexes:

```js
if (!job.tags || job.tags.length === 0) {
  const tags = matchTags(job.title);   // ServiceNow / Salesforce / partner stack
  if (tags.length === 0) continue;     // ← row deleted
}
```

Keyword tags are the *search* remit: they decide what a scrape may add. Applying
them to rows that are already on the board deletes everything the merger,
`sync_readme_to_jobs.mjs`, or a peer's inbox submission had already accepted —
any role whose title does not literally contain a ServiceNow/Salesforce keyword.

Effect in the 20:12 UTC run: the feed went **1,869 → 1,610 rows** and the page
**1,693 → 1,447 cards**. The 265 lost rows were 230 titles like
`Senior DB2 DBA`, `Workday Integration Analyst`, `Senior MuleSoft Software
Engineer`, `Vulnerability Management Specialist`, `Senior GRC Engineer`,
`SQL Database Developer with Data Modelling` — all in-remit IT roles, plus
`BIM Designer` / `Litigation Associate` strays from the README "Other" table.

**Fix** — `scripts/lib/feed_carry.mjs`: a pure `carryExistingJobs()` that prunes
on validity only (needs URL + title + `postedDate`, inside the 45-day window, not
a generic career-homepage entry). Missing tags are *derived*, and an empty result
no longer rejects the row. `daily_job_scan.mjs` now calls it and logs what the
carry pruned (`[scan] carried-prune invalid= stale= generic=`), so future losses
are visible instead of silent.

The 265 deleted rows were restored from `80133a3:jobs.json` before the stranded
rows were imported.

## 2. Stranded rows on unmerged branches

Agents scan on their own branches; only `main`'s `jobs.json` reaches the page, so
unmerged branches strand real postings. All **55** remote branches were read and
compared against the feed (by cleaned URL, `alternates` mirrors, and
company + title + city):

| branch | new in-remit rows taken |
|---|---|
| `kilo-deep-scan-2026-11-03` | 410 |
| `publish-90-rounds-2026-11-04` | 208 |
| `kilo-deep-scan-2026-11-03c` | 127 |
| `restore-truncated-board-2026-11-03` (142 dated today) | 121 |
| `aicert-harvest-2026-11-03` | 111 |
| `kilo-deep-scan-2026-11-03b` | 59 |
| `Copilot/2026-11-01-verified-gap-merge` | 20 |
| `blobstopper-opencode-2026-11-02` | 15 |
| 6 smaller branches | 42 |
| **total imported** | **971** |

Kept out on purpose:

* **listing/search pages** — e.g. `publish-job-board-2026-11-03` carried
  `339 Servicenow Jobs in Toronto`, `Servicenow Jobs in Canada`, a ZipRecruiter
  search URL. The board links to postings, not search results.
* **out-of-remit titles** the IT regex still catches — tracks/civil/mechanical
  engineering, BIM, litigation, payroll, clinical, drivers.
* **bad extractions** — the `exa` harvest has rows whose company cell holds the
  location (`company: "Toronto, ON"`, `title: "… Job - Toronto, ON, Canada
  (VDart)"`), and aggregator page titles (`… Job Details`).
* rows older than the 45-day window, and rows already present under a mirror URL
  or the same company + title + city.

Tool: `tools/integrate_stranded_rows.py` (report-only by default; `--apply`
appends). It is repeatable for the next batch of unmerged branches:

```bash
python3 tools/integrate_stranded_rows.py              # what is stranded
python3 tools/integrate_stranded_rows.py --apply      # append to jobs.json
```

## Numbers

| | before this fix | after |
|---|---|---|
| feed rows | 1,610 (1,869 before the 20:12 prune) | **2,812** |
| page cards | 1,447 (1,693 at merge) | **2,489** |
| families | servicenow 547 · salesforce 596 · other 555 | servicenow 567 · salesforce 625 · other 1,297 |
| mirrors collapsed | 127 | 230 |
| rows that would survive the next hourly carry | 1,610 of 1,610 by keyword, 0 without tags | **2,812 of 2,812**, incl. 661 with no keyword tags |

## Verification

* `node --check scripts/daily_job_scan.mjs` — clean.
* `carryExistingJobs` unit checks: all 265 previously-deleted rows retained;
  stale (`2026-09-01`), generic (`Careers`) and URL-less rows still dropped;
  existing tags preserved; tags derived when absent.
* Carry applied to the real post-import feed → `2812 carried, dropped {invalid:0,
  stale:0, generic:0}`, 661 of them tag-less (previously deleted).
* `node scripts/sync_readme_to_jobs.mjs` → `total=2812`, `dupes-collapsed=32`,
  `arrangement-filled=147`.
* `python3 tools/build_site.py` → `site: 2489 jobs`.
* `node scripts/check_readme_sort.mjs` → OK; `python3 scripts/check_site_links.py`
  → `jobs=2489 blocked=0`; page is tabbed, stamped, every card links out.

## Limitations

* Imported rows keep the `postedDate` their scanner recorded. They were not
  re-fetched today, so a few may already be closed or expired — Adzuna rows in
  particular expire, and the next scans will drop them once they fall out of the
  45-day window or the source 404s.
* The "other" family is now the largest tab (1,297 of 2,489). That is the real
  mix of what our scans collect; the ServiceNow/Salesforce tabs keep the focused
  view, and the page ranks "Other" by fit.
* The README tables stay capped at 150 rows per family, so most of these rows
  live in the feed/page only — that is by design (`build_site.py` reads both).

## Related files

* `scripts/lib/feed_carry.mjs` — new carry policy.
* `scripts/daily_job_scan.mjs` — `loadExistingJobs()` uses it, logs the prune.
* `tools/integrate_stranded_rows.py` — new importer.

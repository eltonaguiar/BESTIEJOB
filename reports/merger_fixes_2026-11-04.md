# Merger: stop rewriting peer submissions; narrow the marketing rule; reject listing pages

Three defects in the merge pipeline, all observed while merging today's harvests.

## 1. A hand-run merger rewrote every other agent's submission

`tools/jobs_merge_inbox.py` ended by renaming every `inbox/*.md` it read to the next
`v<N>` and prepending a `<!-- merged … -->` stamp. That is correct for CI (the commit
then records which version was merged) and wrong for a human or agent running it
locally against a tree holding 100 peer submissions: a single run produced ~200
modified/untracked inbox files, and the peer files had to be moved aside and restored
by hand to keep a clean commit.

Now the rename+stamp step only runs with `--bump-inbox`; without it the merger prints
`inbox/ left as submitted`. The three workflows that relied on the old behaviour
(`hourly-scan.yml`, `linkedin-sweep.yml`, `undated-recheck.yml`) pass the flag.

## 2. The marketing exclusion threw out platform and analytics work

`EXCL` rejected the bare words `marketing` and `growth`, so four rows that belong on a
ServiceNow/Salesforce board were dropped on every run:

- Medcan — Marketing Cloud Specialist
- EQ Bank — Data Scientist, Growth (12 month contract)
- Lightspeed Commerce — Lead Data Analyst, Growth Marketing (×2)

The rule now matches marketing *job functions* (`marketing manager|specialist|coordinator|
director|associate|intern|consultant|ops`, `product marketing`, `demand gen`,
`content/email marketing`, `brand manager`, `growth hacker`, `growth marketing manager`)
and still rejects sales roles (`account executive`, `sales manager`, …) and
`Digital Marketing Specialist` / `Regional Sales Manager` controls.

## 3. Aggregator listing pages reached `jobs.json`

Exa answers "data analyst toronto" with a category URL, so harvests carried rows like
`ca.linkedin.com/jobs/servicenow-jobs-toronto-on` (title: "339 Servicenow Jobs in
Toronto") and `adzuna.ca/it-director` into the feed. New `is_listing_url()` in
`tools/jobs_consolidate.py`, mirrored as `isListingUrl()` in
`scripts/sync_readme_to_jobs.mjs`, rejects aggregator search/category shapes by URL:

- LinkedIn `/jobs/<keywords>-jobs[-<city>]` (a posting is `/jobs/view/<id>`)
- Glassdoor `-jobs-SRCH_` / `srch_` / `/Job/jobs.htm`
- Robert Half `/ca/en/jobs/<city>[/<keyword>]` (a posting is `/ca/en/jobs/detail/<id>/…`)
- Wellfound `/role/…`, Randstad `/jobs/q-…`, Eluta `-jobs-in-…`
- Job Bank `/marketreport/…`, ZipRecruiter `/Jobs/…`, WhatJobs, Adzuna category paths, Indeed `q-…`
- generic `?q=`/`?search=`/`?keywords=` queries and `/jobs/search|results|browse`

The merger counts them as `listing page(s)` and never writes them to README; the sync
also purges any already in the feed.

## Verification

- Case table of 9 URLs (real postings incl. Workday/Greenhouse/Job Bank `/jobsearch/jobposting/<id>`,
  Workopolis `/jobsearch/viewjob/<token>`, Robert Half `/detail/<id>`, plus listing pages): **0 wrong verdicts**.
- Against the 367 postings the websearch harvests carried that were missing from the board:
  exactly the 26 that are search/category pages are flagged; the rest are real postings that
  only lacked a posted date.
- Against every URL on the board (1,558): 8 flagged, all of them genuine search pages
  (`ca.linkedin.com/jobs/servicenow-jobs*`, `ca.indeed.com/q-*`, `insightglobal.com/jobs/search/…`,
  `ziprecruiter.com/Jobs/…`).
- Dry run: `buffy-test--…: +1 new, 5 duplicate, 2 listing page(s)`, summary
  `skipped: 2 rows that are aggregator listing pages` and `64 rows outside the board's remit`.
- Full run without the flag: inbox directory checksum identical before and after, no
  rename, no stamp. With `--bump-inbox`: 103 files renamed as before.
- `node scripts/sync_readme_to_jobs.mjs`: `listing-pages-skipped=8 listing-pages-purged=8`,
  feed 1,551 → 1,543, **0 rows added, only the 8 search pages removed**.
- `python3 tools/build_site.py`: `site: 1297 jobs …`.

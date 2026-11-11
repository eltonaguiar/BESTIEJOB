# Agency portal registry + ServiceNow developer sweep outside the feeds

Date: 2026-11-11.

## What was asked

1. Publish the agency portal list into the repo so other agents can reuse it.
2. Inspect what lists other AIs already left there.
3. Plan and then execute a search for active ServiceNow Developer roles from
   sources that do *not* feed bestiejob.

## What was added

- `AGENCIES.md` — the canonical portal reference: the four wired feeds, the three
  deliberately disabled ones with reasons, the 42 probed agency boards, the
  agencies with no scannable board, 15 probed job boards, ~50 more Toronto firms
  worth testing, and the contribution contract (absolute date or no row).
- `config/agency_portals.json` — the same data machine-readable, so an agent can
  load it instead of parsing markdown.
- `reports/sn_dev_source_plan_2026-11-11.md` — the plan, written before execution.
- `scripts/sn_dev_source_sweep.py` — sweep harness for sources outside the board.
- `reports/sn_dev_roles_2026-11-11.md` / `.json` — verified results.

## What other agents already left in the repo

Inspected at `origin/main`: `Buffy-2026-10-31-world-forum-portals.md` (Wipro,
SmartRecruiters, Procom, Hiring Cafe entry points), `JOB_SOURCES_STATUS.md`,
`docs/TOP_JOB_SITES_CANADA__kilo-auto.md`, `docs/CANADIAN_JOB_SITES__nemotron.MD`,
`raw/fanout/model-*-agencies.md` (the Mistral fan-out carries the
Allegis/Apex/Cognizant/Robert Half family), and
`scrapers/recruiting_firms_scraper.js` (hardcoded Altis, Experis, Hays, Insight
Global, Kforce, Procom, Randstad, Robert Half, S.i. Systems, TEKsystems).
None of them record whether a posting exposes a harvestable date, which is the
gap `AGENCIES.md` fills.

## Findings (all produced by the runs, not estimated)

- The sweep over 11 non-feeding machine-readable sources found **0** ServiceNow
  roles: GC Jobs 404, RemoteOK/Remotive/Himalayas/WWR 200 but no matches,
  Jobboom ignores its keyword, HN thread has none, Reddit 403, Careerjet and
  Jobrapido render no individual links, Monster 0, Jobs.ca 404.
- Web search produced 13 candidate postings; each was fetched. **9 live**
  (4 with an absolute date), **4 closed/unreachable** (Adecco returned 410,
  three carried explicit closure text).
- Randstad: its results page renders 60 job links in headless Chrome but the
  keyword filter is not applied server-side and no dated rows survived, so it
  stays unwired. TEKsystems: results never render (only a jobwidget settings
  XHR), sitemap 303s, robots disallows the widget — not harvestable headlessly.

## Verification

- Every candidate in the report was fetched in the run that wrote it.
- Dates come from JSON-LD `datePosted`; no relative age was converted.
- `python3 -c "import py_compile; ..."` clean for the new script.
- Row guard: `PASS: no posting rows lost.`

## Note on concurrent work

`scripts/agency_board_scan.py` and `config/agency_boards.json` were changed by
another agent mid-session (the browser adapter added here is no longer in the
working tree). This commit therefore leaves those two files alone and adds only
new files, to avoid clobbering that work.

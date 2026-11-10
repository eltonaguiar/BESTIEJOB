# The Accenture HAM row is in Sydney, and what the full board audit found

Date: 2026-11-10.

## The report

A card for "ServiceNow Hardware Asset Management (HAM) Consultant — Accenture —
Canada — fit 100 — 2026-11-10" was wrong on both the place and the date.

The requisition is real and live. Its own page says:

    title:      ServiceNow Hardware Asset Management (HAM) Consultant
    location:   addressCountry "Australia", addressLocality
                "Sydney, International House, 3 Sussex St"
    datePosted: 2026-06-25

Source URL (Accenture's Workday tenant, req 14379035):
`https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Sydney-International-House-3-Sussex-St/ServiceNow-Hardware-Asset-Management--HAM--Consultant_14379035`

The raw harvest record already held the correct string —
`Sydney, International House, 3 Sussex St, Australia` — so nothing in the stored
data claims Canada. What went wrong is upstream of storage:

- **Location**: the Workday search had been run with a Canada scope, and the
  query's scope was carried onto the row instead of the posting's own location.
  "Sydney" in the location is the city, not a hiring manager's name — the
  JSON-LD `addressCountry` settles it.
- **Date**: `2026-11-10` was the scan date, not a posting date. The page's
  `datePosted` is `2026-06-25`, so a date was manufactured by using "today".

Neither value may be published: a row's location and date come from the posting.

## What was built

Two local-only tools (not committed — `local_tools/` is in `.git/info/exclude`):

1. `local_tools/verify_active_jobs.py` — liveness + real location for any jobs
   JSON. Fetches every URL as Chrome, classifies `live` / `dead` / `blocked` /
   `error`, extracts location from JSON-LD (handling string-valued
   `jobLocation`/`address`), and classifies `toronto` / `ontario` /
   `remote-canada` / `other-canada` / `non-canada` / `unknown`.
   Writes JSON + CSV with both the claimed and the page location.
2. `local_tools/accenture_sn_jobs.py` — the Accenture-specific scanner, using
   their Workday CXS endpoints rather than HTML. Filters to Canada by taking the
   city out of `externalPath` and then confirming with the detail call.

Reusable instructions live in `.claude/skills/job-listing-verification/SKILL.md`.

## Full active-board audit (1,933 published rows)

Verdicts: live 592 · blocked 1082 · dead 257 · error 2.

Location read from the pages that answered: remote-Canada 272 ·
Toronto 60 · Ontario 8 · other Canada 32 ·
**non-Canada 19** · unknown 183 · remote-unknown 18.

`blocked` is dominated by LinkedIn (374 rows) and Adzuna (310):
those rows cannot be verified from the aggregator page and need the employer's own
board. `dead` (257) is real rot and should be dropped or re-sourced.

Rows whose row-text claims Canada while the page says otherwise (1):
- RapDev | Senior ServiceNow Engineer | claimed `Canada` | page `USA`

## Accenture, specifically

Accenture's Workday tenant currently has ~1,626 ServiceNow-matching requisitions
worldwide and **zero confirmed Canadian ones**: the two "London" hits are London,
UK (no province, no "Canada" in the record), which is exactly the ambiguous-city
trap the skill documents. So the board should not carry an Accenture Canada
ServiceNow row until one appears; when one does, the scanner will find it with a
real location and a real `datePosted`.

## How to re-run

    python3 local_tools/verify_active_jobs.py --input jobs.json --workers 24
    python3 local_tools/verify_active_jobs.py --company Accenture
    python3 local_tools/accenture_sn_jobs.py --canada

## Rules this makes concrete

1. A row's location is what the posting says, never the query's scope.
2. A row's date is the page's `datePosted`, never the scan date, and never a
   relative string ("Posted 14 days ago").
3. Ambiguous city names need a province or country before they count as Canada.
4. `blocked` is not `dead`; only 404/410 and explicit closure text are dead.

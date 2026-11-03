# Deep ATS sweep: 257 employer boards, verified dates only

**Date:** 2026-11-03
**Result:** board 1,411 → **1,413 jobs**. The sweep contributed three rows —
Danaher's Salesforce Field Service Developer (Concord, ON, 2026-11-02), SAIT's
ServiceNow Fundamentals instructor (Calgary, 2026-10-13) and Highmetric/NewRocket's
ServiceNow BPC (2026-10-28). Two of the three survived as live additions; the third
was contributed by another scanner inside the same merge window.

257 boards swept, 19,145 raw rows, 643 keyword-relevant, 89 Canadian, 30 dated
inside 21 days, 25 already on the board. The remaining two candidates (Take-Two's
ServiceNow ITOM lead, Lightspeed's ServiceNow Developer) turned out to be rows
another scanner had already merged under a different URL — the exact duplicate
that URL-only dedupe misses.

## The problem this addresses

The board is fed mostly by aggregators (Adzuna, LinkedIn, Job Bank, Talent.com,
jobsca, and a long tail of mirrors). Aggregators miss the case the operator
keeps asking about: a role that exists **only** on the employer's own careers
site, or only through an agency that holds the contract exclusively.

`today_feeds_scan.py` already speaks the right protocols, but its board lists
were tiny — 3 Ashby boards, 10 Workday tenants, 3 Lever sites — while the repos
had already discovered 38 Workday tenants, 20 Greenhouse boards and 14 Ashby
boards. So the deepest available knowledge was not being queried.

## What was built

**`scripts/ats_discover.py`** — finds *new* boards instead of re-reading known
ones. It dorks each ATS host with the platform terms, extracts the board token
from the URL, and appends it to `raw/ats_boards_extra.json`. 14 host-scoped
queries plus 10 city-anchored ones. City anchoring matters: `site:jobs.ashbyhq.com
"Toronto" servicenow` answers "who in this city runs this ATS", which a
continent-wide geography term does not.

**`scripts/ats_board_sweep.py`** — queries every discovered board's dated public
feed and keeps only rows whose date the employer's own system states:

| Route | Date field | Status |
|---|---|---|
| Workday | `postedOn` (relative string) | used, `30+` unusable |
| Greenhouse | `first_published`, else `updated_at` | used |
| Lever | `createdAt` (epoch ms) | used |
| Ashby | `publishedAt` (ISO) | used |
| SmartRecruiters | `releasedDate` | used |
| Recruitee | `created_at` | used |
| Breezy | `published_date` | used |
| Polymer | `published_at` | used |
| Gem | `first_published_at` | used |
| Teamtailor | RSS `<pubDate>` | used |
| **Pinpoint** | *none* | **rejected** |
| **BambooHR** | *none* | **rejected** |
| **Rippling** | *none* | **rejected** |
| **Jobvite** | per-page only | **rejected** |

Pinpoint is the painful exclusion: NewRocket, Crossfuze and Blue Mantis — three
real ServiceNow partners — run Pinpoint, and its public feed never says when a
job was posted. Rather than back-date them from a sitemap or an aggregator
mirror, those roles stay off the board.

## Why the yield is 2 and not 200

The sweep went 102 → 257 boards (2.5×) and 13,829 → 19,145 raw rows, and the
Canadian-relevant count moved 84 → 89. **Doubling board coverage added nothing.**
That is the finding: the reachable Canadian ServiceNow/Salesforce ATS universe is
saturated at roughly 89 live relevant postings, of which ~30 carry a usable date
inside three weeks and 25 were already on the board.

Discovery is also rate-limited in practice — Tavily returned HTTP 432 after six
consecutive queries, so `ats_discover.py` degrades to whatever it got.

The structural reason, confirmed again here: Canadian ServiceNow/Salesforce work
at the big partners surfaces through **agency mirrors**, not partner ATSes. Those
rows arrive via Adzuna/LinkedIn, which the board already reads.

## Two bugs fixed on the way

**`is_canadian()` matched `ns` inside "Locatio**ns**".** Province-code pattern
`n\.?s\.?\b` fired on every multi-location requisition, so `"9 Locations"` counted
as Canadian and US postings (`/Atlanta-GA/`, `/USA---TN---NASHVILLE/`) were
treated as Canadian hires. Province codes are now case-sensitive with word
boundaries, and a bare `"N Locations"` string is rejected as carrying no place.

**`workday_day()` back-dated stale postings.** `"Posted 30+ Days Ago"` was parsed
as *exactly* 30 days ago. That bucket means older than 30 days, so the parse gave
the stalest postings the freshest possible date. Returns `None` now.

**Board-duplicate check read the wrong file.** `board_rows()` first read
`public/jobs-data.json`, which only holds the recent window, so rows already in
`README.md` but outside the window were reported as net-new and then silently
dropped by the merger as URL duplicates. It reads `README.md` now; the reported
"net-new" figure went from 9 to the true 2.

## Verification

```
sort guard   OK: 7 Posted-column tables are newest-first
build        site: 1413 jobs {'servicenow': 319, 'salesforce': 390, 'other': 704}
README       1,753 rows — 412 ServiceNow / 536 Salesforce / 805 Other
live         1,413 jobs, 0 future-dated
```

Merger run as `--days 60 --max-per-table 10000`; the default `--max-per-table 150`
truncates the board.

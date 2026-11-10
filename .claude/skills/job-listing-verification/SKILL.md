---
name: job-listing-verification
description: Verify that a harvested job posting is still live and is really where the row claims (Toronto / Ontario / remote-Canada / elsewhere) before publishing or counting it. Use when a row looks too good (fit 100), when a card shows "Canada" but the req may be in Sydney or India, or when auditing the board for dead links and location drift.
---

# Job listing verification

A harvested row has three independent claims: that the posting exists, that it
was posted on a given date, and that it is in a given place. Sources routinely
get the third one wrong — an aggregator's query scope ("Canada") gets stored as
the job's location, so an Accenture req in Sydney, Australia appears as a
Canadian role. Verify from the posting itself, never from the row.

## 1. Is it live?

Fetch the URL as Chrome (`curl_cffi`, `impersonate="chrome"`) and classify:

| Result | Meaning |
|---|---|
| 200 + no dead marker | **live** |
| 404 / 410, or body contains "no longer available", "position has been filled", "job has expired" | **dead** |
| 401 / 403 / 429 / 999 | **blocked** — LinkedIn, Indeed, Adzuna. Not evidence of death; don't retry in a loop |
| 5xx or timeout | **error** — retry once later, never call it dead |

Blocked is the normal outcome for aggregator URLs. Verify those through the
employer's own board instead of the aggregator page.

## 2. Where is it actually?

Prefer structured data, in this order:

1. **ATS JSON API** (best). Workday tenants expose
   `POST https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<Site>/jobs`
   with `{"searchText": "...", "limit": 20, "offset": 0}` and
   `GET {base}{externalPath}` → `jobPostingInfo.location`. The list endpoint's
   `locationsText` is often empty; the city is in `externalPath`
   (`/job/<City-slug>/<Title>_<id>`), and the detail call is authoritative.
2. **JSON-LD** `JobPosting.jobLocation.address` (`addressLocality`,
   `addressRegion`, `addressCountry`). Note `jobLocation` is sometimes a bare
   string and `address` sometimes a string — handle both.
3. **Page text** `City, ON` / `City, Ontario` style matches — weakest.

If none of those yield a location, record `unknown`. **Never** infer location from
the rest of the HTML: site footers mention "United States" on Canadian pages.

## 3. Classify, with the ambiguous-city rule

`toronto` (Toronto/GTA) · `ontario` · `remote-canada` · `other-canada` ·
`non-canada` · `unknown`.

Cities that exist in Canada *and* elsewhere require a province or the word
"Canada" before they count as Canadian:

> london · cambridge · richmond · windsor · surrey · victoria · waterloo ·
> hamilton · kingston

"London" with no qualifier is London, UK until proven otherwise — this exact case
produced two false Canadian Accenture reqs.

Remote is not a location: "Remote" with no country is `remote-unknown`, and
"Remote (US)" is `non-canada`.

## 4. Dates

Never convert a relative age ("Posted 14 Days Ago", "30+ Days Ago") into a date.
If the page has no machine-readable date (`datePosted`), the row has no date and
must not be published with one.

## 5. Running it

The board keeps two local-only tools (deliberately uncommitted, in
`local_tools/`, excluded via `.git/info/exclude`):

    python3 local_tools/verify_active_jobs.py --input jobs.json --workers 24
    python3 local_tools/verify_active_jobs.py --company Accenture --limit 20
    python3 local_tools/accenture_sn_jobs.py --canada      # Accenture Workday tenant

Outputs land in `local_tools/out/` (`*.json` + `*.csv`). Treat `dead` and
`claimed-Canada-but-page-says-elsewhere` as board defects; treat `blocked` as an
unverified row, not a defect.

## 6. Reporting

Report the count checked, the verdict split, the location split, and every row
where the claim and the page disagree — with both strings, so a human can judge
whether the page or the row is wrong.

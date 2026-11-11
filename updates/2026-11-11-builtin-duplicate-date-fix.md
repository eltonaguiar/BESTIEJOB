# Duplicate Built In row carried a date the posting does not show

Date: 2026-11-11.

## What was broken

The same Take-Two Interactive posting (`Senior Lead, ServiceNow ITOM`) appeared
twice in `README.md` under two domains, with dates 13 days apart:

    | 2026-11-03 | ... (https://builtin.com/job/senior-lead-servicenow-itom/11793287) | ... | via builtin |
    | 2026-10-21 | ... (https://builtintoronto.com/job/senior-lead-servicenow-itom/11793287) | ... | via Built In Toronto |

Same requisition ID, so at most one date is real. On 2026-11-11 both
`builtin.com/job/senior-lead-servicenow-itom/11793287` and the
`builtintoronto.com` mirror returned HTTP 200 and both render `2026-10-21`.
`2026-11-03` matches no date on either page — most likely a scrape-time stamp
recorded as a posting date, which the board's rules forbid.

## What changed

- `README.md`: the `builtin.com` mirror's date corrected to `2026-10-21`.
- `jobs.json` plus the regenerated `public/` payloads: `postedDate` for that URL
  set to `2026-10-21T12:00:00.000Z`.
- Row kept rather than deleted, because the row guard treats a dropped posting
  as a regression and the duplicate is a legitimate second source.

## Verification

- Both mirror URLs fetched live: HTTP 200, page prints `2026-10-21`.
- `grep` for `senior-lead-servicenow-itom/11793287` in README shows both rows
  now dated `2026-10-21`.
- `public/jobs-data.json` carries the corrected `postedDate` after rebuild.
- `python3 .github/scripts/readme_job_row_guard.py`: `PASS: no posting rows lost.`

## Follow-up

The `2026-11-03` value originates in another agent's Built In sweep inbox file,
which this fix does not own. If that sweep runs again it can re-introduce the
wrong date; the durable fix is for the sweep to read `postedDate` from the page's
own markup instead of stamping scrape time.

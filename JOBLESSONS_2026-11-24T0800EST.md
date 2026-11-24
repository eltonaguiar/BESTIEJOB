# JOBLESSONS_2026-11-24T0800EST — hourly Toronto ServiceNow / Salesforce scan

## Run meta
- Run time: Tuesday 2026-11-24 08:00 EST (13:00 UTC)
- Repo: eltonaguiar/BESTIEJOB, branch `main`
- Previous hourly commit: `5ae11cea` chore(jobs): add 1 verified fresh Toronto Salesforce job (Wipro, 2026-11-24T07:00EST)
- Board state at run start: README.md clean at HEAD; jobs.json = 5,625 listings (6,020 URLs incl. README)
- Net-new verified fresh Toronto ServiceNow/Salesforce jobs this hour: **0**
- Rows merged to README.md: **0** (README unchanged)

## Sources scanned
| Source | Detail | Result |
|---|---|---|
| raw/adzuna_sn_toronto.json | Adhuna ServiceNow Toronto harvest (07:02 EST) | 91 results, most with no `created` date |
| raw/adzuna_sf_toronto.json | Adzuna Salesforce Toronto harvest (07:02 EST) | results, most with no `created` date |
| raw/live_jobs-data.json | 4,972-job feed (07:23 EST) | parsed, deduped |
| raw/linkedin_guest_2026-11-24.json | 4 fresh LinkedIn guest results | parsed, deduped |
| raw/dice_spectra.json | Dice spectra | non-JSON, not parsed |
| Workday CXS (wd2/wd3/wd4/wd5) | BMO, TD, CIBC, Interac, Manulife, Salesforce, SunLife | all returned "Requested page not found" Application_Error — empty stubs |
| Web search (Glassdoor/Indeed/LinkedIn) | ServiceNow/Salesforce Toronto queries | detail pages behind Cloudflare/login, not verifiable from this host |

## Dedup math
- Existing URLs in jobs.json + README.md: 6,020
- Candidate postings surfaced after dedup: 82
- Of the 82: **none** carried a posted date of 2026-11-23 or 2026-11-24; freshest dated were 2026-11-20 / 2026-11-21
- Many candidates were non-Toronto (Québec, Calgary, Canada-wide) or sales-only roles (Sales Executive, Account Exec, Sales Director, CRM Sales) — not Platform Admin / Platform Developer I / ServiceNow Developer I
- 0 candidates passed the "fresh + Toronto + SN/SF platform role + live-verified" bar

## Employer-direct checks (known partners / technical companies)
- Rogers (jobs.rogers.com Technology): no platform roles
- Bell / Ateko: careers portal client-side rendered, not enumerable from this host; recent LinkedIn roles older / already considered
- TD / BMO / CIBC / Scotiabank Workday CXS: 404 stubs; TD Senior Solution Architect ServiceNow already on board via Built In Toronto; Scotiabank Salesforce Developer JR265640 closed ("not accepting any further applicants")
- ServiceNow Careers Ontario: no fresh Platform Admin / Developer I roles
- Government of Canada Job Bank: postings surfaced were September–October 2026 (stale)
- Manulife / Interac / SunLife Workday CXS: 404 stubs

## Outcome
- Net-new verified fresh jobs: **0** — nothing merged to README.md
- README.md unchanged → GitHub Pages `pages.yml` not re-triggered (it deploys on push to `public/**` or `README.md`); page remains at last successful deploy
- This run recorded as a JOBLESSONS-only commit (`[skip ci]`), matching the 05:00/06:00 "0 net-new" pattern

## Lessons / patterns for future agents
1. Adzuna raw harvests often carry postings with no `created` date; without a posted date a row cannot be certified "fresh" and must not be added to the board.
2. Workday CXS employer-direct URLs (wd2/wd3/wd4/wd5) for Canadian banks frequently return "Requested page not found" Application_Error — treat as empty, do not retry as a job source.
3. Indeed and LinkedIn detail pages are behind Cloudflare from this host; liveness can only be established via the current search listing + snippet, and such rows must be asterisked with the discovery date per board policy.
4. The 07:00 EST scan found 1 fresh role (Wipro Salesforce Marketing Cloud Senior Developer, posted 11-23, verified HTTP 200 on careers.wipro.com) — employer-direct careers pages remain the most reliable fresh-source channel, more so than aggregators.
5. Sales-only / CRM-sales / Account Executive matches surface constantly under ServiceNow/Salesforce keywords; filter them out unless the user explicitly wants sales roles.
6. Non-Toronto matches (Québec, Calgary, Canada-wide) dominate the Canada-wide SN/SF keyword harvest; scope strictly to Toronto/Ontario for this board unless broadening is requested.
7. When 0 net-new jobs are found, still commit a JOBLESSONS file so the hourly run is recorded, rather than skipping the commit.

## Verification
- `parse_candidates.py` deduped 82 candidate URLs against jobs.json + README.md (6,020 URLs) and filtered for SN/SF + Toronto/Ontario/Canada.
- No candidate was dated 2026-11-23 or 2026-11-24; none were live-verified employer-direct postings.

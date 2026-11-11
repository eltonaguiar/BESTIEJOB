# Plan: exhaustive ServiceNow Developer roles from sources that do NOT feed bestiejob

Date: 2026-11-11. Author: Buffy.

## 1. Definition of done

A role counts as **active** when (a) its page returns HTTP 200 right now, (b) the
title is a ServiceNow developer/platform role (not a job *at* ServiceNow and not
a sales job), and (c) the posting states either an absolute posted date or, where
the source never publishes one, is confirmed live and still listed in the
source's own current results. Rows with an absolute date go to the inbox;
undated-but-live rows go in the report marked `live, undated` and are not
published as dated board rows.

## 2. Sources already feeding bestiejob (excluded from the sweep)

Confirmed from the scanners and workflows in this repo:

- Employer ATS sweep: Greenhouse, Lever, Workday CXS, SmartRecruiters, Ashby (by slug list)
- Agency boards integrated 2026-11-11: CareerBeacon, Dice, Procom, Built In Toronto
- Aggregators in the hourly scan and LinkedIn sweep workflows
- Adzuna (keys absent), LinkedIn/Indeed (Cloudflare), Jooble (403)

Anything below appears in none of those paths.

## 3. New sources, by how tractable they are

### Tier 1 — structured API with dates (highest value)
| Source | Endpoint | Date field |
| --- | --- | --- |
| Job Bank Canada | `jobbank.gc.ca/jobsearch/jobsearch?searchstring=servicenow` + detail pages | JSON-LD `datePosted` where present |
| GC Jobs (federal public service) | `emploisfp-psjobs.cfp-psc.gc.ca` search | closing date + posted date |
| RemoteOK | `remoteok.com/api` (JSON) | `date` (ISO) |
| Remotive | `remotive.com/api/remote-jobs?search=servicenow` | `publication_date` |
| Himalayas | `himalayas.app/jobs/api` | `pubDate` |
| We Work Remotely | category RSS | `pubDate` |
| Hacker News "Who is hiring" | Algolia `search?tags=comment,story_<id>` | month thread |

### Tier 2 — server-rendered HTML (parseable, dates vary)
| Source | Why new |
| --- | --- |
| Ontario GoJobs | provincial postings, never scanned here |
| Careerjet Canada | aggregates agency reqs not on the four wired boards |
| Jobrapido Canada | same, different inventory |
| Monster.ca | not in any current scanner |
| Jobs.ca / IFG network | where IFG and other finance-led agencies publish |

### Tier 3 — blocked or JS-only (documented, not harvested)
Glassdoor, Indeed, LinkedIn (Cloudflare), Talent.com, Eluta, TEKsystems,
Randstad search results (JS), Wellfound/Otta (auth), Adzuna (no keys),
ServiceNow Community job board (login-gated).

### Tier 4 — employer-direct, no aggregator involved
ServiceNow partners and Canadian employers whose Workday/Taleo tenants are not
in the slug list: GlideFast, Crossfuze, NewRocket, Levio, Trianz, Sparkrock,
CGI, RBC, TD, BMO, CIBC, Scotiabank, Manulife, Sun Life, TELUS, Rogers, Bell,
Ontario Health, UHN, City of Toronto, Government of Ontario. Each needs its
tenant/site pair discovered before it can be queried.

## 4. Execution steps

1. Probe every Tier-1 endpoint; keep the ones that answer with real postings.
2. Probe Tier-2 search pages; extract links, fetch details, keep absolute dates.
3. Record per-source status (200 / 403 / JS-only / no results) so the next agent
   does not repeat dead work.
4. Filter: title must match `servicenow` AND a role word (developer, engineer,
   consultant, architect, admin, analyst, platform); drop jobs *at* ServiceNow
   unless the role itself is ServiceNow work; drop vendor sales titles.
5. Dedupe by normalised URL against `jobs.json` (5,376 rows) and between sources.
6. Verify liveness of every kept row with a fresh request; drop 404/410.
7. Write `reports/sn_dev_roles_2026-11-11.md` + JSON; date-bearing rows also go
   to `inbox/agency-board--<date>--v1.md` for the normal merge.

## 5. Acceptance criteria

- Every listed role answers HTTP 200 at report time.
- No row without a date is presented as dated.
- Per-source status table shows what was tried and what failed, with the reason.
- No duplicate of an existing bestiejob row.
- Numbers in the report are produced by the run, not estimated.

## 6. Known risks

- Staffing mirrors: the same req appears on Careerjet, Jobrapido and the agency's
  own site; URL dedupe will not catch those, so title+company+city is used too.
- Workday `postedOn` is relative ("Posted 30+ Days Ago"); it is never converted.
- Federal/provincial pages often close applications while leaving the page up;
  liveness is checked, but "closing date passed" is also flagged.

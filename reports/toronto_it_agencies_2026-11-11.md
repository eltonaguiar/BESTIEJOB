# Toronto IT recruiting agencies: what is actually harvestable

Date: 2026-11-11. Companion to `config/agency_boards.json` and
`scripts/agency_board_scan.py`.

Checked 42 agencies and 26 job boards by fetching
their real careers pages (not by asking a search engine what they claim to
have). A board only counts as usable if a **posting page states its own posting
date** — a search-results snippet or a relative "3 days ago" is not a date and
never becomes a row.

## 1. Integrated into the board (4 feeds)

| Feed | Adapter | Link source | Evidence | Enabled |
| --- | --- | --- | --- | --- |
| CareerBeacon | `jsonld` | search (?q=) | 5/5 detail pages returned JSON-LD datePosted; Canadian board, provincial coverage | yes |
| Dice | `dice` | search | 5/5 detail pages carried postedDate + jobLocation.displayName in page payload | yes |
| Procom | `jsonld` | sitemap.xml (298 URLs) | detail pages carry JSON-LD datePosted; list page exposes only one link | yes |
| Built In Toronto | `page_text` | search | 5/5 detail pages carried a literal 'Posted <date>'; location from page text | yes |

Today's first harvest: 4 dated, in-scope rows (3 Toronto, 1 New Brunswick) —
see `inbox/agency-board--2026-11-11--v1.md`.

## 2. Agency boards that answer, but need per-site work

| Agency | Platform | Job links seen | "service now" mentions | Toronto mentions | Endpoint |
| --- | --- | --- | --- | --- | --- |
| Michael Page Canada | - | 54 | 0 | 5 | `https://www.michaelpage.ca/` |
| Randstad Canada | - | 35 | 0 | 7 | `https://www.randstad.ca/` |
| Procom | bullhorn | 20 | 0 | 49 | `https://myprocom-portal.procomservices.com/jobs` |
| Stack IT Recruitment | - | 9 | 0 | 19 | `https://stackitrecruitment.com/jobs/` |
| Arrow Workforce | - | 7 | 0 | 0 | `https://arrowworkforce.com/jobs/` |
| Hays Canada | - | 6 | 0 | 0 | `https://www.hays.ca/` |
| Artech | - | 5 | 0 | 0 | `https://www.artech.com/careers/consultant-jobs` |
| TEKsystems | phenom | 4 | 0 | 0 | `https://careers.teksystems.com/us/en` |
| Alldus | - | 4 | 67 | 0 | `https://alldus.com/` |
| Insight Global | - | 3 | 0 | 0 | `https://insightglobal.com/jobs` |
| Core Resources | - | 2 | 0 | 3 | `https://www.coreresources.ca/` |
| Robert Half Canada | - | 0 | 0 | 1 | `https://www.roberthalf.com/ca/en` |
| Akkodis Canada | - | 0 | 0 | 0 | `https://www.akkodis.com/en-ca` |
| Levio | - | 0 | 7 | 1 | `https://levio.ca/` |

Randstad and TEKsystems are the notable gaps: both carry real Toronto
ServiceNow/Salesforce contract work, but their search pages assemble the result
list client-side, so nothing can be read without a headless browser. They are
listed in the config as `enabled: false` with the reason, rather than silently
dropped.

## 3. Agencies with no public job board at the usual paths

S.i. Systems, Altis Recruitment, Quantum Technology Recruiting, isgSearch, Dean Group, Options Consulting Solutions, Drake International, Futuretek IT, Bay Street Staffing, Mace Staffing, PTC Recruiting, Staffworks, Plan IT Search, Kovasys, DevTalent, Experis Canada, Robert Walters Canada, Eagle Professional, Ian Martin, Tundra Technical, Prime Hires, Brainhunter, ProViso, Systematix, Maplesoft Group, Donna Cona, BeachHead, Huntel Global

These recruit through LinkedIn, jobs.ca, Indeed, or a recruiter directly. The
absence of a board is not evidence they have no vacancies — it means there is
nothing for a scanner to read.

### International Financial Group (IFG), specifically

`ifg.ca` did not resolve (DNS error) from this host. IFG's live postings are
visible through the Jobs.ca network under
`jobs.ca/ifg-international-financial-group` (verified: dated Toronto rows such as
Business Systems Analyst Capital Markets General Ledger, posted 2026-11-04), and
applications route to LinkedIn. IFG is a finance/accounting-led firm that also
carries IT and capital-markets technology roles, so it is worth checking by
hand even though it has no scannable board.

## 4. Job boards probed (beyond the agencies)

| Board | HTTP | Platform | Job links | Dated markers | SN |
| --- | --- | --- | --- | --- | --- |
| CareerBeacon | 200 | - | 25 | 0 | 18 |
| Eluta | 200 | workday | 0 | 0 | 82 |
| Talent.com | 200 | workday | 2 | 0 | 165 |
| Jobs.ca | 404 | - | 0 | 0 | 0 |
| TorontoJobs.ca | 404 | - | 0 | 0 | 0 |
| TechJobs.ca | 200 | - | 0 | 0 | 24 |
| Built In Toronto | 200 | - | 122 | 9 | 135 |
| Dice | 200 | - | 0 | 19 | 280 |
| Monster.ca | 200 | - | 67 | 0 | 0 |
| Jobillico | 404 | - | 0 | 0 | 0 |
| Wowjobs | 200 | - | 5 | 0 | 0 |
| CharityVillage | 404 | - | 0 | 0 | 0 |
| Careerjet CA | 200 | - | 0 | 0 | 0 |
| Jooble CA | 403 | - | 0 | 0 | 3 |
| Jobrapido CA | 200 | - | 0 | 0 | 122 |
| Remotive API | 200 | - | 0 | 0 | 0 |
| WeWorkRemotely API | 200 | - | 2 | 0 | 0 |
| RemoteOK API | 200 | lever | 0 | 0 | 0 |
| Jobspresso | 200 | - | 9 | 0 | 15 |
| NoDesk | 200 | - | 0 | 0 | 0 |
| Hacker News hiring | 200 | - | 0 | 0 | 55 |
| Jobgether CA | 200 | bullhorn | 0 | 0 | 0 |
| Sercanto CA | 404 | - | 0 | 0 | 4 |
| Adzuna CA | 400 | - | 3 | 0 | 0 |
| Glassdoor CA | 200 | - | 0 | 0 | 433 |
| Indeed CA | 200 | smartrecruiters | 0 | 0 | 434 |

Notable: Built In Toronto, Dice and CareerBeacon are the three that both answer
and expose dates. Glassdoor and Indeed return 200 but their listings are
JavaScript-rendered, and Jooble returns 403. Adzuna's public search page returns
400 (its API is the supported path and its keys are absent from this host).

## 5. Worth watching (no board verified yet)

Additional Toronto-market IT staffing firms named in this pass but not yet
proven to expose a dated feed: CorGTA, The Select Group, Judge Group Canada,
Planet Technology, Motion Recruitment, Robert Half Technology, Randstad Digital,
Experis, Akkodis, Hays Technology, Michael Page Technology, Robert Walters,
Altis Recruitment, Quantum Technology Recruiting (QTR), isgSearch, MIS
Consultants, Dean Group, Options Consulting Solutions, Arrow Workforce, Drake
International, Staffworks, Core Resources, Plan IT Search, Kovasys, DevTalent,
Stack IT Recruitment, Agile Staffing Solutions, Futuretek, Bay Street Staffing,
Mace Staffing, PTC Recruiting, Tundra Technical, Maplesoft Group, Donna Cona,
ProViso, Systematix, Brainhunter, BeachHead, Eagle Professional Resources,
Huntel Global, Ian Martin, Alldus, Levio, Prime Hires.

The next step for any of them is the same test used here: open one posting, and
keep the agency only if that posting states an absolute date.

## 6. Running it

    python3 scripts/agency_board_scan.py --dry-run
    python3 scripts/agency_board_scan.py --max-per-source 60 --workers 10
    python3 tools/jobs_merge_inbox.py --dry-run

## 7. Rules the adapters enforce

1. An absolute `datePosted` from the posting, or the row does not exist.
2. Location from the posting's own address; `USA`/`United States` rejects.
3. The employer comes from the posting or the card, never the board's name.
4. A job **at** ServiceNow is not a ServiceNow role — drop employer-only matches.
5. Vendor sales titles are excluded; the board is technical.

# Agency & job-portal reference (for any agent working this board)

Generated 2026-11-11 by Buffy. Machine-readable twin: `config/agency_portals.json`.
Scanner: `scripts/agency_board_scan.py`. Config: `config/agency_boards.json`.

**The one rule.** A portal is only harvestable if a *posting page states an
absolute posting date* (`YYYY-MM-DD`). A search-result snippet, a relative
"3 days ago", or a date scraped from the page footer is not a date. If a source
cannot prove a date on the posting itself, it stays `enabled: false` with a
reason — it does not get fabricated rows.

**Second rule.** Location comes from the posting's own address, never from the
search scope. `USA`/`United States` rejects. Ambiguous city names (London,
Cambridge, Windsor, Richmond, Surrey, Victoria, Waterloo, Hamilton, Kingston)
need a province or "Canada" before they count.

**Third rule.** A job *at* ServiceNow/Salesforce is not a ServiceNow/Salesforce
role, and vendor sales titles are not technical roles.

## A. Wired in and proven (enabled)

| Source | Adapter | Discovery | Detail fetch | Search endpoint |
| --- | --- | --- | --- | --- |
| CareerBeacon | `jsonld` | search | HTTP | `https://www.careerbeacon.com/en/search?q=servicenow,` |
| Dice | `dice` | search | HTTP | `https://www.dice.com/jobs?q=servicenow&location=Toro` |
| Procom | `jsonld` | search | HTTP | `https://myprocom-portal.procomservices.com/jobs` |
| Built In Toronto | `page_text` | search | HTTP | `https://builtintoronto.com/jobs?search=servicenow, h` |

`adapter` is how that board exposes its date: `jsonld` = JSON-LD `datePosted`,
`dice` = `postedDate` in the page payload, `page_text` = literal "Posted <date>".

## B. Disabled on purpose

| Source | Why |
| --- | --- |
| TEKsystems (Phenom) | Search results never render: headless Chrome loads only a jobwidget settings XHR and zero postings; `sitemap.xml` 303-redirects; `robots.txt` disallows the widget paths. Real Toronto SN/SF contract roles exist there, so it needs a logged-in/cookie-bearing session or manual checking. |
| Eluta | Search page serves no server-rendered job links. |
| Talent.com | Same: listing is client-side. |

## C. Agencies whose boards answer (probe results)

| Agency | Platform | HTTP | Endpoint | Yield seen |
| --- | --- | --- | --- | --- |
| Michael Page Canada | - | 200 | `https://www.michaelpage.ca/` | 54 links / 0 SN / 5 TO |
| Randstad Canada | - | 200 | `https://www.randstad.ca/` | 35 links / 0 SN / 7 TO |
| Procom | bullhorn | 200 | `https://myprocom-portal.procomservices.com/jobs` | 20 links / 0 SN / 49 TO |
| Stack IT Recruitment | - | 200 | `https://stackitrecruitment.com/jobs/` | 9 links / 0 SN / 19 TO |
| Arrow Workforce | - | 200 | `https://arrowworkforce.com/jobs/` | 7 links / 0 SN / 0 TO |
| Hays Canada | - | 200 | `https://www.hays.ca/` | 6 links / 0 SN / 0 TO |
| Artech | - | 200 | `https://www.artech.com/careers/consultant-jobs` | 5 links / 0 SN / 0 TO |
| Alldus | - | 200 | `https://alldus.com/` | 4 links / 67 SN / 0 TO |
| TEKsystems | phenom | 200 | `https://careers.teksystems.com/us/en` | 4 links / 0 SN / 0 TO |
| Insight Global | - | 200 | `https://insightglobal.com/jobs` | 3 links / 0 SN / 0 TO |
| Core Resources | - | 200 | `https://www.coreresources.ca/` | 2 links / 0 SN / 3 TO |
| Akkodis Canada | - | 200 | `https://www.akkodis.com/en-ca` | 0 links / 0 SN / 0 TO |
| Levio | - | 200 | `https://levio.ca/` | 0 links / 7 SN / 1 TO |
| Robert Half Canada | - | 200 | `https://www.roberthalf.com/ca/en` | 0 links / 0 SN / 1 TO |

## D. Agencies with no public board at the usual paths

Altis Recruitment, Bay Street Staffing, BeachHead, Brainhunter, Dean Group, DevTalent, Donna Cona, Drake International, Eagle Professional, Experis Canada, Futuretek IT, Huntel Global, Ian Martin, Kovasys, Mace Staffing, Maplesoft Group, Options Consulting Solutions, PTC Recruiting, Plan IT Search, Prime Hires, ProViso, Quantum Technology Recruiting, Robert Walters Canada, S.i. Systems, Staffworks, Systematix, Tundra Technical, isgSearch

Recruit via LinkedIn, jobs.ca, Indeed, or a recruiter directly. Note **IFG
(International Financial Group)**: `ifg.ca` does not resolve here; its live rows
surface on `jobs.ca/ifg-international-financial-group` and apply via LinkedIn.

## E. Job boards probed

| Board | HTTP | Platform | Links | Date markers | SN |
| --- | --- | --- | --- | --- | --- |
| Built In Toronto | 200 | - | 122 | 9 | 135 |
| Monster.ca | 200 | - | 67 | 0 | 0 |
| CareerBeacon | 200 | - | 25 | 0 | 18 |
| Jobspresso | 200 | - | 9 | 0 | 15 |
| Wowjobs | 200 | - | 5 | 0 | 0 |
| Adzuna CA | 400 | - | 3 | 0 | 0 |
| Talent.com | 200 | workday | 2 | 0 | 165 |
| WeWorkRemotely API | 200 | - | 2 | 0 | 0 |
| Careerjet CA | 200 | - | 0 | 0 | 0 |
| CharityVillage | 404 | - | 0 | 0 | 0 |
| Dice | 200 | - | 0 | 19 | 280 |
| Eluta | 200 | workday | 0 | 0 | 82 |
| Glassdoor CA | 200 | - | 0 | 0 | 433 |
| Hacker News hiring | 200 | - | 0 | 0 | 55 |
| Indeed CA | 200 | smartrecruiters | 0 | 0 | 434 |
| Jobgether CA | 200 | bullhorn | 0 | 0 | 0 |
| Jobillico | 404 | - | 0 | 0 | 0 |
| Jobrapido CA | 200 | - | 0 | 0 | 122 |
| Jobs.ca | 404 | - | 0 | 0 | 0 |
| Jooble CA | 403 | - | 0 | 0 | 3 |
| NoDesk | 200 | - | 0 | 0 | 0 |
| RemoteOK API | 200 | lever | 0 | 0 | 0 |
| Remotive API | 200 | - | 0 | 0 | 0 |
| Sercanto CA | 404 | - | 0 | 0 | 4 |
| TechJobs.ca | 200 | - | 0 | 0 | 24 |
| TorontoJobs.ca | 404 | - | 0 | 0 | 0 |

## F. Toronto agencies worth checking next

CorGTA, The Select Group, Judge Group Canada, Planet Technology, Motion
Recruitment, Robert Half Technology, Randstad Digital, Experis, Akkodis, Hays
Technology, Michael Page Technology, Robert Walters, Altis Recruitment, Quantum
Technology Recruiting (QTR), isgSearch, MIS Consultants, Dean Group, Options
Consulting Solutions, Arrow Workforce, Drake International, Staffworks, Core
Resources, Plan IT Search, Kovasys, DevTalent, Stack IT Recruitment, Agile
Staffing Solutions, Futuretek, Bay Street Staffing, Mace Staffing, PTC
Recruiting, Tundra Technical, Maplesoft Group, Donna Cona, ProViso, Systematix,
Brainhunter, BeachHead, Eagle Professional Resources, Huntel Global, Ian Martin,
Alldus, Levio, Prime Hires, Kforce, Apex Systems, Insight Global, S.i. Systems,
Akkodis, Constellation IT, Allegis Group.

Test any of them the same way: open one posting and look for an absolute date.

## G. Lists other agents already left in this repo

| File | Size | Domains | What it carries |
| --- | --- | --- | --- |
| `Buffy-2026-10-31-world-forum-portals.md` | 15693 B | 9 | adzuna.ca, aelumconsulting.com, careers.wipro.com, hiringcafe.com, jobs.smartrecruiters.com, myprocom-portal.procomservices.com |
| `JOB_SOURCES_STATUS.md` | 5728 B | 0 | — |
| `docs/TOP_JOB_SITES_CANADA__kilo-auto.md` | 7619 B | 1 | eltonaguiar.github.io |
| `docs/CANADIAN_JOB_SITES__nemotron.MD` | 15357 B | 0 | — |
| `JOB_AGGREGATOR_FINDINGS.md` | 9952 B | 3 | api.lever.co, boards-api.greenhouse.io, github.com |
| `raw/fanout/model-groq-openai-gpt-oss-120b-agencies.md` | 48 B | 0 | — |
| `raw/fanout/model-deepinfra-meta-llama-meta-llama-3-1-8b-instruct-agencies.md` | 74 B | 0 | — |
| `raw/fanout/model-mistral-ministral-8b-2512-agencies.md` | 2927 B | 11 | accenture.com, allegisglobalsolutions.com, allegisgroup.com, apexsystems.com, cognizant.com, constellationit.com |
| `raw/fanout/model-ollama-llama3-3-70b-agencies.md` | 50 B | 0 | — |

What is additive there: `Buffy-2026-10-31-world-forum-portals.md` carries
Wipro/SmartRecruiters/Procom/Hiring Cafe entry points; the mistral fan-out file
has the Allegis/Apex/Cognizant/Robert Half family; `scrapers/recruiting_firms_scraper.js`
holds a hardcoded firm list (Altis, Experis, Hays, Insight Global, Kforce,
Procom, Randstad, Robert Half, S.i. Systems, TEKsystems). None of them record
whether a posting is harvestable, which is what this file adds.

## H. Contributing a new portal

1. Open one posting and find its absolute date (JSON-LD `datePosted` preferred).
2. Add it to `config/agency_boards.json` with the right `adapter`.
3. `python3 scripts/agency_board_scan.py --only <name> --dry-run`
4. Only after it yields dated, in-scope rows: enable it and re-run the full scan.
5. If it yields nothing, leave `enabled: false` and write `why_disabled`.

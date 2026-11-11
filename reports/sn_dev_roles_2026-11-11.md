# ServiceNow developer roles outside the current feeds

Verified 2026-11-11 01:32 local. Every row below was fetched
in this run; the date column is the posting's own `datePosted`. Nothing here
duplicates a row already in `jobs.json`.

**9 live roles** (4 with an absolute posted date, 5 live but undated), 4 closed or unreachable.

## Live roles with an absolute posting date

| Posted | Role | Employer | Location | Status | URL |
| --- | --- | --- | --- | --- | --- |
| 2026-11-05 | Software Developer - Senior | Akkodis | Toronto, Ontario, CA | live 200 | https://www.jobleads.com/ca/job/software-developer-senior--toron |
| 2026-10-17 | Senior ServiceNow Developer (ITOM) | Systematix | Remote, Canada | live 200 | https://www.jobs.ca/systematix/jobs/senior-servicenow-developer- |
| 2026-10-13 | Consultant, servicenow developer | KPMG Canada | Toronto, ON, CA | live 200 | https://www.jobillico.com/en/job-offer/kpmg-canadaeLtlFq/consult |
| 2026-09-01 | ServiceNow Developer / ServiceNow Architect - Remote (Canada PST | Saransh Inc | Remote, Canada | live 200 | https://www.jobs.ca/saransh-inc/jobs/servicenow-developer-servic |

## Live, but the source publishes no date

Real and currently listed, but not eligible to become a dated board row.

| Role | Employer | Location | Status | URL |
| --- | --- | --- | --- | --- |
| — | Lightspeed Commerce | Toronto, ON | live 200 | https://www.simplyhired.ca/job/YjQcAKOlTkWaMXOa5CB23HMAy2IS19PSG |
| Senior ServiceNow Developer (ITOM) - Systematix | Systematix | Remote, Canada | live 200 | https://systematix.com/opportunity/senior-servicenow-developer-i |
| Senior ServiceNow Developer – Remote · Canada | Hanalytica GmbH | Hanalytica | Remote, Canada | live 200 | https://www.jobs.ca/hanalytica-gmbh/jobs/senior-servicenow-devel |
| — | Maplesoft Group | Remote, Canada | live 200 | https://www.workopolis.com/jobsearch/viewjob/T7s0oCYEH_yoNlqKUg- |
| SYSTEMS INTEGRATOR 1 (SERVICENOW DEVELOPER) Job Details | City o | City of Toronto | Toronto, ON | live 200 | https://jobs.toronto.ca/jobsatcity/job/Toronto-SYSTEMS-INTEGRATO |

## Closed or unreachable

| Employer | Status | Evidence | URL |
| --- | --- | --- | --- |
| Brookfield | 410 | This role is no longer accepting applications. You can still read the original | https://scoutify.com/companies/brookfield/jobs/3116423 |
| Real Ventures | 200 | font-weight="600" font-size="14px" color="text.dark" class="sc-aXZVg dkjSzf">Thi | https://community.getro.com/companies/real-ventures/jobs/989 |
| HCLTech | 200 | has expired This position at HCLTech is no longer accepting applications. The or | https://www.jobs.ca/hcltech/jobs/servicenow-developer-remote |
| Adecco | 410 | http 410 | https://www.adecco.com/en-ca/job-search/servicenow-developer |

## Sources attempted that produced no roles

Recorded so the next agent does not repeat the work.

| Source | Result | Roles |
| --- | --- | --- |
| Job Bank Canada | excluded — already feeds bestiejob | — |
| GoJobs Ontario | excluded — already feeds bestiejob | — |
| SmartRecruiters / Greenhouse / Lever / Ashby | excluded — already feeds bestiejob | — |
| GC Jobs (federal) | http 404 at both endpoints | 0 |
| RemoteOK | http 200, 100 listings, 0 ServiceNow titles | 0 |
| Remotive | http 200, 13 listings, 0 ServiceNow | 0 |
| Himalayas | http 200, paginated 5x100, 0 ServiceNow titles | 0 |
| Jobboom (QC) | http 200 but keyword ignored; 0 ServiceNow anchors | 0 |
| We Work Remotely | http 200, category feed, 0 ServiceNow | 0 |
| Hacker News who-is-hiring | thread 22665398, 0 ServiceNow comments | 0 |
| Reddit r/servicenow | http 403 (blocked) | 0 |
| Careerjet CA | http 200 but no job links in HTML (client-side) | 0 |
| Jobrapido CA | http 200, 122 mentions, 0 individual job links | 0 |
| Monster.ca | http 200, 0 ServiceNow links | 0 |
| Jobs.ca search | http 404 | 0 |

## How to reproduce

    python3 scripts/sn_dev_source_sweep.py --verify
    # JSON: reports/sn_dev_roles_2026-11-11.json

The candidate URLs in this report were found by web search and then fetched
individually; the sweep script covers the machine-readable sources only.

## Limits

- Nine sources in the sweep returned nothing; that is a real result, not a skipped step.
- Indeed, LinkedIn, Glassdoor and Jooble block this host, so their inventory is absent.
- Three employers (KPMG, Brookfield, Lightspeed) publish through Indeed/site widgets;
  the dates shown are from the posting's structured data, not a search snippet.
- No row here has been merged into README yet; that is the normal inbox merge step.

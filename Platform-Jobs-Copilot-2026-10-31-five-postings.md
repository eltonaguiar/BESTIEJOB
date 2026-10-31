# Five supplied postings: source checks

Agent: Copilot, an AI assistant using Copilot SDK in VS Code.
Checked: 2026-10-31 06:18 UTC.

All five supplied URLs are covered in the [README coverage table](README.md#supplied-five-postings-coverage-october-31). One independently verified platform developer vacancy is added; two vendor infrastructure roles are retained separately, one recruiter lead is unverified, and one mirror appears to duplicate an existing contract.

| Posting | Source evidence | Disposition |
|---|---|---|
| [ServiceNow Staff Database Engineer](https://careers.servicenow.com/jobs/744000154789179/staff-database-engineer/) | [Official public ATS](https://api.smartrecruiters.com/v1/companies/ServiceNow/postings/744000154789179): releasedDate October 9; Toronto hybrid, two office days; PostgreSQL, transactions, performance and DevOps | Vendor database engineering; not CSA/CAD platform development. Covered, not counted in selected platform jobs. |
| [Tekgence ServiceNow Developer](https://www.jobs.ca/tekgence-inc/jobs/servicenow-developer-toronto-on-173ede1d1492) | HTTP 403 protection page; exact-match public search did not establish an original employer posting | User's Toronto/October 16 claims retained but unverified. No inferred terms, certification, vacancy status or bypass. |
| [ServiceNow Staff Site Reliability Engineer](https://careers.servicenow.com/jobs/744000156040224/staff-site-reliability-engineer/) | [Official public ATS](https://api.smartrecruiters.com/v1/companies/ServiceNow/postings/744000156040224): releasedDate October 16; Toronto hybrid; Kubernetes, cloud-native operations, SLOs and Python/Go/Java/Ruby | Vendor SRE engineering; not CSA/CAD platform development. Covered, not counted in selected platform jobs. |
| [National Bank FSO-ServiceNow Developer](https://emplois.bnc.ca/en_CA/careers/JobDetail/MONTREAL-Quebec-Canada-P5I27-DEVELOPPEUR-PRINCIPAL/33633) | Employer page: posting date 14-Oct-2026, job 33633, Montreal hybrid, permanent full-time, French; five years development, FSO, JavaScript/Flow Designer/GlideScript, REST/SOAP; CSA/CAD major assets; Apply links | New verified selected row #84. No application submitted. |
| [Brookfield / Handshake 11747479](https://app.joinhandshake.com/public/jobs/11747479) | Public JobPosting JSON-LD: datePosted **October 22, 10:11:50 UTC**, validThrough **November 21, 10:11:50 UTC**, Toronto, full-time; same November 2026-June 2027 contract and duties as earlier employer record | Apparent duplicate of README #07. October 22 is nine calendar days before this check, not six. Mirror expiry is not a confirmed employer application deadline. |

## Brookfield status limitation

The earlier employer Workday record for [R2053249](https://brookfield.wd5.myworkdayjobs.com/brookfield/job/Toronto-Ontario/ServiceNow-Developer--CONTRACT-ROLE-_R2053249-1) had startDate October 20 and canApply=true when checked in the prior round. Two current attempts at its public CXS detail returned HTTP 200 non-JSON content, so current employer acceptance could not be confirmed. This is not proof of closure or continued availability. Handshake's current JSON-LD proves what the mirror states, not the employer's current hiring decision. No duplicate count or changed employer date is introduced.

## Validation

Public ATS metadata for both vendor roles and employer page text/application links for National Bank checked. Brookfield mirror metadata inspected. README selected rows remain sequential and unique (#1-84), all prior 83 selected rows and application documentation preserved, all five supplied links present, and vendor/unverified/duplicate entries excluded from the selected count. Documentation only; no application code, build or tests required. Default-branch publication verified after merge.

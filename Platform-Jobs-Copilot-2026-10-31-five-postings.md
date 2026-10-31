# Five supplied postings: source checks

Agent: Copilot, an AI assistant using Copilot SDK in VS Code.
Checked: 2026-10-31 06:17 UTC.

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

Public ATS metadata for both vendor roles and employer page text/application links for National Bank and FX checked. Brookfield mirror metadata inspected. README selected rows remain sequential and unique (#1-85), all prior 83 selected rows and application documentation preserved, all supplied links present, and vendor/unverified/duplicate entries excluded from the selected count. Documentation only; no application code, build or tests required. Default-branch publication verified after merge.

## Additional supplied leads

The subsequent user lists are also covered in the README, without converting search pages or relative mirror ages into verified employer dates.

- **New verified Canada-remote role:** [FX Innovation / Ateko ServiceNow Platform Administrator 526446](https://www.fxinnovation.com/en/jobs/526446), permanent full-time, application form present. Must reside in Canada; French and English required; support rotation 24/7, two weeks out of five. Two years administration, JavaScript, Flow Designer, ACLs, Business Rules and CMDB. Original posting date and CSA/CAD requirements not stated. Added as #85. The supplied [Quebec October 30 mirror](https://jobs-search.org/platform-administrator_quebec-c117954/2026-10-fxinnovation_i4267273596) returned 403; the [Toronto October 29 mirror](https://jobs-search.org/system-administrator_toronto-c117072/2026-10-fxinnovation_i4266102140) is retained as an unverified alias, not a second counted job.
- **QuoteMachine:** [supplied board](https://www1.communitech.ca/jobs?page=5) and [specific indexed mirror](https://www1.communitech.ca/companies/quotemachine/jobs/97699210-servicenow-developer) returned 403. Toronto/Ottawa and "Today" claims unverified; no two-job count.
- **IDR:** [individual DeveloperJobs mirror](https://developerjobs.io/job/sr-servicenow-developer-1043019) returned 200 with Atlanta remote description and "2d ago", not the supplied "5h ago". Search-discovered [original recruiter URL](https://jobs.idr-inc.com/job/503448-sr-servicenow-developer-atlanta-georgia/) returned 404. Current employer status remains unconfirmed; a stale original or indexed URL is not evidence of an open role.
- **Deloitte Cincinnati:** [supplied mirror](https://wfh.hstn.me/job/servicenow-administrator-remote) disconnected during retrieval. No original source established.
- **Spark Tek CMDB architect / Ares Enterprise developer:** [ZipRecruiter Maryland search](https://www.ziprecruiter.com/Jobs/Remote-Servicenow/--in-Maryland) is not two individual job links. Locations, dates and status remain supplied claims.
- **Early Warning Services application administrator:** [Dice search](https://www.dice.com/jobs/q-servicenow+administrator-jobs) has no supplied requisition. Not promoted.
- **SAIC inventory control associate / unnamed Daytona Beach ITSM admin:** [Dice search](https://www.dice.com/jobs/q-%22ServiceNow%22-jobs) has no supplied individual links. Inventory duties are not presumed platform development, and no employer is invented for the ITSM role.

Final selection after the FX addition: **85 distinct links**, 64 ServiceNow-related (29 Canada-associated, 35 U.S. fallbacks) and 21 Salesforce-related. Only National Bank and FX are new selected rows in this follow-up. The original 83 remain reviewable.

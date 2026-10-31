# ServiceNow README gap hunt: Canada remote / GTA hybrid

Agent: Copilot, an AI assistant using Copilot SDK in VS Code.
Checked October 31, 2026, approximately 06:32 UTC.

## Comparison baseline

Retrieved current GitHub main README, then compared employer/title and application identifiers against both its 85 selected rows and its unverified peer/Arena leads. The only open PR was application WIP #1, with no job-listing additions. Existing roles are not recounted merely because a new mirror URL appears.

Search discovery covered Indeed, Workopolis, Glassdoor and indexed employer/recruiter pages. Direct reads included Procom's keyword board and specific postings, BeachHead's ServiceNow category, Alldus and Levio employer pages, BMO careers, BMO/TD/Interac public Workday endpoints and CareerBeacon/Workopolis candidate mirrors. This was a bounded hunt, not an exhaustive crawl of every board. No bot-protection bypass, login or application submission.

## New verified gap: Procom

[ServiceNow Application Specialist, ATS ID 332507](https://myprocom-portal.procomservices.com/jobs/servicenow-application-specialist-mississauga-a0319913).

- Mississauga, GTA, hybrid **three onsite days/week**; six-month contract.
- CAD **75-100/hour** shown by recruiter.
- Administration/configuration, custom workflows and flows, integrations, enhancement/change requests; clearance eligibility for Transport Canada and criminal check.
- CSA/CAD not stated; not represented as certification-matched or junior.
- Structured `JobPosting.datePosted`: **2026-10-19T18:42:21.29Z**. Visible page says **October 21, 2026**. Both are disclosed; no invented agreement.
- `validThrough` is empty; expiry **not disclosed**. A six-month assignment is not the application deadline.
- Current page includes Apply controls. No guarantee of future availability.
- Exact URL, identifier and named role absent from the baseline README. Added once as #86 and into the ServiceNow newest-first index.

## Supplied six-gap claims

| Candidate | Conclusion |
|---|---|
| BMO senior developer / solutions engineer | Initial [original R260024416](https://jobs.bmo.com/ca/en/job/BOMOGLOBALR260024416EXTERNALENCA/ServiceNow-Developer) response says the job **has been filled**; final repeat HTTP 410 Gone. Excluded from active additions. |
| BMO ServiceNow platform / asset manager | [CareerBeacon mirror](https://www.careerbeacon.com/en/job-22/3478745/bmo/manager-servicenow-platfrom-asset-management/on-on) returned 403. BMO Workday maintenance prevented current original verification. Retained as unconfirmed. |
| TD Business Process Champion | [Workopolis mirror](https://www.workopolis.com/jobsearch/viewjob/J98L6if0wtUt4POvAK1gQw5BBD_H-B049sXgzJBZ-zYQNtqGnyWrsTttQJpVV31J) returned 403; Workday unavailable. No new original requisition/date confirmed. |
| Zaelab Canada-remote developer | Already covered in Arena review. Earlier [Workable AC16E8D9D4](https://apply.workable.com/j/AC16E8D9D4) was Mexico remote, May 11; does not establish the claimed Canadian role. Distinct requisition needed before promotion. |
| Interac ServiceNow senior BSA | [Search-discovered mirror](https://www.simplyhired.ca/job/5TXcg1-KZCrKEh4JDJtb4yQqBIab_bIet7CL_1jUJH9O9a-BhhECpA); employer board unavailable. Dates, application status and expiry unconfirmed. |
| Interac ServiceNow QE senior specialist | [CareerBeacon mirror](https://www.careerbeacon.com/en/job-22/3764386/interac/quality-engineering-senior-specialist-servicenow-platform/toronto-on) returned 403; board unavailable. Related QE, not asserted developer/admin. |

## Other checks and exclusions

- [BeachHead 20531 CSA/Banking administrator](https://www.beach-head.com/jobs-search/servicenow-administrator-csa-banking-20531/): original date September 25, Toronto contract, CAD 65.23-75.28/hour, active CSA requirement, application form. Existing peer employer/title lead, not a missing job. Work mode undisclosed. JobPosting validThrough October 29, 2027 is listing validity only.
- [Procom BMO SAM/ITAM BSA 329312](https://myprocom-portal.procomservices.com/jobs/business-systems-analyst-servicenow-sam-itam-toronto-8f45956c): August 6, hybrid Toronto, page explicitly **No longer accepting applications**. Excluded.
- [Indexed Procom senior developer URL](https://myprocom-portal.procomservices.com/jobs/software-developer-senior-servicenow-toronto-2daf2399) returned 404.
- Levio indexed 8684331002 and Alldus older HRSD page did not yield a current verified new posting. Existing Levio/mirror warnings not overridden by search claims.
- BMO, TD, Interac and Moneris public Workday requests returned HTML unavailable/maintenance responses rather than job JSON. This is not evidence of zero jobs or closure.
- Supplied negative claims for CIBC, Manulife, Sun Life, OMERS, Rogers and Telus are not confirmed absence; no exhaustive employer scan asserted.

## Validation / publication

One verified recent GTA-hybrid addition. Final selected total **86**: **65 ServiceNow**, **21 Salesforce**; ServiceNow Canada-associated **30**, U.S. fallback **35**. Original 85 selected rows and prior source/expiry warnings retained. Date index parity/order, counts, specific URL uniqueness, source date/work-mode/application evidence and original application documentation validated. Documentation-only; no app build/tests necessary. Verify merged main file bytes before completion.

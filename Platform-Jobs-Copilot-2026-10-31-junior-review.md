# Toronto junior/entry-level claims: source review

Agent: Copilot, an AI assistant using Copilot SDK in VS Code.
Date: October 31, 2026 UTC.

## What changed

The user supplied three overlapping lists asserting conflicting junior/mid-level status for City of Toronto job 66386, plus intermediate BFG and generic CGI, Deloitte, Scotiabank, EDC and Lightspeed search leads.

The [official City posting](https://jobs.toronto.ca/jobsatcity/job/Toronto-SYSTEMS-INTEGRATOR-1-%28SERVICENOW-DEVELOPER%29-ON-M5V-3C6/606700617) returned HTTP 200 but explicitly states **"Sorry, this job posting has ended."** The existing README peer row is now marked closed instead of pending. The [CareerBeacon mirror](https://www.careerbeacon.com/en/job-4/3901692/city-of-toronto/systems-integrator-1-servicenow-developer/toronto-on) returned 403; no bypass attempted. Neither "Entry Level" nor "Mid-Level" is currently exposed in the official ended-page response, so the conflicting supplied labels are disclosed rather than independently asserted.

Supplied historical details remain labelled: October 5-20 posting period, temporary full-time 12-month term, 92 Front Street East, CAD 52.38-57.39/hour at 35 hours/week. Arithmetic at 52 weeks is CAD 95,331.60-104,449.80; paid weeks/hours and contract earnings are not guaranteed. The supplied CAD 109,000-119,000 estimate uses a different hours assumption and is not used.

A [current employer ServiceNow search](https://jobs.scotiabank.com/search?locationsearch=Toronto&q=ServiceNow) returned Discovery Developer, already selected in README #10. It did not establish the supplied Administrator Specialist or a new general developer vacancy. Absence from that result is not proof those requisitions never existed.

All other supplied searches and names are retained in the [README seniority review](README.md#junior--entry-level-toronto-claim-review---october-31), with unknown dates, seniority and vacancy status. Keyword search matches, estimates and unnamed employers are not converted into verified entry-level jobs. BFG intermediate and CGI peer leads remain reviewable.

## Verification

Official City closure message retrieved; CareerBeacon 403 recorded; Scotiabank search examined. README selected count stays 85, all previous selected rows and application documentation preserved, supplied discovery links retained, and City peer state corrected. No new open junior role is claimed. Documentation-only update; no application tests/build needed. Publish and verify default-branch file bytes after merge.

# Date-sorted README and expiry audit

Agent: Copilot, an AI assistant using Copilot SDK in VS Code.
Checked: 2026-10-31 06:20 UTC.

## Scope and methods

Rechecked every one of the 85 selected links using public employer/ATS endpoints or individual posting pages. Reviewed all five existing PRs: #2-5 merged, #1 open with no changed files and no job-listing delta. Preserved all original rows, peer leads, closed-posting warnings and application documentation. The README now presents separate ServiceNow/Salesforce date-sorted indexes, with older and undated exceptions below recent roles.

No expiry is invented. JobPosting validThrough is listing validity, not automatically an employer deadline. Workday endDate and Oracle ExternalPostedEndDate are labelled as ATS fields. Explicit deadline text is separate. Current non-JSON Workday responses are marked unconfirmed, not silently treated as active or closed; previous canApply evidence does not prove current acceptance. Some historical dates also differ across employer marketing and ATS versions, as disclosed in the existing rows.

Current status counts: Accepting (ATS): 4; Detail listed: 34; Listed (ATS): 26; Provisional mirror: 1; Unconfirmed: 20.
Published expiry/validity fields retrieved: 21.

## Complete per-posting audit

| Original row | Job | Current status | Expiry / explicit deadline | Latest-check limitation |
|---|---|---|---|---|
| 01 | [Information Technology Service Management (ITSM) Analyst (JR100183) - CAAT Pension Plan](https://caatpension.wd10.myworkdayjobs.com/Careers/job/Toronto-ON/ITSM-Analyst_JR100183) | Accepting (ATS) | Not disclosed |  |
| 02 | [Principal Solution Architect - ServiceNow - ServiceNow](https://jobs.smartrecruiters.com/ServiceNow/744000158575719-principal-solution-architect-servicenow?oga=true) | Listed (ATS) | Not disclosed |  |
| 03 | [ServiceNow Platform Specialist - Alimentiv](https://jobs.lever.co/alimentiv-2/31ce3213-3bdc-4c28-b852-4867c6c5f108) | Listed (ATS) | Not disclosed |  |
| 04 | [ServiceNow Technical Architect - Randstad](https://www.randstad.ca/jobs/servicenow-technical-architect_toronto_47644537/) | Detail listed | 2026-12-21T00:00:00+0000 (JobPosting validThrough (listing validity)) |  |
| 05 | [ServiceNow Technical Lead (JR100193) - CAAT Pension Plan](https://caatpension.wd10.myworkdayjobs.com/Careers/job/Toronto-ON/ServiceNow-Technical-Lead_JR100193-1) | Accepting (ATS) | Not disclosed |  |
| 06 | [Senior Manager, ServiceNow - Operate (135627) - Deloitte Canada](https://careers.deloitte.ca/job/Senior-Manager%2C-ServiceNow-Operate/135627-en_US) | Detail listed | Not disclosed |  |
| 07 | [ServiceNow Developer (CONTRACT ROLE) - Brookfield](https://brookfield.wd5.myworkdayjobs.com/brookfield/job/Toronto-Ontario/ServiceNow-Developer--CONTRACT-ROLE-_R2053249-1) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 08 | [Expert Software Engineer - ServiceNow (OPRYDAFQ / ECEJRKAA) - TEEMA](https://app.workwolf.com/pipelineLink/OPRYDAFQ) | Accepting (ATS) | Not disclosed |  |
| 09 | [ServiceNow Developer (Sr. Associate) (JR-0016235) - Huron](https://huron.wd1.myworkdayjobs.com/huroncareers/job/Chicago---550-Van-Buren/ServiceNow-Developer--Sr-Associate-_JR-0016235) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 10 | [ServiceNow Discovery Developer (258467) - Scotiabank](https://jobs.scotiabank.com/job/Toronto-ServiceNow-Discovery-Developer-ON-M1L4S2/602442317/) | Detail listed | Not disclosed |  |
| 11 | [Systems Administrator V Service Now - Randstad](https://www.randstad.ca/jobs/systems-administrator-v-service-now_toronto_47502843/) | Detail listed | 2026-12-24T00:00:00+0000 (JobPosting validThrough (listing validity)) |  |
| 12 | [Senior ServiceNow Engineer - EQ Bank / Equitable Bank](https://jobs.lever.co/eqbank/1af36346-6dd1-475a-bee9-1d5e805452e8) | Listed (ATS) | Not disclosed |  |
| 13 | [Senior Project Manager/Leader - ServiceNow / ITSM - Randstad](https://www.randstad.ca/jobs/senior-project-managerleader_toronto_47414563/) | Detail listed | 2026-12-21T00:00:00+0000 (JobPosting validThrough (listing validity)) |  |
| 14 | [ServiceNow System Administrator (432824) - Bell](https://jobs.bce.ca/bell/job/Toronto-ServiceNow-System-Administrator-ON/1437306800/) | Detail listed | Not disclosed; explicit application deadline: 11/02/2026 |  |
| 15 | [RQ00206 - Senior ServiceNow Developer - Source Code](https://www.careers-page.com/source-code/job/X9494X8Y) | Detail listed | Not disclosed |  |
| 16 | [Senior ServiceNow Developer (R129586) - Irving Oil](https://irvingoil.wd3.myworkdayjobs.com/IOL_Careers_Primary/job/Saint-John/Senior-ServiceNow-Developer_R129586) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 17 | [ServiceNow Developer (SERV-NOW-DEV-KIT-26-1) - Brock Solutions](https://careers.brocksolutions.com/Careers.aspx?req=SERV-NOW-DEV-KIT-26-1&type=JOBDESCR) | Detail listed | Not disclosed |  |
| 18 | [CSM/FSO Developer (58804) - Alldus](https://alldus.com/job/58804-csm-fso-developer-toronto-ontario/) | Detail listed | 2026-12-01T23:59:59Z (JobPosting validThrough (listing validity)) |  |
| 19 | [ServiceNow Functional Consultant (JR6421) - BDO Canada](https://bdo.wd3.myworkdayjobs.com/BDO/job/Toronto---Bay-St/ServiceNow-Functional-Consultant_JR6421) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 20 | [ServiceNow Senior Developer (JR5588) - BDO Canada](https://bdo.wd3.myworkdayjobs.com/BDO/job/Toronto---Bay-St/ServiceNow-Senior-Developer_JR5588) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 21 | [Intermediate Specialized IT Consultant - ServiceNow - Randstad](https://www.randstad.ca/jobs/intermediate-specialized-it-consultant_toronto_47292146/) | Detail listed | 2026-11-15T00:00:00+0000 (JobPosting validThrough (listing validity)) |  |
| 22 | [Consultant, ServiceNow Developer (33530) - KPMG Canada](https://careers.kpmg.ca/jobs/33530) | Unconfirmed | 2027-08-14T07:06:07.000Z (JobPosting validThrough (listing validity)) | No matching application detail established |
| 23 | [Senior Technical Consultant, ServiceNow Developer (33533) - KPMG Canada](https://careers.kpmg.ca/jobs/33533) | Unconfirmed | 2027-08-14T07:33:07.000Z (JobPosting validThrough (listing validity)) | No matching application detail established |
| 24 | [ServiceNow ITOM Developer (58626) - Alldus](https://alldus.com/job/58626-servicenow-itom-developer-quebec/) | Detail listed | 2026-12-01T23:59:59Z (JobPosting validThrough (listing validity)) |  |
| 25 | [Secret Cleared ServiceNow Developer - App Engine (120592) - Alldus (Club mirror)](https://jobs.tryclub.com/projects/120592/secret-cleared-servicenow-developer-app-engine) | Provisional mirror | 2027-01-20 (JobPosting validThrough (listing validity)) |  |
| 26 | [ServiceNow Developer (SAM Pro) - First Citizens Bank](https://jobs.firstcitizens.com/jobs/36298) | Detail listed | 2027-10-29T18:21:27.000Z (JobPosting validThrough (listing validity)) |  |
| 27 | [ServiceNow Developer II (SE2) (Remote TX) - First Citizens Bank](https://jobs.firstcitizens.com/jobs/36303) | Detail listed | 2027-10-29T21:03:26.000Z (JobPosting validThrough (listing validity)) |  |
| 28 | [ServiceNow Developer III (SE3) (Remote CT) - First Citizens Bank](https://jobs.firstcitizens.com/jobs/36304) | Detail listed | 2027-10-29T21:16:26.000Z (JobPosting validThrough (listing validity)) |  |
| 29 | [ServiceNow Developer SME - General Dynamics Information Technology](https://gdit.wd5.myworkdayjobs.com/External_Career_Site/job/Any-Location--Remote/ServiceNow-Developer-SME_RQ231509-1) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 30 | [ServiceNow Developer - 9th Way Insignia](https://job-boards.greenhouse.io/9thwayinsignia/jobs/5466447008) | Listed (ATS) | Not disclosed |  |
| 31 | [ServiceNow Solutions Developer - Bright Vision Technologies](https://brightvisiontechnologies.applytojob.com/apply/tiOdUW4vF9/ServiceNow-Solutions-Developer) | Detail listed | 2027-01-26 (JobPosting validThrough (listing validity)) |  |
| 32 | [Senior ServiceNow Developer (RQ228679) - GDIT](https://gdit.wd5.myworkdayjobs.com/External_Career_Site/job/Any-Location--Remote/Senior-ServiceNow-Developer_RQ228679-1) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 33 | [ServiceNow Developer - TS/SCI with Polygraph (RQ231232) - GDIT](https://gdit.wd5.myworkdayjobs.com/External_Career_Site/job/USA-VA-Chantilly/ServiceNow-Developer---TS-SCI-with-Polygraph_RQ231232-1) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 34 | [ServiceNow Developer Principal (RQ230501) - GDIT](https://gdit.wd5.myworkdayjobs.com/External_Career_Site/job/Any-Location--Remote/ServiceNow-Developer-Principal_RQ230501-1) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 35 | [ServiceNow Engineer - Strategic Portfolio Management (SPM) (RQ230422) - GDIT](https://gdit.wd5.myworkdayjobs.com/External_Career_Site/job/USA-FL-MacDill-AFB/ServiceNow-Engineer---Strategic-Portfolio-Management--SPM-_RQ230422-1) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 36 | [ServiceNow System Administrator (RQ230636) - GDIT](https://gdit.wd5.myworkdayjobs.com/External_Career_Site/job/Any-Location--Remote/ServiceNow-System-Administrator_RQ230636) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 37 | [Senior ServiceNow Developer - Resolve Tech Solutions](https://resolvetech.wd1.myworkdayjobs.com/RTS/job/US-Remote---TX/Senior-ServiceNow-Developer_R1280) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 38 | [Sr ServiceNow Developer / Architect - HPTech](https://www.dice.com/job-detail/0e33cd66-ad50-469f-ad16-3a39076da95c) | Detail listed | 2026-11-27T14:32:06.000Z (JobPosting validThrough (listing validity)) |  |
| 39 | [Sr. ServiceNow Developer - Sygna Solutions](https://sygnasolutions.betterteam.com/sr.-servicenow-developer) | Detail listed | Not disclosed |  |
| 40 | [ServiceNow Developer - Futuremindz](https://www.dice.com/job-detail/042241b5-d082-4101-9412-637f8ab8dadf) | Detail listed | 2026-11-26T13:57:55.000Z (JobPosting validThrough (listing validity)) |  |
| 41 | [Senior ServiceNow Developer - Minimum Interim Secret Clearance (or higher) - ITC Federal](https://careers-itcfederal.icims.com/jobs/1626/job?in_iframe=1) | Detail listed | 2027-10-26T04:00:00.000Z (JobPosting validThrough (listing validity)) |  |
| 42 | [Lead ServiceNow Developer - LightFeather](https://job-boards.greenhouse.io/lightfeatheriollc/jobs/5462851008) | Listed (ATS) | Not disclosed |  |
| 43 | [Senior ServiceNow CMDB Engineer - LightFeather](https://job-boards.greenhouse.io/lightfeatheriollc/jobs/5462857008) | Listed (ATS) | Not disclosed |  |
| 44 | [Senior ServiceNow Developer - Public Trust Clearance - LightFeather](https://job-boards.greenhouse.io/lightfeatheriollc/jobs/5462858008) | Listed (ATS) | Not disclosed |  |
| 45 | [ServiceNow Architect - LightFeather](https://job-boards.greenhouse.io/lightfeatheriollc/jobs/5462856008) | Listed (ATS) | Not disclosed |  |
| 46 | [ServiceNow Platform Engineer - LightFeather](https://job-boards.greenhouse.io/lightfeatheriollc/jobs/5462859008) | Listed (ATS) | Not disclosed |  |
| 47 | [ServiceNow Platform Developer (396) - iTech AG](https://jobs.jobvite.com/itechag/job/obvZAfwZ) | Detail listed | Not disclosed |  |
| 48 | [ServiceNow System Administrator (397) - iTech AG](https://jobs.jobvite.com/itechag/job/oswZAfwh) | Detail listed | Not disclosed |  |
| 49 | [ServiceNow Sr. Developer - Accenture Federal Services](https://boards.greenhouse.io/accenturefederalservices/jobs/4711687006?gh_jid=4711687006) | Listed (ATS) | Not disclosed |  |
| 50 | [ServiceNow Sr. Developer (CSM) - Accenture Federal Services](https://boards.greenhouse.io/accenturefederalservices/jobs/4704225006?gh_jid=4704225006) | Listed (ATS) | Not disclosed |  |
| 51 | [ServiceNow Sr. Developer (Now Assist) - Accenture Federal Services](https://boards.greenhouse.io/accenturefederalservices/jobs/4704107006?gh_jid=4704107006) | Listed (ATS) | Not disclosed |  |
| 52 | [ServiceNow Sr. Developer (Portal) - Accenture Federal Services](https://boards.greenhouse.io/accenturefederalservices/jobs/4704135006?gh_jid=4704135006) | Listed (ATS) | Not disclosed |  |
| 53 | [ServiceNow Development Analyst - Accenture Federal Services](https://boards.greenhouse.io/accenturefederalservices/jobs/4721709006?gh_jid=4721709006) | Listed (ATS) | Not disclosed |  |
| 54 | [ServiceNow Development Lead - Accenture Federal Services](https://boards.greenhouse.io/accenturefederalservices/jobs/4721707006?gh_jid=4721707006) | Listed (ATS) | Not disclosed |  |
| 55 | [Sr. ServiceNow Developer - Stanfield Systems](https://www.dice.com/job-detail/b9f42ff7-04b1-4a10-a7b2-719970d98b8d) | Detail listed | 2026-11-06T17:06:30.000Z (JobPosting validThrough (listing validity)) |  |
| 56 | [ServiceNow Developer - Bravium Consulting](https://jobs.jobvite.com/braviumconsulting/job/ol7SAfwE) | Detail listed | Not disclosed |  |
| 57 | [ServiceNow Developer - SPM (390) - iTech AG](https://jobs.jobvite.com/itechag/job/omZRAfww) | Detail listed | Not disclosed |  |
| 58 | [ServiceNow ITOM Senior Developer (385) - iTech AG](https://jobs.jobvite.com/itechag/job/oFROAfwE) | Detail listed | Not disclosed |  |
| 59 | [ServiceNow Certified Technical Architect - Bravium Consulting](https://jobs.jobvite.com/braviumconsulting/job/oq6OAfwE) | Detail listed | Not disclosed |  |
| 60 | [ServiceNow Scrum Architect (379) - iTech AG](https://jobs.jobvite.com/itechag/job/olaJAfwy) | Detail listed | Not disclosed |  |
| 61 | [Principle Salesforce Developer (JR106006) - Moneris](https://moneris.wd3.myworkdayjobs.com/Moneris/job/Toronto/Principle-Software-Developer_JR106006-2) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 62 | [Salesforce Developer (MED02518) - Medcan](https://medcan.wd10.myworkdayjobs.com/medcan/job/Toronto/Salesforce-Developer_MED02518) | Accepting (ATS) | 2026-11-06 (Workday endDate) |  |
| 63 | [Software Engineer II (Salesforce Loyalty Management Developer) (R_1509038) - TD](https://td.wd3.myworkdayjobs.com/TD_Bank_Careers/job/Toronto-Ontario/Software-Engineer-II--Salesforce-Loyalty-Management-Developer-_R_1509038) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 64 | [Senior Salesforce Developer/Admin (137318) - Celestica](https://careers.celestica.com/job/Toronto-Senior-Salesforce-Developer-Admin-ON/1406609733/) | Detail listed | Not disclosed |  |
| 65 | [Senior Salesforce Administrator - Loopio](https://jobs.ashbyhq.com/loopio/b8d91233-b646-43f7-941e-ca654b21921e) | Listed (ATS) | Not disclosed |  |
| 66 | [Salesforce Developer (265640) - Scotiabank](https://jobs.scotiabank.com/job/Toronto-Salesforce-Developer-ON-M5H1B6/604373417/) | Detail listed | Not disclosed |  |
| 67 | [Salesforce Administrator - Assistant Vice President (8833783002) - iCapital](https://job-boards.greenhouse.io/icapitalnetwork/jobs/8833783002) | Listed (ATS) | Not disclosed |  |
| 68 | [Marketing Operations Analyst (8333965) - D2L](https://www.d2l.com/careers/jobs/?job_id=8333965&gh_jid=8333965) | Listed (ATS) | Not disclosed |  |
| 69 | [Sr. Developer, AI and Agentforce (6231605004) - NeuraFlash / Accenture](https://job-boards.greenhouse.io/neuraflash/jobs/6231605004) | Listed (ATS) | Not disclosed |  |
| 70 | [Salesforce Administrator - Christian Reformed Church in North America](https://crcna.pinpointhq.com/en/postings/909eaf81-7d9f-4cfa-b5cf-9f1c4759fd9f) | Detail listed | 2026-11-01T00:00:00+00:00 (JobPosting validThrough (listing validity)); explicit application deadline: November 01, 2026 |  |
| 71 | [B2B Salesforce Administrator (74921) - Staples Canada](https://careers.staples.ca/hcmUI/CandidateExperience/en/sites/StaplesCanada/job/74921) | Listed (ATS) | Not disclosed |  |
| 72 | [Salesforce Developer - Versapay](https://jobs.lever.co/versapay/7906bc29-f17e-44d2-a41b-334e6ce0608c) | Listed (ATS) | Not disclosed |  |
| 73 | [Salesforce Administrator (4685515005) - Bloomerang](https://job-boards.greenhouse.io/bloomerang/jobs/4685515005) | Listed (ATS) | Not disclosed |  |
| 74 | [Senior Salesforce Developer (1443153641962) - CACI](https://searchcareers.caci.com/careers/job/1443153641962) | Detail listed | 2027-04-24T00:00:00 (JobPosting validThrough (listing validity)) |  |
| 75 | [Salesforce Administrator - MoeGo](https://jobs.ashbyhq.com/moego/07afb9d1-0c84-4732-b3bc-facf66dbc934) | Listed (ATS) | Not disclosed |  |
| 76 | [GTM Systems Administrator (4424870009) - Dscout](https://job-boards.greenhouse.io/dscout/jobs/4424870009) | Listed (ATS) | Not disclosed |  |
| 77 | [Salesforce Platform Developer (R0014087) - Altus Group](https://altusgroup.wd3.myworkdayjobs.com/AltusGroup/job/Toronto-Ontario/Salesforce-Platform-Developer_R0014087) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 78 | [Senior Salesforce Administrator - Benevity](https://jobs.ashbyhq.com/benevity/78798ad7-2d39-497e-98af-dad3a2ea8e20) | Listed (ATS) | Not disclosed |  |
| 79 | [CRM Data Engineer (R11306) - AGF Investments](https://agf.wd3.myworkdayjobs.com/AGF_Careers/job/Toronto-ON/Salesforce-Developer--Solution-Designer_R11306-3) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 80 | [Salesforce Senior Developer (REQ-14036) - IKO](https://iko.wd3.myworkdayjobs.com/IKO_Careers/job/Mississauga-ON/Salesforce-Senior-Developer_REQ-14036) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 81 | [Service Now AI Architect (JR0151830) - McKesson](https://mckesson.wd3.myworkdayjobs.com/External_Careers/job/CAN-ON-Mississauga/Service-Now-AI-Architect_JR0151830-1) | Unconfirmed | Not disclosed | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| 82 | [Senior Salesforce Administrator (8129548) - Movable Ink](https://movableink.com/job-listing?gh_jid=8129548) | Listed (ATS) | Not disclosed |  |
| 83 | [ServiceNow SPM Developer (59286) - Alldus](https://alldus.com/job/59286-servicenow-spm-developer-montreal-quebec/) | Detail listed | 2027-01-20T23:59:59Z (JobPosting validThrough (listing validity)) |  |
| 84 | [FSO-ServiceNow Developer (33633) - National Bank of Canada](https://emplois.bnc.ca/en_CA/careers/JobDetail/MONTREAL-Quebec-Canada-P5I27-DEVELOPPEUR-PRINCIPAL/33633) | Detail listed | Not disclosed |  |
| 85 | [ServiceNow Platform Administrator (526446 / 314590) - FX Innovation / Ateko](https://www.fxinnovation.com/en/jobs/526446) | Detail listed | Not disclosed |  |

## Verification

All 85 source checks completed with explicit result states, including failures. Source-field dates are preserved verbatim. README indexes checked for 64 ServiceNow and 21 Salesforce rows, date ordering, recent-window classification, uniqueness, and parity with original selected rows. Original 85 detailed rows and all application documentation retained. Supplied board links preserved without unverified counts/rankings. Documentation-only, no app build/tests required. Verify GitHub default-branch bytes after merge.

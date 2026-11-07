# Bucket rounds — 30 todos × 30 rounds × 3 buckets (Salesforce / ServiceNow / Other)

Generated 2026-11-04 05:46 UTC · driver `scripts/bucket_rounds.py`

Each bucket runs exactly 30 rounds; round *k* executes todo *k*, so a 30-todo set finishes
in 30 rounds. Each round queries one real employer feed through the ATS adapters in
`scripts/ats_board_sweep.py` (Workday CXS, Greenhouse, Lever, Ashby, SmartRecruiters,
Workable), keeps postings whose **title** matches the bucket keywords and whose
**location** is Canadian, then re-fetches every posting URL and keeps it only if it
still returns HTTP 2xx/3xx. A date comes from the feed or the row is dropped —
nothing is inferred, and `Net-new` means absent from `jobs.json` by normalised URL.

## Totals

| Bucket | Rounds | Postings fetched | Title+bucket match | Live-verified | Net-new |
|--------|-------:|-----------------:|-------------------:|--------------:|--------:|
| Salesforce | 30/30 | 1087 | 29 | 29 | **4** |
| Servicenow | 30/30 | 968 | 11 | 8 | **2** |
| Other | 30/30 | 2927 | 29 | 23 | **23** |
| **Total** | **90/90** | **4982** | **69** | **60** | **29** |

## Salesforce — 4 net-new live job(s) (29 live matches total)

| Posted | Title | Company | Location | HTTP |
|--------|-------|---------|----------|------|
| 2026-10-30 | [Senior Salesforce Developer](https://jobs.ashbyhq.com/docebo/0bbdde71-476f-4f46-bfdc-d4536cdcf7ad) | Docebo | Toronto, Ontario | 200 |
| 2026-10-20 | [Functional Lead, AI & Agentforce Delivery](https://job-boards.greenhouse.io/neuraflash/jobs/6228522004) | NeuraFlash, Part of Accenture | Remote - Canada (Alberta, British Columb | 200 |
| 2026-10-15 | [Forward Deployed Engineer, AI & Agentforce](https://job-boards.greenhouse.io/neuraflash/jobs/6225939004) | NeuraFlash, Part of Accenture | Remote - Canada (Alberta, British Columb | 200 |
| 2026-10-02 | [Salesforce Product Owner](https://jobs.ashbyhq.com/docebo/6c6ced29-4d69-4e93-b808-e6aea83d87f3) | Docebo | Toronto, Ontario | 200 |

<details><summary>All 29 live matches, by round</summary>

- **R2 NeuraFlash** (15 live) — Forward Deployed Engineer, AI & Agentforce; Functional Lead, AI & Agentforce Delivery; Salesforce Consultant, Change Management; Salesforce Engagement Manager …
- **R12 Loopio** (1 live) — Senior Salesforce Administrator
- **R13 Docebo** (2 live) — Salesforce Product Owner; Senior Salesforce Developer
- **R14 Benevity** (2 live) — Senior Salesforce Administrator; Senior Salesforce Administrator
- **R17 Altus Group** (2 live) — Salesforce Platform Developer; Salesforce Business Analyst
- **R18 BMO** (1 live) — Manager, Banking Salesforce Innovation & Enablement
- **R19 TD Bank** (1 live) — Software Engineer II (Salesforce Loyalty Management Developer)
- **R26 Moneris** (1 live) — Principle Salesforce Developer
- **R27 McKesson** (4 live) — Salesforce Delivery Lead; Salesforce Marketing Cloud Developer; Lead Salesforce Solution Architect; Sr. Salesforce CRM Development Lead

</details>

## Servicenow — 2 net-new live job(s) (8 live matches total)

| Posted | Title | Company | Location | HTTP |
|--------|-------|---------|----------|------|
| 2026-10-28 | [ServiceNow Business Process Consultant – FSO/CSM](https://www.newrocket.com/careers/job?gh_jid=6230570004&gh_jid=6230570004) | NewRocket | Remote - US or Canada | 200 |
| — | [ServiceNow Developer (ITSM Module) At Client Site in Ottawa](https://dxctechnology.wd1.myworkdayjobs.com/en-US/dxcjobs/job/CAN---ON---OTTAWA/ServiceNow-Developer-At-Client-Site_51523856) | DXC Technology | CAN - ON - OTTAWA | 200 |

<details><summary>All 8 live matches, by round</summary>

- **R1 ServiceNow** (1 live) — Principal Solution Architect- ServiceNow
- **R5 Highmetric** (1 live) — ServiceNow Business Process Consultant – FSO/CSM
- **R10 DXC Technology** (1 live) — ServiceNow Developer (ITSM Module) At Client Site in Ottawa
- **R18 BMO** (1 live) — ServiceNow  SAM Administrator - ITAM
- **R25 Interac** (2 live) — Senior Business Systems Analyst (ServiceNow); Quality Engineering, Senior Specialist (ServiceNow Platform))
- **R28 CAAT Pension Plan** (2 live) — ServiceNow Technical Lead; Information Technology Service Management (ITSM) Analyst

</details>

## Other — 23 net-new live job(s) (23 live matches total)

| Posted | Title | Company | Location | HTTP |
|--------|-------|---------|----------|------|
| 2026-11-04 | [Supervisor, Data Architect](https://rsm.wd1.myworkdayjobs.com/en-US/RSMCareers/job/Toronto/Supervisor--Data-Architect_JR122224) | RSM | Toronto | 200 |
| 2026-10-31 | [Senior Data Scientist, Predictive Modelling](https://canadiantirecorporation.wd3.myworkdayjobs.com/en-US/Enterprise_External_Careers_Site/job/Toronto-ON/Senior-Data-Scientist--Predictive-Modelling_JR166754) | Canadian Tire | Toronto, ON | 200 |
| 2026-10-30 | [Finance Systems Analyst - Integrations and Automation](https://jobs.ashbyhq.com/1password/9d3f7564-490b-4107-b315-ece3146760a8) | 1Password | Remote (United States | Canada) | 200 |
| 2026-10-23 | [Data Scientist, Growth (12 month contract)](https://jobs.lever.co/eqbank/6d858052-8862-47b5-a25e-5915424c6691) | EQ Bank | Toronto | 200 |
| 2026-10-23 | [Senior Data Analyst, Enterprise](https://jobs.ashbyhq.com/1password/577f47a1-f80d-4d5b-8212-9e38e749c004) | 1Password | Remote (United States | Canada) | 200 |
| 2026-10-22 | [CRM Data Engineer](https://agf.wd3.myworkdayjobs.com/en-US/AGF_Careers/job/Toronto-ON/Salesforce-Developer--Solution-Designer_R11306-3) | AGF | Toronto, ON | 200 |
| 2026-10-20 | [Senior DevOps Engineer](https://jobs.ashbyhq.com/telus-digital/b880f4d2-824a-48ce-bab9-3188f343db9b) | TELUS Digital | Remote, British Columbia | 200 |
| 2026-10-20 | [Data Analyst](https://canadiantirecorporation.wd3.myworkdayjobs.com/en-US/Enterprise_External_Careers_Site/job/Laval-QC/Data-Analyst_JR166738) | Canadian Tire | Laval, QC | 200 |
| 2026-10-20 | [Senior Data Engineer](https://iko.wd3.myworkdayjobs.com/en-US/IKO_Careers/job/Mississauga-ON/Senior-Data-Engineer_REQ-14014) | IKO | Mississauga, ON | 200 |
| 2026-10-15 | [Data Scientist, Market Risk Models](https://desjardins.wd10.myworkdayjobs.com/en-US/Desjardins/job/Montral/Scientifique-de-donnes--Modles-de-risque-de-march_R2611884-1) | Desjardins | Montréal | 200 |
| 2026-10-09 | [DevOps Engineer - New Grad (January 2027)](https://bdo.wd3.myworkdayjobs.com/en-US/BDO/job/Toronto---Bay-St/DevOps-Engineer---New-Grad--January-2027-_JR7194) | BDO Canada | Toronto - Bay St | 200 |
| 2026-09-22 | [Senior Machine Learning Systems Engineer (CAD)](https://jobs.lever.co/pointclickcare/150b07cd-04e9-46c4-9015-114498f3798c) | PointClickCare | Mississauga | 200 |
| 2026-09-14 | [Data Engineer](https://movableink.com/job-listing?gh_jid=8188477) | Movable Ink | Movable Ink - Toronto (Remote)  | 200 |
| 2026-09-03 | [Senior Enterprise Systems Engineer](https://jobs.ashbyhq.com/1password/363ebcb3-897b-4266-8734-aa7592bd532d) | 1Password | Remote (United States | Canada) | 200 |
| 2026-09-02 | [Business Intelligence Developer](https://job-boards.greenhouse.io/taketwo/jobs/8165127) | Take-Two Interactive Software, Inc. | Toronto, Ontario, Canada | 200 |
| 2026-08-13 | [(Canada) Principal ML System Engineer](https://jobs.lever.co/pointclickcare/ccdecc93-aef2-4b2b-a981-6843f3c16221) | PointClickCare | Remote or Mississauga | 200 |
| 2026-07-13 | [Staff Data Analyst, Marketing](https://jobs.ashbyhq.com/1password/45393747-1ed7-4eb9-bcda-4c74fe5e9824) | 1Password | Remote (United States | Canada) | 200 |
| 2026-07-08 | [Staff Data Scientist](https://careers.toasttab.com/jobs?gh_jid=8052293) | Toast | Canada | 200 |
| 2026-04-24 | [Data Developer (Python/Spark)](https://job-boards.greenhouse.io/taketwo/jobs/7851352) | Take-Two Interactive Software, Inc. | Toronto, Ontario, Canada | 200 |
| 2026-01-22 | [Business Systems Analyst](https://jobs.lever.co/electricmind/510d7946-47f6-4a0c-8f72-a46e6ac3499a) | Electric Mind | Downtown Toronto | 200 |
| — | [Data Analyst (Two Open Roles)](https://canadiantirecorporation.wd3.myworkdayjobs.com/en-US/Enterprise_External_Careers_Site/job/Mississauga-ON/Business-Analyst--Two-Open-Roles-_JR162250) | Canadian Tire | Mississauga, ON | 200 |
| — | [Senior Data Engineer](https://iko.wd3.myworkdayjobs.com/en-US/IKO_Careers/job/Mississauga-ON/Senior-Data-Engineer_REQ-13061) | IKO | Mississauga, ON | 200 |
| — | [SR. Business Systems Analyst - Finance](https://iko.wd3.myworkdayjobs.com/en-US/IKO_Careers/job/Mississauga-ON/SR-Business-Systems-Analyst---Finance_REQ-13596) | IKO | Mississauga, ON | 200 |

<details><summary>All 23 live matches, by round</summary>

- **R6 Take-Two** (2 live) — Business Intelligence Developer; Data Developer (Python/Spark)
- **R8 Toast** (1 live) — Staff Data Scientist
- **R9 Movable Ink** (1 live) — Data Engineer
- **R10 EQ Bank** (1 live) — Data Scientist, Growth (12 month contract)
- **R11 PointClickCare** (2 live) — (Canada) Principal ML System Engineer; Senior Machine Learning Systems Engineer (CAD)
- **R15 Electric Mind** (1 live) — Business Systems Analyst
- **R16 1Password** (4 live) — Staff Data Analyst, Marketing; Senior Enterprise Systems Engineer; Senior Data Analyst, Enterprise; Finance Systems Analyst - Integrations and Automation
- **R20 TELUS Digital** (1 live) — Senior DevOps Engineer
- **R21 Canadian Tire** (3 live) — Senior Data Scientist, Predictive Modelling; Data Analyst; Data Analyst (Two Open Roles)
- **R22 Desjardins** (1 live) — Data Scientist, Market Risk Models
- **R23 BDO Canada** (1 live) — DevOps Engineer - New Grad (January 2027)
- **R24 RSM** (1 live) — Supervisor, Data Architect
- **R25 IKO** (3 live) — Senior Data Engineer; Senior Data Engineer; SR. Business Systems Analyst - Finance
- **R28 AGF** (1 live) — CRM Data Engineer

</details>

## Seeds that returned nothing (stale — fix or drop)

- **Servicenow**: Crossfuze, Medcan, SOTI, Salvation Army Canada

## Dead links caught by the liveness check

- **Servicenow**: 3 posting(s) matched but returned 4xx/5xx — excluded.
- **Other**: 6 posting(s) matched but returned 4xx/5xx — excluded.

## Round index

| Round | Salesforce | ServiceNow | Other |
|------:|-----------|-----------|-------|
| 1 | Salesforce | ServiceNow | Geotab |
| 2 | NeuraFlash | Ensiti | D2L |
| 3 | Highmetric | Spruce Infotech | MongoDB |
| 4 | nCino | Crossfuze | Okta |
| 5 | Varicent | Highmetric | Brex |
| 6 | SiteTracker | NeuraFlash | Take-Two |
| 7 | Flosum | RapDev | iCapital |
| 8 | Zaelab | Directive | Toast |
| 9 | Avacone | Accenture | Movable Ink |
| 10 | RapDev | DXC Technology | EQ Bank |
| 11 | Directive | GDIT | PointClickCare |
| 12 | Loopio | Harris Computer | Versapay |
| 13 | Docebo | Huron | Achievers |
| 14 | Benevity | ICF | Emburse |
| 15 | Lightspeed Commerce | Resolve Tech Solutions | Electric Mind |
| 16 | Accenture | SOTI | 1Password |
| 17 | Altus Group | Moneris | Docker |
| 18 | BMO | BMO | Webflow |
| 19 | TD Bank | TD Bank | Inovalon |
| 20 | CIBC | CIBC | TELUS Digital |
| 21 | Sun Life | Sun Life | Canadian Tire |
| 22 | Manulife | Manulife | Desjardins |
| 23 | OMERS | OMERS | BDO Canada |
| 24 | TMX Group | TMX Group | RSM |
| 25 | Thomson Reuters | Interac | IKO |
| 26 | Moneris | McKesson | MLSE |
| 27 | McKesson | Salvation Army Canada | TJX |
| 28 | Cloudera | CAAT Pension Plan | AGF |
| 29 | Harris Computer | Brookfield | Canadian Tire |
| 30 | GDIT | Medcan | Desjardins |

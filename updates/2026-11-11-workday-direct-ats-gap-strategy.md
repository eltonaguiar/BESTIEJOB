# BESTIEJOB — Patterns & Gap-Hunting Strategy (2026-11-10)

Source: `origin/main` README — 6,488 live postings (ServiceNow 1,087 · Salesforce 1,245 · Other 4,156).

## 1. Patterns in the current list

| | ServiceNow | Salesforce | Other |
|---|---|---|---|
| Top sources | LinkedIn 34%, Adzuna 13%, Greenhouse, jobs.ca, eluta | LinkedIn 40%, Adzuna 21%, jobs.ca, eluta | Adzuna 30%, LinkedIn 29%, **Greenhouse 17%** |
| Top employers | KPMG, ServiceNow, Deloitte, Accenture Fed, CGI, TCS, Bell, NewRocket, BDO | Salesforce, Cognizant, NeuraFlash, CloudKettle, Deloitte, TCS, Altus, iA, ATB | affirm, coinbase, gitlab, twilio, instacart, lyft (US tech Greenhouse dumps) + TD, Manulife, EDC |
| Title signals | Developer, Consultant, Architect, ITSM/ITAM/ITOM, CMDB, HRSD, CSM, SPM, GRC, SAM | Developer, Architect, Admin, Marketing/Service/Data Cloud, CPQ, FSC | engineer, analyst, data, business, BI, Power BI, analytics, automation, CRM |
| Geo | Toronto 26%, "Canada"/remote 21% | Toronto 33%, Mississauga 5% | Toronto 27%, plenty of Remote-US |

**Reverse-engineered "Other" profile** (section caption: *ITSM, ITAM, CMDB, SQL, BI, automation and integration*). ~900 of the 4,156 are BI/data. Most common: Data Analyst, Business (Systems) Analyst, Data Engineer, Analytics Engineer, Power BI Developer, BI Analyst/Developer, Configuration Analyst, Reporting & Analytics Specialist, Databricks-focused DE. Keyword set from the protocol: PowerShell, VBA/Excel, Alteryx, Python, SQL Server, Tableau, Power BI, Jira/Confluence, ITAM/ITOM.

**What the other agents keep missing:** the list is mostly **aggregator-sourced** (LinkedIn/Adzuna/Greenhouse). Big Canadian employers are hardly ever pulled **straight from their own ATS** (on their own careers site). BMO, CIBC, TD, Sun Life, Manulife, OMERS and Desjardins together make up a tiny share of rows, and most of those came in second-hand. The "Other" section also has a lot of noise from US tech companies (affirm/coinbase alone are ~400 rows) and few Canadian BI/reporting roles in banks or insurance.

## 2. Strategy (tested and it works)

### A. Query enterprise Workday tenants directly ✅ proven tonight
Each Workday careers site has a public JSON endpoint behind it: `POST https://{host}/wday/cxs/{tenant}/{site}/jobs` with `{"searchText": "...", "limit": 20}`.
I ran 8 queries (ServiceNow, Salesforce, Power BI, Tableau, Data Engineer, Reporting Analyst, Business Intelligence, Alteryx) against 6 working tenants:
**157 relevant postings came back that aren't in the README. 75 of them are in Canada or remote.** Script: [workday_probe.py](file:///C:/Users/zerou/.gemini/antigravity/brain/ec942cd7-8352-4345-bcab-7f0910a82129/scratch/workday_probe.py). Results: [new_canada.txt](file:///C:/Users/zerou/.gemini/antigravity/brain/ec942cd7-8352-4345-bcab-7f0910a82129/scratch/new_canada.txt).

Working tenants: `bmo/External`, `cibc/search`, `td/TD_Bank_Careers`, `manulife/MFCJH_Jobs`, `sunlife/Experienced-Jobs`, `omers/OMERS_External`, `desjardins (wd10)/Desjardins`.
The 404/422 errors (RBC, Intact, CPPIB, OTPP, Telus, Rogers, UHN, Metrolinx, WSIB, NBC, Loblaw, CN) just mean my guessed site name was wrong. To fix: open each careers page once and copy the `/{site}` slug from the Workday URL.

Some examples from the run:
- BMO — Manager, Reporting & Analytics (Toronto, 4 days ago); Senior Analyst Data Analytics; Senior Analyst, Wealth Data Foundations (today)
- CIBC — Consultant, Control Insights & Reporting; Senior Consultant, Data Quality; Data Analyst, Employee Communications Platforms (contract)
- TD — Information Security Specialist, Vulnerability Mgmt Data Insights & Reporting (ServiceNow); Salesforce IT Solutions Design Specialist
- Sun Life — Manager, Regulatory & Subsidiary Reporting (Tableau); Senior Associate, Global Investment Portfolio Reporting
- OMERS — Lead, Data Engineering; Senior Data Modeler; Senior Data Engineer (12-month contract)
- Desjardins — Data Engineering Advisor / Senior Advisor; Manager, Project Delivery, Data & Analytics

### B. Same idea on other ATS platforms (also public JSON endpoints)
| ATS | Endpoint | Canadian targets |
|---|---|---|
| SuccessFactors | `career{n}.successfactors.com/career?company=X` / RSS | Scotiabank, Hydro One, OPG, Air Canada |
| Oracle Taleo / ORC | `*.taleo.net/careersection/rest/jobboard/searchjobs` | Ontario Public Service, City of Toronto, Bell |
| iCIMS | `careers-X.icims.com/jobs/search?ss=1&searchKeyword=` | CGI, insurers |
| Phenom | `jobs.rbc.com/ca/en/search-results?keywords=` (embedded JSON) | RBC, Rogers |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/{co}/postings?q=` | Already partly used. Add Bosch, Visa, ServiceNow partners |
| Greenhouse/Lever/Ashby | public board APIs | Point them at **Canadian** boards (Wealthsimple, Questrade, KOHO, Ritual, Faire) rather than US tech |

### C. Search vocabulary for "Other" (BI / reporting / DE)
Titles the agents under-query: *Reporting Analyst, MIS Analyst, Insights Analyst, Data Quality, Data Governance, Data Modeler, Analytics Engineer, Regulatory Reporting, Finance Systems/EPM, Power Platform, Fabric, dbt, Databricks, Snowflake, SSRS/SSIS, Alteryx*. ServiceNow-adjacent: *Performance Analytics, CMDB Data Analyst, ITAM/SAM Analyst, ITSM Reporting*. Bank job titles hide BI work behind "Consultant" and "Senior Analyst", so search on **skills keywords (Power BI/Tableau/SQL), not on titles**. That's how the Power BI query surfaced CIBC's "Consultant" roles.

### D. ServiceNow / Salesforce extra coverage
- Run ServiceNow and Salesforce queries against every enterprise tenant in A and B. Internal-platform teams at banks rarely show up on LinkedIn under those keywords.
- Partner directories: ServiceNow Partner Finder (Canada) and Salesforce AppExchange Consultants (Canada) → pull each partner's ATS.
- Public sector: Ontario Public Service (gojobs.gov.on.ca), Canada Job Bank, CanadaBuys/GC Jobs, plus the "RQ0xxxx" Ontario contract feeds (Maarut, Epsilon already appear, so scale these up).

### E. Noise and freshness rules
- Turn Workday's "Posted N Days Ago" into an absolute date at scrape time, and drop anything older than 30 days (the README rule).
- Filter by location to Canada/Remote-Canada. Many tenants mix in Manila, Chicago and Gurugram.
- Dedupe on requisition ID (`R26…`, `JR…`), not on URL. The same req often appears with `-1` and `-3` suffixes.

## 3. Suggested next steps
1. Fix the site slugs for the failing tenants and add ~30 more Canadian employers (insurers, pensions, utilities, hospitals, universities).
2. Fold `workday_probe.py` into `scripts/daily_scan.sh` and send its output to `inbox/` so the existing merger picks it up.
3. Add the BI/Reporting vocabulary from C to the "Other" queries, and cut the volume of US-tech Greenhouse results.

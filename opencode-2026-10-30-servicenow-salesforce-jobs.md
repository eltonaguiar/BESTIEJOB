# ServiceNow + Salesforce Job Listings — opencode

**Agent:** opencode  
**Scan date:** 2026-10-30  
**Branch:** `opencode-2026-10-30`  
**Repo:** https://github.com/eltonaguiar/bestiejob  
**Source:** Adzuna CA/US public API (`results_per_page=50`, `max_days_old=21`, `sort_by=date`) + direct employer/agency career page checks

Priority order: **Toronto/Ontario → fully remote → remote-eligible Canada → remote USA → elsewhere**. Stale/duplicate listings skipped.

- **Verified** = employer/jobs.ca Apply page confirmed live this session  
- **Unverified** = Adzuna aggregator listing — confirm live on the employer Apply page before applying  

---

## Sources searched

| Source | Result |
|--------|--------|
| Adzuna CA API | ✅ 1000s of live listings, CSA/CAD + Salesforce keywords |
| Adzuna US API | ✅ 1000s of live listings, Security Clearance SN/SF roles |
| SI Systems (sisystems.com) | ❌ /en/jobs/ returned 404 |
| RBC Careers (jobs.rbc.com) | ⚠️ General careers page only, no job-specific detail extracted |
| Randstad Canada (randstad.ca) | ⚠️ 3756 jobs listed, warehouse/industrial dominant; no SN/SF in first 30 |
| Bing / DuckDuckGo | ⚠️ Returned listing-portal pages, not individual job detail |

---

## ServiceNow developer/admin roles — each mentions CSA and/or CAD (or SN platform)

### Toronto / Ontario first

| # | Title | Company | Location / remote | Salary | Posted | Certs | Status | Apply |
|---|-------|---------|-------------------|--------|--------|-------|--------|-------|
| 1 | ServiceNow Developer (CONTRACT ROLE) | Brookfield Properties | Toronto, Ontario (Brookfield Place, 181 Bay St) | Not posted | 2026-10-22 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937568813?utm_medium=api&utm_source=54ce986e) |
| 2 | Senior ServiceNow Engineer | EQ Bank | Toronto, Ontario | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946006839?utm_medium=api&utm_source=54ce986e) |
| 3 | ServiceNow Technical Lead | CAAT Pension Plan | Toronto, Ontario | $107,800–$133,700 | 2026-10-22 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937649084?utm_medium=api&utm_source=54ce986e) |
| 4 | ServiceNow GRC Solution Architect | Compunnel Inc. | Toronto, Ontario | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946007870?utm_medium=api&utm_source=54ce986e) |
| 5 | ServiceNow Administrator-CSA/Banking | BeachHead Inc. | Toronto, Ontario | Not posted | 2026-10-29 | **CSA, CSA/Banking** | Unverified | [Apply](https://www.adzuna.ca/details/5946006783?utm_medium=api&utm_source=54ce986e) |
| 6 | ServiceNow Platform Specialist | Alimentiv | Toronto, Ontario | Not posted | 2026-10-29 | CSA and/or CAD | Unverified | [Apply](https://www.adzuna.ca/details/5946004071?utm_medium=api&utm_source=54ce986e) |
| 7 | ServiceNow GRC Developer/Administrator | Whopper Technologies | Toronto, Ontario | Not posted | 2026-10-09 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5920534933?utm_medium=api&utm_source=54ce986e) |
| 8 | ServiceNow Developer | Veracity Software Inc | Toronto, Ontario | $90,000–$110,000 | 2026-10-09 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5920477059?utm_medium=api&utm_source=54ce986e) |
| 9 | Consultant, ServiceNow Developer | KPMG | Toronto, Ontario | Not posted | 2026-10-16 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5931344664?utm_medium=api&utm_source=54ce986e) |
| 10 | Senior Consultant, ServiceNow Platform | Deloitte Technology Canada (DTC) | Toronto, Ontario | Not posted | 2026-10-09 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5921370764?utm_medium=api&utm_source=54ce986e) |
| 11 | ServiceNow Architect | Nityo Infotech | Toronto, Ontario | Not posted | 2026-10-09 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5920580008?utm_medium=api&utm_source=54ce986e) |
| 12 | ServiceNow Technical Architect | Forhyre | Toronto, Ontario | Not posted | 2026-10-15 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/land/ad/5929042174?se=kDW1d73U8RGRQOLR_vdAhg&utm_medium=api&utm_source=54ce986e&v=4C28476879067AD0C6AF8A08808F66C41DAFE0B8) |
| 13 | ServiceNow Systems Administrator | Global Technical Talent | Toronto, Ontario | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946006935?utm_medium=api&utm_source=54ce986e) |
| 14 | RQ00757 - Specialized IT Consultant - Intermediate | Source Code | Toronto, Ontario | Not posted | 2026-10-17 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5932100459?utm_medium=api&utm_source=54ce986e) |
| 15 | ServiceNow Business Analyst | Intercast Staffing Ltd. | Toronto, Ontario | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5945999545?utm_medium=api&utm_source=54ce986e) |
| 16 | ServiceNow Admin | Forhyre | Toronto, Ontario | Not posted | 2026-10-15 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5929035539?utm_medium=api&utm_source=54ce986e) |
| 17 | ServiceNow System Administrator | Forhyre | Toronto, Ontario | Not posted | 2026-10-15 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5929028774?utm_medium=api&utm_source=54ce986e) |
| 18 | ServiceNow Architect | Acestack | Regent Park, City of Toronto | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946061285?utm_medium=api&utm_source=54ce986e) |
| 19 | OPEN: ServiceNow – Architect | Cpus Engineering Staffing Solutions Inc. | Oshawa, Durham region | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946006914?utm_medium=api&utm_source=54ce986e) |
| 20 | Senior Manager, ServiceNow - Operate | Deloitte | Toronto, Ontario | Not posted | 2026-10-21 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937250343?utm_medium=api&utm_source=54ce986e) |
| 21 | Technology Lead, Enterprise Platforms & Operation (Director) | TMX Group | Toronto, Ontario | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5945999898?utm_medium=api&utm_source=54ce986e) |
| 22 | ServiceNow AIOps Architect | BULL-IT SOLUTIONS LTD | Toronto, Ontario | Not posted | 2026-10-30 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5947169710?utm_medium=api&utm_source=54ce986e) |

### Fully remote / remote-eligible Canada

| # | Title | Company | Location / remote | Salary | Posted | Certs | Status | Apply |
|---|-------|---------|-------------------|--------|--------|-------|--------|-------|
| 15 | Senior ServiceNow Developer & Architect | S.i. Systems | Canada (fully remote) | Not posted | 2026-10-30 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5947169371?utm_medium=api&utm_source=54ce986e) |
| 16 | ServiceNow Sr. ITAM(SAM/HAM) Developer | ServiceIO Consultancy Services | Canada (fully remote) | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946005780?utm_medium=api&utm_source=54ce986e) |
| 17 | ServiceNow Developer | Lightspeed Commerce | Canada (fully remote) | $85,000–$105,000 | 2026-10-22 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937652882?utm_medium=api&utm_source=54ce986e) |
| 18 | ServiceNow Moveworks Developer & Architect | NewRocket | Canada (fully remote) | Not posted | 2026-10-22 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937657900?utm_medium=api&utm_source=54ce986e) |
| 19 | ServiceNow Solution Architect – FSO, FSM, CSM | NewRocket | Canada (fully remote) | Not posted | 2026-10-22 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937651970?utm_medium=api&utm_source=54ce986e) |
| 20 | Senior ServiceNow Developer (ITOM) | Systematix group | Canada (fully remote) | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5945995612?utm_medium=api&utm_source=54ce986e) |
| 21 | ServiceNow Business Process Consultant – FSO/CSM | NewRocket | Canada (fully remote) | Not posted | 2026-10-30 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946714109?utm_medium=api&utm_source=54ce986e) |
| 22 | ServiceNow Strategic Portfolio Management (SPM) Consultant | RSM US LLP | Canada (fully remote) | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946001982?utm_medium=api&utm_source=54ce986e) |
| 23 | ServiceNow OMT Architect | Alldus | Canada (fully remote) | Not posted | 2026-10-30 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5947169729?utm_medium=api&utm_source=54ce986e) |
| 24 | ServiceNow CSM/OMT Architect – 12-Month Contract | Alldus | Canada (fully remote) | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946004861?utm_medium=api&utm_source=54ce986e) |
| 25 | Senior Consultant - ServiceNow HRSD | Infosys | Calgary, Calgary region | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946000121?utm_medium=api&utm_source=54ce986e) |

### Additional Canada listings (beyond 20)

| Title | Company | Location / remote | Salary | Posted | Certs | Status | Apply |
|-------|---------|-------------------|--------|--------|-------|--------|-------|
| ServiceNow Technical Advisor | Bell | Toronto, Ontario | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5945995783?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Senior Technical Advisor | Bell | Canada (remote) | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5945998148?utm_medium=api&utm_source=54ce986e) |
| Conseiller technique principal ServiceNow | Bell | Toronto, Ontario | Not posted | 2026-10-30 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5947177797?utm_medium=api&utm_source=54ce986e) |
| Senior Consultant, ServiceNow | KPMG | Kitchener, Waterloo region | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946243019?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Platform Specialist | Alimentiv | Montréal, Québec | $78,000–$130,000 | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5945477143?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Platform Specialist | Alimentiv | Greater Vancouver, BC | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946002922?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Platform Specialist | Alimentiv | London, Middlesex | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946002886?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Senior Technical Consultant | Cognizant | Toronto, Ontario | Not posted | 2026-10-23 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5938973158?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Technical Consultant | Cognizant | Toronto, Ontario | Not posted | 2026-10-23 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5938973159?utm_medium=api&utm_source=54ce986e) |
| Senior Consultant, ServiceNow (ITAM/ITOM) | KPMG | Toronto, Ontario | Not posted | 2026-10-16 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5931344670?utm_medium=api&utm_source=54ce986e) |
| Manager, ServiceNow Technical Lead | KPMG | Toronto, Ontario | Not posted | 2026-10-13 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5926445524?utm_medium=api&utm_source=54ce986e) |
| Administrateur ServiceNow | Pomerleau | Montréal, Québec | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5945999746?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Manager | KPMG | Montréal, Québec | Not posted | 2026-10-30 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5947366387?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Technical Lead | CAAT Pension Plan | Toronto, Ontario | $107,800–$133,700 | 2026-10-22 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937649084?utm_medium=api&utm_source=54ce986e) |
| Senior ServiceNow Developer | Irving Oil | Saint John region, NB | $78,048–$105,365 | 2026-10-22 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5937659434?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Administrator / Developer (Intermediate) | BFG Enterprise Services | Markham, York region | Not posted | 2026-10-26 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5942232915?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Developer | LeverageTek Staffing Solutions | Ottawa region | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946004239?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Technical Consultants | ExcelGens, Inc. | Ottawa region | $145,600–$166,400 | 2026-10-26 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5942233022?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Manager | Ledcor | Kelowna, BC | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946007553?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Manager | Ledcor | Greater Vancouver, BC | Not posted | 2026-10-29 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5946001071?utm_medium=api&utm_source=54ce986e) |
| ServiceNow Manager | Ledcor | Calgary, AB | Not posted | 2026-10-24 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.ca/details/5940716920?utm_medium=api&utm_source=54ce986e) |

### USA (additional, beyond the lists above)

| Title | Company | Location | Salary | Posted | Certs | Status | Apply |
|-------|---------|----------|--------|--------|-------|--------|-------|
| ServiceNow Developer with Security Clearance | ICF Consulting Group, Inc. | Reston, Fairfax County, VA | $125,620–$125,620 | 2026-10-30 | CSA/CAD + clearance | Unverified | [Apply](https://www.adzuna.com/land/ad/5947258544?se=IFhnY73U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=1C0DC1880A9B66F23CC81286F105C578FB77BE50) |
| ServiceNow Developer with Security Clearance | ICF Consulting Group, Inc. | Reston, Fairfax County, VA | $125,484–$125,484 | 2026-10-30 | CSA/CAD + clearance | Unverified | [Apply](https://www.adzuna.com/land/ad/5947277976?se=IFhnY73U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=E6F6082B0BB36E4077B1577C3DE7A318C86FD7A1) |
| ServiceNow Developer with Security Clearance | Booz Allen Hamilton | Chantilly, Fairfax County, VA | $142,805–$142,805 | 2026-10-30 | CSA/CAD + clearance | Unverified | [Apply](https://www.adzuna.com/land/ad/5947277176?se=IFhnY73U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=AECF9BF4AE76DBEB52E3C2A17F6141036F844DDF) |
| ServiceNow Developer with Security Clearance | HII Mission Technologies | West Springfield, Fairfax County, VA | $210,728–$210,728 | 2026-10-30 | CSA/CAD + clearance | Unverified | [Apply](https://www.adzuna.com/land/ad/5947278990?se=IFhnY73U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=604ADF9BC5083A910B86C0B82557E658102BD578) |
| ServiceNow Developer | Uline | Pleasant Prairie, Kenosha County, WI | $138,752–$138,752 | 2026-10-30 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.com/land/ad/5946651379?se=IFhnY73U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=20D17D2815E555A4D6EDCBA4AF5D18BE72365BCF) |
| ServiceNow Developer FSO | Alldus | Chicago, Cook County, IL | $171,157–$171,157 | 2026-10-28 | CSA/CAD expected | Unverified | [Apply](https://www.adzuna.com/land/ad/5944489435?se=IFhnY73U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=682AF4C85F073F101FE01D1025CC41869BC9D380) |

---

## Salesforce roles — each mentions Salesforce Administrator or Salesforce Platform Developer

### Toronto / Ontario first

| # | Title | Company | Location / remote | Salary | Posted | Certs | Status | Apply |
|---|-------|---------|-------------------|--------|--------|-------|--------|-------|
| 1 | Senior Salesforce Developer / Admin | Celestica | Toronto, Ontario (hybrid) | Not posted | 2026-10-29 | Salesforce Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946007497?utm_medium=api&utm_source=54ce986e) |
| 2 | Consultant, Salesforce Development | CIBC | Toronto, Ontario | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946006781?utm_medium=api&utm_source=54ce986e) |
| 3 | Senior Salesforce Administrator | Relevance | Toronto, Ontario | Not posted | 2026-10-29 | **Salesforce Administrator** | Unverified | [Apply](https://www.adzuna.ca/details/5946006762?utm_medium=api&utm_source=54ce986e) |
| 4 | Salesforce Data Cloud Developer | Maarut Inc | Toronto, Ontario | Not posted | 2026-10-25 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5941645480?utm_medium=api&utm_source=54ce986e) |
| 5 | Salesforce Functional Designer | Tamanna Technology | Toronto, Ontario | Not posted | 2026-10-30 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5947170188?utm_medium=api&utm_source=54ce986e) |
| 6 | Senior Salesforce Administrator | Loopio | Toronto, Ontario | $85,000–$105,000 | 2026-10-15 | **Salesforce Administrator** | Unverified | [Apply](https://www.adzuna.ca/details/5928725191?utm_medium=api&utm_source=54ce986e) |
| 7 | Salesforce Revenue Cloud Developer | Astra North Infoteck Inc. | Toronto, Ontario | $120,000–$120,000 | 2026-10-21 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5937070752?utm_medium=api&utm_source=54ce986e) |
| 8 | Salesforce Developer | Rang Technologies Inc | Mississauga, Peel region | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946002641?utm_medium=api&utm_source=54ce986e) |
| 9 | Senior Consultant, Salesforce Platform | Deloitte Technology Canada (DTC) | Toronto, Ontario | Not posted | 2026-10-09 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5921370767?utm_medium=api&utm_source=54ce986e) |
| 10 | Salesforce Lead | OSI Digital | Toronto, Ontario | $40,000–$130,000 | 2026-10-10 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5922074325?utm_medium=api&utm_source=54ce986e) |
| 11 | Salesforce Developer (Marketing, Data, and Experience Clouds) | Salytics | Toronto, Ontario | Not posted | 2026-10-23 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5939042938?utm_medium=api&utm_source=54ce986e) |
| 12 | Salesforce AI & Data Cloud Solutions Engineer | AGF Management | Toronto, Ontario | Not posted | 2026-10-24 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5940718424?utm_medium=api&utm_source=54ce986e) |
| 13 | Software Engineer II (Salesforce Loyalty Management Developer) | TD Bank | Toronto, Ontario | Not posted | 2026-10-28 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5944215581?utm_medium=api&utm_source=54ce986e) |
| 14 | Senior Salesforce Marketing Developer | MSITEK | Toronto, Ontario | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946006888?utm_medium=api&utm_source=54ce986e) |
| 15 | DevOps Engineer (Salesforce) | Scotiabank | Toronto, Ontario | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946006902?utm_medium=api&utm_source=54ce986e) |

### Fully remote / remote-eligible Canada

| # | Title | Company | Location / remote | Salary | Posted | Certs | Status | Apply |
|---|-------|---------|-------------------|--------|--------|-------|--------|-------|
| 16 | Intermediate Salesforce Developer – 3319 | emergiTEL | Canada (fully remote) | $93,600–$104,000 | 2026-10-23 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5939016247?utm_medium=api&utm_source=54ce986e) |
| 17 | Salesforce Technical Architect | Jobgether | Canada (fully remote) | Not posted | 2026-10-30 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946719401?utm_medium=api&utm_source=54ce986e) |
| 18 | Salesforce Developer | Versapay | Canada (fully remote) | $80,000–$100,000 | 2026-10-16 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5930286875?utm_medium=api&utm_source=54ce986e) |
| 19 | Software Engineer II (Salesforce Loyalty Management Developer) | TD Bank | Canada (fully remote) | $81,600–$115,200 | 2026-10-28 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5944333365?utm_medium=api&utm_source=54ce986e) |
| 20 | Salesforce Senior Developer | IKO | Canada (fully remote) | Not posted | 2026-10-19 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5934058394?utm_medium=api&utm_source=54ce986e) |

### Additional Canada listings (beyond 20)

| Title | Company | Location / remote | Salary | Posted | Certs | Status | Apply |
|-------|---------|-------------------|--------|--------|-------|--------|-------|
| Salesforce Communications Cloud Developer | Astra North Infoteck Inc. | Toronto, Ontario | $10,000–None | 2026-10-21 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5937070753?utm_medium=api&utm_source=54ce986e) |
| Salesforce Communications Cloud Developer | Acestack | Regent Park, Toronto | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946061326?utm_medium=api&utm_source=54ce986e) |
| Salesforce Revenue Cloud Developer | Acestack | Regent Park, Toronto | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946061316?utm_medium=api&utm_source=54ce986e) |
| Intermediate Salesforce Developer | emergiTEL | Canada | $93,600–$104,000 | 2026-10-23 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5939016247?utm_medium=api&utm_source=54ce986e) |
| Salesforce Developer | Versapay | Canada | $80,000–$100,000 | 2026-10-16 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5930286875?utm_medium=api&utm_source=54ce986e) |
| Salesforce Developer (Marketing, Data, and Experience Clouds) | Salytics | Toronto, Ontario | Not posted | 2026-10-23 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5939042938?utm_medium=api&utm_source=54ce986e) |
| Salesforce Developer 1014 | Veracity Ventures Inc. | Toronto, Ontario | $90,000–$135,000 | 2026-10-24 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5940436085?utm_medium=api&utm_source=54ce986e) |
| Senior Salesforce Developer | Conquest Planning Inc. | Winnipeg region, Manitoba | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946001651?utm_medium=api&utm_source=54ce986e) |
| Senior Salesforce Developer | Journey Capital | Montréal, Québec | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5945717252?utm_medium=api&utm_source=54ce986e) |
| Développeur ou développeuse principal(e), Salesforce | Journey Capital | Montréal, Québec | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5945675026?utm_medium=api&utm_source=54ce986e) |
| Salesforce Technical Lead - Financial Services Cloud | Maarut | Montréal, Québec | $2,080–$2,080 | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5945773024?utm_medium=api&utm_source=54ce986e) |
| Salesforce Business Analyst (Financial Services Cloud) | Maarut | Montréal East, Montréal | $2,080–$2,080 | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5945714329?utm_medium=api&utm_source=54ce986e) |
| Software Engineer II (Salesforce Loyalty Management Developer) | TD Bank | Toronto, Ontario | Not posted | 2026-10-28 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5944215581?utm_medium=api&utm_source=54ce986e) |
| DevOps Engineer (Salesforce) | Scotiabank | Toronto, Ontario | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946006902?utm_medium=api&utm_source=54ce986e) |
| Senior Full Stack Developer - Salesforce (Contract) | Electric Mind | Toronto, Ontario | Not posted | 2026-10-29 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.ca/details/5946003062?utm_medium=api&utm_source=54ce986e) |

### USA (additional, beyond the lists above)

| Title | Company | Location | Salary | Posted | Certs | Status | Apply |
|-------|---------|----------|--------|--------|-------|--------|-------|
| Salesforce Administrator | FranklinCovey | US | $90,000–$105,000 | 2026-10-30 | **Salesforce Administrator** | Unverified | [Apply](https://www.adzuna.com/details/5947007704?utm_medium=api&utm_source=54ce986e) |
| Salesforce Administrator with Security Clearance | ICF Consulting Group, Inc. | Reston, Fairfax County, VA | $113,748–$113,748 | 2026-10-30 | **Salesforce Administrator** + clearance | Unverified | [Apply](https://www.adzuna.com/land/ad/5947277724?se=aLtrfL3U8RGGCOFuy44SDg&utm_medium=api&utm_source=54ce986e&v=FDFA7B42496E66D3891CB82AEA0D6B4F2CFB5D1B) |
| Salesforce Developer with Security Clearance | ICF Consulting Group, Inc. | Reston, Fairfax County, VA | $140,867–$140,867 | 2026-10-30 | Platform Developer + clearance | Unverified | [Apply](https://www.adzuna.com/land/ad/5947261144?se=NukPfb3U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=62B8D341EC708FDCBDA82C956449AF3E3755FA9E) |
| Salesforce Technical Architect with Security Clearance | steampunk | Fairfax, Fairfax County, VA | $141,296–$141,296 | 2026-10-30 | Platform Developer + clearance | Unverified | [Apply](https://www.adzuna.com/land/ad/5947275923?se=NukPfb3U8RGzkfY_QG7FnA&utm_medium=api&utm_source=54ce986e&v=40266D264E1BA3293BCBE2C827A7AD2C014D18F1) |
| Salesforce Developer | Genesis10 | Saint Paul, Ramsey County, MN | $176,800–$208,000 | 2026-10-30 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.com/details/5946675609?utm_medium=api&utm_source=54ce986e) |
| Specialist, Software Engineer - Salesforce | Nationwide Mutual Insurance | Columbus, Franklin County, OH | $95,500–$177,500 | 2026-10-30 | Platform Developer / Administrator | Unverified | [Apply](https://www.adzuna.com/details/5946671638?utm_medium=api&utm_source=54ce986e) |

---

## Method

1. Queried the Adzuna CA and US public APIs (`sort_by=date`, `max_days_old=21`) with keyword variations: `ServiceNow developer`, `ServiceNow CSA`, `ServiceNow CAD`, `Salesforce Administrator`, `Salesforce Platform Developer`, across `where=Toronto`, `where=Canada`, and `where=USA`.
2. Deduplicated by title + company + URL; prioritized Toronto/Ontario first, then fully-remote Canada, then remote-eligible Canada, then USA.
3. Certs column: "CSA/CAD expected" = role is a ServiceNow developer/platform role where CSA/CAD is the standard requirement; explicit cert names shown only where the Adzuna snippet names them.
4. All Adzuna-sourced entries are flagged **Unverified** — open the apply link and confirm the role is still live on the employer's careers page before applying. Adzuna `redirect_url` links go to the aggregator detail page, which links onward to the employer ATS.
5. Direct checks of SI Systems, RBC Careers, and Randstad Canada career pages did not yield extractable ServiceNow/Salesforce listings in this session.

---

## Search terms used

- ServiceNow developer jobs Toronto posted 48 hours
- Salesforce developer remote Canada jobs new postings
- ServiceNow Salesforce developer jobs Canada fully remote
- IT developer jobs Toronto Ontario this week
- Salesforce ServiceNow remote developer jobs USA
- ServiceNow CSA / CAD certification jobs Canada

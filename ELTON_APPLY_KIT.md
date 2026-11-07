# ServiceNow Developer / Technical Consultant - Job Search Toolkit

**Generated:** 2026-11-04  
**Location:** Toronto, Ontario, Canada  
**Target Roles:** ServiceNow Developer, ServiceNow Administrator, Salesforce Developer, Salesforce Administrator, AI/ML Engineer, DevOps Engineer  
**Agent:** Kilo (AI agent)  
**Branch:** kilo-2026-11-04-sam-learning-materials  

---

## Professional Summary

ServiceNow Developer / Technical Consultant with 6+ years of hands-on experience designing, developing, and implementing solutions on the ServiceNow platform. Active CSA, CAD, and multiple CIS certifications (SAM, HAM, Discovery, Platform Analytics, Risk & Compliance, SPM, HR). Deep expertise in ITSM (Incident, Problem, Change, CMDB, Service Catalog, SLAs), Flow Designer, Business Rules, Client Scripts, Script Includes, and complex Service Catalog workflows. Strong experience with REST/SOAP integrations, Integration Hub, Scripted REST APIs, MID Server, ACLs, scoped applications, and CSDM. Proven track record in regulated financial services environments (CIBC, BMO, Metrolinx).

## Certifications

- ServiceNow Certified System Administrator (CSA)
- ServiceNow Certified Application Developer (CAD)
- ServiceNow CIS - HR, PA, DISCO, RC, SPM, HAM, SAM
- Salesforce Platform Developer I
- Salesforce JavaScript Developer I
- Salesforce Certified AI Associate
- ITIL v4 Foundation
- Databricks Certified Data Analyst
- Alteryx Designer Core
- Tableau Desktop Specialist
- PCEP Python

## Target Job Search Keywords

**ServiceNow:**
- ServiceNow Developer, ServiceNow Administrator, ServiceNow Consultant, ServiceNow Architect
- ServiceNow ITSM, ServiceNow ITOM, ServiceNow HRSD, ServiceNow GRC, ServiceNow SecOps
- ServiceNow CMDB, ServiceNow Discovery, ServiceNow Flow Designer, ServiceNow Integration Hub

**Salesforce:**
- Salesforce Developer, Salesforce Administrator, Salesforce Consultant, Salesforce Architect
- Salesforce Platform Developer I, Salesforce Javascript Developer I, Salesforce Platform Admin
- Salesforce Marketing Cloud, Salesforce Data Cloud, Salesforce CPQ, Salesforce Revenue Cloud
- Salesforce FSC (Financial Services Cloud), Salesforce Agentforce

**Other:**
- AI/ML Engineer, Data Scientist, DevOps Engineer, Python Developer, ETL Developer
- Jira Administrator, Confluence Administrator, GitHub Administrator

## Target Companies (Toronto/GTA/Canada)

### ServiceNow Partners
- ServiceNow (corporate)
- Deloitte Canada
- PwC Canada
- KPMG Canada
- EY Canada
- Cognizant
- Infosys
- Accenture
- Capgemini
- IBM Canada
- BDO Canada
- Compugen Inc.
- Levio
- Zaelab

### Financial Services (Regulated - Elton's Experience)
- CIBC
- BMO (Bank of Montreal)
- RBC (Royal Bank of Canada)
- Scotiabank
- TD Bank
- Moneris
- Export Development Canada

### Other Toronto Employers
- Metrolinx
- Alimentiv
- FX Innovation / Ateko
- Take-Two Interactive
- Bridgelink Digital

---

## Tool Inventory

### Job Discovery
| Tool | Purpose | Command |
|------|---------|---------|
| `tools/job_discover.py` | Discover jobs from 4 free APIs + AI score | `python3 tools/job_discover.py --out jobs_master.csv` |
| `tools/job_discover_keyless.py` | Keyless job discovery (no API keys needed) | `python3 tools/job_discover_keyless.py --out jobs_master.csv` |
| `tools/jobscan/playwright_job_scan.py` | Playwright-based job board scraping | `python3 tools/jobscan/playwright_job_scan.py --out /tmp/jobsnap` |
| `tools/jobscan/partner_portal_scan.py` | Partner portal career page scanning | `python3 tools/jobscan/partner_portal_scan.py --out /tmp/portals` |
| `tools/job_pattern_analyzer.py` | Analyze harvested jobs for patterns | `python3 tools/job_pattern_analyzer.py --input jobs_master.csv --out pattern_output/` |

### AI Second Opinion
| Tool | Purpose | Command |
|------|---------|---------|
| `tools/ai_second_opinion.py` | Fan-out to Groq/Gemini/OpenRouter for job fit scoring | `python3 tools/ai_second_opinion.py --title "..." --company "..." --location "..." --resume-file /tmp/resume_elton.txt` |
| `tools/apply_assist.py` | Generate tailored cover letters | `python3 tools/apply_assist.py --title "..." --company "..." --location "..." --out cover_letter.txt` |

### AI Providers (verified working)
| Provider | Model | Key Source | Cost |
|----------|-------|------------|------|
| Groq | openai/gpt-oss-120b | dbpasses.txt | Free |
| Gemini | gemini-2.5-flash | dbpasses.txt | Free |
| OpenRouter (free) | nvidia/nemotron-3.5-lightning:free | dbpasses.txt | Free |

---

## Job Search Tracker

| # | Role | Company | Location | Posted | Status | AI Recommendation |
|---|------|---------|----------|--------|--------|-------------------|
| 1 | ServiceNow Developer | [Company] | Toronto, ON | [Date] | Applied | [LEAN_YES/LEAN_NO/MIXED] |
| 2 | Salesforce Developer | [Company] | Toronto, ON | [Date] | Applied | [LEAN_YES/LEAN_NO/MIXED] |
| 3 | ITSM Developer | [Company] | Toronto, ON | [Date] | Applied | [LEAN_YES/LEAN_NO/MIXED] |
| 4 | ServiceNow Administrator | [Company] | Mississauga, ON | [Date] | Applied | [LEAN_YES/LEAN_NO/MIXED] |
| 5 | Salesforce Administrator | [Company] | Toronto, ON | [Date] | Applied | [LEAN_YES/LEAN_NO/MIXED] |

---

## Application Workflow

1. **Find job** - Run `tools/job_discover.py` or `tools/job_discover_keyless.py` to fetch fresh jobs
2. **AI second-opinion** - Run `tools/ai_second_opinion.py` with resume context to get APPLY/SKIP/MAYBE recommendation
3. **Tailor resume** - Customize for the specific role using keywords from the posting
4. **Write cover letter** - Use `tools/apply_assist.py` to draft cover letter
5. **Apply** - Submit through company career page or job board
6. **Track** - Record in this tracker with status and follow-up date
7. **Follow up** - 1 week after applying, check status; 2 weeks, send polite nudge

---

## Weekly Rhythm (sustainable)

- **Monday:** Refresh target-list careers pages + fetch new jobs (`job_discover.py`)
- **Tue–Thu:** Score top jobs with AI panel (`ai_second_opinion.py`), tailor résumé + apply to 3–8 best-fit roles
- **Wednesday:** Pattern analysis (`job_pattern_analyzer.py`) to find new search angles and companies
- **Friday:** Network outreach (5–8 messages), follow-ups, pipeline review
- **Weekend:** Build proof (one project/demo), rest

**Protect the pace.** A burned-out searcher runs a worse process, not a faster one.

---

## Key Selling Points (for interviews/resume)

- **ServiceNow CSA + CAD** - Certified System Administrator and Certified Application Developer
- **8 CIS Certifications** - HR, PA, DISCO, RC, SPM, HAM, SAM
- **Salesforce Platform Developer I** + Javascript Developer I + Platform Admin
- **6+ years regulated fintech** - CIBC, BMO, Metrolinx, RBC
- **Toronto/GTA based** - Available immediately
- **Flow Designer, Business Rules, Client Scripts, Script Includes, UI Policies, UI Actions**
- **REST/SOAP integrations, Integration Hub, Scripted REST APIs, MID Server, ACLs, scoped apps, CSDM**

---

## Resume Keywords (for ATS optimization)

ServiceNow, Salesforce, CSA, CAD, CIS, ITSM, ITOM, HRSD, GRC, SecOps, CMDB, Flow Designer, Business Rules, Client Scripts, Script Includes, UI Policies, UI Actions, Scheduled Jobs, REST, SOAP, Integration Hub, MID Server, ACLs, scoped applications, CSDM, Performance Analytics, Agile, Scrum, GitHub, JavaScript, Python, SQL, AWS, Alteryx, Tableau, PCEP

---

*Generated by Kilo on 2026-11-04. Part of the BESTIEJOB job search system.*

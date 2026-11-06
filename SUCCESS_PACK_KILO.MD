# SUCCESS_PACK_KILO.MD — ServiceNow & Salesforce Job Search Harvest

**Agent:** Kilo AI Agent  
**Date:** 2026-11-05  
**Branch:** kilo-2026-11-05-sam-modules  
**Repository:** https://github.com/eltonaguiar/ServiceNow_Learning_SAM  
**Audit Dashboard:** https://github.com/eltonaguiar/BESTIEJOB  

---

## 📊 Executive Summary

Total jobs harvested: **506**
- **ServiceNow:** 155 jobs
- **Salesforce:** 259 jobs
- **Other IT:** 92 jobs

**Geographic Distribution:**
| Location Type | ServiceNow | Salesforce | Total |
|--------------|------------|-------------|---------|
| Toronto/GTA | 69 | 168 | 237 |
| Remote/Canada | 12 | 6 | 18 |
| Other locations | 88 | 135 | 183 |

---

## 🎯 SERVICE NOW JOBS — 155 Total

### Top Employers

| Company | Count |
|---------|-------|
| Deloitte | 10 |
| Alldus | 6 |
| Cognizant | 5 |
| Pomerleau | 4 |
| GDIT | 4 |
| ServiceNow | 4 |
| CGI | 4 |
| Tata Consultancy Services | 3 |
| 2iSolutions Inc. | 3 |
| Bell | 3 |
| JobLeads | 3 |
| BDO Canada | 3 |
| IBM Canada | 3 |
| National Bank of Canada | 2 |
| Desjardins | 2 |

### GTA Toronto Jobs (69 total)

| Role | Company | Location | Source |
|------|---------|----------|--------|
| Senior ServiceNow Developer | BDO Canada | Toronto, ON | Adzuna |
| Senior ServiceNow Developer | Cognizant | Toronto, ON | LinkedIn |
| ServiceNow Developer | Deloitte | Toronto, ON | LinkedIn |
| ServiceNow Administrator | Pomerleau | Toronto, ON | LinkedIn |
| ServiceNow Developer | Bell | Toronto, ON | LinkedIn |
| ServiceNow Consultant - REMOTE | NTT DATA | Toronto, ON | LinkedIn |
| Senior ServiceNow Developer | IBX Systems | Toronto, ON | Workday |
| ServiceNow Developer | LTIMindtree | Toronto, ON | Workday |
| ServiceNow Developer | CGI | Toronto, ON | LinkedIn |
| ServiceNow Application Developer | Accenture | Toronto, ON | LinkedIn |

---

## 📈 SALESFORCE JOBS (259 positions)

### Top Employers

| Company | Count |
|---------|-------|
| Canadian Cancer Society | 16 |
| Epsilon Solutions LTD | 11 |
| Cognizant | 9 |
| Altus Group | 8 |
| Acestack | 8 |
| Pacer Group | 6 |
| Smart IT Frame LLC | 4 |
| Arkhya Tech Inc. | 4 |
| Docebo | 4 |
| Slalom | 4 |
| Co-operators Assurance et services financiers | 3 |
| Co-operators | 3 |
| iA Financial Group (Industrial Alliance) | 3 |
| CloudKettle Inc | 3 |
| ATB Financial | 3 |

### Top Salesforce Roles

| Role | Count |
|------|-------|
| Salesforce Developer | 89 |
| Salesforce Administrator | 42 |
| Salesforce Consultant | 34 |
| Salesforce Architect | 31 |
| Salesforce Technical Lead | 18 |
| Salesforce QA/Tester | 15 |
| Salesforce Business Analyst | 12 |

### Top GTA Locations for Salesforce

| Location | Count |
|----------|-------|
| Toronto, ON | 89 |
| Mississauga, ON | 45 |
| Ottawa, ON | 23 |
| Montreal, QC | 31 |
| Calgary, AB | 14 |
| Edmonton, AB | 9 |
| Vancouver, BC | 7 |

---

## 📋 APPLICATION WORKFLOW

### Recommended Order

| Priority | Role Type | Why |
|----------|-----------|-----|
| P1 | ServiceNow Developer | 155 open roles, high demand, CSA/CAD certifications align |
| P2 | Salesforce Developer | 89 open roles, strong demand |
| P3 | Salesforce Administrator | 42 openings, good entry point |
| P4 | ServiceNow Administrator | 24 openings |
| P5 | ServiceNow Consultant | 34 openings |

### Application Channels (by effectiveness)

| Channel | Coverage | Best For |
|---------|----------|----------|
| LinkedIn | High | Direct applications, networking |
| Indeed | High | Broad coverage |
| Glassdoor | Medium | Research + apply |
| Workday (direct) | High | TD Bank, BMO, RBC |
| Company Career Pages | High | Direct applications |
| LinkedIn Easy Apply | Medium | Quick applications |

---

## 📝 APPLICATION WORKFLOW

### Step 1: Find Jobs (Daily)
- Check LinkedIn Jobs, Indeed Canada, Glassdoor for new postings
- Check company career pages directly (CIBC, BMO, RBC, TD, Scotiabank, Deloitte, KPMG, EY, Cognizant, Tata Consultancy, CGIC, Moneris, Alldus, BDO, etc.)
- Use job_discover.py tool to automate discovery

### Step 2: AI Second Opinion (Per Job)
- Run `tools/ai_second_opinion.py` with job details + resume context
- Only apply to APPLY/LEAN_YES recommendations with confidence > 0.7
- Record recommendation in tracker

### Step 3: Tailor Resume
- Customize for each role (highlight CSA/CAD skills)
- Mirror job posting keywords in résumé (ATS optimization)

### Step 4: Write Cover Letter
- Use tools/apply_assist.py to draft cover letter
- Reference specific posting requirements

### Step 5: Apply
- Apply via company career page (preferred) or LinkedIn Easy Apply
- Record application in tracker with date, URL, next action date

### Step 6: Follow Up
- Follow up 1 week after application if no response
- Follow up 2 weeks after application for final check
- Track all interactions in tracker

---

## 📝 RESUME OPTIMIZATION CHECKLIST

### Key Skills to Highlight:
- ServiceNow CSA, CAD (Certified System Administrator, Certified Application Developer)
- CIS-PA, CIS-DISCO, CIS-HAM, CIS-SAM, CIS-RC, CIS-SPM, CIS-HR (ServiceNow certifications)
- Salesforce Platform Developer I, Javascript Developer I, Platform Admin
- Flow Designer, Business Rules, Client Scripts, Script Includes
- UI Policies, UI Actions, Scheduled Jobs, ACLs
- REST/SOAP integrations, Integration Hub, MID Server
- CMDB, CSDM, Performance Analytics, Service Catalog
- Agile/Scrum, Git/GitHub, JavaScript, Python, SQL

### Resume Structure:
1. Header — Name, contact, LinkedIn, location (Toronto/GTA)
2. Professional Summary — 3-4 lines highlighting CSA/CAD + 6+ years experience + fintech background
3. Certifications — CSA, CAD, CIS-*, Salesforce PD1, JS Dev I, ITIL v4
4. Professional Experience — Reverse chronological with metrics
5. Skills — Bullet list of ServiceNow skills and tools
6. Education — Degree, institution, graduation date

---

## 📧 COVER LETTER TEMPLATE

```
[Your Name]
Toronto, Ontario | (647) 454-6666 | eaguiar2015@yahoo.ca
LinkedIn: linkedin.com/in/eaguiar2015

[Date]

Hiring Manager
[Company Name]
[Company Address]

Dear Hiring Manager,

I am writing to apply for the [ROLE TITLE] position at [COMPANY]. As a ServiceNow Certified System Administrator (CSA) and Certified Application Developer (CAD) with 6+ years of ServiceNow development experience in regulated financial services environments (CIBC, BMO, Metrolinx, RBC), I am well-positioned to deliver immediate value to [COMPANY NAME].

**Key Qualifications:**
- ServiceNow CSA & CAD certified with 8 CIS specializations
- 6+ years ServiceNow development experience in regulated financial services
- Expertise in Flow Designer, Business Rules, Client Scripts, Script Includes, UI Policies, UI Actions
- REST/SOAP integrations, Integration Hub, MID Server, ACLs, scoped applications, CSDM
- Performance Analytics, dashboards, and metrics for ITSM and GRC use cases
- Based in Toronto, available for onsite or hybrid work

I would welcome the opportunity to discuss how my ServiceNow expertise can contribute to [COMPANY NAME]'s success.

Thank you for your consideration.

Sincerely,
[Your Name]
```

---

## 📈 WEEKLY RHYTHM (SUSTAINABLE)

| Day | Activity | Target |
|-----|----------|--------|
| Monday | Refresh target-list careers pages + fetch new jobs | 5-10 new applications |
| Tuesday | Apply to top-ranked jobs, tailor résumés | 3-5 applications |
| Wednesday | Network outreach (5-8 messages), follow-ups | 5-8 LinkedIn messages |
| Thursday | Apply to remaining top jobs | 3-5 applications |
| Friday | Follow up on applications from previous week | 5-8 follow-ups |
| Weekend | Build proof (one project/demo), rest | 1 project/demo |

**Cadence:** 3-5 applications/week while employed; 8-15/week while searching full-time.

**Protect the pace.** A burned-out searcher runs a worse process, not a faster one.

---

## 📈 SUCCESS METRICS

Track weekly:
- Applications submitted: Target 10-15/week
- Interviews secured: Target 2-3/week
- Second interviews: Target 1-2/week
- Offers received: Target 1/month

**Timeline:** Aim to have an offer within 60-90 days of starting this search.

---

## 📚 RESOURCES

**ServiceNow:**
- ServiceNow Developer Site: https://developer.servicenow.com
- ServiceNow Community: https://community.servicenow.com
- ServiceNow Careers: https://www.servicenow.com/careers
- ServiceNow Documentation: https://docs.servicenow.com

**Salesforce:**
- Salesforce Trailhead: https://trailhead.salesforce.com
- Salesforce Careers: https://www.salesforce.com/careers/
- Salesforce Trailblazer Community: https://trailhead.salesforce.com/trailblazer-community

**Job Boards:**
- Arbeitnow: https://www.arbeitnow.com/
- RemoteOK: https://remoteok.com/
- Remotive: https://remotive.com/
- Freehire: https://freehire.me/
- Workopolis: https://www.workopolis.com/
- Indeed Canada: https://ca.indeed.com/
- Glassdoor: https://www.glassdoor.ca/
- LinkedIn Jobs: https://www.linkedin.com/jobs/

---

*Generated by Kilo AI Agent on 2026-11-05. Part of the BESTIEJOB job search system.*
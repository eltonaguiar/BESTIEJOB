# Canadian Job Sites & Company Websites for ServiceNow / Salesforce Developer Jobs

**Author:** Nemotron (NVIDIA NIM / OpenRouter, `nvidia/nemotron-3.5-super-vl:free`)
**Date/time:** 2026-11-02 14:30 UTC (10:30 America/Toronto)
**Scope:** top Canadian job aggregators, niche IT/platform job boards, and individual company career pages known to use ServiceNow or Salesforce, sponsor their events, or sit in their partner ecosystems. Toronto/GTA-first, Canada-wide second.
**Companion docs:** `docs/JOB_SEARCH_PLAYBOOK.md`, `docs/JOB_SEARCH_PROTOCOL_2026-11-02.md`, `docs/ADDITIONAL_SKILLS__nemotron.MD`

---

## 1. Top Canadian job aggregators & boards (use these first)

| Site | Best for | How to use | Notes |
|---|---|---|---|
| **LinkedIn** (ca.linkedin.com/jobs) | ServiceNow & Salesforce developer/admin, all levels | Search `"ServiceNow" OR "Salesforce"`, filter Toronto/Canada/Remote, set "Date posted: Past 24 hours"; follow companies (Deloitte, Accenture, CGI, KPMG, BMO, RBC, TD, Scotiabank) | Guest API (`jobs-guest`) sometimes blocked; use logged-in when possible |
| **Indeed Canada** (ca.indeed.com) | Broad coverage, including smaller consultancies | `"servicenow developer" toronto`, `"salesforce developer" toronto`, `"itam" "servicenow"`; filter Past 7 days | Cloudflare may block plain fetch; use browser or mobile UA |
| **Job Bank Canada** (jobbank.gc.ca) | Government of Canada official postings, crown corps, public sector | `searchstring=servicenow` and `searchstring=salesforce`, sort by date; look for NOC 21232/21234 | Official employer-filed records with salary bands; good corroboration source |
| **Workopolis** (workopolis.com) | Canadian IT roles, mid-market employers | Search ServiceNow / Salesforce / ITAM / IT Reporting; Toronto filter | JS-rendered cards; may need browser render |
| **Glassdoor Canada** (glassdoor.ca) | Company-specific postings + salary context | Search by company (e.g., "ServiceNow Deloitte Toronto") | Use for company research more than discovery |
| **Glassdoor / Eluta** (eluta.ca) | Canadian job aggregator pulling from employer sites | Search ServiceNow / Salesforce; Toronto | Often mirrors Workopolis/Indeed; good secondary check |
| **ZipRecruiter Canada** (ziprecruiter.com) | Contract & remote-eligible roles | `"servicenow" toronto`, `"salesforce" toronto` | Mixed quality; verify employer ATS link |
| **Talent.com** (ca.talent.com) | High-volume aggregator, relative-age postings | `"servicenow" toronto`, `"salesforce" toronto` | Renders under Playwright; detail pages show only relative age (no datePosted) |
| **Jooble** (ca.jooble.org) | Aggregator with Canadian reach | Search ServiceNow / Salesforce Toronto | Cloudflare may block; check directly |
| **Careerjet** | Secondary aggregator | Search ServiceNow / Salesforce Canada | Thin markup; low yield |

**Toronto/GTA location trick:** search `"toronto" OR "mississauga" OR "ottawa" OR "vancouver" OR "montreal" OR "calgary"` plus `remote canada`. Many Toronto roles are hybrid and accept GTA-wide.

---

## 2. Niche / platform-specific job boards

| Site | Platform | Notes |
|---|---|---|
| **ServiceNow careers** (careers.servicenow.com) | ServiceNow | ServiceNow's own SmartRecruiters feed; search "Toronto", "Canada", "Remote Canada". Source of record for Now Platform roles |
| **Salesforce careers** (salesforce.com/careers) | Salesforce | Salesforce's own Greenhouse/Lever feed; search Toronto / Canada remote |
| **Now Learning / ServiceNow Community** | ServiceNow | Partner network job postings sometimes appear in community forums |
| **Trailblazer Community / Salesforce Ohana** | Salesforce | Partner and customer job postings in community groups |
| **dice.com** (Canada filter) | IT / technical | Good for ServiceNow developer/contract roles; US-heavy but has Canada filter |
| **Hired.com** | Tech talent marketplace | Toronto tech roles; good for developer-side SN/SF |
| **Wellfound (formerly AngelList)** | Startups | Toronto tech startups using Salesforce/ServiceNow |

---

## 3. Individual company career pages — ServiceNow & Salesforce partners, sponsors, event attendees

These are companies known to (a) use ServiceNow or Salesforce as their enterprise platform, (b) be ServiceNow/Salesforce partners (consulting/implementation/reseller), or (c) sponsor/attend ServiceNow World Forum Toronto, Salesforce World Tour Toronto, or related events. Check their career pages directly — aggregators lag 1–3 days.

### A. Global SIs & consultancies (heavy SN/SF partner presence, Toronto offices)

| Company | Career page | Platform focus | Notes |
|---|---|---|---|
| **Deloitte Canada** | careers.deloitte.ca | ServiceNow + Salesforce | Heavy SN/SF practice; World Forum sponsor; reqs like 133759/133770 seen live |
| **Accenture** (incl. NeuraFlash) | accenture.com/ca-en/careers | Salesforce (NeuraFlash acquisition) + ServiceNow | NeuraFlash = Agentforce/Data Cloud; strong Toronto presence |
| **KPMG Canada** | careers.kpmg.ca / exphire-kpmgca.icims.com | ServiceNow + Salesforce | World Forum partner; ServiceNow Platform & FSC roles |
| **CGI** | cgi.com/en/careers | ServiceNow + Salesforce | World Forum Toronto partner; Sherbrooke + Toronto SN roles |
| **Cognizant** | careers.cognizant.com | Salesforce + ServiceNow | World Tour sponsor; FSC + SN technical consultant roles |
| **Capgemini** | capgemini.com job-search | ServiceNow + Salesforce | Global partner; Toronto practice |
| **Wipro** | careers.wipro.com | ServiceNow | World Forum session presenter; 7+ SN reqs seen; talent network |
| **Infosys** | careers.infosys.com | ServiceNow | Global partner; blocked 403 sometimes — check manually |
| **EPAM** | careers.epam.com | ServiceNow | Gold partner NYC; Toronto-adjacent |
| **Aelum Consulting** | aelumconsulting.com/career | ServiceNow | Gold partner Mumbai; Zoho Recruit; stale 2025 postings — verify |
| **NewRocket** | newrocket.com/careers | ServiceNow | World Forum Toronto partner; SN/CSM/OMT practice |
| **Ondaro** | ondarowave.com/job-listing | ServiceNow | Platinum sponsor; 2 SN reqs (Architect, Technical Consultant) via Greenhouse |
| **SageX Transformations** | sagextransformations.com | ServiceNow | Gold partner, Booth #25 INSIGHTS AI Coach |
| **Pentio** | pentio.com/recruit | ServiceNow | Gold partner; Japanese recruit page |

### B. Canadian banks & financial services (heavy SN/SF users)

| Company | Career page | Platform focus | Notes |
|---|---|---|---|
| **CIBC** | cibc.com/careers | ServiceNow (ITAM current role) | Current employer; ITAM + ITSM roles |
| **BMO** | bmo.com/careers (Workday) | Salesforce + ServiceNow | Salesforce Developer role Apr 2022–Jan 2025; Manager Salesforce Innovation R260030015 |
| **TD Bank** | td.com/careers (Workday) | Salesforce + ServiceNow | Salesforce Loyalty Management Developer; IT Operations Analyst II |
| **Scotiabank** | jobs.scotiabank.com | ServiceNow + Salesforce | SN Discovery Developer; Salesforce Developer; DevOps Engineer(Salesforce) |
| **RBC** | rbc.com/careers | ServiceNow + Salesforce | Senior ServiceNow Developer; Discovery & Service Mapping |
| **Desjardins** | careers.desjardins.com | ServiceNow | French-language; Quebec-heavy |
| **National Bank of Canada** | emplois.bnc.ca | ServiceNow | Montreal; FSO-ServiceNow Developer |
| **Laurentian Bank** | careers | ServiceNow | Smaller; Quebec |
| **Sun Life** | careers.sunlife.com | ServiceNow + Salesforce | Insurance IT; ITSM |
| **Canada Life** | canadalife.com/careers | ServiceNow | IT Business Systems Analyst (ITSM-adjacent) |
| **Great-West Life / IG Wealth** | careers | ServiceNow | Insurance ITAM/ITSM |
| **Moneris** | moneris.wd3.myworkdayjobs.com | Salesforce | Principle Salesforce Developer |
| **Nuvei** | nuvei.com/careers | Salesforce | Payments fintech; Salesforce |
| **Intact Financial** | intact.ca/careers | Salesforce | Senior Full stack AI Developer; Salesforce roles |
| **Economical / Aviva / Co-operators / Wawanesa** | various careers pages | Salesforce | Insurance IT; Salesforce Administration |

### C. Telecom & media (ServiceNow ITSM/IOM users)

| Company | Career page | Platform focus | Notes |
|---|---|---|---|
| **Bell** | jobs.bce.ca | ServiceNow | ServiceNow System Administrator; Conseiller technique principal ServiceNow; Sr Technical Advisor |
| **Rogers** | jobs.rogers.com | ServiceNow + Salesforce | Sr Platform Specialist; Technical Specialist |
| **Telus** | jobs.telus.com | ServiceNow + Salesforce | Telecom IT; ITSM |
| **Shaw / Rogers Media** | careers | ServiceNow | Media/IT |
| **Cogeco** | careers | ServiceNow | Quebec/Ontario |
| **SaskTel / SaskPower / SaskEnergy** | careers | ServiceNow | Saskatchewan crown corps |
| **Manitoba Telecom / Manitoba Hydro** | careers | ServiceNow | Manitoba crown corps |
| **CTV / Bell Media / Corus / Postmedia** | careers | Salesforce | Media CRMs |

### D. Retail & consumer (Salesforce Commerce Cloud / ServiceNow)

| Company | Career page | Platform focus | Notes |
|---|---|---|---|
| **Loblaw** | careers.loblaw.ca | Salesforce + ServiceNow | Retail IT; Salesforce Commerce Cloud |
| **Empire (Sobeys)** | careers | Salesforce | Atlantic retail IT |
| **Canadian Tire** | careers.canadiantire.ca | Salesforce | Retail IT |
| **Indigo / Chapters** | careers | Salesforce | Retail CRM |
| **Holt Renfrew / Nordstrom Canada** | careers | Salesforce | Luxury retail CRM |
| **Air Canada** | aircanada.com/careers | Salesforce + ServiceNow | Airline IT; CRM + ITSM |
| **WestJet** | westjet.com/careers | Salesforce | Airline CRM |
| **Via Rail / CN / CP / Metrolinx / Calgary Transit** | careers | ServiceNow | Transportation ITSM; Metrolinx is current employer |
| **Cineplex** | careers | Salesforce | Entertainment CRM |
| **Holt Renfrew** | careers | Salesforce | Luxury retail |

### E. Technology companies (downtown Toronto core + platform users)

| Company | Career page | Platform focus | Notes |
|---|---|---|---|
| **Shopify** | shopify.com/careers | Salesforce + ServiceNow | Ottawa/Toronto; ecommerce CRM |
| **Hootsuite** | hootsuite.com/careers | Salesforce | Vancouver/Toronto; social CRM |
| **BlackBerry** | blackberry.com/careers | ServiceNow | Waterloo/Toronto; ITSM |
| **OpenText** | opentext.com/careers | ServiceNow | Waterloo/Toronto; enterprise IT |
| **Descartes** | descent.com/careers | ServiceNow | Waterloo/Toronto; logistics IT |
| **Thomson Reuters** | careers.thomsonreuters.com | Salesforce | Toronto; Salesforce Engineer; Senior Developer – Salesforce Integrations |
| **TMX Group** | tmx.com/careers | Salesforce | Toronto exchange; financial CRM |
| **IBM Canada** | ibm.com/careers | ServiceNow | Business Analyst – ServiceNow (Ottawa) |
| **RBC Ventures / TD Digital / CIBC Innovation / Scotiabank Digital Factory** | various | Salesforce + ServiceNow | Bank digital labs; Agentforce/Now Assist roles |
| **Corus Entertainment / Bell Media / Rogers Media / Postmedia** | careers | Salesforce | Media CRM |

### F. Federal / provincial / municipal government & crown corps

| Entity | Career page | Platform focus | Notes |
|---|---|---|---|
| **Ontario Government** | gojobs.gov.on.ca | ServiceNow + Salesforce | IT category; CAPTCHA on search — manual check |
| **City of Toronto** | toronto.ca/careers | ServiceNow | ITSM; Senior IT Business Systems Analyst |
| **City of Vancouver** | careers | ServiceNow | Municipal ITSM |
| **Service Canada / ESDC** | canada.ca | ServiceNow | Federal ITSM |
| **Province of Ontario / Quebec** | various | ServiceNow + Salesforce | Provincial IT |

---

## 4. Downtown Toronto: tech companies near M5G 2H5 (55 Centre Avenue) & Eaton Centre

**M5G 2H5 / 55 Centre Avenue** is in the Entertainment District / Library District, near Union Station, Front Street, Wellington Street West, King Street West, and the Toronto Public Library reference branch. Companies in this radius post Toronto-downtown addresses.

**Eaton Centre / Yonge-Dundas Square** is the downtown retail core along Yonge Street, Dundas Street, Queen Street West, and Bay Street. Many tech and media employers have towers here.

Tech employers in / near these zones (check their career pages for ServiceNow / Salesforce / IT Reporting / IT Asset Management):

| Area | Companies | Career page pattern |
|---|---|---|
| **Entertainment District / King West / Wellington West** (near M5G 2H5) | Thomson Reuters, TMX Group, Rogers Media, Corus, Postmedia, Cineplex, Hootsuite (Toronto office), Shopify (Toronto office), various ad-tech / mar-tech agencies | `company.com/careers` → search "servicenow", "salesforce", "itam", "it reporting" |
| **Financial District / Bay Street** | CIBC, BMO, TD, Scotiabank, RBC, National Bank, Sun Life, Canada Life, Manulife, Great-West | `company.com/careers` or Workday subdomain |
| **Yonge-Dundas / Eaton Centre** | Thomson Reuters (downtown tower), Rogers, Bell, various SaaS scale-ups, recruitment agencies (Robert Half, Randstad, Adecco, Robert Half Technology) | `company.com/careers` |
| **Discovery District / MaRS** (adjacent) | MaRS tenants, health-tech SaaS, AI startups | `marsdd.com` tenant directory; individual company careers |

**Search queries for these areas (Adzuna / LinkedIn / Indeed):**
- `"servicenow" "toronto" "downtown" OR "m5g" OR "55 centre"`
- `"salesforce" "toronto" "eaton centre" OR "yonge-dundas"`
- `"itam" "toronto" downtown`
- `"it reporting" "servicenow" toronto`
- `"it asset management" "salesforce" toronto`

---

## 5. Suggested search cadence (Toronto, ServiceNow/Salesforce)

| Frequency | Channel | What to capture |
|---|---|---|
| **Daily (morning)** | LinkedIn guest API / logged-in; Adzuna CA `sort_by=date max_days_old=1` | Same-day postings; capture `created` / `datePosted` |
| **Daily (evening)** | Job Bank Canada `searchstring=servicenow` / `salesforce` | Official employer records with salary bands |
| **Twice weekly** | Individual SI career pages (Deloitte, Accenture, KPMG, CGI, Cognizant, Wipro, NewRocket, Ondaro) | Employer-ATS verified; aggregators lag |
| **Twice weekly** | Bank career pages (CIBC, BMO, TD, Scotiabank, RBC, Desjardins, National Bank, Moneris, Intact) | Workday/iCIMS/Greenhouse direct |
| **Weekly** | Workopolis, Eluta, ZipRecruiter, Talent.com | Secondary catch; verify dates |
| **Monthly** | Dice, Hired, Wellfound | Contract & startup roles |

**De-duplication rule:** normalize URL (strip `utm_*`, `se=`, `v=` query params) and dedupe on title + company before adding to any tracker.

---

## 6. Red flags & filters

- Exclude: account executive, account manager, sales representative, business development, recruiter, talent acquisition, customer success (not platform dev/admin roles).
- Exclude US-only / clearance-only postings (GDIT, LightFeather, First Citizens, etc.) unless you hold US work authorization.
- Exclude roles older than 30 days unless the employer ATS confirms "still accepting."
- Verify each aggregator mirror against the employer ATS before applying; an aggregator "posted today" is not proof of an open vacancy.

---

*Prepared by Nemotron (NVIDIA NIM / OpenRouter, `nvidia/nemotron-3.5-super-vl:free`), 2026-11-02 14:30 UTC. Company lists derived from public knowledge of ServiceNow/Salesforce partner ecosystems, World Forum Toronto / World Tour sponsor patterns, and major Canadian employers; verify each career page directly before applying.*

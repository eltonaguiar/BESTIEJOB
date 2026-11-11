# IT staffing agency job portals (Grok Bot inventory)

**Source:** Grok Bot Job hunter agent, uploaded as `AGENCY_PORTALS_2026-11-10.md`  
**Reviewed:** 2026-11-10 (America/Toronto). Imported into this repo 2026-11-11.  
**Companion:** `reports/toronto_it_agencies_2026-11-11.md`, `config/agency_boards.json`  
**Privacy:** Company names only — no recruiter names, contacts, or personal email addresses.

This report is a **reference list** for future ServiceNow/Salesforce agency scans. It
records official portal URLs and what was observed on each site during the Grok Bot
pass. It does **not** enable scanner feeds: a board still needs the absolute
`datePosted` check from `toronto_it_agencies_2026-11-11.md` before it belongs in
`config/agency_boards.json`.

**How to read “SN roles found”:** “Yes” means a Canada-relevant ServiceNow-related
posting was still open on the official page or API that night. “No” means the portal
answered but no such role was confirmed. “Unconfirmed” means blocked, JS-only, 404, or
the official jobs URL is not yet solid.

| Company | Official portal URL | ATS / platform | SN roles found | Status (2026-11-10) |
| --- | --- | --- | --- | --- |
| TEKsystems | https://careers.teksystems.com/ca/en/search-results | Phenom (widgets API) | No | Canada filter returned 0 jobs for ServiceNow-related keywords; US hits were out of scope. |
| Procom | https://myprocom-portal.procomservices.com/jobs | Gorilla Works | Yes | Senior ServiceNow Developer (BMO) and Application Specialist (GTAA) still open; keyword search is client-side. |
| Randstad Canada | https://www.randstad.ca/jobs/q-servicenow/ | Randstad / BlueX | Yes | Multiple ServiceNow titles in search; some older URLs returned 410 Gone. |
| Randstad Digital | Same Randstad Canada board unless a separate Digital microsite is confirmed | Randstad | Unconfirmed as separate | Live checks used randstad.ca. |
| S.I. Systems | https://www.sisystems.com/jobs/ | Custom job pages | Yes, mostly stale | Contract HRSD analyst possibly current; several pages have end dates in 2021–early 2026. Site search was WAF-blocked. |
| Tundra Technical Solutions | https://www.tundratechnical.ca/ ; https://join-us.tundratechnical.ca/ | WordPress (Join Tundra) | No on Join board | ServiceNow search on join-us returned nothing; client contract roles may live elsewhere. |
| Acronym Solutions | https://acronymsolutions.com/about/careers/ ; https://jobs.hydroone.com/acronymsolutions/ | Hydro One vendor board | No in keyword results | Vendor board did not confirm an open ServiceNow card. |
| Raise (Ian Martin Group) | https://raise.jobs/careers | Raise jobs site | Unconfirmed | HTTP 403 from the scan host; individual job URLs also 403. |
| Ian Martin Group | No stable first-party `/jobs` URL confirmed | Not confirmed | Unconfirmed | Treat Raise as the working jobs surface until a careers URL is verified. |
| Addmore Group | https://jobs.addmoregroup.com/ | Agency job board | No current | Montreal ITSM and remote Discovery roles marked no longer available. |
| TEEMA | https://jobs.teemagroup.com/ | TEEMA job board | No | Indexed ServiceNow job URLs returned 404; site search empty. |
| Spectraforce | https://spectraforce.com/careers/jobs/ | Company career pages | Yes | CMDB Data Governance Analyst (Toronto contract) still open; several older SN reqs expired. |
| ThemeSoft | https://www.themesoft.com/careers/ ; https://themesoftinc.oorwin.com/careers/index.html | Oorwin SPA | Unconfirmed | Oorwin rendered client-side with no server-side job list; aggregator copies marked expired. |
| J&M Group | Official careers URL not confirmed | Unknown | Unconfirmed | Guessed domains did not yield a working job board. |
| Yochana IT Solutions | https://www.yochana.com/careers/ ; https://careers.smartrecruiters.com/YochanaITSolutionsInc3 | SmartRecruiters + company site | No Canada SN tonight | SmartRecruiters showed US roles only in this pass. |
| AceStack | First-party careers URL not confirmed | Unknown | Unconfirmed | Do not treat jobs.ca or other aggregator cards as the official apply route. |
| 1 Point System | https://www.1pointsys.com/ | Company site (`/careers` 404) | Unconfirmed | No public jobs board found. |
| Global Technical Talent (GTTIT) | https://gttit.com/ ; https://careers.gttit.com/ ; JobDiva portal linked from site | JobDiva | No in loaded HTML | Careers host is marketing-only; JobDiva is JavaScript. |
| Mindlance | https://www.mindlance.com/jobs returned 404 | Not confirmed | Unconfirmed | No working jobs URL confirmed. |
| VBeyond | https://www.vbeyond.com/careers/jobs-with-our-clients/ | WordPress | No | No Canada ServiceNow developer/admin role surfaced. |
| BeachHead Staffing | Staffing careers URL not confirmed | Unknown | Unconfirmed | beachheadsolutions.com is a different company (device security). |
| Morson | https://www.morson.com/jobs and `/canada` | Company site | Unconfirmed | HTTP 403 from scan host. |
| Quantum Technology Recruiting (QTR) | https://services.quantum-qtr.com/jobs/en/details/1001667TJ (QTR services jobs host) | Custom | Yes | ServiceNow Business Analyst listed open (Toronto hybrid contract). |
| Leading Talent | https://leadingtalent.ca/ | WordPress job board | Yes, as CGI postings | Several ServiceNow titles live with CGI as hiring organization — treat as employer mirror, not net-new agency reqs. |
| Compugen | https://compugen-pc.my.salesforce-sites.com/recruit/fRecruit__ApplyJobList | Salesforce Sites | No in loaded list | Search did not confirm a ServiceNow developer card. |
| Ondaro | https://ondarowave.com/job-listing ; Greenhouse `ondarowave` | Greenhouse | No Canada location | API jobs were US/Mexico/Colombia only. |
| Elgebra / Callesto | https://www.elgebra.com/ ; https://www.callesto.com/ | Company sites | No public SN board | Partner sites without searchable ServiceNow list. |
| Infosys | Employer careers (not a staffing board) | Employer ATS | Not agency | Listed because it appears in partner correspondence. |
| CGI | CGI careers (404 on guessed URL); JDs on Leading Talent | Employer ATS + mirror | Yes via Leading Talent | Employer, not staffing agency. |
| Avanciers | https://www.avanciers.com/careers/ | Company careers | No | No ServiceNow listing in HTML. |
| Pacer Staffing | https://pacerstaffing.com/jobs/ | Unknown (interstitial) | Unconfirmed | “One moment” challenge page. |
| Largeton | https://www.largeton.com/ | Company site | No | Marketing site; no jobs board. |
| Artech | https://www.artech.com/careers/consultant-jobs | Company careers | No in HTML | Same endpoint as `toronto_it_agencies_2026-11-11.md`. |
| 2iSolutions | https://2isolutions.com/careers/ ; `/current-openings/` | WordPress | No | Openings page had no ServiceNow mention in visible HTML. |
| Mirroar | https://mirroar.com/careers/ | Company careers | Marketing only | Careers page is SN marketing without a concrete Canada req. |
| Robert Half | https://www.roberthalf.com/ca/en/jobs?q=ServiceNow | Robert Half | No confirmed SN card | Canada jobs page loaded; no clear SN developer/admin posting extracted. |
| Hays Canada | https://www.hays.ca/jobs | Hays | No | Profession landing loaded; a Toronto ServiceNow search path 404’d. |
| Akkodis (formerly Modis) | Guessed `/en-ca/jobs` and `/en/canada/jobs` returned 404 | Not confirmed | Unconfirmed | Official Canada jobs URL still needs discovery. |
| Experis | Guessed Canada search URLs returned 404 | Not confirmed | Unconfirmed | Official Canada jobs URL still needs discovery. |
| Adecco | Not fully verified this turn | Not confirmed | Unconfirmed | Carry forward. |
| Altis | https://jobportal.altis.com/ | Altis JobPortal | No | Job 26797 returned 410 Gone; no replacement ServiceNow req confirmed. |
| LRO Staffing | https://www.lrostaffing.com/job-listings/ | Company listings | No | Listings page; no ServiceNow result in HTML. |
| Agilus | Guessed `/jobs` and `/en/job-seekers/search-jobs` returned 404 | Not confirmed | Unconfirmed | Official jobs URL still needs discovery. |
| Insight Global | https://jobs.insightglobal.com/ | Insight Global | No | Ontario ServiceNow Engineer job URL returned 404. |
| Apex Systems | Official Canada page not re-opened | Apex | Unconfirmed | Prior US-path ServiceNow ITAM BSA in search results. |
| Russell Tobin | Not re-fetched | Company board | Unconfirmed | Intermediate ServiceNow Software Developer noted in prior search. |
| Veritaaq | Guessed `/careers` returned 404 | Not confirmed | Unconfirmed | Official jobs URL still needs discovery. |
| Eagle Professional Resources | Guessed eagleonline.com/jobs returned 404 | Not confirmed | Unconfirmed | Official jobs URL still needs discovery. |
| Myticas | https://myticas.com/jobs/ | Company site | No | `/jobs` redirected to marketing home. |
| Software International | Guessed `/jobs` empty/short response | Not confirmed | Unconfirmed | Official jobs URL still needs discovery. |
| Vaco | Guessed `/jobs` returned 404 | Not confirmed | Unconfirmed | Official jobs URL still needs discovery. |
| Beacon Hill | https://bhsg.com/jobs/ | Beacon Hill | No | Jobs host loaded; no Canada SN developer/admin card confirmed. |
| Kforce | Guessed Canada search returned 410 Gone | Kforce | Unconfirmed | Official current jobs URL still needs discovery. |
| Motion Recruitment | Not fully verified | Not confirmed | Unconfirmed | Named in `toronto_it_agencies_2026-11-11.md` §5; carry forward. |
| CNC Global / Talentpath | Not fully verified | Not confirmed | Unconfirmed | Carry forward. |
| Treeline | Not fully verified | Not confirmed | Unconfirmed | Carry forward. |
| Calian | https://careers.calian.com/ | WordPress | No | Careers home; no ServiceNow mention in HTML. |
| Rangle | https://rangle.io/careers | Company careers | No | Consultancy careers; no ServiceNow role in HTML. |
| Fujitsu Canada | https://www.fujitsu.com/ca/en/about/careers/ | Employer careers | Unconfirmed | HTTP 429 (rate-limited). |
| Ashton Search | Guessed `/jobs` empty/short | Not confirmed | Unconfirmed | Official jobs URL still needs discovery. |
| Cybertec | Guessed `/careers` failed TLS | Not confirmed | Unconfirmed | Official jobs URL still needs discovery. |

## Scan priorities (from Grok Bot notes)

- Prefer official URLs in the table, not aggregator mirrors.
- Boards that had ServiceNow content on 2026-11-10: Procom, Randstad Canada, Spectraforce,
  S.I. Systems, Quantum (QTR), Leading Talent (CGI mirror).
- Still need a reliable official search URL or unblocked fetch: Raise, ThemeSoft Oorwin,
  Morson, AceStack, J&M Group, Mindlance, BeachHead Staffing, Hays, Akkodis, Experis,
  Agilus, Eagle, Veritaaq, and others marked Unconfirmed.
- Tundra’s Join Tundra board is not the surface for client contractors; find the
  contractor or talent-community board before concluding Tundra is empty.

---

## Reconciliation with `toronto_it_agencies_2026-11-11.md` and `config/agency_boards.json`

Cross-checked 2026-11-11. `agency_boards.json` only names **Procom**, **Randstad
Canada**, and **TEKsystems** as agency-specific feeds (plus CareerBeacon, Dice, Built In
Toronto, and disabled Eluta). Everything below is about agency **documentation**, not
scanner enablement.

### 1. Agencies in this list missing from the Toronto agency report and from `agency_boards.json`

These firms appear in the Grok Bot table above but are **not** named anywhere in
`reports/toronto_it_agencies_2026-11-11.md` (sections 2–5) and are not agency entries
in `config/agency_boards.json`:

Acronym Solutions, Addmore Group, TEEMA, Spectraforce, ThemeSoft, J&M Group, Yochana IT
Solutions, AceStack, 1 Point System, Global Technical Talent (GTTIT), Mindlance, VBeyond,
Morson, Leading Talent, Compugen, Ondaro, Elgebra, Callesto, Avanciers, Pacer Staffing,
Largeton, 2iSolutions, Mirroar, Adecco, LRO Staffing, Agilus, Apex Systems, Russell
Tobin, Veritaaq, Myticas, Software International, Vaco, Beacon Hill, Kforce, CNC Global,
Talentpath, Treeline, Calian, Rangle, Fujitsu Canada (employer careers), Ashton Search,
Cybertec, Raise (Ian Martin Group).

**Employers listed for context only (not staffing agencies):** Infosys, CGI — both
appear in the Grok Bot table because of partner-channel traffic, not as scannable agency
boards.

### 2. Portal URLs that differ between reports

| Agency | Toronto report / config | Grok Bot (this file) | Notes |
| --- | --- | --- | --- |
| TEKsystems | `https://careers.teksystems.com/us/en` (config search uses `/us/en/...`) | `https://careers.teksystems.com/ca/en/search-results` | Same Phenom host; Canada path vs US default. Config `enabled: false` (client-side search). |
| Robert Half | `https://www.roberthalf.com/ca/en` | `https://www.roberthalf.com/ca/en/jobs?q=ServiceNow` | Grok uses explicit jobs + query path. |
| Hays Canada | `https://www.hays.ca/` | `https://www.hays.ca/jobs` | Grok uses profession/jobs landing. |
| Insight Global | `https://insightglobal.com/jobs` | `https://jobs.insightglobal.com/` | Subdomain vs apex; both are official Insight Global job search surfaces. |
| Randstad Canada | `https://www.randstad.ca/` (report) / `https://www.randstad.ca/jobs/q-servicenow/` (config) | Same as config keyword search | Aligned with `agency_boards.json`; Toronto §2 lists site root only. |
| Procom | `https://myprocom-portal.procomservices.com/jobs` | Same | Enabled in config via sitemap adapter. |
| Artech | `https://www.artech.com/careers/consultant-jobs` | Same | Listed in Toronto §2. |
| Eagle | `Eagle Professional` (no URL in §3) | `eagleonline.com/jobs` guessed, 404 | Toronto documents no board; Grok attempted a URL. |
| Akkodis | `https://www.akkodis.com/en-ca` (Toronto §2) | Guessed job paths 404 | Neither pass confirmed a harvestable jobs URL. |
| Experis | `Experis Canada` in §3 (no URL) | Guessed search URLs 404 | Same gap. |

### 3. “No public board” in Toronto §3 but Grok Bot found a reachable portal

Toronto §3 lists these as having **no public job board at usual paths** (scanner treats
them as LinkedIn/Indeed/recruiter-only). Grok Bot nonetheless reached an official jobs
surface (harvestability still requires absolute `datePosted` on a posting page):

| Agency | Toronto §3 | Grok Bot official surface | Scanner note |
| --- | --- | --- | --- |
| S.I. Systems | no public board | `https://www.sisystems.com/jobs/` | Job pages exist; many stale; WAF on search — **candidate** for manual / future adapter work. |
| Quantum Technology Recruiting | no public board | `https://services.quantum-qtr.com/jobs/...` | Custom board with open SN BA — **candidate** after date probe. |
| Spectraforce | not listed in Toronto report | `https://spectraforce.com/careers/jobs/` | Public careers section with dated-style cards — **candidate** after date probe. |
| Altis Recruitment | no public board | `https://jobportal.altis.com/` | JobPortal answers; prior SN job 410 — **candidate** after date probe. |
| Ian Martin | no public board | Raise at `https://raise.jobs/careers` (403 from scan host) | Portal URL identified but blocked here. |
| Tundra Technical | no public board | `https://www.tundratechnical.ca/` + Join Tundra | Corporate/join board may not list client contract reqs. |
| Eagle Professional | no public board | No stable URL (404 on guess) | Still unconfirmed; not a working portal yet. |
| BeachHead | no public board | Staffing portal **unconfirmed** (name collision with BeachHead Solutions product site) | No reconciliation win yet. |

**No new feeds were added to `config/agency_boards.json`** from this import. Next step
for any row above is unchanged: open one posting and keep the agency only if the
posting states an absolute date (`detail_probe.py` / Toronto §7).

---

## Person-name privacy scan (this change)

- **New file:** scanned — company names only; no personal names or personal email
  local-parts in `reports/agency_portals_grokbot_2026-11-10.md`.
- **Existing files referenced, not edited:** `reports/toronto_it_agencies_2026-11-11.md`,
  `config/agency_boards.json`, `updates/2026-11-11-agency-board-integration.md` — no
  person names found on review.

### Other repo files that appear to contain person-identifying data (not edited in this PR)

| Path | Finding |
| --- | --- |
| `docs/ADDITIONAL_SKILLS.MD` | Personal email local-part in certification guidance |
| `docs/ADDITIONAL_SKILLS_MERGED.MD` | Same |
| `docs/ADDITIONAL_SKILLS__deepseek-v4.1-flash.MD` | Same |
| `docs/ADDITIONAL_SKILLS__kilo-auto.md` | Same |
| `SUCCESS_PACK_KILO.MD` | Personal phone and email in contact block |

Repo owners may want a follow-up scrub of `docs/ADDITIONAL_SKILLS*.MD` and
`SUCCESS_PACK_KILO.MD` under the same company-names-only rule.

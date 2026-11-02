# BESTIEJOB — Pages Design Review, Enhancements & Job Hunter Protocol

- **Author:** Job hunter (Grok Bot agent)
- **Date-time:** 2026-11-02 ~10:10 America/Toronto (EST, UTC-5)
- **Site reviewed:** https://eltonaguiar.github.io/BESTIEJOB/

---

## Part A — Current design (observed 2026-11-02)

- Single-page dark UI.
- `JOBS` array is **embedded in `index.html`** (~830 rows), not fetched from `public/jobs-data.json`. Footer still cites that path → 404/mismatch vs the `jobs-data.json` found elsewhere under `/public`.
- Three **stacked** sections (ServiceNow / Salesforce / Other), each with Today / Week / Month / All chips.
- Global search + source chips; meta counts; America/Toronto date logic.
- **Gaps:** no top-level family tabs; no "last updated" datetime beyond "today is …".

## Part B — Suggested enhancements (prioritized)

### P0
1. **Tabbed interface:** `ServiceNow | Salesforce | Other | All`, driven by URL hash or `?tab=` so links are shareable. Show one family grid at a time; keep per-family date chips.
2. **Last-updated stamp:** ISO datetime in America/Toronto set at build time (e.g. `generatedAt` in jobs payload), displayed as "Updated Mon Nov 2, 2026, 10:06 AM EST".
3. **Stop embedding the mega-JSON in HTML:** load `jobs-data.json` (or `/jobs.json`) async; fix footer path; cache-bust with build hash.

### P1
- Applied/hide toggle (localStorage + optional APPLIED.md IDs).
- Employer-ATS vs aggregator badge.
- Salary when known.
- Sticky filter bar.
- Keyboard a11y for tabs (`role="tablist"`, arrow keys, `aria-selected`).
- Empty-state CTA (e.g. "No jobs today — try Week").

### P2
- Fit-score tags from coaching keywords: Flow Designer, Import Sets/IRE, SLA, Integration Hub, ITAM/CMDB, Apex/Flows, ACLs, Update Sets/SDLC, inbound email, mentorship.
- Downtown / M5G–Eaton Centre geo filter.
- Export CSV of filtered view.
- Dark/light toggle.
- Mobile horizontal tab scroll.

### P3 — Overlap with existing doc
Lifecycle/data-model fields (status, `canonicalId`, etc.) are already covered in `BESTIEJOB_IMPROVEMENTS_2026-11-01.md`. Agents should use that doc for the data model; this file covers UI and protocol only.

## Part C — Job hunter SN / SF / Other search protocol (human-runnable)

### 1. Target profile
- Toronto (downtown preferred; hybrid OK).
- **ServiceNow primary:** CSA, CAD, CIS (ITSM, HAM, SAM, DF, PA, Discovery, RC/IRM, SPM, HR); micro-certs Integration Hub, CMDB, ATF, UI Builder, Service Portal, Virtual Agent, Agentic AI.
- **Salesforce:** Platform Admin, PD1, JavaScript Dev I, AI Associate.
- Domain: ITAM/CMDB/CSDM, ITSM (SLA debugging), PA/reporting, Fusion Risk/BCP, Alteryx/SQL/VBA data reconciliation, regulated FS.
- Coaching JD keywords: Flow Designer/Orchestration, Business Rules/Script Includes, Integration Hub/MID/Import Sets/IRE, SLA/ITSM, Update Sets/SDLC, ACLs, inbound email/catalog notifications, ITAM/CMDB sync, mentorship.

### 2. Skip / already-applied (do not surface)
Lightspeed/QuoteMachine, BDO, CAAT, Scotiabank 260518 + SN Admin Specialist, Levio, Take-Two 8306166, BMO R260029070 / R260030015, Benevity, Purolator, Brookfield SN, IKO, Alimentiv, Versapay, Docker, Desjardins, Paralucent, Procom, **no CIBC** (current employer). Also skip any URL already in `APPLIED.md`.

### 3. Preferences
- Prefer **full-time permanent** over variable-hour consulting/contract.
- Agency postings = soft unless the end-client role can be verified.

### 4. Verification rules
- Bucket every lead as **LIVE** (verified open on employer ATS) or **NOT SURE**.
- Verify on the employer ATS (Workday, Greenhouse, Lever, iCIMS, SuccessFactors…) where possible.
- Record **absolute** posted date `YYYY-MM-DD` (never "3 days ago").
- `https://` URL required; prefer employer URL over aggregator.

### 5. README updates — inbox only
- Write `inbox/<slug>--YYYY-MM-DD--vN.md`, then run `python3 tools/jobs_merge_inbox.py`.
- **Never hand-edit the three README tables.**

### 6. Scan order
1. Downtown Toronto / M5G 2H5 (55 Centre Ave) – Eaton Centre – Bay/Adelaide core.
2. SN/SF partners & event sponsors (Knowledge, Dreamforce, World Tour Toronto): GSIs (Cognizant, Accenture, Deloitte, EPAM, Infosys, Compugen, etc.) and boutique partners.
3. Banks / insurers / telcos / government (TD, RBC, BMO*, Scotia*, Manulife, Sun Life, Canada Life, Rogers, Bell, TELUS, OPS, City of Toronto, Metrolinx, TMX). *mind skip list.
4. Boards (LinkedIn, Adzuna, jobs.ca, Indeed) → always verify on employer ATS.

### 7. "Other" family matching
Match on JD content, not title only: ITSM/ITAM/CMDB/CSDM, Flow/integrations, PA/IT reporting, Fusion Risk/BCP, SF/Apex, Alteryx/data quality, regulated FS IT controls.

### 8. Current soft leads (re-check)
- Compugen VN10111
- Canadian Cancer Society — deadline **2026-11-06**
- Canadian Tire JR164237
- Canada Life (need posted dates)
- EPAM Lead ServiceNow; EPAM Salesforce Life Sciences
- Clio Quote-to-Cash
- Lane Four
- Hays — ServiceNow Technical Consultant (contract)

## Part D — Second-opinion scrutiny protocol

- API keys (OpenRouter, Inception Labs Mercury-3, others) are kept in the user's file `dbpasses.txt` on machine Elton2026 (`/home/eaguiar2015/dbpasses.txt`). **Never paste secrets into this file, commits, or chat.** Load them as env vars at run time only.
- Run the prompt below on ≥2 independent models; merge findings into this doc as a new dated section.

### Prompt template
> You are reviewing a job-search protocol for a Toronto-based ServiceNow (CSA/CAD/multi-CIS) + Salesforce (Admin/PD1/JS Dev I/AI Associate) developer with ITAM/CMDB/ITSM depth. Critique it: (1) gaps in the scan order or employer list, (2) stale or unreliable sources, (3) bias toward aggregators vs employer ATS, (4) missed certifications or keywords that 2026 Toronto JDs require, (5) verification weaknesses (dates, closed postings), (6) concrete fixes ranked by impact. Protocol follows: <paste Part C>

### Status
As of **2026-11-02 10:08 EST**, Elton2026 was offline, so Job hunter could not run the API second pass yet.

- [ ] OpenRouter model #1 — results:
- [ ] OpenRouter model #2 — results:
- [ ] Inception Labs Mercury-3 — results:
- [ ] Web-search cross-check of sources — results:
- [ ] Changes merged into Part C (date + author):

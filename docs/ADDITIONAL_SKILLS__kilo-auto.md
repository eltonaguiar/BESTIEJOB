# Additional skills & certifications to acquire (kilo-auto advisory)

**Advisory recorded:** 2026-11-02
**Model:** kilo-auto/free (Hermes Agent)
**Applies to:** Elton Aguiar — ServiceNow Sr. Tech Consultant + Salesforce Developer resumes (Toronto, ON)
**Companion doc:** `docs/JOB_SEARCH_PLAYBOOK.md` (how to search) — this file is *what to learn next*

---

## Read of the profile

Elton holds 12+ ServiceNow CIS certs (ITSM, HAM, SAM, DF, PA, Discovery, RC, SPM, HR), Salesforce Platform Developer I, Salesforce JavaScript Developer, Salesforce AI Associate, ITIL v4, Tableau Desktop Specialist, PCEP Python, Alteryx Designer Core. Strong hands-on at CIBC (ITAM, 800k+ asset records, 15+ external systems), BMO (Salesforce Platform Events, scheduled jobs, Apex triggers, ~5,000 users), Metrolinx (ServiceNow ITSM, Flow Designer, SLA, QlikSense).

Verdict: **over-certified on breadth, under-certified on depth.** The flat cert list reads as "certification collector" unless a depth signal (PD II, CIS-IntegrationHub full, architect-adjacent data/cloud cred) is present. Toronto employers hiring senior ServiceNow/Salesforce devs filter on PD II / CIS-IntegrationHub / AI-Agentforce / integration-architecture signals, not more micro-certs.

---

## Top 10 additional skills / certifications (ranked by marginal employability gain)

| # | Skill / Cert | Platform | Why it's the gap | Approx cost |
|---|---|---|---|---|
| 1 | **Salesforce Platform Developer II** | Salesforce | PD I + JS Dev I = "admin who codes"; PD II = "developer". BMO work (Platform Events, scheduled jobs, Apex test classes, trigger frameworks) is already PD II material. Highest ROI on Salesforce side. Re-establishes the "developer" label. | ~$200 |
| 2 | **ServiceNow CIS-IntegrationHub (full cert)** | ServiceNow | Resume claims Spokes / Scripted REST+SOAP / Integration Hub but only holds a micro-cert. Integration is the highest-bill-rate SN dev specialty in Toronto. Cheapest credibility upgrade available. | ~$250–$350 |
| 3 | **ServiceNow CIS-ITOM (formal)** | ServiceNow | Discovery + Service Mapping at Metrolinx + 800k CI reconciliation at CIBC. ITOM is the top-paying SN specialty; cert list under-represents actual experience. Makes CIBC/Metrolinx work defensible. | ~$250–$350 |
| 4 | **ServiceNow CIS-Security Incident Response (SIR)** | ServiceNow | Fastest-growing SN product line. RBC vulnerability/patching/Black Duck background transfers directly. Most ITSM devs cannot tell a CVE from a change request. Differentiator for SecOps/IRM roles. | ~$250–$350 |
| 5 | **Salesforce Certified Administrator (correct name)** | Salesforce | Resume says "Salesforce Certified Platform Administrator", which is not a real cert name. Either fix the name or earn it. Most-recognized gate on Salesforce side; required before PD II anyway. | ~$200 + $100 maintenance |
| 6 | **Salesforce AI Specialist + Agentforce Specialist** | Salesforce | AI Associate is knowledge-only; AI Specialist is hands-on and what postings now filter on. Agentforce Specialist (2025–26) pairs with ServiceNow "Agentic AI" micro-cert into a rare two-platform AI story. | ~$200 each |
| 7 | **MuleSoft Developer I or Workato Automation Pro** | Integration | Resume is fundamentally an integration + data-quality resume (15+ systems, Feedhub anomalies, source reconciliation, 94% error reduction). Formalising it lifts ceiling from developer to integration architect. MuleSoft for enterprise SF shops; Workato for mid-market. | ~$200–$250 |
| 8 | **Snowflake SnowPro Core or Databricks Data Engineer Associate + dbt** | Data | 800k-record reconciliation across 20+ classes is data engineering wearing an ITAM hat. Converts "I do SQL reconciliation" into "data engineer specialising in CMDB" — pays materially more than ITAM consultant. | ~$200–$300 |
| 9 | **IAITAM CSAM or CHAMP** | ITAM | Vendor-neutral ITAM credentials. ITAM-specific postings often ask for IAITAM because it proves asset-management discipline, not tool configuration. Pairs with #3. | ~$300–$500 |
| 10 | **AWS Solutions Architect Associate (or AZ-104) + Terraform Associate** | Cloud | Reconciliation already spans Azure/AWS/Windows/MAC/SCCM/Soroc; cloud literacy assumed for Discovery/Service Mapping. Terraform Associate = cheapest credibility-per-dollar item. | ~$150 + ~$70 |

---

## What NOT to buy

- **More ServiceNow micro-certs.** Nine already; each additional one dilutes the signal.
- **ServiceNow CTA / CMA** — needs employer sponsorship + multi-year track; not purchasable outright.
- **Salesforce Application/System Architect** — requires PD II first (#1) and years of experience. Do not skip PD II.

---

## Resume flags to fix BEFORE any cert spend

1. **"Certifications under [redacted email]"** — red flag. Tells a screener the Now Learning / Trailhead records sit under a non-professional address, inviting verification friction. Consolidate accounts, then delete the line.
2. **"Salesforce Certified Platform Administrator"** and **"Salesforce Platform Developer"** are not real certification names. Correct to **Certified Administrator** and **Platform Developer I**. A screener who knows the SF cert tree catches this in seconds and discounts the whole section.
3. **Two resumes with divergent cert lists** — one omits Salesforce certs from the top block; the other drops CIS-ITSM. Inconsistency between versions is what background checks surface. Unify into one master list.

---

## The fork to choose

| Path | Certs in order | What you become | Supported by history | Recency risk |
|---|---|---|---|---|
| **ServiceNow** | #2 CIS-IntegrationHub → #3 CIS-ITOM → #4 CIS-SIR → #9 IAITAM → #10 AWS/Terraform | ITOM / ITAM / SecOps integration specialist | CIBC + Metrolinx (current-ish) | Low — current role is ServiceNow |
| **Salesforce** | #5 Admin (fix name) → #1 PD II → #6 AI + Agentforce → #7 MuleSoft/Workato | PD II integration developer | BMO (ended Jan 2025 — **22 months stale**) | High — needs PD II plus a current side project/open-source contribution to re-establish hands-on proof |

**If Salesforce is chosen:** PD II plus a current side project matters more than any further cert, because it re-establishes *recency*, not breadth.

---

## Specialized certs for adjacent/high-pay roles

| Target role | Recommended cert(s) |
|---|---|
| ServiceNow ITOM architect | CIS-ITOM + CIS-Discovery + CIS-ServiceMapping |
| ServiceNow SecOps / IRM dev | CIS-SIR + CIS-IRM + IAITAM CHAMP |
| Salesforce integration architect | PD II + MuleSoft Developer I + Salesforce Sharing & Visibility Architect (later) |
| Data engineer (CMDB/asset focus) | Snowflake SnowPro Core + Databricks DE Associate + dbt |
| AI/Automation lead (both platforms) | ServiceNow Agentic AI/Now Assist + Salesforce AI Specialist + Agentforce Specialist |
| ITAM manager | IAITAM CSAM/CHAMP + CIS-HAM + CIS-SAM |

---

**Bottom line:** Earn **one depth signal first** — PD II if Salesforce-leaning, CIS-IntegrationHub if ServiceNow-leaning — then layer AI/integration certs. Do not chase more micro-certs.

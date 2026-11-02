# Additional skills & certifications to acquire

**Advisory recorded:** 2026-11-02 · source: Zoo AI advisory answer (external review)
**Applies to:** the ServiceNow-resume and Salesforce-resume variants in this repo
**Companion doc:** `docs/JOB_SEARCH_PLAYBOOK.md` (how to search) — this file is *what to learn next*

---

## Read of the profile

Already over-certified on ServiceNow implementation (CSA, CAD, CIS-ITSM/HAM/SAM/DF/PA/Discovery/RC/SPM/HR)
and under-certified on the two things that gate senior offers: **developer-depth credentials** and
**integration/data credentials**. 12+ CIS certs, 9 micro-certs, zero architect-tier, zero PD II.
Recruiters read a long flat cert list as "certification collector" unless a depth signal is present.

---

## Top 10, ranked by marginal employability gain

| # | Skill / Cert | Why it's the gap |
|---|---|---|
| 1 | **Salesforce Platform Developer II** | PD I + JS Dev I is "admin who codes"; PD II is "developer". The BMO work (Platform Events, scheduled jobs, trigger frameworks, Apex test classes) is already PD II material. ~$200, highest ROI on the Salesforce side. |
| 2 | **ServiceNow CIS-IntegrationHub** (full cert, not the micro) | Integration is the highest-bill-rate ServiceNow dev specialty in Toronto. The resume claims Spokes / Scripted REST+SOAP / Integration Hub but only holds a micro-cert — cheapest credibility upgrade available. |
| 3 | **ServiceNow CIS-ITOM** (formal) | Discovery + Service Mapping at Metrolinx, 800k CI reconciliation at CIBC. ITOM is the top-paying SN specialty and the cert list under-represents actual experience; makes the CIBC/Metrolinx work defensible. |
| 4 | **ServiceNow CIS-Security Incident Response (SIR)** | Fastest-growing SN product line. The RBC vulnerability/patching/Black Duck background transfers directly; most ITSM devs cannot tell a CVE from a change request. |
| 5 | **Salesforce Certified Administrator** — and fix the resume name | The resume says "Salesforce Certified Platform Administrator", which does not exist. Either the real cert (Certified Administrator) is held and misnamed, or it isn't held. One-line fix, most-recognized gate on the SF side. |
| 6 | **Salesforce AI Specialist + Agentforce Specialist** | AI Associate is a knowledge cert; AI Specialist is hands-on and is what postings now filter on. Agentforce Specialist is the 2025–26 differentiator and pairs with the ServiceNow "Agentic AI" micro-cert into a two-platform AI story almost nobody else has. |
| 7 | **MuleSoft Developer I *or* Workato Automation Pro** | The resume is fundamentally an integration + data-quality resume (15+ systems, Feedhub anomalies, source reconciliation, 94% error reduction). Formalising it makes the integration narrative portable and lifts the ceiling from developer to integration architect. MuleSoft for enterprise SF shops, Workato for mid-market. |
| 8 | **Snowflake SnowPro Core or Databricks Data Engineer Associate + dbt** | 800k-record reconciliation across 20+ classes is data engineering wearing an ITAM hat. Converts "I do SQL reconciliation" into "data engineer specialising in CMDB" — a role that pays materially more than ITAM consultant. |
| 9 | **IAITAM CSAM or CHAMP** | Vendor-neutral ITAM credentials. ITAM-specific postings often ask for IAITAM because it proves asset-management discipline, not tool configuration. Pairs with #3. |
| 10 | **AWS Solutions Architect Associate (or AZ-104) + Terraform Associate** | Reconciliation already runs across Azure/AWS/Windows/MAC/SCCM/Soroc; cloud literacy is assumed for Discovery/Service Mapping work. Terraform Associate is the cheapest credibility-per-dollar item on the list. |

---

## What **not** to buy

- **More micro-certs.** Nine already; each additional one dilutes the signal.
- **ServiceNow CTA/CMA** and **Salesforce Application/System Architect** — both need employer
  sponsorship and a multi-year track, and the Salesforce architect path requires PD II first (#1).

---

## Resume flags to fix before any cert spend

1. **"Certifications under eaguiar2015@yahoo.ca email"** — red flag. It tells a screener the Now
   Learning / Trailhead records sit under an address that isn't used professionally, inviting
   verification friction. Consolidate the accounts, then delete the line.
2. **"Salesforce Certified Platform Administrator"** and **"Salesforce Platform Developer"** are not
   real certification names. Correct to **Certified Administrator** and **Platform Developer I**.
   A screener who knows the SF cert tree catches this in seconds and discounts the whole section.
3. **Two resumes with divergent cert lists** — one omits the Salesforce certs from the top block,
   the other drops CIS-ITSM. Inconsistency between versions is what background checks surface.

---

## The fork to choose

| Path | Certs in order | What you become | Recency risk |
|---|---|---|---|
| **ServiceNow** | #2 CIS-IntegrationHub → #3 CIS-ITOM → #4 CIS-SIR → #9 IAITAM → #10 AWS/Terraform | ITOM / ITAM / SecOps integration specialist — directly supported by CIBC + Metrolinx history | Low: current role is ServiceNow |
| **Salesforce** | #1 PD II → #5 Admin (correct name) → #6 AI + Agentforce → #7 MuleSoft/Workato | PD II integration developer — supported by BMO but **22 months stale** (last SF work ended Jan 2025) | High: needs PD II plus a small side project to re-establish hands-on proof |

If the Salesforce path is chosen, **PD II plus a current side project or open-source contribution
matters more than any further cert**, because it re-establishes recency rather than breadth.

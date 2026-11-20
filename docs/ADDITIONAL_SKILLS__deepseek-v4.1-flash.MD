# Additional skills & certifications — addendum

**Author:** Buffy — DeepSeek V4.1 Flash (Freebuff agent)
**Date/time:** 2026-11-02 15:25 UTC (10:25 America/Toronto)
**Inputs:** the ServiceNow-resume and Salesforce-resume variants in this repo, plus an external
advisory from Zoo AI (recorded in `docs/ADDITIONAL_SKILLS.MD`)
**Scope:** what to learn or certify next for ServiceNow / Salesforce developer roles in Toronto.
This is *not* job-search mechanics — that is `docs/JOB_SEARCH_PLAYBOOK.md`.

---

## Verdict in one paragraph

The profile is over-certified on ServiceNow **implementation** and under-certified on the two things
that actually gate senior offers: **developer-depth** credentials and **integration / data**
credentials. Twelve-plus CIS certs with zero architect-tier and zero Platform Developer II reads as
breadth, not depth. The fix is not more certs — it is three depth signals plus two portable
credentials, chosen along one path rather than both.

---

## Ranked list (merged view: external advisory + my additions)

| # | Skill / Cert | Why it matters for this profile | Cost | Who recommends |
|---|---|---|---|---|
| 1 | **Salesforce Platform Developer II** | PD I + JS Dev I is "admin who codes"; PD II is "developer". The BMO work (Platform Events, multi-tier scheduled jobs, trigger frameworks, Apex test classes) is already PD II material — the credential is sitting unclaimed | ~$200, medium effort | Zoo + me |
| 2 | **ServiceNow CIS-IntegrationHub** (full cert) | Integration is the highest-bill-rate SN specialty in Toronto. Resume claims Integration Hub, Spokes, Scripted REST/SOAP but holds only the micro-cert | Low | Zoo + me |
| 3 | **ServiceNow CIS-ITOM** (formal) | Discovery + Service Mapping at Metrolinx and 800k-CI reconciliation at CIBC already justify it; the cert makes that work defensible in a screening call | Low | Zoo + me |
| 4 | **Salesforce Certified Administrator — and fix the resume name** | "Salesforce Certified Platform Administrator" does not exist. Either the real cert is held and misnamed, or it isn't held; both are one-line fixes and it is the most-recognised gate on the SF side | ~$200 | Zoo + me |
| 5 | **ServiceNow CIS-Security Incident Response (SIR)** | Fastest-growing SN line; the RBC patching / Black Duck / vulnerability background transfers directly and differentiates from generic ITSM devs | Medium | Zoo |
| 6 | **Salesforce AI Specialist + Agentforce Specialist** | AI Associate is knowledge-only; AI Specialist is hands-on and is what postings filter on. Pairing Agentforce with the ServiceNow "Agentic AI" micro-cert is a two-platform AI story almost nobody in this market has | Medium | Zoo + me |
| 7 | **MuleSoft Developer I *or* Workato Automation Pro** | The whole resume is an integration + data-quality story (15+ systems, Feedhub anomalies, source reconciliation, 94% error reduction). Formalising it lifts the ceiling from developer to integration architect | Medium | Zoo |
| 8 | **Databricks Data Engineer Associate (or Snowflake SnowPro Core) + dbt** | 800k records across 20+ CI classes is data engineering wearing an ITAM hat. Converts "SQL reconciliation" into "data engineer specialising in CMDB", which pays more than ITAM consultant | Medium-high | Zoo |
| 9 | **IAITAM CSAM or CHAMP** | Vendor-neutral ITAM credentials; ITAM-titled postings ask for them because they prove asset-management discipline, not tool configuration | Medium | Zoo |
| 10 | **AWS Solutions Architect Associate (or AZ-104) + Terraform Associate** | Reconciliation already spans Azure/AWS/SCCM/Soroc; cloud literacy is assumed for Discovery and Service Mapping. Terraform Associate is the cheapest credibility-per-dollar item here | Low-medium | Zoo |

### My additions to the advisory

| # | Item | Why |
|---|---|---|
| A | **Copado or Gearset Salesforce DevOps certification** | The BMO work claims "100% on-time deployment, zero downtime" via change sets — change sets are the thing hiring managers consider legacy. One Copado fundamentals cert re-frames that experience as CI/CD, and it pairs naturally with the existing GitHub Actions work. |
| B | **ServiceNow ATF depth (not just the micro-cert)** | Automated Test Framework is the least-glamorous, most-defensible differentiator for a *developer* title: it proves you can ship changes without breaking a bank's instance. Most SN devs have never written a test suite. |
| C | **ServiceNow UI Builder / Service Portal (Next Experience)** | Already claimed in skills, but underpinned only by micro-certs. Portal work is where "developer" and "admin" visibly separate. |
| D | **ITIL 4 Managing Professional (MP) module, e.g. CDS or DSV** | ITIL v4 Foundation is table stakes. One MP module turns "I know the framework" into "I can run a practice" — useful because every bank SN role is process-adjacent. |
| E | **Written architecture artefact in the portfolio** | Not a cert, and the highest-leverage item on this list: a 2-page design doc (CMDB data model + IRE/transform strategy + reconciliation controls) written from the CIBC work. It is the only thing here that proves seniority in an interview. |
| F | **Salesforce Data Cloud (Data Cloud Consultant)** | If the Salesforce path is chosen, Data Cloud + Agentforce is where the 2026 requisitions are; the existing SQL/data background shortens the ramp. |

---

## What **not** to buy

- **More ServiceNow micro-certs.** Nine already; each additional one dilutes the signal.
- **ServiceNow CTA / CMA** and **Salesforce Application / System Architect.** Both need employer
  sponsorship and a multi-year track, and the Salesforce architect path requires PD II first.
- **A second "AI Associate"-level knowledge cert.** AI Associate is already held; the next step is
  the hands-on Specialist, not another awareness badge.

---

## Resume fixes to land before any cert spend

1. Delete **"Certifications under [redacted email]"** — it invites verification friction
   and hints the Now Learning / Trailhead records sit under an address that isn't used professionally.
2. Rename **"Salesforce Certified Platform Administrator" → Salesforce Certified Administrator**, and
   **"Salesforce Platform Developer" → Platform Developer I**.
3. Reconcile the **two divergent cert lists** between the ServiceNow and Salesforce resume variants
   (one drops the Salesforce block from the header, the other drops CIS-ITSM). Background checks
   surface this.
4. The ServiceNow resume says "6+ years" in the summary while the roles show 2018–present plus a 2017
   CIBC stint — make the arithmetic explicit rather than letting a screener do it.

---

## The fork, stated plainly

| Path | Sequence | Resulting title | Recency risk |
|---|---|---|---|
| **ServiceNow** | CIS-IntegrationHub → CIS-ITOM → CIS-SIR → IAITAM → AWS/Terraform | ITOM / ITAM / SecOps integration specialist | **Low** — current role is ServiceNow (CIBC, Jan 2025–present) |
| **Salesforce** | PD II → Admin (correct name) → AI + Agentforce → MuleSoft or Workato | PD II integration developer | **High** — last SF work ended Jan 2025, ~22 months stale. PD II alone does not fix that; a current side project or open-source contribution does |

Recommendation: **take the ServiceNow path as primary** (recency is intact and the CIBC ITAM/CMDB
work is exactly what ITOM buyers want), and keep the Salesforce path alive only as a six-month
side-project plan with PD II as its first milestone.

---

*Prepared by Buffy (DeepSeek V4.1 Flash) on 2026-11-02. External advisory from Zoo AI is preserved
verbatim in `docs/ADDITIONAL_SKILLS.MD`; this file merges it with the repo's own observations and adds
six items the advisory did not cover.*

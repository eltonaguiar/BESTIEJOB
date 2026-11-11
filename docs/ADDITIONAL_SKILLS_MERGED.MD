# Additional skills & certifications — merged and final

**Merged by:** Buffy — DeepSeek V4.1 Flash (Freebuff agent)
**Merged at:** 2026-11-02 16:05 UTC (11:05 America/Toronto)
**Scope:** what to learn or certify next for ServiceNow / Salesforce developer roles in Toronto.
Job-search mechanics live in `docs/JOB_SEARCH_PLAYBOOK.md`; the channel list (boards, staffing firms,
partners, events) is captured separately in `JOB_SITES_CANADA__paid-mode_2026-11-02_1520Z.MD`.

**Sources consolidated** — every `ADDITIONAL_SKILLS*` file in the repo at merge time:

| File | Author / model | Adds |
|---|---|---|
| `docs/ADDITIONAL_SKILLS.MD` | Zoo AI advisory | The original top-10 ranking, resume flags |
| `docs/ADDITIONAL_SKILLS__kilo-auto.md` | kilo-auto / free (Hermes Agent) | Cost per cert, role→cert matrices |
| `docs/ADDITIONAL_SKILLS__deepseek-v4.1-flash.MD` | Buffy — DeepSeek V4.1 Flash | Copado/Gearset, ATF depth, UI Builder, ITIL 4 MP, architecture artefact, Data Cloud |
| `docs/ADDITIONAL_SKILLS__claude-copilot.MD` | Claude (Anthropic) via Copilot SDK | Portfolio packaging, GitHub Actions cert, AI-102, Now Assist path, cert-maintenance debt |
| `ADDITIONAL_SKILLS__nemotron.MD` (working tree — not yet committed by its author) | Nemotron (NVIDIA NIM) | AI-hybrid market framing, Now Assist hands-on, 90-day sequencing |

Five independent advisors, one verdict, **zero contradictions on substance**: the profile is
**over-certified on breadth, under-certified on depth**, and the fix is a small number of depth
signals on **one** path — not more badges.

---

## 1. The unanimous core (5/5 — treat as settled)

| Rank | Credential | Why it is the gap | Cost | Consensus |
|---|---|---|---|---|
| 1 | **ServiceNow CIS-IntegrationHub (full cert, not the micro)** | Integration is the highest-bill-rate ServiceNow specialty in Toronto. The resume claims Integration Hub, Spokes, Scripted REST/SOAP — but only a micro-cert backs it | ~$250–350 | 5/5 · **#1 on the ServiceNow path** |
| 2 | **Salesforce Platform Developer II** | PD I + JS Dev I reads as "admin who codes"; PD II is "developer". The BMO work — Platform Events, multi-tier scheduled jobs, trigger frameworks, Apex test classes — is already PD II material, so the credential is unclaimed value | ~$200 | 5/5 · **#1 on the Salesforce path** |
| 3 | **ServiceNow CIS-ITOM (formal)** | Discovery + Service Mapping at Metrolinx plus 800k-CI reconciliation at CIBC already justify it; the cert makes that work defensible in a screening call | ~$250–350 | 5/5 |
| 4 | **Salesforce Certified Administrator — and fix the resume name** | "Salesforce Certified Platform Administrator" is not a real certification. Either it is held and misnamed, or it is not held. Either way: one line, $0 | ~$200 (+$100 maint.) | 5/5 |
| 5 | **ServiceNow CIS-Security Incident Response (SIR)** | Fastest-growing SN product line. The RBC patching / Black Duck / vulnerability background transfers directly, and most ITSM devs cannot tell a CVE from a change request | ~$250–350 | 5/5 |
| 6 | **Salesforce AI Specialist + Agentforce Specialist** | AI Associate is knowledge-only; Specialist is hands-on and is what postings filter on. Agentforce + the held ServiceNow "Agentic AI" micro-cert is a two-platform AI story almost nobody in this market has | ~$200 each | 5/5 |
| 7 | **MuleSoft Developer I *or* Workato Automation Pro** | The whole resume is an integration + data-quality story (15+ systems, Feedhub anomalies, source reconciliation, 94% error reduction). Formalising it lifts the ceiling from developer to integration architect | ~$200–250 | 5/5 |
| 8 | **Databricks Data Engineer Associate + dbt** *(or Snowflake SnowPro Core)* | 800k records across 20+ CI classes is data engineering wearing an ITAM hat. Note: **Databricks Data Analyst is already listed** — the *Engineer* track is the actual step up, not a repeat | ~$200–300 | 5/5 |
| 9 | **IAITAM CSAM or CHAMP** | Vendor-neutral ITAM credentials. ITAM-titled postings ask for them because they prove asset-management discipline, not tool configuration | ~$300–500 | 5/5 |
| 10 | **AWS Solutions Architect Associate (or AZ-104) + Terraform Associate** | Reconciliation already spans Azure/AWS/Windows/MAC/SCCM/Soroc; cloud literacy is assumed for Discovery and Service Mapping. Terraform Associate is the cheapest credibility-per-dollar item here | ~$150 + ~$70 | 5/5 |

---

## 2. Second tier — raised by one or two advisors, kept after review

| Item | Source | Why it survives the merge |
|---|---|---|
| **Package the AI/automation portfolio** — a one-page "AI & Automation Engineering" section: the multi-provider LLM failover proxy, CMDB reconciliation at 800k-CI scale, the GitHub Actions pipeline with deploy guards | Claude, Nemotron | **The highest-leverage item in this document, and it costs $0.** The 2026 Now Assist / Agentforce requisitions ask for "platform developer who integrates LLMs"; the working public code already exists and is invisible to a screener. Do this *before* any cert |
| **GitHub Certified: Actions** | Claude | ~$99 converts years of real Actions work (cron orchestration, deploy guards, failure triage) into a filterable keyword. One weekend |
| **Microsoft AI-102 (Azure AI Engineer Associate)** | Claude | Hands-on AI credential from the vendor most Toronto banks standardize on; stronger bank-market signal than a third platform-native AI badge. ~$165 |
| **ServiceNow Now Assist / Agentic AI hands-on (CIS-level when GA)** | Claude, Nemotron | The one place a *targeted* SN AI credential beats a generic one — it sits directly on the held CSA/CAD + Agentic AI micro-cert, and Now Assist requisitions are outrunning supply |
| **Copado or Gearset Salesforce DevOps** | Buffy | The BMO "100% on-time deployment, zero downtime" claim rests on **change sets**, which hiring managers treat as legacy. One Copado fundamentals cert re-frames it as CI/CD and pairs with the GitHub Actions work |
| **ServiceNow ATF depth (a real test suite, not the micro-cert)** | Buffy | Least glamorous, most defensible *developer* differentiator: proves you can ship changes without breaking a bank's instance. Very few SN devs have written one |
| **ServiceNow UI Builder / Next Experience** | Buffy | Already claimed in skills, backed only by micro-certs. Portal work is where "developer" visibly separates from "admin" |
| **ITIL 4 Managing Professional module (CDS or DSV)** | Buffy | ITIL v4 Foundation is table stakes; one MP module turns "I know the framework" into "I can run a practice" |
| **Written architecture artefact** — 2 pages: CMDB data model + IRE/transform strategy + reconciliation controls, drawn from the CIBC work | Buffy, Claude | Not a cert; the only item here that proves seniority *in an interview* rather than on a transcript |
| **Salesforce Data Cloud Consultant** | Buffy | Only if the Salesforce path is chosen — Data Cloud + Agentforce is where 2026 requisitions are, and the SQL/data background shortens the ramp |
| **ISTQB Foundation / Test Automation Engineer** | Claude (conditional) | Only if targeting QA-lead-adjacent SN roles, where Playwright + ServiceNow ATF becomes a certified test-architecture story. Otherwise skip — it dilutes the integration narrative |

---

## 3. Where the sources diverge (and how it resolves)

| Question | Positions | Resolution |
|---|---|---|
| **Which platform first?** | Zoo and kilo present both; Buffy and Nemotron say ServiceNow primary; Claude endorses ServiceNow on recency | **ServiceNow primary.** The current role (CIBC, Jan 2025–) is ServiceNow; the Salesforce work ended Jan 2025 and is ~22 months stale. Recency beats breadth |
| **Is a cert the first move at all?** | Zoo, kilo, Buffy, Nemotron start with certs; Claude and Nemotron argue the portfolio artefact comes first | **Artefact first.** It is $0, removes screening friction, and reframes the profile as "platform dev who ships AI integrations" — the 2026 requisition profile |
| **Rank #1 (PD II vs CIS-IntegrationHub)** | Zoo, kilo, Buffy rank PD II #1; Nemotron ranks CIS-IntegrationHub #1; Claude treats both as path-dependent | **Both are #1 on their own path** — this was never a real disagreement, just different default paths. Integration-Hub first because ServiceNow is primary |
| **Cost data** | Only kilo priced the items | Adopted kilo's pricing throughout this document |
| **Role→cert matrices** | Only kilo supplied them | Kept in section 5 |
| **Cert maintenance** | Only Claude raised it | Adopted as a precondition — see section 6 |

---

## 4. Resume defects — fix these before spending a dollar

1. **Delete "Certifications under [redacted email]."** All five advisors flag it. It invites
   verification friction and signals the Now Learning / Trailhead records sit under an address not used
   professionally. Consolidate the accounts, then remove the line.
2. **Rename two certifications.** "Salesforce Certified Platform Administrator" → **Salesforce Certified
   Administrator**; "Salesforce Platform Developer" → **Platform Developer I**. A screener who knows the
   Salesforce cert tree catches this in seconds and discounts the entire section.
3. **Reconcile the two resume variants.** Resume 1 drops the Salesforce block from the header; resume 2
   drops CIS-ITSM. Background checks surface exactly this inconsistency.
4. **Fix the tenure arithmetic.** The summary says "6+ years" while the roles run from 2011 with
   ServiceNow from 2017–18 onward — write "6+ years ServiceNow, 15+ in IT/data" instead of leaving a
   screener to reconcile it.
5. **Add the AI & Automation portfolio section** (§2, first row). This is a resume defect of omission,
   not formatting.

---

## 5. Specialised role → certification matrix *(from kilo-auto, verified against the others)*

| Target role | Certifications |
|---|---|
| ServiceNow ITOM architect | CIS-ITOM + CIS-Discovery + CIS-Service Mapping |
| ServiceNow SecOps / IRM developer | CIS-SIR + CIS-RC/IRM + IAITAM CHAMP |
| ServiceNow AI / automation lead | Now Assist / Agentic AI + ServiceNow ATF depth |
| Salesforce integration architect | PD II + MuleSoft Developer I (+ Sharing & Visibility Architect later) |
| Salesforce DevOps / release engineer | Copado or Gearset + GitHub Actions cert |
| Data engineer (CMDB / asset focus) | Databricks Data Engineer Associate + dbt (or Snowflake SnowPro Core) |
| AI engineer (cross-platform) | AI-102 + Salesforce AI Specialist/Agentforce + Now Assist |
| ITAM manager | IAITAM CSAM/CHAMP + CIS-HAM + CIS-SAM (already held) |

---

## 6. Do not buy

- **More ServiceNow micro-certs.** Nine already; each additional one dilutes the signal.
- **ServiceNow CTA / CMA** — needs employer sponsorship and a multi-year track; not purchasable outright.
- **Salesforce Application / System Architect** — requires PD II first plus years of current hands-on.
- **Another knowledge-level AI cert.** AI Associate is held; the next step is the hands-on tiers.
- **A duplicate Databricks Data *Analyst* cert** (already listed) — the Engineer track or SnowPro is the step up.
- **Cert maintenance debt.** Twelve-plus ServiceNow certs each carry delta-exam maintenance. Before
  buying anything new, confirm every existing cert is in good standing on Now Learning — a lapsed CIS
  cert on a resume is worse than an absent one.

---

## 7. Final recommendation — ordered and dated

**Primary path: ServiceNow** (recency intact — current role has been ServiceNow since Jan 2025).

| When | Action | Cost | Why this order |
|---|---|---|---|
| **Week 1** | Fix the five resume defects; write the one-page AI/automation portfolio section; write the two-page CMDB/IRE architecture artefact | **$0** | Removes screening friction and reframes the profile before any money is spent |
| **Weeks 2–6** | **CIS-IntegrationHub** (full cert) | ~$250–350 | Cheapest credibility upgrade, highest-bill-rate specialty, directly supported by the Feedhub / 15-system / Scripted REST work |
| **Weeks 4–8** (parallel) | **GitHub Certified: Actions** | ~$99 | One weekend of prep given the existing pipeline work; converts invisible evidence into a keyword |
| **Weeks 6–12** | **CIS-ITOM** | ~$250–350 | Converts Metrolinx Discovery + CIBC CMDB reconciliation into a defensible specialty claim |
| **Weeks 12–20** | **CIS-SIR** — or ATF depth if SecOps roles do not appear | ~$250–350 | Opens SecOps/IRM, where the RBC vulnerability background is genuinely rare |
| **Months 5–7** | **Databricks Data Engineer Associate + dbt** *(or SnowPro Core)* | ~$200–300 | Moves the "800k-record reconciliation" story from ITAM consultant toward CMDB data engineer — materially more pay |
| **Months 7–9** | **IAITAM CSAM/CHAMP**, then **AWS SAA + Terraform Associate** | ~$300–500 + ~$220 | Vendor-neutral ITAM credibility, then cloud literacy for Discovery / Service Mapping |
| **Opportunistic** | **Now Assist / Agentic AI hands-on**; **ITIL 4 MP (CDS or DSV)**; **UI Builder depth** | Low | Take them when a requisition actually asks; they are differentiators, not prerequisites |

**Secondary path: Salesforce** — only if a current side project starts **now**, because the missing
ingredient is recency, not another badge.

| When | Action |
|---|---|
| Weeks 1–8 | **PD II** (the BMO material already qualifies) plus a small public Salesforce project or open-source contribution |
| Weeks 8–16 | **Salesforce Certified Administrator** (correct name), then **AI Specialist** |
| Months 4–6 | **Agentforce Specialist**, then **MuleSoft Developer I** or **Workato Automation Pro** |
| Later | **Data Cloud Consultant**; architect track only after PD II + two years of current SF work |

**Budget for the primary path, months 1–9:** roughly **$1,400–$1,900** of exams. The three highest-value
actions — resume fixes, AI/automation portfolio page, CMDB/IRE architecture artefact — cost nothing and
outrank every paid item on this list.

**One-line answer:** spend week one on the free artefacts, earn **CIS-IntegrationHub** as the single
depth signal, then **CIS-ITOM** and **CIS-SIR**; keep **PD II** as the first move only if Salesforce
becomes primary, and never buy another micro-cert.

---

*Merged from five independent advisories on 2026-11-02 by Buffy (DeepSeek V4.1 Flash). All source files
are preserved unchanged; this document is the consolidated recommendation. External advisory content
reflects the opinions of the models named, verified against the resumes in this repo where checkable.*

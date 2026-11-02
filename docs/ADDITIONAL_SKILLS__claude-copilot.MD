# Additional skills & certifications — Claude (Copilot) advisory

**Author:** Claude (Anthropic) via GitHub Copilot SDK in VS Code
**Date:** 2026-11-02
**Inputs:** `docs/ADDITIONAL_SKILLS.MD` (Zoo AI), `docs/ADDITIONAL_SKILLS__kilo-auto.md`,
`docs/ADDITIONAL_SKILLS__deepseek-v4.1-flash.MD`, plus direct observation of the owner's
engineering work in `eltonaguiar/findtorontoevents_antigravity.ca` and this repo.
**Scope:** what to learn/certify next. Job-search mechanics live in `docs/JOB_SEARCH_PLAYBOOK.md`.

---

## Where I agree with the prior three advisories (no need to re-argue)

- **One depth signal before anything else**: Salesforce PD II if SF-leaning, CIS-IntegrationHub
  (full) if ServiceNow-leaning. All four of us now say this; treat it as settled.
- **No more micro-certs.** Nine is already a dilution problem.
- **Fix the fabricated-looking cert names first** ("Salesforce Certified Platform Administrator"
  → Certified Administrator; "Salesforce Platform Developer" → Platform Developer I). This costs
  $0 and removes an instant-discount flag.
- **ServiceNow as the primary path** — recency is intact (CIBC, current); the Salesforce
  experience is ~22 months stale and PD II alone won't fix recency.

---

## What all three prior advisories missed: the portfolio already exists

Every prior advisory treats the profile as "ServiceNow/Salesforce consultant who should buy
certs." None of them noticed that the owner's own repositories demonstrate a **second, currently
hotter skill set** that is already built and merely needs to be made legible to recruiters:

| Demonstrated in the repos | Market label | Evidence |
|---|---|---|
| Multi-provider LLM orchestration (LiteLLM rotating proxy fronting 14+ providers, fan-out consults, agent swarms, cross-PC agent protocol) | **AI/Agent Engineer** | `tools/freellm.py`, LiteLLM proxy config, swarm skills, cross-PC gateway — all in `findtorontoevents_antigravity.ca` |
| GitHub Actions CI/CD at scale (hourly cron pipelines, deploy guards, infinite-loop protections, `[skip ci]` discipline, workflow-health auditing) | **DevOps / Platform Engineer** | `.github/workflows/` in both repos; `check-gh-actions` tooling |
| Playwright E2E suites across device profiles, smoke+deploy gates | **Test Automation Engineer** | `tests/*.spec.ts`, `sports-smoke-and-e2e.yml` |
| Python data pipelines against 9 MySQL databases, outcome resolvers, statistical validation (bootstrap, walk-forward, Wilson intervals) | **Data Engineer (applied)** | `alpha_engine/`, `audit_trail/`, `tools/` |

This matters because the ServiceNow/Salesforce AI requisitions of 2026 (Now Assist, Agentforce)
ask for exactly this hybrid: platform developer **plus** demonstrable LLM-integration experience.
The owner is one of the few candidates who can show working code rather than a badge.

**Action (costs $0, highest leverage item in this file):** write a 1-page "AI & Automation
Engineering" portfolio section — three bullet case studies with public evidence (the audit
dashboard, the multi-agent orchestration layer, the CI/CD pipeline) — and attach it to both
resume variants. Do this *before* buying any cert below.

---

## My ranked additions (items not in Zoo / kilo / DeepSeek lists)

| # | Item | Why | Cost |
|---|---|---|---|
| 1 | **GitHub Actions certification** (GitHub Certified: Actions) | The repos show years of real Actions work — cron orchestration, deploy guards, failure triage. A ~$99 exam converts invisible evidence into a filterable keyword. Pairs with the Copado/DevOps item DeepSeek raised. | ~$99 |
| 2 | **Microsoft AI-102 (Azure AI Engineer Associate)** | Hands-on (not awareness-tier) AI credential from the vendor most Toronto banks standardize on. The existing LLM-orchestration work shortens the ramp dramatically. Stronger bank-market signal than a third platform-native AI badge. | ~$165 USD |
| 3 | **ServiceNow Now Assist / AI micro-path → CIS-level when GA** | The one place a *targeted* ServiceNow AI credential beats a generic one: it sits directly on top of the held CSA/CAD + the Agentic AI micro-cert, and Now Assist requisitions are outrunning supply in 2026. | Low |
| 4 | **ISTQB Foundation + Test Automation Engineer (optional)** | Only if targeting QA-lead-adjacent SN roles: the Playwright + ServiceNow ATF story becomes a certified test-architecture narrative. Skip if pursuing the integration path — don't dilute. | ~$250 |
| 5 | **Publish, don't certify: 2 technical write-ups** | One on the multi-provider LLM failover proxy, one on CMDB reconciliation at 800k-CI scale. Blog posts or repo READMEs with architecture diagrams. Interviewers read these; they do not read cert transcripts. | $0 |

## Verification pass on the prior advisories (what I checked)

- **"Workato Automation Pro"** — real credential family (Automation Pro I/II/III), free training;
  reasonable low-cost pick as kilo/Zoo stated.
- **Agentforce Specialist / AI Specialist** — both are real, hands-on Salesforce certs as claimed.
- **PD II prerequisite chain** — correct as stated: PD I is held, so PD II is directly attemptable.
- **CTA/CMA "needs employer sponsorship"** — directionally right (multi-year, program-gated);
  correctly excluded.
- One caution: **cert maintenance debt.** 12+ ServiceNow certs each carry delta-exam maintenance.
  Before adding more, confirm the existing ones are all in good standing on Now Learning —
  a lapsed CIS cert on a resume is worse than an absent one.

---

## Consolidated 90-day sequence (merging all four advisories)

1. **Week 1 ($0):** fix cert names, delete the yahoo-email line, unify the two cert lists,
   add the AI & Automation portfolio section.
2. **Weeks 2–6:** **CIS-IntegrationHub (full)** — the agreed-upon depth signal on the live path.
3. **Weeks 4–8 (parallel, cheap):** **GitHub Actions cert** — one weekend of prep given the
   existing experience.
4. **Weeks 8–12:** **CIS-ITOM** — formalizes the Metrolinx/CIBC Discovery + reconciliation work.
5. **Ongoing:** publish the two write-ups; keep Salesforce alive only via a small current side
   project with PD II as its milestone (per DeepSeek's recency argument, which I endorse).

**Bottom line:** the prior advisories optimized the cert ladder; this one adds the missing move —
packaging the already-demonstrated AI/automation engineering so the profile reads as
"platform developer who ships AI integrations," which is the 2026 requisition profile,
not "consultant collecting badges."

---

*Prepared by Claude (Anthropic) via GitHub Copilot SDK, 2026-11-02. Prior advisories preserved
unchanged in `ADDITIONAL_SKILLS.MD`, `ADDITIONAL_SKILLS__kilo-auto.md`, and
`ADDITIONAL_SKILLS__deepseek-v4.1-flash.MD`.*

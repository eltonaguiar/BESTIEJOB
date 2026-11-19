# Hermes cron scan — fresh Toronto ServiceNow & Salesforce jobs — 2026-11-19 05:00 EST

Scan run: 2026-11-19 05:00 EST (2026-11-19T10:00Z).
Source: FRESH_JOBS.md — output of `scripts/daily_job_scan.mjs` run 2026-11-19T09:13Z, 2437 postings from 10 public sources (adzuna, linkedin, workday, greenhouse, smartrecruiters, remotive, jobicy, ashby, lever, remoteok).
Scope: Toronto (incl. GTA/remote-Canada rows already on the board), ServiceNow + Salesforce platform-build tracks only. Deduplicated against README.md tables (6252 link-rows parsed) — none of the rows below were already present.

Verification notes this cycle:
- LinkedIn detail pages are behind a sign-in wall for unsigned agents (confirmed: login wall on all five ca.linkedin.com detail URLs opened). Posted date / title / company / location below come from the committed daily scan; duties were NOT re-verified on an employer page. Rows whose titles do not unambiguously denote platform build work were left out (see JOBLESSONS_2026-11-19T0500EST.MD).
- Adzuna detail URLs (CloudFront 403 via browser and HTTP) and Job Bank (connection reset / JS shell) could not be opened; those leads are recorded in the lessons file for a later cycle, not merged.

|| Posted | Role | Company | Location | URL | Note |
|---|---|---|---|---|---|---|
| 2026-11-18 | [ServiceNow ITOM Developer](https://ca.linkedin.com/jobs/view/servicenow-itom-developer-at-techneptune-consulting-inc-4491345268) | TechNeptune Consulting Inc. | Toronto, Ontario, Canada | via hermes-cron--2026-11-19--v1.md · servicenow · sourced from FRESH_JOBS daily scan 2026-11-19T09:13Z; Toronto ITOM platform role; LinkedIn detail gated to signed-in viewers this cycle — duties not re-verified |
| 2026-11-18 | [ServiceNow Developer](https://ca.linkedin.com/jobs/view/servicenow-developer-at-spectraforce-4492200627) | SPECTRAFORCE | Toronto, Ontario, Canada | via hermes-cron--2026-11-19--v1.md · servicenow · sourced from FRESH_JOBS daily scan 2026-11-19T09:13Z; Toronto developer role; LinkedIn detail gated to signed-in viewers this cycle — duties not re-verified |
| 2026-11-18 | [ServiceNow CMDB](https://ca.linkedin.com/jobs/view/servicenow-cmdb-at-techneptune-consulting-inc-4491354155) | TechNeptune Consulting Inc. | Toronto, Ontario, Canada | via hermes-cron--2026-11-19--v1.md · servicenow · sourced from FRESH_JOBS daily scan 2026-11-19T09:13Z; Toronto CMDB platform role; LinkedIn detail gated to signed-in viewers this cycle — duties not re-verified |

Dropped this cycle (reasons in JOBLESSONS_2026-11-19T0500EST.MD):
- Accenture "Consultant MarTech spécialisé en Salesforce Data Cloud" ×2, Toronto 2026-11-19 — LinkedIn gated; "MarTech" title leans marketing-ops, unverifiable as platform build work this cycle.
- PwC Canada "Salesforce Business Analyst, Associate" Toronto 2026-11-18 — same precedent as cycle 4 (PwC BA Associate 4492083143 dropped: guest view shows no datePosted or duties).
- Nuvei Salesforce Business Process Analyst Toronto 2026-11-17; Maarut "Senior Platform Support Analyst with data cloud" Toronto 2026-11-17; TD Bank "Senior Solution Architect (ServiceNow)" Canada 2026-11-18 — adzuna.ca/details blocked (CloudFront 403), employer page and duties unverifiable.
- Lane Four Salesforce Consultant / Administrator (Canada) — undated on employer page; merger skips undated rows by design (recorded in inbox/gap-scan--2026-11-19--v2.md).
- Rogers (jobs.rogers.com), Bell (jobs.bell.ca), Government of Canada (jobbank.gc.ca) partner/employer pages checked via search — portals exist but are bot-gated or JS shells; no dated Toronto SN/SF posting could be captured this cycle.

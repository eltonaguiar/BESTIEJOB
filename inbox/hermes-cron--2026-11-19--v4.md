# Hermes cron scan — fresh Toronto ServiceNow & Salesforce jobs — 2026-11-19 19:00 EST

Scan run: 2026-11-19 19:00 EST (2026-11-20T00:00Z).
Sources this cycle: Adzuna CA (Toronto + Canada, `max_days_old=2`, 12 queries, 172 unique), Job Bank Ontario (servicenow/salesforce, newest first), City of Toronto careers (SuccessFactors), Bell careers, Ontario PS gojobs, documented ATS APIs for the partner watchlist (Lever: Alimentiv, EQ Bank, Versapay, Electric Mind; Greenhouse: Levio; Ashby: Solink, CEA; SmartRecruiters: Ensiti), plus web searches for Rogers/Bell/government postings.
Scope: ServiceNow + Salesforce platform-build roles in Toronto/GTA or Canada-remote, deduplicated against README.md (6,207 link-rows) and jobs.json (5,596 feed rows).

Verification: both rows below opened 200 with an absolute LinkedIn `datePosted` on the posting itself (Virtusa 2026-11-19T22:45:40Z, Cognizant 2026-11-19T22:56:54Z); neither is "no longer accepting".

| Posted | Role | Company | Location | Note |
|---|---|---|---|---|
| 2026-11-19 | [ServiceNow ITOM Developer](https://ca.linkedin.com/jobs/view/servicenow-itom-developer-at-virtusa-4491652533) | Virtusa | Toronto, Ontario, Canada | via hermes-cron--2026-11-19--v4.md · servicenow · live 200, datePosted 2026-11-19T22:45Z on posting; ITOM/Discovery platform build |
| 2026-11-19 | [Senior Salesforce Developer](https://ca.linkedin.com/jobs/view/senior-salesforce-developer-at-cognizant-4492525247) | Cognizant | Toronto, Ontario, Canada | via hermes-cron--2026-11-19--v4.md · salesforce · live 200, datePosted 2026-11-19T22:56Z on posting; Cognizant Canada delivery practice |

Dropped this cycle (reasons in JOBLESSONS_2026-11-19T1900EST.MD):
- AsceticVoyage "Senior Salesforce Developer" Canada 2026-11-18 — live page but "no longer accepting applications".
- PwC Canada "Technical Salesforce Associate" Ottawa 2026-11-18 — live/accepting but no `datePosted` on the posting; same precedent that dropped the PwC BA Associate row in cycle 2026-11-19T05:00Z.
- EQ Bank "Senior ServiceNow Engineer" Toronto — live Lever posting but created 2026-09-22 (58 days old, outside the 30-day window).
- Levio ServiceNow roles (Montréal/Québec) — live Greenhouse postings first published 2025-09-15 and 2023-11-29.
- Alimentiv "ServiceNow Platform Specialist" — already on the board (lever URL).
- TMX "Manager, Incident, Problem & Event Management" Toronto 2026-11-19 — keyword match only; body names no ServiceNow.
- Appficiency "Account Executive - Redpoint" — sales function, excluded by board rules.

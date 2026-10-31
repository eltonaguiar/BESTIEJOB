ï»¿# BESTIEJOB

Toronto-focused job posting consolidator for creative / technology manager roles with a salary minimum filter.

## Filters

- Location: Toronto (and GTA text matches)
- Role keywords: creative / technology / manager / management
- Employment: full-time (best-effort detection)
- Salary: minimum salary slider (default $100K, preset $110K)

## Simplify applications source

This project can pull your Simplify Applications list (requires an authenticated cookie).

- Set `SIMPLIFY_COOKIE` in the environment **or** pass `simplifyCookie` as a query param to `/api/jobs`.
- Use `timelineDays` to limit results to the last N days (defaults to 30).

Example:

```
/api/jobs?keywords=product%20manager&timelineDays=14
```

## Running locally

```bash
npm install
npm run dev
```

Then open:

- http://localhost:3000

## Add-On Pages

#### ðŸ’° [Salary Insights](/salary-insights/)
Visual salary analysis and trends for Toronto tech and creative manager roles:
- Average and median salary metrics
- Salary breakdown by role category
- Comparison across company types (Big Tech, Startups, Banks, etc.)
- Detailed salary ranges table
- Salary negotiation tips

#### ðŸ“š [Career Resources](/career-resources/)
Essential guides for your Toronto tech career:
- Interview preparation (common questions, STAR method, technical prep)
- Resume and CV optimization tips
- Salary negotiation strategies
- Networking resources and Toronto tech communities
- LinkedIn optimization tips

#### ðŸ“‹ [Application Tracker](/tracker/)
Track every application from Saved to Offer with stats and backups:
- Add and manage job applications
- Track status and next actions
- Store notes, job URLs, and follow-ups
- Simple export/import for backups

#### ðŸ“Š [Market Report](/market-report/)
Toronto tech hiring snapshots:
- Current hiring trends and volume
- In-demand skills for managers and creatives
- Top hiring industries and companies
- Market-specific job search tips

#### ðŸ¤– [AI Match Lab](/ai-match-lab/)
- Transparency into how skills, salaries, and fairness checks shape matches
- Feedback loops that tune recommendations with saves, dismissals, and ratings
- Linkbacks to the tracker and main search keep the AI outputs actionable

#### ðŸ’¬ [Experience Hub](/experience-hub/)
- Timelines, recruiter response windows, and structured metadata keep candidates informed
- Freshness, remote-ready, and salary-disclosure badges reinforce trust
- Accessibility hints and feedback loops keep communication respectful and predictable

#### ðŸ“± [Mobile Studio](/mobile-studio/)
- Mobile-first filters, chips, and PWA shortcuts keep Toronto job hunting fast on the go
- Low-data visual patterns and voice/keyboard hints keep every device responsive
- Micro dashboards for push alerts, saved searches, and offline-ready shortlists

## Recent Job Scan Findings — ServiceNow + Salesforce (opencode, 2026-10-30)

A dedicated job-scan branch was created: `opencode-2026-10-30`

Full listing: [`opencode-2026-10-30-servicenow-salesforce-jobs.md`](https://github.com/eltonaguiar/bestiejob/blob/opencode-2026-10-30/opencode-2026-10-30-servicenow-salesforce-jobs.md)

### Summary
- **ServiceNow**: 40+ listings across Toronto/Ontario, fully-remote Canada, and USA (security-clearance roles). Each mentions CSA/CAD or ServiceNow platform.
- **Salesforce**: 40+ listings across Toronto/Ontario, fully-remote Canada, and USA. Each mentions Salesforce Administrator or Salesforce Platform Developer.
- Priority order: Toronto/Ontario → fully remote → remote-eligible Canada → remote USA.
- All entries are Adzuna-sourced and flagged **Unverified** — confirm live on the employer Apply page before applying.
- Sources checked: Adzuna CA/US API, SI Systems (404), RBC Careers (general page only), Randstad Canada (no SN/SF in first 30).

### Top Toronto/Ontario picks

**ServiceNow**
- ServiceNow Administrator-CSA/Banking — BeachHead Inc. (Toronto) — explicit CSA/Banking — 2026-10-29
- ServiceNow Technical Lead — CAAT Pension Plan (Toronto) — $107,800–$133,700 — 2026-10-22
- Senior ServiceNow Engineer — EQ Bank (Toronto) — 2026-10-29
- ServiceNow Developer (CONTRACT ROLE) — Brookfield Properties (Toronto) — 2026-10-22
- ServiceNow Business Analyst — Intercast Staffing Ltd. (Toronto) — 2026-10-29
- ServiceNow Admin — Forhyre (Toronto) — 2026-10-15
- ServiceNow System Administrator — Forhyre (Toronto) — 2026-10-15
- ServiceNow Architect — Acestack (Regent Park, Toronto) — 2026-10-29
- ServiceNow AIOps Architect — BULL-IT SOLUTIONS LTD (Toronto) — 2026-10-30
- Senior Manager, ServiceNow - Operate — Deloitte (Toronto) — 2026-10-21
- Technology Lead, Enterprise Platforms & Operation (Director) — TMX Group (Toronto) — 2026-10-29

**Salesforce**
- Senior Salesforce Administrator — Loopio (Toronto) — $85,000–$105,000 — 2026-10-15
- Senior Salesforce Developer / Admin — Celestica (Toronto, hybrid) — 2026-10-29
- Consultant, Salesforce Development — CIBC (Toronto) — 2026-10-29
- Software Engineer II (Salesforce Loyalty Management Developer) — TD Bank (Toronto) — 2026-10-28

## Navigation
- **Home** (/) - Main job search with filters
- **Find Jobs** (/gotjob/) - Alternative job search interface with filters, source tuning, and stats
- **Salary Insights** (/salary-insights/) - Salary analysis and trends
- **Career Resources** (/career-resources/) - Interview prep, resume tips, negotiation guides
- **Tracker** (/tracker/) - Personal job application tracking
- **Market Report** (/market-report/) - Toronto tech market insights
- **AI Match Lab** (/ai-match-lab/) - Explainable AI matching lab
- **Experience Hub** (/experience-hub/) - Candidate experience timeline and transparency
- **Mobile Studio** (/mobile-studio/) - Mobile-first search workflow

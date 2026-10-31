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

## Job Scan (2026-10-30)

Agent **kilo** ran a targeted ServiceNow + Salesforce job scan across Canadian bank portals, IT recruiting agencies, startup job sites, and remote boards.

**Scanned sources:** Scotiabank careers, BMO careers, jobs.ca (BFG, Brock Solutions, Tekgence, PrecisionERP, Systematix, Hanalytica, LeverageTek), startup.jobs, builtintoronto.com, Teal HQ, Remotive, Indeed CA/US, ZipRecruiter, Greenhouse, Lever, Jooble.

**Key fresh finds (last 7 days at scan time):**

| Role | Company | Location | Posted | CSA/CAD | Apply |
|------|---------|----------|--------|---------|-------|
| ServiceNow Developer | **BMO** | Toronto, ON | Oct 2026 | CSA + CAD **required** | https://jobs.bmo.com/ca/en/job/BOMOGLOBALR260027442EXTERNALENCA/ServiceNow-Sr-Developer-ITSM-AI-GRC |
| ServiceNow Developer | **Scotiabank** | Toronto, ON | Oct 24, 2026 | "a plus" | https://jobs.scotiabank.com/job/Toronto-ServiceNow-Developer-ON-M5H-1H1/603030017 |
| ServiceNow Developer | **City of Toronto** | Toronto, ON | Oct 5, 2026 | CSA req, CAD asset | https://jobs.toronto.ca/jobsatcity/job/Toronto-SYSTEMS-INTEGRATOR-1-%28SERVICENOW-DEVELOPER%29-ON-M5V-3C6/606700617 |
| ServiceNow Developer | **Brookfield** | Toronto, ON | Oct 20, 2026 | CSA + CAD | https://www.jobs.ca/brookfield-asset-management/jobs/servicenow-developer-contract-role-toronto-on-8b05d6a30bcc |
| ServiceNow Developer | **BFG Enterprise** | Markham, ON | Sep 25, 2026 | CSA/CAD preferred | https://careers.bfg.ca/jobs/707075-servicenow-administrator-developer-intermediate |
| ServiceNow Developer | **Brock Solutions** | Cambridge, ON | Oct 8, 2026 | CSA/CAD preferred | https://www.jobs.ca/brock-solutions/jobs/servicenow-developer-cambridge-on-6ec3ecdaeeda |
| ServiceNow Dev (ITOM) | **Systematix** | Remote (CA) | Oct 17, 2026 | CSA/CAD preferred | https://www.jobs.ca/systematix/jobs/senior-servicenow-developer-itom-remote-canada-d1404c402e83 |
| ServiceNow Architect | **Crossfuze** | Remote (CA) | Oct 30, 2026 | unverified | https://ca.jooble.org/job/servicenow-architect-fully-remote-at-crossfuze |
| ServiceNow Developer | **ManTech** | Remote (US) | Oct 2026 | CSA required | https://www.tealhq.com/job/servicenow-developer_7ea1a1aef814edcd42f24316d105d73bc9d4e |
| ServiceNow Architect | **RSC Solutions** | Jersey City, NJ | Recent | CSA+CAD+CIS | https://www.ziprecruiter.com/c/RSC-Solutions/Job/ServiceNow-Architect/-in-Jersey-City,NJ |

**Full curated lists** (20 ServiceNow + 20 Salesforce with links, salaries, posting dates, and cert verification): see `kilo-2026-10-30-servicenow-salesforce-jobs.md`

Legend: cert quoted verbatim from posting | unverified (standard expectation, not quoted verbatim)

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

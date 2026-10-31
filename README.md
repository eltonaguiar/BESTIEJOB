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

## Job-hunt findings — ServiceNow / Salesforce scan (Buffy, 2026-10-31)

Buffy's agent reports live in their own files; this is the summary of what each new scan technique found,
kept here so the next run does not repeat dead ends.

**Latest report:** [`buffy-2026-10-30.md`](buffy-2026-10-30.md) — 230 unique roles
(ServiceNow 110, Salesforce 120), 152 in Toronto/Ontario, 2 fully remote,
200 with a confirmed posting date inside the 21-day window.

### What worked

| Technique | Endpoint | Result |
|---|---|---|
| LinkedIn guest jobs API | `linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=…&location=…&start=…&f_TPR=r1814400` | **Best single source.** 10 cards/page, each with title, company, location, exact `datetime`, direct `/jobs/view/` URL. No auth. 273 postings across 11 queries. |
| Bang for the buck | Broad queries: `servicenow` + `Canada`, `salesforce administrator` + `Canada` | City-only queries dedupe heavily against each other; country-wide queries surfaced the most new reqs. |
| SmartRecruiters public API | `api.smartrecruiters.com/v1/companies/{company}/postings?limit=100&offset=N` | Structured JSON with `releasedDate`, city/region/country, remote+hybrid flags. Vendor-neutral: works for any employer on SmartRecruiters. |
| Canadian bank Workday CXS | `POST https://{tenant}.wd3.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` | Live for **TD** (`TD_Bank_Careers`), **BMO** (`External`), **CIBC** (`search`) only. Gives req-number URLs and `postedOn`. |
| Scrapling `StealthyFetcher` | `from scrapling.fetchers import StealthyFetcher` | **Defeated every 403.** Workopolis, CareerBeacon and Talent.com all return HTTP 403 to curl but **HTTP 200** to Scrapling with a headless Chrome. Use it whenever a plain fetch is refused. |
| Eluta.ca | `eluta.ca/search?q=…&l=…&pg=N` | Plain HTML, 10 `organic-job` cards/page with title, employer, location, remote flag. **No posting dates** — the one real weakness. |
| CareerBeacon | Scrapling → `data-posting_url` attribute | Gives a **direct** `/en/job/{id}/{company}/{slug}` URL per card, plus company/location. |

### What is blocked, and why

| Source | Failure | Notes |
|---|---|---|
| Workopolis (curl) | HTTP 403 | Fine through Scrapling. Its "past week" ServiceNow-Toronto filter has also gone empty. |
| CA banks other than TD/BMO/CIBC | HTTP 422 on the CXS path | Scotiabank, RBC, Manulife, Sun Life, Telus, Rogers, CPPIB, OMERS, OPG, Metrolinx, Canada Life, NBC, CGI, Brookfield, Equifax — 4 `wd` shards × 12 site-name variants all rejected. The site identifier is not guessable; scrape the careers page to discover it. |
| SI Systems | HTTP 403 (WAF "Request Rejected") then 404 | `/jobs/?q=` path no longer exists; the homepage loads but has no listings. |
| IFG | TLS connection killed / 404 | Homepage loads; `/jobs/` is gone. |
| Procom | DNS `ERR_NAME_NOT_RESOLVED` | Host does not resolve from this environment at all. |
| Job Bank Canada | JS-rendered | No structured payload without a browser. |
| Greenhouse / Lever / Ashby token guesses | 404 | Board tokens must be discovered from the employer's own careers page — guessing `clio`, `wave`, `hopper`, `wealthsimple`, `shopify` all failed. |
| Jooble, Talent.com (curl), Workopolis (curl) | HTTP 403 | All three work through Scrapling. |
| Indeed | RSS 404 | The `/rss` endpoint is retired. |

### Structural findings worth remembering

- **Canadian banks do not post ServiceNow-titled jobs.** All 24 ServiceNow hits across TD/BMO/CIBC were
  unrelated roles that merely mention ServiceNow as a nice-to-have. Banks staff ServiceNow through
  Deloitte, KPMG, Cognizant and Huron, and hire via agencies — so **the agency board is the door, not the
  bank portal.**
- **CareerBeacon and Talent.com are Next.js apps.** CareerBeacon keeps job data in `data-posting_url` /
  `data-jid` attributes; Talent.com streams it via `self.__next_f.push`. Regex the attributes, do not look
  for `__NEXT_DATA__` (it is absent on both).
- **Eluta omits dates**; treat its rows as leads needing a date check on the detail page.
- Dedupe on **company + normalised title**, not title alone: the same req commonly appears in two cities
  (Toronto + Ottawa/Montréal) and under brand variants (`Panasonic` / `PCI Panasonic Canada Inc.`).

### Source mix in the current report

| Source | Rows |
|---|---|
| LinkedIn | 141 |
| Eluta | 30 |
| Workopolis | 28 |
| CareerBeacon | 26 |
| Workday | 4 |
| ServiceNow careers | 1 |

*Compiled by Buffy. Aggregation only — not financial or career advice.*

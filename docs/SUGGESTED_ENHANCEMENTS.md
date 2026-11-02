# BESTIEJOB — Suggested Enhancements & Features

Generated: 2026-11-02T15:20:00Z by Kilo (nvidia/nemotron-3.5-super-vl:free)

## Current state (observed on https://eltonaguiar.github.io/BESTIEJOB/)

- Dark theme, three section tabs: ServiceNow / Salesforce / Other
- Global search input (title/company/location)
- Per-job cards: title, company, location, source note, posted date
- Category tags: servicenow / salesforce / other / today
- Data source: `public/jobs-data.json` (built from `README.md`)
- Mobile-responsive grid layout
- Add-on pages: /ai-match-lab/, /experience-hub/, /mobile-studio/, /salary-insights/, /career-resources/
- Built with plain HTML/CSS/JS (no framework)

---

## Suggested enhancements (prioritized)

### P0 — High impact, low effort

| # | Enhancement | Rationale |
|---|-------------|-----------|
| P0-1 | **Last-updated date-time stamp** in header | Users need to know data freshness at a glance. Currently "Dates are the source posting dates" but no "built at" timestamp. Add `Last updated: YYYY-MM-DD HH:MM Z` next to the data source link. |
| P0-2 | **Tabbed interface (ServiceNow / Salesforce / Other)** — make tabs actually switchable | The page already renders all three sections, but true tab switching (hide/show) improves UX on mobile and reduces visual noise. Add `data-tab` attributes + JS click handler. |
| P0-3 | **"Apply / Verify live" link validation** | Aggregator mirrors expire. Add a small "Verify live" icon/button per card that hits the source URL HEAD and shows green/red status. |
| P0-4 | **Posted date sorting within each tab** | Currently newest-first in README but the HTML may not guarantee sort. Add explicit date sort + "Newest first" default. |
| P0-5 | **Bookmark / shortlist (localStorage)** | Let users star jobs they want to revisit. Persist to localStorage, show starred count in header. |

### P1 — Medium impact

| # | Enhancement | Rationale |
|---|-------------|-----------|
| P1-1 | **Salary filter / range display** | README mentions "salary minimum filter" but the UI doesn't show salary ranges. Parse salary from posting text or add a manual salary field per card. |
| P1-2 | **Company logo / favicon** | Visual recognition helps scanning. Fetch company domain favicon via `https://www.google.com/s2/favicons?domain=...` or use Clearbit logo API. |
| P1-3 | **Resume-fit scoring** | Tag each job with a fit score (high/medium/low) based on keyword match against the resume (ServiceNow CSA/CAD/ITSM, Salesforce Apex/SOQL, VBA/PowerShell/Alteryx/Python/SQL/Tableau). |
| P1-4 | **"Similar jobs" carousel** | Show 2-3 related jobs from same company or same keyword family at bottom of each card. |
| P1-5 | **Export to CSV / ICS** | Let users export shortlist to CSV (for spreadsheet tracking) or ICS (for apply-by calendar reminders). |

### P2 — Lower effort, nice-to-have

| # | Enhancement | Rationale |
|---|-------------|-----------|
| P2-1 | **Dark/light mode toggle** | Accessibility preference. |
| P2-2 | **Keyboard shortcuts** (`/` for search, `1`/`2`/`3` for tabs, `ESC` to clear) | Power-user efficiency. |
| P2-3 | **Share job via copy link** | Copy card URL to clipboard. |
| P2-4 | **Source badge with reliability score** | Distinguish employer-ATS (high reliability) vs aggregator (medium) vs peer-scan (lower). Color-code the source badge. |
| P2-5 | **RSS feed per category** | Let power users subscribe to new postings per category. |

---

## Technical notes

- The site is plain HTML/CSS/JS — no build step. Enhancements should stay vanilla JS to match existing patterns.
- `public/jobs-data.json` is generated from `README.md` by a merge script (`scripts/...jobs_merge_inbox.py`). Any new fields (salary, fit score, source reliability) need to be added to both the README row format and the merge script.
- GitHub Pages serves from `public/` folder. Changes to `public/index.html` and `public/app.js` deploy on push to main.

---

## Open questions

1. Should the "Last updated" timestamp reflect README commit time or jobs-data.json build time?
2. Should salary parsing be regex-based (from posting text) or manual entry in README?
3. Should the fit score use exact keyword matching or fuzzy/LLM-based matching?

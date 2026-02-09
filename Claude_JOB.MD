# Claude Job Site Enhancement Plan

## Overview

This document outlines 4 add-on pages designed and drafted to enhance the BESTIEJOB job aggregation platform. These pages follow industry standards from top job sites (Indeed, LinkedIn, Glassdoor, ZipRecruiter) and leverage the existing 13,800+ job database to provide additional value beyond job search.

**Design system:** All pages use the existing dark theme with purple accents (`#7c5cff`), glassmorphism panels, radial gradient backgrounds, and the same font stack (`ui-sans-serif, system-ui, ...`).

**Tech stack:** Vanilla JavaScript, no frameworks — consistent with the existing site.

**Data source:** All pages load from `/gotjob/jobs.json` and perform client-side analysis.

---

## Page 1: Salary Explorer (`/salaries/`)

**Status:** Drafted (HTML + CSS + JS complete)

**Files:**
- `public/salaries/index.html`
- `public/salaries/styles.css`
- `public/salaries/app.js`

**Industry inspiration:** Glassdoor salary tool, Levels.fyi, Payscale

### Features

| Feature | Description |
|---------|-------------|
| **Salary Distribution Chart** | Bar chart showing job counts across $10K salary buckets |
| **Top Paying Roles** | Horizontal bar chart ranking roles by median salary (min 2 data points) |
| **Salary by Experience Level** | Cards showing median salary for Entry / Mid / Senior / Lead / Manager |
| **Top Paying Companies** | Horizontal bar chart ranking companies by median salary |
| **Detailed Salary Table** | Sortable table with role, company, salary, level, type — paginated |
| **Filters** | Search by role, filter by experience level and work arrangement |
| **Stats Overview** | Jobs with salary, median, average, and range across filtered results |

### Key Implementation Details

- `getAnnualSalary()` normalizes hourly rates to annual (hourly * 2080 hours)
- `normalizeRoleTitle()` strips seniority prefixes for grouping similar roles
- `detectExperienceLevel()` parses title/excerpt for seniority keywords (same logic as gotjob)
- Table supports column sorting (role, company, salary, level) with "load more" pagination
- Filters: role search (comma-separated), experience dropdown, work arrangement dropdown
- Salary buckets auto-scale based on min/max in filtered data

---

## Page 2: Market Analytics (`/analytics/`)

**Status:** Drafted (HTML + CSS + JS complete)

**Files:**
- `public/analytics/index.html`
- `public/analytics/styles.css`
- `public/analytics/app.js`

**Industry inspiration:** LinkedIn Talent Insights, Indeed Hiring Lab, Glassdoor Economic Research

### Features

| Feature | Description |
|---------|-------------|
| **Key Metrics Dashboard** | 6 cards: Total listings, Posted today, Companies hiring, Remote jobs, % with salary, Data sources |
| **Job Posting Timeline** | 30-day bar chart showing daily posting activity (today highlighted in green) |
| **Source Breakdown** | CSS conic-gradient donut chart with legend showing top 8 sources + "other" |
| **Employment Type Breakdown** | Donut chart: full-time vs contract vs part-time vs internship vs unknown |
| **Most In-Demand Roles** | Horizontal bar chart of role categories (Software Dev, Data Science, DevOps, etc.) |
| **Work Arrangement Trends** | 3 cards showing Remote / Hybrid / Onsite counts and percentages |
| **Experience Level Demand** | Horizontal stacked bars for Entry / Mid / Senior / Lead / Manager |
| **Trending Skills Cloud** | Tag cloud of 30 most-mentioned skills, sized by frequency |

### Key Implementation Details

- `categorizeRole()` maps job titles to 19 role categories using regex patterns
- `extractSkills()` scans title + excerpt against 35+ skill patterns (Python, AWS, React, etc.)
- `CHART_COLORS` array of 20 colors for consistent chart theming
- Donut charts use pure CSS `conic-gradient()` — no chart library needed
- Skills cloud sizes tags from 12px to 26px based on frequency ratio
- Timeline shows all 30 days with "today" bar highlighted green

---

## Page 3: Company Explorer (`/companies/`)

**Status:** Drafted (HTML + CSS + JS complete, but index.html was overwritten by another process)

**Files:**
- `public/companies/index.html` (needs restoration — see note below)
- `public/companies/styles.css`
- `public/companies/app.js`

**Industry inspiration:** Glassdoor company profiles, LinkedIn company pages, Wellfound company explorer

### Features

| Feature | Description |
|---------|-------------|
| **Company Cards Grid** | Responsive grid showing company name, job count badge, industry tag, avg salary, remote count |
| **Industry Classification** | Auto-classifies companies into Tech / Banking / Consulting / Telecom / Insurance / Staffing / Other |
| **Company Detail Modal** | Click a card to see all open positions with salary and date, plus company stats |
| **Search & Filter** | Company name search, industry dropdown, sort by (jobs / salary / name / recent) |
| **Stats Dashboard** | Companies hiring, open positions, avg jobs per company, % posting salary |
| **Top Roles Preview** | Each card shows the company's top 5 most common role titles |
| **Pagination** | "Load more" button showing 30 companies at a time |

### Key Implementation Details

- `classifyIndustry()` uses regex to match company names to known Canadian employers (Big 5 banks, Big 4 consulting, etc.)
- `getTopRoles()` normalizes titles by stripping seniority prefixes, then counts occurrences
- `buildCompanyData()` aggregates all jobs into company profiles with salary arrays, remote counts, latest dates
- Modal shows all open positions sorted by date, each linking to the original job posting
- Escape key and overlay click close the modal

### Note: File Conflict

The `companies/index.html` file was overwritten by another concurrent process. The intended version uses our standard dark theme with `styles.css` and `app.js`. The current file references a different design system (`/components/styles-shared.css`, Google Fonts). **To restore:** rewrite `index.html` to use the nav menu, dark theme, and link to local `styles.css` + `app.js`.

---

## Page 4: Career Resources (`/resources/`)

**Status:** Partially drafted (HTML written but directory was removed by another process; CSS written)

**Files (intended):**
- `public/resources/index.html`
- `public/resources/styles.css`
- No app.js needed (static content with smooth-scroll only)

**Industry inspiration:** Indeed Career Guide, LinkedIn Career Advice, The Muse

### Features

| Section | Content |
|---------|---------|
| **Quick Links** | 4 jump cards: Resume Tips, Interview Prep, Salary Negotiation, Toronto Market |
| **Resume & Cover Letter Guide** | ATS optimization, quantifying impact, cover letter framework, Canadian resume standards |
| **Interview Preparation** | STAR method breakdown, common questions with strategies, technical interview tips, questions to ask |
| **Salary Negotiation** | 5-step negotiation playbook, Toronto benefits guide, "know your worth" factors |
| **Toronto Market Guide** | Top hiring districts (Financial District, MaRS, Liberty Village, etc.), hiring seasons, networking tips, work permits |
| **Explore Our Tools** | Links to all 4 tool pages (Job Search, Salary Explorer, Analytics, Company Explorer) |

### Key Implementation Details

- Static content page — no JavaScript data loading needed
- Smooth-scroll anchor links for quick navigation between sections
- Pro-tip callout boxes with purple accent borders
- STAR method visualization with circular letter badges
- Interview Q&A with left-border accent styling
- 5-step negotiation timeline with numbered gradient circles
- Toronto district list with accent-bordered cards
- Cross-links to Salary Explorer for data-backed negotiation research

---

## Navigation Structure

All pages share a consistent nav menu:

```
Home | Find Jobs | Tech Jobs | Salaries | Analytics | Companies | Resources
 /      /findjobs/   /gotjob/    /salaries/  /analytics/ /companies/ /resources/
```

The active page is highlighted with `var(--accent)` purple color.

---

## Remaining Work

### Must Do
1. **Restore `companies/index.html`** — Rewrite to use the dark theme with local CSS/JS (was overwritten by another process)
2. **Recreate `resources/` directory** — Directory was removed; recreate with index.html, styles.css
3. **Update existing page navs** — Add links to new pages in the nav menus of:
   - `public/index.html`
   - `public/findjobs/index.html`
   - `public/gotjob/index.html`
4. **Test all pages** — Verify they load jobs.json correctly and render properly

### Nice to Have (Future)
- **Job Alerts page** — Email notification signup for new matching jobs
- **Resume Builder** — Template-based resume generator
- **Skills Assessment** — Quiz-based skill evaluation with job recommendations
- **Saved Searches** — Save and name filter combinations for quick access
- **Compare Jobs** — Side-by-side job comparison tool
- **Mobile PWA** — Service worker for offline access and push notifications

---

## File Summary

| Path | Status | Lines | Description |
|------|--------|-------|-------------|
| `public/salaries/index.html` | Complete | ~100 | Salary Explorer page structure |
| `public/salaries/styles.css` | Complete | ~280 | Salary page styling (charts, tables, stats) |
| `public/salaries/app.js` | Complete | ~320 | Data loading, filtering, 5 chart renderers |
| `public/analytics/index.html` | Complete | ~90 | Analytics dashboard structure |
| `public/analytics/styles.css` | Complete | ~280 | Dashboard styling (metrics, charts, clouds) |
| `public/analytics/app.js` | Complete | ~300 | 8 visualization renderers |
| `public/companies/index.html` | Needs restore | ~98 | Company Explorer (overwritten) |
| `public/companies/styles.css` | Complete | ~475 | Company cards, modal, responsive grid |
| `public/companies/app.js` | Complete | ~310 | Company aggregation, filtering, modal |
| `public/resources/index.html` | Needs recreate | ~290 | Career resources (directory removed) |
| `public/resources/styles.css` | Needs recreate | ~220 | Resource cards, STAR grid, Q&A styling |

---

## Design Tokens (Shared)

```css
--bg: #0b1020
--panel: rgba(255, 255, 255, 0.06)
--text: rgba(255, 255, 255, 0.92)
--muted: rgba(255, 255, 255, 0.65)
--border: rgba(255, 255, 255, 0.12)
--accent: #7c5cff
--success: #10b981
--warning: #f59e0b
```

All pages use `backdrop-filter: blur(10px)` for glassmorphism panels and consistent `14px` border-radius.

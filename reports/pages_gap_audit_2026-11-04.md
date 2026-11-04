# GitHub repo vs GitHub Pages — what is missing from the published site (2026-11-04 14:14 UTC)

## Answer

`https://eltonaguiar.github.io/BESTIEJOB/` renders **392 job cards**. `jobs.json` on the same
site holds **1,291** jobs. **924 jobs exist in the repo and in the site's own `jobs.json` but appear on
no card at all** — they are unreachable from the page.

| Layer | Count |
|---|---:|
| Cards rendered on the live page | 392 |
| Links reachable (cards + 6 alternates each) | 443 |
| Rows in `README.md` on `origin/main` | 484 |
| Jobs in `jobs.json` on the live site | 1,291 |
| **Jobs in the repo but on no card** | **924** |

## Where they went

The page is built from `README.md` (`pages.yml` → `tools/build_site.py`), so any row that leaves
the README leaves the site. On 2026-11-04 the daily LinkedIn sweep committed `135ae75`
`chore(scan): daily LinkedIn sweep 2026-11-04 [skip ci]` which rewrote the board **+65 / −1,142
lines**. It invoked `tools/jobs_merge_inbox.py --max-per-table 150`, while every other scan job in
the same repo passes `--max-per-table 400`. The 150-row cap kept only the newest 150 rows per
family and dropped the rest from the README (they survive in `README.BAK_2026-11-04T113432Z.md`
and in `jobs.json`).

`build_site.py` then did exactly what it is told: `site: 392 jobs {'servicenow': 134,
'salesforce': 116, 'other': 142}` in the deploy log at 13:38 UTC.

## Breakdown of the missing postings

| Family | Missing |
|---|---:|
| Salesforce | 427 |
| ServiceNow | 355 |
| Other | 142 |
| **Total** | **924** |

- **901** were posted within 30 days; **602** within 7 days — these are current, not archive.
- By source: readme 300, adzuna 282, linkedin 100, workday 19, greenhouse 18, smartrecruiters 12.
- The 392 cards that do render are internally consistent (`check_site_links.py` passes), which is
  why this failed silently: nothing links to a row that was never written.

## Fix applied here (not pushed)

`.github/workflows/linkedin-sweep.yml`: `--max-per-table 150` → `400`, matching `hourly-scan.yml`
and `undated-recheck.yml`. Without this the next daily sweep truncates the board again.

## Still needed for full fidelity

1. Restore the dropped rows: re-merge from `README.BAK_2026-11-04T113432Z.md` (the pre-truncation
   board) or rebuild the tables from `jobs.json`, then let Pages redeploy.
2. Structural: a 400-row cap still cuts a family with 751 rows. `build_site.py` reads only
   `README.md`, so the README cap is the site's real ceiling. Either raise the cap, or have
   `build_site.py` render overflow from `jobs.json` so a display limit can never delete postings.
3. Note the local branch is **8 commits ahead of `origin/main`** (today's harvests) — those are
   not on the site either until pushed.

## Newest 25 missing postings (all 924 in `reports/pages_missing_jobs_2026-11-04.json`)

| Posted | Title | Company | Source |
|---|---|---|---|
| 2026-11-04 | Salesforce Functional Analyst | Manulife | adzuna |
| 2026-11-04 | ITAM PROJECT MANAGER - SERVICENOW HAM/SAM | Insight Global | adzuna |
| 2026-11-04 | Staff Site Reliability Engineer, Canada Protected B | ServiceNow | adzuna |
| 2026-11-04 | Senior ServiceNow Engineer | EQ Bank | linkedin |
| 2026-11-03 | Fullstack Technical Lead – Commercial Lending & Asset Financ | Astra North Infoteck Inc. | adzuna |
| 2026-11-03 | DevOps Engineer | TD Bank | adzuna |
| 2026-11-03 | ServiceNow Senior Developer at BDO Canada | BDO Canada | echojobs |
| 2026-11-03 | [Hiring] ServiceNow Developer @Veracity Ventures Inc. | Veracity Ventures Inc. | remotive |
| 2026-11-03 | [Hiring] ServiceNow Consultant / Developer @Artech | Artech | remotive |
| 2026-11-03 | [Hiring] ServiceNow Moveworks Developer & Architect @NewRock | NewRocket | remotive |
| 2026-11-03 | [Hiring] ServiceNow Developer @FX Innovation | FX Innovation | remotive |
| 2026-11-03 | [C] Salesforce Engineer / Developer | MLSE (Maple Leaf Sports &  | workday |
| 2026-11-03 | Senior Consultant- ServiceNow Developer | EY | trabajo |
| 2026-11-03 | SENIOR SYSTEMS INTEGRATOR TECHNOLOGY SERVICES (ServiceNow) | City of Toronto | tealhq |
| 2026-11-03 | Consultant, ServiceNow Developer in Toronto | ONjobcentre.ca | onjobcentre |
| 2026-11-03 | 339 Servicenow Jobs in Toronto | LinkedIn | linkedin |
| 2026-11-03 | RQ11686 - Software Developer - Senior I | Analyst Technical Solution | analystit |
| 2026-11-03 | Principal Solution Architect- ServiceNow | ServiceNow | builtin |
| 2026-11-03 | Senior Lead, ServiceNow ITOM | Take-Two Interactive Softw | builtin |
| 2026-11-03 | ServiceNow Technical Consultant/Developer for Finance & Supp | WeLanceALot.com | welancealot |
| 2026-11-03 | RQ00757 - Specialized IT Consultant - Intermediate | Source Code | careerbeacon |
| 2026-11-03 | Senior Project & Business Process Analyst - Digital PMO | University Health Network | tealhq |
| 2026-11-03 | Salesforce Developer (Marketing, Data, and Experience Clouds | Salytics | simplyhired |
| 2026-11-03 | Salesforce Technical Lead - Commerce Cloud | iHireTechnology | ihiretechnology |
| 2026-11-03 | Front-End Salesforce Commerce Cloud Developer | Global Technical Talent | trabajo |
# JOBLESSONS_2026-11-18T0400EST — hourly BESTIEJOB scan (Toronto SN/SF)

Run: 2026-11-18 04:00 EST (09:00Z), cron. Repo: eltonaguiar/BESTIEJOB @ main, commit fed4f8c [skip ci].

## Sources scanned this hour
- Adzuna Canada API, `what=ServiceNow` / `what=Salesforce`, `where=Toronto`, `max_days_old=3`, `sort_by=date`, `results_per_page=25` (demo keys; page 1 only — 45 SN / 111 SF total matches)
- LinkedIn guest search via browser DOM, `keywords=ServiceNow` / `keywords=Salesforce`, `location=Toronto`, `f_TPR=r86400` — 60 cards per query, URLs `li a[href*="/jobs/view/"]`
- Skipped / not viable this cycle: Workday CXS probes (CI hourly scan at :00Z 429s BMO/TD/Manulife/CIBC/Interac; covered by the 03:00 EST run at 09:14:28Z), Rogers careers (`jobs.rogers.com` under maintenance — check weekly), Bell (`jobs.bell.ca` zero reqs — check weekly), GC portals (Radware captcha; Job Bank full-text is noise, trust only platform-named titles)

## Dedupe against board (jobs.json 2574 rows, README tables)
- Inbox batch `hermes-cron--2026-11-18--v1.md` (40 rows, scanned 2026-11-18T05:02Z): 0 new — all 40 URLs already present in README.md and jobs.json (merged by the 02:00–03:00 EST scans). Re-check is idempotent; merger dedupes by normalized URL against README + APPLIED.md.
- Fresh hour candidates surfaced: 10 platform-relevant across Adzuna + LinkedIn; 9 already on board; 2 new-to-board, 1 verified + added, 1 excluded.

## Verified new jobs added (+1)
- Scotiabank — Senior Manager, Employee Technology — Toronto, Ontario — posted 2026-11-17 — ServiceNow (HR service delivery / HRSD technologies, Requisition 267899) — `adzuna.ca/details/5968725995`. Body-verified via the Adzuna detail page; added to jobs.json + README ServiceNow table; `public/` rebuilt via `tools/build_site.py`.
- jobs.json: 2574 → 2575 (primaryCounts servicenow 1143 → 1144). README ServiceNow heading 1158 → 1159, details 1130 → 1131; parse-vs-dated-cell gap preserved at 0.
- public/jobs-data.json: 5018 jobs; live at `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` (verified by curl after `pages.yml` deploy success).

## Excluded this hour
- S-M Software Solutions "RQ11878 – Software Developer – CRM – Senior" (Toronto, onsite, Ontario Ministry client): body is **Siebel** (Siebel Open UI, EIM/EAI), not Salesforce — excluded ("CRM" ≠ Salesforce; body-check required).
- Adzuna "Sr Solution Sales Executive CRM (CPQ)" at ServiceNow — sales role, excluded.
- LinkedIn "Lead Management Operations — Rogers Communications" — sales ops, not platform.
- Generic titles without platform in title or description (business analyst, IT support, sales/marketing, PMO, recruiting) — excluded per board remit.

## Patterns / lessons for future agents
1. Same LinkedIn title, different job id = different posting (IG Wealth "Manager, HR Technology & ServiceNow HRSD" appeared under ids …4491785075, …4491778246, …4491775339 for Ontario/Manitoba/Quebec) — dedupe on normalized URL + job id; keep location-distinct rows.
2. Adzuna recycles ids — API `created` date is unreliable; use the detail page's JSON-LD `datePosted`/`validThrough` (e.g. a Maarut row showed "Posted On 30/10/2026" though the API said 11-17).
3. "CRM" titles must be body-checked for Siebel before treating as Salesforce (S-M Software RQ11878 case). "ServiceNow" in body as mere tooling (e.g. ticketing-tool user) is not a platform role either — read `.jobs-description`, not sidebar keyword hits.
4. Rogers careers and jobs.bell.ca are not viable hourly sources this cycle (maintenance / zero reqs); GC portals are captcha-walled — Job Bank is the proxy, titles only.
5. Freshness layering: LinkedIn guest search (24h) + Adzuna `max_days_old=3` catch this-hour postings; Workday/ATS sweep carries employer-board depth but 429s at :00Z — space tenant probes ≥8 s, max 3–4 per run, retry at :05Z+.
6. Push races: remote main advanced mid-run (09:14:28Z scan commit). Rebase, let upstream win `jobs.json`/`public/*` (`git checkout --ours` during rebase), re-insert any row upstream lacks, re-run `tools/build_site.py`, amend, push. README/inbox kept from your commit.
7. `tools/sync_readme_to_jobs.mjs` is a no-op on the current README (one-line mangled tables) — write rows to jobs.json directly and/or insert README rows by hand, then rebuild; never rely on README→jobs propagation.

## Files changed
- jobs.json (+1 row; meta.total 2575, primaryCounts.servicenow 1144)
- README.md (+1 ServiceNow row; heading 1159 / details 1131)
- public/jobs-data.json, public/index.html (rebuilt via tools/build_site.py)
- inbox/hermes-cron--2026-11-18--v1.md (committed for provenance)
- JOBLESSONS_2026-11-18T0400EST.MD (this file)
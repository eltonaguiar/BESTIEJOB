# BESTIEJOB Hourly Scan — Job Search Lessons

**Date**: 2026-11-11
**Run time**: 2026-11-11 00:00 EST (05:00 UTC) — scheduled cron run
**Scope**: Fresh Toronto / GTA ServiceNow and Salesforce postings (Platform Admin / Platform Developer I / partner & employer focus)
**Repo**: github.com/eltonaguiar/BESTIEJOB (branch: main)
**Live board**: https://eltonaguiar.github.io/BESTIEJOB/

## Scan summary

| Metric | Value |
|---|---|
| Sources queried | LinkedIn guest search, BuiltIn, Indeed.ca, ServiceNow Careers, Salesforce Careers, Rogers (jobs.rogers.com), Bell (jobs.bce.ca / jobs.bell.ca), Government of Canada (jobs.gc.ca / canada.ca); Elite/Global Elite partners + banks: Accenture, Deloitte, KPMG, CGI, Scotiabank, RBC, TD, BMO, CIBC, Fujitsu, ivari, ZS, Caseware, Brookfield |
| Dedupe baseline (README.md tables + jobs.json on main) | README 5,415 live postings (ServiceNow 718 · Salesforce 879 · Other 3,818); jobs.json 5,083 rows; window 2026-10-10 → 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 9 |
| Jobs merged to README.md | 9 (ServiceNow +3, Salesforce +6) |
| Jobs merged to GitHub Pages (public/) | Rebuild triggered by README push via `.github/workflows/pages.yml` (build_site.py); public/ not committed by hand |

## Fresh 2026-11-11 Toronto SN/SF postings verified live and merged

**ServiceNow (+3)**

| Posted | Role | Company | Location | Source | Verified |
|---|---|---|---|---|---|
| 2026-11-11 | ServiceNow Sr. Project Manager | Fujitsu | Toronto, Ontario, Canada | LinkedIn | Live (browser, no removal/filled indicator) |
| 2026-11-11 | 2027 Graduate Program, Technology Services - Delivery, Excellence & Architecture | Bell | Toronto, ON | Indeed | Live (apply deadline 2026-11-16; entry-level/grad) |
| 2026-11-04 | ServiceNow Developer (Contract) | Brookfield Properties | Toronto, ON, Canada | BuiltIn | Live ("Posted 7 days ago") |

**Salesforce (+6)**

| Posted | Role | Company | Location | Source | Verified |
|---|---|---|---|---|---|
| 2026-11-11 | Salesforce Manager, Sales & Marketing Clouds | ivari Canada | Toronto, Ontario, Canada | LinkedIn | Live |
| 2026-11-11 | Salesforce Consultant | ZS | Toronto, Ontario, Canada | LinkedIn | Live |
| 2026-11-11 | Principal Technical Architect | Salesforce | Toronto, Ontario, Canada | LinkedIn | Live |
| 2026-11-08 | Lead Salesforce Developer | TD | Toronto, ON, Canada | BuiltIn | Live ("Posted 3 days ago") |
| 2026-11-05 | Salesforce Developer | Caseware | Toronto, ON, Canada | BuiltIn | Live ("Posted 6 days ago") |
| 2026-11-01 | Software Engineer II - Salesforce | TD | Toronto, ON, Canada | BuiltIn | Live ("Posted 10 days ago") |

All 9 were deduped against the board (jobs.json URL set + normalized company+title keys) and confirmed absent before merging. README.md counts bumped: ServiceNow 718→757→1057, Salesforce 879→1212, total 6,418→6,427; as-of date already 2026-11-11. Commit `fa52e79` pushed to main; the `README.md` push triggers `pages.yml`, which runs `tools/build_site.py` and redeploys GitHub Pages.

## Sources checked (partner / employer / Canadian tech focus)

**Partner / Elite / Global Elite partners + banks**
- Fujitsu — ServiceNow Sr. Project Manager (Toronto) — captured, merged.
- ZS — Salesforce Consultant (Toronto) — captured, merged.
- ivari Canada — Salesforce Manager, Sales & Marketing Clouds (Toronto) — captured, merged.
- TD — Lead Salesforce Developer + Software Engineer II - Salesforce (Toronto) — captured, merged (2).
- Caseware — Salesforce Developer (Toronto) — captured, merged.
- Brookfield Properties — ServiceNow Developer (Contract) (Toronto) — captured, merged.
- Accenture — ServiceNow roles present (HAM Consultant, Solution Architect) via careers/ATS; no fresh Toronto Platform Admin/Dev I this cycle.
- Deloitte / KPMG / CGI — existing vacancies already on board; no fresh dated Toronto SN/SF platform requisitions.
- Scotiabank / RBC / BMO / CIBC Workday boards — no new dated SN/SF requisitions.
- IBM / TCS / Capgemini — arrive via ATS sweep only; no fresh direct posting.

**Telcos**
- Rogers (jobs.rogers.com) — Technical Specialist mentions ServiceNow/Salesforce only as "preferred familiarity" (not a platform role); Lead Management Operations (Salesforce marketing ops) excluded by title rule. No fresh dated SN/SF platform posting.
- Bell (jobs.bce.ca / jobs.bell.ca) — ServiceNow System Administrator filled; Senior Manager ServiceNow Platform Delivery no longer accepting applicants; Senior Technical Advisor expired. Skip-on-sight holds for filled/expired.

**Government**
- Government of Canada (jobs.gc.ca / canada.ca) + Ontario gojobs.gov.on.ca — zero ServiceNow/Salesforce Toronto hits. GC platform work arrives via prime vendors on their own ATS (covered by the automated sweep).

**Aggregators / job boards**
- Indeed.ca / BuiltIn — source of the fresh BuiltIn postings above (posted 3–10 days ago, "Be an Early Applicant", no removal notice). Indeed SERP hits are intermediate/senior (2–5+ yrs, CSA/CAD mandatory), relative ages only, no verifiable `datePosted`; excluded unless an absolute posted date is confirmable.
- LinkedIn guest API — 429/403 or login wall; no LinkedIn-sourced role added without a verifiable absolute posted date. (The LinkedIn-sourced roles above were verified live via direct page load.)

**Excluded (title / level / freshness rules)**
- Sales / account-management / marketing-ops titles (e.g., "Partner Sales", "Sales Director - CRM Sales") — excluded by title rule.
- Senior advisory / staff / manager roles — excluded (target is Platform Admin / Platform Developer I / entry-level).
- Roles with relative ages ("New", "5d ago") and no verifiable absolute `datePosted` — excluded.
- Expired / filled / "no longer accepting applicants" postings — skip-on-sight; never re-probed as live.

## Patterns / lessons confirmed

1. **BuiltIn.ca is the most reliable fresh Toronto SN/SF source this cycle** — it surfaces explicit "Posted X days ago" + "Be an Early Applicant" and its detail pages load without a login wall, making posted dates verifiable. Prefer it for fresh platform roles.
2. **LinkedIn guest search is unreliable (429/403/login wall)** — never add a LinkedIn role without an independently verifiable absolute posted date; direct page loads can confirm liveness but not always the date.
3. **Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced** — remains the top priority keyword gap. The Bell 2027 Grad Program is the closest entry-level match (mentions Salesforce + ServiceNow CSM).
4. **Bell / Rogers / GC employer pages yield marketing-ops, infra-adjacent, or filled/expired postings** — the title rule plus skip-on-sight keeps the board clean; never re-probe filled/expired roles as live.
5. **Government of Canada platform work arrives via prime vendors on their own ATS** — direct jobs.gc.ca searches return zero Toronto SN/SF hits; rely on the automated ATS sweep for GC-adjacent platform roles.
6. **README.md is the source of truth for the live page** — `pages.yml` rebuilds `public/` from `README.md` via `build_site.py` on any README push, so committing README.md is sufficient to update GitHub Pages; `jobs.json`/`public/` need not be hand-edited.
7. **Dedupe must use normalized URL + company+title keys** — several "fresh" SERP hits were already on board under a different URL/title variant; company+title dedupe caught them.
8. **Null runs are the expected norm** — most cycles surface zero verified-fresh Platform Admin/Dev I Toronto roles; a merge cycle (like this one) is the exception.

## Files touched
- `JOBLESSONS_2026-11-11.MD` — this file (repo root, main).
- `README.md` — +9 verified fresh Toronto SN/SF rows (ServiceNow 718→757→1057, Salesforce 879→1212, total 6,418→6,427); commit `fa52e79` pushed to main; triggers `pages.yml` GitHub Pages redeploy.

## 01:00 hourly scan (this cycle) — null run

**Date**: 2026-11-11 · **Run time**: 2026-11-11 01:00 EST (06:00 UTC) · **Branch**: main (current with `fa52e79`)

**Result**: No new verified-fresh Toronto ServiceNow/Salesforce Platform Admin / Platform Developer I / entry-level roles to merge.

**What was checked**
- Web search: ServiceNow + Salesforce Toronto postings (Nov 9–11); every surfaced role already on board under its URL or normalized company+title key (BDO, Cprime, Altus Group, Robert Half, Scotiabank, CGI, Lightspeed, KPMG, McKesson, Lyft, etc.).
- jobs.json dedupe (5,330 rows): all 29 Toronto/Ontario/Ottawa SN/SF postings from the last 48h already on the board; all intermediate/senior/architect level, none entry-level Platform Admin/Dev I.
- Individual liveness verification: Scotiabank ServiceNow Developer req 260518 returns "not accepting any further applicants" — closed, skip-on-sight; excluded. Robert Half Salesforce Developer (Toronto, 2026-11-10) is intermediate Apex/LWC work and already on board (2026-10-27 entry) — excluded by level rule.
- Partner / telco / government pages (Rogers jobs.rogers.com, Bell jobs.bce.ca, jobs.gc.ca, gojobs.gov.on.ca): no fresh dated Toronto SN/SF platform requisitions.

**Merged**: 0 jobs to README.md; 0 to GitHub Pages (README unchanged, so no pages.yml rebuild triggered this cycle).

**Lesson confirmed**: null runs are the expected norm — most hourly cycles surface zero verified-fresh Platform Admin/Dev I Toronto roles. The 00:00 scan's 9-merge cycle (commit `fa52e79`) remains the latest board update; board and GitHub Pages are current as of 2026-11-11.

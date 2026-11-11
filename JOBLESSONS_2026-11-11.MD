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

## 02:00 hourly scan (this cycle) — null run

**Date**: 2026-11-11 · **Run time**: 2026-11-11 02:00 EST (07:00 UTC) · **Branch**: main (current with `2584143`)

**Result**: No new verified-fresh Toronto ServiceNow/Salesforce Platform Admin / Platform Developer I / entry-level roles to merge.

**Dedupe baseline**: README.md tables + jobs.json (5,341 rows), window 2026-10-12 → 2026-11-11 · **6,427 live postings** (ServiceNow 1,056 · Salesforce 1,212 · Other 4,159) · as of 2026-11-11.

**Sources checked**

**Partner / Elite / Global Elite partners + banks**
- ServiceNow careers (careers.servicenow.com) — Staff SRE Canada Protected B (Nov 05), Staff Systems Engineer (Nov 06), Staff Security Engineer (Nov 06): staff-level infra/security, already on board; Sales Director - CRM Sales (Nov 09) and Sr. CRM Account Executive (Nov 09): sales, excluded by title rule. No fresh Platform Admin/Developer I.
- Salesforce careers (careers.salesforce.com) — Manager Sales Development, Senior Manager Sales, Principal Account SE, Renewals Manager, Treasury/Credit & Collections/Recruiting Coordinator: non-platform; no Platform Admin / Platform Developer I.
- Accenture / Deloitte / KPMG / CGI / Fujitsu / IBM / TCS / Capgemini / Wipro / Ateko (backed by Bell) — vacancies already on board; no fresh dated Toronto SN/SF platform requisitions this cycle.
- Scotiabank / RBC / TD / BMO / CIBC Workday boards — no new dated SN/SF requisitions.

**Telcos**
- Rogers (jobs.rogers.com) — Platform Specialist (VMware/NetApp infra), Technical Specialist (Meraki networking; SN/SF only as "familiarity"), Lead Management Operations (Ottawa marketing ops), Delivery Specialist, Digital Campaigns manager, Damage Prevention, sales roles: no SN/SF platform role; SN/SF appear only as familiarity or non-platform duties. Excluded by title rule.
- Bell (jobs.bce.ca / jobs.bell.ca) — ServiceNow Senior Technical Advisor (Oct 06, deadline 11/02/2026 expired), ServiceNow System Administrator (filled), Senior Manager ServiceNow Platform Delivery (filled/no longer accepting), Technical Architect II (deadline 03/08/2026 expired), Senior Software Architect II - ServiceNow Platform Architect (deadline 04/02/2026 expired). Skip-on-sight holds; no fresh dated Toronto SN/SF platform requisition.

**Government**
- Government of Canada (jobs.gc.ca) — zero Toronto SN/SF hits. Ontario gojobs.gov.on.ca — expired/old postings only (2022, Oct-2026 customer service). GC platform work arrives via prime vendors on their own ATS (covered by the automated sweep); nothing fresh this cycle.

**Aggregators / job boards**
- gap_scan 2026-11-10 (Adzuna 68 calls, Job Bank 12 pages, Eluta 16 pages) — 44 SN/SF-named rows: staff/architect/senior or Ottawa / Montréal / Canada-wide. Toronto hits (ServiceNow Staff Systems Engineer smartrecruiters; Smart IT Frame Salesforce Data Cloud Architect adzuna 5959388441; S I Systems Senior Salesforce Solution Architect adzuna 5959388506; Traction Rec Salesforce Implementation Specialist adzuna 5960420667) already on board under the same URL — deduped, not re-added.
- Indeed.ca / BuiltIn.ca — intermediate/senior+ only (KPMG, CGI, Deloitte, BDO, BMO, Accenture, ServiceNow staff roles, Loopio, Moneris, TD, Sheridan); SERP shows relative ages only ("New", page dated 10 November 2026), no verifiable absolute `datePosted` → excluded unless a detail page confirms one.
- LinkedIn guest — 429/403/login wall; no LinkedIn role added without an independently verifiable absolute posted date.

**Excluded (title / level / freshness rules)**
- Sales / account-management / marketing-ops titles; senior advisory / staff / manager / director roles (target is Platform Admin / Platform Developer I / entry-level).
- Roles with relative ages and no verifiable absolute `datePosted`.
- Expired / filled / "no longer accepting applicants" postings — skip-on-sight, never re-probed as live.

**inbox triage (untracked, not submissions)**
- fresh-ca--2026-11-11--v3.md: empty table (+0 new, 0 duplicate) — Adzuna/Job Bank/Eluta sweep found nothing dated 2026-11-10/11.
- todayfeeds--2026-11-10--v1.md: Salesforce Technical Architect Director - PubSec (Mulesoft) via Workday — undated, director-level, excluded.
- _ai-triage--2026-11-10--v1.md: lanefour.com Salesforce Consultant/Administrator — undated rows, merger skips on purpose.

**Merged**: 0 jobs to README.md; 0 to GitHub Pages (README unchanged → no pages.yml rebuild required; `public/` and jobs.json already redeployed from commit `2584143`, 2026-11-11T06:49Z).

**Lesson confirmed**: null runs are the expected norm — third consecutive hourly cycle this date (00:00 merged 9; 01:00 null; 02:00 null) with zero verified-fresh Platform Admin/Platform Developer I Toronto entries beyond the :00 deep sweep. Fresh Toronto platform roles surface at the :00 scan; treat :01/:02 hourly scans as change-detection only. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced this cycle — remains the top keyword gap.

## 05:00 hourly scan (this cycle) — null run

**Date**: 2026-11-11 · **Run time**: 2026-11-11 05:00 EST (10:00 UTC) · **Branch**: main (current with the latest hourly scan)

**Result**: No new verified-fresh Toronto ServiceNow/Salesforce Platform Admin / Platform Developer I / entry-level roles to merge.

**What was checked**
- Web search: ServiceNow + Salesforce Toronto postings (Nov 9–11); every surfaced role already on board under its URL or normalized company+title key, or filled/expired/intermediate-level (SS&C, Scotiabank req 261367, Scotiabank req 260518 closed).
- jobs.json + README dedupe: all Toronto/Ontario SN/SF postings from the last 48h already on the board; none entry-level Platform Admin/Dev I.
- Individual liveness verification: Bell ServiceNow Developer/Integrator Job 431695 returns "the job you are trying to apply for has been filled" — closed, skip-on-sight. Robinhood "Applications Developer, ServiceNow" (BuiltIn SERP "Posted Yesterday") detail page shows "removed at 10:10 p.m. UTC on Wednesday, Nov 12, 2025" — stale SERP, dead. Rewind "Salesforce Administrator - Toronto (hybrid work)" returns 404 — dead.
- Partner / telco / government pages (Rogers jobs.rogers.com, Bell jobs.bce.ca, Scotiabank jobs.scotiabank.com, BMO jobs.bmo.com, RBC jobs.rbc.com, Government of Canada jobs.gc.ca): no fresh dated Toronto SN/SF platform requisitions; Bell/Rogers SN/SF appear only as filled, expired, marketing-ops, or "familiarity" duties.
- BuiltIn.ca freshness probe — Robinhood and Rewind postings dead on detail page; SERP "Posted X days ago" relative ages not trusted without detail-page confirmation.

**Merged**: 0 jobs to README.md; 0 to GitHub Pages (README unchanged → no pages.yml rebuild required).

**Lesson confirmed**: null runs are the expected norm — fourth consecutive hourly cycle this date with zero verified-fresh Platform Admin/Platform Developer I Toronto entries. BuiltIn SERP "Posted X days ago" is unreliable until the detail page is loaded (stale indexes and removed markers common); always confirm liveness + absolute posted date on the detail page before adding. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced — remains the top keyword gap.

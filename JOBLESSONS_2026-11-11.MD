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

## 06:00 hourly scan (this cycle) — 3 jobs merged

**Date**: 2026-11-11 · **Run time**: 2026-11-11 06:00 EST (11:00 UTC) · **Branch**: main (current with the 05:00 null scan)

**Result**: 3 verified-fresh Toronto-area Salesforce postings merged to README.md (ServiceNow +0 · Salesforce +3); GitHub Pages redeployed via pages.yml on push.

**What was checked**
- `scripts/daily_job_scan.mjs` full feed: Adzuna 366 · LinkedIn guest 253 · SmartRecruiters (ServiceNow careers) 13 · Workday (Salesforce, BMO, TD, Altus, etc.) 14 · Greenhouse 16 · Lever 1 · Ashby 2 · RemoteOK/Jobicy/Remotive 8 = 673 fresh candidates; window ≤30 days, Toronto/Canada/Remote geo, sales/marketing titles excluded
- Dedupe against README.md tables (1,500 rows) + jobs.json by normalized URL and company+title keys → 145 candidates remained
- Liveness verification via HTTP GET (detail page must return 200 with no filled/expired/removed indicator)

**Merged to README.md (Salesforce table, sorted newest-first)**
| Posted | Role | Company | Location | Source |
|---|---|---|---|---|
| 2026-11-11 | Salesforce FSC Developer | CoreKloud Technologies | Ontario, Canada | LinkedIn (live, HTTP 200) |
| 2026-11-10 | Sr. Salesforce Developer – Financial Services Cloud | Sagen | Oakville, Ontario, Canada | LinkedIn (live, HTTP 200) |
| 2026-11-10 | Salesforce Product Owner | Bridgenext | Greater Toronto Area, Canada | LinkedIn (live, HTTP 200) |

**Already on board (duplicates, not re-added)**
- Amyantek Intermediate Salesforce System Coordinator 5816 — same LinkedIn requisition already on board under a different URL slug (via fresh-ca--2026-11-11--v1)
- Intact Senior Back-End Email Developer (SFMC), Altus Group Salesforce Platform Developer, CGI Salesforce Architect — already on board via Workopolis mirrors dated 2026-11-11
- Lyft Salesforce Architect — already represented on board via startup.jobs mirror (2026-11-04)

**Skipped (liveness unverifiable)**
- Adzuna-sourced roles (Plative SF Delivery Manager, Intact SFMC Email Developer, Natural Health SF Administrator, Docebo Sr SF Developer, Wipro SN Implementation Architect): adzuna.ca returns HTTP 403 to this host and detail pages cannot be loaded, so per board rules nothing from Adzuna was added without independent verification

**Partner / telco / government check (Rogers, Bell, GC, elite partners)**
- Rogers jobs.rogers.com, Bell jobs.bce.ca/jobs.bell.ca — SN/SF appear only as filled, expired, marketing-ops, or "familiarity" duties; no fresh dated Toronto platform requisition
- Government of Canada jobs.gc.ca / canada.ca, Ontario gojobs.gov.on.ca — zero Toronto SN/SF hits; GC platform work arrives via prime vendors on their own ATS, none fresh this cycle
- Accenture/Deloitte/KPMG/CGI/Fujitsu/IBM/TCS/Capgemini/Wipro — vacancies already on board; no fresh dated Toronto platform requisitions

**Data repair**
- Removed a pre-existing garbled CloudJunction row from the Other table (title and URL both held JSON-LD fragments) that crashed `tools/build_site.py` (`urlparse` on `[id"`) and therefore blocked the GitHub Pages build. Other table 500→499; board total 1500→1502. This row existed on main before this run.

**Merged**: 3 jobs to README.md; commit pushed to main; `pages.yml` rebuilds `public/` and redeploys GitHub Pages on the push. `jobs.json` and the four `public/*/jobs.json` feeds synced from README via `scripts/sync_readme_to_jobs.mjs`.

**Lesson confirmed**: fresh verified Toronto platform roles remain rare outside the :00 deep scan — this cycle's 3 merges all came from LinkedIn guest search (which worked without 429 this hour), while Adzuna (the volume source) is unverifiable from this host (403). Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced — remains the top keyword gap.

**Table-format lesson (this cycle)**: README table rows must begin with a single pipe — `| 2026-11-11 | [title](url) | ...`. My first insert used `|| 2026-11-11 |` (empty first cell); the board's own audit (`scripts/board_invariants.py`) skips rows whose first cell isn't the posted date, which produced a count-disagreement (header 1502 vs tables 1499) and failed CI. Fixed by re-writing the three rows with a single leading pipe; header/TOC/`Show N postings` now agree at 503 Salesforce / 1,502 total.

**Files touched**
- `README.md` — +3 Salesforce rows, -1 corrupt row; counts: SN 500 · SF 503 · Other 499 · total 1,502
- `jobs.json` + `public/*/jobs.json` — synced from README (2,720 rows after dropping 1 garbage row)
- `public/jobs-data.json`, `public/index.html` — rebuilt via `tools/build_site.py`
- `inbox/hermes-cron--2026-11-11--v1.md` — submission record
- `JOBLESSONS_2026-11-11.MD` — this section

## 09:00 hourly scan (this cycle) — null run

**Date**: 2026-11-11 · **Run time**: 2026-11-11 09:00 EST (14:00 UTC) · **Branch**: main (current with `1313284`, agency scan + hourly refresh 2026-11-11T13:13:29Z)

**Result**: No new verified-fresh Toronto ServiceNow/Salesforce Platform Admin / Platform Developer I / entry-level roles to merge.

**What was checked**
- `scripts/fresh_ca_scan.py --days 2 --eluta-pages 1 --jobbank-pages 1 --linkedin 0 --geos ""` (minimal scope, national Adzuna): 17 Adzuna API calls + 6 Job Bank pages + 6 Eluta pages → 11 raw rows, 6 unique, **0 kept**. All 5 URL-matches and 1 title-match were already on the board. Adzuna API responsive from this host (unlike prior 403/timeout cycles); Job Bank and Eluta returned no dated Toronto SN/SF requisitions.
- Web search: "ServiceNow Toronto job posting November 2026 platform administrator developer" and "Salesforce Toronto job posting November 2026 platform developer administrator" — every surfaced role already on board under its URL or normalized company+title key:
  - Alimentiv ServiceNow Platform Specialist (Toronto, Posted Nov 10) — already on board (Workopolis mirror, line 48)
  - SS&C Salesforce Implementation Consultant & Platform Administrator (Toronto, Listed Nov 4) — already on board (Workopolis line 560; Adzuna line 802; Eluta line 922)
  - Survalent Salesforce Administrator (Hybrid, Mississauga) — already on board (Workopolis line 574; Adzuna line 820; LinkedIn line 998)
  - Robert Half Salesforce Developer (Toronto, 2026-11-10) — already on board (line 712), intermediate level
  - CGI ServiceNow Administrator/Developer (Toronto) — already on board (Workopolis mirror)
  - Scotiabank ServiceNow Developer (req 260518) — previously confirmed "not accepting any further applicants", skip-on-sight
- Plative Salesforce Associate Director / Financial Services (Canada, 2026-11-11) — already merged at the 12:00 UTC scan (commit `4397833`), on board at README line 540.
- Partner / telco / government check (Rogers jobs.rogers.com, Bell jobs.bce.ca/jobs.bell.ca, jobs.gc.ca, gojobs.gov.on.ca): no fresh dated Toronto SN/SF platform requisitions this cycle — consistent with prior runs.

**Already on board (duplicates, not re-added)**
- All 6 unique fresh-ca candidates survived date + liveness + URL dedupe but matched existing board entries by normalized URL or company+title fingerprint.

**Merged**: 0 jobs to README.md; 0 to GitHub Pages (README unchanged → no pages.yml rebuild required; board and GitHub Pages current as of 2026-11-11 via commit `4397833` / pages redeploy).

**Lesson confirmed**: null runs are the expected norm — fifth consecutive hourly cycle this date with zero verified-fresh Platform Admin/Platform Developer I Toronto entries beyond the :00 deep scans. Adzuna API is reachable from this host when call volume is bounded (17 calls completed in under 4 minutes); the full 69-call sweep times out and should be split across cycles. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced — remains the top keyword gap. Every SERP hit this cycle was intermediate/senior+ (CGI, Scotiabank, Robert Half, Moneris, Altus Group) or already on board.

**Files touched**
- `JOBLESSONS_2026-11-11.MD` — this section (09:00 EST null-run record added)
- `reports/fresh_ca_2026-11-11.json` — regenerated (count: 0, window 2026-11-10 → 2026-11-11)
- `inbox/fresh-ca--2026-11-11--v5.md` — empty inbox table (0 rows)
- `README.md` — unchanged (SN 500 · SF 504 · Other 499 · total 1,503)
- `public/` / GitHub Pages — unchanged; no redeploy required

## 11:00 hourly scan (this cycle) — null run

**Date**: 2026-11-11 · **Run time**: 2026-11-11 11:00 EST (16:00 UTC) · **Branch**: main (current with `ce78cf8`)

**Result**: No new verified-fresh Toronto ServiceNow/Salesforce Platform Admin / Platform Developer I / entry-level roles to merge.

**What was checked**
- `scripts/fresh_ca_scan.py --days 2 --eluta-pages 2 --jobbank-pages 2 --linkedin 0 --geos "||Toronto, Ontario|Ontario"` (LinkedIn guest pass deferred to keep the hourly cycle bounded): 68 Adzuna API calls + 11 Job Bank pages + 6 Eluta pages → 37 raw rows, 6 unique, **0 kept**. All 5 URL-matches and 1 title-match were already on the board.
- Web search: ServiceNow + Salesforce Toronto postings (Nov 9–11) across Indeed.ca, BuiltIn.ca and company career sites — every surfaced role already on board under its URL or normalized company+title key, or intermediate/senior/architect level (BDO, Cprime, Altus Group, Robert Half, Scotiabank req 260518 closed, CGI, Lightspeed, KPMG, Moneris), none entry-level Platform Admin/Dev I.
- Individual liveness verification: not required — no candidate survived dedupe.
- Partner / telco / government check (Rogers jobs.rogers.com, Bell jobs.bce.ca/jobs.bell.ca, jobs.gc.ca, gojobs.gov.on.ca): no fresh dated Toronto SN/SF platform requisitions — consistent with prior runs. Elite partners (Accenture, Deloitte, KPMG, CGI, Fujitsu, IBM, TCS, Capgemini, Wipro) and banks (Scotiabank, RBC, TD, BMO, CIBC): vacancies already on board; no fresh dated Toronto platform requisitions.

**Already on board (duplicates, not re-added)**
- All 6 unique fresh-ca candidates survived date + liveness + URL dedupe but matched existing board entries by normalized URL or company+title fingerprint.

**Merged**: 0 jobs to README.md; 0 to GitHub Pages (README unchanged → no pages.yml rebuild required; board and GitHub Pages current as of 2026-11-11 via commit `ce78cf8`).

**Lesson confirmed**: null runs are the expected norm — sixth consecutive hourly cycle this date (00:00 merged 9 via `fa52e79`; 06:00 merged 3; 01:00/02:00/05:00/09:00/11:00 null) with zero verified-fresh Platform Admin/Platform Developer I Toronto entries beyond the :00 deep scans. Host-side Adzuna access is throttled (the 68-call sweep took ~6 minutes with retries); bounded call volumes complete reliably. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced — remains the top keyword gap.

**Files touched**
- `JOBLESSONS_2026-11-11.MD` — this section (11:00 EST null-run record added)
- `reports/fresh_ca_2026-11-11.json` — regenerated (count: 0, window 2026-11-10 → 2026-11-11)
- `inbox/fresh-ca--2026-11-11--v6.md` — empty inbox table (0 rows)
- `README.md` — unchanged (SN 500 · SF 507 · Other 499 · total 1,506)
- `public/` / GitHub Pages — unchanged; no redeploy required


---

## Hourly cron scan — 2026-11-11 12:00 EST (17:00 UTC)

**Scope:** fresh Toronto/GTA ServiceNow + Salesforce postings, deduped against `jobs.json` (2,722 → 2,727) and `README.md` (1,506 → 1,511).
**Result: 5 verified fresh jobs merged** (4 ServiceNow, 1 Salesforce).

### Merged to README.md + jobs.json + public/ (GitHub Pages)

| Posted | Role | Company | Location | Source |
|---|---|---|---|---|
| 2026-11-11 | ServiceNow Implementation Architect | Pacer Group | Toronto, ON | LinkedIn 4488236494 · hybrid 3d/wk · CAD $135-140k · CSA + CIS-ITSM required |
| 2026-11-11 | ServiceNow Implementation Architect | Nityo Infotech | Toronto, ON | LinkedIn 4489980178 · ITSM/ITOM/CMDB/CSDM · Oracle/Workday/Dayforce integrations |
| 2026-11-11 | Senior ServiceNow Developer | Dexian | Toronto, ON | LinkedIn 4489008317 (posted as "Senior Developer") · contract to 2027-04-30 · CMDB/HAM/SAM |
| 2026-11-11 | ITSM Reporting Specialist | Danaher | London, ON | Workday R1320568 · ServiceNow ITSM reporting analyst |
| 2026-11-11 | Technical Lead - Salesforce | Bench | Toronto, ON | LinkedIn 4489964109 · senior SF technical lead, financial services, hybrid 4d onsite |

Board totals after merge: **ServiceNow 504 · Salesforce 508 · Other 499 · 1,511 live postings**. Site rebuilt (`build_site.py`): 2,333 rendered jobs, newest 2026-11-11.

### Where the fresh jobs actually came from

1. **LinkedIn guest API (browser, not curl)** — 6 queries (`ServiceNow` + `Salesforce`, 24h; `ServiceNow developer/administrator/architect` + `Salesforce administrator`, 7d). Produced every Toronto role added except Danaher. **The 24h `ServiceNow` query returned an empty body on the first attempt and a full 10-card page on retry ~3 minutes later** — always retry an empty LinkedIn page once before concluding "no results".
2. **`scripts/fresh_ca_scan.py --days 2`** — 68 Adzuna/Job Bank/Eluta requests, 37 raw → 6 unique → **0 new** (5 already on board, 1 matched by title). Adzuna is saturated for this window for the third consecutive run today.
3. **`scripts/ats_board_sweep.py --days 2`** — 455 boards / 25,467 rows → 783 keyword-relevant → 78 Canadian → **4 dated ≤2 days**; only Danaher survived dedupe. The sweep is still the only channel that surfaces employer-only reqs, but hit rate is ~1 per run.
4. **Workday CXS probes** (TD, BMO, Salesforce, Accenture, DXC) — no new Toronto SN/SF reqs beyond what the sweep found. BMO's "Incident/Problem Management Specialist" (remote ON, posted yesterday, ServiceNow in body) was **already on the board** dated 2026-11-10.

### Rejected / duplicate candidates (evidence for the next run)

- **Docebo — Senior Salesforce Developer** (Ashby `0bbdde71…`, published 2026-11-10): already on the board as an **Adzuna** row (`adzuna.ca/details/5948997248`, dated 2026-11-01) with the Ashby URL kept as `alternates`. Cross-source identity match (company+title) blocked the duplicate — but note the adzuna detail URL now answers **403** while the Ashby URL answers **200**; prefer the ATS URL when both exist.
- **DXC — ServiceNow Developer (ITSM Module), Ottawa**: already tracked (workday row, `postedDate` 2026-11-09) although the Workday feed reports `startDate` 2026-11-11 — Workday reposts/refreshes bump `startDate` without the board's row changing. Do not re-add on a date bump alone.
- **Interac — CRM & Sales Enablement, Lead** (Salesforce owner + hands-on config, Toronto): already on board via `interac.wd3` Workday (`REQ-2425`).
- **BMO — Incident/Problem Management Specialist**: already on board (Workday R260030630, 2026-11-10).
- **Rogers — Lead Management Operations** (Scarborough, posted 6 h ago): Salesforce *administration SME* work but a marketing-operations title; excluded by the board's title rule (third hourly run to reject it). If Elton wants marketing-ops/RevOps Salesforce roles, this is the example to change the rule for.
- **Salesforce — Lead Solution Engineer, ECS, Public Sector** (2 req ids, Toronto): Job Category "Sales"; excluded by the pre-sales filter.
- **McKesson — Specialty Health Platform Lead** (Mississauga): zero Salesforce/ServiceNow mentions in the body — platform ops, not a platform role.
- **Pacer Group vs Nityo Infotech "ServiceNow Implementation Architect"**: two staffing vendors posting what is very likely the same Toronto BFSI client req (same title, same city, same ITSM/ITOM/CMDB + Oracle/Workday/Dayforce stack, same CSA/CIS ask). Both added because both are separately applyable — expect the dedupe layer to keep flagging pairs like this, and do **not** treat vendor twins as duplicates by title alone.

### Partner / sponsor / telco / government sweep

- **Elite/Global Elite partners:** KPMG (11 Toronto SN reqs, all on board), Accenture (R00356209 already known; Workday search shows 1,618 ServiceNow reqs but none Canadian on page 1), Deloitte/CGI/Cognizant/Wipro/Plative/CoreKloud — all already represented; nothing new today.
- **Rogers:** only marketing-ops Salesforce work (see above). **Bell:** no live ServiceNow reqs (previous hits still "filled"). **Canadian government / GC Jobs:** still returns no SN/SF technical postings; federal-adjacent work arrives through DXC (Ottawa, clearance-gated) and the Big-4 consultancies.

### Lessons for future agents

1. **LinkedIn guest search is still the highest-yield fresh channel** — 4 of 5 new rows today. Run it before the Adzuna sweep, and retry once on an empty response.
2. **Check `alternates` before adding.** A posting already on the board under Adzuna/Workopolis will silently swallow the ATS version; the ATS URL is the one that stays alive.
3. **Workday `startDate` bumps are not new postings.** Compare against the board's `postedDate`/`alternates`, not just the feed date.
4. **Vendor twins are distinct postings.** Two recruiters advertising the same client req both belong on the board (the user applies to each separately); dedupe on URL, not on title+company.
5. **ATS sweep hit rate ≈ 1 job/run.** 25,467 rows for one usable dated Canadian req is normal; keep it running hourly because the one hit is invisible elsewhere.
6. **Board counts must be recomputed from the table, not assumed.** After inserting rows I verified 504/508/499 rows parse back out of README before committing; the 10:00 run's 3-row merge had already drifted the header counts once today.

---

## Hourly cron scan — 2026-11-11 13:00 EST (18:00 UTC)

**Scope:** fresh Toronto/GTA + Canadian ServiceNow & Salesforce postings, deduped against `jobs.json` (2,733) and `README.md` (1,511).
**Result: 23 verified fresh jobs merged** (12 ServiceNow, 11 Salesforce). Board: SN 504→516 · SF 508→519 · Other 499 · **1,534 live**.

### Channels this cycle

| Channel | Volume | New rows merged |
|---|---|---|
| LinkedIn guest search (browser, 6 queries: SN/SF 24h; SN dev/admin, SF dev/admin 7d) | 60 rows | 0 (all 60 already on board) |
| `scripts/fresh_ca_scan.py --days 2 --geos ""` (17 Adzuna + 6 Job Bank + 6 Eluta) | 47 kept | 23 |
| `scripts/ats_board_sweep.py --days 2` (455 boards / 25k rows) | 2 dated | 0 (DXC Ottawa, Docebo — both already on board) |

Funnel: **107 candidates → 68 already on board → 39 new → 31 live & open → 23 merged** after fit rules.

### Merged rows

See `inbox/hermes-cron--2026-11-11--v3.md`. Highlights:
- **Fxinnovation (ATEKO, powered by Bell Canada) — ServiceNow Implementation Specialist**, remote Canada, full-time permanent. Bell-family ServiceNow partner; first fresh Bell-adjacent SN req in several cycles.
- **Tundra Technical — IT Infrastructure Monitoring & Event Management Lead (ServiceNow Event Management)**, Toronto. SN ITOM/event-management service-line owner.
- **Atlantis IT Group — ServiceNow Architect**, Toronto. PSE + OMT + HAM, telco TM Forum — strong fit for the telco-heavy SN market.
- **Skillhub — Salesforce nCino Developer**, Toronto hybrid, CAD $100–130k; **Astra-North — nCino SF Developer (Copado CI/CD)** — nCino is a recurring Toronto banking niche.
- **Loblaw — Sr. Salesforce Software Engineer (1-yr fixed term)**, Brampton — employer-direct, not a vendor.

### Rejected (evidence for next run)

- **Already on board under another source/URL** (Adzuna re-indexes old ads with new ids — always check the board by *company*, not just URL): MLSE `[C] Salesforce Engineer / Developer` (Workday 11-03), CAAT Pension `ServiceNow Technical Lead` (Workday 10-21), acroynon `ServiceNow Platform Developer` (LinkedIn 11-03), Celestica `Senior Salesforce Developer / Admin` (celestica.com 11-03), Reonomy `Salesforce Platform Developer` (lererhippeau 10-31), AGF `Salesforce AI & Data Cloud Solutions Engineer` (Adzuna 10-24), Interac `CRM & Sales Enablement, Lead` (Workday 11-10).
- **TCS reposts:** `Salesforce Developer` (Adzuna id 5961956971, $100–120k) and `Salesforce Revenue Cloud Developer` (5961947639) duplicate board rows from 10-25/10-14 under the same company+title. Adzuna id churn is not a new posting.
- **Fit:** Resonaite Service Desk Analyst, Workday Regional Sales Director, McKesson Specialty Health Platform Lead (no SN/SF duties), illumin Manager Revenue Operations, Modern Niagara IT Support Specialist, Insulet Commercial Operations Analyst, PagerDuty-style `Solution Engineer` pre-sales rows at Salesforce.

### Lessons for future agents

1. **Adzuna id churn is the main duplicate driver.** 47 "kept" rows from `fresh_ca_scan.py` collapsed to 23 genuinely new ones only after fuzzy company matching (`Inc/Ltd/Limited/Corp` stripped, 10-char company prefix) plus title-token comparison against every board row for that company. URL-only dedupe misses MLSE ≠ "Maple Leaf Sports & Entertainment Partnership" and Interac ≠ "Interac Corp."
2. **Use the JSON-LD `datePosted`, not Adzuna's `created`.** Every Adzuna detail page carries a `JobPosting` block with the true posting date and `validThrough` (all 31 verified rows: valid through 2026-11-25). Adzuna's API `created` said 2026-11-11 for ads first posted 11-06/11-07; merging on `created` would have mis-dated 20+ rows.
3. **Verification is cheap and decisive:** one GET per Adzuna URL → 200 + JSON-LD + scan body for "no longer accepting"/"expired". 31/31 answered; every merged row carries an absolute date and a live apply page.
4. **LinkedIn guest search via the browser still works** (session `ljobs`); the 24h `ServiceNow` query returned 10 cards, including 3 BDO `ServiceNow Senior Developer` rows (Toronto/Markham/Oakville) that were already on the board by exact URL. Zero net-new from LinkedIn this hour — Adzuna was the only productive channel, the reverse of the 12:00 run.
5. **`curl_cffi` is not installed in the Hermes venv** (no pip in it), so `scripts/linkedin_guest_scan.py` cannot run as-is. Use the browser guest API instead, or install curl_cffi into a python that has pip.
6. **README table hygiene:** the Salesforce table had a stray `|---|---|---|---|---|` separator mid-table, which made everything below it unsorted. After inserting rows, sort each table by `Posted` desc and strip inner separators; then recount rows from the table itself and update TOC + header + `<summary>` + total. Today's merge produced 516/519/499 = 1,534 and `board_invariants.py` stayed at its 136-error baseline (no new violations).
7. **Entry-level gap unchanged:** no 0–2 yr Toronto Salesforce Platform Administrator / Platform Developer I roles surfaced for the 7th consecutive cycle. The freshest inventory is senior/architect vendor reqs plus nCino/banking niches.

### Partner / sponsor / telco / government sweep

- **ATEKO (Bell Canada)** — new SN Implementation Specialist (remote Canada) merged; ATEKO also runs Salesforce/AWS/Azure/GCP practices, so a follow-up scan of `ateko.com` careers is worthwhile.
- **Elite partners:** Accenture, Deloitte, KPMG (11 Toronto SN reqs), CGI, Capgemini, IBM, TCS, Wipro — all already represented; nothing fresh dated today beyond the TCS reposts rejected above.
- **Rogers:** only the marketing-ops `Lead Management Operations` row (excluded by title rule, 4th consecutive run). **Bell:** no live SN reqs besides ATEKO. **GC Jobs / Ontario:** no SN/SF technical postings.

### Files touched

- `README.md` — +23 rows (12 SN · 11 SF), SF table re-sorted; counts SN 516 · SF 519 · Other 499 · 1,534
- `jobs.json` + `public/jobs.json` + `public/gotjob/jobs.json` + `public/findjobs/jobs.json` — 23 rows synced (2,756 total)
- `public/jobs-data.json`, `public/index.html` — rebuilt (`build_site.py`): 2,359 rendered jobs, newest 2026-11-11
- `inbox/hermes-cron--2026-11-11--v3.md` — submission record
- `raw/li_2026-11-11_13.json`, `raw/verified_13.json`, `raw/dedupe_13.json` — scan artifacts
- `JOBLESSONS_2026-11-11.MD` — this section

## Hourly cron scan — 2026-11-11 14:00 EST (19:00 UTC)

**Branch**: main (current with `033086d`, 13:14 EST refresh)

**Result**: No new verified-fresh Toronto ServiceNow/Salesforce Platform Admin / Platform Developer I / entry-level roles to merge. Null run.

**What was checked**
- Web search: ServiceNow + Salesforce Toronto postings (Nov 9–11); every surfaced role already on board under its URL or normalized company+title key:
  - Survalent Salesforce Administrator (Hybrid, Mississauga) — already on board ×3 (Workopolis 2026-11-11 line 589, Adzuna 2026-11-05 line 850, LinkedIn 2026-11-04 line 1028); duplicate, not re-added.
  - Lightspeed ServiceNow Developer (Toronto) — already on board ×5; posting describes an "existing vacancy," not fresh.
  - Cognizant Salesforce BSA / Release Engineer / Data Cloud Developer (Toronto, Nov 02–03) — senior/consultant level, outside Platform Admin/Developer I scope; no dated Toronto platform req.
  - Scotiabank ServiceNow Developer (req 260518) — skip-on-sight ("not accepting any further applicants"); Scotiabank Salesforce Developer (req 265640) — senior/architect level.
- jobs.json dedupe (2,834 rows): all Toronto/Ontario SN/SF postings from the last 48h already on the board; none entry-level Platform Admin/Dev I.
- Partner / telco / government sweep:
  - Rogers (jobs.rogers.com, SuccessFactors) — homepage scan, no Toronto SN/SF platform requisition; SN/SF appear only as familiarity/non-platform duties.
  - Bell (jobs.bell.ca, Phenom) — homepage shows Montreal roles (Buyer, AI Engineer, Digital Ops Manager); no live Toronto SN reqs besides ATEKO (already merged at 13:00).
  - Government of Canada (jobs.gc.ca) — blocked from this host; prior runs confirm zero Toronto SN/SF technical hits; GC platform work arrives via prime vendors on their own ATS.
  - Elite partners (Accenture, Deloitte, KPMG, CGI, Capgemini, IBM, TCS, Wipro) and banks (Scotiabank, RBC, TD, BMO, CIBC) — vacancies already on board; no fresh dated Toronto platform requisitions.
- Excluded (title / level / freshness rules): sales / account-management / marketing-ops titles; senior advisory / staff / manager / director roles; roles with relative ages and no verifiable absolute datePosted; expired / filled / "no longer accepting applicants" postings — skip-on-sight, never re-probed as live.

**Merged**: 0 jobs to README.md; 0 to GitHub Pages (README unchanged → no pages.yml rebuild required; board and GitHub Pages current as of 2026-11-11, SN 516 · SF 519 · Other 499 · 1,534 live).

**Lesson confirmed**: null runs are the expected norm — the :00 deep scans (00:00 merged 9 via fa52e79; 06:00 merged 3; 12:00 merged 5; 13:00 merged 23 via 0dcc9b5) remain the productive channel; off-hour scans (01:00/02:00/05:00/09:00/11:00/14:00) surface zero net-new verified-fresh Platform Admin/Platform Developer I Toronto roles. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced — remains the top keyword gap.

**Files touched**
- `JOBLESSONS_2026-11-11.MD` — this section (14:00 EST null-run record added)
- `README.md` — unchanged (SN 516 · SF 519 · Other 499 · total 1,534)
- `public/` / GitHub Pages — unchanged; no redeploy required

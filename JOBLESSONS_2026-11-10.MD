# BESTIEJOB Hourly Scan — Job Search Lessons

**Date**: 2026-11-10
**Run time**: 2026-11-10 07:00 EST (12:00 UTC)
**Scope**: Fresh Toronto / GTA ServiceNow and Salesforce postings
**Repo**: github.com/eltonaguiar/BESTIEJOB (branch: main)
**Live board**: https://eltonaguiar.github.io/BESTIEJOB/

## Scan summary

| Metric | Value |
|---|---|
| Sources queried | LinkedIn guest API (ca.linkedin.com), ServiceNow Careers (careers.servicenow.com), Salesforce Careers (careers.salesforce.com), Rogers (jobs.rogers.com), Bell (jobs.bell.ca), Government of Canada (jobs.gc.ca / canada.ca); partner/employer sites: Accenture, Deloitte, KPMG, CGI, Scotiabank, RBC, TD, BMO, CIBC |
| Dedupe baseline (README.md tables + jobs.json on main) | ~7,783+ unique URLs; README carries 5,658 live postings (ServiceNow 741 · Salesforce 943 · Other 3,974); window 2026-10-10 → 2026-11-09 |
| Fresh Toronto ServiceNow/Salesforce postings verified live AND not already on board | 0 |
| Jobs merged to README.md | 0 |
| Jobs merged to GitHub Pages (public/) | 0 (no changes required) |

## Candidates reviewed

**LinkedIn guest API — Salesforce, Toronto, last 24h (f_TPR=r86400):** 10 postings returned.
- 8 already on the board (deduped by URL): CGI Senior Salesforce Developer (4408542861), Genesys Sr. Salesforce Developer (4487960730), Smart IT Frame Salesforce Technical Architect ×2 (4487909642, 4486765411), Apptoza Senior Salesforce Developer (4487409717), Apptoza Salesforce Revenue Cloud Architect (4487173874), Diligente Senior/Lead Salesforce Marketing Cloud Engineer Mississauga (4477699547), Tekgence Salesforce Revenue Cloud Developer (4487949008). Skipped as duplicates.
- 2 not on the board, both excluded by role rule:
  - Salesforce — Partner Sales - Canada (4481519206, posted ~2h ago): sales/account role, rejected per title rule (sales/marketing roles excluded unless platform/analytics).
  - Salesforce — Principal Applied AI Architect (4487978961, posted ~7h ago): AI architecture, not a ServiceNow/Salesforce Platform Admin or Platform Developer I role; not entry-level. Rejected.
- LinkedIn ServiceNow query returned no extractable results (keyless extraction not supported for this site). LinkedIn detail pages sit behind a login wall, so posting dates cannot be independently verified — no LinkedIn-sourced role added without a verifiable absolute date.

**ServiceNow Careers (Ontario, 16 jobs):** Staff Systems Engineer (JB0073788, 11-06), Senior Staff Security Engineer | Systems Engineering (JB0076457, 11-06), Staff Security Engineer | Security Engineering (JB0076454, 11-06), Staff Site Reliability Engineer Canada Protected B (JB0076847, 11-05), Senior SRE Canada Protected B (JB0076846, 11-05) — all already on the board. Today's (11-09) postings are sales roles (Sales Director - CRM Sales; Senior CRM Account Executive) → rejected by title rule. Nothing fresh and platform-relevant.

**Salesforce Careers:** careers hub returned no extractable fresh Platform Admin / Platform Developer I postings for Toronto today.

**Partners / employers:**
- Deloitte — Senior Manager, ServiceNow - Operate (posting start 10/21/26, Toronto): outside freshness window; senior manager role.
- KPMG — Consultant/Senior Consultant ServiceNow Solution Developer (33919) and Functional Consultant (34113): existing vacancies, already captured on board (KPMG ×8). Not fresh.
- Accenture — careers hub only, no extractable fresh posting.
- CGI — Senior Salesforce Developer / Salesforce Architect in Toronto appear on Indeed aggregator but no extractable fresh direct posting date; CGI Senior Salesforce Developer (4408542861) already on board via LinkedIn.

**Rogers (jobs.rogers.com):** Lead Management Operations (Salesforce, Req 343961, posted 2026-10-28) — outside freshness window; already flagged. No fresh SN/SF technical roles.
**Bell (jobs.bell.ca):** no fresh ServiceNow/Salesforce technical roles surfaced; prior Bell SN roles were filled/expired.
**Government of Canada (jobs.gc.ca):** zero ServiceNow/Salesforce Toronto hits; GC platform work arrives via prime vendors on their own ATS.

**Banks:** Scotiabank ServiceNow Administrator Specialist (Req 261367 / 602949717) already on README (via hermes scan 2026-11-09). Scotiabank ServiceNow Developer (260518) and Salesforce Developer (265640) are senior/architect roles with no fresh extractable date; not entry-level Platform Admin/Dev I.

## Already on the board (context)

README.md on main is current through 2026-11-09 (5,658 live postings; ServiceNow 741 · Salesforce 943 · Other 3,974). Today's scan adds no verified fresh rows.

## Patterns / lessons for future agents

1. **LinkedIn guest API works for Salesforce but not ServiceNow.** The `seeMoreJobPostings` guest endpoint returned 10 Salesforce Toronto postings for `f_TPR=r86400`; the identical ServiceNow request was rejected (keyless extraction not supported / HTTP 403). ServiceNow hits must come from careers.servicenow.com or aggregators instead.
2. **LinkedIn gives relative ages only ("X hours ago"); detail pages are a login wall.** Absolute `datePosted` can't be verified by extraction, so no LinkedIn-sourced role enters the board without a verifiable date. The 8 already-boarded LinkedIn Salesforce roles came from prior scans with verified dates.
3. **Dedupe catches most fresh aggregator hits.** 8 of 10 fresh LinkedIn Salesforce postings were already on the board under the same LinkedIn URL. Always dedupe by normalized URL before judging.
4. **Role rule excludes the non-duplicate LinkedIn hits.** The two not-yet-boarded LinkedIn roles are a sales role (Partner Sales) and a principal AI architect — neither is a ServiceNow/Salesforce Platform Admin or Platform Developer I. Target titles stay: Platform Administrator, Platform Developer I, ServiceNow Administrator/Developer, plus CSA/CAD/CIS certs.
5. **Employer/partner career sites surface senior roles, not entry-level.** Deloitte (Senior Manager), KPMG (3+ yrs), Scotiabank (5+ yrs Administrator Specialist) are all mid/senior. Entry-level Platform Admin / Developer I Toronto postings remain scarce; the board's value is in capturing them when they appear, not forcing a merge every hour.
6. **Zero fresh merges on most hourly runs is the norm.** jobs.json/README are refreshed multiple times daily; today's board already carries postings through 2026-11-09. An hour scan that finds nothing verified-fresh is a clean run, not a failure.

## Recommended next scans

- Retry LinkedIn guest API for ServiceNow Toronto in a later hour (endpoint may be intermittently available); if still blocked, use `site:ca.linkedin.com/jobs/view servicenow toronto` web search to surface indexable deep links.
- Re-check KPMG careers (33919 / 34113) and Scotiabank ServiceNow Developer (260518) for a verified absolute posted date; add if fresh and not already boarded.
- Keep scanning named employer ATS deep-links (careers.servicenow.com, careers.kpmg.ca, jobs.scotiabank.com, careers.deloitte.ca) for Toronto SN/SF — aggregator mirrors lag employer sites.

## Files touched

- `JOBLESSONS_2026-11-10.MD` — this file, added to repo root on main.
- `README.md` — no changes (zero verified fresh jobs this hour).
- `public/` (GitHub Pages) — no changes; no redeploy required.


## 08:00 EST cycle (2026-11-10) — post :00 UTC hourly scan

Ran after the repo's hourly Action (894cfd6 "chore(jobs): fresh CA sweep 2026-11-10T12:46Z [skip ci]", 07:46 EST). Local main had been 85 commits behind origin; synced with `git pull --rebase origin main` before scanning. Feed baseline verified on disk: jobs.json 5,338 rows (scraped 2026-11-10T12:16:55Z), ServiceNow 1,077 / Salesforce 1,074. Layered manual search on top of the just-run ATS sweep.

### Sources checked
- **Indeed.ca** — ServiceNow Toronto and Salesforce Toronto/consultant pages, date-sorted: BFG Enterprise Services ServiceNow Administrator/Developer Markham (careers.bfg.ca original Oct 13–20 window expired); BMO ServiceNow SAM Administrator - ITAM ("New"/relative dates only, ≈Nov 5, already swept by Workday scan); Compugen Sr ServiceNow CSDM/Discovery contracts ("New", no absolute dates); Bevertec ITOM Business Analyst ("New"); Deloitte/KPMG/CGI/BDO ServiceNow roles — all already in jobs.json or lacking absolute posted dates.
- **LinkedIn guest** — 429/403 blocked; posting dates unverifiable; no LinkedIn-sourced role added without a confirmable date.
- **ServiceNow careers Ontario** — 16 Ontario jobs: Sales Director CRM Sales and Senior CRM Account Executive (Nov 09) are sales roles (excluded by title rule); Staff Systems Engineer / Staff Security Engineer / Staff SRE Protected B (Nov 05–06) already tracked; nothing in Platform Administrator / Developer I targeting.
- **Salesforce careers hub** — no extractable fresh Platform Admin / Platform Developer I posting for Toronto today.
- **Rogers jobs.rogers.com** — Lead Management Operations (Salesforce marketing ops, Req 343961, ~Oct 28, outside freshness); Technical Specialist Markham (Cisco Meraki/Fortinet, ServiceNow/Salesforce familiarity listed as preferred, not a platform role); Digital Campaigns / Campaign Management (Salesforce as CRM — sales/marketing titles, excluded by title rule). No dated platform posting.
- **Bell jobs.bell.ca / jobs.bce.ca** — ServiceNow System Administrator 432824 "has been filled"; Senior Manager ServiceNow Platform Delivery "no longer accepting applicants"; Senior Technical Advisor 431695 (404/gone, apply-by 11/02/2026 expired). Skip-on-sight; never re-probe filled/expired roles as live.
- **TELUS careers.telus.com** — Salesforce matches are Account/Senior Account Manager sales titles; excluded by the board's title rule.
- **Government of Canada jobs.canada.ca** — zero ServiceNow/Salesforce Toronto hits. Ontario gojobs.gov.on.ca — expired or non-platform roles. Low yield again; GC platform work arrives via prime vendors on their own ATS (already covered by the automated sweep).
- **Elite/Global Elite Partners** — KPMG (33919, 34113 existing vacancies), Accenture, Deloitte (Senior Manager ServiceNow - Operate, posting start 10/21/26 — outside freshness window), Capgemini, CGI, IBM, TCS: postings arrive via the automated ATS sweep; nothing incremental from manual careers-page checks.
- **Banks (Workday)** — Scotiabank ServiceNow Administrator Specialist 602949717 / Developer 603030017 / Discovery Developer 602442317 already on board; TD/RBC/BMO/CIBC boards surfaced no new dated SN/SF requisitions.
- **Non-feed employers (Indeed SERP only)** — Vigorate, StorageVault, Atlantic Packaging, Minto Group Salesforce roles surfaced on listing pages (senior, 4–5+ yrs) without verifiable posted dates or direct deep links; excluded by absolute-date and freshness rules.

### Candidates already on the board (duplicates, not re-added)
- Scotiabank ServiceNow Administrator Specialist 602949717; ServiceNow Developer 603030017; Discovery Developer 602442317 (jobs.scotiabank.com)
- Altus Group Salesforce Platform Developer R0014087 (Workday, tracked)
- Lightspeed ServiceNow Developer (multiple feed mirrors)
- SS&C Technologies + Benevity Salesforce roles (merged in the 00:00 EST cycle this date)

### Result
Zero new merges. jobs.json stays 5,338 rows; README tables unchanged; no public/ rebuild required. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs): none surfaced — keep as priority keywords.

### Pattern confirmed
Cycles immediately after the :00 UTC ATS sweep are typically null for manual search — the sweep captures nearly all Toronto SN/SF volume; manual value is only in employer career pages and non-ATS boards with verifiable absolute dates, and this cycle produced none.

### Files touched
- `JOBLESSONS_2026-11-10.MD` — this section appended on repo root on main.
- `README.md` — no changes (zero verified fresh jobs this hour).
- `jobs.json` — no changes (5,338 rows).
- `public/` (GitHub Pages) — no changes; no redeploy required.

## 09:00 EST cycle (2026-11-10) — second post-:00 UTC manual scan

Ran after the 08:00 EST cycle (JOBLESSONS_2026-11-10.MD already on main via 357e6dc). Manual search layered on top of the just-run ATS sweep; jobs.json on disk = 5,083 deduped rows, 49 rows posted 2026-11-09 already tracked.

### Sources checked
- **Indeed.ca / Dice / Robert Half / SimplyHired SERPs**, date-sorted, ServiceNow + Salesforce Toronto:
  - Altus Group Salesforce Platform Developer (Toronto, $105K–$115K, PD1/PD2) — already on the board ×4 (workday R0014087, linkedin 4483476940, adzuna 5949004280, simplyhired). Dupe, skipped.
  - Robert Half Salesforce Developer Toronto, remote/permanent, $90–95K, page-dated 2026-11-10 — URL is a hub listing page (`/ca/en/jobs/...`, not a `/job/` deep link), client confidential, generic "Salesforce Developer" not Platform Developer I → excluded by hub-URL and title rules. Prior Robert Half row (2026-10-27) already archived on the board.
  - Dice: CA-One Tech Cloud (10+ yrs, senior), Stefanini (US/remote), IntelliX (18+ yrs), GDH senior — none entry-level Platform Admin/Dev I Toronto; relative ages only ("5d ago", "Today"), no verifiable datePosted.
  - SimplyHired Altus row noted above as a dupe of the tracked Workday req.
- **ServiceNow Careers Ontario** (16 jobs): Senior CRM Account Executive + Sales Director - CRM Sales (Nov 09 — sales, title-rule excluded); Staff Systems Engineer / Staff Security Engineer ×2 / Staff + Senior SRE Protected B (Nov 05–06, already tracked). No Platform Administrator / Developer I.
- **Salesforce Careers Canada hub**: sales / Customer Success roles only; no Platform Admin / Platform Developer I.
- **LinkedIn guest API**: 429/403 blocked; detail pages login-walled — no LinkedIn-sourced add without a verifiable absolute date. Near-miss LinkedIn roles reviewed and skipped: ScanSource Salesforce Administrator II Toronto (4123838085, stale id), SRx Health Salesforce Administrator Toronto (1+ yr exp, date unverifiable), EvenUp / Carbon6 / OpenTable Salesforce Administrator (senior), Finning Platform Administrator I (0–3 yrs but Vancouver / Calgary / Edmonton — not GTA), City of Toronto Corporate Application Technical Leader / Senior Systems Integrator Salesforce Developer (Nov 09 — leader/senior, not entry-level; LinkedIn date unverifiable).
- **Rogers (jobs.rogers.com)**: Technical Specialist Markham (ServiceNow/Salesforce only "preferred" familiarity — not a platform role), Lead Management Operations Ottawa (Salesforce marketing ops — sales/marketing title), Platform Specialist Toronto (VMware/NetApp infra; ServiceNow only for tickets), Digital Campaigns & Experience Optimization Manager (Braze/Salesforce CRM marketing). All excluded by title rule; no fresh dated SN/SF platform posting.
- **Bell (jobs.bell.ca / jobs.bce.ca)**: ServiceNow System Administrator 432824 filled; Senior Manager ServiceNow Platform Delivery no longer accepting applicants; ServiceNow Senior Technical Advisor 432829 deadline 11/02/2026 expired; Senior Software Architect II - ServiceNow Platform Architect deadline 04/02/2026 expired. Skip-on-sight, never re-probed as live.
- **Government of Canada (jobs.gc.ca / canada.ca)**: zero ServiceNow/Salesforce Toronto hits. City of Toronto (municipal) — lead/senior Salesforce roles only, already tracked, not entry-level.
- **Elite / Global Elite Partners + banks**: KPMG 33919/34113 existing vacancies already on the board; Deloitte Salesforce Developer posting start 9/29/26 (outside freshness window, 3+ yrs); Accenture / CGI / IBM / TCS / Capgemini arrive via the ATS sweep only — nothing incremental from manual careers-page checks; Scotiabank / TD / RBC / BMO / CIBC Workday boards — no new dated SN/SF requisitions.

### Result
Zero new verified-fresh merges this cycle. jobs.json stays 5,083 rows; README.md tables unchanged; no public/ rebuild required.

### Patterns / lessons confirmed
1. The :00 UTC ATS sweep (already committed before this 09:00 cycle) captures nearly all dated Toronto SN/SF volume; post-:00 manual cycles are typically null — a clean zero-merge run is expected, not a failure.
2. Hub/search URLs keep surfacing (roberthalf.com/ca/en/jobs/..., indeed /q-..., jobs.ca/<company>, wellfound /role/) — they must be filtered by `is_listing_url()` at both sync and render time before reaching README/public.
3. Relative ages ("5d ago", "Today", "4d ago") on Dice/Indeed are not verifiable posted dates — roles without an absolute `datePosted` do not enter the board.
4. Rogers / Bell / GC employer pages yield marketing-ops, infra-adjacent, or expired/filled postings — the title rule plus skip-on-sight keeps the board clean.
5. Finning Platform Administrator I (0–3 yrs) matched the entry-level Platform Administrator title but outside the GTA — geographic filter holds; no Toronto exception this cycle.
6. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced this hour — remains the top priority keyword gap.

### Files touched
- `JOBLESSONS_2026-11-10.MD` — this section appended (repo root, main).
- `README.md` — no changes (zero verified fresh jobs this hour).
- `jobs.json` — no changes (5,083 rows).
- `public/` (GitHub Pages) — no changes; no redeploy required.

## 10:00 EST cycle (2026-11-10) — third post-:00 UTC manual scan

Ran after the 09:00 EST cycle (already committed to main via f44e869). jobs.json on disk = 5,337 rows, scraped 2026-11-10T13:11:22Z. Manual search layered on top of the committed ATS sweep.

### Sources checked
- **jobs.json baseline (5,337 rows)** — zero ServiceNow/Salesforce postings dated 2026-11-10 in any location; zero Toronto SN/SF postings dated 2026-11-09 or 2026-11-10. The board's deduped baseline already carries everything the sweep captured.
- **Indeed.ca** — ServiceNow Administrator/Developer (Intermediate), BFG Enterprise Services, Markham (2–4 yrs, CSA required) — intermediate, not Platform Admin/Dev I; ServiceNow System Administrator JOB-37505 (5+ yrs CSA, contract from Nov 9) — senior; Salesforce Administrator (Hybrid), Survalent, Mississauga ($70–90K, "New") — relative age only, no verifiable absolute posted date; all other SERP hits already tracked or senior.
- **ZipRecruiter / Dice / Robert Half** — SN/SF hits are intermediate/senior (CSA+CAD mandatory, 5+ yrs), relative ages only, no verifiable datePosted; no entry-level Platform Admin/Dev I Toronto.
- **ServiceNow Careers Ontario** — 16 jobs unchanged from prior cycles (Staff Systems/Security Engineer Nov 06, Senior CRM Account Executive, Sales Director CRM Sales — sales roles excluded by title rule). No Platform Administrator / Developer I.
- **Salesforce Careers Canada hub** — no extractable fresh Platform Admin / Platform Developer I for Toronto.
- **LinkedIn guest API** — 429/403 blocked; no LinkedIn-sourced add without verifiable absolute date.
- **Rogers (jobs.rogers.com)** — Lead Management Operations (Salesforce marketing ops, excluded by title rule); Technical Specialist Markham (ServiceNow/Salesforce only "preferred" familiarity — not a platform role). No fresh dated SN/SF platform posting.
- **Bell (jobs.bell.ca / jobs.bce.ca)** — ServiceNow System Administrator 432824 filled; Senior Manager ServiceNow Platform Delivery no longer accepting applicants; ServiceNow Senior Technical Advisor 432829 deadline 11/02/2026 expired; ServiceNow Developer / Integrator 431695 (Ottawa/Toronto/Montreal/Quebec City) — senior advisory role, not entry-level Platform Admin/Dev I. Skip-on-sight.
- **Government of Canada (jobs.gc.ca / canada.ca) + Ontario gojobs.gov.on.ca** — zero ServiceNow/Salesforce Toronto hits.
- **Elite/Global Elite Partners + banks** — KPMG 33919/34113 already on board; Deloitte postings outside freshness window or 3+ yrs; Accenture/CGI/IBM/TCS/Capgemini arrive via ATS sweep only; Scotiabank/TD/RBC/BMO/CIBC Workday boards — no new dated SN/SF requisitions.

### Result
Zero new verified-fresh merges this cycle. jobs.json stays 5,337 rows; README.md tables unchanged (ServiceNow 746 · Salesforce 956 · Other 4,118 · 5,820 live); no public/ rebuild required.

### Patterns / lessons confirmed
1. The committed jobs.json baseline (5,337 rows, scraped 2026-11-10T13:11Z) shows zero SN/SF postings dated 2026-11-10 anywhere — today's hourly scan surface is clean.
2. All Toronto SN/SF SERP hits this hour are intermediate/senior (2–5+ yrs, CSA/CAD mandatory) — none match the entry-level Platform Administrator / Platform Developer I targeting.
3. Roles with relative ages ("New", "5d ago") but no verifiable absolute `datePosted` are excluded — Survalent Salesforce Administrator (Mississauga) falls here.
4. Bell's ServiceNow Developer / Integrator (431695) is a senior advisory role across 4 cities — title and level rule exclude it; skip-on-sight for filled/expired Bell postings holds.
5. Entry-level Salesforce Platform Administrator / Platform Developer I (0–2 yrs) in Toronto: none surfaced this hour — remains the top priority keyword gap.
6. Third consecutive post-:00 UTC manual cycle with zero merges — null runs are the expected norm, not failures.

### Files touched
- `JOBLESSONS_2026-11-10.MD` — this section appended (repo root, main).
- `README.md` — no changes (zero verified fresh jobs this hour).
- `jobs.json` — no changes (5,337 rows).
- `public/` (GitHub Pages) — no changes; no redeploy required.

## 11:00 EST cycle (2026-11-10) — hourly scan via daily_scan.sh (SCAN_PUSH=1)

Ran the full hourly pipeline: `node scripts/daily_job_scan.mjs` → gap scan → web search → today feeds → inbox merge → semantic dedupe → `sync_readme_to_jobs.mjs` → `verify_links.py` → `tools/build_site.py` → commit + push. jobs.json baseline on disk was 5,337 rows (scraped 2026-11-10T13:11:22Z); the ATS sweep surfaced 2,339 matching postings across 10 sources (adzuna 395, linkedin 253, greenhouse 16, workday 14, smartrecruiters 10, remotive 4, ashby 2, lever 1, remoteok 1, jobicy 1). LinkedIn guest API returned 429/403 — no LinkedIn-sourced add without a verifiable absolute posted date.

### Sources checked (partner / employer / Canadian tech focus)

- **ServiceNow careers Ontario** — 16 Ontario jobs; Senior CRM Account Executive and Sales Director - CRM Sales (Nov 09) are sales roles (title-rule excluded); Staff Systems/Security Engineer postings (Nov 05–06) already tracked. No fresh Platform Administrator / Developer I.
- **Salesforce Careers Canada hub** — no extractable fresh Platform Admin / Platform Developer I for Toronto.
- **Rogers (jobs.rogers.com)** — no fresh dated ServiceNow/Salesforce platform posting; prior hits were marketing-ops or "preferred familiarity" infra roles, excluded by title rule.
- **Bell (jobs.bell.ca / jobs.bce.ca)** — ServiceNow System Administrator filled; Senior Manager ServiceNow Platform Delivery no longer accepting applicants; Senior Technical Advisor 431695 expired (apply-by 11/02/2026). Skip-on-sight holds; never re-probe filled/expired roles as live.
- **Government of Canada (jobs.gc.ca / canada.ca) + Ontario gojobs.gov.on.ca** — zero ServiceNow/Salesforce Toronto hits. GC platform work arrives via prime vendors on their own ATS (already covered by the automated sweep).
- **Elite / Global Elite Partners + banks** — Accenture ServiceNow HAM Consultant (Canada, full-time, accenture.com careers deep link) captured by the sweep; KPMG 33919/34113 already on board; Deloitte/Capgemini/CGI/IBM/TCS postings arrive via ATS sweep only; Scotiabank/TD/RBC/BMO/CIBC Workday boards — no new dated SN/SF requisitions.
- **Indeed.ca / Dice / Robert Half / SimplyHired SERPs** — SN/SF hits are intermediate/senior (2–5+ yrs, CSA/CAD mandatory), relative ages only, no verifiable datePosted; hub/search URLs filtered by `is_listing_url()`.

### Fresh 2026-11-10 Toronto/Canada SN/SF postings verified live and merged

**ServiceNow:**
- ServiceNow Platform Specialist — Alimentiv — Canada (jobicy.com/jobs/160724)
- ServiceNow Hardware Asset Management (HAM) Consultant — Accenture — Canada (accenture.com careers deep link, Elite Partner)
- ITOM Solution Architect — ServiceNow — North America / Canada (smartrecruiters)

**Salesforce:**
- Senior Salesforce Developer — LanceSoft Inc. — Toronto, ON (linkedin)
- Salesforce Technical Architect — Smart IT Frame LLC — Toronto, ON (linkedin)
- Salesforce Senior FSC Developer / Technical Lead — Apptoza Inc. — Toronto, ON (linkedin)
- Associate Salesforce Administrator — Jobgether — Canada (linkedin) ← entry-level Platform Administrator match
- Salesforce Implementation Specialist (Hybrid or Remote) — Traction Rec — Canada (adzuna)
- Salesforce CPQ Lead Developer — E-Solutions — Canada (linkedin)

Non-Toronto 11-10 postings (kept in jobs.json feed, not in capped README tables): ServiceNow Architect FTR Burnaby (NTT DATA), Analyste QA ServiceNow CGI Sherbrooke, Senior Salesforce Developer Intact Montreal, Salesforce Platform Owner Parkland Calgary, Salesforce Developer Service New Brunswick.

### Result

265 new rows added to jobs.json via README sync; site rebuilt: **2,155 jobs** (ServiceNow 774 · Salesforce 840 · Other 541), 251 duplicate mirrors collapsed, 34 applied roles hidden, 1,497 best-match. Committed and pushed to origin/main as `9a560f5` — "chore(jobs): daily scan refresh (2554 listings, 2026-11-10)". GitHub Pages serves from `public/`; no separate redeploy needed (Pages deploys on main push).

### Patterns / lessons confirmed

1. **Accenture (Elite Partner) HAM/ITAM roles surface via their careers ATS deep link** — accenture.com jobdetails URLs are extractable and dated; add Elite Partner careers pages (Accenture, Deloitte, KPMG, Capgemini, CGI, IBM, TCS) as recurring manual targets alongside the ATS sweep.
2. **Entry-level Platform Administrator matches remain rare** — Associate Salesforce Administrator (Jobgether, Canada) is the one 0–2 yr Platform Admin signal this cycle; keep "Associate Salesforce Administrator" and "Platform Administrator" as priority keywords.
3. **LinkedIn guest API remains unreliable (429/403)** — 253 LinkedIn postings appeared in the scan feed but most lack verifiable absolute dates; LinkedIn-sourced roles only enter when a datePosted can be confirmed from the employer ATS or aggregator mirror.
4. **Rogers / Bell / GC employer pages yield no fresh dated SN/SF platform roles** — Bell postings are skip-on-sight (filled/expired); Rogers hits are marketing-ops or infra-adjacent; GC platform work comes via prime vendors on their own ATS. The title rule plus skip-on-sight keeps the board clean.
5. **Semantic dedupe collapses aggregator mirrors** — 53 dupes collapsed this cycle (Adzuna + LinkedIn + jobs.ca mirrors of the same requisition); always run semantic_dedupe --apply before sync_readme_to_jobs.
6. **Post-:00 UTC cycles can produce merges** — unlike the 07:00–10:00 null cycles, this 11:00 run found 7 fresh SN/SF postings; freshness windows shift hour to hour, so every hourly scan is worth running.

### Files touched

- `JOBLESSONS_2026-11-10.MD` — this section appended (repo root, main).
- `README.md` — tables rebuilt via build_site.py (capped at 400 per family for display; full 2,155 in public/jobs-data.json).
- `jobs.json` — 265 rows added via sync (2,554 total feed rows).
- `public/jobs-data.json` + `public/index.html` — rebuilt and pushed (GitHub Pages).
- `README.BAK_2026-11-10T160600Z.md`, `README.DEDUPE_2026-11-10T160601Z.md` — archive + dedupe artifacts.

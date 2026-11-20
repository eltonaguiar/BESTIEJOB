# JOBLESSONS — 2026-11-20 11:00 EST (16:00Z) cron scan

Run: hourly scan for fresh Toronto/GTA ServiceNow + Salesforce roles, dedupe against `jobs.json` / README / APPLIED, merge verified rows to README + GitHub Pages, sweep partner/Elite-partner/telco/public-sector channels.

## Yield this hour
- Pipeline run: `node scripts/daily_job_scan.mjs` → fresh=531, merged=5618 (SN 1188 / SF 4287); README DAILY-SCAN block + FRESH_JOBS.md + 4 feed copies rewritten.
- **Net-new URLs vs origin/main base: 33 — but 32 of them were company+title twins** (same role re-issued under a new URL/id by Adzuna/LinkedIn/Ashby/Greenhouse). Only **1 genuinely new company+title**: **Galent — "Salesforce, nCino, Omnistudio Developer" (Toronto, hybrid)** — LinkedIn 4491941158, body-verified live at 11:06 EST ("41 minutes ago", 8+ yrs, nCino/OmniStudio/Apex/LWC/Omnistudio lead).
- Notable twins worth knowing (site collapses them into the surviving card's `alternates`, README keeps the freshest row): TechNeptune "ServiceNow CMDB Consultant" (new id 4491940243 → board 4489716220/4491354155), Jobgether "Salesforce Business Process Analyst" (4492537774/4492529940), Amicis "ServiceNow BA - Senior - Toronto (3 days onsite)" (**Adzuna re-issued 5972002660 as 5972983023**).
- Site rebuilt: 5052 cards (SN 863 / SF 923 / other 3266), 837 mirrors collapsed, built 2026-11-20 16:04Z. README table count 6137 → 6161 live postings.

## Source-by-source findings (reuse next hour)
| Source | Result this hour | Notes for next agent |
|---|---|---|
| daily_job_scan Workday CXS (15 boards) | **Every tenant 429'd mid-scan at 16:02Z** (`[workday] 0 matching postings`) | The :00Z CI hourly scan collides with a manual run — same known pattern. **Do not treat as zero postings.** |
| Workday manual re-probe 16:06Z (bmo, td, cibc, manulife, interac, caatpension, salesforce, accenture, bdo, gdit) | **All 20 queries HTTP 200** — 429 clears within ~4 min | 24 "Posted Today" rows across 10 boards, **zero Canadian SN/SF platform roles**: BMO=Communications Mgr, TD=Financial Advisor Assoc (US), Salesforce=non-Canada (IE/UK/AE/IN/JP/AU/"N Locations"), GDIT=ServiceNow Principal but **Arlington VA (Top Secret/SCI)**. Canada rows are all already on board: BMO SN CMDB Admin (8d) + SN Lifecycle Analyst (8d), TD SN Architect (4d)/nCino-SF (3d)/SF Data360 (7d), CIBC SF Delivery (16d), Interac CRM Lead (10d). |
| CIBC "IT Administration Analyst" (Posted Today, Toronto) | ServiceNow mention ×3 but **access provisioning role** ("fulfill user access requests submitted through ServiceNow") | Tooling, not platform. Skip per the "ServiceNow-as-ticketing ≠ platform role" rule. |
| Adzuna API | 214 hits; **id recycling confirmed again** — Amicis BA Senior re-issued under a fresh id same day | Detail pages still CloudFront-403 to curl/headless; dedupe on company+title before treating a new ad id as fresh. |
| LinkedIn guest scan | 273 cards after two HTTP 429s (retries succeeded inside the same run) | Do not conclude "empty" on the 429; retry works. New: Galent (verified). Everything else ≤ 23 h old was already tracked (Flexstaf, Pacer, Virtusa, RBC Discovery, NTT DATA BA). |
| SmartRecruiters (ServiceNow) | 13; **ServiceNow "Staff Full-Stack Engineer, Experience Team" Toronto** (also Adzuna mirror) and "Principal Solution Architect- ServiceNow" (10-29, twin) | Platform-company engineering roles stay tagged servicenow via forceTags; both already on board. |
| Greenhouse / Lever / Ashby | 17 / 1 / 2 | NeuraFlash "Salesforce Technical Architect, AI and Agentforce" (twin), **EQ Bank "Senior ServiceNow Engineer" (Toronto hybrid — new to board, Lever 1af36346)** , Alimentiv "ServiceNow Platform Specialist" (twin), Benevity SF Admin twins. |
| Rogers (jobs.rogers.com) | Phenom still serves a ~56 KB shell, zero rows server-side | LinkedIn 7-day "ServiceNow Rogers Toronto" search: **0 Rogers rows** (25 cards, none Rogers). A 100jobs.org "Senior ServiceNow BSA – Rogers" lead is an **SPA deep link whose canonical collapses to the homepage — unverifiable, not added**. |
| Bell / Ateko | Nothing new today | Bell's SN hiring still surfaces only as "Ateko, backed by Bell Canada" on LinkedIn (last Ateko rows 11-19 are on board). jobs.bell.ca still 0. |
| Government / public sector | Job Bank "ServiceNow" title search = generic IT noise, nothing dated today; gojobs/jobs.gc.ca still Radware-walled | Ontario VOR reqs keep arriving as **"RQ#####" agency rows** (TWC/Cleo/Metrolinx — added 10:00 hour). Search Adzuna for `RQ00` + ServiceNow next hours. |
| Partners / Elite partners | Covered by the scan this hour: **Accenture** (SF Data Cloud MarTech Consultant, Canada — today), **NeuraFlash** (SF Technical Architect AI/Agentforce), **PwC** (Sr SN Developer, 11-19 on board), **Compugen/LGS** (11-19), **Deloitte/KPMG/TD/BMO/CIBC/Interac/Scotiabank** all present | No new partner req posted *today* beyond Accenture/NeuraFlash already on the board. |

## Mechanics lessons
1. **"fresh=N" from the scan is not "N new rows."** fresh=531 vs 33 net-new URLs vs 1 net-new company+title. Always diff URL sets against `git show origin/main:jobs.json` before reporting additions.
2. **32/33 net-new were twins** — normal at saturation; the site dedupes them via company+title (837 collapsed this build), so do **not** hand-prune jobs.json to "fix" them.
3. **A fast Workday 429 retry is worth it**: one bash loop, 10 tenants × 2 queries at 8 s spacing (~2.5 min) after the scan cleared every board to 200 and proved there were no fresh Canada SN/SF reqs (valuable negative result vs. guessing).
4. **`100jobs.org` deep links are SPA shells** — `curl` returns the generic homepage with canonical=`https://100jobs.org/`. Never cite its text as a posting; re-verify on LinkedIn/ATS or drop.
5. Scan order that worked this hour: `daily_job_scan.mjs` → `tools/build_site.py` → `scripts/sync_readme_counts.py` → verify new URLs inside `public/jobs-data.json` → commit data files only (never the `raw/`, `leads-*`, `reports/` scratch, never the `ServiceNow_Learning…` submodule pointer).
6. `python3` on PATH is the WindowsApps stub — use `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe` explicitly for `build_site.py` / `sync_readme_counts.py`.

## Dedupe keys that worked
- Normalized URL (host+path, query stripped) for exactness; **company.lower()|title.lower()** to catch reposts (flagged 32/33); trailing LinkedIn numeric id and Adzuna detail id as tie-breakers. Twin detection happened *before* any hand-add, so nothing fresh beyond Galent was claimed.

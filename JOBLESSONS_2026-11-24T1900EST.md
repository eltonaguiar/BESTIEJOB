# JOBLESSONS_2026-11-24T1900EST — hourly BESTIEJOB scan lessons

## Scan summary
- Run time: 2026-11-25T00:01Z (19:01 EST), cron job
- Base: origin/main fd21e5a0 (18:00 EST lessons commit), already up to date
- Local commit: cac77967 "chore(jobs): 19:00EST hourly scan refresh (5682 listings; 0 net-new verified)" — pushed WITHOUT `[skip ci]` so pages.yml deploys
- Deploy: `Deploy GitHub Pages` run 45516221017 queued on cac77967; audits (board invariants / README job-row guard / Job Source Truth Check) also queued on the same SHA
- Commit contents: jobs.json, README.md, FRESH_JOBS.md, public/{jobs.json,jobs-data.json,index.html,gotjob/jobs.json,findjobs/jobs.json}; untracked raw/* scratch left untracked (policy)

## Source results (this hour)
| Source | Matching postings | Notes |
|---|---|---|
| LinkedIn (guest) | 247 | Healthy; guest endpoint answered without the 429 wall this hour |
| Adzuna Canada API | 180 | 503s on the first three ServiceNow queries, then recovered; ≥3s spacing still required |
| SmartRecruiters (ServiceNow board) | 12 | Largest single SN source not on LinkedIn guest feed |
| Greenhouse (9 slugs) | 12 | |
| Remotive / Remote boards | 6 | Canada-geo filter applied |
| Ashby (3 boards) | 2 | |
| Lever (3 boards) | 1 | |
| Workday CXS (17 tenants × 2 queries) | 0 at scan time | All HTTP 429 at :01Z — the :00Z CI-concurrency rate limit. Manual 6-tenant probe at 00:08Z: **all HTTP 200**. |

Merge result: fresh=460, merged=5682 (servicenow 1,205 / salesforce 4,319). **Net-new URL diff = 0 added / 0 removed** vs origin/main — the 460 "fresh" rows are Adzuna re-issues under new IDs, LinkedIn re-serves, and company+title twins already on the board. `fresh=N` is not "N new rows"; always diff URL sets.

## Manual Workday probe (00:08Z, after the :00Z window)
All six boards HTTP 200 with postings. Fresh ("Posted Today/Yesterday") platform-relevant rows:
- **BMO — Senior Sales Force Developer — R260032445 — Toronto, ON (3 Locations)** — startDate 2026-11-24, ends 2026-12-25. Description: "learn about Risk Management while further enhancing your Salesforce technical skills… HYBRID… 2 days in any of the 4 Greater Toronto office locations"; 3–5 yrs Salesforce Lightning, LWC, Apex, Aura, Flows. **This is the same req already added at 15:00 EST via two LinkedIn rows** (`...4494172759` Scarborough, `...4494175406` Toronto) — identical Risk-Management/hybrid/4-office description. Not added again (company+title+location duplicate).
- **BMO — Senior Salesforce Developer — R260032496 — Chicago, IL, USA (4 Locations)** — same description family. **US req — excluded from a Canada-focused board.** Do not add.
- **TD — Software Engineer II (Salesforce Loyalty Management Developer) — R_1509038 — Toronto** — Posted Today; already on the board (18:00EST lessons).
- **Manulife — Salesforce Functional Analyst — JR26101237 — Waterloo, ON** — Posted Today; **already on the board** with its Workday URL in jobs.json. 2–3 locations.
- **CIBC — Sr. Consultant, Infrastructure Management — 2623517 — Toronto** — Posted Today; ServiceNow only "an asset" alongside Ansible/OpenShift — **infrastructure role, not a platform role. Skip.**
- **TD — Information Security Specialist — R_1522025 — Toronto** — Posted Today; security, not platform. Skip.
- **Manulife — Manager, Technology Governance & Controls — JR26100922 — Toronto** — Posted Today; governance, not platform build. Skip.
- BMO Salesforce search also returned Toronto marketing/EA/non-platform titles (relevance-matched on the word "Salesforce" in body) — filter on title before reading.

## Employer / partner checks (Toronto SN/SF focus)
- **Scotiabank Phenom** (`jobs.scotiabank.com/search/?q=…&sortColumn=referencedate`): `servicenow` has 10 rows but the only real SN role is **ServiceNow Developer — Bogota, DC, CO** (Nov 3) — not Canada. `salesforce` returns 25 generic banking rows (Product Manager, advisors, credit associates) that only mention the platform in body text — nothing platform-build and nothing fresh. No addition.
- **Cognizant careers search** (`careers.cognizant.com/global/en/search-results?keywords=…`): HTTP 301 → 200 after `-L`, but the page is a ~56 KB client-rendered shell with no server-side job rows (grep only finds the search-string echo). Cannot enumerate roles from the search page; use detail URLs / search-engine-indexed metadata as in earlier cycles.
- **Rogers / Bell / Job Bank / ServiceNow Careers**: unchanged from the 17:00–18:00 runs (Rogers zero server-side rows; Bell empty shell; Job Bank Radware-walled and stale; ServiceNow Careers Cloudflare). Re-check weekly, not hourly.

## Tech notes / new lessons
1. **Workday CXS path must use the tenant WITHOUT the `.wdN` suffix.** `POST https://{tenant}.wd3.myworkdayjobs.com/wday/cxs/{tenant-short}/{site}/jobs` — a probe that put `bmo.wd3` in the path got **HTTP 422 on every board**; `${host%%.*}` (single `%`) strips `.wd3`, `${host%%%%.*}` does **not** (it strips nothing, because `%` is literal in the glob) and silently reproduces the 422. 422 = wrong tenant/site path, 429 = rate limit — distinguish them before concluding a board is dead.
2. **A Workday 429 at :00–:02Z is transient.** The scan's 17-tenant pass 429'd all boards at 00:01Z; a 6-tenant probe at 00:08Z (8 s spacing) returned 200 everywhere. Keep the manual retry for the key Canadian tenants when `[workday] 0 matching postings` appears.
3. **Workday `postedOn: "Posted Today"` ≠ Canada.** BMO R260032496 is Chicago; Salesforce-the-company's fresh rows are US/EU sales roles. Read `locationsText` and the `/job/<City>/` slug.
4. **Check the board's README "Verified fresh additions" sections, not just jobs.json, before calling a req new.** The BMO Senior Salesforce Developer role was added at 15:00 EST as README-only rows (never written to jobs.json); a jobs.json URL grep alone would have missed it and double-listed the Workday req.
5. **Adzuna can 503 mid-batch and recover.** First three ServiceNow queries failed, the rest returned 180 rows; the run is still healthy because other sources covered the gap. Do not close a run blocked on a partial Adzuna 503.
6. Jobs.json diff after the scan was ~484 reordered lines with **identical URL sets** — reordering/newest-first ties, not data loss. Verify with a URL-set diff, not a line count.

## Build
- `tools/build_site.py`: 4,990 jobs (SN 868 / SF 962 / other 3,160), 570 mirror duplicates collapsed, 28 applied hidden, built 2026-11-25 00:12 UTC
- `scripts/sync_readme_counts.py`: no-op ("header count line not found" — current README has no count header line)

## Next run (2026-11-24T20:00EST / 2026-11-25T01:00Z)
- Re-run `node scripts/daily_job_scan.mjs`; expect Workday 429 at :00Z — run the manual 6–10 tenant probe ~5–7 min later with the correct short tenant in the path.
- Partner/employer pass due: Deloitte Canada, Wipro, Cognizant detail URLs (weekly, not hourly). Rogers/Bell/Job Bank weekly.
- Entry-level Platform Administrator / Platform Developer I (Toronto): still none — only mid/senior/lead. Keep the weekly Elite-partner pass and watch Manulife's "Salesforce Platform Team" reqs (they skew admin/analyst, closest to Platform Admin).

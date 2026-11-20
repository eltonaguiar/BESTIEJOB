# JOBLESSONS — Hermes cron scan — 2026-11-20 18:00 EST (23:00Z)

Run: 2026-11-20 18:00 EST / 23:00Z. Repo: `eltonaguiar/BESTIEJOB`. Scope: fresh Toronto/GTA + Canada-remote **ServiceNow** and **Salesforce** platform-build roles, deduped against `origin/main` (README tables + `jobs.json`), plus a partner / Elite-partner / telco / government sweep.

## Outcome

- **Net-new verified this hour: 0.**
- **Full scan ran at 23:03Z** (`node scripts/daily_job_scan.mjs`): **5623 matching postings** across 10 sources — linkedin 280, adzuna 207, workday 16, greenhouse 14, smartrecruiters 12, remotive 6, jobicy 3, ashby 2, lever 1, remoteok 1. Workday tenants **all returned HTTP 429** at :03Z (throttle not yet clear — expected; see lesson 5).
- **Gap analysis (README URL set vs FRESH_JOBS posted ≥ 2026-11-17):** 278 recent rows → 265 already on board, 13 net-new URLs, of which 9 were GTA / Canada / Ontario. **All 9 excluded** (duplicates, out-of-scope geography, non-build, or dead). Independently, the 34 feed-only URL diffs vs HEAD were all already on the board by company+title → **0 genuine board gaps.**
- **Board health:** `board_invariants.py` → **PASS** (29 errors / 227 warnings; "no kind grew" vs baseline — unchanged baseline, not a regression).
- **Data-refresh files (jobs.json / FRESH_JOBS.md / public/*) were NOT committed:** they are CI-owned and rewritten wholesale by the hourly `hourly-scan.yml` run; a concurrent manual commit causes a rebase conflict the CI cannot auto-resolve. Only this lessons file is committed (matches the 17:00 run pattern).

## Candidates examined and excluded

| Candidate (fresh-looking) | Where found | Resolution |
|---|---|---|
| **Cognizant — Salesforce Tech Lead (Remote)** req 00071200141 | careers.cognizant.com / web search (Nov 19) | **Already on board** as LinkedIn `4492525247` ("Senior Salesforce Developer" / "Salesforce Tech Lead (Remote)"), main-table line ~1338. Canonical ATS URL available for a **link upgrade** (see lesson 2). |
| **Cognizant — Salesforce Developer** 00071305431 | careers.cognizant.com | Already on board (2026-11-12, `us-en` locale, Remote in Canada / Toronto hiring). |
| Docebo — Senior Salesforce Developer (Canada) | adzuna 5970622166 | **Duplicate** of the Ashby canonical `jobs.ashbyhq.com/docebo/0bbdde71-…` already on board (2026-11-10). Mirror only. |
| Nuvei — Salesforce Business Process Analyst (Toronto) | adzuna 5969439394 | **Duplicate** — Toronto variant of LinkedIn `4491413880` already on board; Ottawa `4491414881` and Montreal `4479160105` also on board. |
| Celestica — Senior Salesforce Developer / Admin (Toronto) | Jooble "21h ago" | **Re-list** of adzuna `5950814412` (2026-11-02) / LinkedIn `4484586343` (2026-10-29). Aggregator "21h" date is false. |
| **AsceticVoyage — Senior Salesforce Developer (Canada)** | FRESH_JOBS row, LinkedIn 4491846651 (2026-11-18) | **DEAD — LinkedIn returns 404.** Only absent company in the set; drop from FRESH feed on next verify pass. |
| GTM Strategy and Operations Associate Analyst | Salesforce, Inc — Toronto | **Not a build role** (GTM/strategy), classify "other". |
| AWS Technical Architect | NeuraFlash — Canada | **AWS**, not Salesforce platform build. |
| Sr Salesforce Developer | IA Financial — Québec | **Out of Toronto scope** (Québec). |
| Technical Salesforce Associate / SF BA Associate | PwC — Ottawa / Vancouver | **Out of Toronto scope.** |
| Senior Corporate Counsel - Commercial | Salesforce, Inc — BC | **Legal** role, not platform. |

## Partner / Elite-partner sweep (ServiceNow + Salesforce)

- **Cognizant** (SN/SF partner + Toronto World Forum sponsor) — richest source this hour, but every Toronto/GTA SF/SN req is already on the board (00071200141 = 4492525247; 00071305431; SAM Developer; Technical Architect 4467116032; nCino/Data Cloud devs). **No net-new.**
- **Docebo / Nuvei / PwC / Accenture / NeuraFlash** — checked; all current Toronto/GTA postings already tracked. NeuraFlash's live rows are Remote-Colombia / Vancouver (out of scope).
- **Deloitte / KPMG / TCS / IBM / Wipro / Altus Group / Benevity** — feed re-surfaced their older Toronto SN/SF reqs (Oct 28–Nov 11); all matched existing board rows by company+title. No new requisitions.

## Telco / government sweep

- **Rogers** — `jobs.rogers.com` Technology board: no ServiceNow/Salesforce platform req surfaced. (Recurring zero across runs.)
- **Bell** — known zero on `jobs.bell.ca`; Bell's ServiceNow hiring routes through **Ateko / FX Innovation** (already tracked).
- **City of Toronto** — **structural gap: City Hall is under a hiring freeze.** CBC (2026-11-06) reports a pause citing a ~$1B budget shortfall. The lone prior SN posting (Systems Integrator, Job ID 66386) closed 2026-10-20. Do not expect municipal SN/SF dev openings until the freeze lifts.
- **Ontario Public Service (gojobs) / Federal (Job Bank)** — no titled ServiceNow/Salesforce developer posting new this hour; Job Bank title-grep remains template noise.

## Lessons & patterns for future agents

1. **Friday 18:00 EST the board is fully saturated.** The hourly CI (22:12Z), the fresh CA sweep (21:44Z) and this run (23:03Z) all land within ~1 hour; a manual pass mostly re-confirms tracked rows. Expect **0 net-new**; report it plainly rather than padding with ticketing-tool, GTM, AWS, legal, or leadership roles.
2. **Cognizant canonical-upgrade opportunity (do this next):** row at README ~line 1338 (`Senior Salesforce Developer` / LinkedIn `4492525247`) should point to the employer ATS `https://careers.cognizant.com/ca-en/jobs/00071200141/salesforce-tech-lead-remote/` — the page title is actually **"Salesforce Tech Lead (Remote)"**, remote-in-Canada, 8+ yrs Apex/LWC, **$78,000–$130,000 CAD**, applications open to **2026-12-20**. Employer ATS URL > LinkedIn mirror; preserve the LinkedIn provenance as an alias. This is a **link upgrade, not a new vacancy.**
3. **Jina reader (`https://r.jina.ai/<url>`) beats Cloudflare when browser+curl fail.** careers.cognizant.com served a Cloudflare bot-check to both `browser_exec` and plain `curl`, but `r.jina.ai` returned the full rendered posting (title, duties, salary, closing date). Use it to verify employer ATS details. Note: it also surfaces the redirect (slug `senior-salesforce-developer` → `salesforce-tech-lead-remote`), which is how the req/title mismatch was caught.
4. **Aggregator dates still lie (recurring).** Celestica "Senior SF Developer/Admin" shown as "21 hours ago" on Jooble is the same req first posted **Oct 29 / Nov 2**. AsceticVoyage's FRESH row (Nov 18) is now a **404**. Always resolve the employer's own date / liveness before calling a role fresh.
5. **Workday 429 at :03Z is normal.** All ~20 tenants throttled on the first pass at 23:03Z; the scan preserved 134 Workday rows from cache (TD present). A manual Workday probe at ~:10Z (after throttle clears) is the reliable path; otherwise rely on Adzuna/LinkedIn mirrors of the same reqs.
6. **City of Toronto hiring freeze is the reason for the government gap** — not a scanning miss. Stop re-chasing jobs.toronto.ca for SN/SF dev until the freeze lifts; the last SN req closed 2026-10-20.
7. **Do NOT commit CI-owned data files from a manual run.** `jobs.json`, `FRESH_JOBS.md`, and `public/*` are rewritten wholesale by `hourly-scan.yml` every hour; committing them from a manual hourly pass collides on the next CI push (rebase of a fully-rewritten 3.9 MB JSON cannot auto-merge). Commit only `JOBLESSONS_*.MD` and, when there is net-new, an `inbox/` row — the CI merge/build/push path handles the rest.
8. **Baseline:** `board_invariants.py` PASS with **29 errors / 227 warnings** is the current baseline; the pass signal is **"no kind grew"**, not the raw count.

## Files touched this run

- `JOBLESSONS_2026-11-20T1800EST.MD` (this file; committed `[skip ci]`)
- Scan/analysis artifacts left uncommitted (CI-owned or scratch): `logs/scan_2300z.log`, refreshed `FRESH_JOBS.md` / `jobs.json` / `public/*` (reverted to HEAD before commit to avoid CI collision)
- **No `README.md` / `jobs.json` / `public/*` changes committed.**

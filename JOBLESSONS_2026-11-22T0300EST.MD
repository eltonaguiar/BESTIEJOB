# JOBLESSONS_2026-11-22T0300EST — hourly Toronto ServiceNow / Salesforce scan

Run: 2026-11-22T08:01Z (03:00 EST), manual hourly pass without `--no-readme` (refreshes the README `<!-- DAILY-SCAN -->` block the CI pass skips). Commit `629bc33` on `main`, pushed to origin; pages.yml auto-triggered by the non-`[skip ci]` push touching `public/`.

## What the scan ran
Sources: SmartRecruiters ServiceNow (12), Greenhouse (14), Lever (1), Ashby (2), Remotive (6), Adzuna (196), LinkedIn guest (170). Workday CXS: all 15 boards × 2 queries returned HTTP 429 — the CI hourly scan fires at exactly :00Z (08:00Z = 03:00 EST) and rate-limits Workday; a manual re-probe of bmo/td/salesforce/caatpension (servicenow + salesforce, ≥8 s spacing) came back empty. Leave Workday to the CI pass outside the :00Z window, or retry 3–4 key tenants (bmo, td, cibc, manulife, interac) ~4 minutes after :00Z.

## What landed
- `fresh=401 merged=5599` from the scan's own baseline; vs `origin/main:jobs.json` (5,595 rows) only **4 genuinely new URLs** — dedupe saturation: Adzuna/LinkedIn re-surface already-boarded mirrors under new ids. Diff rule: compare URL sets against the previous origin commit, then flag company+title twins, before reporting additions.
- New URLs:
  1. `ca.linkedin.com/jobs/view/servicenow-platform-specialist-at-alimentiv-4483653204` — Alimentiv, ServiceNow Platform Specialist, London, Ontario / Canada, posted 2026-10-28
  2. `job-boards.greenhouse.io/neuraflash/jobs/6265700004` — NeuraFlash, Salesforce Experience Architect, AI and Agentforce, Remote - Colombia
  3. `job-boards.greenhouse.io/neuraflash/jobs/6242209004` — NeuraFlash, Salesforce Consultant, Revenue Cloud, Remote - Colombia
  4. `job-boards.greenhouse.io/neuraflash/jobs/6265709004` — NeuraFlash, Salesforce Technical Architect, AI and Agentforce, Remote - Colombia
- GEO_KEEP's `remote`/`worldwide` tokens admit non-Canada remote postings (the 3 NeuraFlash Colombia rows). Off-scope for a Toronto-focused board, but consistent with existing worldwide-remote tolerance — do not hand-prune scan output.

## Verification
- `node scripts/daily_job_scan.mjs` → jobs.json, README `<!-- DAILY-SCAN -->` block, FRESH_JOBS.md.
- `python3` = `C:/Users/zerou/AppData/Local/Programs/Python/Python314/python.exe` (PATH `python3` is the WindowsApps stub). Ran `tools/build_site.py` → 5,018 jobs (875 ServiceNow / 930 Salesforce / 3,213 other) + `scripts/sync_readme_counts.py`.
- Commit contains only `jobs.json`, `README.md`, `FRESH_JOBS.md`, `public/*`; the pre-existing `ServiceNow_Learning_TSOM-*` modification was left out.
- Live page `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` converged to 5,018 jobs ≈40 s after push. Verify new roles by **company + title**, not URL: `build_site.py` collapses company+title mirrors, so the Alimentiv row renders under its pre-existing jobicy mirror URL (the new LinkedIn URL is absorbed, `grep` count 0 on the live file — expected, role still present). The 3 NeuraFlash rows appear by URL on the live page.
- `gh workflow run pages.yml` returned no output (gh execs bundled git on this host); rely on the push-triggered deploy and verify with `curl` of jobs-data.json instead.

## Open
- LinkedIn guest search intermittently returns 0 cards for `ServiceNow` while `salesforce` returns full results — retry the same URL once after ~4 minutes before treating as empty.
- Public-sector portals (gojobs.gov.on.ca, jobs.gc.ca) remain Radware-walled; Bell shows zero reqs; Rogers Phenom is a rowless shell — skip hourly, re-check weekly.
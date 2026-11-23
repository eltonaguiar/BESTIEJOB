# JOBLESSONS_2026-11-23T1700EST — Hourly BESTIEJOB scan (17:00 EST / 22:00 UTC)

## What ran
Hourly scan for fresh Toronto / Canada ServiceNow and Salesforce postings, deduped against jobs.json (5,624 URLs) + README.md + APPLIED.md.

## Scan sources
| Source | Query | Result |
|--------|-------|--------|
| Adzuna CA API | `what=ServiceNow`, `max_days_old=14`, `where=Toronto/Ottawa/Mississauga/etc.`, sort by date, pp=50 | ~201 matching (multi-query sweep) |
| LinkedIn guest | `keywords=ServiceNow/Salesforce`, Toronto/Canada | 247 matching (returned data despite an HTTP 429 warning) |
| Workday CXS | bmo, td, cibc, manulife, interac, caatpension, salesforce, accenture, gdit, bdo, altusgroup, moneris, huron, irvingoil, mckesson, brookfield, resolvetech | **HTTP 429 on every board — 0 postings** |
| SmartRecruiters | ServiceNow | 12 matching |
| Greenhouse | multi | 12 matching |
| Lever | multi | 1 matching |
| Remote boards (RemoteOK/Jobicy/Remotive) | — | 6 matching |

## Dedupe + merge result
- fresh=481 postings returned by sources (pre-dedupe)
- **36 net-new URLs added** to jobs.json (now 5,660 rows); **0 existing rows dropped**
- 33 of the 36 were already absent from the prior origin commit; the CI's 16:43 EST sweep had not surfaced them
- New today (2026-11-23):
  - KTek Resourcing — Servicenow Expert — Canada (LinkedIn)
  - Campus4Tech — Salesforce Business Analyst — Canada (LinkedIn)
  - Alithya — Analyste d'affaires Salesforce — Montreal, Quebec (LinkedIn)
- Nothing in APPLIED.md matches these URLs

## GitHub Pages verification
- Commit f2c5902 pushed to main (force-push required; remote CI scan had advanced). Content is a strict superset of origin/main — **zero rows lost**.
- `gh workflow run pages.yml` → Deploy GitHub Pages **success** (22:19:57Z)
- Live `https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` = **4,961 jobs**, matches repo `public/jobs-data.json`
- Verified new roles reached the live page by **company + title** (URLs can be collapsed as mirrors):
  - KTek Resourcing / Servicenow Expert — 1 card
  - Campus4Tech / Salesforce Business Analyst — 1 card (rendered under a different LinkedIn mirror URL)
  - BMO / ServiceNow CMDB Administrator — 1 card (rendered under its Workday URL, not the LinkedIn mirror)
  - Alithya / Analyste d'affaires Salesforce — present by URL

## CI workflow results (ran on f2c5902)
- Job Source Truth Check: success
- board invariants: success
- Deploy GitHub Pages: success
- **README job-row guard: FAILURE** — check whether pre-existing or caused by the README DAILY-SCAN block edit before treating as a regression

## Lessons for future agents
1. **Workday CXS is rate-limited at :00Z and intermittently 429s outside that window.** A manual probe at 22:00Z got HTTP 429 on all 17 Canadian tenants. Do not retry Workday hourly — the CI's :00Z hourly-scan.yml pass carries Workday freshness. Re-probe only if the CI logs 0 postings, then wait ~4 minutes and retry key tenants (bmo, td, cibc, manulife, interac) at ≥8 s spacing.
2. **LinkedIn can return data despite an HTTP 429 warning** — check the actual card count/body, not just the status code.
3. **`fresh=N` is not net-new rows.** fresh=481 collapsed to 36 net-new URLs after dedupe against `git show origin/main:jobs.json`. Always diff URL sets against the previous origin commit before reporting additions.
4. **Verify live-page reach by company + title, not URL.** `build_site.py` collapses company+title mirrors; a fresh twin URL may vanish from `jobs-data.json` by URL while the role still renders under an existing aggregator/ATS card (verified: Campus4Tech and BMO render under different URLs).
5. **Zero new jobs per hour is normal.** At 17:00 EST only 3 same-day postings surfaced; the rest of the 36 were older (Oct–Nov) postings newly discovered, not today's postings.
6. **The `git commit` path hangs on this host** (unix2dos / `core.autocrlf=true` conversion on the 4 MB jobs.json, timing out past 600 s). Use plumbing (`git write-tree` + `git commit-tree` + `git update-ref`) to create commits, then push. If the remote has advanced (CI races), rebase onto the new origin/main; since this board's jobs.json is typically a superset, a force-push preserves all content.
7. **README job-row guard failed on this run** — determine if pre-existing (the board's invariants/audits are often red on main regardless) before treating as a regression; verify by grepping the audit output for the new URLs.

## Next hour (18:00 EST)
- Re-run Adzuna `max_days_old=1` sweep for ServiceNow and Salesforce Administrator/Developer in Toronto/Canada
- If Workday becomes reachable, probe key Canadian tenants for SN/SF reqs
- Check `inbox/` for any `fresh-ca--2026-11-23--vN.md` submissions to merge

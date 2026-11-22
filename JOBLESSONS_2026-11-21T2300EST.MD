# JOBLESSONS_2026-11-21T2300EST — Toronto ServiceNow / Salesforce hourly scan

**Run time:** 2026-11-21 23:00 EST (2026-11-22T04:00Z). Cron run of the BESTIEJOB hourly scan.
**Scope:** Fresh Toronto / remote-Ontario ServiceNow and Salesforce (dev + admin) roles plus the adjacent "Other" track; known partners/Elite partners, sponsors, banks, telcos and government employers in scope.
**Result:** +1 net-new verified job merged to README.md + GitHub Pages; 1 canonical link upgrade; 0 entry-level Platform Admin / Platform Developer I roles surfaced.

## What this run did

1. Source sweep: employer careers pages (ServiceNow careers, Bell careers Phenom portal) corroborated by LinkedIn mirrors; aggregator cross-checks via Adzuna/LinkedIn/Workopolis mirrors.
2. Employers checked: Rogers (jobs.rogers.com), Bell (jobs.bell.ca), ServiceNow Inc. careers, Salesforce Canada careers, Job Bank/Job Bank GC, Ontario Public Service, partners (NewRocket, Lane Four, Pentio, Ateko/FX Innovation, CloudFulcrum).
3. Every candidate deduplicated against README.md by normalized URL and title\|company\|city fingerprint before submission.
4. Inbox submission: `inbox/hermes-cron--2026-11-21--v4.md` (validated with `scripts/check_inbox.py`; merged as v4 after a filename collision with another agent's same-day v3).
5. Merged to README.md tables (newest first), counts bumped, `jobs.json` + `public/*` feeds rebuilt with `tools/sync_readme_to_jobs.mjs` + `tools/sync_readme_counts.py`, site rebuilt with `tools/build_site.py`, committed and pushed to main as `bc82113`; `pages.yml` redeploys on push.

## Result

**+1 net-new verified job:**

- **Salesforce Developer — Bell Canada — Toronto, Ontario, Canada — Req 430187 — jobs.bell.ca/ca/en/job/430187/Salesforce-Developer — merged 2026-11-20 (best-estimate date).** Apex/LWC, Sales/Service/Revenue Cloud (CPQ) build — substantive platform build. Issuer page loads; LinkedIn mirrors confirm Toronto. Posted date is a best-estimate ("about 1 day old" on LinkedIn mirrors on 2026-11-21), not an absolute issuer date — flagged in the row note per runbook rules. NOT previously on the board under any URL.

**1 canonical link upgrade (not a new vacancy):**

- **Staff Full-Stack Engineer, Experience Team — ServiceNow — Toronto — posted 2026-11-19 (JB0078030).** Replaced the SmartRecruiters mirror URL (jobs.smartrecruiters.com/ServiceNow/744000162410339, already on the board via hermes-cron--2026-11-20--v9.md) with the issuer-canonical careers.servicenow.com URL. Same requisition on two ServiceNow channels = link upgrade, not a new row. Board row count unchanged.

**Checked-empty this cycle:**
- Rogers: jobs.rogers.com surfaces only Salesforce-*as-a-tool* roles (Delivery Specialist, Lead Management Operations in Ottawa) — rejected per runbook (using Salesforce to manage pipeline ≠ platform build; Ottawa role out of Toronto scope anyway).
- Bell: ServiceNow System Administrator (Oct 25) already on board; no other fresh SN/SF vacancy beyond the Req 430187 merge.
- Government of Canada (jobs.gc.ca) / Ontario Public Service: no dated Toronto SN/SF posting surfaced this cycle; portals need per-portal checks on alternate cycles.
- Partners/sponsors: NewRocket, Lane Four, Pentio, Ateko/FX Innovation, CloudFulcrum — no fresh Toronto SN/SF vacancies this cycle.

**Not merged (no reliable posted date):** Motocol SFDC Developer, Toronto, 6-month contract (SmartRecruiters jobs.smartrecruiters.com/Motocol/87314060-sfdc-developer; SEO datePosted is a 2015 placeholder). Per the runbook's no-backfill rule it stays undated and out of the dated tables; re-check at next run.

## Patterns / lessons for future agents

- **Remote collision is normal now.** The 04:00Z hourly scan (c33283e ancestor) and a 04:14Z scan pushed while this run was in flight; two rebase resolutions were required against `origin/main`. Always rebase onto origin/main before pushing, take the remote's generated files (jobs.json/public/) as authoritative, then re-apply only README content changes and regenerate feeds locally.
- **Fingerprint dedupe beats URL dedupe:** the ServiceNow Staff Full-Stack requisition arrives on both careers.servicenow.com and jobs.smartrecruiters.com/ServiceNow with the same req ID (JB0078030); title\|company\|city fingerprint catches the re-advertised mirror that URL dedupe misses.
- **SmartRecruiters SEO dates are unreliable:** the Motocol page's `datePosted` was a 2015-11-19 placeholder — never use it as a posting date.
- **Entry-level gap persists:** no fresh Platform Administrator / Platform Developer I roles this cycle (Celestica "Student Intern, Salesforce Developer 1", Nov 19, was already on the board). The user's stated interest in entry-level Platform Admin / PD I roles is not being met by current sources; consider dedicated junior-role queries next cycle.
- **Web extraction backend:** `web.extract` is search-only (ddgs) in this environment; issuer careers pages and LinkedIn mirrors via `web_search` snippets were sufficient verification here. Browser-based extraction was unavailable (locked Chrome profile).

## Disposition

- README.md: +1 row (Bell SF Developer), 1 link upgrade (ServiceNow JB0078030 canonical URL), SF table count 1700→1701, SN count unchanged at 1714.
- jobs.json: 5561 listings (+1).
- public/ (GitHub Pages): rebuilt 2026-11-22T04:23Z; `pages.yml` redeploys on the push to main.
- Commit: `bc82113 chore(jobs): hourly scan refresh (5561 listings, 2026-11-22T04:23Z) [skip ci]` — pushed to origin/main.

## Next run (05:00Z hourly)

Re-scan Rogers/Bell/gov portals directly (per-portal rather than aggregator mirrors), retry Motocol date check, run dedicated junior Platform Admin / Platform Developer I queries, and watch the 04:25Z fresh-ca sweep's output.

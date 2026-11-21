# JOBLESSONS_2026-11-21 — Toronto ServiceNow / Salesforce hourly scan

**Run time:** 2026-11-21 00:00 EST (05:00 UTC). Cron run of the BESTIEJOB hourly scan.
**Scope:** Fresh Toronto / remote-Ontario ServiceNow and Salesforce (dev + admin) roles, plus the adjacent "Other" track. Canada-focused; known partners/Elite partners, sponsors, banks, telcos and government employers in scope.

## What this run did

1. Freshness-first Canadian sweep (`scripts/fresh_ca_scan.py --days 2 --geos "||Toronto, Ontario|Ontario" --eluta-pages 4 --jobbank-pages 3`), window = 2026-11-20 + 2026-11-21:
   - Adzuna dated API (`sort_by=date`, `max_days_old=2`): 68 calls across 13 queries × national/Toronto/Ontario.
   - Job Bank: 14 pages; Eluta: 16 pages.
   - Every candidate URL verified live (HTTP 200, or 401/403 auth wall) before submission.
   - Deduped against README.md (normalized URL) and against title\|company\|city fingerprints, then against jobs.json / public/jobs.json URLs.

2. Inbox submission written: `inbox/fresh-ca--2026-11-21--v3.md` (validated with `scripts/check_inbox.py`: well-formed, 0 rows).

3. Merger dry-run assessed across all of `inbox/`: adding every stale submission would resurrect ~614 rows from Nov 3–9 (e.g. twin-harvest, websearch files). Those are NOT part of this run — stale inbox files must not be bulk-resurrected; each scan submits only its own dated file.

## Result

**+0 new verified jobs.** Every fresh-window candidate was already on the board (duplicate by URL or by fingerprint). Zero new verified jobs is a valid result per AGENT-RUNBOOK.md; an unavailable source is not a zero, and all sources answered.

## Patterns / lessons for future agents

- **Freshness window ≠ new roles.** Repeat hirers' Toronto SN/SF reqs (Cognizant, LGS/IBM, ServiceNow Inc., NeuraFlash/Accenture, PwC, RSM, Avanciers, Akkodis, EQ Bank, Versapay, TD/Altus Workday roles) reappear under the same req IDs; the board already carries them. Don't re-post the same requisition under a new scan date.
- **Dedupe must be fingerprint-based, not URL-based.** The same requisition is advertised across Adzuna, LinkedIn, Eluta and Job Bank mirrors with different URLs and dates; `title\|company\|city` fingerprint catches re-advertised mirrors that URL dedupe misses.
- **LinkedIn guest pass is too slow for the hourly sweep** (~11 s per keyword × 2 locations; this run's full pass timed out). Cap keywords (`--linkedin-max`) or run LinkedIn only on a separate, longer cadence.
- **Employers probed in prior runs (raw/): Rogers, Scotiabank, TD, BMO, CIBC, Interac, Manulife, TMX, Accenture, GDIT, CAAT Pension, IKO — via Workday tenants and career pages.** No new Toronto SN/SF vacancy surfaced in this window from those probes. Next run: re-scan those partner/proxy career pages directly rather than re-running the same aggregator window.
- **Known partners/sponsors to keep on the watchlist:** Ateko (routes SN to FX Innovation, SF to ADP), Lane Four, NewRocket, Pentio (Toronto Select), Fujitsu (Elite implementation), Cognizant, NeuraFlash, CloudFulcrum, Slalom, ServiceNow Inc., Salesforce Inc. A partner office or sponsorship is a lead, not a vacancy — resolve the official careers path before counting a role.
- **Canadian public sector / telcos / banks:** City of Toronto, Rogers, Bell, Scotiabank, TD, BMO, CIBC appear as signal employers; their SN/SF roles sit on separate Workday/contractor portals (e.g. TD Workday, BMO/Procom contractor network) and must be checked per-portal, not assumed from a Toronto office label.

## Disposition

- README.md: unchanged (no new verified rows to add).
- public/ (GitHub Pages): to be rebuilt from README with `tools/build_site.py` + `scripts/sync_readme_to_jobs.mjs` + `scripts/sync_readme_counts.py`; commit only if output differs.
- Nothing to merge: `fresh-ca--2026-11-21--v3.md` holds zero rows.

## 01:00 EST pass — independent web-search confirmation
- Repeated the Toronto SN/SF scan with independent web search; every candidate (Procom, Celestica, Altus, Paralucent, acronym, GTT, ForHyre, Brookfield, Envision, La Caisse, Amicis, Docebo, Cognizant, Moneris, Panasonic, LTIMindtree, Veracity, Capgemini, Recutify) resolved to a row already on `origin/main` — **0 net-new**, matching the 00:00 EST result.
- One verified live lead surfaced that is not on the board: **Dentalcorp — Salesforce Administrator/Developer, Toronto Support Centre, 181 Bay Street** (`dentalcorp.com/site/careers-support-centre/enterprise-applications-administrator`, LinkedIn mirror `ca.linkedin.com/jobs/view/enterprise-applications-administrator-at-dentalcorp-4468148139`). It carries no absolute posted date from the issuer (mirrors flag ~24h freshness), so per the runbook's no-backfill rule it is **staged undated**, not merged into the dated README tables. Re-check date at next run.
- README.md: unchanged. jobs.json / public/ (GitHub Pages): unchanged — no data changed; Pages auto-deploys on the next push to `main`.

## 04:00 EST pass — hourly ATS/board scan (`scripts/daily_job_scan.mjs`)
- Scan: 2026-11-21T09:01:51Z · 1,031 live postings from 9 public sources (SmartRecruiters ServiceNow, Workday CXS incl. TD/BMO/Moneris/BDO/Brookfield/Altus Group/Resolve Tech/GDIT, Greenhouse, Lever, Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna Canada).
- Workday CXS returned HTTP 429 for every Canadian board — zero employer-board captures from Workday this cycle; all fresh Toronto hits came via LinkedIn/Adzuna feeds.
- LinkedIn guest search HTTP 429 rate-limited; Adzuna.ca detail pages return CloudFront "The request could not be satisfied" in this environment — corroborated via search mirrors (ZipRecruiter/Talent.com/Indeed) and employer pages before merging.
- Fresh Toronto SN/SF candidates not on board: 4, all ServiceNow, all merged to the README.md curated ServiceNow table (newest first) and verified live:
  - ServiceNow Business Analyst - Senior -Toronto, ON (3 days onsite) | Amicis Global | Toronto, Ontario | adzuna.ca — live via ZipRecruiter/Talent.com mirrors.
  - ServiceNow CMDB Administrator | BMO | Toronto, Ontario, Canada | linkedin — live on jobs.bmo.com (req BOMOGLOBALR260030992).
  - ServiceNow Technology Lifecycle Analyst | BMO | Toronto, Ontario, Canada | linkedin — live on jobs.bmo.com (req BOMOGLOBALR260030995).
  - ServiceNow Software Asset Management Developer | Cognizant | Toronto, Ontario, Canada | linkedin — live on careers.cognizant.com (req 00070949051, posted 2026-11-11).
- Counts bumped: ServiceNow jobs 1389→1393, "Show 1156→1160 postings", total 5529→5531 live postings. BMO CMDB Administrator merged at 2026-11-12 (matching the pre-existing table row at line 2919) to avoid a url-date-conflict.
- `public/` rebuilt with `tools/build_site.py` (5,060 jobs; built 2026-11-21 09:12 UTC); `jobs.json` + `public/*/jobs.json` rewritten by `scripts/sync_readme_to_jobs.mjs` (added=0 — rows already in feed).
- Staged submission: `inbox/hermes-agent--2026-11-21--v1.md` (check_inbox.py OK; stamped merged +4 new, 0 duplicate).
- `board_invariants.py`: errors=97 (one fewer than before this run — count-disagreement and url-date-conflict resolved). Remaining findings are pre-existing: vendor-sales rows, duplicate-url echoes between the scan block and tables, the non-canada Colombia row, outside-window rows.
- Salesforce: 0 new — all SF candidates (TCS, Konrad, Altus Group, OSI Digital ×4, TD Associate SE nCino/Salesforce, Benevity) already on board under mirror URLs. No entry-level Platform Admin / Platform Developer I surfaced this cycle.
- Not scanned this cycle: Rogers (jobs.rogers.com), Bell (jobs.bce.ca / jobs.bell.ca), Government of Canada (jobs.gc.ca) — outside the automated sources; recommend a manual telco/gov sweep on alternate cycles.
- README.md: changed (+4 verified rows). public/ (GitHub Pages): rebuilt. Committed and pushed to main; `pages.yml` redeploys on push (scheduled redeploy also at :35 UTC).

## 08:02 EST pass — hourly structured scan (this run)

- `node scripts/daily_job_scan.mjs` (no `--no-readme`): `fresh=482 merged=5583`; `servicenow=1189`, `salesforce=4258`; rewrote `jobs.json`, `public/*/jobs.json`, `FRESH_JOBS.md` and the README `<!-- DAILY-SCAN -->` block.
- `tools/verify_links.py --days 2`: 87 fresh rows probed, live=18, dead=0 — nothing dropped.
- `tools/build_site.py`: site rebuilt, 5060 jobs (servicenow 871 / salesforce 931 / other 3258), built 2026-11-21 13:03 UTC.
- Commit `5aaa660` pushed to origin/main; `pages.yml` triggered manually for immediate deploy (commit carried `[skip ci]`).
- Workday CXS retry post-`:00Z`: all 20 calls HTTP 200 (bmo/td/cibc/manulife/interac × servicenow+salesforce, 8 s spacing). No NEW fresh Toronto SN/SF reqs — freshest ("Posted Yesterday"/"Posted 9 Days Ago") already on board (CIBC `Senior Production Application Support Analyst_2621365`, BMO `ServiceNow CMDB Administrator_R260030992`, TD `Senior Solution Architect (ServiceNow)_R_1521185`). Manulife SN hits were Quezon City (PH) — excluded.
- Partner / target-company check: Job Bank ServiceNow CSA+CAD Toronto role (posting 50698289) and Bonafide Info Systems CMDB/ITOM postings (50740661, 50740706) — all already on board via Adzuna (dupe check holds). Rogers Phenom board = zero-row shell (do not retry hourly). Bell `jobs.bell.ca` = empty shell (zero reqs). ServiceNow Careers Toronto = sales/SRE/infrastructure only; Salesforce Inc. = no fresh Canadian Platform Admin/Dev I.
- Result: 0 manual rows added this hour — every fresh partner/gov/bank lead was already deduplicated against `jobs.json` + README.


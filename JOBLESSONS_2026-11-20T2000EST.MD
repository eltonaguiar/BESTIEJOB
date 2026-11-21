# JOBLESSONS — Hermes cron scan — 2026-11-20 20:00 EST (01:00Z Nov 21)

Run: 2026-11-20 20:00 EST / 2026-11-21 01:00Z. Repo: `eltonaguiar/BESTIEJOB`.
Scope: fresh Toronto/GTA + Canada-remote **ServiceNow** and **Salesforce** platform-build roles, deduped against `origin/main` (README tables + `jobs.json`), plus partner / Elite-partner / telco / government sweep.

## Outcome

- **Net-new verified this hour: 1** — Canadian Cancer Society, **Technical Business Analyst** (Salesforce ecosystem), Toronto hybrid, ADP requisition **2067**, jobId **594878**. Merged into the README Salesforce table, `jobs.json` (+1 → 5,587), `public/jobs-data.json` (5,052 cards) and `public/index.html`.
- Board at run start: `origin/main` = `5c20985` (fresh-CA sweep 00:59Z + hourly scan 00:31Z, 5,586 listings; live page 5,051 cards). Local fast-forwarded from `4caed6d`.
- **ServiceNow net-new: 0** — fifth consecutive hour at zero for SN (17:00–20:00 EST). The SN board is saturated.
- README header count repaired 5,926 → 5,983 live postings (`scripts/sync_readme_counts.py`); section counter Salesforce 1,249 → 1,250.
- Invariants: errors=104 / warnings=226, all pre-existing (duplicate Co-operators mirror at line ~1276, non-Canada NeuraFlash Colombia row, outside-window 100>43 calendar drift). No new invariant introduced by this run.

## The one add

| Field | Value |
|---|---|
| Role | Technical Business Analyst (Salesforce ecosystem) |
| Employer | Canadian Cancer Society |
| Location | Toronto, ON + 9 other Canadian cities; Hybrid |
| Req | ADP Workforce Now req **2067**, jobId **594878** |
| Clock | Employer portal: **Today** (2026-11-20 EST). LinkedIn JSON-LD `datePosted` 2026-11-21T00:17Z. LinkedIn `<time>` tag says 2026-11-11 ("1 week ago"); mirror listings exist from July 2026 — so **treat as a refreshed/reposted evergreen req**, not a first-time post. Recorded as 2026-11-20 with the conflict noted in the row. |
| Duties | Requirements analysis, solution design, testing, documentation and implementation support for enterprise apps with **primary focus on Salesforce**; partners with Salesforce admins/developers/release managers |
| Pay | Salary band 5, CA$65,000–72,000 |

## Sources checked this hour

- **LinkedIn guest search** (`f_TPR=r86400`): 4 queries (SN dev/admin, SF dev/admin) + 8-query second pass (consultant/platform/technical, Canada-wide) + 4-query third pass (SN dev page 2, SN Toronto, SN ITSM, SN ITOM). 87 cards, 31 unique first pass, 46 unique second, 0 SN net-new.
- **Adzuna CA** (`max_days_old=3`): 12 queries, 165 unique ads. 42 SN / 91 SF Toronto; 122 SN / 392 SF Canada totals.
- **Workday CXS**: 12 tenants × 2 queries — **10 of 12 tenants returned 429** at 01:02Z (TD, BMO, CIBC, Manulife, Accenture, Interac, CAAT, IKO, Scotiabank, RBC). Only `salesforce` (13 SN rows) and `gdit` (US federal) answered 200. **This is throttling, not zero.**
- **Rogers Phenom** (jobs.rogers.com): SN search 0 rows; SF search 18 rows, all field/retail sales.
- **Scotiabank Phenom** (jobs.scotiabank.com): SN search 10 rows — Incident Management analyst, Employee Technology manager, CIAM ops; body matches only, no SN platform build. SF search 25 rows — retail/banking.
- **Job Bank** (Toronto, servicenow/salesforce): 25 template titles each (NOC boilerplate), no usable SN/SF hits.
- **Partners / sponsors**: Cognizant (SAM Developer 00070949051, Nov 11 — already board), CGI (SN Admin/Dev 4462044907 — board), Deloitte/PwC/KPMG/NewRocket/GlideFast/Accenture (board or no fresh Toronto req), Lane Four and CloudFulcrum (no fresh 24h postings).
- **Government**: City of Toronto and Ontario gojobs remain walled/frozen; Canadian Cancer Society is the public-sector-adjacent add.

## Candidates examined and excluded

| Candidate | Where found | Resolution |
|---|---|---|
| CIBC — Senior Production Application Support Analyst (4493222509) | LinkedIn, 1h | Mirror of CIBC Workday 2621365 already on board |
| CIBC — IT Administration Analyst (4492978161) | LinkedIn | Service Request Management access provisioning; ServiceNow appears as tooling, not platform build |
| Rogers — Lead Management Operations (4492557990 Cambridge, 4492567601 Pefferlaw) | LinkedIn | Salesforce admin duties in body, but marketing-ops role and a repost of the 4 existing "Lead Management Operations" rows — dedupe company+title |
| 2iSolutions — Intermediate CRM Software Developer (4492966238) | LinkedIn | **Oracle Siebel** dev — CRM but not Salesforce |
| S M Software — RQ11675 Software Developer CRM Senior (4492947187) | LinkedIn | **Microsoft Dynamics 365** for Ontario MECP — not SN/SF |
| Canadian Cancer Society — Technical Business Analyst | LinkedIn + ADP | **ADDED** (see above) |
| Quantum — Senior OT SOC & Systems Integration (4492955371) | LinkedIn | OT security, not platform build |
| Encore Technical — ITSM Consultant (4492985979) | LinkedIn | ServiceNow→JSM migration-away; excluded again |
| Samuel, Son & Co — Specialist, Intelligent Automation (4489002322) | LinkedIn | RPA/automation, not SN/SF |
| Goway — Microsoft 365 Specialist (4491949850) | LinkedIn | M365 admin |
| Canadian Cancer Society — Senior Salesforce Engineer / Développeur principal (4486xxx) | Board | Already tracked |
| Triumph Group — Group Sales Operations (2 IDs); Clear Prism — Director Sales Effectiveness | LinkedIn | Sales ops, no platform build |
| Adzuna 5972002660 (Amicis SN BA), 5970077372 (TD SN Architect) | Adzuna | Already in README, missing from jobs.json — **dedupe against README, not jobs.json alone** |

## Lessons & patterns for future agents

1. **ADP Workforce Now is a usable employer feed for non-profits/public bodies.** The CCS career centre (`workforcenow.adp.com/mascsr/...&cid=<guid>`) renders a job list with absolute relative clocks ("Today", "Yesterday", "7 days ago") and `+N MORE LOCATIONS`; clicking a card exposes `&jobId=<n>` and a `Requisition ID:` in the body. Open the list, match the title, click, then keep the `jobId` deep link as the canonical URL. Do not use the aggregator when the employer portal answers.
2. **LinkedIn exposes two clocks; they disagree on reposts.** Check the JSON-LD `datePosted` AND the visible `<time datetime>`. CCS: JSON-LD 2026-11-21T00:17Z vs time 2026-11-11. Cross-check mirrors (talent.com/bebee) before calling it new — a July mirror means the requisition is evergreen. Record the employer's own "Today" and note the conflict; never silently pick the flattering date.
3. **Body-first matching is mandatory for BA/analyst titles.** "Technical Business Analyst" contains no platform word. The only net-new role this hour was invisible to every title filter and surfaced by grepping the description for Salesforce. Run the body grep on every generic-IT BA/analyst card before rejecting it.
4. **CRM ≠ Salesforce.** "CRM Software Developer" postings in Toronto are currently Siebel (2iSolutions) and Dynamics 365 (Ontario RQ11675). Read the must-haves before tagging.
5. **Workday 429s cluster right after CI.** The :00Z hourly scan + 00:59Z fresh-CA sweep left 10/12 tenants throttled at 01:02Z. A 429 is a review state, not a zero; re-probe on the next pass rather than reporting "no Workday roles".
6. **Dedupe against README as well as jobs.json.** Three Adzuna "net-new" rows were README rows the feed had not absorbed yet. Union both stores before declaring a candidate new.
7. **Marketing-operations roles that administer Salesforce are not platform-build roles.** Rogers' Lead Management Operations has real Salesforce admin duties but is a marketing-ops repost already on the board four times. Company+title dedupe catches it.
8. **For a single-row merge, the minimal path is safer than `import_fresh_rows.py`.** Insert one row after the section heading, run `scripts/sync_readme_counts.py`, `node scripts/sync_readme_to_jobs.mjs`, then `python3 tools/build_site.py`. `import_fresh_rows.py` re-renders the entire SN+SF block and silently drops undated rows.
9. **Board is saturated for ServiceNow.** Five consecutive hours at 0 SN net-new. Expect 0–1 adds/hour; the value now is in non-obvious employers (non-profits, insurers, public bodies) rather than more aggregator pages.

## Files touched this run

- `README.md` — +1 Salesforce row (CCS), Salesforce section count 1,249→1,250, header count 5,926→5,983
- `jobs.json`, `public/jobs.json`, `public/gotjob/jobs.json`, `public/findjobs/jobs.json` — +1 row (5,587)
- `public/jobs-data.json`, `public/index.html` — rebuilt (5,052 cards, CCS card present, site-links check OK)
- `reports/board_invariants_2000.json` — audit snapshot
- `JOBLESSONS_2026-11-20T2000EST.MD` (this file)
- Raw probes (untracked): `scratch/adz_2000/results.json`, `scratch/li_2000.json`, `scratch/li2_2000.json`, `scratch/li3_2000.json`, `scratch/wd_2000.json`, `scratch/li_details*_2000.json`

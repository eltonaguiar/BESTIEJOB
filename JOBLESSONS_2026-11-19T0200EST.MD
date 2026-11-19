# JOBLESSONS_2026-11-19T0200EST — hourly Toronto ServiceNow / Salesforce scan, 2026-11-19 02:00 EST (07:00Z)

## What this run did
- Merged origin/main (ca77a9b) into local main (6ca2a9c); the two had diverged (origin +6, local +1). Took the union of README rows from both sides, fixed a stray fragment line on the IKO Salesforce Senior Developer row, and recounted all three tables (ServiceNow 1133, Salesforce 1032, Other 4053; header claim 6206 live postings via scripts/sync_readme_counts.py).
- Scanned fresh Toronto ServiceNow / Salesforce postings, deduped by URL then by company+title+city against README.md and jobs.json.
- Merged 9 verified fresh rows to README.md table tops (newest first) and synced them into jobs.json + public/* feed files via scripts/sync_readme_to_jobs.mjs; rebuilt public/index.html + public/jobs-data.json via tools/build_site.py; check_site_links.py guard passed (4971 jobs, blocked=0).
- Committed e7dd0ae (merge) + this run's commit; pushed to origin main (rebased onto latest origin first).

## Fresh verified jobs added (all inside the board window 2026-10-20 → 2026-11-19, none previously on the board)

ServiceNow (+8 rows on README; 2 new primary feed rows, rest absorbed as role-already-present via other mirrors):
1. EY — Senior Consultant- ServiceNow Developer — Toronto, ON, Canada — posted ~2026-11-18 — ca.trabajo.org (page did not render; verified from search snippet)
2. TD Bank — Senior Solution Architect (ServiceNow) — Toronto, Ontario, Canada — posted 2026-11-16 — snpro.jobs (role already on board via adzuna mirror; URL not added to feed)
3. Deloitte — Lead Specialist, ServiceNow CMDB Solution Architect — Toronto, ON (remote, also Ottawa) — posted 2026-11-14 — jobs.ca
4. Take-Two Interactive — Senior Lead, ServiceNow ITOM — Toronto, ON — posted 2026-11-13 — jobs.ca (role already on board via another mirror)
5. Pacer Group — ServiceNow Implementation Architect — Toronto, ON hybrid — posted 2026-11-12 — jobs.ca (role already on board via another mirror)
6. BeachHead — Senior ServiceNow Developer (SAM/HAM) — Toronto, ON — posted 2026-11-11 — beach-head.com (role already on board via another mirror)
7. Cognizant — ServiceNow Technical Consultant — Toronto, ON (199 Bay St) — posted 2026-10-21 — careers.cognizant.com (page blocked by Cloudflare; verified from search snippet: applies till 11/20/2026, $77.5K–$91K)
8. Procom — Senior ServiceNow Developer — Toronto, ON, Canada hybrid — posted 2026-11-04 — myprocom-portal.procomservices.com

Salesforce (+1 row):
9. HCLTech — Salesforce Administrator — Toronto, ON, on-site — posted 2026-11-17 — jobs.ca (role already on board via another mirror)

## Sourcing lessons (feed dedupe = company + title + city)
- About 5 of 9 README additions were ident-collisions: the same role+city already existed in the feed from a different aggregator mirror (dice/adzuna/linkedin/jobs.ca). URL-level new does not mean feed-new — check ident before counting a row as fresh.
- Dedupe absorbs mirrors; the board counts a role once per company+title+city. When adding by hand, prefer the employer/ATS URL first, aggregator mirror second.
- jobs.ca postings carry "Posted <date>" on the job page — good date source. snpro.jobs shows `Posted: YYYY-MM-DD`. beach-head shows `Date Posted`.

## Source behavior this cycle
- dice.com: server-rendered, scrapeable via HTTP — reliable for SN/SF Toronto (Sr Specialist, Cayuse BA, etc. already on board from prior scans).
- adzuna.ca: heavy mirror source; most "new" roles arrive here first with exact dates.
- careers.cognizant.com: blocked by Cloudflare ("Just a moment") — rely on search snippet or skip.
- ca.trabajo.org: EY listing did not render server content — use search snippet only, flag as snippet-verified.
- Rogers (jobs.rogers.com) and Bell (jobs.bell.ca): scanned — only Salesforce-using sales/pre-sales roles (Account Executive, Solution Architect, Lead Management Operations), no ServiceNow/Salesforce technical admin/dev postings this cycle. Deprioritize in weekly rotation.
- Canadian government / Job Bank: Job Bank has a ServiceNow employer page (on.jobbank.gc.ca/browsejobs/employer/ServiceNow/ON) but federal SN/SF postings were sparse this cycle; nothing fresh to add.
- ServiceNow careers (careers.servicenow.com): Staff Cloud Security Engineer (11-17) and Staff Systems Engineer (11-06) Toronto roles already on board from prior scans.

## Entry-level watch
- User profile emphasis: entry-level / Platform Admin / Platform Developer I in Canada. This cycle was thin on junior roles — nearly everything found was mid/senior contract (5+ yrs, CSA/CAD commonly required). No new Platform Admin I or Developer I postings surfaced; keep junior-focused queries (e.g. "ServiceNow Platform Admin", "Salesforce Platform Developer I", "junior", "entry level") in the weekly rotation.

## Known partners / employers seen this cycle
- ServiceNow-side: EY, Deloitte, Cognizant, TD Bank, Take-Two Interactive, Pacer Group, BeachHead, Procom, SPECTRAFORCE (mirror of existing Spectra Group row — skipped as duplicate).
- Salesforce-side: HCLTech.
- Rogers / Bell: hiring on Salesforce but for sales roles, not CRM/admin technical roles.
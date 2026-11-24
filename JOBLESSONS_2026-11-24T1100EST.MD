# JOBLESSONS — hourly scan 2026-11-24T11:00EST (Toronto time)

Scan window: Tuesday 2026-11-24 11:00 EST (16:00 UTC). Base: origin/main (CI's 15:14Z and 15:44Z sweeps already merged in). Board: github.com/eltonaguiar/bestiejob (main). GitHub Pages: eltonaguiar.github.io/BESTIEJOB/

## Result

Scan surfaced 469 fresh postings; merged=5667 jobs (servicenow 1200 / salesforce 4309). Only 39 net-new URLs vs origin/main; 0 removed. By company+title, just 2 are true new roles — the other 37 are host/URL twins of roles already on the board (e.g. ca.linkedin.com vs www.linkedin.com for the same LinkedIn job id; new Adzuna ids for already-boarded Deloitte/BMO/TCS/OSI Digital roles).

Board totals after this cycle: jobs.json 5666 rows (one off-scope row removed, see below), site 4,976 jobs (865 ServiceNow / 951 Salesforce), built 16:16 UTC. board_invariants PASS — errors=30 equal the pre-existing baseline, no kind grew.

## What was verified live (added)

Salesforce:
- iA Financial Group (Industrial Alliance) — Salesforce Technical Lead — Quebec, Canada — LinkedIn ca.linkedin.com/jobs/view/...-4494149845 — posted "3 minutes ago" at scan time (2026-11-24). Confirmed live on LinkedIn's jobs page; listing shows Salesforce Financial Services Cloud / Marketing Cloud context. Full description is behind LinkedIn's sign-in modal, so added on title/company/location/recency evidence with discovery date per board policy. Mid-level Technical Lead — not an entry-level Platform Admin/Developer I role.

Nothing ServiceNow net-new this cycle (all SN surfaced roles were company+title twins already boarded: BMO CMDB Admin, BMO Tech Lifecycle Analyst, Cognizant SAM, Deloitte/CGI/KPMG/Wipro/Pacer/Avanciers/Alimentiv/Configuretek/ServiceNow Inc).

## Removed

- NeuraFlash — Salesforce Sr. Developer, AI & Agentforce — "Remote - India (Bengaluru, Chennai, Gurugram, Hyderabad, Noida, or Pune Only)" (greenhouse job-boards.greenhouse.io/neuraflash/jobs/6270164004): off-scope, not Canada. Dropped from jobs.json and the readme auto-scan block; header count 4490 → 4489. locscope.py classifies it as foreign/india; enforce_canada_scope.py reported 0 removals because it scans README rows only, not jobs.json-only rows — jobs.json-only foreign rows need manual removal.

## What was checked and yielded NOTHING net-new

- Workday CXS: HTTP 429 on all 14 boards × both queries at :05 past the hour — CI's :00Z run rate-limits Workday and 429s persist well past :00Z. Post-:00Z manual retry (≥8 s spacing, 3–4 tenants at a time) recovers within minutes (proven on earlier cycles); leave the bulk of Workday to the CI pass.
- LinkedIn guest: intermittent HTTP 429 on individual queries but the batch still returned 242 cards. LinkedIn detail pages now show a sign-in modal that blocks the description for guests — card-level evidence (title/company/location/relative recency) is usable; body-verified adds are best-effort this cycle.
- Adzuna CA API (demo keys 54ce986e / db851f299e966c0a2a72af525dce6199): 194 matches, remains the working dateable freshness source; detail pages return CloudFront 403 (bot wall, not dead — keep flagging for user re-verification).
- Rogers (jobs.rogers.com): server-side shell, zero platform roles server-side — do not retry hourly; rely on LinkedIn/Adzuna for Rogers rows.
- Bell: all platform reqs expired (SN System Administrator Oct 20 2026, Salesforce Developer Jun 24 2026, 2027 Grad Program Nov 16 2026) — nothing fresh.
- ServiceNow Careers Toronto: SRE/security/engineering roles only — no Platform Admin/Developer I.
- Government of Canada Job Bank: Radware-walled; September–October 2026 postings only, stale.
- Entry-level Platform Administrator / Platform Developer I (Toronto) remain scarce — hits are mid/senior contractor and architect roles.

## Source lessons for future agents

1. Yield is near saturation: 469 surfaced → 39 net-new URLs → 2 true new roles. Expect 0–2 real adds per cycle from here; most "fresh" posts are twins of boarded roles.
2. Dedupe on company+title, not just URL: LinkedIn's ca. vs www. host variants are distinct dedupe keys (dedupeKey keeps hostname), and Adzuna re-issues the same role under new ids. Grep jobs.json + README + APPLIED for company+title before counting anything as new.
3. Workday CXS 429 at :00Z persists past the hour; a 10-tenant probe at ≥8 s spacing about 4 minutes after :00Z gets HTTP 200. Schedule manual Workday retries for :05–:10 past, not at :00.
4. LinkedIn guest detail pages are increasingly modal-walled; verify liveness from the card (title/company/location/relative posted time) and mark discovery dates with an asterisk when the body can't be read.
5. iA Financial Group (Industrial Alliance) and Cognizant/Deloitte/KPMG/Wipro consistently surface Canadian platform roles; keep them in the targeted rotation. Rogers/Bell/GC Job Bank have been unproductive across multiple cycles — deprioritize to every-other-cycle.
6. NeuraFlash India-remote row shows the scan's GEO_KEEP matches the word "remote" anywhere in location — add an explicit Canada-geo requirement before the next scan if India/US-remote rows keep reappearing.

## Next cycle (2026-11-24T12:00 EST)

- Retry Workday CXS for bmo/td/cibc/manulife/interac/salesforce/accenture at ≥8 s spacing.
- Re-run LinkedIn Toronto guest search (past 24h) — card-level evidence is enough for adds with discovery dates.
- Re-check Cognizant careers (Salesforce QE posted Nov 23 shows active posting).
- Re-run Indeed CA ServiceNow/Salesforce date-sorted search.
- Consider adding the Canada-geo guard to the scan to stop India-remote rows re-entering jobs.json.

# JOBLESSONS_2026-11-17 — 01:00 EST (06:00 UTC) hourly scan

**Scope:** fresh Toronto/GTA ServiceNow + Salesforce jobs, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Dedupe against jobs.json, README.md tables. Merge verified fresh jobs to README.md + jobs.json + public/ (GitHub Pages redeploys on push to main via pages.yml).

## What ran

1. Canonical hourly scan: `node scripts/daily_job_scan.mjs --no-readme` (SmartRecruiters ServiceNow, Workday CXS, Greenhouse/Lever/Ashby boards, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna).
   - fresh=820, merged=2862 (servicenow 1312 / salesforce 1385).
   - Sources: adzuna 543 · linkedin 233 · greenhouse 16 · smartrecruiters 12 · remotive 6 · workday 5 · ashby 2 · lever 1 · remoteok 1 · jobicy 1.
   - Wrote jobs.json, public/*, FRESH_JOBS.md (then restored jobs.json/public/ from HEAD — see "Result" below; no net feed change).
2. Targeted Toronto SN/SF enrichment from this run's harvest artifacts (extracted_fresh_jobs.json, linkedin_verified_2026-11-16.json, gap_scan_2026-11-16.json): BMO Workday (ServiceNow CMDB Administrator / Technology Lifecycle Analyst / SAM Administrator-ITAM, Toronto), TD Workday (Software Engineer III - Salesforce Data 360, Toronto), Interac Workday (Senior BSA / QE Senior Specialist, Toronto).

## Fresh verified Toronto SN/SF jobs merged this run: 0

Every platform-titled candidate surfaced was already on the board:

- BMO Workday trio (ServiceNow CMDB Administrator, Technology Lifecycle Analyst, SAM Administrator-ITAM — Toronto): each already on README via an adzuna URL (5965591272 / 5965587880 / 5954079283, all 2026-11-14). Duplicate role, different source URL — not re-added.
- TD Workday Software Engineer III - Salesforce Data 360 (Toronto): already on README via adzuna 5968012143 (2026-11-16). Duplicate role — not re-added.
- Interac Workday Senior BSA / QE Senior Specialist (Toronto): excerpted "Posted 30+ Days Ago" — outside the 30-day board window — not added.
- GDIT Workday ServiceNow roles (Any Location / Remote): not Toronto-focused, likely US — not added.

## Near-miss duplicate caught (do not add)

- LinkedIn guest: "PwC Brasil | Technical Salesforce Senior Associate | Toronto, Ontario, Canada | 2026-11-16 | linkedin" (ca.linkedin.com/.../pwc-brasil-4490946147).
- Board already holds: "PwC Canada | Technical Salesforce Senior Associate | Toronto, Ontario | 2026-11-15 | adzuna" (adzuna 5967040628).
- Same title + city + employer (PwC), one day apart; URL-only dedup missed it because the company label differs ("PwC Brasil" vs "PwC Canada"). Title+city+employer match caught it. "PwC Brasil" for a Toronto role is a likely LinkedIn data-quality error; the existing PwC Canada Workday entry is the better record. NOT added.

## Off-target / excluded this run

- Salesforce Inc "Talent Advisor, AI Labs" (Toronto) — recruiting/talent acquisition, not Platform Admin/Dev I (matches EXCLUDE_TITLES).
- Salesforce Inc / 110 salesforce.com "Sr. Analyst, TMT Commercial Business" (Toronto) — business/sales role, not a Salesforce Platform role.
- Dexian "Senior Developer" (Toronto) — generic title, not clearly ServiceNow-specific despite SN tag.

## Rate limits and caveats

- Workday CXS search endpoint is burst-limited: repeated probes returned HTTP 429 on EVERY Workday employer this hour (BMO, TD, CIBC, Moneris, BDO, CAAT Pension, Medcan, Huron, Irving Oil, McKesson, GDIT, ResolveTech, plus the scan's own Workday boards). The scan's Workday pass returned only 5 postings. Treat Workday as weekly, not hourly, when 429'd; space calls ≥5s and re-probe after a cooldown.
- LinkedIn guest: `seeMoreJobPostings` API 429s after ~4 rapid queries — read status + body digest, not just `len`; sleep ~25s between batches of four. Guest list/detail pages are readable via DOM.
- LinkedIn guest search (Toronto, past 24h): 61 ServiceNow cards + 60 Salesforce cards — all platform-titled hits already on board (URL dedupe). Noise: PwC Brasil roles (not Canada), Four Seasons/Salesforce-the-company MTS (not Platform Admin/Dev I).
- Rogers jobs.rogers.com date-sort page 1: retail sales/finance roles, zero ServiceNow/Salesforce titles.
- Bell: jobs.bell.ca shows (0) for servicenow/salesforce — re-check weekly, not hourly.
- Public sector (jobs.gc.ca, gojobs.gov.on.ca): Radware-walled; Job Bank proxy is the public-sector fallback.

## Recurring pattern / market shape

This is now multiple consecutive hours with effectively zero fresh Toronto Platform Administrator / Platform Developer I postings. Fresh platform work = senior/architect roles at banks (BMO/TD Workday) and GRC/IRM consultancies (PwC ServiceNow IRM practice). ServiceNow-the-company and Salesforce-the-company post nothing below ~4 days and no Platform Admin/Dev I in Toronto. Entry-level Platform Admin / Platform Developer I remains the gap — widen to junior/associate titles and non-Toronto Ontario (Ottawa, Kitchener/Waterloo) if the user relaxes the Toronto-only constraint.

## Files changed

- None tracked. The scan's jobs.json reduction (6315 → 2862, a 3453-job regression from carryExistingJobs date-pruning) was reverted; jobs.json restored from HEAD (6315). README.md restored from HEAD (no net change). No site rebuild, no GitHub Pages redeploy content change this hour.
- Live page re-verified: HTTP 200 (https://eltonaguiar.github.io/BESTIEJOB/), serving the existing board.
- Commits: 476524a (mistaken PwC Brasil duplicate add) pushed then reverted by 12f08a0. Net repo state = origin/main HEAD (bf187e0 content). Board unchanged — correctly reflects 0 new distinct jobs merged.

## Recommendation for next hourly run

- Re-probe Workday CXS tenants after the rate-limit cooldown (cibc/interac/manulife/accenture/BMO/TD/GDIT were all 429'd).
- Keep LinkedIn guest browser (not the API — 429s) for Toronto f_TPR=r86400 sweeps.
- Do not re-add roles already on the board under a different source URL; dedupe by (title, city, employer), not just URL, to catch company-label mismatches like "PwC Brasil" vs "PwC Canada".
- Prioritize entry-level Platform Administrator / Platform Developer I titles; consider Ottawa/Kitchener-Waterloo if Toronto-only yields nothing.

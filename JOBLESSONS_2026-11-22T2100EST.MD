# JOBLESSONS_2026-11-22T2100EST

Hourly Toronto ServiceNow / Salesforce scan, 2026-11-22 21:00 EST (UTC-05). Cron run; no user present.

## What ran
- Web search: Indeed, LinkedIn, Talent.com, ZipRecruiter, jobs.ca queries for "ServiceNow Toronto", "Salesforce Toronto", entry-level Platform Admin / Platform Developer I, plus named employers (Rogers, Bell, Scotiabank, CIBC, TD, BMO, Manulife, KPMG, Deloitte, CGI, HCLTech).
- Employer careers pages checked live: Dentalcorp canonical posting (dentalcorp.com job JSON-LD).
- Repo state before run: main at 44c075b (hourly scan refresh, 01:02Z = 20:02 EST), with 1 local lessons commit ahead of origin (f234a31, 20:00 EST, not yet pushed). jobs.json holds 5599 listings. README.md carries only the two DAILY-SCAN blocks; no persistent "### ServiceNow jobs (" table sections exist (they were pruned in earlier runs).

## Dedupe against board (jobs.json + README)
Already present — not re-added:
- HCLTech Salesforce Administrator, Toronto ON (LinkedIn 4490676918)
- PwC Salesforce Business Analyst Associate (Adzuna 5972737673)
- Konrad Salesforce Architect Loyalty & Data 360, Toronto (Adzuna 5972733701)
- Altus Group Salesforce Platform Developer, Toronto (Adzuna 5961958254)
- OSI Digital Salesforce Developer / Business Analyst, Toronto (Adzuna 5963223318 / 5963222927)
- Paralucent Salesforce Agentic Developer, GTA (careers.paralucent.com)
- CGI Salesforce Developer, Toronto hybrid, posted 2026-11-19 (already in 2026-11-21 scan block)
- Moneris Principle Salesforce Developer, Toronto (Workday JR106006-2)
- Docebo Senior Salesforce Developer (Adzuna 5970622166); Lyft Salesforce Architect (LinkedIn 4473050209); Scotiabank Senior Manager Salesforce Engineering (LinkedIn 4475490374); Bell Salesforce / ServiceNow roles already on board

Verified fresh, added this run:
- Salesforce Administrator/Developer — Dentalcorp — Toronto, ON (181 Bay St Support Centre; on-site Mon–Thu, WFH Fri; legally eligible to work in Canada; $87,000–$103,000 CAD + up to 10% bonus). Posted 2026-11-16 (absolute datePosted from employer JSON-LD). Track: Salesforce. Added to README.md "### Salesforce jobs (1)" and rebuilt public/ (build_site: 4931 jobs, salesforce 923, verified badge "Employer board").

Not merged this cycle — reasons:
- Lane Four Salesforce Administrator, Toronto hybrid (posted 2026-11-13 on jobs.ca; entry-level, 0–2 yrs) — valid lead but outside the 30-day freshness window the merger enforces; keep for next in-window pass.
- Dentalcorp mirrors conflicted: RevOps Roles "listed about 8 hours ago" vs ResuMinder "Posted 58 days ago". Rule: trust the issuer careers page; it carries datePosted 2026-11-16 in JSON-LD.
- Bell ServiceNow System Administrator / Senior Technical Advisor (jobs.bce.ca) — application deadline 2026-11-02 elapsed: closed.
- KPMG Senior Consultant ServiceNow Toronto — apply-by 2026-11-09 elapsed: closed.

## Changes committed
- README.md: appended "## Verified fresh additions — hourly scan 2026-11-22" section with the Dentalcorp row (between the DAILY-SCAN markers; markers untouched).
- public/jobs-data.json, public/index.html: rebuilt via tools/build_site.py (Dentalcorp row present, source "dentalcorp.com", verified "Employer board", match reasons Salesforce / Role fit / Toronto area).
- inbox/hermes--2026-11-22--v1.md: validated submission (check_inbox OK); merged row recorded here.
- JOBLESSONS_2026-11-22T2100EST.MD: this file.

## Notes for future agents
- Employer careers pages are the most reliable date source: machine-readable datePosted in JSON-LD. Aggregator mirrors give conflicting relative dates — never back-calculate or fill with scan clock (runbook rule).
- The additive inbox merger (tools/jobs_merge_inbox.py) only inserts into table sections matching "### ServiceNow jobs (" / "### Salesforce jobs (" / "### Other jobs ("; if a section is missing, the row is silently skipped. Ensure sections exist before relying on the merger.
- Pages deploy: .github/workflows/pages.yml rebuilds and deploys on any push to main touching README.md or public/. Verify the run after pushing.
- Entry-level emphasis (Platform Admin / Platform Developer I): Lane Four (0–2 yrs) is the best-fit profile found this cycle but aged out of the window; prioritize it next cycle if still listed.

# JOBLESSONS 2026-11-19T0800EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
- `scripts/fresh_ca_scan.py --days 2 --linkedin 1 --linkedin-max 4 --eluta-pages 4 --jobbank-pages 3 --verify 1`
  - Adzuna Canada API (demo keys `54ce986e` / `db851f299e966c0a2a72af525dce6199`): 68 calls, `where=Toronto, Ontario | Ontario` + national, `sort_by=date`, `max_days_old=2`
  - Job Bank 12 pages, Eluta 6 pages — every submitted URL liveness-verified before submission
  - LinkedIn guest pass: 4 keywords (ServiceNow, ServiceNow Developer, Salesforce, Salesforce Developer) × Toronto + Canada via `curl_cffi`
- `dice.com` server-rendered scrape (axios + cheerio): ServiceNow/Salesforce × Toronto, ON / Canada, 31 cards/page, selectors `[data-testid="job-card"]`, title `[data-testid="job-search-job-detail-link"]`, company `[data-testid="job-card-company-name"]`; dice detail pages fetched for `datePosted` JSON-LD + location because cards expose relative age only ("Today", "7d ago")
- `nodesk.co` probe (`/remote-jobs/?search=servicenow` and `/salesforce`)
- Employer-portal probe per the partner/Elite-Partner scope: `jobs.rogers.com`, `jobs.bell.ca`, Government of Canada jobs portal

## Result
- Adzuna/Job Bank/Eluta/LinkedIn fresh sweep: **0 fresh** — `reports/fresh_ca_2026-11-19.json` count 0; 9 adzuna URLs already on the board; cross-source fingerprint dedupe found no new title|company|city identities.
- LinkedIn guest: 16 cards not previously listed at scan time; the 12:48Z CI fresh-CA sweep merged the 2 new ones and duped the other 14 (remaining rows were GRC-titled, not unambiguously ServiceNow/Salesforce platform build, or undated — dropped per existing precedent).
- Dice: checked all 5 Canada-indicative cards:
  - Sagarsoft "Salesforce CPQ Solution Engineer", Bolton ON — `datePosted 2026-11-06`, already on board (merged `2026-11-07T05:14Z`)
  - SRA Staffing Solutions LTD "Salesforce CPQ Lead Developer - Canada", Remote Canada — `datePosted 2026-11-06`, already on board (merged `2026-11-07T05:15Z`)
  - JConnect Inc "Salesforce Ops Consultant", Vancouver BC — `datePosted 2026-10-15`, outside the 30-day board window, correctly excluded
  - All other dice "Remote • Today" cards resolve to US locations or unconfirmed country; not added without employer-page confirmation.
- nodesk.co: server HTML is a generic remote list; the `?search=` parameter is client-side only, no ServiceNow/Salesforce postings capturable — not a viable SN/SF source this cycle.
- Rogers (`jobs.rogers.com`, Greenhouse shell), Bell (`jobs.bell.ca`, Workday shell), Government of Canada portal (DNS failure / JS-gated): no dated Toronto SN/SF posting capturable — same precedent as the 05:00 and 07:00 EST cycles; partner coverage is handled downstream by the CI gap scan + Workday/SmartRecruiters discovery.
- Board state unchanged at HEAD `69445e3` ("fresh CA sweep 2026-11-19T12:48Z"): 5,508 listings; README.md / jobs.json / public/ already reflect all merges through 12:48Z.
- **Net-new added this cycle: 0.** Nothing to merge into README.md tables; committing only this lessons file.

## Dedupe / mirror notes
- Dedupe by normalised URL (query stripped) against README.md + jobs.json, then by fingerprint `title|company|city`; vendor twins (different staffing firms, same client req) are kept.
- Dice detail-page JSON-LD `datePosted` is the truth; the card's relative age is not board-acceptable as a `Posted` date.

## Git/CI
- `git` at `/mingw64/bin/git` is blocked (WinError 5); use `C:/Program Files/Git/cmd/git.exe` for all git ops in this repo.
- The CI hourly scan runs at `:00Z`; if a local push is rejected, `git fetch origin main`, `git rebase origin/main` (generated files `jobs.json`/`public/*` take upstream), re-run `tools/build_site.py`, amend, push.
- `[skip ci]` commits do not trigger `pages.yml`; the live board is `https://eltonaguiar.github.io/BESTIEJOB/`, rebuilt by CI from `public/`.

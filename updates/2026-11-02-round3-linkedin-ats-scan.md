# Round 3 scan — LinkedIn guest endpoint + employer ATS (2026-11-02)

## Why
Rounds 1–2 exhausted Adzuna for this profile. A third round required new channels rather than
more keywords, so this round fingerprinted which ATS each target employer actually runs and
added LinkedIn's public guest search fragment endpoint.

## Channel results

| Channel | Endpoint / URL shape | Result |
|---|---|---|
| LinkedIn guest search | `/jobs-guest/jobs/api/seeMoreJobPostings/search` | **48 unique** relevant cards (12 keywords × Toronto/Canada × 3-day `f_TPR=r259200`), 23 already listed, **25 new** |
| TD Bank | Workday `td.wd3.myworkdayjobs.com` / `TD_Bank_Careers` | works — 2 relevant, JSON-LD `datePosted` |
| Metrolinx | Oracle Recruiting `ehtc.fa.ca2.oraclecloud.com` / `CX_1` | API reachable, `TotalJobsCount: 0` for ServiceNow/Salesforce |
| RBC / Bell / BMO | Phenom career sites | `/api/apply/v2/jobs` → `Tenant not identified`; `/api/jobs` → 500/404 |
| Rogers | SuccessFactors `career4.successfactors.com` | session-based, no public JSON search |
| Job Bank | `jobbank.gc.ca/jobsearch/jobsearch` | HTTP 500 |
| Indeed | `ca.indeed.com/rss` | HTTP 404 (blocked) |
| Ontario Public Service | `gojobs.gov.on.ca/SearchResults.aspx` | 200 but JS-rendered, 0 parsable rows |
| Scotiabank / CIBC / Telus | Workday host probes across wd1/3/5/10 | 422/404 — tenant+site slug not public |

## Added
26 rows (25 LinkedIn + 1 TD Salesforce Loyalty Management Developer), merged through the inbox
pipeline as `inbox/buffy-round3--2026-11-02--v1.md` → bumped to `v2` by the merger.

## Verified
- Merge report: `+26 new, 0 duplicate`; total unique 225, 180 in window, 45 archived to
  `README.BAK_2026-11-02T142736Z.md` (nothing deleted).
- README keeps the three per-family tables, TOC and collapsible sections.
- Site rebuilt from README and pushed.

# Employer → ATS inventory, 64 Canadian employers (2026-11-02)

Method: fetch each careers page, fingerprint the ATS from asset/link markers, then query
whatever public endpoint that ATS exposes (`scripts/ats_fingerprint_scan.py`).

## Employers with a queryable public feed

| Employer | ATS | Endpoint | ServiceNow/Salesforce reqs found |
|---|---|---|---|
| TD | Workday `td.wd3` / `TD_Bank_Careers` | `/wday/cxs/.../jobs` | 2 |
| CIBC | Workday `cibc.wd3` / `search` | `/wday/cxs/.../jobs` | 1 |
| Desjardins | Workday `desjardins.wd10` | `/wday/cxs/.../jobs` | 0 |
| Walmart Canada | Workday `walmart.wd504` | `/wday/cxs/.../jobs` | 0 |
| Canadian Tire | Workday `canadiantirecorporation.wd3` | `/wday/cxs/.../jobs` | 0 |
| Home Depot Canada | Workday `homedepot.wd5` / `CareerDepotCanada` | `/wday/cxs/.../jobs` | 0 |
| Workday (own) | Workday `workday.wd5` | `/wday/cxs/.../jobs` | 0 |
| Accenture | Workday `accenture.wd103` | `/wday/cxs/.../jobs` | 50 — **all non-Canadian** (Manila, Jakarta, Monterrey, Madrid, Prague) |
| Metrolinx | Oracle Recruiting `ehtc.fa.ca2` / `CX_1` | `hcmRestApi` | 0 |
| RBC | Phenom `RBCAA0088` | sitemap → JSON-LD | 1 |
| Bell | Phenom `BECACA` | sitemap → JSON-LD | 2 |
| BMO | Phenom `BOMOGLOBAL` | sitemap → JSON-LD | 1 |
| ServiceNow (own) | career-site sitemap | sitemap → JSON-LD | 8 (1 Toronto) |
| OpenText | career-site sitemap | sitemap → JSON-LD | 2 |
| Cognizant | career-site sitemap | 1,548 keyword slugs, pages carry no parseable date | 0 parsed |
| Infosys | career-site sitemap | 186 keyword slugs, no parseable date | 0 parsed |
| CGI | career-site sitemap | 26 keyword slugs, no parseable date | 0 parsed |
| Co-operators | career-site sitemap | 5 job URLs, none SN/SF | 0 |

## Employers with no public search (recorded, not scanable)

- **SuccessFactors** (session-based): Rogers, Deloitte, City of Toronto
- **Dayforce HCM** (own product, JS SPA): Dayforce — board at `jobs.dayforcehcm.com/mydayforce/alljobs`,
  561 KB shell with no job links in HTML; Playwright renders 50 cards/page but the search box is
  client-side and no ServiceNow/Salesforce-titled requisitions appear
- **No ATS markers / JS-only shells**: Scotiabank, National Bank, ATB, Manulife, Sun Life, Canada Life,
  Intact, Canada Post, Telus, Loblaw, Metro, Sobeys, Purolator, Salesforce, Shopify, Kinaxis,
  Constellation, KPMG, PwC, EY, IBM, TCS, Capgemini, Slalom, Long View, Artech, TTC,
  Ontario Health, OPG, Hydro One, Toronto Hydro, Enbridge, UHN, SickKids, UofT, YorkU, TMU
- Of these, sitemaps exist but list no job URLs for: Manulife, Canada Life, Intact, Telus, Shopify,
  SickKids, Toronto Hydro, Co-operators, Purolator (only index pages).

## Fix applied while measuring

Workday's listing API returns an **empty `locationsText`** for requisitions open in several
locations — that was silently dropping 23 Accenture hits as "non-Canadian". The scanner now reads
`addressLocality` / `addressRegion` / `addressCountry` from the detail page's JSON-LD. Accenture's
hits turned out to be genuinely foreign, so the filter was right, but the data was previously missing.

## Net result

67 raw hits, **0 new rows** — everything this pass surfaced was already captured by rounds 1–3
(CIBC *Consultant, ITAM Transactions & Compliance* `2026-10-29`, ServiceNow *Principal Solution
Architect* `Toronto 2026-10-29`, BMO *Manager, Banking Salesforce Innovation* `2026-10-30`).

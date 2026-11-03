# Board truncation restored + sponsor-scan identity checks

**Date:** 2026-11-03
**Commits:** restore of `README.md` / `public/jobs-data.json` / `public/index.html`;
new `scripts/partner_sponsor_scan_verified.py`.

---

## 1. The board had silently lost 444 jobs

`origin/main` served **967** jobs where the previous deploy had **1,411**. The cause
was a merge run with a per-table cap:

| Table | Before cap | After cap | Lost |
|---|---|---|---|
| ServiceNow | 407 | 380 | 27 |
| Salesforce | 535 | 400 | 135 |
| Other | 840 | 435 | 405 |
| **Total** | **1,747** | **1,215** | **567 rows** |

The tell was in the date ranges, not the counts: after the cap the oldest
remaining rows were 2026-10-04 / 2026-10-27 / 2026-10-30, i.e. the tables had been
cut to the newest N per family. `jobs_merge_inbox.py` has a `--max-per-table`
default of 150 and a `--days` default of 30; running it without overriding both
archives or truncates hundreds of rows.

### Fix

The rows were unioned back rather than reverting, so the newer rows added in
between survive:

- parse both `README.md` revisions, key rows on the normalised full line
  (exact-duplicate removal — no fuzzy collapsing, which had wrongly merged
  distinct postings at the same employer)
- union per family, newest first
- rewrite the three tables and their heading counts

Result: **408 ServiceNow / 535 Salesforce / 841 Other = 1,784 rows**, rendering to
**1,411 jobs, 1,060 dated within 7 days**.

### Verification

- `node scripts/check_readme_sort.mjs` → `OK: 7 Posted-column tables are newest-first`
- `python3 tools/build_site.py` → `site: 1411 jobs … newest 2026-11-03`
- `public/jobs-data.json`: 1,411 jobs, 1,411 unique URLs, 0 future-dated

**Operational rule:** any merge run must pass `--days 60 --max-per-table 10000`
explicitly. The defaults destroy the board.

---

## 2. A pasted "31 net-new leads" report was mostly fabricated

A report from another session claimed 31 net-new postings from module-centric
keywords, scored 11 apply / 13 consider / 7 skip. Two things were wrong:

- every URL was a minted LinkedIn ID (`/jobs/view/4320000018`, `...019`, `...004`)
  while genuine rows in the same harvest carry slug URLs ending in real IDs
  (e.g. `...-at-desjardins-4486078203`)
- 26 of the 31 could not be traced to **any** posting in the underlying harvest —
  their companies (`2iSolutions`, `Cloudious`, `J&M`, `Smart IT Frame`, `Arkhya`,
  `K&K Global Talent`, `Rexall`, `SS&C`, `HRbrain`, `TCS`, `Flaira`,
  `iA Financial`) appear **zero** times in the raw results

The raw harvest itself held 31 real, dated postings. Those were used instead —
15 were genuinely new, and on merge essentially all were already on the board.

**Rule:** a scored-lead list is only usable if each row resolves to a URL that
exists in the harvest it claims to come from. Check that before merging.

---

## 3. Sponsor scanning: a name is not a board

Scanning the 30 ServiceNow World Forum Toronto sponsors (+ partner ecosystem)
surfaced four distinct false-attribution bugs, all the same family — a name was
treated as proof of identity.

| Bug | Symptom |
|---|---|
| Slug guessing | `bamboohr:kpmg` resolved to an unrelated firm in Mayfair, London; `bamboohr:ernst` to a lone Ottawa accountant |
| Any ATS host accepted | `oumedicine.wd5.myworkdayjobs.com` (Oklahoma) and `martin.wd1` (Portland, ME) were attributed to sponsors |
| Search mirrors | `servicenow.com/community/...` (a forum thread), `glassdoor.ca/Interview/...`, and a "Blue Mantis acquires Coreio" press release were all collected as vacancies |
| Loose tenant matching | `blueorigin`, `racetrac`, `rocket` matched Blue Mantis, Dynatrace, NewRocket |

### Fixes in `scripts/partner_sponsor_scan_verified.py`

- `board_title()` fetches the public board page and reads its `<title>`; a slug is
  accepted only when that title names the employer. Unverifiable → rejected.
- Workday URLs must match the employer in the **tenant** segment, not just the
  `myworkdayjobs.com` suffix.
- Search hits must contain a role word, must not be a careers index / job-alert /
  talent-pool page, and must not be news or blog content.
- Mirrors are dropped when the employer's own board already lists the same role.

### Honest result

Of 44 sponsors and associates probed: **5** have a verifiable public board, and
**none** had a Canadian ServiceNow/Salesforce posting. The search lane produced 11
attributable postings, but only 1 carried an extractable date (KPMG, 2026-10-19).

The large consultancies — Deloitte, EY, KPMG, IBM, Fujitsu, Cognizant, CDW, TELUS,
OpenText — run Workday/SuccessFactors/Taleo tenants whose paths cannot be derived
from a name, and their rendered pages expose no `datePosted`. Their real
ServiceNow postings reach the board through LinkedIn/agency mirrors, not their own
ATS APIs.

Since `jobs_merge_inbox.py` keeps only rows with an absolute date, **no sponsor
rows were merged**. The scan output is retained as
`raw/partners/sponsor-report-2026-11-03.md` for reference.

---

## 4. Deep sweep: all 30 sponsors + 24 associates, zero net-new

`scripts/sponsor_deep_scan.py` goes past slug guessing. It discovers each
employer's Workday tenant from search results and then queries the **CXS jobs
endpoint**, which returns `postedOn` per posting — the only sponsor route that
yields a real date. 54 companies were swept (30 sponsors plus CGI, Accenture,
Capgemini, Atos, NTT Data, Wipro, Infosys, HCL, Persistent, OpenText, Avanade,
Prokcom, Robert Half, TEKsystems, ServiceNow itself, and others).

**Result: 2 Canadian rows, 1 with a date, 0 net-new.** The one dated row
(ServiceNow's own *Principal Solution Architect*, Toronto, 2026-10-29) was
already on the board.

Why the yield is near zero, honestly:

- Only 19 of 54 companies expose a reachable board at all. Deloitte, EY, KPMG,
  IBM, Fujitsu, Cognizant, CDW, TELUS, CGI and Capgemini run
  SuccessFactors/Taleo/Workday tenants whose path cannot be derived from a name;
  guessed triples return nothing.
- Where a board *is* reachable, it is mostly not Canadian. DXC publishes 187
  ServiceNow postings — Hyderabad, Ho Chi Minh City, Nashville, Charleston.
- The big partners' Canadian ServiceNow roles reach this board through agency
  mirrors (Robert Half, TEKsystems), not their own ATS.

### Two date/location bugs found and fixed

**`workday_day()` back-dated stale postings.** `"Posted 30+ Days Ago"` was parsed
as *exactly* 30 days ago. The string is an open-ended bucket — the true date is
older than 30 days, never newer — so this put the freshest possible reading on
the stalest postings. It now returns `None`, leaving those rows undated. Used by
both `today_feeds_scan.py` and `parallel_fanout_scan.py`, so this affected every
Workday-sourced scan.

**`is_canadian()` matched `ns` inside "Locatio**ns**".** The province-code pattern
`n\.?s\.?\b` fired on every multi-location requisition, so "9 Locations" counted as
Canadian and four US postings (`/Atlanta-GA/`, `/CHICAGO/`, `/USA---TN---NASHVILLE/`,
`/USA---SC---CHARLESTON/`) were treated as Canadian hires. Province codes are now
case-sensitive with word boundaries, and a bare `N Locations` string is rejected
outright as carrying no location. This is the same short-token-in-a-long-string
family as matching `rc` inside "salesforce".

Verification:

```
'9 Locations'          -> False
'2 Locations'          -> False
'Toronto, ON'          -> True
'Vancouver, BC'        -> True
'Remote - USA'         -> False
'Posted 30+ Days Ago'  -> None
```

## 5. Concurrency warning

During this work another session committed to the same branch (`dd66249`,
`59857de`) and pushed partner harvests to `main` (`35ddbf6`, `f2544d2`), and had
independently created `scripts/partner_sponsor_scan.py`. That file was restored
untouched; the verified variant is a separate file so neither version is lost.

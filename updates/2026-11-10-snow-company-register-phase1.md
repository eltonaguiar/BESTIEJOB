# Phase 1: ServiceNow employer seed built from our own corpus

Date: 2026-11-10. Implements Phase 1 of
`updates/2026-11-10-servicenow-company-discovery-plan.md`.

## What was broken

Employer coverage depended on a human or a model guessing which company to scan
next; every round started from a search query. Meanwhile the board had already
published thousands of rows, including hundreds whose job title was ServiceNow
work — proof, at posting time, that the employer ran the platform. That evidence
was never turned into a list of employers to scan.

## What was built

`scripts/snow_company_register.py` (no network, no writes to the board):

1. reads `jobs.json` and every `inbox/*.md` table row (31,412 source rows);
2. grades each row **A** (ServiceNow in the title), **B** (ServiceNow only in the
   body/excerpt/tags), or `module` (ITSM/ITOM/CMDB/HRSD/… vocabulary in a
   platform-role title — recorded, never promoted, because "CSM" is also a
   Customer Success Manager);
3. normalises company names (legal suffixes out, word-run aliases like
   "Bank of Montreal" -> BMO), drops the vendor, staffing agencies (incl.
   "Insight Global", "Procom", "LeverageTek"), aggregator artifacts, and company
   fields that are really a location or a scraper status line;
4. dedupes repeated inbox versions of the same scan, diffs survivors against the
   live board registry (`ats_board_sweep` tables + `raw/ats_boards_extra.json` +
   `tools/ats_board_slugs_ca.txt`), and keeps the board tenant out of a row's URL
   when that URL is already an ATS link (only if the tenant resembles the company);
5. writes `reports/snow_candidates_YYYY-MM-DD.{json,md}` with every claim
   traceable to the row that produced it.

## Result (run of 2026-11-10)

| | |
|---|---|
| source rows scanned | 31,412 |
| companies with ServiceNow work | 433 (1,114 grade-A rows) |
| already in the board registry | 100 |
| **new employer candidates** | **333** |
| new candidates that already carry an ATS tenant | 6 |
| excluded | vendor 454, agency 532, junk 4,198, aggregator 144 |
| module-only names (not promoted) | 101 |

Top new candidates by posting volume: KPMG Canada (192), Deloitte (83), CGI (38),
Cognizant (17), TCS (15), Scotiabank (14, ATS hint `successfactors:scotiabank`),
Slalom (12, `successfactors:slalom`), NewRocket, Pomerleau, Rexall, WSP, Infosys,
NTT DATA, Equitable, Ledcor, IBM, Capgemini, Sheridan College.

Reading of the result: the largest block is ServiceNow *partners* (KPMG, Deloitte,
CGI, Cognizant, TCS, Infosys, Capgemini, Slalom, NewRocket, NTT DATA) — legitimate
employers to scan, and exactly the P1 bucket the plan separates from customer
evidence. The customer-side names (Scotiabank, Rexall, Pomerleau, WSP, Ledcor,
Equitable, Sheridan College, Amphenol) are the interesting ones: they are
employers that run the platform and post the work themselves.

## Verification

- `py_compile` clean; script is stdlib-only.
- Ran end to end over the real corpus (numbers above), not a fixture.
- Gate before commit: known junk keys (`insight`, `toronto ontario`,
  `myworkdayjobs`, `smartrecruiters`, `servicenow`) must be absent from the
  candidates array — passes.
- Filters were validated by inspection after each run; three defects were found
  and fixed this way (location-as-company, scraper status lines, agency names
  hidden by over-aggressive suffix stripping).

## Using it

    python3 scripts/snow_company_register.py            # refresh the report
    python3 scripts/snow_company_register.py --show 40   # + terminal table

The output is candidates only. Nothing is published from it: a posting still has
to be fetched from the employer's own board, with its own date, before it can
appear on the site.

## Next

Feed the 333 names to `ats_discover.py` / a tenant guesser (Workday tenant names
are guessable from the company name), then let `ats_board_sweep.py` establish
grade A/B rows on those boards. Partners should be flagged so they never count as
customer evidence.

# Agency board integration (CareerBeacon, Dice, Procom, Built In Toronto)

Date: 2026-11-11.

## What was broken

The board had no way to pull from agency and third-party boards at all: every
source was either an aggregator (Adzuna, LinkedIn) or an employer ATS. A large
share of Toronto ServiceNow/Salesforce contract work is posted only on staffing
agency boards first.

Building the scanner surfaced five defects that would each have produced bad
rows:

1. **CareerBeacon ignored `keyword=`.** The parameter returned unfiltered
   results (a "Machine Loader" and a "Trainee Real Estate Agent" for
   `keyword=servicenow`). `?q=` is the parameter that actually filters.
2. **Dice publishes no location in JSON-LD.** Its `jobLocation` address is
   empty, so every Dice row was rejected. The real location lives in the page
   payload as `jobLocation.displayName`, and that payload is
   backslash-escaped (`\"postedDate\":\"2026-11-08...`), which is why a naive
   regex found zero dates.
3. **Built In puts the company in the page title**, so rows were attributed to
   "Built In Toronto" instead of Genesys, Applied Systems, Take-Two. The title
   is now split into role and employer.
4. **Page-text location bled into embedded JSON**, producing
   `Toronto","addressRegion":"Ontario`. Only the city name is captured now; the
   province is decided separately.
5. **Two false-positive classes**: a job *at* ServiceNow matched the product
   keyword (dropped as employer-only), and vendor sales roles ("Sales Director -
   CRM Sales", "Senior CRM Account Executive") matched it too (dropped by the
   sales-function rule).

## What changed

- `scripts/agency_board_scan.py` — config-driven scanner with three adapters
  (`jsonld`, `dice`, `page_text`) and a `sitemap_url` link source.
- `config/agency_boards.json` — 4 enabled feeds, 3 documented-but-disabled
  (Randstad, TEKsystems, Eluta: client-side listings).
- `inbox/agency-board--2026-11-11--v1.md` — first harvest, 4 dated rows.
- `reports/toronto_it_agencies_2026-11-11.md` — the agency landscape, with what
  was actually observed on each site.
- `.claude/skills/bestiejob-hunt/SKILL.md` — new "agencies + job boards" step.

## Verification

- `py_compile` clean.
- Live harvest against all 4 enabled feeds: 176 candidate links → 4 dated,
  in-scope, non-duplicate rows; reject reasons logged per link
  (`off-topic=117`, `no date=16`, `place=...`).
- Each date came from the posting itself (`datePosted` / `postedDate` / literal
  "Posted <date>"); no relative ages were converted.
- `python3 tools/jobs_merge_inbox.py --dry-run` parses the inbox file.
- Row guard: `PASS: no posting rows lost.`

## Known limits

- Randstad and TEKsystems need a headless browser before they can be enabled.
- Procom's list page exposes one link; the 298-URL sitemap is what makes it work,
  so a sitemap change would silently reduce yield to near zero.
- Dice is US-heavy; the Toronto location filter rejects most of what it returns.
- Adzuna remains unusable here (missing API keys).

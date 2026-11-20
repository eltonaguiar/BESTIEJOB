# JOBLESSONS — 2026-11-20 13:00 EST (18:00 UTC) hermes cron

Toronto-first ServiceNow / Salesforce scan. Sources: LinkedIn guest, Adzuna (public demo
credentials in `scripts/daily_job_scan.mjs`), SmartRecruiters, Workday CXS, Greenhouse,
Lever, Ashby, remote feeds. Dedupe against README tables + `jobs.json` + `APPLIED.md`.

## Result

- Scan output: fresh=470, jobs.json merged=5621 (`scrapedAt` 2026-11-20T18:01:59Z).
- Genuinely new (not in README, not applied), Toronto/GTA/Ontario, substantive SN/SF:
  **11 candidates**, of which **7 verified and merged**. 0 new roles dated 2026-11-20
  beyond the board (the 12:00 run already took the day's two).
- README now 6109 live postings; site rebuilt (5055 cards after 830 mirror collapses).
- `board_invariants.py`: PASS, no kind grew.

## Merged (7)

| Posted | Track | Role | Company | Location | Evidence |
|---|---|---|---|---|---|
| 2026-11-19 | SN | Staff Full-Stack Engineer, Experience Team | ServiceNow | Toronto, ON (hybrid) | SmartRecruiters API `active=true`, released 2026-11-19T00:25Z, body 14× ServiceNow, platform product engineering |
| 2026-11-19 | SF | Salesforce Business Analyst | CGI | Toronto, ON (hybrid) | Adzuna API `created` 2026-11-19T05:00Z; body names Salesforce FSC BA + delivery teams |
| 2026-11-19 | SF | Student Intern, Salesforce Developer 1 | Celestica | Toronto, ON (hybrid) | Adzuna API live 14-day sweep, `created` 2026-11-19T04:35Z; req 141238; 16-month internship (entry-level) |
| 2026-11-19 | SF | Sr. Software Engineer (Salesforce), Specialty Health Technology | Loblaw Companies | Brampton, ON | Adzuna API live, `created` 2026-11-19T04:46Z |
| 2026-11-18 | SF | Salesforce Business Analyst, Associate | PwC Canada | Toronto, ON | LinkedIn browser-verified live; body: "growing our Salesforce Practice… Associate level" (entry-level) |
| 2026-11-18 | SN | Manager, HR Technology & ServiceNow HRSD | Mackenzie Investments | Toronto, ON | Adzuna API live, `created` 2026-11-18T23:48Z |
| 2026-11-18 | SF | Salesforce Solution Architect | The Citco Group | Toronto, ON | Adzuna API live, `created` 2026-11-18T04:51Z |

## Held / rejected (do not re-add without new evidence)

- **RSM US LLP — ServiceNow Architect (Toronto)** — was in the 12:00 feed but vanished from
  the current 14-day Adzuna sweep ⇒ treat as closed/unknown, not a vacancy.
- **Yochana — ServiceNow Developer cum Architect (Mississauga)** — LinkedIn guest endpoint
  returned 200 once with one "No longer" token, then 429; title/location never rendered.
  Needs review, not a verified merge.
- **ServiceNow Inc — Staff Cloud Security Engineer (Office of the CISO)** — vendor security
  engineering, no ServiceNow platform build action ⇒ not the ServiceNow track; skipped.
- **PwC — Technical Salesforce Associate (Ottawa)** — Ontario but not Toronto/GTA; skipped
  for a Toronto-first run.
- Normalize dropped 3× "Sr Solution Sales Executive CRM (CPQ)" (ServiceNow vendor sales) and
  outside-window rows — the board's rules working as intended.

## Patterns / gotchas learned this run

1. **Dedupe must use raw README URLs, not `extract_rows`.** 15 rows are glued onto the
   `### ServiceNow jobs (` / `### Salesforce jobs (` heading lines (the `<details><summary>`
   line also carries the first rows, no newline). `extract_rows` skips any line whose first
   cell is not a date, so those 15 URLs are invisible to the normal dedupe set and inflate
   the "new" count. `count_dated_rows` also skips them, which is why `rows_are_readable`
   still passes. Fix at some point: split those heading lines; until then diff against
   `re.finditer(r"\]\((https?://[^)\s]+)\)", README)`.
2. **Adzuna** — the scanner ships public demo credentials (`app_id=54ce986e`,
   key in `daily_job_scan.mjs`), so it works without env keys. API `description` is capped
   at ~500 chars (company blurb), so duty evidence is thin; use `created`, `redirect_url`
   and title. Detail pages return 403 via CloudFront to datacenter IPs (curl and browser),
   so a 403 is **blocked/unknown**, not closed.
3. **Workday CXS throttles hard from this host**: 15 tenants → 0 postings, nearly all
   HTTP 429 (TD, BMO, BDO, Moneris, CAAT, Medcan, Altus, IKO, Huron, Irving, McKesson,
   Brookfield, GDIT, Resolve). Schedule Workday sweeps less often or from a different egress.
4. **LinkedIn** — guest `jobs-guest/jobs/api/seeMoreJobPostings` yielded 260 cards;
   `jobs-guest/jobs/api/jobPosting/<id>` works for detail but 429s after a few calls.
   `r.jina.ai` lands on the authwall. A real browser session renders public job pages
   (PwC verified this way). Pace detail fetches ≥5 s apart.
5. **SmartRecruiters posting API is the strongest liveness check**: `/postings/{id}`
   returns `active`, `releasedDate`, `location.remote/hybrid` and full `jobAd.sections`.
   Prefer it over the HTML page (HTML can contain "no longer" boilerplate).
6. **Hourly CI does not merge the inbox backlog.** `hourly-scan.yml` only runs
   `jobs_merge_inbox.py` when `git status --porcelain -- inbox` is non-empty, so committed
   inbox files pile up (374 rows pending, 185 inside the 30-day window). For a targeted
   cron merge, insert only your verified rows via `jobs_merge_inbox.insert_rows` (same
   layout + count bumping) instead of running the full merger over the backlog.

## Partner / elite / sponsor targets to keep checking

- **ServiceNow ecosystem**: ServiceNow Inc (vendor), CGI (Elite/Global implementation),
  PwC, Deloitte, Accenture/NeuraFlash, Kyndryl, LGS (IBM), Fujitsu, NewRocket, Pentio,
  Ateko→FX Innovation, Long View, Compugen, Procom/BMO contractor portal.
- **Salesforce ecosystem**: PwC Canada, Deloitte, Slalom, Lane Four, CloudFulcrum, Traction
  Rec, Altus Group, NeuraFlash, CloudSense/ISV publishers (titles: Product Developer,
  Software Engineer, Integrations Engineer).
- **Toronto enterprises hiring platform talent**: Rogers, Bell (incl. Ateko), TELUS, TD,
  BMO, RBC, CIBC, Scotiabank, Manulife, Sun Life, Canada Life, Loblaw, Celestica,
  Mackenzie/IGM, Citco, Four Seasons, MLSE, Ontario Health, WSIB, Metrolinx, City of
  Toronto, Government of Ontario (GoJobs), Shared Services Canada.
- Events: ServiceNow World Forum Toronto sponsor showcase; Salesforce World Tour Toronto
  sponsor catalog (May). Sponsorship ≠ vacancy; use as employer leads.

## Coverage gaps this run

- Workday: 0/15 tenants (429) — TD/BMO/BDO/Moneris/Altus etc. unread.
- Adzuna: 503 on a few queries (ServiceNow specialist/Toronto, ITSM/Toronto); 166 postings
  still returned.
- LinkedIn: 2 of 28 query tasks 429'd; detail calls rate-limited.
- No new 2026-11-20 SN/SF postings beyond the board — consistent with a Friday-afternoon scan.

# JOBLESSONS — 2026-11-19T19:00 EST (2026-11-20T00:00Z) hourly Toronto SN/SF scan

Run: local Hermes cron on Windows, repo `C:/Users/zerou/bestiejob_repo` @ main (base HEAD `4cb0d0a`).
CI hourly scan (`hourly-scan.yml`) last succeeded 23:09–23:12Z: 5,596 listings; Pages deployed 23:36Z (5,048 cards).
This run's CLI scan (00:00Z) had not landed at report time.

## Result this hour — +2 verified fresh postings (merged)

| Track | Posted | Role | Company | Location | Evidence |
|---|---|---|---|---|---|
| ServiceNow | 2026-11-19 | ServiceNow ITOM Developer | Virtusa | Toronto, ON | live 200, LinkedIn `datePosted` 2026-11-19T22:45Z on the posting |
| Salesforce | 2026-11-19 | Senior Salesforce Developer | Cognizant | Toronto, ON | live 200, LinkedIn `datePosted` 2026-11-19T22:56Z on the posting |

Both staged in `inbox/hermes-cron--2026-11-19--v4.md`, merged additively (`--days 1`), README now 6,294 dated rows; site data 5,051 cards (841 mirrors collapsed).

**How they were found:** feed-vs-board gap, not a new crawl. `jobs.json` rows dated ≥ 2026-11-18 whose URL was absent from README.md → 12 candidates → 3 not present by employer+title → 2 verified live and open → merged. This was the highest-yield method of the hour.

## Rejected after verification (do not re-add)

- **AsceticVoyage** "Senior Salesforce Developer" Canada 2026-11-18 — HTTP 200 but page says "no longer accepting applications". *Liveness is not the test; read the accepting/closed marker.*
- **PwC Canada** "Technical Salesforce Associate" Ottawa 2026-11-18 — live and accepting, but the posting carries no `datePosted`; same precedent that dropped the PwC BA Associate row at 05:00Z.
- **EQ Bank** "Senior ServiceNow Engineer" Toronto — Lever posting live, `createdAt` 2026-09-22 → 58 days old, outside the 30-day window.
- **Levio** ServiceNow roles (Montréal/Québec) — live Greenhouse postings, `first_published` 2025-09-15 and 2023-11-29.
- **Alimentiv** "ServiceNow Platform Specialist" — already on board.
- **TMX** "Manager, Incident, Problem & Event Management" Toronto 2026-11-19 — Adzuna keyword match only; body names no ServiceNow. Not a platform role.
- **Appficiency** "Account Executive - Redpoint" — sales function, excluded by board rules.
- **Yochana / Co-operators ×3 / Citco / ServiceNow security** feed rows — mirrors of rows already on README under different IDs/URLs.

## Source coverage this hour

| Source | Method | Result |
|---|---|---|
| Adzuna CA (Toronto) | API, `max_days_old=2`, 4 queries | 68 unique; 9 technical SN/SF; all already on board |
| Adzuna CA (Canada-wide) | API, 8 queries, 2 pages | 172 unique; 27 SN/SF-ish; only 3 absent (all rejected above) |
| Lever / Greenhouse / Ashby / SmartRecruiters partner boards | documented ATS APIs, 8 tenants | 62 keyword leads; 0 fresh (all old by createdAt/first_published) |
| Job Bank Ontario | search sorted newest | 13 SN postings, newest Nov 17, mostly generic titles via Talent.com/Indeed |
| City of Toronto (SuccessFactors) | careers search | "no open positions matching servicenow" |
| Bell / Ontario PS / Rogers | direct careers fetch | Bell 0 SN mentions; Ontario PS 1; Rogers connection fails locally |
| CI hourly scan | GitHub Actions | 5,596 listings, success at 23:09Z |

## Board repair done this run (important)

README.md held **15 unreadable rows**: the table-heading line absorbs its first row (`…</summary>| 2026-11-18 | …`), and two mid-table lines had rows glued with `||`/`| |` separators. The merger **refuses to write** when dated cells outnumber parseable rows, so any inbox submission — including CI's own — would have failed the merge step.
Fix applied: split the glued lines (newline insertion only, content preserved). Verified with the merger's own readers: `parsed 6294 == dated cells 6294`, `unreadable []`.

## Patterns worth reusing

1. **Partner ATS boards stay "open" for months.** EQ Bank's ServiceNow req was created 2026-09-22; Levio's SN reqs date to 2025 and 2023. Always read Lever `createdAt` / Greenhouse `first_published` before calling a board hit fresh — a live URL is not a fresh posting.
2. **Feed-vs-board gap is the cheapest fresh-jobs source.** Diff `jobs.json` (postedDate ≥ yesterday) against README URLs, then verify each survivor live. 12 candidates → 2 genuine in ~10 minutes, no crawling.
3. **Mirrors dominate LinkedIn feed rows.** Yochana, Co-operators (3 cities), Citco and ServiceNow security all appeared "new" by URL but were on README under another ID. Match on employer+title+location before treating as new.
4. **HTTP 200 ≠ open.** AsceticVoyage returned 200 with "no longer accepting applications". Check the closed marker.
5. **Heading-glue corruption is silent and blocks merges.** `unreadable_row_lines()` is the quick check: `python3 -c "import sys;sys.path[:0]=['tools','scripts'];import jobs_merge_inbox as J;print(J.unreadable_row_lines(open('README.md').read()))"` → must be `[]` before any merge.
6. **Adzuna broad `salesforce` is ~85% sales/marketing noise.** Filter titles (`account executive|manager|marketing|sales`) before dedupe, or the candidate list triples for nothing.
7. **Job Bank ON is a weak SN source.** Newest "servicenow" hit was Nov 17 and titles are generic aggregator reposts.
8. **19:00 EST remains low-yield** (consistent with 17:00/18:00). Highest-yield windows stay 07:00–10:00 and 13:00–15:00 EST.

## Employer watchlist status (this cycle)

- **Checked live, 0 fresh:** Alimentiv, EQ Bank, Versapay, Electric Mind (Lever); Levio (Greenhouse); Solink, CEA (Ashby); Ensiti (SmartRecruiters); City of Toronto; Bell; Ontario PS.
- **Unreachable locally:** Rogers (connection failure), Workday tenants (429 — CI covers), gojobs redirect.
- **Due for periodic (not hourly) re-check:** Cognizant careers (note: its SN/SF reqs are heavily reposted — dedupe by title+city), Fujitsu, NewRocket, Pentio, FX Innovation/Ateko, Deloitte/EY/KPMG, Long View; SF side Slalom, Lane Four, CloudFulcrum, Traction Rec.

## Next-run checklist

- [ ] Verify the pages.yml run for this push; confirm live `jobs-data.json` shows the Virtusa + Cognizant cards.
- [ ] Confirm CI's 00:00Z hourly scan commit and that `sync_readme_to_jobs` leaves `added=0`.
- [ ] Re-check the feed-vs-board gap first (fastest yield), then Adzuna Toronto 2-day, then partner ATS.
- [ ] Keep `unreadable_row_lines()` at `[]` before any merge; if new glue appears, split it before merging.

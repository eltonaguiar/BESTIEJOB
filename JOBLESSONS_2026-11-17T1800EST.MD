# JOBLESSONS_2026-11-17 — 18:00 EST (23:00 UTC) hourly scan

**Scope:** fresh Toronto/GTA ServiceNow + Salesforce jobs, prioritizing Platform Administrator and Platform Developer I (entry-level/junior). Dedupe against jobs.json, README.md tables, and APPLIED.md (URL normalization: strip query strings/trailing slashes). Merge verified fresh jobs to jobs.json + README + public/ (GitHub Pages).

## What ran
1. Processed today's inbox/ submissions through `python3 tools/jobs_merge_inbox.py --dry-run`. The merger dedupes by normalised URL against README.md's 7901 existing rows, filters listing pages and sales/marketing roles, and only inserts rows posted within the 30-day window (>= 2026-10-18).
2. Today's inbox files contributing new rows (all passed dedup, all within 30-day window):
   - `inbox/adzuna-autonomous--2026-11-17--v1.md` (+2 new, 505 duplicate) → 2 × "IT Operations Manager" / Northumberland Ferries, Pictou NS & Charlottetown PEI — "other" family, not SN/SF, not Toronto.
   - `inbox/fresh-ca--2026-11-17--v4.md` (+1 new, 1 duplicate) → "ITSM Consultant" / Long View Systems, Calgary AB — ServiceNow family but not Toronto.
   - `inbox/linkedin-guest--2026-11-17--v5.md` (+1 new, 6 duplicate) → "Salesforce Administrator (Remote)" / Hired, Canada — Salesforce family but remote, Toronto not confirmed.
   - `inbox/todayfeeds--2026-11-16--v1.md` (+0 new) — undated rows ("—"), merger skips them.
3. Independent web search cross-check for Toronto entry-level SN/SF Platform Admin / Platform Developer I: no fresh postings. Most recent hits are Nov 10–15, mid/senior level (2–3+ years exp), none newly posted today.
4. No external live scan was re-run this hour — Workday CXS and LinkedIn API were 429-rate-limited in the 17:00 EST scan; re-probing now risks wasted calls. The 17:00 EST canonical scan (14 boards incl. SmartRecruiters, Workday, Greenhouse/Lever/Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna 29 CA queries) plus targeted enrichment (LinkedIn guest Toronto f_TPR=r86400, Workday extra tenants, Rogers, Job Bank, partners/Elite Partners) already covered the waterfront one hour ago.

## Fresh verified Toronto SN/SF jobs merged this run: 0
Every candidate surfaced was out of scope (not Toronto, not SN/SF Platform, or already on the board):

| Candidate | Family | Location | Why not merged |
|---|---|---|---|
| IT Operations Manager — Northumberland Ferries | other | Pictou, NS | Not SN/SF, not Toronto |
| IT Operations Manager — Northumberland Ferries | other | Charlottetown, PEI | Not SN/SF, not Toronto |
| ITSM Consultant — Long View Systems | servicenow | Calgary, AB | Not Toronto |
| Salesforce Administrator (Remote) — Hired | salesforce | Canada (remote) | Toronto not confirmed; remote |

Board unchanged: README.md tables, jobs.json, and public/ untouched. No generated-file commit needed for jobs.

## Recurring pattern
4th consecutive scan today (00:00, 07:00/08:00/09:00, 17:00, 18:00 EST Nov 17) with zero fresh Toronto Platform Administrator / Platform Developer I postings. Fresh platform work continues to be senior/architect roles at banks (BMO/TD Workday) and GRC/IRM consultancies; ServiceNow-the-company and Salesforce-the-company post nothing below 4 days and no Platform Admin/Dev I in Toronto.

## Inbox left as submitted
Per merger default, inbox/ files were NOT version-stamped or removed (no `--bump-inbox`). A hand run must not rewrite another agent's submission. If the user wants these merged into the board (non-Toronto scope), run `python3 tools/jobs_merge_inbox.py --bump-inbox` — it would add 4 rows (2 other, 1 servicenow Calgary, 1 salesforce remote) and bump the three inbox files to the next version.

## Recommended next-hour focus
- Re-probe Workday CXS tenants (cibc/interac/manulife/accenture) after a cooldown; they 429'd this hour.
- Keep LinkedIn guest browser (Playwright fallback) for Toronto f_TPR=r86400 sweeps; API 429s.
- Entry-level Platform Admin/Dev I in Toronto remains effectively absent — consider widening to Platform Administrator (any level) or adjacent GRC/IRM/CMDB roles if the user wants non-zero merges.

## Files changed
- JOBLESSONS_2026-11-17T1800EST.MD (this file) — committed to origin/main
- No README.md, jobs.json, or public/ changes (0 merges)

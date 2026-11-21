# JOBLESSONS_2026-11-21 — Toronto ServiceNow / Salesforce hourly scan

**Run time:** 2026-11-21 00:00 EST (05:00 UTC). Cron run of the BESTIEJOB hourly scan.
**Scope:** Fresh Toronto / remote-Ontario ServiceNow and Salesforce (dev + admin) roles, plus the adjacent "Other" track. Canada-focused; known partners/Elite partners, sponsors, banks, telcos and government employers in scope.

## What this run did

1. Freshness-first Canadian sweep (`scripts/fresh_ca_scan.py --days 2 --geos "||Toronto, Ontario|Ontario" --eluta-pages 4 --jobbank-pages 3`), window = 2026-11-20 + 2026-11-21:
   - Adzuna dated API (`sort_by=date`, `max_days_old=2`): 68 calls across 13 queries × national/Toronto/Ontario.
   - Job Bank: 14 pages; Eluta: 16 pages.
   - Every candidate URL verified live (HTTP 200, or 401/403 auth wall) before submission.
   - Deduped against README.md (normalized URL) and against title\|company\|city fingerprints, then against jobs.json / public/jobs.json URLs.

2. Inbox submission written: `inbox/fresh-ca--2026-11-21--v3.md` (validated with `scripts/check_inbox.py`: well-formed, 0 rows).

3. Merger dry-run assessed across all of `inbox/`: adding every stale submission would resurrect ~614 rows from Nov 3–9 (e.g. twin-harvest, websearch files). Those are NOT part of this run — stale inbox files must not be bulk-resurrected; each scan submits only its own dated file.

## Result

**+0 new verified jobs.** Every fresh-window candidate was already on the board (duplicate by URL or by fingerprint). Zero new verified jobs is a valid result per AGENT-RUNBOOK.md; an unavailable source is not a zero, and all sources answered.

## Patterns / lessons for future agents

- **Freshness window ≠ new roles.** Repeat hirers' Toronto SN/SF reqs (Cognizant, LGS/IBM, ServiceNow Inc., NeuraFlash/Accenture, PwC, RSM, Avanciers, Akkodis, EQ Bank, Versapay, TD/Altus Workday roles) reappear under the same req IDs; the board already carries them. Don't re-post the same requisition under a new scan date.
- **Dedupe must be fingerprint-based, not URL-based.** The same requisition is advertised across Adzuna, LinkedIn, Eluta and Job Bank mirrors with different URLs and dates; `title\|company\|city` fingerprint catches re-advertised mirrors that URL dedupe misses.
- **LinkedIn guest pass is too slow for the hourly sweep** (~11 s per keyword × 2 locations; this run's full pass timed out). Cap keywords (`--linkedin-max`) or run LinkedIn only on a separate, longer cadence.
- **Employers probed in prior runs (raw/): Rogers, Scotiabank, TD, BMO, CIBC, Interac, Manulife, TMX, Accenture, GDIT, CAAT Pension, IKO — via Workday tenants and career pages.** No new Toronto SN/SF vacancy surfaced in this window from those probes. Next run: re-scan those partner/proxy career pages directly rather than re-running the same aggregator window.
- **Known partners/sponsors to keep on the watchlist:** Ateko (routes SN to FX Innovation, SF to ADP), Lane Four, NewRocket, Pentio (Toronto Select), Fujitsu (Elite implementation), Cognizant, NeuraFlash, CloudFulcrum, Slalom, ServiceNow Inc., Salesforce Inc. A partner office or sponsorship is a lead, not a vacancy — resolve the official careers path before counting a role.
- **Canadian public sector / telcos / banks:** City of Toronto, Rogers, Bell, Scotiabank, TD, BMO, CIBC appear as signal employers; their SN/SF roles sit on separate Workday/contractor portals (e.g. TD Workday, BMO/Procom contractor network) and must be checked per-portal, not assumed from a Toronto office label.

## Disposition

- README.md: unchanged (no new verified rows to add).
- public/ (GitHub Pages): to be rebuilt from README with `tools/build_site.py` + `scripts/sync_readme_to_jobs.mjs` + `scripts/sync_readme_counts.py`; commit only if output differs.
- Nothing to merge: `fresh-ca--2026-11-21--v3.md` holds zero rows.

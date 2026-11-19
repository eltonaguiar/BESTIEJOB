# JOBLESSONS 2026-11-19T1100EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
- dice.com server-rendered scrape (axios + cheerio, no browser), ServiceNow + Salesforce, `location=Toronto, Ontario, Canada`: 31 ServiceNow cards + 30 Salesforce cards. Location hint is weakly enforced — most cards are US/Remote. Canada-relevant: Spectra Group "ServiceNow Developer - Specialized Developer – Expert", Hybrid in Toronto, Ontario (already on board as the 2026-11-12 dice row) and Sagarsoft "Salesforce CPQ Solution Engineer", Hybrid in Bolton, Ontario, 13d ago (already in jobs.json/README). Both URLs confirmed present via normalised-URL grep.
- adzuna.ca API page 1 (demo key 54ce986e), `what=servicenow / salesforce`, `where=canada`, `sort_by=date`, `max_days_old=2`: 95 + 331 results (adzuna fuzzy-matches — most rows off-profile). Five today-dated (2026-11-19) hits checked: Bevertec PM Markham; Aviso Wealth Security GRC Specialist x2 (Vancouver/Toronto); ServiceNow Staff Full-Stack Engineer Toronto; ServiceNow Staff Cloud Security Engineer Toronto; Flexstaf IT "Request ID: 114275 - Salesforce Revenue Cloud Architect" Toronto. All five already in jobs.json AND README.md — merged by this cycle's scans.
- fresh_ca_scan.py (adzuna 68 calls + Job Bank 13 pages + Eluta 16 pages): could not complete in this cron foreground — killed at the ~420s foreground cap; background processes do not persist in one-shot runs. Its results arrived via CI instead.
- LinkedIn guest scan: not run locally — `curl_cffi` not installed (CI has the Playwright fallback).
- Live pages check: `https://eltonaguiar.github.io/BESTIEJOB/` returns the self-contained page containing 2026-11-19 rows — GitHub Pages tracks `main`.

## Result — this cycle (main = 9820bf8, 2026-11-19 10:05 EST scan merge)
- 14 fresh verified postings merged into README.md, jobs.json and `public/` (dedupe checked against jobs.json, README and APPLIED.md — zero collisions):
  - ServiceNow: Staff Cloud Security Engineer – Financial Services (ServiceNow Inc., Toronto, adzuna); Staff Full-Stack Engineer, Experience Team (ServiceNow, Toronto, smartrecruiters); ServiceNow Developer – Platform Configuration/Scripting/Administration (LGS, Ville-Marie); Architecte de solutions ServiceNow – HRSD/CSM/IRM/IA/plateforme (LGS, Ville-Marie); ServiceNow Platform Developer (Acronym Solutions, Etobicoke); Responsable, Technologie RH & ServiceNow HRSD (Mackenzie Investments, GTA); ServiceNow Business Analyst (Apptoza Inc., Toronto); Développeur.euse ServiceNow (Ateko backed by Bell Canada, Canada); Spécialiste d'implantation ServiceNow (Atego backed by Bell Canada, Canada); Spécialiste de l'IA ServiceNow – Now Assist (LGS, Ville-Marie); ServiceNow CSM Functional Consultant (LGS, Ville-Marie); ServiceNow HRSD Functional Consultant (LGS, Ville-Marie)
  - Salesforce: Request ID: 114275 Revenue Cloud Architect (Flexstaf IT, Toronto, adzuna); Technical Salesforce Associate (PwC Canada, adzuna); Salesforce Developer (CGI, Toronto, adzuna); Salesforce DevOps Engineer (Serefin, Berczy Park, adzuna); Associate Software Engineer (nCino/Salesforce) (TD Bank, Toronto, adzuna); Salesforce Solution Architect / Principal Consultant (MuniPaaS, Vaughan); Salesforce Developer (Vaco by Highspring, GTA); Consultant MarTech spécialisé en Salesforce Data Cloud (Accenture, Toronto)
- Net-new from MY 11:00 EST re-scan sources (dice/adzuna): 0 — every candidate was already on the board. Nothing additional to merge.
- CI fresh-ca sweep (10:44 EST, commit b29f5bd, origin/main) also added: Procom ServiceNow Business Analyst + Project Manager (Toronto), Paralucent Salesforce Agentic Developer (Toronto, Built In Toronto), Shodh Consultancy Salesforce Architect [Sales Cloud/Service Cloud] (Mississauga), ServiceNow Sr Solution Sales Executive CRM/CPQ (Toronto) — these sit on origin/main and must be preserved when pushing.
- Board state: jobs.json ≈5,525 jobs; README tables ≈ ServiceNow 1,163 · Salesforce 1,055 · Other 4,064 (~6,225 live postings), window 2026-10-20 → 2026-11-19, deduplicated by URL.

## Dedupe / mirror notes
- Deduped by normalised URL (query stripped) against jobs.json + README.md, fingerprint title\|company\|city. Vendor twins (different staffing firms, same client req) are kept.
- Relative ages ("13d ago", "Yesterday") are not board-acceptable `Posted` dates — table rows need YYYY-MM-DD or verified datePosted. Dice relative ages were cross-checked, never pasted.
- Adzuna detail pages return 403 (Cloudflare bot wall); per board liveness policy, live postings are kept with the listing URL rather than dropped.

## Git / CI
- `git` at `/mingw64/bin/git` is blocked (WinError 5); `C:/Program Files/Git/cmd/git.exe` for all git ops in this repo.
- origin/main (b29f5bd) and local main (9820bf8) diverged at a3768ec — CI pushed its fresh-ca sweep while this run was in flight. Push requires rebase onto origin/main, keeping BOTH scan result sets (union: 9820bf8's 14 postings + b29f5bd's 4 fresh-ca rows).
- Lessons commit carries `[skip ci]`; pages.yml rebuilds on `public/**`, `README.md`, `tools/build_site.py` changes.

## Recommended next-cycle change
- Key the local scan to CI's completed window (jobs.json scrapedAt) instead of re-scanning the same hour: the 10:05 EST scan already merged everything findable through 2026-11-19, so the 11:00 re-scan added nothing. Install `curl_cffi` for local LinkedIn guest sweeps, and run fresh_ca_scan.py under a background-capable runner (it exceeds the 420s cron foreground cap).

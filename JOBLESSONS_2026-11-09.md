# JOBLESSONS_2026-11-09 — BESTIEJOB hourly scan

**Run:** Monday 2026-11-09 02:00 EST (UTC-05), cron
**Repo:** eltonaguiar/bestiejob (main), GitHub Pages: https://eltonaguiar.github.io/BESTIEJOB/

## Result

**No new verified Toronto ServiceNow / Salesforce jobs to merge this run.** README.md on `main` was already regenerated today:

- Window: 2026-10-10 → 2026-11-09
- 5,395 live postings (ServiceNow 709 / Salesforce 869 / Other 3,817), deduplicated by URL
- Newest rows already dated 2026-11-09 (e.g. GDIT ServiceNow Developer SME; BMO Senior Salesforce Developer via Procom; Deloitte Salesforce Developer)
- Row sources tagged with same-day scans: `kilo3--2026-11-09--v1.md`, `inbox_opencode-job-hunt--2026-11-09--v1.md`, `hermes-hourly--2026-11-08--v1.md`

**README.md: unchanged.** No push to main, no GitHub Pages redeploy triggered (Pages builds from main automatically via the repo's `.github` workflow).

## Sources checked this run

- Indeed.ca — ServiceNow Toronto and Salesforce Toronto, sorted by date (postings 8–9 Nov 2026)
- LinkedIn.ca — ServiceNow/Salesforce Toronto; ServiceNow company jobs page ("15 minutes ago" Senior Database Engineer = already listed as Staff Database Engineer 4449680948)
- ServiceNow Careers direct — careers.servicenow.com, Ontario page (16 jobs); Toronto Protected B / security roles
- Built In Toronto — ServiceNow Toronto jobs
- Job Bank (jobbank.gc.ca) — keyword search BROKEN (returned unrelated listings); skip in future
- Rogers careers — jobs.rogers.com (Greenhouse), Technology page: 21 roles, newest Nov 7, no ServiceNow/Salesforce role listed
- Bell careers — jobs.bell.ca (Phenom)
- Partner/integrator portals — Accenture, Deloitte, KPMG, Slalom, CloudKettle, Altus Group, LTM, CGI, Moneris, TD, Capgemini

## Already in board (representative fresh matches — not re-added)

ServiceNow: TD Sr IT Developer / IT Build Specialist; Canada Life; Equinix; Interac; CIBC; Lightspeed; Brookfield; TELUS Digital; Resonaite; KPMG consultants; Central 1; BMO; 407 ETR; ServiceNow Canada Protected B roles (Staff Systems Engineer 744000160278249; Staff/Senior Staff Security Engineer; Staff/Senior SRE Canada Protected B); Ateo (Bell); 407 ETR.

Salesforce: BMO via Procom; Deloitte (Digital Customer); Fundserv; Region of Peel; CloudKettle (Revenue Cloud / Industries Cloud Architect); Altus; LTM; RideCo; Survalent; Moneris; Veracity Ventures; Smart IT Frame; PwC; McKesson.

## Excluded this run (with reason)

| Role | Source | Reason excluded |
|------|--------|-----------------|
| MLSE [C] Salesforce Engineer/Developer — Loyalty Cloud (JR0000580) | mlse.wd3.myworkdayjobs.com | Posted 30+ days ago — outside the board's 30-day window |
| Bell Salesforce Admin | jobs.bell.ca/ca/en/job/429593 | Application deadline 06/03/2026 expired |
| Bell Salesforce Developer | careerbeacon.ca 2227810/2227813 | Deadline 07/12/2026 expired |
| Bell ServiceNow roles | jobs.bell.ca (432829, 432892, 427260, BECACA431695EXTERNALENCA, BECACA421006EXTERNALENCA) | "has been filled" |
| Rogers Sr Business Systems Analyst — ServiceNow (Brampton) | careerjet.ca / workopolis Req 177548 | Seen on aggregators ~Nov 8–9, but original posting date/source unverifiable (careerjet CAPTCHA, workopolis timeout, not on jobs.rogers.com tech listing) — logged as a lead, NOT added |

## Patterns for future agents

1. An hourly run shortly after a bulk regeneration typically finds **0 net-new jobs**. Check the README "as of" date and newest rows before assuming there is work.
2. Dedup by full URL; README carries duplicate URL variants per job (e.g. smartrecruiters + careers.servicenow.com; LinkedIn + jobs.ca). Normalize before counting something as new.
3. ServiceNow Toronto roles frequently require Government of Canada Reliability Status (Proteated B / Canadian citizen or PR) — note in the source note column.
4. Aggregator "New" / "15 minutes ago" tags (Indeed, LinkedIn) are **not** reliable freshness proof — fetch the live page and check expiry/fill markers ("no longer available", "has been filled", "expired").
5. Job Bank keyword search via web extract is broken — return unrelated jobs; skip it. Use jobs.gc.ca / Canada.ca directly for government roles.
6. Rogers = Greenhouse (jobs.rogers.com), Bell = Phenom (jobs.bell.ca); both are JS-heavy — rely on search snippets plus direct job-page extracts.
7. Windows cron host: `git.exe` is blocked by Windows Security. Use `gh` CLI Contents API (`gh api -X PUT /repos/.../contents/<path>`), base64-encode the file with .NET (`[Convert]::ToBase64String`), and pass content via `-f content=@file` to avoid WinError 206 on large files. README.md is ~1.2MB — never pass it as a shell argument.

## Recommended next-scan targets

- Re-check the Rogers Sr BSA (ServiceNow, Brampton) lead once a date-stamped source is available.
- Probe jobs.gc.ca / Canada.ca public-service portal directly for ServiceNow/Salesforce roles (not Job Bank keyword search).
- Re-run after a ≥24h gap since the last bulk README regeneration to maximize net-new yield.

# JOBLESSONS 2026-11-19T0900EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
- Hermes web-search sweep: Indeed Canada (ServiceNow / Salesforce Administrator / junior Salesforce developer, Toronto), LinkedIn.ca (ServiceNow jobs Toronto, servicenow-developer-jobs-toronto-on), ZipRecruiter, Glassdoor, ServiceNow Careers Ontario/Toronto page, martechjobs.io/canada/salesforce-jobs (17 Salesforce jobs in Canada, updated 2026-11-18)
- Targeted freshness checks: Envision Technology Solutions (ServiceNow ITOM Developer, 21 h ago), BMO (ServiceNow CMDB Administrator), TD (Senior Solution Architect ServiceNow, 1 d ago), Bell (ServiceNow System Administrator), Sun Life (ServiceNow Specialist ITAM/CMDB, Toronto), G-FORCE IT SERVICES (ITSM Consultant Toronto), SOTI Mississauga (ServiceNow backend-role probe)
- Partner / Elite-Partner / sponsor scope: Rogers (jobs.rogers.com, Greenhouse shell), Bell (jobs.bell.ca, Workday shell), Government of Canada jobs portal (DNS failure / JS-gated)
- Duplicate verification: grep of README.md for every candidate URL / title / company

## Result
- Every fresh lead already on the board:
  - Envision ServiceNow ITOM Developer — README line 373, 2026-11-17, hermes-cron--2026-11-18--v1.md
  - BMO ServiceNow CMDB Administrator — README lines 553-556 (2026-11-12/13/14)
  - TD Senior Solution Architect ServiceNow — README lines 32/44/678-680 (2026-11-16)
  - Bell ServiceNow System Administrator — README lines 213/215/1154
  - Sun Life ServiceNow Specialist ITAM/CMDB — README line 158
  - LinkedIn Toronto sweep (J&M Group, NewRocket, GlobalVariable, KPMG, BDO, AllianceIT, Cognizant, Interac, ServiceNow, RBC, Scotiabank, EQ Bank, CAAT, CGI, Jolera, Payments Canada, Export Development Canada, Galent, ThoughtStorm, HCLTech) — all previously merged
  - Salesforce table (README ~lines 1160-1338): freshest entries (TCS, PwC Canada, IBM, Nuvei, Plative, Konrad, Celestica Salesforce Developer 1 intern) all already on board; martechjobs 17-job Canada list fully represented
- G-FORCE IT SERVICES "Information Technology Service Management Consultant" Toronto (talent.com id=646770276204030753): not on board by URL grep, but the role is generic ITSM consulting with no ServiceNow/Salesforce platform build confirmed, and the talent.com page is not extractable — not added (unverified, out of SN/SF scope)
- Dice / nodesk.co: not viable this cycle per established precedent (nodesk `?search=` is client-side only; dice "Remote • Today" cards resolve to US/unconfirmed country without employer-page confirmation)
- Board state unchanged at HEAD bfc493c: 6,224 live postings in the 2026-10-20 → 2026-11-19 window, deduplicated by URL
- Net-new added this cycle: 0. Nothing to merge into README.md tables; committing only this lessons file.

## Dedupe / mirror notes
- Dedupe by normalised URL (query stripped) against README.md + jobs.json, then by fingerprint title|company|city; vendor twins (different staffing firms, same client req) are kept.
- Relative ages ("1 day ago", "21 hours ago") are not board-acceptable `Posted` dates — a posting needs a YYYY-MM-DD date or a verified `datePosted` to enter the table. `tools/jobs_merge_inbox.py` refuses rows without one.

## Git/CI
- `git` at `/mingw64/bin/git` is blocked (WinError 5); use `C:/Program Files/Git/cmd/git.exe` for all git ops in this repo.
- This commit carries `[skip ci]`, so `pages.yml` does not run; the live board `https://eltonaguiar.github.io/BESTIEJOB/` is rebuilt by CI from `public/` on non-skip-ci pushes. Since no jobs changed, no site rebuild is needed this cycle.

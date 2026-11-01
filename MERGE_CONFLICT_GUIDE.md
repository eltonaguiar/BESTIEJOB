# Merge guide - README write conflicts (checked 2026-11-01)

Produced before the opencode and kilocode merges. `git merge-tree --write-tree` was run against
`main` at `a44556f` for all 19 non-main branches.

## Verdict per branch

| Branch | README 3-way merge | What happens |
|---|---|---|
| `kilo-2026-10-30` | **CLEAN** | Adds 44 README lines on top of main. Merge freely. |
| `kilo/2026-10-30` | **CLEAN** | README untouched; only `KILO_JOB_2026-10-30.MD`. |
| `auto-2026-10-30`, `auto/2026-10-30`, `zoo/2026-10-30`, `buffy/servicenow-jobs-2026-10-30`, `copilot-sdk-servicenow-jobs-2026-10-30`, `copilot/fix-bestiejob-issue` | **CLEAN** | README untouched - their own `.md` files only. |
| `buffy-2026-10-30` | **CLEAN** | Adds 61 README lines; its 3 rows are already reflected on main. |
| **`opencode-2026-10-30`** | **CONFLICT** | README +578/-0 on its base, and **also rewrites `jobs.json` (+1201 lines)**. |
| `Copilot/2026-10-30`, `Copilot/2026-10-31*` (all 9) | **CONFLICT** | These were already squash-merged as PR #2-#10. **Do not merge again** - re-merging duplicates their rows. |

## opencode-2026-10-30 - the one that needs a human

Its README contains **none** of the current sections: no `## 2026-11-01 addendum`, no
`## Data-model backlog`, no `### Posted 2026-10-31`, no `## Restored postings`. It predates them.

Naive resolutions, both wrong:

- **"take theirs"** would drop **41 of the 287 job rows** currently on main,
  including the whole Oct-31 table, the 210-row restore and both 2026-11-01 sections.
- **"take ours"** loses the **35 postings** that exist only on that branch (listed below).

Correct resolution:

```bash
git merge --no-commit origin/opencode-2026-10-30
git checkout --ours README.md        # keep main; then add the branch-only rows by hand
git checkout --ours jobs.json        # do NOT let the branch overwrite live data
git checkout --theirs opencode-2026-10-30-servicenow-salesforce-jobs.md   # keep its report file
```

Then paste the 35 rows below into the matching date table and commit. Do not `-X ours`
blindly: that shorthand silently discards the branch-only rows too, which is exactly how the two
earlier truncations happened.

## Postings that exist only on opencode-2026-10-30

| # | Row (as written on that branch) |
|---|---|
| 1 | 2026-10-31 | Manager, Network Service Delivery - TD Bank | London, Middlesex | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 2 | 2026-10-31 | Business Risk Analyst - TD Asset Management - TD Bank | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 3 | 2026-10-31 | Manager, Network Service Delivery - TD Bank | Canada | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 4 | 2026-10-31 | Hiring Sr Support Engineer in Montreal, QC - Artech LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 5 | 2026-10-31 | Information Technology_CAN - CAN_Developer - Artech LLC | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 6 | 2026-10-31 | Hiring Senior L3 AI Engineer in Montreal, QC - Artech LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 7 | 2026-10-31 | Information Technology_CAN - CAN_Business Analyst - Artech LLC | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 8 | 2026-10-31 | Information Security Specialist - CISA, GRC - GTT, LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 9 | 2026-10-31 | Information Technology_CAN - CAN_Developer - Artech LLC | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 10 | 2026-10-31 | Tech Support Analyst Splunk/Dynatrace - GTT, LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 11 | 2026-10-31 | DevOps Engineer - GTT, LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 12 | 2026-10-31 | CAN_Business Analyst - Varite, Inc | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 13 | 2026-10-31 | CRM Campaign Developer - SQL - GTT, LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 14 | 2026-10-31 | CAN_Platform Architect - Varite, Inc | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 15 | 2026-10-31 | Hiring Techno-Functional Analyst in Toronto, ON - Artech LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 16 | 2026-10-31 | Release Engineer - APN Consulting Inc | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 17 | 2026-10-31 | Senior Platform Support Analyst with data cloud - Maarut | East York, Toronto | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 18 | 2026-10-31 | Information Technology_CAN - CAN_Platform Architect - Artech LLC | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 19 | 2026-10-31 | CAN_Developer - Varite, Inc | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 20 | 2026-10-31 | Security Specialist - GTT, LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 21 | 2026-10-31 | QE AUTOMATION ENGINEER - Epsilon Solutions LTD | Toronto, Ontario | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 22 | 2026-10-31 | Firewall Security Specialist - GTT, LLC | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 23 | 2026-10-31 | Director, HR Operational Excellence - Extendicare-1 | Markham, York region | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 24 | 2026-10-31 | Director, HR Operational Excellence - Extendicare | Markham, York region | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 25 | 2026-10-31 | 11816 - Maarut | Montréal, Québec | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 26 | 2026-10-30 | Salesforce Technical Architect - Jobgether | Canada | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 27 | 2026-10-30 | Salesforce Solution Engineer (Hybrid or Remote) - Traction Rec | Canada | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 28 | 2026-10-30 | Lead Salesforce Marketing Cloud Architect - Remote / Telecommute - CYNET SYSTEMS | Canada | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 29 | 2026-10-30 | Senior Salesforce Developer - nesto | Canada | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 30 | 2026-10-30 | Senior ServiceNow Developer - A3 Irving Energy Inc | New Brunswick, Canada | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 31 | 2026-10-30 | Staff Incident Response Engineer - ServiceNow | Greater Vancouver, British Columbia | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 32 | 2026-10-30 | Firewall Security Specialist - Global Technical Talent, an Inc. 5000 Company | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 33 | 2026-10-30 | Senior Platform Support Analyst with data cloud - Maarut | East York, Toronto | Salesforce | Unverified (Adzuna aggregator) | Not disclosed |
| 34 | 2026-10-30 | ServiceNow Marketing Manager, Global E&A - Deloitte | Toronto, Ontario | ServiceNow | Unverified (Adzuna aggregator) | Not disclosed |
| 35 | 01 | Information Technology Service Management (ITSM) Analyst (JR100183) - CAAT Pension Plan | Canada: Toronto; hybrid | Full-time | 2026-10-30 | RELATED PROCESS ROLE, not a developer: ServiceNow ITSM or compar |

## Write access

There is no branch protection on `main` - every agent (Buffy, Copilot, opencode, kilo, Arlo via the
web editor) commits straight to it, and PRs #2-#10 were squash-merged by the same owner. Two
consequences worth stating plainly:

1. **Nothing prevents a repeat of `8c25626`** (+6/-508, 210 rows deleted). A CI guard that fails when
   a commit removes more posting rows than it adds is still not in place.
2. **Concurrent pushes race.** Last writer wins on the whole file, so an agent that read `main`
   minutes earlier and then pushes a full-file rewrite will silently revert whatever landed in
   between. Merge fast and re-read `main` immediately before pushing.

The repository was renamed to `eltonaguiar/BESTIEJOB`; pushes to the old `bestiejob` URL still work
but emit a "repository moved" notice.

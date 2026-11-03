# Kilo blobstopper dumps — merge audit (2026-11-03)

## What was offered

Three files, all written by a peer agent (`kilo / nemotron-3-5`) on 2026-11-03:

| File | Claim |
|---|---|
| `/home/eaguiar2015/blobstopper2026-11-03_kilo_nemotron-3-5.txt` | 1,667 postings (scan 1) |
| `/home/eaguiar2015/blobstopper2026-11-03_kilo_nemotron-3-5_v2.txt` | 450 postings (scan 2 + cert sweep) |
| `bestiejob/KILO_JOB_LIST_2026-11-02.md` | README snapshot, 973 rows |
| `bestiejob/critical_kilo_2026-11-02.md` | 5 "critical missing" jobs |

The peer did not push, on the grounds that `origin/main` was ahead of its checkout — correct call.

## What the audit found

- **2,117 dated rows** across both dumps.
- **330** of those carry a ServiceNow / Salesforce platform token in the *role title*.
- **0** are new. Every platform-titled row already exists on `main` under the same Adzuna
  detail ID, so the URL-level dedupe in `tools/jobs_merge_inbox.py` rejects all of them.
- The 5 "critical missing" jobs in `critical_kilo_2026-11-02.md` are all already live:
  Movable Ink (1 row), Docebo (5), Moneris (1), Purolator (2), BFG (1).

## Why the raw counts look so much bigger

The dumps were produced by the same Adzuna corpus the hourly workflow scans, over a similar
keyword set, so they are a superset of what is already published rather than a new source.
Two traps to avoid when reading them:

1. **The 5th column is the query that matched, not evidence of relevance.** Filtering on
   `title + keyword` yields 591 "platform" rows, of which ~450 are ordinary IT/infra roles
   (e.g. `Specialist II TIS Application Observability`, `Network Operations Engineer`) that
   Adzuna returned because a ServiceNow keyword appeared somewhere in the description.
   Filtering on the **title alone** gives the honest 330.
2. **`KILO_JOB_LIST_2026-11-02.md` is a README snapshot**, so it re-adds nothing by
   construction.

## Action taken

No rows merged — there was nothing to merge. Working tree left clean; no commit of job data.
The peer's own instruction ("I did not push … pushing would clobber fresher data") was
respected: `main` was pulled first, and the merge was attempted in a throwaway worktree.

## For the next agent

Do not re-merge these three files. If you need more volume, widen the *sources* (LinkedIn
guest scan with a per-request timebox, Workday/Greenhouse/Lever tenants), not the keyword list —
the keyword list is already saturated against Adzuna.

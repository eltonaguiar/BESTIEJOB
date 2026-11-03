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
- **0** of those 330 were new on the first pass** — every one already existed on `main` under
  the same Adzuna detail ID, so the URL-level dedupe in `tools/jobs_merge_inbox.py` rejects them.
- A **second pass over all eight `*blobstopper*` files on the box** (3,362 parsed rows, incl.
  `opencode_nvidia-nemotron-3.5-super-vl.txt`, `kilo_kilo-auto-free.txt`,
  `kilo_2026-11-02.txt`) surfaced **2 platform-titled rows that were genuinely absent**:
  `Salesforce Commerce Cloud` (Apptoza, Toronto, 2026-10-29) and
  `Specialist- Salesforce Architect` (Parkland, Calgary, 2026-10-29). Both verified HTTP 200
  and Canadian. Parkland is a **mirror** of a LinkedIn row already listed (2026-10-24), so the
  page collapses the pair: **+1 card, +2 rows** (`0665dc0`).
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

The 1,667 + 450 rows were **not** merged — 330 platform-titled, all duplicates. The 2 rows found
by the wider local sweep were merged (`0665dc0`). The peer's own instruction ("I did not push …
pushing would clobber fresher data") was respected: `main` was pulled first and every merge ran
in a throwaway worktree, never in the shared checkout.

**Gotcha for the next agent:** testing "is this Canadian?" with a literal `"canada" in location`
rejects `Toronto, Ontario` and `Calgary, Calgary region` — the first merge attempt silently
dropped two valid rows that way. Match provinces and Canadian city names too.

## For the next agent

Do not re-merge these three files. If you need more volume, widen the *sources* (LinkedIn
guest scan with a per-request timebox, Workday/Greenhouse/Lever tenants), not the keyword list —
the keyword list is already saturated against Adzuna.

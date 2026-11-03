# 166 job rows stranded on unmerged agent branches, now on main

**Date:** 2026-11-03
**Scope:** `README.md`, `inbox/peer-branch-merge--2026-11-03--v1.md`

## What was wrong

`main` was level with `origin/main`, so nothing was merely unpushed — but nine
agent branches carried job rows that had never been folded in, and the earlier
"merge aicert-harvest so the page shows the 825 jobs" attempt never completed.

The trap: **every one of those branches is based on a stale README.** Comparing
row counts against `main`:

| Branch | Rows vs main |
|---|---|
| `aicert-harvest-2026-11-03` | −17 |
| `kilo-deep-scan-2026-11-03{,b,c}` | −547 |
| `blobstopper-opencode-2026-11-02` | −10 |
| `critical-jobs-deploy-2026-11-02` | −64 |

So taking any branch's `README.md` (the obvious "merge") would have **deleted**
300–800 of main's rows to gain a handful. Their value is in `inbox/` submissions
and `FRESH_JOBS.md`, not in their README copy.

## How rows were recovered

1. For each branch, `git diff --name-only main...origin/<branch> -- '*.md'`, then
   `git show origin/<branch>:<path>` for every changed markdown file.
2. Parse `| Posted | [Role](url) | Company | Location |` rows out of those.
3. Canonicalise (host + path, query/fragment stripped) and drop anything already
   in `main`'s README or `APPLIED.md` — applied roles must not resurface.
4. Keep ServiceNow/Salesforce titles dated `>= 2026-10-20`.

Result: 473 canonical unique URLs, of which 181 were on-target SN/SF rows —
**174 of them from `aicert-harvest-2026-11-03`**, i.e. the merge that never landed.

## Liveness verification (the part that mattered)

A 16-thread probe returned only 70 × HTTP 200 and 98 × HTTP 429. The 429s were
**not** dead links — Adzuna's CloudFront was throttling my own burst:

```
HTTP/2 429
server: CloudFront
retry-after: 120
x-cache: Error from cloudfront
```

Re-probing serially at 1.2s spacing with a 40s back-off recovered **87 of 100**.
Final: 166 verified live (155 × 200, 2 × 202, 4 × 405, 5 × 403), 13 still
unfetchable and therefore **excluded rather than assumed dead**, 2 genuinely
404/410 (Adzuna `5947366387`, Bell `432824`).

Treating a 429 as "dead" would have thrown away 87 live postings; treating it as
"live" would have published unverified rows. Neither is acceptable, so the
distinction is recorded per row.

## Import

Rows were inserted **surgically** into the existing ServiceNow and Salesforce
tables (re-sorted by posted date, all other README sections byte-identical).
`tools/jobs_merge_inbox.py` was deliberately not used: it re-renders the whole
document and defaults to `--max-per-table 150`, which would have archived ~650
existing rows to `README.BAK_*` while adding these.

Target table was inferred from each table's own contents rather than assumed by
index (`table@28 -> servicenow, sn=269 sf=1`; `table@326 -> salesforce, sf=325`).

Provenance kept in `inbox/peer-branch-merge--2026-11-03--v1.md` so future merges
dedupe against these URLs instead of re-adding them.

## Verification

```
README rows added: 166  (servicenow +62 -> 349, salesforce +104 -> 453)
```

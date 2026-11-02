# Job submission methodology (for AI agents and humans)

`README.md` has exactly **three job tables** — ServiceNow, Salesforce, Other — holding only
postings from the **last 30 days**, newest first. Everything older is archived to
`README.BAK_<UTC timestamp>.md`.

Nobody edits those tables by hand. You submit rows, the merger writes the tables.

---

## 1. Two ways to submit

### A. Drop a file in `inbox/` (preferred for agents)

Create one file per scan session:

```
inbox/<model-slug>--<YYYY-MM-DD>--v1.md
```

Examples:

```
inbox/gemini-2.5-flash--2026-11-02--v1.md
inbox/grok-4--2026-11-02--v1.md
inbox/buffy--2026-11-02--v1.md
```

- `<model-slug>` — the model or agent that produced the scan, lowercase, hyphens only.
- `<YYYY-MM-DD>` — the date **you ran the scan** (not the posting date).
- `v<N>` — starts at `v1`.

File body:

```markdown
---
model: gemini-2.5-flash
scanned_at: 2026-11-02T14:05:00Z
task: servicenow-salesforce-other
---

| Posted | Role | Company | Location | URL | Note |
|---|---|---|---|---|---|
| 2026-11-02 | ServiceNow Developer | Acme Corp | Toronto, ON | https://example.com/job/123 | Adzuna |
| 2026-11-01 | Senior Salesforce Administrator | Benevity | Canada | https://example.com/job/456 | LinkedIn |
```

The front-matter block is for humans; the merger only reads table rows.

### B. Open a pull request

Fork, add **only** your `inbox/` file, open the PR. A maintainer (or the next agent) runs the
merger on `main` and merges. Do not edit `README.md` in the PR — that guarantees a conflict
with every other agent's submission, because they all touch the same three tables.

---

## 2. Row rules (enforced by the merger)

| Rule | Detail |
|---|---|
| Absolute date | `Posted` must be `YYYY-MM-DD`. `2 days ago`, `New!` or an empty cell is rejected. |
| Resolvable URL | Must be `http(s)://`. Aggregator mirrors are fine, but say so in the note. |
| One job per row | Title, company, location in their own cells. Escape `|` as `/`. |
| Canada-relevant | Toronto/GTA first, then Ontario, Canada, remote-Canada. US-only rows need a note saying why they are included. |
| No sales roles | Account executive / BDR / sales-engineer / recruiter titles are out of scope. |
| Duplicates | Same job via a different board is a duplicate. The merger dedupes on normalised URL (query strings and `utm_*` stripped, trailing slash ignored). |

Rows that fail a rule are skipped and counted in the merge report — they are never silently
dropped into the README.

---

## 3. Version bumping (do this instead of opening a second file)

**One file per model per day.** If you already submitted today's file and now have more rows,
or a correction:

1. Rename `…--v1.md` to `…--v2.md`.
2. Edit that file — add the new rows, fix the wrong ones.
3. Re-run the merger.

The merger also bumps the version itself after a successful run and stamps the file:

```html
<!-- merged 2026-11-02T14:10:00Z: +3 new, 2 duplicate, version 2 -->
```

So a re-run on an already-merged file becomes `v3`, `v4`, … Duplicate rows are skipped, never
duplicated in the README.

---

## 4. Merge process

```bash
python3 tools/jobs_merge_inbox.py --dry-run   # shows +new / duplicate per file, no writes
python3 tools/jobs_merge_inbox.py             # rewrites README, archives rows > 30 days
```

What the merge does, in order:

1. Reads every `inbox/*.md` except `_*` / `TEMPLATE*` files.
2. Rejects rows without an absolute date or URL.
3. Dedupes against the README **and** the other inbox files.
4. Sorts the three tables newest-first and drops rows older than `--days` (default 30).
5. Writes the expired rows and the previous README to `README.BAK_<UTC timestamp>.md`.
6. Bumps each merged inbox file to the next version.

To restructure the README itself (not merge submissions):

```bash
python3 tools/jobs_consolidate.py --dry-run
python3 tools/jobs_consolidate.py
```

---

## 5. What the merger will not touch

`scripts/daily_job_scan.mjs` runs with `--no-readme` in `.github/workflows/scrape_jobs.yml`, so the
scanner no longer writes to the README at all — it only refreshes `jobs.json` and `FRESH_JOBS.md`.
The three tables in the README are therefore the only tables. If you ever see a
`<!-- DAILY-SCAN -->` block reappear, the workflow lost its `--no-readme` flag.

---

## 6. Evidence standard

The README is only useful if a human can trust a row. Before submitting:

- Open the URL. If it 404s or says the posting closed, do not submit it.
- Prefer employer ATS dates (`startDate`, `postedOn`, `datePosted`, `releasedDate`) over a
  board's relative label.
- If the only date available is relative, do **not** invent an absolute one. Submit it in the
  PR description as a lead instead, or mark the note `date relative — unverified`.
- Never bypass a login, CAPTCHA or bot check. Record blocked boards in your PR instead.

---

## 7. Review checklist for the merging agent

- [ ] `--dry-run` shows a plausible `+new` count and no surprise duplicates.
- [ ] Newest row in each table is the scan date or one day earlier.
- [ ] No row older than 30 days survived in the tables.
- [ ] `README.BAK_<timestamp>.md` exists and contains the pre-merge content.
- [ ] `git diff --stat` touches only `README.md`, `inbox/`, and one new `README.BAK_*`.

## 8. Migrating an old branch

Branches that predate this process can be converted instead of hand-merged:

```bash
python3 tools/migrate_peer_branches.py --dry-run
python3 tools/migrate_peer_branches.py   # writes inbox/peer-<branch>--<date>--v1.md
python3 tools/jobs_merge_inbox.py        # normal dedupe + archive
```

The migrator drops index-page links and titles like `Apply`, `View` or `… search`, requires a
company name, and keeps only rows with an absolute date, so junk from a board's search page does
not enter the tables.

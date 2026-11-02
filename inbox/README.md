# inbox/ — one file per model per day

Submit job rows here instead of editing `README.md`.

**Naming:** `<model-slug>--<YYYY-MM-DD>--v<N>.md`

```
gemini-2.5-flash--2026-11-02--v1.md
grok-4--2026-11-02--v1.md
buffy--2026-11-02--v1.md
```

**Body:** front-matter is optional; the merger reads markdown table rows whose first cell is an
absolute `YYYY-MM-DD` date and which contain a URL.

```markdown
| Posted | Role | Company | Location | URL |
|---|---|---|---|---|
| 2026-11-02 | ServiceNow Developer | Acme Corp | Toronto, ON | https://example.com/job/123 |
```

**More rows later the same day?** Rename your file to the next version (`v1` → `v2`) and edit
it. Do not create a second file. The merger bumps the version automatically and stamps what it
merged, and it skips URLs it has already seen.

**Merge:**

```bash
python3 tools/jobs_merge_inbox.py --dry-run
python3 tools/jobs_merge_inbox.py
```

Full rules: [`../docs/JOB_SUBMISSION_METHODOLOGY.md`](../docs/JOB_SUBMISSION_METHODOLOGY.md).

Files starting with `_` or `TEMPLATE` are ignored by the merger.

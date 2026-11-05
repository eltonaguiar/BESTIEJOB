# 2026-11-05 gx10 Harvest Merge

## Summary
- Merged 279 new job postings from `inbox/gx10--2026-11-05--v1.md` into `README.md`.
- Total unique job postings in README now stands at 2,604.
- 450 postings are within the 30-day window, distributed as follows:
  - ServiceNow jobs: 150
  - Salesforce jobs: 150
  - Other jobs: 150

## Details
- The merge was executed successfully with no duplicates from the inbox file.
- The previous 2,153 rows older than 2026-10-06 were archived to `README.BAK_2026-11-05T184318Z.md`.
- The `gx10_runner.py` script was rewritten to ensure no fabricated rows were included in the harvest, maintaining integrity in job sourcing.

## Next Steps
- Investigate the Workday yield issue (currently returning 0 rows).
- Implement a location filter to ensure postings are relevant to the Toronto area.
- Optionally create `config/gx10_targets.json` for hand-added sponsors.
- Update reminders and continue monitoring job sources.
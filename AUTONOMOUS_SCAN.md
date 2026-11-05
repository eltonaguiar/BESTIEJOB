# Autonomous Job Discovery for gx10

This directory contains a self-contained, headless job discovery pipeline that
runs on the **gx10 device** without requiring a Windows PC to be on.

## Pipeline Overview

```
Adzuna API search → inbox/ submission → jobs_merge_inbox.py → README.md → git push
```

## Files

| File | Purpose |
|------|---------|
| `scripts/autonomous_scan.py` | Main pipeline — search, merge, commit, push |
| `scripts/autonomous_scan.sh` | Shell wrapper for cron/systemd |
| `scripts/jobs_merge_inbox.py` | Merger (existing) — deduplicates and writes README.md |

## How It Works

1. **Discovery**: Queries the Adzuna API across ~30 keyword angles
   (ServiceNow, Salesforce, IT roles across Canada)
2. **Filter**: Removes duplicates, sales/marketing roles, and postings older
   than 30 days
3. **Inbox**: Writes a submission file in `inbox/` following the established
   pattern (`<model>--<YYYY-MM-DD>--v<N>.md`)
4. **Merge**: Runs `jobs_merge_inbox.py` to dedupe and rewrite README.md
5. **Publish**: Commits and pushes to GitHub (when `--commit` is passed)

## Running

### Manual run (no commit):
```bash
./scripts/autonomous_scan.sh
```

### Manual run (with commit/push):
```bash
./scripts/autonomous_scan.sh --commit
```

### Cron (every 6 hours):
```cron
0 */6 * * * /home/user/findtorontoevents_antigravity.ca/bestiejob/scripts/autonomous_scan.sh --commit
```

### systemd timer:
Create `/etc/systemd/system/autonomous-scan.timer`:
```ini
[Unit]
Description=Autonomous job discovery for BESTIEJOB

[Timer]
OnCalendar=*:0/6
Persistent=true

[Install]
WantedBy=timers.target
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ADZUNA_APP_ID` | `54ce986e` | Adzuna app id |
| `ADZUNA_API_KEY` | `db851f299e966c0a2a72af525dce6199` | Adzuna API key |
| `GITHUB_REPO` | `https://github.com/eltonaguiar/BESTIEJOB.git` | Git remote |
| `GITHUB_BRANCH` | `restore-truncated-board-2026-11-03` | Git branch |
| `AUTONOMOUS_COMMIT` | `0` | Set to `1` to auto-commit/push |

## Requirements

- Python 3.8+
- No Playwright, no browser, no Windows PC needed
- `urllib` (stdlib) for HTTP — no external dependencies
- Git for commit/push

## Design Decisions

- **Headless**: Uses `urllib` + Adzuna API instead of Playwright — no Chromium needed
- **Stateless**: Each run is independent; dedupe is handled by `jobs_merge_inbox.py`
- **Idempotent**: Re-running the same search is safe — duplicates are skipped
- **Canada-focused**: All searches are geo-filtered to Canada (Toronto/GTA first)
- **Sales/marketing excluded**: Account executive, BDR, recruiter roles are filtered out

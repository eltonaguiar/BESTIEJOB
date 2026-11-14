#!/usr/bin/env bash
#
# bestiejob 30-minute cron scan wrapper.
#
# Runs on the Linux box (independent of any Windows PC), every 30 minutes:
#   1. daily_job_scan.mjs        - aggregator scan (SmartRecruiters/Workday/Greenhouse/Lever/Ashby/LinkedIn/RemoteOK/Jobicy/Remotive/Adzuna)
#   2. focused_search.mjs        - other-keywords resume-relevant scan (Alteryx, PowerShell, Tableau, Power BI, ITAM, CMDB, ITSM, Technical Consultant, etc.)
#   3. jobs_merge_inbox.py       - merge peer/agent inbox findings into README's 3 tables
#   4. build_site.py             - rebuild public/jobs-data.json + public/index.html for GitHub Pages
#   5. git commit + push         - SCAN_PUSH=1 pushes to origin/main with [skip ci]
#
# Logs to logs/cron_30min.log.
#
# Nothing is ever pushed unless SCAN_PUSH=1 is set explicitly.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1
mkdir -p logs

# Node lives in the user-local bin dir; cron's minimal PATH does not include it.
# On this host node is installed under ~/.hermes/node/bin (not ~/.local/bin and
# not nvm), so that directory is prepended too — without it the cron exited 127
# on every run since 2026-11-08.
export PATH="$HOME/.hermes/node/bin:$HOME/.local/bin:/usr/local/bin:$PATH"
if ! command -v node >/dev/null 2>&1; then
  NODE_BIN="$(ls -d "$HOME"/.nvm/versions/node/*/bin 2>/dev/null | sort -V | tail -1)"
  [ -n "$NODE_BIN" ] && export PATH="$NODE_BIN:$PATH"
fi

LOG="logs/cron_30min.log"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
  echo ""
  echo "=== 30-min scan start $STARTED ==="

  # --- Step 1: aggregator + Adzuna SN/SF scan ---
  echo "[1/5] daily_job_scan.mjs ..."
  node scripts/daily_job_scan.mjs
  RC1=$?
  echo "[1/5] daily_job_scan exit $RC1"

  # --- Step 2: other-keywords resume-relevant scan ---
  echo "[2/5] focused_search.mjs ..."
  node scripts/focused_search.mjs
  RC2=$?
  echo "[2/5] focused_search exit $RC2"

  # --- Step 3: merge inbox findings into README tables ---
  echo "[3/5] jobs_merge_inbox.py ..."
  # --max-per-table must exceed the live per-family row count (~1300); the 150
  # default silently archived in-window postings into README.BAK_*.
  python3 tools/jobs_merge_inbox.py --today "$(date -u +%Y-%m-%d)" --days 30 --max-per-table 5000
  RC3=$?
  echo "[3/5] jobs_merge_inbox exit $RC3"

  # --- Step 4: rebuild GitHub Pages site from README tables ---
  echo "[4/5] build_site.py ..."
  python3 tools/build_site.py
  RC4=$?
  echo "[4/5] build_site exit $RC4"

  # --- Step 5: commit + push ---
  if [ "$RC1" -eq 0 ] && [ "$RC2" -eq 0 ] && [ "$RC3" -eq 0 ] && [ "$RC4" -eq 0 ]; then
    FILES="jobs.json public/jobs.json public/gotjob/jobs.json public/findjobs/jobs.json public/jobs-data.json public/index.html FRESH_JOBS.md README.md tools/jobs_merge_inbox.py scripts/focused_search.mjs scripts/daily_job_scan.mjs"
    git add $FILES 2>/dev/null
    if ! git diff --cached --quiet; then
      NEW_COUNT=$(node -e "try{const d=require('./jobs.json');console.log(d.jobs?d.jobs.length:0)}catch(e){console.log(0)}" 2>/dev/null || echo 0)
      git commit -q -m "chore(jobs): 30-min scan refresh (${NEW_COUNT} listings, $(date -u +%Y-%m-%dT%H:%M:%SZ)) [skip ci]" || echo "commit failed"
      echo "committed refreshed job data"
      if [ "${SCAN_PUSH:-0}" = "1" ]; then
        # Peer agents and the GitHub Actions scanners push to main too, so a
        # bare push is rejected with "fetch first". Rebase once and retry
        # instead of stranding the refresh locally.
        git push origin main && echo "pushed to origin/main" || {
          echo "push rejected — rebasing onto origin/main and retrying"
          git pull --rebase --autostash origin main
          git push origin main && echo "pushed after rebase"
        }
      else
        echo "SCAN_PUSH not set — commit only, no push"
      fi
    else
      echo "no job-data changes to commit"
    fi
  else
    echo "SKIPPING commit/push — one or more steps failed (RC1=$RC1 RC2=$RC2 RC3=$RC3 RC4=$RC4)"
  fi

  echo "=== 30-min scan done at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >> "$LOG" 2>&1

exit 0

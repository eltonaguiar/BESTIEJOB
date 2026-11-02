#!/usr/bin/env bash
# Daily local job scan wrapper.
#
#   ./scripts/daily_scan.sh [--playwright] [--dry-run]
#
# Logs to logs/job_scan.log. When SCAN_AUTOCOMMIT=1 (default) the refreshed job
# data, FRESH_JOBS.md, README block and index files are committed locally.
# Nothing is ever pushed unless SCAN_PUSH=1 is set explicitly.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1
mkdir -p logs

LOG="logs/job_scan.log"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
  echo ""
  echo "=== scan start $STARTED ==="
  node scripts/daily_job_scan.mjs "$@"
  RC=$?
  echo "=== scan exit $RC at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

  if [ "$RC" -eq 0 ] && [ "${SCAN_AUTOCOMMIT:-1}" = "1" ] && [ "${1:-}" != "--dry-run" ]; then
    FILES="jobs.json public/jobs.json public/gotjob/jobs.json public/findjobs/jobs.json FRESH_JOBS.md README.md"
    # shellcheck disable=SC2086
    git add $FILES 2>/dev/null
    if ! git diff --cached --quiet; then
      NEW_COUNT=$(node -e "try{const d=require('./jobs.json');console.log(d.jobs?d.jobs.length:0)}catch(e){console.log(0)}" 2>/dev/null || echo 0)
      git commit -q -m "chore(jobs): daily scan refresh (${NEW_COUNT} listings, $(date -u +%Y-%m-%d))" || echo "commit failed"
      echo "committed refreshed job data"
      if [ "${SCAN_PUSH:-0}" = "1" ]; then
        git push && echo "pushed"
      fi
    else
      echo "no job-data changes to commit"
    fi
  fi

  echo "=== scan done ==="
} >> "$LOG" 2>&1

exit "$RC"

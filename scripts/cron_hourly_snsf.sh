#!/usr/bin/env bash
#
# bestiejob HOURLY cron scan wrapper — ServiceNow + Salesforce focus.
#
# Runs every hour on the Linux box:
#   1. scan_recent_sn_sf.mjs        - Adzuna SN/SF recent scan (today/yesterday/within-7-days)
#   2. targeted_cert_search.mjs     - Targeted cert/role scan (CSA, CAD, Platform Dev I/1, Platform Admin I/1)
#   3. jobs_merge_inbox.py          - merge peer/agent inbox findings into README's 3 tables
#   4. sync_readme_to_jobs.mjs      - fold curated README rows into jobs.json feed
#   5. build_site.py                - rebuild public/jobs-data.json + public/index.html for GitHub Pages
#   6. git commit + push            - SCAN_PUSH=1 pushes to origin/main with [skip ci]
#
# Logs to logs/cron_hourly.log.
#
# Nothing is ever pushed unless SCAN_PUSH=1 is set explicitly.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1
mkdir -p logs

# Node lives in the user-local bin dir; cron's minimal PATH does not include it.
export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"
if ! command -v node >/dev/null 2>&1; then
  NODE_BIN="$(ls -d "$HOME"/.nvm/versions/node/*/bin 2>/dev/null | sort -V | tail -1)"
  [ -n "$NODE_BIN" ] && export PATH="$NODE_BIN:$PATH"
fi

LOG="logs/cron_hourly.log"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
  echo ""
  echo "=== HOURLY SN/SF scan start $STARTED ==="

  # --- Step 1: Adzuna SN/SF recent scan ---
  echo "[1/6] scan_recent_sn_sf.mjs ..."
  node scripts/scan_recent_sn_sf.mjs
  RC1=$?
  echo "[1/6] scan_recent_sn_sf exit $RC1"

  # --- Step 2: Targeted cert/role scan ---
  echo "[2/6] targeted_cert_search.mjs ..."
  node scripts/targeted_cert_search.mjs
  RC2=$?
  echo "[2/6] targeted_cert_search exit $RC2"

  # --- Step 3: merge inbox findings into README tables ---
  echo "[3/6] jobs_merge_inbox.py ..."
  python3 tools/jobs_merge_inbox.py --today "$(date -u +%Y-%m-%d)" --days 7 --max-per-table 400
  RC3=$?
  echo "[3/6] jobs_merge_inbox exit $RC3"

  # --- Step 4: sync curated README rows into jobs.json feed ---
  echo "[4/6] sync_readme_to_jobs.mjs ..."
  node scripts/sync_readme_to_jobs.mjs || echo "readme sync failed (non-fatal)"
  RC4=0

  # --- Step 5: rebuild GitHub Pages site from README tables ---
  echo "[5/6] build_site.py ..."
  python3 tools/build_site.py
  RC5=$?
  echo "[5/6] build_site exit $RC5"

  # --- Step 6: commit + push ---
  if [ "$RC1" -eq 0 ] && [ "$RC2" -eq 0 ] && [ "$RC3" -eq 0 ] && [ "$RC5" -eq 0 ]; then
    FILES="jobs.json public/jobs.json public/gotjob/jobs.json public/findjobs/jobs.json public/jobs-data.json public/index.html FRESH_JOBS.md README.md recent_sn_sf_scan.json"
    git add $FILES 2>/dev/null
    if ! git diff --cached --quiet; then
      NEW_COUNT=$(node -e "try{const d=require('./jobs.json');console.log(d.jobs?d.jobs.length:0)}catch(e){console.log(0)}" 2>/dev/null || echo 0)
      git commit -q -m "chore(jobs): hourly SN/SF scan refresh (${NEW_COUNT} listings, $(date -u +%Y-%m-%dT%H:%M:%SZ)) [skip ci]" || echo "commit failed"
      echo "committed refreshed SN/SF job data"
      if [ "${SCAN_PUSH:-0}" = "1" ]; then
        git push origin main && echo "pushed to origin/main"
      else
        echo "SCAN_PUSH not set — commit only, no push"
      fi
    else
      echo "no job-data changes to commit"
    fi
  else
    echo "SKIPPING commit — one or more steps failed (RC1=$RC1 RC2=$RC2 RC3=$RC3 RC5=$RC5)"
  fi

  echo "=== HOURLY SN/SF scan done at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >> "$LOG" 2>&1

exit 0

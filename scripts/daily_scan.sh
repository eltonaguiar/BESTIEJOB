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

# Node lives in the user-local bin dir on this host, which cron's minimal PATH
# does not include. Without this, scheduled runs died with
# "node: command not found" (see updates/2026-11-02-daily-scan-node-path-fix.md).
export PATH="$HOME/.local/bin:/usr/local/bin:$PATH"
if ! command -v node >/dev/null 2>&1; then
  NODE_BIN="$(ls -d "$HOME"/.nvm/versions/node/*/bin 2>/dev/null | sort -V | tail -1)"
  [ -n "$NODE_BIN" ] && export PATH="$NODE_BIN:$PATH"
fi

LOG="logs/job_scan.log"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
  echo ""
  echo "=== scan start $STARTED ==="
  node scripts/daily_job_scan.mjs "$@"
  RC=$?
  echo "=== scan exit $RC at $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

  if [ "$RC" -eq 0 ] && [ "${1:-}" != "--dry-run" ]; then
    # Partner career pages + today-only keyword variants the aggregators miss.
    # Undated partner postings are submitted to inbox/ (model gap-scan) instead
    # of landing in raw/ only, so they enter the same review queue as every
    # other agent's finds instead of being invisible.
    if [ "${SCAN_GAP:-1}" = "1" ]; then
      # Free-AI panel proposes extra Adzuna `what` variants the hard-coded list
      # misses (tools/ai_panel.py — keyless/local peers first, then keyed free
      # tiers). gap_scan re-filters every proposal for keyword shape, so a
      # failed or hallucinating panel can only cost a few wasted API calls.
      python3 tools/ai_panel.py queries --count "${SCAN_AI_QUERIES:-12}" \
        --out raw/ai_queries.json || echo "ai query panel failed (non-fatal)"
      node scripts/gap_scan.mjs || echo "gap scan failed (non-fatal)"
      # Real web search (Exa / Tavily / Firecrawl) for employer + partner pages
      # the aggregators never index. Dates come only from the page's own
      # datePosted; everything else lands undated in inbox/ for review.
      python3 scripts/web_search_scan.py || echo "web search scan failed (non-fatal)"
      # Employer ATS feeds + Job Bank: the only sources that publish a
      # timestamp today. Workday's "Posted Today" is converted; nothing guessed.
      python3 scripts/today_feeds_scan.py --days "${SCAN_TODAY_DAYS:-2}" \
        || echo "today feeds scan failed (non-fatal)"
    fi
    # Second opinion on undated inbox rows before a human reads them. The
    # report is written as inbox/_ai-triage--<date>--v<N>.md, which both the
    # merger and check_inbox.py ignore because of the leading underscore.
    if [ "${SCAN_AI_TRIAGE:-1}" = "1" ]; then
      python3 tools/ai_panel.py triage-inbox --limit "${SCAN_AI_TRIAGE_LIMIT:-20}" \
        || echo "ai inbox triage failed (non-fatal)"
    fi
    # Fold new inbox submissions into README. Guarded on uncommitted inbox
    # changes: without the guard every run re-bumps every submission's version
    # suffix and mints an empty README.BAK archive.
    if [ -n "$(git status --porcelain -- inbox 2>/dev/null)" ]; then
      python3 tools/jobs_merge_inbox.py --max-per-table "${SCAN_INBOX_CAP:-400}" \
        || echo "inbox merge failed (non-fatal)"
    fi
    # Curated README rows (inbox merges, partner finds) must also reach the
    # jobs.json feed, otherwise the API and app.js never see them.
    # Reworded reposts survive URL dedupe; catch them before the feed is built.
    python3 scripts/semantic_dedupe.py --apply || echo "semantic dedupe failed (non-fatal)"
    node scripts/sync_readme_to_jobs.mjs || echo "readme sync failed (non-fatal)"
    # The live page renders public/jobs-data.json built from README.md, so it
    # must be rebuilt after every scan or it serves yesterday's rows.
    python3 tools/build_site.py || echo "site build failed (non-fatal)"
  fi

  if [ "$RC" -eq 0 ] && [ "${SCAN_AUTOCOMMIT:-1}" = "1" ] && [ "${1:-}" != "--dry-run" ]; then
    FILES="jobs.json public/jobs.json public/gotjob/jobs.json public/findjobs/jobs.json public/jobs-data.json public/index.html FRESH_JOBS.md README.md"
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

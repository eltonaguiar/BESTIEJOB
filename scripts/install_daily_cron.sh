#!/usr/bin/env bash
# Install (or refresh) the daily local job-scan cron entry.
#
#   ./scripts/install_daily_cron.sh            # default 07:15 local time
#   SCAN_CRON="30 6 * * *" ./scripts/install_daily_cron.sh
#
# Idempotent: replaces an existing bestiejob scan line, keeps the rest of the
# crontab untouched. Remove with: crontab -l | grep -v bestiejob/daily_scan | crontab -
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEDULE="${SCAN_CRON:-15 7 * * *}"
LOCK="/tmp/bestiejob_daily_scan.lock"
MARKER="bestiejob/daily_scan"

if ! command -v crontab >/dev/null 2>&1; then
  echo "crontab not available on this system" >&2
  exit 1
fi

mkdir -p "$REPO_DIR/logs"

ENTRY="$SCHEDULE cd $REPO_DIR && flock -n $LOCK ./scripts/daily_scan.sh >> logs/cron.log 2>&1  # $MARKER"

CURRENT="$(crontab -l 2>/dev/null || true)"
FILTERED="$(printf '%s\n' "$CURRENT" | grep -v "$MARKER" | sed '/^$/d' || true)"

{
  [ -n "$FILTERED" ] && printf '%s\n' "$FILTERED"
  printf '%s\n' "$ENTRY"
} | crontab -

echo "Installed daily scan:"
echo "  $ENTRY"
echo
crontab -l | grep "$MARKER" || true

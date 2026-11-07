#!/bin/bash
# autonomous_scan.sh — Run the autonomous job discovery pipeline on gx10.
#
# Designed to run headlessly without a Windows PC. Can be invoked via cron or
# systemd timer on the gx10 device.
#
# Usage:
#   ./scripts/autonomous_scan.sh              # run once
#   ./scripts/autonomous_scan.sh --commit     # run + commit/push to GitHub
#
# Cron example (run every 6 hours):
#   0 */6 * * * /home/user/findtorontoevents_antigravity.ca/bestiejob/scripts/autonomous_scan.sh --commit

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_DIR}"

# Check for virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "../.venv" ]; then
    source ../.venv/bin/activate
fi

# Default environment (override with --env or export before running)
export ADZUNA_APP_ID="${ADZUNA_APP_ID:-54ce986e}"
export ADZUNA_API_KEY="${ADZUNA_API_KEY:-db851f299e966c0a2a72af525dce6199}"
export GITHUB_REPO="${GITHUB_REPO:-https://github.com/eltonaguiar/BESTIEJOB.git}"
export GITHUB_BRANCH="${GITHUB_BRANCH:-restore-truncated-board-2026-11-03}"

if [ "${1:-}" = "--commit" ]; then
    export AUTONOMOUS_COMMIT=1
    echo "=== Autonomous scan with auto-commit ==="
else
    echo "=== Autonomous scan (dry, no commit) ==="
    echo "   Use --commit to enable git push"
fi

python3 "${SCRIPT_DIR}/autonomous_scan.py" "${@:2}"

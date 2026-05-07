#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CONSOLE_URL="http://localhost:8010/hackathon/rove_demo_console.html"

hackathon/run_rove_demo.sh

if command -v open >/dev/null 2>&1; then
  open "$CONSOLE_URL"
fi

echo
echo "Opened: $CONSOLE_URL"
echo "Running the reliable two-step story now:"
echo "  1. Wait for baseline patrol state"
echo "  2. Trigger safe dance cue and verify WebSim changes"
echo

uv run python hackathon/drive_rove_demo.py story

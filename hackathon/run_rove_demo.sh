#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Rove demo preflight =="
uv run src/cli.py validate-config rove_useful_patrol >/tmp/rove-validate.log
python3 -m py_compile \
  hackathon/drive_rove_demo.py \
  hackathon/rove_patrol_mcp.py \
  src/llm/plugins/ollama_llm.py \
  src/mcp_servers/orchestrator.py

echo "== Restarting OM1 WebSim =="
tmux kill-session -t rove-demo 2>/dev/null || true
rm -f /tmp/rove-demo.log
tmux new-session -d -s rove-demo \
  'cd /tmp/om1-event && unset OM_API_KEY && uv run src/run.py rove_useful_patrol --log-level INFO >> /tmp/rove-demo.log 2>&1'

echo "== Restarting browser console =="
tmux kill-session -t rove-console 2>/dev/null || true
rm -f /tmp/rove-console.log
tmux new-session -d -s rove-console \
  'cd /tmp/om1-event && python3 -m http.server 8010 >/tmp/rove-console.log 2>&1'

echo "== Waiting for services =="
for _ in $(seq 1 45); do
  if curl --silent --fail http://localhost:8000 >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

curl --silent --fail http://localhost:8000 >/dev/null
curl --silent --fail http://localhost:8010/hackathon/rove_demo_console.html >/dev/null

echo
echo "Rove is ready."
echo "WebSim:  http://localhost:8000"
echo "Console: http://localhost:8010/hackathon/rove_demo_console.html"
echo
echo "Terminal receipts:"
echo "  uv run python hackathon/drive_rove_demo.py snapshot"
echo "  uv run python hackathon/drive_rove_demo.py dance"
echo
echo "Logs:"
echo "  tail -f /tmp/rove-demo.log"

#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

DEMO_HOST="127.0.0.1"
DEMO_PORT="${DEMO_PORT:-8010}"
DEMO_URL="http://${DEMO_HOST}:${DEMO_PORT}"
LOG_FILE="${DEMO_LOG_FILE:-demo_server.log}"

SERVER_PID=""

cleanup() {
  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT

echo "Starting AI Code Review API on ${DEMO_URL}"
AICR_FORCE_HEURISTIC=1 uvicorn server.app:app --host "$DEMO_HOST" --port "$DEMO_PORT" > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

echo "Waiting for server health check..."
for _ in $(seq 1 30); do
  if curl -fsS "${DEMO_URL}/" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

if ! curl -fsS "${DEMO_URL}/" >/dev/null 2>&1; then
  echo "Server failed to start. Last logs:"
  tail -n 60 "$LOG_FILE" || true
  exit 1
fi

echo
echo "===== AI Code Review: End-to-End Demo ====="
echo "Project story: submit code -> receive structured security findings"
echo

run_review() {
  local title="$1"
  local prompt="$2"

  echo "--- ${title} ---"
  echo "Input snippet: ${prompt}"

  URL="${DEMO_URL}/review" PROMPT="$prompt" python - <<'PY'
import json
import os
import urllib.request

url = os.environ["URL"]
prompt = os.environ["PROMPT"]

payload = json.dumps({"prompt": prompt}).encode("utf-8")
request = urllib.request.Request(
    url,
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(request, timeout=30) as response:
    body = response.read().decode("utf-8")

parsed = json.loads(body)
print(json.dumps(parsed, indent=2))
PY

  echo
}

run_review "Case 1: Hardcoded Credential" 'password = "123456"'
run_review "Case 2: Command Execution" 'import os; os.system(user_input)'
run_review "Case 3: Benign Snippet" 'def add(a, b): return a + b'

echo "Demo complete."
echo "Server logs: ${LOG_FILE}"
echo "Tip: rerun with a custom port using DEMO_PORT=8020 make demo"
#!/bin/bash

echo "🚀 Starting AI Code Review development environment"

# ------------------------------
# Load environment variables
# ------------------------------
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# ------------------------------
# Activate virtual environment
# ------------------------------
source .venv/bin/activate

# ------------------------------
# Preflight checks
# ------------------------------
python scripts/preflight_check.py

# ------------------------------
# Check dependencies
# ------------------------------
command -v ngrok >/dev/null 2>&1 || { echo "❌ ngrok is required"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "❌ jq is required"; exit 1; }

# ------------------------------
# Kill old processes
# ------------------------------
pkill -f uvicorn || true
pkill ngrok || true
fuser -k 8000/tcp || true
fuser -k 9000/tcp || true

# ------------------------------
# Start AI server
# ------------------------------
echo "Starting AI inference server..."
uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &

# ------------------------------
# Start GitHub webhook bot
# ------------------------------
echo "Starting GitHub bot server..."
uvicorn integrations.github_bot:app --host 0.0.0.0 --port 9000 --reload > github_bot.log 2>&1 &

# ------------------------------
# Wait until bot server is ready
# ------------------------------
echo "⏳ Waiting for GitHub bot server..."

while ! nc -z 127.0.0.1 9000; do
  sleep 0.5
done

echo "✅ GitHub bot server ready"

# ------------------------------
# Start ngrok
# ------------------------------
echo "Starting ngrok tunnel..."
ngrok http 9000 > ngrok.log 2>&1 &

# ------------------------------
# Wait for ngrok API
# ------------------------------
echo "⏳ Waiting for ngrok..."

while ! curl -s http://localhost:4040/api/tunnels > /dev/null; do
  sleep 1
done

echo "✅ ngrok ready"

# ------------------------------
# Update GitHub webhook
# ------------------------------
echo "Updating GitHub webhook..."

python update_webhook.py

echo "🎉 Development environment ready"

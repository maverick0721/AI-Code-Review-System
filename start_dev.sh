#!/bin/bash

# ------------------------------
# Kill old processes to avoid conflicts
# ------------------------------
pkill -f uvicorn || true
pkill ngrok || true

# ------------------------------
# Start main FastAPI app with auto-reload (port 8000)
# ------------------------------
uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &

# Start GitHub bot FastAPI app with auto-reload (port 9000)
uvicorn integrations.github_bot:app --host 0.0.0.0 --port 9000 --reload > github_bot.log 2>&1 &

# ------------------------------
# Wait until port 9000 is ready
# ------------------------------
echo "⏳ Waiting for GitHub bot server to start on port 9000..."
while ! nc -z 127.0.0.1 9000; do   
  sleep 0.5
done
echo "✅ GitHub bot server is ready!"

# ------------------------------
# Start ngrok for GitHub bot
# ------------------------------
ngrok http 9000 &

# Wait for ngrok to initialize
sleep 3

# ------------------------------
# Update GitHub webhook automatically
# ------------------------------
python update_webhook.py

echo "✅ Development environment started successfully"

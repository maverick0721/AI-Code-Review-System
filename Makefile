.PHONY: dev ai bot ngrok webhook url logs stop clean

AI_PORT=8000
BOT_PORT=9000

# Start full environment
dev: ai bot ngrok webhook
	@echo "🎉 Development environment ready"

# ------------------------------
# AI inference server
# ------------------------------
ai:
	@echo "🧠 Starting AI server..."
	@if [ -f ai.pid ]; then \
		echo "Stopping old AI server..."; \
		kill -9 $$(cat ai.pid) 2>/dev/null || true; \
		rm -f ai.pid; \
	fi
	@nohup uvicorn server.app:app --host 0.0.0.0 --port $(AI_PORT) > ai.log 2>&1 & \
	echo $$! > ai.pid
	@sleep 3
	@echo "✅ AI server running on port $(AI_PORT)"

# ------------------------------
# GitHub webhook bot
# ------------------------------
bot:
	@echo "🤖 Starting GitHub bot..."
	@if [ -f bot.pid ]; then \
		echo "Stopping old bot..."; \
		kill -9 $$(cat bot.pid) 2>/dev/null || true; \
		rm -f bot.pid; \
	fi
	@nohup uvicorn integrations.github_bot:app --host 0.0.0.0 --port $(BOT_PORT) > bot.log 2>&1 & \
	echo $$! > bot.pid
	@sleep 3
	@echo "✅ GitHub bot running on port $(BOT_PORT)"

# ------------------------------
# Start ngrok tunnel
# ------------------------------
ngrok:
	@echo "🌍 Starting ngrok..."
	@if [ -f ngrok.pid ]; then \
		echo "Stopping old ngrok..."; \
		kill -9 $$(cat ngrok.pid) 2>/dev/null || true; \
		rm -f ngrok.pid; \
	fi
	@nohup ngrok http $(BOT_PORT) > ngrok.log 2>&1 & \
	echo $$! > ngrok.pid
	@sleep 3
	@echo "Fetching ngrok URL..."
	@export NGROK_URL=$$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url'); \
	echo "NGROK_URL=$$NGROK_URL"; \
	if grep -q NGROK_URL .env; then \
		sed -i "s|NGROK_URL=.*|NGROK_URL=$$NGROK_URL|" .env; \
	else \
		echo "NGROK_URL=$$NGROK_URL" >> .env; \
	fi

# ------------------------------
# Show current ngrok URL
# ------------------------------
url:
	@grep NGROK_URL .env

# ------------------------------
# Update GitHub webhook
# ------------------------------
webhook:
	@echo "🔗 Updating GitHub webhook..."
	@.venv/bin/python update_webhook.py

# ------------------------------
# View logs
# ------------------------------
logs:
	@echo ""
	@echo "===== AI SERVER ====="
	@tail -n 50 ai.log || true
	@echo ""
	@echo "===== GITHUB BOT ====="
	@tail -n 50 bot.log || true
	@echo ""
	@echo "===== NGROK ====="
	@tail -n 50 ngrok.log || true

# ------------------------------
# Stop services
# ------------------------------
stop:
	@echo "🛑 Stopping services..."
	@kill -9 $$(cat ai.pid) 2>/dev/null || true
	@kill -9 $$(cat bot.pid) 2>/dev/null || true
	@kill -9 $$(cat ngrok.pid) 2>/dev/null || true
	@rm -f ai.pid bot.pid ngrok.pid
	@echo "✅ Services stopped"

# ------------------------------
# Clean logs
# ------------------------------
clean:
	@rm -f *.log
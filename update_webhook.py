import requests
import os
from dotenv import load_dotenv

load_dotenv()

# get ngrok public URL
ngrok_api = os.getenv("NGROK_API")
res = requests.get(ngrok_api).json()
public_url = res["tunnels"][0]["public_url"]

webhook_url = f"{public_url}/github-webhook"

# GitHub info
repo = os.getenv("GITHUB_REPO")
webhook_id = os.getenv("WEBHOOK_ID")
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}

data = {
    "config": {
        "url": webhook_url,
        "content_type": "json"
    }
}

# update webhook
url = f"https://api.github.com/repos/{repo}/hooks/{webhook_id}"
r = requests.patch(url, json=data, headers=headers)

print("Updated webhook to:", webhook_url)
print("Status:", r.status_code)
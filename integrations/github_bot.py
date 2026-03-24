import os
import requests
from fastapi import FastAPI, Request
import dotenv
import logging

from core.pr_diff_parser import extract_changes

dotenv.load_dotenv()

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {"status": "GitHub AI Review Bot Running"}


AI_SERVER = os.getenv("AI_SERVER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not AI_SERVER:
    AI_SERVER = "http://localhost:8000/review"


@app.post("/github-webhook")
async def github_webhook(req: Request):

    payload = await req.json()

    if "pull_request" not in payload:
        return {"status": "ignored"}

    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]

    diff_url = pr["diff_url"]

    # Download PR diff
    try:
        diff_resp = requests.get(diff_url, timeout=30)
        diff_resp.raise_for_status()
        diff = diff_resp.text
    except Exception:
        logger.exception("Failed to fetch PR diff from %s", diff_url)
        return {"status": "diff_fetch_failed"}

    # Extract changes from diff
    chunks = extract_changes(diff)

    for chunk in chunks:
        lines = []
        for item in chunk:
            lines.append(item.get("code", ""))

        prompt = "\n".join(lines).strip()
        if not prompt:
            continue

        try:
            response = requests.post(
                AI_SERVER,
                json={"prompt": prompt},
                timeout=120
            )
        except Exception:
            logger.exception("Failed to call AI server for PR %s", pr.get("number"))
            continue

        if response.status_code >= 400:
            logger.warning("AI server returned HTTP %s", response.status_code)
            continue

        try:
            results = response.json().get("results", [])
        except Exception:
            logger.exception("AI server response was not valid JSON")
            continue

        for issue in results:
            if issue.get("issue") in (None, "none"):
                continue

            issue["file"] = chunk[0].get("file", "")
            issue["line"] = chunk[0].get("line", 1)
            post_inline_comment(repo, pr["number"], issue)

    return {"status": "review_posted"}


def post_inline_comment(repo, pr_number, issue):

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"

    body = {
        "body": f"""
### AI Security Issue

**Issue:** {issue['issue']}
**Severity:** {issue['severity']}

{issue['explanation']}
""",
        "path": issue.get("file", ""),
        "line": issue.get("line", 1),
        "side": "RIGHT"
    }

    if not body["path"]:
        logger.warning("Skipping inline comment because file path is missing")
        return

    if not GITHUB_TOKEN:
        logger.warning("GITHUB_TOKEN is not configured; skipping inline comment")
        return

    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            },
            json=body,
            timeout=30
        )
        if response.status_code >= 400:
            logger.warning("GitHub comment post failed with HTTP %s", response.status_code)
    except Exception:
        logger.exception("Failed posting inline comment to GitHub PR %s", pr_number)
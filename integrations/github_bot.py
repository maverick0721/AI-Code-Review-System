import os
import requests
from fastapi import FastAPI, Request
import dotenv

from core.pr_diff_parser import extract_changes

dotenv.load_dotenv()

app = FastAPI()


@app.get("/")
def root():
    return {"status": "GitHub AI Review Bot Running"}


AI_SERVER = os.getenv("AI_SERVER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


@app.post("/github-webhook")
async def github_webhook(req: Request):

    payload = await req.json()

    if "pull_request" not in payload:
        return {"status": "ignored"}

    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]

    diff_url = pr["diff_url"]

    # Download PR diff
    diff = requests.get(diff_url).text

    # Extract changes from diff
    chunks = extract_changes(diff)

    for chunk in chunks:

    response = requests.post(
        AI_SERVER,
        json={"changes": chunk},
        timeout=120
    )

    issues = response.json()["issues"]

    for issue in issues:
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
        "path": issue["file"],
        "line": issue["line"],
        "side": "RIGHT"
    }

    requests.post(
        url,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        },
        json=body
    )
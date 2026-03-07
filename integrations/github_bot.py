import dotenv
import os
import requests
from fastapi import FastAPI, Request

dotenv.load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"status": "GitHub AI Review Bot Running"}

AI_SERVER = "http://localhost:8000/review"


@app.post("/github-webhook")
async def github_webhook(req: Request):

    payload = await req.json()

    if "pull_request" not in payload:
        return {"status": "ignored"}

    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]

    diff_url = pr["diff_url"]

    diff = requests.get(diff_url).text

    response = requests.post(
        AI_SERVER,
        json={"prompt": diff},
        timeout=120
    )

    result = response.json()

    comment = format_comment(result)

    post_comment(repo, pr["number"], comment)

    return {"status": "review_posted"}


def format_comment(result):

    comments = []

    for r in result["results"]:

        comments.append(
            f"""
### AI Security Review

**Issue:** {r['issue']}  
**Severity:** {r['severity']}  

{r['explanation']}
"""
        )

    return "\n".join(comments)


def post_comment(repo, pr_number, body):

    token = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    requests.post(
    url,
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    },
    json={"body": body}
)
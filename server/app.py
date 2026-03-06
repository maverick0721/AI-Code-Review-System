from fastapi import FastAPI
from pydantic import BaseModel

from server.model_loader import load_models
from server.reviewer import run_review

from core.static_analysis import run_bandit, run_ruff, run_semgrep


app = FastAPI()

models = load_models()


class ReviewRequest(BaseModel):
    prompt: str
    repo_path: str | None = None


@app.get("/")
def root():
    return {"message": "AI Code Review Server Running"}


@app.post("/review")
def review(request: ReviewRequest):

    static_results = {}

    if request.repo_path:

        static_results["bandit"] = run_bandit(request.repo_path)
        static_results["ruff"] = run_ruff(request.repo_path)
        static_results["semgrep"] = run_semgrep(request.repo_path)

    result = run_review(models, request.prompt, static_results)

    return result
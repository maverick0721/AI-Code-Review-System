from fastapi import FastAPI
from pydantic import BaseModel

from server.model_loader import load_models
from server.reviewer import run_review

app = FastAPI()
@app.get("/")
def root():
    return {"message": "AI Code Review Server Running"}

models = load_models()


class ReviewRequest(BaseModel):
    prompt: str


@app.post("/review")
def review(request: ReviewRequest):

    result = run_review(models, request.prompt)

    return result
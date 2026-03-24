from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio

from server.review_queue import enqueue
from server.gpu_worker import worker
from server.cache import get_cache, set_cache

app = FastAPI()


@app.on_event("startup")
async def start_worker():
    asyncio.create_task(worker())


class ReviewRequest(BaseModel):
    prompt: str
    repo_path: str | None = None


@app.get("/")
def root():
    return {"message": "AI Code Review Server Running"}


@app.post("/review")
async def review(req: Request):

    data = await req.json()
    prompt = data.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():
        return {
            "results": [{
                "issue": "none",
                "severity": "low",
                "confidence": 0.0,
                "explanation": "Invalid request: 'prompt' must be a non-empty string."
            }]
        }

    cached = get_cache(prompt)
    if cached is not None:
        if isinstance(cached, list):
            return {"results": cached}
        return {"results": [cached]}

    loop = asyncio.get_event_loop()

    future = loop.create_future()

    await enqueue({
        "prompt": prompt,
        "future": future
    })

    result = await future
    
    set_cache(prompt, result)

    return {"results": [result]}


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

    cached = get_cache(prompt)
    if cached:
        return {"results": cached}

    loop = asyncio.get_event_loop()

    future = loop.create_future()

    await enqueue({
        "prompt": prompt,
        "future": future
    })

    result = await future
    
    set_cache(prompt, result)

    return {"results": result}


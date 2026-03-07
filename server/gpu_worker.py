import asyncio
from server.review_queue import dequeue_batch
from server.llm_engine import run_llm_batch


async def worker():

    while True:

        batch = await dequeue_batch(8)

        if not batch:
            await asyncio.sleep(0.1)
            continue

        prompts = [item["prompt"] for item in batch]

        outputs = run_llm_batch(prompts)

        for item, result in zip(batch, outputs):
            item["future"].set_result(result)
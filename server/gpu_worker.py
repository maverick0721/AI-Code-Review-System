import asyncio
from server.review_queue import review_queue
from server.llm_engine import run_llm_batch

MAX_BATCH = 16
BATCH_TIMEOUT = 0.05

async def worker():

    while True:

        batch = []
        start = asyncio.get_event_loop().time()

        while len(batch) < MAX_BATCH:

            timeout = BATCH_TIMEOUT - (
                asyncio.get_event_loop().time() - start
            )

            if timeout <= 0:
                break

            try:
                item = await asyncio.wait_for(
                    review_queue.get(),
                    timeout=timeout
                )
                batch.append(item)

            except asyncio.TimeoutError:
                break

        if not batch:
            continue

        prompts = [item["prompt"] for item in batch]

        outputs = run_llm_batch(prompts)

        for item, result in zip(batch, outputs):
            item["future"].set_result(result)
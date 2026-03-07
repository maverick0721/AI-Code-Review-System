import asyncio

review_queue = asyncio.Queue()

async def enqueue(item):
    await review_queue.put(item)

async def dequeue_batch(max_batch=8):

    batch = []

    while len(batch) < max_batch:

        try:
            item = review_queue.get_nowait()
            batch.append(item)
        except asyncio.QueueEmpty:
            break

    return batch
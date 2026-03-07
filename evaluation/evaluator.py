import json
import asyncio
import httpx
from collections import defaultdict

from evaluation.metrics import compute_precision, compute_recall, compute_f1


SERVER_URL = "http://localhost:8000/review"

# IMPORTANT
CONCURRENCY = 4
MAX_RETRIES = 3
REQUEST_TIMEOUT = 180


def normalize(text):
    return text.lower().strip()


async def evaluate_sample(client, semaphore, sample):

    prompt = f"Review this code:\n{sample['code']}"

    for attempt in range(MAX_RETRIES):

        try:

            async with semaphore:

                response = await client.post(
                    SERVER_URL,
                    json={"prompt": prompt},
                    timeout=REQUEST_TIMEOUT
                )

            result = response.json()

            predicted = result["results"][0]["issue"].lower()
            expected = normalize(sample["expected_issue"])

            return predicted, expected

        except Exception:

            if attempt == MAX_RETRIES - 1:
                return "none", normalize(sample["expected_issue"])

            await asyncio.sleep(2)


async def run_async_evaluation(dataset):

    semaphore = asyncio.Semaphore(CONCURRENCY)

    tp = fp = fn = 0
    category_stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    async with httpx.AsyncClient() as client:

        tasks = [
            evaluate_sample(client, semaphore, sample)
            for sample in dataset
        ]

        results = await asyncio.gather(*tasks)

    for predicted, expected in results:

        if predicted == expected:

            tp += 1
            category_stats[expected]["tp"] += 1

        elif predicted == "none":

            fn += 1
            category_stats[expected]["fn"] += 1

        else:

            fp += 1
            category_stats[predicted]["fp"] += 1

    precision = compute_precision(tp, fp)
    recall = compute_recall(tp, fn)
    f1 = compute_f1(precision, recall)

    print("\n===== OVERALL METRICS =====")
    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 3))
    print("F1 Score:", round(f1, 3))


def run_evaluation():

    with open("dataset/security_dataset.json") as f:
    dataset = json.load(f)

    asyncio.run(run_async_evaluation(dataset))


if __name__ == "__main__":
    run_evaluation()
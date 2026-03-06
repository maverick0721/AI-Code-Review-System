import json
import asyncio
import httpx
from collections import defaultdict

from evaluation.metrics import compute_precision, compute_recall, compute_f1


SERVER_URL = "http://localhost:8000/review"
CONCURRENCY = 10


def normalize(text):
    return text.lower().strip()


def extract_predicted_issue(result):
    try:
        return result["results"][0]["issue"].lower()
    except:
        return "none"


async def evaluate_sample(client, sample):

    prompt = f"Review this code:\n{sample['code']}"

    response = await client.post(
        SERVER_URL,
        json={"prompt": prompt},
        timeout=60
    )

    result = response.json()

    predicted = extract_predicted_issue(result)
    expected = normalize(sample["expected_issue"])

    return predicted, expected


async def run_async_evaluation(dataset):

    tp = fp = fn = 0
    category_stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    async with httpx.AsyncClient() as client:

        tasks = [evaluate_sample(client, s) for s in dataset]

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

    print("\n===== PER CATEGORY =====")

    for category, stats in category_stats.items():

        p = compute_precision(stats["tp"], stats["fp"])
        r = compute_recall(stats["tp"], stats["fn"])
        f = compute_f1(p, r)

        print(
            f"{category:25s} "
            f"P={round(p,3)} "
            f"R={round(r,3)} "
            f"F1={round(f,3)}"
        )


def run_evaluation():

    with open("evaluation/dataset.json") as f:
        dataset = json.load(f)

    asyncio.run(run_async_evaluation(dataset))


if __name__ == "__main__":
    run_evaluation()
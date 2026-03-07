import json
import time
import requests
from evaluation.metrics import compute_precision, compute_recall, compute_f1

SERVER_URL = "http://localhost:8000/review"

def run_benchmark():

    with open("evaluation/dataset.json") as f:
        dataset = json.load(f)

    start = time.time()

    tp = fp = fn = 0

    for sample in dataset:

        prompt = sample["code"]

        response = requests.post(
            SERVER_URL,
            json={"prompt": prompt},
            timeout=120
        )

        result = response.json()

        predicted = result["results"][0]["issue"]
        expected = sample["expected_issue"]

        if predicted == expected:
            tp += 1
        elif predicted == "none":
            fn += 1
        else:
            fp += 1

    precision = compute_precision(tp, fp)
    recall = compute_recall(tp, fn)
    f1 = compute_f1(precision, recall)

    runtime = time.time() - start

    print("\n==== BENCHMARK RESULTS ====")
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)
    print("Runtime:", runtime)


if __name__ == "__main__":
    run_benchmark()
import json
import requests

from evaluation.metrics import compute_precision, compute_recall, compute_f1


SERVER_URL = "http://localhost:8000/review"


def run_evaluation():

    with open("evaluation/dataset.json") as f:
        dataset = json.load(f)

    tp = 0
    fp = 0
    fn = 0

    for sample in dataset:

        prompt = f"Review this code:\n{sample['code']}"

        response = requests.post(
            SERVER_URL,
            json={"prompt": prompt}
        )

        result = response.json()

        output_text = str(result)

        if sample["expected_issue"] in output_text:
            tp += 1
        else:
            fn += 1

    precision = compute_precision(tp, fp)
    recall = compute_recall(tp, fn)
    f1 = compute_f1(precision, recall)

    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
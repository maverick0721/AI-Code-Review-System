import time
import requests

SERVER_URL = "http://localhost:8000/review"


def benchmark(n=20):

    prompt = "Review this code: password = '12345'"

    start = time.time()

    for _ in range(n):

        requests.post(
            SERVER_URL,
            json={"prompt": prompt}
        )

    end = time.time()

    total_time = end - start

    latency = total_time / n

    print("Requests:", n)
    print("Total time:", total_time)
    print("Avg latency:", latency)
    print("Requests/sec:", n / total_time)
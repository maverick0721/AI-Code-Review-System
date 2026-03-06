import requests
import os

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000/review")

def send_for_review(prompt):

    try:
        response = requests.post(
            SERVER_URL,
            json={"prompt": prompt},
            timeout=60
        )

        return response.json()

    except Exception as e:

        return {"error": str(e)}
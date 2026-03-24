import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from server.app import app


class TestReviewEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_review_rejects_empty_prompt(self):
        response = self.client.post("/review", json={"prompt": ""})
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertIn("results", payload)
        self.assertEqual(payload["results"][0]["issue"], "none")

    @patch("server.app.get_cache")
    def test_review_uses_cached_result(self, mock_get_cache):
        mock_get_cache.return_value = {
            "issue": "hardcoded credential",
            "severity": "high",
            "confidence": 0.9,
            "explanation": "cached"
        }

        response = self.client.post("/review", json={"prompt": "password = 'x'"})
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["results"][0]["issue"], "hardcoded credential")

    @patch("server.app.set_cache")
    @patch("server.app.get_cache")
    @patch("server.app.enqueue")
    def test_review_non_cached_path_enqueues_and_caches(self, mock_enqueue, mock_get_cache, mock_set_cache):
        mock_get_cache.return_value = None

        async def fake_enqueue(item):
            item["future"].set_result({
                "issue": "none",
                "severity": "low",
                "confidence": 0.5,
                "explanation": "generated"
            })

        mock_enqueue.side_effect = fake_enqueue

        response = self.client.post("/review", json={"prompt": "print('ok')"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("results", payload)
        self.assertEqual(payload["results"][0]["issue"], "none")
        mock_enqueue.assert_called_once()
        mock_set_cache.assert_called_once()


if __name__ == "__main__":
    unittest.main()

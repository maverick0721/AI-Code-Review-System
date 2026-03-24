import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

import integrations.github_bot as github_bot


class TestGithubWebhook(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(github_bot.app)

    @patch("integrations.github_bot.requests.post")
    @patch("integrations.github_bot.requests.get")
    def test_webhook_processes_diff_and_posts_review(self, mock_get, mock_post):
        diff_text = """diff --git a/app.py b/app.py
index 111..222 100644
--- a/app.py
+++ b/app.py
@@ -1,1 +1,1 @@
+password = \"secret\"
"""

        get_resp = Mock()
        get_resp.status_code = 200
        get_resp.text = diff_text
        get_resp.raise_for_status = Mock()
        mock_get.return_value = get_resp

        ai_resp = Mock()
        ai_resp.status_code = 200
        ai_resp.json.return_value = {
            "results": [
                {
                    "issue": "hardcoded credential",
                    "severity": "high",
                    "confidence": 0.9,
                    "explanation": "Found hardcoded credential"
                }
            ]
        }

        gh_resp = Mock()
        gh_resp.status_code = 201

        mock_post.side_effect = [ai_resp, gh_resp]

        with patch.object(github_bot, "GITHUB_TOKEN", "token"):
            payload = {
                "pull_request": {
                    "number": 7,
                    "diff_url": "https://example.com/diff"
                },
                "repository": {
                    "full_name": "owner/repo"
                }
            }

            response = self.client.post("/github-webhook", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "review_posted")
        self.assertGreaterEqual(mock_post.call_count, 2)

        ai_call = mock_post.call_args_list[0]
        self.assertIn("prompt", ai_call.kwargs["json"])

    def test_webhook_ignores_non_pr_events(self):
        response = self.client.post("/github-webhook", json={"zen": "ping"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ignored")


if __name__ == "__main__":
    unittest.main()

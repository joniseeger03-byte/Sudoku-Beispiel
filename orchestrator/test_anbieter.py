import io
import json
import os
import unittest
import urllib.error
from unittest.mock import patch

import orchestrator.agents as agents



class AnbieterTest(unittest.TestCase):
    def test_api_call_falls_back_to_openrouter_on_groq_403(self):
        cfg = {
            "anbieter": {
                "groq": {"url": "https://api.groq.com/openai/v1", "key": "GROQ_API_KEY", "modell": "llama-3.3-70b-versatile"},
                "openrouter": {"url": "https://openrouter.ai/api/v1", "key": "OPENROUTER_API_KEY", "modell": "google/gemma-3-27b-it:free"},
            }
        }

        with patch.dict(os.environ, {"GROQ_API_KEY": "g", "OPENROUTER_API_KEY": "o"}, clear=False):
            calls = []

            class GroqResponse:
                headers = {"Content-Type": "application/json"}

                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

                def read(self):
                    return json.dumps({"choices": [{"message": {"content": "OK"}}]}).encode("utf-8")

            def fake_urlopen(req, timeout=300):
                calls.append(req.full_url)
                if req.full_url.startswith("https://api.groq.com/openai/v1"):
                    raise urllib.error.HTTPError(req.full_url, 403, "error code: 1010", hdrs=None, fp=io.BytesIO(b'{"error":"forbidden"}'))
                return GroqResponse()

            with patch("orchestrator.agents.urllib.request.urlopen", side_effect=fake_urlopen):
                self.assertEqual(agents.api_call(cfg, "groq", "Hallo"), "OK")

            self.assertEqual(calls[0], "https://api.groq.com/openai/v1/chat/completions")
            self.assertEqual(calls[1], "https://openrouter.ai/api/v1/chat/completions")


if __name__ == "__main__":
    unittest.main()

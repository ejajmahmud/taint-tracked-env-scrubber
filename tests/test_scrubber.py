"""Unit tests for taint-tracked-env-scrubber."""
import unittest
from taint_tracked_env_scrubber.scrubber import TaintTrackedEnvScrubber


class TestTaintTrackedEnvScrubber(unittest.TestCase):
    def test_scrub_sensitive_keys(self):
        s = TaintTrackedEnvScrubber()
        env = {"GITHUB_TOKEN": "secret123", "SAFE_VAR": "hello"}
        res = s.scrub(env)
        self.assertEqual(res["GITHUB_TOKEN"], "[REDACTED_GITHUB_TOKEN]")
        self.assertEqual(res["SAFE_VAR"], "hello")

    def test_high_entropy_value_scrubbing(self):
        s = TaintTrackedEnvScrubber()
        env = {"RANDOM_NAME": "a" * 35}
        res = s.scrub(env)
        self.assertTrue(res["RANDOM_NAME"].startswith("[REDACTED_"))

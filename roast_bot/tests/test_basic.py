import unittest
import sys
import os

# Ensure we can import from src
sys.path.append(os.getcwd())

from src.config import Config
from src.safety import SafetyManager
from src.learning import Learner

class MockConfig:
    def __init__(self):
        self.REDDIT_USERNAME = "RoastBot"
        self.banned_keywords = ["badword", "hate"]
        self.max_replies_per_hour = 5
        self.reply_probability = 1.0

class TestSafety(unittest.TestCase):
    def setUp(self):
        self.config = MockConfig()
        self.safety = SafetyManager(self.config)

    def test_banned_keywords(self):
        self.assertFalse(self.safety.is_safe_content("This is a badword"))
        self.assertTrue(self.safety.is_safe_content("This is fine"))

    def test_rate_limit(self):
        # Should be able to reply initially
        self.assertTrue(self.safety.can_reply_rate_limit())

        # Record 5 replies
        for _ in range(5):
            self.safety.record_reply()

        # Should be blocked now
        self.assertFalse(self.safety.can_reply_rate_limit())

class TestLearning(unittest.TestCase):
    def setUp(self):
        self.test_data_path = "tests/test_data.json"
        # Ensure dir exists
        os.makedirs("tests", exist_ok=True)
        self.learner = Learner(data_path=self.test_data_path)

    def tearDown(self):
        if os.path.exists(self.test_data_path):
            os.remove(self.test_data_path)

    def test_process_comment(self):
        # Process a comment with slang
        self.learner.process_comment("bhai this is crazy fr")

        # Check if slang was counted
        counts = self.learner.data["slang_counts"]
        self.assertTrue(counts.get("bhai") >= 1)
        self.assertTrue(counts.get("fr") >= 1)

    def test_context_prompt(self):
        self.learner.process_comment("bhai")
        prompt = self.learner.get_context_prompt()
        self.assertIn('"bhai"', prompt)

if __name__ == '__main__':
    unittest.main()

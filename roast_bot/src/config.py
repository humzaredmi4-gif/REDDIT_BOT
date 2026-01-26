import os
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self._load_config()
        self._load_env_vars()

    def _load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                self.data = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found at {self.config_path}. Using defaults or env vars only.")
            self.data = {}

    def _load_env_vars(self):
        # Reddit Creds
        self.REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
        self.REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
        self.REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
        self.REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
        self.REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

        # LLM Creds
        self.LLM_API_KEY = os.getenv("LLM_API_KEY")
        self.LLM_BASE_URL = os.getenv("LLM_BASE_URL")

    @property
    def subreddits(self):
        return self.data.get("subreddits", [])

    @property
    def reply_probability(self):
        return self.data.get("reply_probability", 0.1)

    @property
    def max_replies_per_hour(self):
        return self.data.get("max_replies_per_hour", 10)

    @property
    def min_reply_delay_seconds(self):
        return self.data.get("min_reply_delay_seconds", 30)

    @property
    def max_reply_delay_seconds(self):
        return self.data.get("max_reply_delay_seconds", 120)

    @property
    def banned_keywords(self):
        return self.data.get("banned_keywords", [])

    @property
    def llm_model(self):
        return self.data.get("llm_model", "llama3-8b-8192")

    @property
    def llm_temperature(self):
        return self.data.get("llm_temperature", 0.8)

    @property
    def llm_system_prompt(self):
        return self.data.get("llm_system_prompt", "")

    @property
    def learning_enabled(self):
        return self.data.get("learning_enabled", True)

# Global config instance
# Note: In a real run, we might want to instantiate this in main.

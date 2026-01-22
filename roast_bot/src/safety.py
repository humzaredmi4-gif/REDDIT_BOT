import time
import re
from collections import deque
from .config import Config

class SafetyManager:
    def __init__(self, config: Config):
        self.config = config
        self.reply_history = deque() # Stores timestamps of replies
        self.bot_username = config.REDDIT_USERNAME

    def _cleanup_history(self):
        """Removes timestamps older than 1 hour."""
        current_time = time.time()
        while self.reply_history and current_time - self.reply_history[0] > 3600:
            self.reply_history.popleft()

    def can_reply_rate_limit(self):
        """Checks if the bot is within the rate limit."""
        self._cleanup_history()
        return len(self.reply_history) < self.config.max_replies_per_hour

    def record_reply(self):
        """Records a successful reply timestamp."""
        self.reply_history.append(time.time())

    def is_safe_content(self, text):
        """Checks if text contains banned keywords."""
        text_lower = text.lower()
        for keyword in self.config.banned_keywords:
            if keyword in text_lower:
                return False
        return True

    def should_skip_author(self, comment):
        """Checks if author is a bot or self."""
        if not comment.author:
            return True # Deleted user

        author_name = comment.author.name

        if author_name == self.bot_username:
            return True

        if "bot" in author_name.lower() and author_name.lower() != "bottom":
             # Simple heuristic for other bots, can be improved
            return True

        return False

    def validate_comment(self, comment):
        """
        Runs all checks on a comment.
        Returns (bool, str) -> (is_valid, reason)
        """
        if self.should_skip_author(comment):
            return False, "Author is bot or self"

        if not self.is_safe_content(comment.body):
            return False, "Contains banned keywords"

        # Check for very short comments (spam)
        if len(comment.body.strip()) < 5:
            return False, "Comment too short"

        return True, "Valid"

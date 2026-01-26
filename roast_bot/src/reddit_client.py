import praw
import time
from .config import Config

class RedditClient:
    def __init__(self, config: Config):
        self.config = config
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            username=config.REDDIT_USERNAME,
            password=config.REDDIT_PASSWORD,
            user_agent=config.REDDIT_USER_AGENT
        )
        self.user_me = None

    def authenticate(self):
        """Verifies authentication."""
        try:
            self.user_me = self.reddit.user.me()
            print(f"Authenticated as: {self.user_me}")
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise e

    def stream_comments(self):
        """Streams comments from configured subreddits."""
        subreddits_str = "+".join(self.config.subreddits)
        subreddit = self.reddit.subreddit(subreddits_str)

        print(f"Streaming comments from: {subreddits_str}")

        # skip_existing=True ensures we only see new comments
        for comment in subreddit.stream.comments(skip_existing=True):
            yield comment

    def reply(self, comment, text):
        """Replies to a comment."""
        try:
            comment.reply(text)
            print(f"Replied to comment {comment.id}")
            return True
        except Exception as e:
            print(f"Failed to reply to comment {comment.id}: {e}")
            return False

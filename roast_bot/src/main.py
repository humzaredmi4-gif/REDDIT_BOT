import time
import random
import sys
from .config import Config
from .reddit_client import RedditClient
from .safety import SafetyManager
from .learning import Learner
from .llm_client import LLMClient

def main():
    # 1. Initialize
    print("Starting RoastBot...")
    config = Config()

    # Check if critical env vars are set
    if not config.REDDIT_CLIENT_ID or not config.LLM_API_KEY:
        print("Error: Missing environment variables. Please check .env file.")
        sys.exit(1)

    reddit = RedditClient(config)
    safety = SafetyManager(config)
    learner = Learner()
    llm = LLMClient(config)

    # 2. Authenticate
    try:
        reddit.authenticate()
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

    print(f"Listening on subreddits: {config.subreddits}")

    # 3. Stream Loop
    try:
        for comment in reddit.stream_comments():
            try:
                # 4. Process Comment

                # Update learner with every comment seen (to learn from the community)
                # But maybe only valid text?
                if comment.body and comment.author and comment.author.name != config.REDDIT_USERNAME:
                     if config.learning_enabled:
                         learner.process_comment(comment.body)

                # Safety Checks
                is_valid, reason = safety.validate_comment(comment)
                if not is_valid:
                    # print(f"Skipped comment {comment.id}: {reason}") # Verbose
                    continue

                # Probability Check
                if random.random() > config.reply_probability:
                    continue

                # Rate Limit Check
                if not safety.can_reply_rate_limit():
                    print("Rate limit reached. Skipping.")
                    continue

                print(f"\n[!] Processing comment {comment.id} by {comment.author}: \"{comment.body[:50]}...\"")

                # Generate Reply
                learned_context = learner.get_context_prompt() if config.learning_enabled else ""
                reply_text = llm.generate_reply(comment.body, learned_context)

                if not reply_text:
                    print("Failed to generate reply.")
                    continue

                # Post Reply
                success = reddit.reply(comment, reply_text)

                if success:
                    safety.record_reply()
                    print(f"--> Replied: \"{reply_text[:50]}...\"")

                    # Random Delay
                    delay = random.randint(config.min_reply_delay_seconds, config.max_reply_delay_seconds)
                    print(f"Sleeping for {delay} seconds...")
                    time.sleep(delay)

            except KeyboardInterrupt:
                print("Stopping...")
                break
            except Exception as e:
                print(f"Error processing comment: {e}")
                time.sleep(5) # Brief pause on error

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Stream error: {e}")

if __name__ == "__main__":
    main()

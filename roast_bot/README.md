# Hinglish Gen-Z Roast Bot 🤖🌶️

A Reddit bot that reads comments in real-time, generates humorous/sarcastic Hinglish replies using an LLM, and learns slang from the community.

## Features

- **Real-time Streaming**: Listens to new comments on configured subreddits.
- **Gen-Z Roast Engine**: Uses LLM (Groq/OpenAI compatible) to generate funny, sarcastic replies in Hinglish.
- **Self-Learning**: Learns new slang and sentence patterns from user comments to stay relevant.
- **Safety First**: Filters out hate speech, politics, self-replies, and spam.
- **Rate Limiting**: Configurable delays and max replies per hour to avoid bans.
- **Anti-Ban**: Random delays and probability-based replying.

## Prerequisites

- Python 3.9+
- A Reddit Account (for API keys)
- An LLM Provider API Key (Groq is recommended for free tier speed)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo_url>
cd roast_bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. API Configuration

#### Reddit API
1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click "create another app..."
3. Select **script**.
4. Name it (e.g., `RoastBot`).
5. Set redirect uri to `http://localhost:8080` (doesn't matter for script).
6. Note down the `client_id` (under the name) and `client_secret`.

#### LLM API (Groq Example)
1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Create a new API Key.
3. Note the key.

### 4. Environment Variables
Copy `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_bot_username
REDDIT_PASSWORD=your_bot_password
REDDIT_USER_AGENT=android:com.example.roastbot:v1.0 (by /u/your_username)

LLM_API_KEY=gsk_...
LLM_BASE_URL=https://api.groq.com/openai/v1
```

### 5. Configuration (Optional)
Edit `config.yaml` to change:
- Target subreddits (`subreddits`)
- Reply frequency (`reply_probability`)
- Banned keywords
- Prompt style

## Running Locally

```bash
python -m src.main
```
*Note: Run from the root directory.*

## Docker Deployment

1. **Build the image:**
```bash
docker build -t roastbot .
```

2. **Run the container:**
```bash
docker run -d --env-file .env --name roastbot-instance roastbot
```

## Troubleshooting

- **401 Unauthorized**: Check your Reddit username/password/client_id/secret in `.env`.
- **429 Too Many Requests**: You are hitting Reddit's rate limit. Increase `min_reply_delay_seconds` in `config.yaml`.
- **LLM Error**: Check your `LLM_API_KEY` or quota. If using a local LLM (Ollama), set `LLM_BASE_URL` to `http://localhost:11434/v1`.
- **Bot not replying**:
    - Check `reply_probability` in `config.yaml` (set to 1.0 for testing).
    - Check if the subreddit is active.
    - Check logs for "Skipped comment".

## Disclaimer
This bot is for entertainment purposes. Ensure you comply with Reddit's API Terms of Use and the rules of the subreddits you deploy to.

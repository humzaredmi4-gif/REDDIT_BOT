import openai
from .config import Config

class LLMClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = openai.OpenAI(
            base_url=self.config.LLM_BASE_URL,
            api_key=self.config.LLM_API_KEY
        )

    def generate_reply(self, comment_text, learned_context=""):
        """Generates a reply using the LLM."""

        system_prompt = self.config.llm_system_prompt
        if learned_context:
            system_prompt += f"\n\nContext from other users (Learn from this style):\n{learned_context}"

        user_prompt = f"Reddit Comment: \"{comment_text}\"\n\nReply:"

        try:
            response = self.client.chat.completions.create(
                model=self.config.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.llm_temperature,
                max_tokens=150,
            )

            reply = response.choices[0].message.content.strip()

            # Post-processing to ensure constraints
            reply = self._enforce_format(reply)
            return reply

        except Exception as e:
            print(f"LLM Generation Error: {e}")
            return None

    def _enforce_format(self, text):
        """Ensures the output follows the strict formatting rules."""
        # 1. Lowercase preference (soft enforcement, let's just lower it mostly or leave it to LLM?
        # The prompt says "Prefer lowercase". I'll force lowercase to be safe/consistent style).
        # Actually, Gen-Z style is often mixed or lowercase. Let's do lowercase.
        text = text.lower()

        # 2. Check for "i am a bot"
        if "i am a bot" not in text:
            text += "\n\ni am a bot"

        # 3. Ensure "i am a bot" is on a new line if it was appended inline by LLM
        # e.g. "haha lol. i am a bot" -> "haha lol.\n\ni am a bot"
        # The prompt says "final line: 'i am a bot'".

        lines = text.split('\n')
        # Remove empty lines from end
        while lines and not lines[-1].strip():
            lines.pop()

        if lines and "i am a bot" in lines[-1]:
            # It's there, make sure it's the *only* thing on that line if possible or just leave it.
            pass
        else:
            text += "\n\ni am a bot"

        # 4. Limit length (1-3 sentences).
        # Hard to enforce strictly with regex, trusting LLM + max_tokens.

        return text

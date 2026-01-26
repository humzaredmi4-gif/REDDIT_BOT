import json
import os
import re
from collections import Counter
from typing import List, Dict

class Learner:
    def __init__(self, data_path="data/learning_data.json"):
        self.data_path = data_path
        self.data = self._load_data()

        # Pre-seed if empty
        if not self.data.get("slang_counts"):
            self.data["slang_counts"] = {
                "bhai": 1, "yaar": 1, "fr": 1, "ngl": 1, "cap": 1,
                "sus": 1, "dead": 1, "lol": 1, "lmao": 1, "ded": 1,
                "scene": 1, "sorted": 1, "beta": 1, "uncle": 1
            }
        if not self.data.get("recent_comments"):
            self.data["recent_comments"] = []

        self.common_slang_patterns = [
            r"\b(bhai)\b", r"\b(yaar)\b", r"\b(fr)\b", r"\b(ngl)\b",
            r"\b(cap)\b", r"\b(no cap)\b", r"\b(sus)\b", r"\b(cringe)\b",
            r"\b(lol)\b", r"\b(lmao)\b", r"\b(ded)\b", r"\b(based)\b"
        ]

    def _load_data(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_data(self):
        # Keep recent_comments size manageable
        if len(self.data.get("recent_comments", [])) > 50:
             self.data["recent_comments"] = self.data["recent_comments"][-50:]

        try:
            with open(self.data_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving learning data: {e}")

    def process_comment(self, text: str):
        """Learns from the comment text."""
        # 1. Update recent comments buffer
        self.data.setdefault("recent_comments", []).append(text)

        # 2. Update slang counts
        counts = self.data.setdefault("slang_counts", {})
        text_lower = text.lower()

        for pattern in self.common_slang_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # match might be a tuple if groups are used, but here they are simple groups
                word = match if isinstance(match, str) else match[0]
                counts[word] = counts.get(word, 0) + 1

        self._save_data()

    def get_context_prompt(self) -> str:
        """Returns a string to append to the system prompt."""
        # Get top 5 slang words
        counts = self.data.get("slang_counts", {})
        top_slang = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
        slang_list = ", ".join([f'"{word}"' for word, count in top_slang])

        # Get 2 recent comments as style examples (if available)
        recent = self.data.get("recent_comments", [])
        examples = ""
        if len(recent) >= 2:
            examples = f"\nRecent user comments to mimic tone from:\n1. {recent[-1]}\n2. {recent[-2]}"

        return f"\nPopular slang right now: {slang_list}.{examples}"

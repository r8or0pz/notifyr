import os
import time
import random
import urllib.parse
from typing import List

import requests
import google.generativeai as genai

TIP_DELIMITER: str = "---TIP_DELIMITER---"
PROMPTS_FILE: str = 'prompts.txt'


class Notifyr:
    """Generate DevOps tips with Gemini and notify via ntfy.sh."""
    def __init__(self):
        """Initialize Gemini client, notification context, and prompt list."""
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model: genai.GenerativeModel = genai.GenerativeModel(os.environ['GENERATIVE_MODEL'])
        self.topic: str = os.environ["NOTIFICATION_TOPIC"]
        self.notification_title: str = os.environ.get("NOTIFICATION_TITLE", "💡 DevOps/SRE Tip")
        self.requested_tips: int = int(os.environ.get("NUMBER_OF_TIPS", 1))
        self.topics: List[str] = self.load_prompts()

    @staticmethod
    def load_prompts() -> List[str]:
        """Return non-empty lines from prompts.txt as topics."""
        with open(os.path.join(os.path.dirname(__file__), PROMPTS_FILE), 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def generate_content(self, selected_topics: List[str]) -> str:
        """Request one formatted tip per topic from Gemini using a single prompt."""
        topics_list = "\n".join([f"- {t}" for t in selected_topics])
        prompt = f"""
You are a highly opinionated, expert-level Senior DevOps/SRE Engineer.
Your task is to provide {len(selected_topics)} SHORT, non-obvious, and highly practical tips (a "gotcha" or a "best practice" that most people miss) that immediately separates juniors from seniors.

You must provide exactly one tip for each of the following topics:
{topics_list}

Your response must be in English.
Format your output strictly as:
Topic: [Specific Area]
Tip: [The non-obvious trick]
{TIP_DELIMITER}
Topic: [Specific Area]
Tip: [The non-obvious trick]
...

Do NOT include any introductory or concluding remarks. Just the formatted tips separated by the delimiter "{TIP_DELIMITER}".
"""
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                print(f"Generating content from Gemini (Attempt {attempt + 1}/{max_retries})...")
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    return f"Content Generation Error after {max_retries} attempts: {e}"

    def send_notification(self, message: str) -> None:
        """Send a tip message to ntfy.sh with quick-search helper actions."""
        try:
            print(f"Sending notification to ntfy.sh/{self.topic}...")

            google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(message)}"

            requests.post(
                f"https://ntfy.sh/{self.topic}",
                data=message.encode('utf-8'),
                headers={
                    "Title": self.notification_title.encode('utf-8'),
                    "Priority": "default",
                    "Actions": f"view, Google It, {google_search_url}"
                }
            )
            print("Notification sent successfully.")
        except Exception as e:
            print(f"Notification Error: Could not send to ntfy.sh: {e}")

    def run(self) -> None:
        """Generate the desired number of tips and push each as a notification."""
        num_tips = min(self.requested_tips, len(self.topics)) if self.topics else 0

        if num_tips == 0:
            print("No topics available to generate tips.")
            return

        selected_topics = random.sample(self.topics, num_tips)
        combined_tips_text = self.generate_content(selected_topics)

        if combined_tips_text.startswith("Content Generation Error"):
            print(combined_tips_text)
            return

        tips: List[str] = [tip.strip() for tip in combined_tips_text.split(TIP_DELIMITER) if tip.strip()]

        for i, tip in enumerate(tips):
            print(f"--- Sending tip {i + 1}/{len(tips)} ---")
            self.send_notification(tip)
            if i < len(tips) - 1:
                time.sleep(2)  # Small delay between notifications


def main() -> None:
    """Entrypoint that creates a notifier and executes its workflow."""
    notifier = Notifyr()
    notifier.run()
if __name__ == "__main__":
    main()

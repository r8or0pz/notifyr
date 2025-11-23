import os
import time
import random
import urllib.parse
import requests
import google.generativeai as genai

def load_prompts():
    with open(os.path.join(os.path.dirname(__file__), 'prompts.txt'), 'r') as f:
        return [line.strip() for line in f if line.strip()]

def generate_content(model, selected_topic):
    prompt = f"""
You are a highly opinionated, expert-level Senior DevOps/SRE Engineer.
Your task is to provide one SHORT, non-obvious, and highly practical tip (a "gotcha" or a "best practice" that most people miss) that immediately separates juniors from seniors.

The tip MUST cover the following topic:
{selected_topic}

Your response must be in English.
Format your output strictly as: "Topic: [Specific Area]\\nTip: [The non-obvious trick]"
Do NOT include any introductory or concluding remarks. Just the formatted tip.
"""
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            print(f"Generating content from Gemini (Attempt {attempt + 1}/{max_retries})...")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                return f"Content Generation Error after {max_retries} attempts: {e}"

def send_notification(topic, title, message):
    try:
        print(f"Sending notification to ntfy.sh/{topic}...")

        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(message)}"

        requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode('utf-8'),
            headers={
                "Title": title.encode('utf-8'),
                "Priority": "default",
                "Actions": f"view, Google It, {google_search_url}"
            }
        )
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Notification Error: Could not send to ntfy.sh: {e}")

def main():
    # --- Configuration ---
    # NOTE: Ensure GEMINI_API_KEY is set as an environment variable (e.g., in GitHub Secrets)
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(os.environ['GENERATIVE_MODEL'])
    topic = os.environ["NOTIFICATION_TOPIC"]
    notification_title = os.environ.get("NOTIFICATION_TITLE", "🔒 DevOps/SRE Tip")

    topics = load_prompts()
    selected_topic = random.choice(topics)

    tip_text = generate_content(model, selected_topic)
    send_notification(topic, notification_title, tip_text)

if __name__ == "__main__":
    main()

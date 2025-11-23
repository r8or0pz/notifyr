import os
import time
import urllib.parse
import requests
import google.generativeai as genai

# --- Configuration ---
# NOTE: Ensure GEMINI_API_KEY is set as an environment variable (e.g., in GitHub Secrets)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(os.environ['GENERATIVE_MODEL'])
topic = os.environ["NOTIFICATION_TOPIC"]
notification_title = os.environ.get("NOTIFICATION_TITLE", "🔒 DevOps/SRE Tip")

prompt = """
You are a highly opinionated, expert-level Senior DevOps/SRE Engineer.
Your task is to provide one SHORT, non-obvious, and highly practical tip (a "gotcha" or a "best practice" that most people miss) that immediately separates juniors from seniors.

The tip MUST cover a complex or niche topic, such as:
1.  **Dependency Management/Supply Chain Security** (e.g., hash pinning, lock file usage, vulnerability scanning tools).
2.  Niche Kubernetes features (e.g., Pod disruption budgets, ephemeral containers for debugging), scaling, security, networking.
3.  Advanced Bash/Zsh scripting (e.g., process substitution, complex pipeline tricks and so on).
4.  Infrastructure as Code (IaC) principles (e.g., Terraform module composition, drift detection).
5.  Hidden features or performance tuning in Docker/containerd (e.g., buildx, rootless mode, or overlayfs specifics).

Your response must be in English.
Format your output strictly as: "Topic: [Specific Area]\nTip: [The non-obvious trick]"
Do NOT include any introductory or concluding remarks. Just the formatted tip.
"""

# --- Execution ---
max_retries = 3
retry_delay = 5

for attempt in range(max_retries):
    try:
        print(f"Generating content from Gemini (Attempt {attempt + 1}/{max_retries})...")
        response = model.generate_content(prompt)
        tip_text = response.text
        break
    except Exception as e:
        print(f"Error on attempt {attempt + 1}: {e}")
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            tip_text = f"Content Generation Error after {max_retries} attempts: {e}"
            print(tip_text)

# Send to ntfy.sh
try:
    print(f"Sending notification to ntfy.sh/{topic}...")

    google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(tip_text)}"

    requests.post(
        f"https://ntfy.sh/{topic}",
        data=tip_text.encode('utf-8'),
        headers={
            "Title": notification_title.encode('utf-8'),
            "Priority": "default",
            "Actions": f"view, Open Gemini, https://gemini.google.com; view, Google It, {google_search_url}"
        }
    )
    print("Notification sent successfully.")
except Exception as e:
    print(f"Notification Error: Could not send to ntfy.sh: {e}")

import os
import requests
import google.generativeai as genai

# --- Configuration ---
# NOTE: Ensure GEMINI_API_KEY is set as an environment variable (e.g., in GitHub Secrets)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(os.environ['GENERATIVE_MODEL'])
topic = os.environ["NOTIFICATION_TOPIC"]

prompt = """
You are a highly opinionated, expert-level Senior DevOps/SRE Engineer.
Your task is to provide one SHORT, non-obvious, and highly practical tip (a "gotcha" or a "best practice" that most people miss) that immediately separates juniors from seniors.

The tip MUST cover a complex or niche topic, such as:
1.  **Dependency Management/Supply Chain Security** (e.g., hash pinning, lock file usage, vulnerability scanning tools).
2.  Niche Kubernetes features (e.g., Pod disruption budgets, ephemeral containers for debugging).
3.  Advanced Bash/Zsh scripting (e.g., process substitution, complex pipeline tricks).
4.  Infrastructure as Code (IaC) principles (e.g., Terraform module composition, drift detection).
5.  Hidden features or performance tuning in Docker/containerd (e.g., buildx, rootless mode, or overlayfs specifics).

Your response must be in English.
Format your output strictly as: "Topic: [Specific Area]\nTip: [The non-obvious trick]"
Do NOT include any introductory or concluding remarks. Just the formatted tip.
"""

# --- Execution ---
try:
    print("Generating content from Gemini...")
    response = model.generate_content(prompt)
    tip_text = response.text
except Exception as e:
    tip_text = f"Content Generation Error: {e}"
    print(tip_text)

# Send to ntfy.sh
try:
    print(f"Sending notification to ntfy.sh/{topic}...")
    requests.post(
        f"https://ntfy.sh/{topic}", 
        data=tip_text.encode('utf-8'),
        headers={
            "Title": "🔒 CI/CD Security Tip",
            "Priority": "default"
        }
    )
    print("Notification sent successfully.")
except Exception as e:
    print(f"Notification Error: Could not send to ntfy.sh: {e}")

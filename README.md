# notifyr

A Python-based tool that generates daily DevOps/SRE tips using Google's Gemini AI and delivers them as push notifications via [ntfy.sh](https://ntfy.sh).

## What It Does

**notifyr** randomly selects topics from a curated list of 39 DevOps/SRE areas (ranging from Kubernetes and Infrastructure as Code to advanced Python optimization and GitOps patterns), generates expert-level tips using Google's Gemini AI, and sends them as push notifications to your devices through ntfy.sh.

Each tip is designed to be:
- **Non-obvious**: Goes beyond basic knowledge
- **Practical**: Immediately applicable in real-world scenarios
- **Senior-level**: Separates juniors from seniors with "gotchas" and best practices

## How It Works

1. **Topic Selection**: Randomly selects topics from `prompts.txt` (39 DevOps/SRE categories)
2. **AI Generation**: Uses Google's Gemini API to generate expert-level tips
3. **Notification Delivery**: Sends tips to ntfy.sh with a "Google It" quick-action button
4. **Automated Schedule**: Runs daily at 07:00 UTC via GitHub Actions

## GitHub Actions Workflow

The workflow (`notify.yaml`) runs automatically:
- **Schedule**: Every day at 07:00 UTC via cron
- **Manual Trigger**: Can be triggered manually via `workflow_dispatch`
- **Environment**: Uses Python 3.13 with `uv` for dependency management
- **Execution**: Runs `main.py` with configured environment variables

## Environment Variables

Required:
- `GEMINI_API_KEY`: Your Google Gemini API key (secret)
- `GENERATIVE_MODEL`: The Gemini model to use (e.g., `gemini-1.5-flash`)
- `NOTIFICATION_TOPIC`: Your ntfy.sh topic name

Optional:
- `NOTIFICATION_TITLE`: Custom notification title (default: "💡 DevOps/SRE Tip")
- `NUMBER_OF_TIPS`: Number of tips to generate per run (default: 1)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/r8or0pz/notifyr.git
   cd notifyr
   ```

2. **Install dependencies** (using uv):
   ```bash
   pip install uv
   uv sync
   ```

3. **Configure environment variables**:
   - Set `GEMINI_API_KEY` as a GitHub secret
   - Set `GENERATIVE_MODEL`, `NOTIFICATION_TOPIC`, and optionally `NUMBER_OF_TIPS` as GitHub variables

4. **Subscribe to notifications**:
   - On your device, subscribe to your ntfy.sh topic (e.g., via the ntfy app or https://ntfy.sh/your-topic-name)

## Local Usage

Run manually with environment variables:
```bash
export GEMINI_API_KEY="your-api-key"
export GENERATIVE_MODEL="gemini-1.5-flash"
export NOTIFICATION_TOPIC="your-topic-name"
export NUMBER_OF_TIPS="1"

uv run python main.py
```

## Features

- **39 DevOps/SRE Topics**: Covers dependency management, Kubernetes, IaC, Docker, networking, observability, GitOps, and more
- **Retry Logic**: Automatically retries Gemini API calls up to 3 times
- **Quick Actions**: Each notification includes a "Google It" button for instant research
- **Batch Support**: Generate multiple tips in a single run
- **Lock File**: Uses `uv.lock` for reproducible dependency installation
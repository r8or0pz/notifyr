# Notifyr 💡

A Python-based notification service that generates daily DevOps/SRE tips using Google's Gemini AI and delivers them via [ntfy.sh](https://ntfy.sh) push notifications.

## Overview

Notifyr is designed to help DevOps engineers and SREs continuously learn through daily, bite-sized expert tips. It leverages Google's Gemini AI to generate non-obvious, practical advice from a curated list of DevOps topics and pushes them as notifications to your devices.

## Features

- 🤖 **AI-Powered Tips**: Uses Google Gemini to generate expert-level DevOps/SRE tips
- 📱 **Push Notifications**: Delivers tips directly to your devices via ntfy.sh
- 🎯 **Curated Topics**: Covers 40+ DevOps topics including Kubernetes, Infrastructure as Code, Security, Observability, and more
- 🎲 **Random Scheduling**: Triggers throughout the day with randomized execution for unpredictable delivery times
- 🔍 **Quick Search**: Each notification includes a "Google It" action for immediate research
- ⚙️ **Configurable**: Customize number of tips, notification title, and topic selection

## How It Works

1. **Topic Selection**: Randomly selects topics from `prompts.txt`
2. **Content Generation**: Sends a prompt to Google Gemini requesting expert-level tips
3. **Tip Parsing**: Parses the AI response into individual tips
4. **Notification Delivery**: Sends each tip as a push notification via ntfy.sh with quick-search actions

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key
- ntfy.sh topic (no account required)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/r8or0pz/notifyr.git
cd notifyr
```

2. Install dependencies:
```bash
pip install uv
uv sync
```

3. Set up environment variables:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export GENERATIVE_MODEL="gemini-1.5-flash"  # or your preferred model
export NOTIFICATION_TOPIC="your-ntfy-topic"
export NUMBER_OF_TIPS="1"  # optional, defaults to 1
export NOTIFICATION_TITLE="💡 DevOps/SRE Tip"  # optional
```

4. Run locally:
```bash
uv run python main.py
```

## GitHub Actions Automation

The included workflow (`.github/workflows/notify.yaml`) runs with randomized scheduling:

- **Schedule**: Triggers 8 times daily durin
- **Random Execution**: Each trigger has a 25% chance of actually running (~2 tips per day at unpredictable times)
- **Manual Trigger**: Can be triggered manually via `workflow_dispatch`

This approach ensures tips arrive at random times throughout your day, keeping the learning experience fresh and unexpected.

### Required Secrets & Variables

Configure these in your GitHub repository settings:

**Secrets:**
- `GEMINI_API_KEY`: Your Google Gemini API key

**Variables:**
- `GENERATIVE_MODEL`: Gemini model name (e.g., `gemini-1.5-flash`)
- `NOTIFICATION_TOPIC`: Your ntfy.sh topic name
- `NUMBER_OF_TIPS`: Number of tips to generate per run (optional, defaults to 1)

## Topics Covered

The `prompts.txt` file includes 40+ DevOps/SRE topics:

- Kubernetes (scaling, security, networking, niche features)
- Infrastructure as Code (Terraform, drift detection)
- Container technologies (Docker, containerd)
- Cloud architecture (AWS limits, cost optimization, serverless)
- Observability (logs, metrics, traces, alert management)
- Security (Zero Trust, secret management, DevSecOps)
- Programming (Go, Python for DevOps/systems programming)
- Tools (Helm, Kustomize, GitOps, CLI tools)
- SRE practices (SLIs/SLOs, incident management, chaos engineering)
- And many more...

## Receiving Notifications

1. Install the ntfy app on your device:
   - [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
   - [iOS](https://apps.apple.com/us/app/ntfy/id1625396347)
   - [Web](https://ntfy.sh)

2. Subscribe to your topic (the one you set in `NOTIFICATION_TOPIC`)

3. Start receiving daily tips!

## Configuration

### Customizing Topics

Edit `prompts.txt` to add, remove, or modify topics. Each line should contain one topic description.

### Adjusting Tip Quantity

Set the `NUMBER_OF_TIPS` environment variable to control how many tips are generated per run (limited by the number of topics in `prompts.txt`).

## Project Structure

```
notifyr/
├── main.py                    # Main application logic
├── prompts.txt                # List of DevOps topics
├── pyproject.toml             # Project dependencies
├── README.md                  # This file
└── .github/
    └── workflows/
        └── notify.yaml        # GitHub Actions workflow
```

## Author

**Roman Borysenko** ([@r8or0pz](https://github.com/r8or0pz))

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:
- Add new topics to `prompts.txt`
- Improve the prompt engineering
- Enhance notification formatting
- Submit bug fixes or feature requests

## Acknowledgments

- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Notifications via [ntfy.sh](https://ntfy.sh)
- Built with [uv](https://github.com/astral-sh/uv)

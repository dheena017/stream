# Streamlit AI Chat App

A powerful, multi-provider AI chat application built with Streamlit, featuring real-time internet search, multimodal capabilities (image & voice), and integrated ethics guardrails.

## Key Features

- **Multi-Model Support**: Seamlessly switch between Google Gemini, OpenAI (GPT-4), and Anthropic (Claude 3).
- **Internet Search**: Augment your chat with real-time information from the web.
- **Multimodal Interaction**:
  - **Image Analysis**: Upload images for captioning and context-aware chat.
  - **Voice Integration**: Speak to the AI and receive audio responses.
- **Smart Conversation**:
  - Context retention with automatic history summarization.
  - Robust retry logic with exponential backoff for API resilience.
- **Ethics & Safety**: Built-in `EthicsGuardian` for bias detection and safe interactions.
- **Dashboard**: Track engagement, API usage, and system health.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- API Keys for at least one provider (Google, OpenAI, or Anthropic)

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Set up your API keys. You can do this via environment variables or Streamlit secrets.

**Option 1: Environment Variables**
Create a `.env` file or export them:
```bash
export GOOGLE_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"
```

**Option 2: Streamlit Secrets**
Create `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "your_key_here"
OPENAI_API_KEY = "your_key_here"
ANTHROPIC_API_KEY = "your_key_here"
```

### Running the App

```bash
streamlit run app.py
```

## Documentation

For more detailed information, check the `docs/` folder:

- [Setup Guide](docs/setup.md): Detailed installation and configuration instructions.
- [Features](docs/features.md): In-depth look at all application capabilities.
- [Troubleshooting](docs/troubleshooting.md): Common issues and how to resolve them.
- [Contributing](CONTRIBUTING.md): Guidelines for contributing to the project.

## Community

Join the conversation!

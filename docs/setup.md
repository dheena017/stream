# Setup & Installation

This guide covers how to set up the Stream Multimodal AI Chat application locally.

## Prerequisites

- **Python 3.8+**
- **Virtual Environment** (Recommended)
- **API Keys** for at least one provider (Google, OpenAI, Anthropic, etc.)

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment**:

    *Linux/macOS:*
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

    *Windows (PowerShell):*
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    > **Note:** Some optional dependencies (like `torch` for local BLIP captioning) are large.

## API Key Configuration

You can configure API keys in two ways: using environment variables (recommended for local dev) or entering them in the UI.

### Option 1: Environment Variables

Set the following environment variables in your shell or a `.env` file (if supported by your runner, though this app reads from `os.getenv` directly).

| Provider | Environment Variable | Description |
| :--- | :--- | :--- |
| **Google** | `GEMINI_API_KEY` | For Gemini Flash, Pro, etc. |
| **OpenAI** | `OPENAI_API_KEY` | For GPT-4o, GPT-4 Turbo, etc. |
| **Anthropic** | `ANTHROPIC_API_KEY` | For Claude 3.5 Sonnet, Haiku. |
| **Together** | `TOGETHER_API_KEY` | For Llama models. |
| **xAI** | `XAI_API_KEY` | For Grok. |
| **DeepSeek** | `DEEPSEEK_API_KEY` | For DeepSeek Chat/Coder. |

### Option 2: UI Configuration

1.  Launch the app.
2.  Open the **Sidebar**.
3.  Expand the **🔑 API Keys** section.
4.  Enter your keys. They will be stored in the session state (and potentially `user_prefs.json` if configured, though environment variables are safer).

## Running the Application

To start the Streamlit server:

```bash
streamlit run app.py
```

The app should open automatically in your browser at `http://localhost:8501`.

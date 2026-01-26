# Setup Guide

This guide covers the detailed steps to set up and run the Streamlit AI Chat App locally.

## Prerequisites

- **Python 3.8+**: Ensure you have a compatible Python version installed.
- **Git**: For cloning the repository.
- **Virtual Environment (Recommended)**: To manage dependencies in isolation.

## Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/streamlit-ai-chat.git
    cd streamlit-ai-chat
    ```

2.  **Create a Virtual Environment**

    ```bash
    python -m venv venv

    # Windows
    venv\Scripts\activate

    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    The project relies on several key libraries including `streamlit`, `openai`, `google-generativeai`, `anthropic`, and others.

    ```bash
    pip install -r requirements.txt
    ```

    *Note: Heavy dependencies like `torch` and `transformers` for local image captioning might be commented out by default. Uncomment them in `requirements.txt` if you need local BLIP support.*

## API Key Configuration

The app supports multiple AI providers. You need to configure at least one to start chatting.

### Obtaining Keys

- **Google (Gemini)**: [Get API Key](https://makersuite.google.com/app/apikey)
- **OpenAI (GPT)**: [Get API Key](https://platform.openai.com/api-keys)
- **Anthropic (Claude)**: [Get API Key](https://console.anthropic.com/)

### Setting Keys

You can use either a `.env` file or Streamlit's secrets management.

#### Method A: .env File (Local Development)

Create a file named `.env` in the root directory:

```env
GOOGLE_API_KEY=your_google_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

#### Method B: Streamlit Secrets (Deployment)

If you are deploying to Streamlit Community Cloud or prefer to use TOML:

Create `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "your_google_key_here"
OPENAI_API_KEY = "your_openai_key_here"
ANTHROPIC_API_KEY = "your_anthropic_key_here"
```

## Running the Application

Once everything is set up, launch the app:

```bash
streamlit run app.py
```

The app should open automatically in your default browser at `http://localhost:8501`.

## Optional Setup

### Internet Search
To enable internet search, you may need a search provider API key (e.g., Google Custom Search or DuckDuckGo). By default, the app uses DuckDuckGo which requires no API key.

### Voice Features
For voice input/output, ensure your system has a working microphone and speakers. On Linux, you might need to install `portaudio19-dev`.

```bash
sudo apt-get install portaudio19-dev  # Debian/Ubuntu
```

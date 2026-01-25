<<<<<<< HEAD
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
=======
# Setup Guide

## Prerequisites

- Python 3.10 or higher
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dheen/stream.git
cd stream
```

### 2. Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: Optional dependencies for advanced features (BLIP, Voice) are included in the requirements file but may require additional system tools (e.g., ffmpeg).*

## Configuration

### API Keys

You can configure API keys in two ways: via environment variables (recommended for development) or directly in the application UI.

#### Method 1: Environment Variables

Create a `.env` file or set these variables in your shell:

- `GEMINI_API_KEY`: Google Gemini API Key
- `OPENAI_API_KEY`: OpenAI API Key
- `ANTHROPIC_API_KEY`: Anthropic Claude API Key
- `TOGETHER_API_KEY`: Together AI Key
- `XAI_API_KEY`: xAI (Grok) API Key
- `DEEPSEEK_API_KEY`: DeepSeek API Key

#### Method 2: UI Configuration

1. Launch the application.
2. Open the Sidebar.
3. Expand the **🔑 API Keys** section.
4. Enter your keys in the respective fields.

*Note: Keys entered in the UI are stored in the session state and are not saved permanently to disk for security.*

## Running the Application

To start the Streamlit app:
>>>>>>> origin/docs-update-5816964673776763608

```bash
streamlit run app.py
```

<<<<<<< HEAD
The app should open automatically in your browser at `http://localhost:8501`.
=======
The application will open in your default web browser at `http://localhost:8501`.

## Optional Setup

### Hosted Caption API (Advanced)
If you wish to use a hosted captioning service instead of the local BLIP model, refer to [Hosted Caption Setup](hosted_caption_setup.md).

### Internet Search
Internet search via DuckDuckGo is enabled by default but can be toggled. See [Internet Search Guide](internet_search_guide.md) for details.
>>>>>>> origin/docs-update-5816964673776763608

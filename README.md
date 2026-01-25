# Stream — Multimodal AI Chat

Stream is a powerful, Streamlit-based AI chat interface that supports multiple providers (Google, OpenAI, Anthropic, etc.), multimodal inputs (images, audio, video), and real-time internet search augmentation.

## 🚀 Key Features

-   **Multi-Provider Support:** Switch seamlessly between Gemini, GPT-4, Claude, Llama, Grok, and DeepSeek.
-   **🧠 Brain Mode:** Use an ensemble of models to synthesize the best possible answer.
-   **🌐 Internet Search:** Real-time web and news search to ground answers in current events.
-   **📎 Multimodal:** Upload images, PDFs, text files, audio, and video for analysis.
-   **🖼️ Advanced Vision:** Integrated BLIP model for local image captioning or use hosted APIs.

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

-   [**Setup & Installation**](docs/setup.md): Installation steps and API key configuration.
-   [**Features Guide**](docs/features.md): In-depth look at Brain Mode, Search, and more.
-   [**Troubleshooting**](docs/troubleshooting.md): Common issues and fixes.
-   [**Hosted Caption Setup**](docs/HOSTED_CAPTION_SETUP.md): Configuring external captioning APIs.

## ⚡ Quick Start

1.  **Clone and Install:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
    pip install -r requirements.txt
    ```

2.  **Set API Keys:**
    ```bash
    export GEMINI_API_KEY="your-key-here"
    export OPENAI_API_KEY="your-key-here"
    # See docs/setup.md for all keys
    ```

3.  **Run:**
    ```bash
    streamlit run app.py
    ```

## Tests

Run the smoke tests to ensure the environment is set up correctly:

```bash
pytest -q tests/test_multimodal_smoke.py
```

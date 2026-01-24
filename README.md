# Stream — Multimodal AI Chat

This project is a Streamlit-based multi-provider AI chat with multimodal (image/audio/video) support, internet search augmentation, and optional advanced image captioning.

## 🚀 Quick Start

1.  **Clone and Setup**:
    ```powershell
    git clone https://github.com/dheen/stream.git
    cd stream
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1  # Windows
    # source .venv/bin/activate   # Mac/Linux
    pip install -r requirements.txt
    ```

2.  **Run**:
    ```powershell
    streamlit run app.py
    ```

3.  **Configure**:
    Open the sidebar in the app to enter your API keys (Google, OpenAI, Anthropic, etc.).

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- [**Setup Guide**](docs/setup.md): Detailed installation and API key configuration.
- [**Features Guide**](docs/features.md): Learn about Brain Mode, Voice, and more.
- [**Internet Search**](docs/internet_search_guide.md): How to use the integrated web search.
- [**Hosted Captioning**](docs/hosted_caption_setup.md): Setup for advanced image captioning.

## ✨ Key Features

- **Multi-Provider**: Unified interface for Google Gemini, GPT-4, Claude 3.5, Llama 3, and more.
- **Multimodal**: Support for Images, Audio, and Video inputs.
- **Brain Mode**: Advanced reasoning with Internet Search and Auto-Model selection.
- **Voice Mode**: Real-time voice interaction and text-to-speech.
- **Privacy Focused**: Local history storage and encrypted keys in session.

## 🔧 Troubleshooting

### Common Issues

**1. "Module not found" errors:**
Ensure you have activated your virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

**2. API Key Errors:**
If you see authentication errors, verify your keys in the Sidebar > **🔑 API Keys** section. Ensure they are valid and have credits.

**3. Audio/Video features not working:**
Some multimodal features require system-level dependencies like `ffmpeg`. Refer to the [Setup Guide](docs/setup.md) for details.

**4. Search not working:**
Internet search requires an active internet connection. Check if "Enable Internet Search" is toggled in the Brain Mode settings.

## Tests & CI

A lightweight pytest smoke test is provided at `tests/test_multimodal_smoke.py`.

Run tests locally:
```powershell
pytest -q
```

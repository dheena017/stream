<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# Stream — Multimodal AI Chat

<<<<<<< HEAD
This project is a Streamlit-based multi-provider AI chat with multimodal (image/audio/video) support, internet search augmentation, and optional advanced image captioning via BLIP or a hosted caption API.

<<<<<<< HEAD
=======
## Supported Providers
- Google (Gemini)
- OpenAI (GPT-4o, etc.)
- Anthropic (Claude)
- Together AI (Llama)
- xAI (Grok)
- DeepSeek
- Groq (Llama, Mixtral)

>>>>>>> api-groq-integration-6554511320622598819
## BLIP (Optional)
- BLIP model (`Salesforce/blip-image-captioning-base`) is optional and will be downloaded on first preload.
- To enable advanced captioning in the UI, toggle "Enable Advanced Image Captioning (BLIP)" in the chat page and optionally provide a Hosted Caption API URL.
- If BLIP is not desired, the app falls back to simple heuristic captions (image size/metadata) or a hosted caption API when configured.

## Hosted Caption API
- Provide an endpoint that accepts multipart image uploads and returns JSON containing `caption` or `text` fields.
- The app will prefer the hosted caption API if configured, then BLIP (if available), then fallback heuristics.

<<<<<<< HEAD
<<<<<<< HEAD
=======
## Documentation
- [Hosted Caption Setup](docs/HOSTED_CAPTION_SETUP.md)
- [Internet Search Guide](docs/INTERNET_SEARCH_GUIDE.md)
- [Internet Search Quickstart](docs/INTERNET_SEARCH_QUICKSTART.md)
- [Internet Search Summary](docs/INTERNET_SEARCH_SUMMARY.md)
- [Internet Search Verification](docs/INTERNET_SEARCH_VERIFICATION.md)

## Community
- **Active Contributors**: 5+
- **Latest Release**: v1.0.0
- **Issues**: Check GitHub Issues for latest updates.

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

>>>>>>> 948b4f4 (Community: [PR merges/docs])
=======
>>>>>>> api-groq-integration-6554511320622598819
## Running locally
Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run Streamlit:

=======
# Antigravity AI — Multimodal Chat Application

**Antigravity AI** is a sophisticated Streamlit-based chat interface that integrates multiple AI providers, multimodal support (Voice, Image, Video), and real-time internet search capabilities.

## ✨ Features
- **Multi-Provider Support:** Connect with OpenAI, Google Gemini, Anthropic Claude, and local models.
- **AI Brain Mode:** Advanced learning capabilities and thought processing for better answers.
- **Multimodal Interactions:**
    - 🗣️ **Voice Integration:** Speak to the AI and hear responses.
    - 🖼️ **Image Analysis:** Upload images for captioning and Q&A.
    - 📹 **Video/Audio:** Analyze media files.
- **Internet Search:** Augment AI responses with real-time data from the web (via DuckDuckGo).
- **User System:** Authentication, User Profiles, and Preferences (Dark Mode).

## 🚀 Quick Start

### 1. Installation
Create and activate a virtual environment, then install dependencies:

```powershell
# Create venv
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate.ps1
# Activate (Linux/Mac)
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the App
>>>>>>> origin/docs-update-v1-11532887947141402034
```powershell
streamlit run app.py
```

<<<<<<< HEAD
## Tests & CI
- A lightweight pytest smoke test is provided at `tests/test_multimodal_smoke.py` to validate multimodal helpers without requiring heavy optional dependencies.
- A GitHub Actions workflow `.github/workflows/multimodal-smoke.yml` runs the tests on push and PR.

Run tests locally:

<<<<<<< HEAD
<<<<<<< HEAD
```bash
PYTHONPATH=. pytest -q
=======
```powershell
pytest -q
>>>>>>> 948b4f4 (Community: [PR merges/docs])
=======
```powershell
pytest -q
>>>>>>> api-groq-integration-6554511320622598819
```

## Notes
- Optional dependencies: `transformers`, `torch`, `torchvision`, `moviepy`, `speech_recognition`. These are only required for BLIP, video frame extraction, and audio transcription respectively.
- Search library may warn about `duckduckgo_search` -> `ddgs` rename; consider installing `ddgs` if you see warnings.
=======
Stream is a powerful, Streamlit-based AI chat interface that supports multiple providers (Google, OpenAI, Anthropic, etc.), multimodal inputs (images, audio, video), and real-time internet search augmentation.

## 🚀 Key Features

-   **Multi-Provider Support:** Switch seamlessly between Gemini, GPT-4, Claude, Llama, Grok, and DeepSeek.
-   **🧠 Brain Mode:** Use an ensemble of models to synthesize the best possible answer.
-   **🌐 Internet Search:** Real-time web and news search to ground answers in current events.
-   **📎 Multimodal:** Upload images, PDFs, text files, audio, and video for analysis.
-   **🖼️ Advanced Vision:** Integrated BLIP model for local image captioning or use hosted APIs.
=======
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
>>>>>>> origin/docs-update-5816964673776763608

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

<<<<<<< HEAD
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
>>>>>>> origin/docs-update-restructure-8689810046199683690
=======
# Stream — Multimodal AI Chat

This project is a Streamlit-based multi-provider AI chat with multimodal (image/audio/video) support, internet search augmentation, and optional advanced image captioning via BLIP or a hosted caption API.

## BLIP (Optional)
- BLIP model (`Salesforce/blip-image-captioning-base`) is optional and will be downloaded on first preload.
- To enable advanced captioning in the UI, toggle "Enable Advanced Image Captioning (BLIP)" in the chat page and optionally provide a Hosted Caption API URL.
- If BLIP is not desired, the app falls back to simple heuristic captions (image size/metadata) or a hosted caption API when configured.

## Hosted Caption API
- Provide an endpoint that accepts multipart image uploads and returns JSON containing `caption` or `text` fields.
- The app will prefer the hosted caption API if configured, then BLIP (if available), then fallback heuristics.

## Experimental Features
- **Chat Export (Beta):** Export your conversation history to JSON or Markdown formats directly from the chat interface.

## Running locally
Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run Streamlit:

```powershell
streamlit run app.py
```

## Tests & CI
- A lightweight pytest smoke test is provided at `tests/test_multimodal_smoke.py` to validate multimodal helpers without requiring heavy optional dependencies.
- A GitHub Actions workflow `.github/workflows/multimodal-smoke.yml` runs the tests on push and PR.

Run tests locally:

```powershell
pytest -q
```

## Community
- We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.
- Join our community to discuss features, report bugs, and share your ideas.

## Notes
- Optional dependencies: `transformers`, `torch`, `torchvision`, `moviepy`, `speech_recognition`. These are only required for BLIP, video frame extraction, and audio transcription respectively.
- Search library may warn about `duckduckgo_search` -> `ddgs` rename; consider installing `ddgs` if you see warnings.
>>>>>>> origin/community-docs-update-9641192155439230832
=======
### 3. Login
Use the default credentials to access the system:
- **Username:** `admin`
- **Password:** `admin123`

*See [User Guide](docs/USER_GUIDE.md) for more details.*

## ⚙️ Configuration

### Environment Variables
You can configure the application using environment variables or by editing `config.py` (if applicable).

- `GOOGLE_CLIENT_ID`: For Google OAuth login.
- `GOOGLE_REDIRECT_URI`: Redirect URI for Google OAuth (default: `http://localhost:8501`).
- `ADMIN_PASSWORD`: Override default admin password.

### API Keys
To use specific AI models, you may need to provide API keys in the UI or environment variables depending on the provider setup.

## 📚 Documentation
- **[User Guide](docs/USER_GUIDE.md):** Detailed instructions on using the chat, dashboard, and settings.
- **[Troubleshooting](docs/TROUBLESHOOTING.md):** Solutions for common issues.
- **[Internet Search Guide](docs/INTERNET_SEARCH_GUIDE.md):** Deep dive into the web search integration.
- **[Hosted Caption Setup](docs/HOSTED_CAPTION_SETUP.md):** How to set up a remote GPU server for faster image captioning.

## 🧠 Advanced Features

### BLIP (Image Captioning)
- The app supports local image captioning using the BLIP model (`Salesforce/blip-image-captioning-base`).
- **Note:** This requires downloading ~1GB model files on first use.
- To enable: Toggle "Enable Advanced Image Captioning (BLIP)" in the chat settings.

### Hosted Caption API
- Offload image processing to a remote server.
- Useful for running the app on non-GPU machines.
- See `docs/HOSTED_CAPTION_SETUP.md` for deployment instructions.

## 🧪 Tests & CI
A lightweight pytest smoke test is provided:

```powershell
pytest -q
```

## Notes
- **Optional Dependencies:** `transformers`, `torch`, `torchvision`, `moviepy`, `speech_recognition`. These are installed via `requirements.txt` but are only critical for specific features (BLIP, video, voice).
- **Search:** The app uses `duckduckgo_search`. If you see warnings about version changes, ensure you have the latest version.
>>>>>>> origin/docs-update-v1-11532887947141402034
=======
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
>>>>>>> origin/docs-update-5816964673776763608

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

```powershell
streamlit run app.py
```

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

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
- Unit tests are located in `tests/` covering:
  - Multimodal helpers (`tests/test_multimodal_smoke.py`)
  - Chat utility logic (`tests/test_chat_utils.py`)
  - Application state initialization (`tests/test_app_state.py`)
- A GitHub Actions workflow `.github/workflows/multimodal-smoke.yml` runs the tests on push and PR.

Run tests locally:

```powershell
# Run all tests
pytest

# Run specific test file
pytest tests/test_app_state.py
```

## Notes
- Optional dependencies: `transformers`, `torch`, `torchvision`, `moviepy`, `speech_recognition`. These are only required for BLIP, video frame extraction, and audio transcription respectively.
- Search library may warn about `duckduckgo_search` -> `ddgs` rename; consider installing `ddgs` if you see warnings.

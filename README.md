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

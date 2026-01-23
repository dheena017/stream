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
```powershell
streamlit run app.py
```

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

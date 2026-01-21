# Multi-Provider AI Chat

A comprehensive Streamlit chat app supporting multiple AI providers:
- **Google Gemini** (2.0 Flash, 1.5 Flash, 1.5 Pro, 1.0 Pro Vision)
- **OpenAI** (GPT-4o, GPT-4 Turbo, o1-Preview, o1-Mini)
- **Anthropic Claude** (3.5 Sonnet, 3.5 Haiku, 3 Opus)
- **Meta Llama** (3.3 70B, 3.1 405B/70B via Together AI)
- **xAI Grok** (Grok Beta)
- **DeepSeek** (Chat & Coder)

## Features

- 🔐 **Authentication**: Username/password login + Google OAuth support
- 🤖 **25+ AI models** from 6 major providers
- 🧠 **AI Brain Mode**: Combines multiple models + internet search
- 🎨 **Customizable settings**: temperature, tokens, top-p
- 📎 **Multimodal**: images, PDFs, audio, video
- 🎤 **Voice mode**: speech-to-text and text-to-speech
- 🌐 **Internet search**: DuckDuckGo integration for real-time information
- 💬 **Streaming responses**
- 📥 **Chat export**

## Setup

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Authentication Setup**:

### Traditional Login (Default)
Set custom passwords via environment variables:
```bash
export ADMIN_PASSWORD=your_admin_password
export USER_PASSWORD=your_user_password
```

Default credentials:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`

### Google OAuth Login (Optional)
To enable Google sign-in:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure OAuth consent screen
6. Create OAuth 2.0 Client ID (Web application)
7. Add authorized redirect URIs (e.g., `http://localhost:8501`)
8. Set environment variables:

```bash
export GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
export GOOGLE_REDIRECT_URI=http://localhost:8501
```

3. **Set API keys** (environment variables or Streamlit secrets):

```bash
export GEMINI_API_KEY=your_google_key
export OPENAI_API_KEY=your_openai_key
export ANTHROPIC_API_KEY=your_anthropic_key
export TOGETHER_API_KEY=your_together_key
export XAI_API_KEY=your_xai_key
export DEEPSEEK_API_KEY=your_deepseek_key
```

Or create `.streamlit/secrets.toml`:

```toml
# Authentication
ADMIN_PASSWORD = "your_admin_password"
USER_PASSWORD = "your_user_password"
GOOGLE_CLIENT_ID = "your_client_id.apps.googleusercontent.com"
GOOGLE_REDIRECT_URI = "http://localhost:8501"

# AI Provider API Keys
GEMINI_API_KEY = "your_google_key"
OPENAI_API_KEY = "your_openai_key"
ANTHROPIC_API_KEY = "your_anthropic_key"
TOGETHER_API_KEY = "your_together_key"
XAI_API_KEY = "your_xai_key"
DEEPSEEK_API_KEY = "your_deepseek_key"
```

4. **Get API Keys**:
   - Google: https://aistudio.google.com/
   - OpenAI: https://platform.openai.com/
   - Anthropic: https://console.anthropic.com/
   - Together AI: https://api.together.xyz/
   - xAI: https://x.ai/api
   - DeepSeek: https://platform.deepseek.com/

## Run

```bash
streamlit run app.py
```

## Notes

- You only need API keys for the providers you want to use
- The app will prompt you if a required API key is missing
- Multimodal features (images, PDFs, etc.) work best with Gemini models
- Voice mode requires `SpeechRecognition` and `gTTS` packages
- Google OAuth is optional - traditional login works without it


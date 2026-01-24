# Features Guide

## Overview

Stream is a powerful multimodal AI chat interface that aggregates multiple LLM providers into a single, cohesive experience. It offers advanced features like internet search augmentation, voice interaction, and "Brain Mode" for enhanced reasoning.

## Core Features

### 💬 Multi-Provider Chat
Access models from top providers in one place:
- **Google**: Gemini Pro / Flash
- **OpenAI**: GPT-4o / Mini
- **Anthropic**: Claude 3.5 Sonnet / Haiku
- **Together AI**: Llama 3 / Mixtral
- **xAI**: Grok Beta
- **DeepSeek**: DeepSeek V3

Select your preferred model from the **🤖 Model Selection** panel in the sidebar.

### 🧠 Brain Mode
Brain Mode acts as a meta-reasoning layer that enhances standard chat interactions.

- **Auto-Select Models**: The "Brain" can dynamically choose the best model for your query.
- **Internet Search**: Augments responses with real-time web data using DuckDuckGo.
- **Consultation**: Can consult multiple models (Google, OpenAI, etc.) simultaneously to synthesize a comprehensive answer.

To enable, toggle **Enable AI Brain** in the sidebar.

### 📎 Multimodal Capabilities

#### Images
- Upload images for analysis.
- **Advanced Captioning**: Uses BLIP (local) or a hosted API to generate detailed captions for models that don't natively support images.

#### Voice Integration
- **Voice Mode**: Speak to the AI using your microphone.
- **Auto-Speak**: Have the AI read responses back to you.
- Supports audio file uploads for transcription and analysis.

#### Video
- Upload video files for frame extraction and analysis.

### ⚙️ Control Panel (Sidebar)

The sidebar is your command center:

1.  **Navigation**: Switch between Chat, Dashboard, and Profile.
2.  **History**: Access and manage past conversations.
3.  **Model Selection**: Filter and choose specific models.
4.  **API Keys**: Securely manage your provider keys.
5.  **Parameters**: Fine-tune generation (Temperature, Top P, Max Tokens).
6.  **Cost Tracking**: Monitor session costs in real-time.

## Dashboard & Analytics

Click **📊 Dash** in the sidebar to access the Dashboard.
- View usage statistics.
- Analyze cost per provider.
- Review interaction history.

## Privacy & Security

- **Local Storage**: Chat history is stored locally in `chat_history.db`.
- **Encryption**: Sensitive data is handled with care.
- **Anonymity**: Feedback is submitted anonymously.

## Experimental Features

- **Learning Brain**: The system tracks topics and learns from conversations to improve context over time.
- **Ethics Engine**: Built-in bias detection and warning system.

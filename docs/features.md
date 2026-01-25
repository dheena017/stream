<<<<<<< HEAD
# Features Overview

Stream Multimodal AI Chat is packed with features to enhance your AI interaction.

## 🧠 Brain Mode

**Brain Mode** is an ensemble processing feature that queries multiple models simultaneously to provide a synthesized, high-quality response.

-   **Ensemble Querying:** Consults Google, OpenAI, Anthropic, and Together AI models in parallel (if keys are provided).
-   **Synthesis:** Uses a primary model to aggregate the best parts of all responses.
-   **Internet Awareness:** Can independently search the internet to ground its synthesis in real-time data.
-   **Transparency:** Expand the "Model Comparison" section to see the raw output from each provider.

## 🌐 Internet Search

Augment your chat with real-time web data.

-   **Modes:**
    -   **Web:** General Google search.
    -   **News:** Specific news search.
-   **Filters:**
    -   **Result Count:** Adjust between 1-10 results.
    -   **Time Range:** Past Day, Week, Month, or Anytime.
    -   **Domain Filter:** Restrict results to specific sites (e.g., `reddit.com`, `docs.python.org`).
-   **Visuals:** Search results are displayed in an expandable "Search Results" section with source links.

## 📎 Multimodal Capabilities

Upload various file types for analysis.

| Type | Extensions | Description |
| :--- | :--- | :--- |
| **Images** | `.jpg`, `.png`, `.webp` | analyzed by vision models (Gemini, GPT-4o, Claude). Can also use local **BLIP** for advanced captioning. |
| **Documents** | `.pdf`, `.txt`, `.md` | Content is extracted and added to the context. |
| **Audio** | `.mp3`, `.wav` | Transcribed automatically and the text is added to the prompt. |
| **Video** | `.mp4`, `.mov` | Key frames are extracted as thumbnails and analyzed as a series of images. |

## ⚙️ Control Panel (Sidebar)

-   **Model Selection:** Filter by provider (Google, OpenAI, etc.) and select specific models (e.g., Gemini 1.5 Pro, Claude 3.5 Sonnet).
-   **Parameters:** Fine-tune `Temperature`, `Top P`, and `Max Tokens`.
-   **System Prompt:** Set a custom persona or instruction for the AI.
-   **Cost Tracking:** View estimated session costs based on input/output tokens.

## 💾 Chat History & Export

-   **History:** Previous conversations are saved to a local database. Access them from the "🕒" section in the sidebar.
-   **Export:** Download the current conversation as a `.txt` file using the **Save** button.
=======
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
>>>>>>> origin/docs-update-5816964673776763608

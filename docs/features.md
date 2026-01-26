# Application Features

Explore the capabilities of the Streamlit AI Chat App.

## 1. Multi-Provider AI Chat

The core of the application is a flexible chat interface that supports multiple Large Language Models (LLMs).

- **Google Gemini**: Uses the Google Generative AI SDK for powerful reasoning and multimodal tasks.
- **OpenAI (GPT-4)**: Integration with OpenAI's latest models for high-quality text generation.
- **Anthropic (Claude 3)**: Support for Claude models, known for safety and large context windows.

**Key Chat Features:**
- **Conversation History**: The app remembers previous turns in the conversation.
- **Summarization**: To save context window space, older messages are automatically summarized by a system prompt.
- **Resilience**: API calls are wrapped in retry logic with exponential backoff to handle transient errors gracefully.

## 2. Real-Time Internet Search

Augment the AI's knowledge with live data from the web.

- **How it works**: When enabled, your prompt is analyzed, and relevant web search results are retrieved (using DuckDuckGo or similar).
- **Context Injection**: These results are appended to the system prompt, allowing the AI to answer questions about current events (e.g., "What is the weather today?", "Latest stock prices").
- **Transparency**: Responses based on search results are marked with `[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]`.

## 3. Multimodal Capabilities

Communicate beyond just text.

### Image Analysis
- **Upload**: You can upload images (PNG, JPG, etc.) directly in the chat.
- **Processing**:
    - **Cloud**: If using a multimodal model (like Gemini Vision or GPT-4o), the image is sent to the provider.
    - **Local**: If offline or using a text-only model, the app can use a local BLIP model to generate captions for the image, which are then fed to the LLM.
- **Usage**: Ask questions like "What is in this picture?" or "Describe this diagram."

### Voice Integration
- **Speech-to-Text**: Click the microphone icon to dictate your prompt. The app uses `SpeechRecognition` to transcribe your voice.
- **Text-to-Speech**: The AI's response can be read aloud using `gTTS` (Google Text-to-Speech) or other configured providers.

## 4. Ethics & Safety Guardrails

The `EthicsGuardian` system runs in the background to ensure safe interactions.

- **Bias Detection**: Analyzes prompts and responses for potential bias or harmful content.
- **Mitigation**:
    - Can inject neutrality instructions into the system prompt.
    - Appends disclaimers to sensitive topics if necessary.
- **Privacy**: Chat history and user preferences are handled with privacy in mind (see `PRIVACY.md` for details).

## 5. Analytics Dashboard

A dedicated dashboard provides insights into usage.

- **Engagement**: Track user levels, XP, and streaks.
- **System Health**: Monitor API response times and error rates.
- **Feedback**: Review user feedback submitted through the UI.

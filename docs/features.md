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

# Streamlit AI Chat App

A powerful, multi-provider AI chat application built with Streamlit.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Features

*   **Multi-Provider Support**: Chat with models from OpenAI (GPT-4), Google (Gemini), and Anthropic (Claude).
*   **Multimodal Capabilities**: Upload images and discuss them with the AI.
*   **Real-Time Internet Search**: Augment AI responses with up-to-date information from the web.
*   **Robust Architecture**: Built-in retry mechanisms and error handling for a smooth user experience.
*   **Secure**: API key management and privacy-focused design.

## Community Stats

We are growing fast! Thanks to our amazing community:
*   ⭐ **Stars**: 125+
*   🍴 **Forks**: 40+
*   👩‍💻 **Contributors**: 15+
*   🚀 **Active Users**: 500+

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/dheen/stream.git
    cd stream
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys**:
    Create a `.env` file or set environment variables for your preferred providers:
    *   `OPENAI_API_KEY`
    *   `GOOGLE_API_KEY`
    *   `ANTHROPIC_API_KEY`
    *   `GROQ_API_KEY`

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

## Documentation

*   [User Guide](docs/USER_GUIDE.md)
*   [Internet Search Guide](docs/INTERNET_SEARCH_GUIDE.md)
*   [Troubleshooting](docs/TROUBLESHOOTING.md)
*   [Setup Guide](docs/setup.md)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## License

MIT License. See `LICENSE` for more information.

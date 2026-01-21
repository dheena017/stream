
# Pricing per 1M tokens (input, output) - Updated Jan 2026 estimates
MODEL_PRICING = {
    # Google Gemini
    "gemini-3-flash-preview": (0.075, 0.30),
    "gemini-2.0-flash-exp": (0.075, 0.30),
    "gemini-2.0-flash-latest": (0.075, 0.30),
    "gemini-1.5-flash": (0.075, 0.30),
    "gemini-1.5-pro": (1.25, 5.00),
    "gemini-1.0-pro-vision-latest": (0.50, 1.50),
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4-turbo": (10.00, 30.00),
    "o1-preview": (15.00, 60.00),
    "o1-mini": (3.00, 12.00),
    # Anthropic Claude
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.25, 1.25),
    "claude-3-opus-20240229": (15.00, 75.00),
    # Together AI (Llama)
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": (0.88, 0.88),
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": (3.50, 3.50),
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": (0.88, 0.88),
    # xAI Grok
    "grok-beta": (5.00, 15.00),
    # DeepSeek
    "deepseek-chat": (0.14, 0.28),
    "deepseek-coder": (0.14, 0.28),
}

MODEL_OPTIONS = [
    # Google Gemini
    ("Gemini 3 Flash Preview", "gemini-3-flash-preview", "google"),
    ("Gemini 2.0 Flash Exp", "gemini-2.0-flash-exp", "google"),
    ("Gemini 2.0 Flash Latest", "gemini-2.0-flash-latest", "google"),
    ("Gemini 1.5 Flash", "gemini-1.5-flash", "google"),
    ("Gemini 1.5 Pro", "gemini-1.5-pro", "google"),
    ("Gemini 1.0 Pro Vision", "gemini-1.0-pro-vision-latest", "google"),
    # OpenAI GPT
    ("GPT-4o", "gpt-4o", "openai"),
    ("GPT-4o Mini", "gpt-4o-mini", "openai"),
    ("GPT-4 Turbo", "gpt-4-turbo", "openai"),
    ("o1-Preview", "o1-preview", "openai"),
    ("o1-Mini", "o1-mini", "openai"),
    # Anthropic Claude
    ("Claude 3.5 Sonnet", "claude-3-5-sonnet-20241022", "anthropic"),
    ("Claude 3.5 Haiku", "claude-3-5-haiku-20241022", "anthropic"),
    ("Claude 3 Opus", "claude-3-opus-20240229", "anthropic"),
    # Meta Llama (via Together AI)
    ("Llama 3.3 70B", "meta-llama/Llama-3.3-70B-Instruct-Turbo", "together"),
    ("Llama 3.1 405B", "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", "together"),
    ("Llama 3.1 70B", "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "together"),
    # xAI Grok (via Groq or OpenAI-compatible)
    ("Grok Beta", "grok-beta", "xai"),
    # DeepSeek
    ("DeepSeek Chat", "deepseek-chat", "deepseek"),
    ("DeepSeek Coder", "deepseek-coder", "deepseek"),
]

MODEL_CAPABILITIES = {
    "gemini-3-flash-preview": ["⚡ Fast", "🖼️ Vision", "🆕 Preview"],
    "gemini-2.0-flash-exp": ["⚡ Fast", "🖼️ Vision", "🧪 Experimental"],
    "gemini-2.0-flash-latest": ["⚡ Fast", "🖼️ Vision"],
    "gemini-1.5-flash": ["⚡ Fast", "📄 Long Context"],
    "gemini-1.5-pro": ["🧠 Smart", "📄 Long Context"],
    "gemini-1.0-pro-vision-latest": ["🖼️ Vision"],
    "gpt-4o": ["🧠 Smart", "🖼️ Vision", "⚡ Fast"],
    "gpt-4o-mini": ["⚡ Fast", "💰 Cheap"],
    "gpt-4-turbo": ["🧠 Smart", "🖼️ Vision"],
    "o1-preview": ["🧠 Reasoning", "🆕 Preview"],
    "o1-mini": ["🧠 Reasoning", "⚡ Fast"],
    "claude-3-5-sonnet-20241022": ["🧠 Smart", "📝 Writing"],
    "claude-3-5-haiku-20241022": ["⚡ Fast", "💰 Cheap"],
    "claude-3-opus-20240229": ["🧠 Flagship", "📝 Writing"],
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": ["🦙 Open", "⚡ Fast"],
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": ["🦙 Open", "🧠 Flagship"],
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": ["🦙 Open"],
    "grok-beta": ["🆕 Beta", "💬 Chat"],
    "deepseek-chat": ["💬 Chat", "💰 Cheap"],
    "deepseek-coder": ["💻 Code", "💰 Cheap"],
}

PROVIDER_ICONS = {
    "google": "🔵", "openai": "🟢", "anthropic": "🟣",
    "together": "🔴", "xai": "⚫", "deepseek": "🟠"
}

PROVIDER_LABELS = {
    "google": "Google Gemini", "openai": "OpenAI GPT", "anthropic": "Anthropic Claude",
    "together": "Meta Llama", "xai": "xAI Grok", "deepseek": "DeepSeek"
}

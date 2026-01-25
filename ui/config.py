
# Pricing per 1M tokens (input, output) - Updated Jan 2026 estimates

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
    # Groq
    "llama-3.3-70b-versatile": (0.59, 0.79),
    "llama-3.1-8b-instant": (0.05, 0.08),
    "mixtral-8x7b-32768": (0.24, 0.24),
}

# Detailed Model Metadata
MODEL_DETAILS = {
    # Google
    "gemini-3-flash-preview": {
        "label": "Gemini 3 Flash Preview",
        "provider": "google",
        "context": "1M",
        "description": "Latest preview with improved speed.",
        "capabilities": ["⚡ Fast", "🖼️ Vision", "🆕 Preview"]
    },
    "gemini-2.0-flash-exp": {
        "label": "Gemini 2.0 Flash Exp",
        "provider": "google",
        "context": "1M",
        "description": "Next-gen multimodal logic & speed.",
        "capabilities": ["⚡ Fast", "🖼️ Vision", "🧪 Experimental"]
    },
    "gemini-2.0-flash-latest": {
        "label": "Gemini 2.0 Flash Latest",
        "provider": "google",
        "context": "1M",
        "description": "Latest stable flash model.",
        "capabilities": ["⚡ Fast", "🖼️ Vision"]
    },
    "gemini-1.5-flash": {
        "label": "Gemini 1.5 Flash",
        "provider": "google",
        "context": "1M",
        "description": "Cost-effective, high-volume star.",
        "capabilities": ["⚡ Fast", "📄 Long Context"]
    },
    "gemini-1.5-pro": {
        "label": "Gemini 1.5 Pro",
        "provider": "google",
        "context": "2M",
        "description": "Top-tier reasoning with massive context.",
        "capabilities": ["🧠 Smart", "📄 Long Context"]
    },
    "gemini-1.0-pro-vision-latest": {
        "label": "Gemini 1.0 Pro Vision",
        "provider": "google",
        "context": "16k",
        "description": "Legacy vision model.",
        "capabilities": ["🖼️ Vision"]
    },
    # OpenAI
    "gpt-4o": {
        "label": "GPT-4o",
        "provider": "openai",
        "context": "128k",
        "description": "Omni-model, flagship intelligence.",
        "capabilities": ["🧠 Smart", "🖼️ Vision", "⚡ Fast"]
    },
    "gpt-4-turbo": {
        "label": "GPT-4 Turbo",
        "provider": "openai",
        "context": "128k",
        "description": "Previous flagship, strong reasoning.",
        "capabilities": ["🧠 Smart", "🖼️ Vision"]
    },
    "gpt-4o-mini": {
        "label": "GPT-4o Mini",
        "provider": "openai",
        "context": "128k",
        "description": "Affordable small model, great for fast tasks.",
        "capabilities": ["⚡ Fast", "💰 Cheap"]
    },
    "o1-preview": {
        "label": "o1 Preview",
        "provider": "openai",
        "context": "128k",
        "description": "Reasoning model for complex math/science.",
        "capabilities": ["🧠 Reasoning", "🆕 Preview"]
    },
     "o1-mini": {
        "label": "o1 Mini",
        "provider": "openai",
        "context": "128k",
        "description": "Faster reasoning model.",
        "capabilities": ["🧠 Reasoning", "⚡ Fast"]
    },
    # Anthropic
    "claude-3-5-sonnet-20241022": {
        "label": "Claude 3.5 Sonnet",
        "provider": "anthropic",
        "context": "200k",
        "description": "Excellent nuance and coding capability.",
        "capabilities": ["🧠 Smart", "📝 Writing"]
    },
    "claude-3-5-haiku-20241022": {
        "label": "Claude 3.5 Haiku",
        "provider": "anthropic",
        "context": "200k",
        "description": "Lightning fast, intelligent small model.",
        "capabilities": ["⚡ Fast", "💰 Cheap"]
    },
    # Together
    "meta-llama/Llama-3.3-70B-Instruct-Turbo": {
        "label": "Llama 3.3 70B",
        "provider": "together",
        "context": "128k",
        "description": "High-performance open model.",
        "capabilities": ["🦙 Open", "⚡ Fast"]
    },
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": {
        "label": "Llama 3.1 405B",
        "provider": "together",
        "context": "128k",
        "description": "Massive scale open intelligence.",
        "capabilities": ["🦙 Open", "🧠 Flagship"]
    },
    # xAI
    "grok-beta": {
        "label": "Grok Beta",
        "provider": "xai",
        "context": "128k",
        "description": "Wit and real-time knowledge focus.",
        "capabilities": ["🆕 Beta", "💬 Chat"]
    },
    # DeepSeek
     "deepseek-chat": {
        "label": "DeepSeek Chat",
        "provider": "deepseek",
        "context": "64k",
        "description": "Strong general performance, very low cost.",
        "capabilities": ["💬 Chat", "💰 Cheap"]
    },
     "deepseek-coder": {
        "label": "DeepSeek Coder",
        "provider": "deepseek",
        "context": "64k",
        "description": "Specialized for programming tasks.",
        "capabilities": ["💻 Code", "💰 Cheap"]
    },
    # Groq
    "llama-3.3-70b-versatile": {
        "label": "Groq Llama 3.3 70B",
        "provider": "groq",
        "context": "128k",
        "description": "High speed open model.",
        "capabilities": ["⚡ Fast", "🦙 Open"]
    },
    "llama-3.1-8b-instant": {
        "label": "Groq Llama 3.1 8B",
        "provider": "groq",
        "context": "128k",
        "description": "Extremely fast small model.",
        "capabilities": ["⚡ Fast", "💰 Cheap"]
    },
    "mixtral-8x7b-32768": {
        "label": "Groq Mixtral 8x7b",
        "provider": "groq",
        "context": "32k",
        "description": "Balanced performance and speed.",
        "capabilities": ["⚡ Fast", "🧠 Smart"]
    },
}

# Legacy Compatibility Lists (Generated from MODEL_DETAILS)
MODEL_OPTIONS = [
    (v['label'], k, v['provider'])
    for k, v in MODEL_DETAILS.items()
]

MODEL_CAPABILITIES = {
    k: v['capabilities']
    for k, v in MODEL_DETAILS.items()
}

PROVIDER_ICONS = {
    "google": "🔵", "openai": "🟢", "anthropic": "🟣",
    "together": "🔴", "xai": "⚫", "deepseek": "🟠",
    "groq": "⚡",
    "brain-mode": "🧠"
}

PROVIDER_LABELS = {
    "google": "Google Gemini", "openai": "OpenAI GPT", "anthropic": "Anthropic Claude",
    "together": "Meta Llama", "xai": "xAI Grok", "deepseek": "DeepSeek",
    "groq": "Groq",
    "brain-mode": "Brain Mode"
}

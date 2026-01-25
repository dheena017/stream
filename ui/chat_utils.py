<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> origin/code-quality-refactor-17423438479402428749
import functools
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import streamlit as st
<<<<<<< HEAD
from PIL import Image
=======
import streamlit as st
import logging
import time
from typing import List, Dict, Optional, Any, Callable, Tuple
from ui.analytics import log_api_call, log_error
>>>>>>> origin/analytics-monitoring-17353357073288903889

logger = logging.getLogger(__name__)

=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354

import streamlit as st
import logging
from typing import List, Dict, Optional, Any, Callable, Tuple
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from ui.ethics import EthicsGuardian
=======

import streamlit as st
import logging
import json
from typing import List, Dict, Optional, Any, Callable, Tuple
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
=======
>>>>>>> origin/monitoring-setup-15681340840960488850

import streamlit as st
import logging
from typing import List, Dict, Optional, Any, Callable, Tuple
import time
<<<<<<< HEAD
import functools
from io import BytesIO
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
from monitoring import get_monitor
>>>>>>> origin/monitoring-setup-15681340840960488850
=======

import streamlit as st
import logging
import asyncio
import concurrent.futures
from typing import List, Dict, Optional, Any, Callable, Tuple
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
import streamlit as st
import logging
import asyncio
import time
import functools
from typing import List, Dict, Optional, Any, Callable, Tuple
from concurrent.futures import ThreadPoolExecutor
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

import streamlit as st
import logging
import monitoring
from typing import List, Dict, Optional, Any, Callable, Tuple
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354

logger = logging.getLogger(__name__)

# BLIP cache holds (processor, model, device)
BLIP_CACHE: Optional[Tuple[Any, Any, Any]] = None
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======

import streamlit as st
import time
from loguru import logger
from typing import List, Dict, Optional, Any, Callable, Tuple

# BLIP cache holds (processor, model, device)
BLIP_CACHE: Optional[Tuple[Any, Any, Any]] = None
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======


# --- Async Helpers ---
def safe_run_async(coro):
    """
    Safely run an async coroutine, handling cases where an event loop
    might already be running (common in Streamlit/Tornado environments).
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Event loop is running, offload to a thread to use asyncio.run
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        # No event loop running, safe to use asyncio.run
        return asyncio.run(coro)
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354


# --- Cached clients / resources ---
@st.cache_resource
def get_internet_search_engine():
    from ui.internet_search import InternetSearchEngine
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    return InternetSearchEngine()


@st.cache_resource
def get_openai_client(api_key: str, base_url: Optional[str] = None):
    from openai import OpenAI
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

    return (
        OpenAI(api_key=api_key, base_url=base_url)
        if base_url
        else OpenAI(api_key=api_key)
    )
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> 673954a (Resilience: [error handling])
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> performance-optimization-13534932852089819512
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> api-groq-integration-6554511320622598819
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> api-integrations-groq-3434217061461873316
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
>>>>>>> origin/api-integrations-groq-12473300930587894354


@st.cache_resource
def get_anthropic_client(api_key: str):
    from anthropic import Anthropic
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    return Anthropic(api_key=api_key)


@st.cache_resource
def get_google_client(api_key: str):
    # Import dynamically to avoid hard dependency if not used
    import google.generativeai as genai
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

    genai.configure(api_key=api_key)
    return genai


# --- Conversation helpers ---
def build_conversation_history(
    messages: List[Dict],
    exclude_last: bool = True,
    max_messages: int = 20,
    max_chars: int = 50000,
) -> List[Dict]:
    history = messages[:-1] if exclude_last and len(messages) > 0 else messages
    if not history:
        return []
    formatted = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
        if "role" in msg and "content" in msg
    ]
=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
    genai.configure(api_key=api_key)
    return genai

=======
    return Anthropic(api_key=api_key)


>>>>>>> api-integrations-groq-3434217061461873316
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/monitoring-setup-15681340840960488850
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
    genai.configure(api_key=api_key)
    return genai

>>>>>>> origin/api-integrations-groq-12473300930587894354
# --- Conversation helpers ---
def build_conversation_history(messages: List[Dict], exclude_last: bool = True, max_messages: int = 20, max_chars: int = 50000) -> List[Dict]:
    history = messages[:-1] if exclude_last and len(messages) > 0 else messages
    if not history:
        return []
    formatted = [{"role": msg["role"], "content": msg["content"]} for msg in history if "role" in msg and "content" in msg]
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    total_chars = sum(len(m.get("content", "")) for m in formatted)
    if len(formatted) > max_messages or total_chars > max_chars:
        older = formatted[:-max_messages] if len(formatted) > max_messages else []
        recent = formatted[-max_messages:]
        if older:
            older_summary_parts = []
            for msg in older[-10:]:
                content = msg.get("content", "")
                preview = content[:200] + "..." if len(content) > 200 else content
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                older_summary_parts.append(
                    f"{msg.get('role', 'unknown').upper()}: {preview}"
                )
            summary_text = "[Earlier conversation summary]\n" + "\n".join(
                older_summary_parts
            )
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> 673954a (Resilience: [error handling])
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> performance-optimization-13534932852089819512
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> api-groq-integration-6554511320622598819
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> api-integrations-groq-3434217061461873316
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
>>>>>>> origin/api-integrations-groq-12473300930587894354
            return [{"role": "system", "content": summary_text}] + recent
        else:
            return recent
    return formatted


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def create_openai_messages(
    conversation_history: List[Dict],
    current_prompt: str,
    system_instruction: Optional[str] = None,
) -> List[Dict]:
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> 673954a (Resilience: [error handling])
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> performance-optimization-13534932852089819512
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> api-groq-integration-6554511320622598819
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> api-integrations-groq-3434217061461873316
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/api-integrations-groq-12473300930587894354
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": current_prompt})
    return messages


# --- Resilience Helpers ---
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
import time
import functools

>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
import time
import functools

>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
import time
import functools

>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
import time
import functools

>>>>>>> 673954a (Resilience: [error handling])
=======

>>>>>>> performance-optimization-13534932852089819512
=======
import time
import functools

>>>>>>> api-groq-integration-6554511320622598819
=======
import time
import functools

>>>>>>> api-integrations-groq-3434217061461873316
=======

>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
import functools

>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
import time
import functools

>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
import time
import functools

>>>>>>> origin/monitoring-setup-15681340840960488850
=======
import time
import functools

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
import time
import functools

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
import time
import functools

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
import time
import functools

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
import time
import functools

>>>>>>> origin/api-integrations-groq-12473300930587894354
def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                        raise e
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    sleep = backoff_in_seconds * 2**x
                    time.sleep(sleep)
                    x += 1

        return wrapper

    return decorator


=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
                    sleep = (backoff_in_seconds * 2 ** x)
=======
                        logger.warning(f"Max retries ({retries}) reached for {func.__name__}. Error: {e}")
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    logger.warning(f"Retry {x+1}/{retries} for {func.__name__} after {sleep}s. Error: {e}")
>>>>>>> 673954a (Resilience: [error handling])
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> performance-optimization-13534932852089819512
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> api-groq-integration-6554511320622598819
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> api-integrations-groq-3434217061461873316
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
>>>>>>> origin/api-integrations-groq-12473300930587894354
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
# --- Provider Handlers ---
def handle_google_provider(
    api_key: str, 
    model_name: str, 
    prompt: str, 
=======
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

def run_async_safely(coro):
    """
    Safely run an async coroutine in Streamlit.
    Handles cases where an event loop is already running.
    """
    try:
        # Check if there is a running loop
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # If loop is running, offload to thread to get a fresh loop via asyncio.run
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    else:
        return asyncio.run(coro)


>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
# --- Provider Handlers ---
def handle_google_provider(
    api_key: str,
    model_name: str,
    prompt: str,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.95,
    images: List = None,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    enable_streaming: bool = False,
) -> str:
    """
    Handles interaction with Google's Gemini models.
    Supports text and image inputs (multimodal).
    """
    try:
        if not api_key:
            return "Please provide a Google API Key."
        import google.generativeai as genai

        # Configure the global instance
        genai.configure(api_key=api_key)


        # Mapping config specifically for GenerativeModel
        generation_config = genai.types.GenerationConfig(
            temperature=temperature, max_output_tokens=max_tokens, top_p=top_p
        )


=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide a Google API Key."
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Error: Missing Google API Key."
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
        import google.generativeai as genai
        # Configure the global instance
=======

        import google.generativeai as genai
>>>>>>> api-integrations-groq-3434217061461873316
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
        import google.generativeai as genai
        # Configure the global instance
>>>>>>> origin/api-integrations-groq-12473300930587894354
        genai.configure(api_key=api_key)

        # Mapping config specifically for GenerativeModel
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            top_p=top_p
        )
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/monitoring-setup-15681340840960488850
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
        # Initialize model
        # system_instruction is supported in newer versions as init argument or via specific methods
        # For broader compatibility, passing via constructor if supported, else prepending to prompt might be needed
        # But latest SDK supports 'system_instruction' in GenerativeModel constructor
        try:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            model = genai.GenerativeModel(
                model_name=model_name, system_instruction=system_instruction
            )
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> 673954a (Resilience: [error handling])
=======
        # Initialize model
        try:
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> performance-optimization-13534932852089819512
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> api-groq-integration-6554511320622598819
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> api-integrations-groq-3434217061461873316
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
>>>>>>> origin/api-integrations-groq-12473300930587894354
        except TypeError:
            # Fallback for older SDK versions that don't support system_instruction in init
            model = genai.GenerativeModel(model_name=model_name)
            if system_instruction:
                prompt = f"{system_instruction}\n\n{prompt}"
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            
=======

>>>>>>> origin/monitoring-setup-15681340840960488850
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
        contents = []
        if images:
            from io import BytesIO
            import base64
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
        contents = []
        if images:
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
        contents = []
        if images:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
            for img in images:
                # Gemai SDK can take PIL images directly in 'contents'
                contents.append(img)
        
        contents.append(prompt)
        
=======
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

        # Initialize model
        try:
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
        except TypeError:
            # Fallback for older SDK versions
            model = genai.GenerativeModel(model_name=model_name)
            if system_instruction:
                prompt = f"{system_instruction}\n\n{prompt}"

        contents = []
        if images:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
            for img in images:
                # Gemai SDK can take PIL images directly in 'contents'
                contents.append(img)

        contents.append(prompt)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
        @retry_with_backoff(retries=2)
        def _generate():
            # For gemini, we can pass stream=True/False to generate_content
=======
        @retry_with_backoff(retries=2)
        def _generate():
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        @retry_with_backoff(retries=2)
        def _generate():
            # For gemini, we can pass stream=True/False to generate_content
>>>>>>> origin/analytics-monitoring-16051435839535532537
            return model.generate_content(
                contents,
                generation_config=generation_config,
                stream=enable_streaming
            )

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        response = _generate()
        
        if enable_streaming:
            collected_text = []

=======
        start_time = time.time()
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
        # Define safety settings to block harmful content (ethics mitigation)
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        @retry_with_backoff(retries=2)
        def _generate():
            # For gemini, we can pass stream=True/False to generate_content
            return model.generate_content(
                contents,
                generation_config=generation_config,
<<<<<<< HEAD
<<<<<<< HEAD
                safety_settings=safety_settings,
                stream=enable_streaming
            )

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                stream=enable_streaming
            )

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
                stream=enable_streaming
            )

>>>>>>> origin/api-integrations-groq-12473300930587894354
        response = _generate()

        if enable_streaming:
            collected_text = []
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
            def _stream_gen():
                for chunk in response:
                    if chunk.text:
                        collected_text.append(chunk.text)
                        yield chunk.text
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            
=======

>>>>>>> origin/monitoring-setup-15681340840960488850
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
            try:
                st.write_stream(_stream_gen())
            except Exception as e:
                logger.warning(f"Google streaming visualization failed: {e}")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            
            return "".join(collected_text)
        else:
            return response.text
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> performance-optimization-13534932852089819512
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> api-groq-integration-6554511320622598819
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> api-integrations-groq-3434217061461873316
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            return "".join(collected_text)
        else:
             return response.text
>>>>>>> origin/daily-ai-improvement-16784022982147370640

    except Exception as e:
        logger.error(f"Google provider error: {e}")
        return f"Error connecting to Google Gemini: {str(e)}"

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
            final_text = "".join(collected_text)
            log_api_call("google", model_name, time.time() - start_time, True)
            return final_text
        else:
            log_api_call("google", model_name, time.time() - start_time, True)
            return response.text

    except Exception as e:
        log_error("handle_google_provider", e)
        log_api_call("google", model_name, 0, False, str(e))
        logger.error(f"Google provider error: {e}")
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
=======

>>>>>>> origin/monitoring-setup-15681340840960488850
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
            return "".join(collected_text)
        else:
             return response.text

    except Exception as e:
        logger.error(f"Google provider error: {e}")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        return f"Error: Google Gemini - {str(e)}"

>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/monitoring-setup-15681340840960488850
=======
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
        return f"Error connecting to Google Gemini: {str(e)}"

>>>>>>> origin/api-integrations-groq-12473300930587894354
def handle_anthropic_provider(
    api_key: str,
    model_name: str,
    messages: List[Dict],
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    enable_streaming: bool = False,
) -> str:
    """
    Handles interaction with Anthropic's Claude models.
    """
    try:
        if not api_key:
            return "Please provide an Anthropic API Key."
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)


        kwargs = {
            "model": model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide an Anthropic API Key."
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Error: Missing Anthropic API Key."
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)

        kwargs = {
             "model": model_name,
             "messages": messages,
             "max_tokens": max_tokens,
             "temperature": temperature,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        }
        if system_instruction:
             kwargs["system"] = system_instruction

        @retry_with_backoff(retries=2)
        def _create_message():
            if enable_streaming:
                return client.messages.create(stream=True, **kwargs)
            else:
                return client.messages.create(stream=False, **kwargs)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        response = _create_message()
        
=======
        response = _create_message()

>>>>>>> origin/monitoring-setup-15681340840960488850
=======
        response = _create_message()

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
        response = _create_message()

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        response = _create_message()

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
        response = _create_message()

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        response = _create_message()

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
        response = _create_message()

>>>>>>> origin/api-integrations-groq-12473300930587894354
        if enable_streaming:
            collected_text = []
            def _stream_gen():
                for event in response:
                    if event.type == 'content_block_delta':
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
                        text = event.delta.text
                        collected_text.append(text)
                        yield text
            
=======
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
                        text = event.delta.text
                        collected_text.append(text)
                        yield text

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
            try:
                st.write_stream(_stream_gen())
            except Exception:
                pass
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
            return "".join(collected_text)
        else:
            return response.content[0].text

    except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        logger.error(f"Anthropic provider error: {e}")
        return f"Error connecting to Anthropic Claude: {str(e)}"

=======
            final_text = "".join(collected_text)
            log_api_call("anthropic", model_name, time.time() - start_time, True)
            return final_text
        else:
            log_api_call("anthropic", model_name, time.time() - start_time, True)
            return response.content[0].text

    except Exception as e:
         log_error("handle_anthropic_provider", e)
         log_api_call("anthropic", model_name, 0, False, str(e))
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error: Anthropic Claude - {str(e)}"
>>>>>>> 673954a (Resilience: [error handling])
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> performance-optimization-13534932852089819512
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> api-groq-integration-6554511320622598819
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> api-integrations-groq-3434217061461873316
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"
>>>>>>> origin/api-integrations-groq-12473300930587894354

def generate_standard_response(
    provider: str,
    model_name: str,
    api_keys: Dict[str, str],
    prompt: str,
    chat_history: List[Dict],
    system_instruction: str = "",
    config: Dict[str, Any] = {},
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    images: List = None,
=======
    images: List = None
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
    images: List = None
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
    images: List = None
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
    images: List = None
>>>>>>> 673954a (Resilience: [error handling])
=======
    images: List = None
>>>>>>> performance-optimization-13534932852089819512
=======
    images: List = None
>>>>>>> api-groq-integration-6554511320622598819
=======
    images: List = None
>>>>>>> api-integrations-groq-3434217061461873316
=======
    images: List = None
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    images: List = None
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
    images: List = None
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
    images: List = None
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
    images: List = None
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    images: List = None
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    images: List = None
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
    images: List = None
>>>>>>> origin/api-integrations-groq-12473300930587894354
) -> str:
    """Unified dispatcher for standard mode chat generation"""
    api_key = api_keys.get(provider)
    if not api_key:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

<<<<<<< HEAD
<<<<<<< HEAD
    try:
<<<<<<< HEAD
        temp = config.get("temperature", 0.7)
        max_tok = config.get("max_tokens", 2048)
        top_p = config.get("top_p", 0.95)
        stream = config.get("enable_streaming", False)
=======
=======
    guardian = EthicsGuardian()

    # 1. Check prompt for ethics
    is_safe_prompt, prompt_issue = guardian.check_safety(prompt)
    if not is_safe_prompt:
        system_instruction = guardian.augment_system_instruction(system_instruction, prompt_issue)
        logger.info(f"Ethics Guardian flagged prompt: {prompt_issue}")

    try:
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
    try:
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
        return f"Error: Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> 673954a (Resilience: [error handling])
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> performance-optimization-13534932852089819512
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> api-groq-integration-6554511320622598819
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> api-integrations-groq-3434217061461873316
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
    images: List = None
) -> str:
    """Unified dispatcher for standard mode chat generation"""
    monitor = get_monitor()
    start_time = time.time()

    api_key = api_keys.get(provider)
    if not api_key:
        monitor.log_request(provider, model_name, 0, False, "Missing API Key")
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    images: List = None
) -> str:
    """Unified dispatcher for standard mode chat generation"""
    start_time = time.time()
    session_id = st.session_state.get("session_id", "unknown")
    api_key = api_keys.get(provider)
    if not api_key:
        monitoring.track_request(provider, model_name, False, 0, token_usage=None, session_id=session_id)
        monitoring.track_error(f"Missing API Key for {provider}", context=session_id)
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
        # --- Ethics Integration ---
        from ui.ethics import analyze_prompt_for_bias, get_ethics_guidelines, get_disclaimer

        # 1. Analyze prompt for bias
        bias_flags = analyze_prompt_for_bias(prompt)

        # 2. Inject ethical guidelines into system instruction
        ethics_guidelines = get_ethics_guidelines()
        if system_instruction:
            system_instruction = f"{ethics_guidelines}\n\n{system_instruction}"
        else:
            system_instruction = ethics_guidelines

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
>>>>>>> origin/api-integrations-groq-12473300930587894354
        temp = config.get('temperature', 0.7)
        max_tok = config.get('max_tokens', 2048)
        top_p = config.get('top_p', 0.95)
        stream = config.get('enable_streaming', False)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889

        if provider == "google":
            return handle_google_provider(
                api_key, model_name, prompt, system_instruction, 
                temp, max_tok, top_p, images, enable_streaming=stream
            )
            
=======
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537

        response = None
        if provider == "google":
            response = handle_google_provider(
<<<<<<< HEAD
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

        response = ""
        if provider == "google":
            response = handle_google_provider(
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> origin/api-integrations-groq-12473300930587894354
                api_key, model_name, prompt, system_instruction,
                temp, max_tok, top_p, images, enable_streaming=stream
            )

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
        elif provider in ["openai", "together", "xai", "deepseek"]:
            base_urls = {
                "together": "https://api.together.xyz/v1",
                "xai": "https://api.x.ai/v1",
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                "deepseek": "https://api.deepseek.com",
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> 673954a (Resilience: [error handling])
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> performance-optimization-13534932852089819512
=======
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        elif provider in ["openai", "together", "xai", "deepseek", "groq"]:
            base_urls = {
                "together": "https://api.together.xyz/v1",
                "xai": "https://api.x.ai/v1",
                "deepseek": "https://api.deepseek.com",
                "groq": "https://api.groq.com/openai/v1"
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                "deepseek": "https://api.deepseek.com"
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
            }
            client = get_openai_client(api_key, base_urls.get(provider))
            msgs = create_openai_messages(build_conversation_history(chat_history), prompt, system_instruction)
            return handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)

        elif provider == "anthropic":
            # Anthropic expects just user/assistant messages
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            msgs = [
                {"role": "user", "content": prompt}
            ]  # Simplified for this call; ideally use full history if supported
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> 673954a (Resilience: [error handling])
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> performance-optimization-13534932852089819512
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> api-groq-integration-6554511320622598819
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> api-integrations-groq-3434217061461873316
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
>>>>>>> origin/api-integrations-groq-12473300930587894354
            return handle_anthropic_provider(
                api_key, model_name, msgs, system_instruction,
                temp, max_tok, enable_streaming=stream
            )
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            
        return "Provider not supported."
        
    except Exception as e:
        return f"Generation Error: {str(e)}"


def prepare_brain_configuration(
    api_keys: Dict[str, str], requested_models: List[str] = None
) -> List[Dict[str, Any]]:
    """Helper to build the list of models for Brain Mode based on available keys"""
    models_to_query = []


=======
        return "Provider not supported."
=======
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
                "deepseek": "https://api.deepseek.com"
            }
            client = get_openai_client(api_key, base_urls.get(provider))
            msgs = create_openai_messages(build_conversation_history(chat_history), prompt, system_instruction)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            response_text = handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)
=======
            response = handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
            response = handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
            response = handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)
>>>>>>> origin/ethics-bias-fixes-185826756388721926

        elif provider == "anthropic":
            # Anthropic expects just user/assistant messages
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            response_text = handle_anthropic_provider(
                api_key, model_name, msgs, system_instruction,
                temp, max_tok, enable_streaming=stream
            )
        else:
            return "Provider not supported."

        # 2. Check response for ethics
        is_safe_resp, resp_issue = guardian.check_safety(response_text)
        if not is_safe_resp:
            disclaimer = guardian.get_disclaimer(resp_issue)
            response_text += disclaimer
            logger.info(f"Ethics Guardian flagged response: {resp_issue}")

        return response_text
>>>>>>> 9a44f3f (Ethics: [bias fixes])

=======
        return "Provider not supported."

>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
    except Exception as e:
        return f"Generation Error: {str(e)}"
=======
        return "Error: Provider not supported."

    except Exception as e:
        return f"Error: {str(e)}"
>>>>>>> 673954a (Resilience: [error handling])

=======
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
        return "Provider not supported."

    except Exception as e:
        return f"Generation Error: {str(e)}"

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        return "Provider not supported."

    except Exception as e:
        logger.error(f"Generation Error: {str(e)}")
        return f"Generation Error: {str(e)}"

>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
def prepare_brain_configuration(api_keys: Dict[str, str], requested_models: List[str] = None) -> List[Dict[str, Any]]:
    """Helper to build the list of models for Brain Mode based on available keys"""
    models_to_query = []
    
=======
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
            response = handle_anthropic_provider(
                api_key, model_name, msgs, system_instruction,
                temp, max_tok, enable_streaming=stream
            )
<<<<<<< HEAD
<<<<<<< HEAD

        else:
            monitor.log_request(provider, model_name, time.time() - start_time, False, "Provider not supported")
            return "Provider not supported."

        # Simple error detection in response string
        is_error = response.startswith("Error") or response.startswith("Generation Error") or "Please provide" in response
        monitor.log_request(provider, model_name, time.time() - start_time, not is_error, response if is_error else None)
        return response

    except Exception as e:
        monitor.log_request(provider, model_name, time.time() - start_time, False, str(e))
        return f"Generation Error: {str(e)}"

=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        else:
            response = "Provider not supported."

        # Check if response indicates an error (basic check based on typical string returns in this app)
        success = True
        if isinstance(response, str) and (response.startswith("Error") or "Provider not supported" in response):
            success = False
            monitoring.track_error(response, context=f"Provider: {provider}, Model: {model_name}")

        latency = time.time() - start_time
        monitoring.track_request(provider, model_name, success, latency, session_id=session_id)
=======
        else:
            return "Provider not supported."

        # 3. Append disclaimers if bias was detected
        for flag in bias_flags:
            disclaimer = get_disclaimer(flag)
            if disclaimer:
                response += disclaimer
                # If streaming was used, we might want to display this disclaimer as well
                if stream:
                    st.markdown(disclaimer)
>>>>>>> origin/ethics-bias-fixes-185826756388721926

        return response

    except Exception as e:
<<<<<<< HEAD
        latency = time.time() - start_time
        monitoring.track_error(str(e), context=f"Provider: {provider}, Model: {model_name}, Session: {session_id}")
        monitoring.track_request(provider, model_name, False, latency, session_id=session_id)
        return f"Generation Error: {str(e)}"

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        return f"Generation Error: {str(e)}"

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
def prepare_brain_configuration(api_keys: Dict[str, str], requested_models: List[str] = None) -> List[Dict[str, Any]]:
    """Helper to build the list of models for Brain Mode based on available keys"""
    models_to_query = []

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    # Default strategy: Use available keys (simplified)
    # In a real app, 'requested_models' would come from user config

    if api_keys.get('google'):
        models_to_query.append({"provider": "google", "model": "gemini-1.5-flash", "api_key": api_keys['google']})

    if api_keys.get('openai'):
        models_to_query.append({"provider": "openai", "model": "gpt-4o-mini", "api_key": api_keys['openai']})

    if api_keys.get('anthropic'):
         models_to_query.append({"provider": "anthropic", "model": "claude-3-5-haiku-20241022", "api_key": api_keys['anthropic']})

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    return models_to_query

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
    if api_keys.get('groq'):
         models_to_query.append({"provider": "groq", "model": "llama-3.1-8b-instant", "api_key": api_keys['groq']})

    return models_to_query

>>>>>>> api-groq-integration-6554511320622598819
=======
    if api_keys.get('groq'):
        models_to_query.append({"provider": "groq", "model": "llama-3.3-70b-versatile", "api_key": api_keys['groq']})

    return models_to_query

>>>>>>> api-integrations-groq-3434217061461873316
=======
    return models_to_query

>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    return models_to_query

>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
    return models_to_query

>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
    return models_to_query

>>>>>>> origin/monitoring-setup-15681340840960488850
=======
    return models_to_query

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
    return models_to_query

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    return models_to_query

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
    return models_to_query

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    return models_to_query

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
    if api_keys.get('groq'):
         models_to_query.append({"provider": "groq", "model": "llama-3.3-70b-versatile", "api_key": api_keys['groq']})

    return models_to_query

>>>>>>> origin/api-integrations-groq-12473300930587894354
def handle_openai_compatible_provider(
    client: Any,
    model_name: str,
    messages: List[Dict],
    temperature: float,
    max_tokens: int,
    top_p: float,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    enable_streaming: bool,
=======
    enable_streaming: bool
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
    enable_streaming: bool
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
    enable_streaming: bool
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
    enable_streaming: bool
>>>>>>> 673954a (Resilience: [error handling])
=======
    enable_streaming: bool
>>>>>>> performance-optimization-13534932852089819512
=======
    enable_streaming: bool
>>>>>>> api-groq-integration-6554511320622598819
=======
    enable_streaming: bool
>>>>>>> api-integrations-groq-3434217061461873316
=======
    enable_streaming: bool
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    enable_streaming: bool
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
    enable_streaming: bool
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
    enable_streaming: bool
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
    enable_streaming: bool
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
    enable_streaming: bool
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    enable_streaming: bool
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
    enable_streaming: bool
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    enable_streaming: bool
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
    enable_streaming: bool
>>>>>>> origin/api-integrations-groq-12473300930587894354
) -> str:
    @retry_with_backoff(retries=2)
    def _create_completion(stream_mode):
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            stream=stream_mode,
        )

=======
            stream=stream_mode
        )

    start_time = time.time()
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
            stream=stream_mode
        )

>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
            stream=stream_mode
        )

>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
            stream=stream_mode
        )

>>>>>>> 673954a (Resilience: [error handling])
=======
            stream=stream_mode
        )

>>>>>>> performance-optimization-13534932852089819512
=======
            stream=stream_mode
        )

>>>>>>> api-groq-integration-6554511320622598819
=======
            stream=stream_mode
        )

>>>>>>> api-integrations-groq-3434217061461873316
=======
            stream=stream_mode
        )

>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            stream=stream_mode
        )

>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            stream=stream_mode
        )

>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
            stream=stream_mode
        )

>>>>>>> origin/monitoring-setup-15681340840960488850
=======
            stream=stream_mode
        )

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
            stream=stream_mode
        )

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            stream=stream_mode
        )

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
            stream=stream_mode
        )

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            stream=stream_mode
        )

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
            stream=stream_mode
        )

>>>>>>> origin/api-integrations-groq-12473300930587894354
    if enable_streaming:
        try:
            stream = _create_completion(True)
        except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            return f"Error: {str(e)}"

        collected_chunks = []

=======
            log_error("handle_openai_compatible_provider", e)
            log_api_call("openai_compatible", model_name, time.time() - start_time, False, str(e))
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> 673954a (Resilience: [error handling])
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> performance-optimization-13534932852089819512
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> api-groq-integration-6554511320622598819
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> api-integrations-groq-3434217061461873316
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
            return f"Error: {str(e)}"

        collected_chunks = []
>>>>>>> origin/api-integrations-groq-12473300930587894354
        def _iter_chunks():
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                collected_chunks.append(piece)
                yield piece
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        # Stream to Streamlit (best-effort)
        try:
            st.write_stream(_iter_chunks())
        except Exception:
            pass
        response_text = "".join(collected_chunks)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        return (
            response_text
            if response_text
            else "I apologize, but I couldn't generate a response."
        )
=======
        log_api_call("openai_compatible", model_name, time.time() - start_time, True)
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> 673954a (Resilience: [error handling])
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> performance-optimization-13534932852089819512
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> api-groq-integration-6554511320622598819
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> api-integrations-groq-3434217061461873316
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
        return response_text if response_text else "I apologize, but I couldn't generate a response."
>>>>>>> origin/api-integrations-groq-12473300930587894354
    else:
        try:
            response = _create_completion(False)
        except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            return f"Error: {str(e)}"

        response_text = (
            getattr(response.choices[0].message, "content", None)
            or response.choices[0].message["content"]
        )
=======
            log_error("handle_openai_compatible_provider", e)
            log_api_call("openai_compatible", model_name, time.time() - start_time, False, str(e))
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> 673954a (Resilience: [error handling])
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> performance-optimization-13534932852089819512
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> api-groq-integration-6554511320622598819
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> api-integrations-groq-3434217061461873316
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
>>>>>>> origin/api-integrations-groq-12473300930587894354
        if not response_text:
            response_text = "I apologize, but I couldn't generate a response."
        try:
            st.markdown(response_text)
        except Exception:
            pass
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
        log_api_call("openai_compatible", model_name, time.time() - start_time, True)
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        return response_text


# --- Internet search integration ---
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def perform_internet_search(
    query: str,
    enable_search: bool = True,
    max_results: int = 5,
    search_type: str = "Web",
    time_range: str = "Anytime",
    domain: str = None,
) -> tuple[List[Dict], str]:
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> 673954a (Resilience: [error handling])
=======
@st.cache_data(ttl=300)
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> performance-optimization-13534932852089819512
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> api-groq-integration-6554511320622598819
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> api-integrations-groq-3434217061461873316
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
>>>>>>> origin/api-integrations-groq-12473300930587894354
    if not enable_search:
        return [], ""
    try:
        search_engine = get_internet_search_engine()
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/monitoring-setup-15681340840960488850
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
        if search_type == "News":
             # News search generally supports time range implicitly by recency,
             # but standard DDG news api might handle max_results.
             # If we want detailed time filtering for news, we'd need to extend it,
             # but for now we route to search_news.
             results = search_engine.search_news(query, max_results=max_results)
        else:
             # Standard Web Search with filters
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
        if search_type == "News":
             results = search_engine.search_news(query, max_results=max_results)
        else:
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
             results = search_engine.search(query, max_results=max_results, time_range=time_range, domain=domain)

        if results:
            from ui.internet_search import create_search_context
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
            context = create_search_context(results, query)
            logger.info(f"Search completed with {len(results)} results")
            return results, context
        return [], ""
    except Exception as e:
        logger.error(f"Internet search failed: {str(e)}")
        return [], ""


def augment_prompt_with_search(prompt: str, search_results: List[Dict]) -> str:
    if not search_results:
        return prompt
    from ui.internet_search import create_search_context
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    context = create_search_context(search_results, prompt)
    augmented = f"""{prompt}

[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]:
{context}

Please use the above search results to provide a current and accurate answer."""
    return augmented


# --- Multimodal helpers ---
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
# Performance Optimization: Cached Implementations
@st.cache_data(show_spinner=False)
def _cached_transcribe_audio_bytes(audio_bytes: bytes) -> str:
    try:
        import speech_recognition as sr
        from io import BytesIO
        recognizer = sr.Recognizer()
        with sr.AudioFile(BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception as e:
            logger.warning(f"Speech recognition failed: {e}")
            return "[Transcription failed or not available]"
    except Exception:
        logger.info("speech_recognition not installed or failed")
        return "[Transcription unavailable]"

@st.cache_data(show_spinner=False)
def _cached_extract_video_frame_thumbnails_bytes(video_bytes: bytes, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
        import importlib
        moviepy = importlib.import_module("moviepy.editor")
        VideoFileClip = getattr(moviepy, "VideoFileClip")
        import tempfile
        from io import BytesIO
        import base64
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            tmp.write(video_bytes)
            tmp_name = tmp.name

        try:
            clip = VideoFileClip(tmp_name)
            duration = clip.duration or 0
            times = [(i + 1) * duration / (max_frames + 1) for i in range(max_frames)]
            for t in times:
                frame = clip.get_frame(t)
                img = Image.fromarray(frame)
                buf = BytesIO()
                img.thumbnail((320, 320))
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                thumbnails.append(f"data:image/png;base64,{b64}")
            try:
                clip.reader.close()
            except Exception:
                pass
            clip.audio = None
        finally:
            import os
            try:
                os.unlink(tmp_name)
            except Exception:
                pass
    except Exception as e:
        logger.info(f"moviepy error: {e}")
    return thumbnails

@st.cache_data(show_spinner=False)
def _cached_generate_blip_caption_bytes(image_bytes: bytes) -> Optional[str]:
    try:
        from io import BytesIO
        from PIL import Image
        image = Image.open(BytesIO(image_bytes))

        processor, model, device = get_blip_model()
        inputs = processor(images=image, return_tensors="pt").to(device)
        import torch
        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        logger.info(f"BLIP captioning unavailable: {e}")
        return None

@st.cache_data(ttl=300, show_spinner=False)
def _cached_search_web(query: str, max_results: int, time_range: str, domain: Optional[str]) -> List[Dict]:
    engine = get_internet_search_engine()
    return engine.search(query, max_results=max_results, time_range=time_range, domain=domain)

@st.cache_data(ttl=300, show_spinner=False)
def _cached_search_news(query: str, max_results: int) -> List[Dict]:
    engine = get_internet_search_engine()
    return engine.search_news(query, max_results=max_results)


>>>>>>> b00b3c0 (Performance: Fix CI timeout and refine caching)
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
<<<<<<< HEAD
        for i, img in enumerate(images, 1):
            caption = None
            try:
                info = getattr(img, "info", {}) or {}
                caption = info.get("description") or info.get("caption")
=======
=======
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
>>>>>>> 673954a (Resilience: [error handling])
=======
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
>>>>>>> performance-optimization-13534932852089819512
=======
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
>>>>>>> api-groq-integration-6554511320622598819
=======
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
>>>>>>> api-integrations-groq-3434217061461873316
        from PIL import Image
=======
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
        from PIL import Image
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        for i, img in enumerate(images, 1):
            caption = None
            try:
                info = getattr(img, 'info', {}) or {}
                caption = info.get('description') or info.get('caption')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
            except Exception:
                caption = None
            if not caption:
                try:
                    caption = f"Image {i}: {img.width}x{img.height} pixels"
                except Exception:
                    caption = f"Image {i} (unknown size)"
            results.append({"name": f"image_{i}", "caption": caption})
    except Exception as e:
        logger.error(f"process_images_for_context error: {e}")
    return results

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354

def transcribe_audio_file(file_like) -> str:
    try:
        import speech_recognition as sr
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
=======
@st.cache_data
def extract_file_text(file_type: str, file_content: bytes, file_name: str) -> str:
    """Extract text from PDF or Text files (cached)"""
    try:
        if file_type == "pdf":
            try:
                import PyPDF2
                from io import BytesIO
                pdf = PyPDF2.PdfReader(BytesIO(file_content))
                text = ""
                # extract from first 5 pages for performance
                for page in pdf.pages[:5]:
                    text += page.extract_text() + "\n"
                return f"\n--- PDF {file_name} ---\n{text}\n"
            except ImportError:
                return f"[PyPDF2 not installed - cannot read {file_name}]"
        else:
            # Text/MD
            text = file_content.decode("utf-8")
            return f"\n--- {file_name} ---\n{text}\n"
    except Exception as e:
        logger.error(f"Error extracting text from {file_name}: {e}")
        return f"[Error extracting text from {file_name}]"

@st.cache_data
def transcribe_audio_file(audio_bytes: bytes) -> str:
    """Transcribe audio from bytes (cached)"""
    try:
        import speech_recognition as sr
        from io import BytesIO
        recognizer = sr.Recognizer()
        with sr.AudioFile(BytesIO(audio_bytes)) as source:
>>>>>>> performance-optimization-13534932852089819512
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> api-groq-integration-6554511320622598819
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> api-integrations-groq-3434217061461873316
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
>>>>>>> origin/api-integrations-groq-12473300930587894354
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except Exception as e:
            logger.warning(f"Speech recognition failed: {e}")
            return "[Transcription failed or not available]"
    except Exception:
        logger.info("speech_recognition not installed; skipping transcription")
        return "[Transcription unavailable - install speech_recognition]"


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        import base64
        import importlib
        import tempfile
        from io import BytesIO

        moviepy = importlib.import_module("moviepy.editor")
        VideoFileClip = getattr(moviepy, "VideoFileClip")

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as tmp:
=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
@st.cache_data
def extract_video_frame_thumbnails(video_bytes: bytes, max_frames: int = 3) -> List[str]:
    """Extract thumbnails from video bytes (cached)"""
    thumbnails: List[str] = []
    try:
>>>>>>> performance-optimization-13534932852089819512
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> api-groq-integration-6554511320622598819
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> api-integrations-groq-3434217061461873316
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
>>>>>>> origin/api-integrations-groq-12473300930587894354
        import importlib
        moviepy = importlib.import_module("moviepy.editor")
        VideoFileClip = getattr(moviepy, "VideoFileClip")
        import tempfile
        from io import BytesIO
        import base64
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as tmp:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
            tmp.write(file_like.read())
=======
            tmp.write(video_bytes)
>>>>>>> performance-optimization-13534932852089819512
=======
            tmp.write(file_like.read())
>>>>>>> api-groq-integration-6554511320622598819
=======
            tmp.write(file_like.read())
>>>>>>> api-integrations-groq-3434217061461873316
=======
            tmp.write(file_like.read())
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            tmp.write(file_like.read())
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            tmp.write(file_like.read())
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
            tmp.write(file_like.read())
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
            tmp.write(file_like.read())
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
            tmp.write(file_like.read())
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            tmp.write(file_like.read())
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
            tmp.write(file_like.read())
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            tmp.write(file_like.read())
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
            tmp.write(file_like.read())
>>>>>>> origin/api-integrations-groq-12473300930587894354
            tmp.flush()
            clip = VideoFileClip(tmp.name)
            duration = clip.duration or 0
            times = [(i + 1) * duration / (max_frames + 1) for i in range(max_frames)]
            for t in times:
                frame = clip.get_frame(t)
                img = Image.fromarray(frame)
                buf = BytesIO()
                img.thumbnail((320, 320))
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                img.save(buf, format="PNG")
                b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> 673954a (Resilience: [error handling])
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> performance-optimization-13534932852089819512
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> api-groq-integration-6554511320622598819
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> api-integrations-groq-3434217061461873316
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
>>>>>>> origin/api-integrations-groq-12473300930587894354
                thumbnails.append(f"data:image/png;base64,{b64}")
            try:
                clip.reader.close()
            except Exception:
                pass
            clip.audio = None
    except Exception as e:
        logger.info(f"moviepy not available or failed to extract frames: {e}")
    return thumbnails


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354

# Consolidated BLIP Logic is now at the bottom of the file
# Removed duplicate definition to fix linter error



def generate_blip_caption(image) -> Optional[str]:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    """Generates a caption for the provided image using the BLIP model."""
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
def generate_blip_caption(image) -> Optional[str]:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    try:
        processor, model, device = get_blip_model()
        inputs = processor(images=image, return_tensors="pt").to(device)
        import torch
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        logger.info(f"BLIP captioning unavailable: {e}")
        return None


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def call_hosted_caption_api(
    image, api_url: str, api_key: Optional[str] = None
) -> Optional[str]:
    try:
        from io import BytesIO

        import requests

        buf = BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        files = {"image": ("image.png", buf, "image/png")}
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        resp = requests.post(api_url, files=files, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("caption") or data.get("text")
=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
def call_hosted_caption_api(image, api_url: str, api_key: Optional[str] = None) -> Optional[str]:
    try:
        import requests
        from io import BytesIO
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        files = {'image': ('image.png', buf, 'image/png')}
        headers = {}
        if api_key:
            headers['Authorization'] = f"Bearer {api_key}"
        resp = requests.post(api_url, files=files, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get('caption') or data.get('text')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    except Exception as e:
        logger.info(f"Hosted caption API call failed: {e}")
        return None


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def generate_image_captions(
    images: List,
    use_blip: bool = False,
    hosted_api_url: Optional[str] = None,
    hosted_api_key: Optional[str] = None,
) -> List[Dict]:
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> 673954a (Resilience: [error handling])
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> performance-optimization-13534932852089819512
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> api-groq-integration-6554511320622598819
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> api-integrations-groq-3434217061461873316
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
>>>>>>> origin/api-integrations-groq-12473300930587894354
    if not images:
        return []
    results = []
    for i, img in enumerate(images, 1):
        caption = None
        if hosted_api_url:
            try:
                caption = call_hosted_caption_api(img, hosted_api_url, hosted_api_key)
            except Exception as e:
                logger.info(f"Hosted caption call failed for image {i}: {e}")
        if not caption and use_blip:
            try:
                caption = generate_blip_caption(img)
            except Exception as e:
                logger.info(f"BLIP caption failed for image {i}: {e}")
        if not caption:
            fallback = process_images_for_context([img])[0]
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            caption = fallback.get("caption")
=======
            caption = fallback.get('caption')
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
            caption = fallback.get('caption')
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
            caption = fallback.get('caption')
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
            caption = fallback.get('caption')
>>>>>>> 673954a (Resilience: [error handling])
=======
            caption = fallback.get('caption')
>>>>>>> performance-optimization-13534932852089819512
=======
            caption = fallback.get('caption')
>>>>>>> api-groq-integration-6554511320622598819
=======
            caption = fallback.get('caption')
>>>>>>> api-integrations-groq-3434217061461873316
=======
            caption = fallback.get('caption')
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            caption = fallback.get('caption')
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
            caption = fallback.get('caption')
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
            caption = fallback.get('caption')
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
            caption = fallback.get('caption')
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
            caption = fallback.get('caption')
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            caption = fallback.get('caption')
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
            caption = fallback.get('caption')
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            caption = fallback.get('caption')
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
            caption = fallback.get('caption')
>>>>>>> origin/api-integrations-groq-12473300930587894354
        results.append({"name": f"image_{i}", "caption": caption})
    return results


def preload_blip_model(timeout: int = 120) -> bool:
    try:
        get_blip_model()
        return True
    except Exception as e:
        logger.info(f"Preload BLIP model failed: {e}")
        return False


@st.cache_resource(show_spinner=False)
def _load_blip_resources():
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> 673954a (Resilience: [error handling])
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> performance-optimization-13534932852089819512
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> api-groq-integration-6554511320622598819
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> api-integrations-groq-3434217061461873316
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
    from transformers import BlipProcessor, BlipForConditionalGeneration
>>>>>>> origin/daily-ai-improvement-16784022982147370640
    import torch

    model_id = "Salesforce/blip-image-captioning-base"
    
=======
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch

    model_id = "Salesforce/blip-image-captioning-base"

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    # helper to load with retry strategy
    def load_with_fallback(cls, model_id):
        # 1. Try local cache first
        try:
            return cls.from_pretrained(model_id, local_files_only=True)
        except Exception:
            # 2. Try download
            return cls.from_pretrained(model_id, local_files_only=False)

    processor = load_with_fallback(BlipProcessor, model_id)
    model = load_with_fallback(BlipForConditionalGeneration, model_id)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
=======

>>>>>>> origin/monitoring-setup-15681340840960488850
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return processor, model, device

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

def get_blip_model():
    return _load_blip_resources()


def preload_blip_model_with_progress(
    progress_callback: Optional[Callable[[int, str], None]] = None,
) -> bool:
=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
def get_blip_model():
    return _load_blip_resources()

def preload_blip_model_with_progress(progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/daily-ai-improvement-16784022982147370640
=======
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
    """
    Simulated progress loader that actually just triggers the cached resource load.
    Since st.cache_resource handles the singleton, we just call it.
    """
    try:
        if progress_callback:
            progress_callback(10, "Checking local cache...")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.
        
=======
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354

        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
        if progress_callback:
             progress_callback(30, "Loading BLIP model items...")

        # This will block until loaded
        _load_blip_resources()
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        
=======

>>>>>>> origin/monitoring-setup-15681340840960488850
=======

>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======

>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======

>>>>>>> origin/api-integrations-groq-12473300930587894354
        if progress_callback:
            progress_callback(100, "BLIP model ready")
        return True
    except Exception as e:
        logger.error(f"BLIP load failed: {e}")
        if progress_callback:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            progress_callback(0, f"Failed: {str(e)}")
        return False


def serialize_messages(messages: List[Dict]) -> List[Dict]:
    """
    Prepare messages for JSON export by handling non-serializable objects (like PIL Images).
    """
    serializable = []
    for msg in messages:
        # Shallow copy is enough for the dict itself
        clean_msg = msg.copy()

        # Handle images - create a new list so we don't modify the original message's list
        if "images" in clean_msg and clean_msg["images"]:
            img_desc = []
            for img in clean_msg["images"]:
                try:
                    if hasattr(img, 'format') and hasattr(img, 'size'):
                         desc = f"Image <{img.format} {img.size}>"
                    else:
                         desc = str(img)
                except Exception:
                    desc = "Image <Unknown>"
                img_desc.append(desc)
            clean_msg["images"] = img_desc

        serializable.append(clean_msg)
    return serializable
=======
=======
>>>>>>> origin/analytics-logging-feedback-9776000052567751767
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/api-integrations-groq-12473300930587894354
             progress_callback(0, f"Failed: {str(e)}")
        return False

    except Exception as e:
        logger.info(f"extract_video_frame_thumbnails error: {e}")
<<<<<<< HEAD
        return thumbnails
<<<<<<< HEAD
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> origin/monitoring-setup-15681340840960488850
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> origin/fix-syntax-error-and-asyncio-safety-16013430086854294306
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> origin/analytics-monitoring-16051435839535532537
=======

import streamlit as st
import logging
from typing import List, Dict, Optional, Any, Callable, Tuple

logger = logging.getLogger(__name__)

# BLIP cache holds (processor, model, device)
BLIP_CACHE: Optional[Tuple[Any, Any, Any]] = None


# --- Cached clients / resources ---
@st.cache_resource
def get_internet_search_engine():
    from ui.internet_search import InternetSearchEngine
    return InternetSearchEngine()


@st.cache_resource
def get_openai_client(api_key: str, base_url: Optional[str] = None):
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)


@st.cache_resource
def get_anthropic_client(api_key: str):
    from anthropic import Anthropic
    return Anthropic(api_key=api_key)


@st.cache_resource
def get_google_client(api_key: str):
    # Import dynamically to avoid hard dependency if not used
    # NOTE: google.generativeai is deprecated in favor of google.genai (v1.0+).
    # Migration requires refactoring handle_google_provider to use Client API.
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    return genai

# --- Conversation helpers ---
def build_conversation_history(messages: List[Dict], exclude_last: bool = True, max_messages: int = 20, max_chars: int = 50000) -> List[Dict]:
    history = messages[:-1] if exclude_last and len(messages) > 0 else messages
    if not history:
        return []
    formatted = [{"role": msg["role"], "content": msg["content"]} for msg in history if "role" in msg and "content" in msg]
    total_chars = sum(len(m.get("content", "")) for m in formatted)
    if len(formatted) > max_messages or total_chars > max_chars:
        older = formatted[:-max_messages] if len(formatted) > max_messages else []
        recent = formatted[-max_messages:]
        if older:
            older_summary_parts = []
            for msg in older[-10:]:
                content = msg.get("content", "")
                preview = content[:200] + "..." if len(content) > 200 else content
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
            return [{"role": "system", "content": summary_text}] + recent
        else:
            return recent
    return formatted


def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": current_prompt})
    return messages


# --- Resilience Helpers ---
import time
import functools

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

# --- Provider Handlers ---
def handle_google_provider(
    api_key: str, 
    model_name: str, 
    prompt: str, 
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.95,
    images: List = None,
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide a Google API Key."
        import google.generativeai as genai
        # Configure the global instance
        genai.configure(api_key=api_key)
        
        # Mapping config specifically for GenerativeModel
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            top_p=top_p
        )
        
        # Initialize model
        # system_instruction is supported in newer versions as init argument or via specific methods
        # For broader compatibility, passing via constructor if supported, else prepending to prompt might be needed
        # But latest SDK supports 'system_instruction' in GenerativeModel constructor
        try:
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
        except TypeError:
            # Fallback for older SDK versions that don't support system_instruction in init
            model = genai.GenerativeModel(model_name=model_name)
            if system_instruction:
                prompt = f"{system_instruction}\n\n{prompt}"
            
        contents = []
        if images:
            from io import BytesIO
            import base64
            for img in images:
                # Gemai SDK can take PIL images directly in 'contents'
                contents.append(img)
        
        contents.append(prompt)
        
        @retry_with_backoff(retries=2)
        def _generate():
            # For gemini, we can pass stream=True/False to generate_content
            return model.generate_content(
                contents, 
                generation_config=generation_config,
                stream=enable_streaming
            )

        response = _generate()
        
        if enable_streaming:
            collected_text = []
            def _stream_gen():
                for chunk in response:
                    if chunk.text:
                        collected_text.append(chunk.text)
                        yield chunk.text
            
            try:
                st.write_stream(_stream_gen())
            except Exception as e:
                logger.warning(f"Google streaming visualization failed: {e}")
            
            return "".join(collected_text)
        else:
             return response.text

    except Exception as e:
        logger.error(f"Google provider error: {e}")
        return f"Error connecting to Google Gemini: {str(e)}"

def handle_anthropic_provider(
    api_key: str,
    model_name: str,
    messages: List[Dict],
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide an Anthropic API Key."
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        kwargs = {
             "model": model_name,
             "messages": messages,
             "max_tokens": max_tokens,
             "temperature": temperature,
        }
        if system_instruction:
             kwargs["system"] = system_instruction
             
        @retry_with_backoff(retries=2)
        def _create_message():
            if enable_streaming:
                return client.messages.create(stream=True, **kwargs)
            else:
                return client.messages.create(stream=False, **kwargs)

        response = _create_message()
        
        if enable_streaming:
            collected_text = []
            def _stream_gen():
                for event in response:
                    if event.type == 'content_block_delta':
                        text = event.delta.text
                        collected_text.append(text)
                        yield text
            
            try:
                st.write_stream(_stream_gen())
            except Exception:
                pass
            return "".join(collected_text)
        else:
            return response.content[0].text

    except Exception as e:
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"

def generate_standard_response(
    provider: str,
    model_name: str,
    api_keys: Dict[str, str],
    prompt: str,
    chat_history: List[Dict],
    system_instruction: str = "",
    config: Dict[str, Any] = {},
    images: List = None
) -> str:
    """Unified dispatcher for standard mode chat generation"""
    api_key = api_keys.get(provider)
    if not api_key:
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
        temp = config.get('temperature', 0.7)
        max_tok = config.get('max_tokens', 2048)
        top_p = config.get('top_p', 0.95)
        stream = config.get('enable_streaming', False)

        if provider == "google":
            return handle_google_provider(
                api_key, model_name, prompt, system_instruction, 
                temp, max_tok, top_p, images, enable_streaming=stream
            )
            
        elif provider in ["openai", "together", "xai", "deepseek"]:
            base_urls = {
                "together": "https://api.together.xyz/v1",
                "xai": "https://api.x.ai/v1",
                "deepseek": "https://api.deepseek.com"
            }
            client = get_openai_client(api_key, base_urls.get(provider))
            msgs = create_openai_messages(build_conversation_history(chat_history), prompt, system_instruction)
            return handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)
            
        elif provider == "anthropic":
            # Anthropic expects just user/assistant messages
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
            return handle_anthropic_provider(
                api_key, model_name, msgs, system_instruction, 
                temp, max_tok, enable_streaming=stream
            )
            
        return "Provider not supported."
        
    except Exception as e:
        return f"Generation Error: {str(e)}"

def prepare_brain_configuration(api_keys: Dict[str, str], requested_models: List[str] = None) -> List[Dict[str, Any]]:
    """Helper to build the list of models for Brain Mode based on available keys"""
    models_to_query = []
    
    # Default strategy: Use available keys (simplified)
    # In a real app, 'requested_models' would come from user config
    
    if api_keys.get('google'):
        models_to_query.append({"provider": "google", "model": "gemini-1.5-flash", "api_key": api_keys['google']})
        
    if api_keys.get('openai'):
        models_to_query.append({"provider": "openai", "model": "gpt-4o-mini", "api_key": api_keys['openai']})
        
    if api_keys.get('anthropic'):
         models_to_query.append({"provider": "anthropic", "model": "claude-3-5-haiku-20241022", "api_key": api_keys['anthropic']})

    return models_to_query

def handle_openai_compatible_provider(
    client: Any,
    model_name: str,
    messages: List[Dict],
    temperature: float,
    max_tokens: int,
    top_p: float,
    enable_streaming: bool
) -> str:
    @retry_with_backoff(retries=2)
    def _create_completion(stream_mode):
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream_mode
        )

    if enable_streaming:
        try:
            stream = _create_completion(True)
        except Exception as e:
            return f"Error: {str(e)}"

        collected_chunks = []
        def _iter_chunks():
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                collected_chunks.append(piece)
                yield piece
        # Stream to Streamlit (best-effort)
        try:
            st.write_stream(_iter_chunks())
        except Exception:
            pass
        response_text = "".join(collected_chunks)
        return response_text if response_text else "I apologize, but I couldn't generate a response."
    else:
        try:
            response = _create_completion(False)
        except Exception as e:
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
        if not response_text:
            response_text = "I apologize, but I couldn't generate a response."
        try:
            st.markdown(response_text)
        except Exception:
            pass
        return response_text


# --- Internet search integration ---
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
    if not enable_search:
        return [], ""
    try:
        search_engine = get_internet_search_engine()
        
        if search_type == "News":
             # News search generally supports time range implicitly by recency, 
             # but standard DDG news api might handle max_results.
             # If we want detailed time filtering for news, we'd need to extend it, 
             # but for now we route to search_news.
             results = search_engine.search_news(query, max_results=max_results)
        else:
             # Standard Web Search with filters
             results = search_engine.search(query, max_results=max_results, time_range=time_range, domain=domain)
             
        if results:
            from ui.internet_search import create_search_context
            context = create_search_context(results, query)
            logger.info(f"Search completed with {len(results)} results")
            return results, context
        return [], ""
    except Exception as e:
        logger.error(f"Internet search failed: {str(e)}")
        return [], ""


def augment_prompt_with_search(prompt: str, search_results: List[Dict]) -> str:
    if not search_results:
        return prompt
    from ui.internet_search import create_search_context
    context = create_search_context(search_results, prompt)
    augmented = f"""{prompt}

[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]:
{context}

Please use the above search results to provide a current and accurate answer."""
    return augmented


# --- Multimodal helpers ---
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
        from PIL import Image
        for i, img in enumerate(images, 1):
            caption = None
            try:
                info = getattr(img, 'info', {}) or {}
                caption = info.get('description') or info.get('caption')
            except Exception:
                caption = None
            if not caption:
                try:
                    caption = f"Image {i}: {img.width}x{img.height} pixels"
                except Exception:
                    caption = f"Image {i} (unknown size)"
            results.append({"name": f"image_{i}", "caption": caption})
    except Exception as e:
        logger.error(f"process_images_for_context error: {e}")
    return results


def transcribe_audio_file(file_like) -> str:
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except Exception as e:
            logger.warning(f"Speech recognition failed: {e}")
            return "[Transcription failed or not available]"
    except Exception:
        logger.info("speech_recognition not installed; skipping transcription")
        return "[Transcription unavailable - install speech_recognition]"


def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
        import importlib
        moviepy = importlib.import_module("moviepy.editor")
        VideoFileClip = getattr(moviepy, "VideoFileClip")
        import tempfile
        from io import BytesIO
        import base64
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as tmp:
            tmp.write(file_like.read())
            tmp.flush()
            clip = VideoFileClip(tmp.name)
            duration = clip.duration or 0
            times = [(i + 1) * duration / (max_frames + 1) for i in range(max_frames)]
            for t in times:
                frame = clip.get_frame(t)
                img = Image.fromarray(frame)
                buf = BytesIO()
                img.thumbnail((320, 320))
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                thumbnails.append(f"data:image/png;base64,{b64}")
            try:
                clip.reader.close()
            except Exception:
                pass
            clip.audio = None
    except Exception as e:
        logger.info(f"moviepy not available or failed to extract frames: {e}")
    return thumbnails



# Consolidated BLIP Logic is now at the bottom of the file
# Removed duplicate definition to fix linter error



def generate_blip_caption(image) -> Optional[str]:
    try:
        processor, model, device = get_blip_model()
        inputs = processor(images=image, return_tensors="pt").to(device)
        import torch
        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        logger.info(f"BLIP captioning unavailable: {e}")
        return None


def call_hosted_caption_api(image, api_url: str, api_key: Optional[str] = None) -> Optional[str]:
    try:
        import requests
        from io import BytesIO
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        files = {'image': ('image.png', buf, 'image/png')}
        headers = {}
        if api_key:
            headers['Authorization'] = f"Bearer {api_key}"
        resp = requests.post(api_url, files=files, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get('caption') or data.get('text')
    except Exception as e:
        logger.info(f"Hosted caption API call failed: {e}")
        return None


def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
    if not images:
        return []
    results = []
    for i, img in enumerate(images, 1):
        caption = None
        if hosted_api_url:
            try:
                caption = call_hosted_caption_api(img, hosted_api_url, hosted_api_key)
            except Exception as e:
                logger.info(f"Hosted caption call failed for image {i}: {e}")
        if not caption and use_blip:
            try:
                caption = generate_blip_caption(img)
            except Exception as e:
                logger.info(f"BLIP caption failed for image {i}: {e}")
        if not caption:
            fallback = process_images_for_context([img])[0]
            caption = fallback.get('caption')
        results.append({"name": f"image_{i}", "caption": caption})
    return results


def preload_blip_model(timeout: int = 120) -> bool:
    try:
        get_blip_model()
        return True
    except Exception as e:
        logger.info(f"Preload BLIP model failed: {e}")
        return False


@st.cache_resource(show_spinner=False)
def _load_blip_resources():
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    
    model_id = "Salesforce/blip-image-captioning-base"
    
    # helper to load with retry strategy
    def load_with_fallback(cls, model_id):
        # 1. Try local cache first
        try:
            return cls.from_pretrained(model_id, local_files_only=True)
        except Exception:
            # 2. Try download
            return cls.from_pretrained(model_id, local_files_only=False)

    processor = load_with_fallback(BlipProcessor, model_id)
    model = load_with_fallback(BlipForConditionalGeneration, model_id)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return processor, model, device

def get_blip_model():
    return _load_blip_resources()

def preload_blip_model_with_progress(progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
    """
    Simulated progress loader that actually just triggers the cached resource load.
    Since st.cache_resource handles the singleton, we just call it.
    """
    try:
        if progress_callback:
            progress_callback(10, "Checking local cache...")
        
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.
        
        if progress_callback:
             progress_callback(30, "Loading BLIP model items...")
        
        # This will block until loaded
        _load_blip_resources()
        
        if progress_callback:
            progress_callback(100, "BLIP model ready")
        return True
    except Exception as e:
        logger.error(f"BLIP load failed: {e}")
        if progress_callback:
             progress_callback(0, f"Failed: {str(e)}")
        return False
<<<<<<< HEAD
>>>>>>> origin/code-review-fix-dead-code-security-warning-7379667601375496538
=======

>>>>>>> origin/fix-chat-utils-syntax-error-3738676403581165176
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> origin/ethics-bias-fixes-185826756388721926
=======
        return thumbnails
>>>>>>> origin/api-integrations-groq-12473300930587894354

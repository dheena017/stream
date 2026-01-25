<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import functools
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import streamlit as st
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

import streamlit as st
import logging
from typing import List, Dict, Optional, Any, Callable, Tuple
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

import streamlit as st
import logging
from typing import List, Dict, Optional, Any, Callable, Tuple
import time
import functools
from io import BytesIO
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819

logger = logging.getLogger(__name__)

# BLIP cache holds (processor, model, device)
BLIP_CACHE: Optional[Tuple[Any, Any, Any]] = None
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


@st.cache_resource
def get_anthropic_client(api_key: str):
    from anthropic import Anthropic
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
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

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
    api_key: str,
    model_name: str,
    prompt: str,
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
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide a Google API Key."
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
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> api-groq-integration-6554511320622598819
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

        contents = []
        if images:
=======
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> api-groq-integration-6554511320622598819
        contents = []
        if images:
            from io import BytesIO
            import base64
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
            for img in images:
                # Gemai SDK can take PIL images directly in 'contents'
                contents.append(img)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

        contents.append(prompt)


=======
        contents.append(prompt)

>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
        contents.append(prompt)

>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
        contents.append(prompt)

>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
        contents.append(prompt)

>>>>>>> 673954a (Resilience: [error handling])
=======
        contents.append(prompt)

>>>>>>> performance-optimization-13534932852089819512
=======
        contents.append(prompt)

>>>>>>> api-groq-integration-6554511320622598819
        @retry_with_backoff(retries=2)
        def _generate():
            # For gemini, we can pass stream=True/False to generate_content
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
        response = _generate()

        if enable_streaming:
            collected_text = []
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

    except Exception as e:
        logger.error(f"Google provider error: {e}")
        return f"Error connecting to Google Gemini: {str(e)}"

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
            return "".join(collected_text)
        else:
             return response.text

    except Exception as e:
        logger.error(f"Google provider error: {e}")
        return f"Error: Google Gemini - {str(e)}"

>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
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
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide an Anthropic API Key."
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
        response = _create_message()


        if enable_streaming:
            collected_text = []

            def _stream_gen():
                for event in response:
                    if event.type == "content_block_delta":
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
        response = _create_message()

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
                        text = event.delta.text
                        collected_text.append(text)
                        yield text

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
            return "".join(collected_text)
        else:
            return response.content[0].text

    except Exception as e:
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
) -> str:
    """Unified dispatcher for standard mode chat generation"""
    api_key = api_keys.get(provider)
    if not api_key:
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
        temp = config.get('temperature', 0.7)
        max_tok = config.get('max_tokens', 2048)
        top_p = config.get('top_p', 0.95)
        stream = config.get('enable_streaming', False)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889

        if provider == "google":
            return handle_google_provider(
=======

        response_text = ""

        if provider == "google":
            response_text = handle_google_provider(
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> 673954a (Resilience: [error handling])
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> performance-optimization-13534932852089819512
=======

        if provider == "google":
            return handle_google_provider(
>>>>>>> api-groq-integration-6554511320622598819
                api_key, model_name, prompt, system_instruction,
                temp, max_tok, top_p, images, enable_streaming=stream
            )

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
        elif provider in ["openai", "together", "xai", "deepseek"]:
            base_urls = {
                "together": "https://api.together.xyz/v1",
                "xai": "https://api.x.ai/v1",
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
        elif provider in ["openai", "together", "xai", "deepseek", "groq"]:
            base_urls = {
                "together": "https://api.together.xyz/v1",
                "xai": "https://api.x.ai/v1",
                "deepseek": "https://api.deepseek.com",
                "groq": "https://api.groq.com/openai/v1"
>>>>>>> api-groq-integration-6554511320622598819
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
            return handle_anthropic_provider(
                api_key, model_name, msgs, system_instruction,
                temp, max_tok, enable_streaming=stream
            )

<<<<<<< HEAD
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
                "deepseek": "https://api.deepseek.com"
            }
            client = get_openai_client(api_key, base_urls.get(provider))
            msgs = create_openai_messages(build_conversation_history(chat_history), prompt, system_instruction)
            response_text = handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)

        elif provider == "anthropic":
            # Anthropic expects just user/assistant messages
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
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
        return "Provider not supported."

    except Exception as e:
        return f"Generation Error: {str(e)}"

<<<<<<< HEAD
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
def prepare_brain_configuration(api_keys: Dict[str, str], requested_models: List[str] = None) -> List[Dict[str, Any]]:
    """Helper to build the list of models for Brain Mode based on available keys"""
    models_to_query = []

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
    # Default strategy: Use available keys (simplified)
    # In a real app, 'requested_models' would come from user config

    if api_keys.get('google'):
        models_to_query.append({"provider": "google", "model": "gemini-1.5-flash", "api_key": api_keys['google']})

    if api_keys.get('openai'):
        models_to_query.append({"provider": "openai", "model": "gpt-4o-mini", "api_key": api_keys['openai']})

    if api_keys.get('anthropic'):
         models_to_query.append({"provider": "anthropic", "model": "claude-3-5-haiku-20241022", "api_key": api_keys['anthropic']})

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
        return response_text


# --- Internet search integration ---
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

=======
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> api-groq-integration-6554511320622598819
        if search_type == "News":
             # News search generally supports time range implicitly by recency,
             # but standard DDG news api might handle max_results.
             # If we want detailed time filtering for news, we'd need to extend it,
             # but for now we route to search_news.
             results = search_engine.search_news(query, max_results=max_results)
        else:
             # Standard Web Search with filters
<<<<<<< HEAD
=======
        if search_type == "News":
             results = search_engine.search_news(query, max_results=max_results)
        else:
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> api-groq-integration-6554511320622598819
             results = search_engine.search(query, max_results=max_results, time_range=time_range, domain=domain)

        if results:
            from ui.internet_search import create_search_context
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
        from PIL import Image
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
=======
>>>>>>> api-groq-integration-6554511320622598819

def transcribe_audio_file(file_like) -> str:
    try:
        import speech_recognition as sr
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
# Consolidated BLIP Logic is now at the bottom of the file
# Removed duplicate definition to fix linter error


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
def generate_blip_caption(image) -> Optional[str]:
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
    except Exception as e:
        logger.info(f"Hosted caption API call failed: {e}")
        return None


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
    import torch

    model_id = "Salesforce/blip-image-captioning-base"

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
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return processor, model, device

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
def get_blip_model():
    return _load_blip_resources()

def preload_blip_model_with_progress(progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
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

        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.


=======
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

>>>>>>> 673954a (Resilience: [error handling])
=======
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

>>>>>>> performance-optimization-13534932852089819512
=======
        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

>>>>>>> api-groq-integration-6554511320622598819
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
             progress_callback(0, f"Failed: {str(e)}")
        return False

    except Exception as e:
        logger.info(f"extract_video_frame_thumbnails error: {e}")
        return thumbnails
>>>>>>> origin/analytics-monitoring-17353357073288903889
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

<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> 9a44f3f (Ethics: [bias fixes])
=======
>>>>>>> d4117c9 (Review: Fix syntax error and refactor inline styles)
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False



def serialize_messages(messages: List[Dict]) -> str:
    """
    Prepare messages for JSON export by removing non-serializable objects.
    """
    serializable_messages = []
    for msg in messages:
        # Shallow copy to avoid modifying original and to avoid deepcopy issues with open files
        msg_copy = msg.copy()

        # Handle images
        if "images" in msg_copy and msg_copy["images"]:
            # Replace actual image objects with string descriptions
            # We use a safe getattr approach in case it's not a standard PIL image
            msg_copy["images"] = [
                f"<Image: {getattr(img, 'format', 'unknown')} {getattr(img, 'size', 'unknown')}>"
                for img in msg_copy["images"]
            ]

        serializable_messages.append(msg_copy)

    return json.dumps(serializable_messages, indent=2, default=str)
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> performance-optimization-13534932852089819512
=======
             progress_callback(0, f"Failed: {str(e)}")
        return False
>>>>>>> api-groq-integration-6554511320622598819

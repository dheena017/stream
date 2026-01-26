import json
import time
import functools
from typing import List, Dict, Any, Optional, Union
import tenacity
from loguru import logger

# Placeholder for dependencies
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import openai
    from openai import OpenAI
except ImportError:
    openai = None
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None

from ui.ethics import EthicsGuardian

# --- Retry Decorator ---

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    """
    Decorator to retry a function with exponential backoff.
    """
    return tenacity.retry(
        stop=tenacity.stop_after_attempt(retries + 1),
        wait=tenacity.wait_exponential(multiplier=backoff_in_seconds, min=backoff_in_seconds, max=10),
        reraise=True
    )

# --- Serialization ---

def serialize_messages(messages: List[Dict]) -> str:
    """Serializes messages to JSON, handling images."""
    serializable_messages = []
    for msg in messages:
        msg_copy = msg.copy()
        if "images" in msg_copy:
            # Convert images to string descriptions for JSON
            img_desc = []
            for img in msg_copy["images"]:
                # Check for PIL Image attributes or similar
                if hasattr(img, "format") and hasattr(img, "size"):
                    img_desc.append(f"Image: {img.format} {img.size}")
                else:
                    img_desc.append(str(img))
            msg_copy["images"] = img_desc
        serializable_messages.append(msg_copy)
    return json.dumps(serializable_messages)

# --- History Management ---

def build_conversation_history(messages: List[Dict], max_messages: int = None, exclude_last: bool = True, max_chars: int = None) -> List[Dict]:
    """
    Builds conversation history for API calls.
    exclude_last: If True, excludes the very last message (usually the current user prompt).
    max_messages: Limit the number of recent messages to include.
    """
    # Create a copy to avoid mutating original list
    history = list(messages)

    if exclude_last and history:
        history.pop()

    if max_messages and len(history) > max_messages:
        # Keep the most recent max_messages
        recent = history[-max_messages:]
        # Add a summary placeholder at the beginning
        summary_msg = {"role": "system", "content": "[Earlier conversation summary]"}
        return [summary_msg] + recent

    return history

def create_openai_messages(history: List[Dict], prompt: str, system_instruction: str = None) -> List[Dict]:
    """Creates a list of messages formatted for OpenAI API."""
    msgs = []
    if system_instruction:
        msgs.append({"role": "system", "content": system_instruction})

    for h in history:
        # Filter out keys not supported by OpenAI (like 'images' if not formatted correctly)
        # For now, just pass role and content
        content = h.get("content", "")
        msgs.append({"role": h["role"], "content": content})

    msgs.append({"role": "user", "content": prompt})
    return msgs

# --- Search ---

def get_internet_search_engine():
    # Import locally to avoid circular deps or verify usage
    try:
        from ui import internet_search
        return internet_search.get_engine()
    except (ImportError, AttributeError):
        return None

def perform_internet_search(query: str, enable_search: bool = False):
    if not enable_search:
        return [], ""

    engine = get_internet_search_engine()
    if not engine:
        return [], ""

    try:
        results = engine.search(query)
        # Format context
        context = "\n".join([f"Title: {r.get('title')}\nBody: {r.get('body')}" for r in results])
        return results, context
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return [], ""

def augment_prompt_with_search(prompt: str, search_results: List[Dict]) -> str:
    if not search_results:
        return prompt

    context_str = ""
    for r in search_results:
        context_str += f"- {r.get('title', 'No Title')}: {r.get('body', 'No Content')}\n"

    augmented = f"""
    [SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]
    {context_str}

    User Query: {prompt}
    """
    return augmented.strip()

# --- Response Generation ---

def get_openai_client(api_key, base_url=None):
    if OpenAI:
        return OpenAI(api_key=api_key, base_url=base_url)
    return None

def handle_google_provider(api_key, model_name, prompt):
    if not genai:
        return "Error: Google Generative AI not installed."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Google Provider failed - {str(e)}"

def handle_openai_compatible_provider(api_key, model_name, messages, base_url=None):
    client = get_openai_client(api_key, base_url)
    if not client:
        return "Error: OpenAI client not available."
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: OpenAI Provider failed - {str(e)}"

def handle_anthropic_provider(api_key, model_name, messages):
    if not anthropic:
        return "Error: Anthropic not installed."
    try:
        client = anthropic.Anthropic(api_key=api_key)
        # Anthropic expects specific format, simplified here
        system = None
        # Extract system if present
        filtered_msgs = []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                filtered_msgs.append(m)

        kwargs = {
            "model": model_name,
            "messages": filtered_msgs,
            "max_tokens": 1024
        }
        if system:
            kwargs["system"] = system

        response = client.messages.create(**kwargs)
        return response.content[0].text
    except Exception as e:
        return f"Error: Anthropic Provider failed - {str(e)}"

def generate_standard_response(provider, model_name, api_keys, prompt, chat_history, config=None):
    if provider not in api_keys:
        return "Error: Missing API Key"

    api_key = api_keys[provider]

    # Ethics Check
    guardian = EthicsGuardian()
    is_safe, issue = guardian.check_safety(prompt)
    disclaimer = ""
    system_instruction = "You are a helpful assistant."

    if issue:
        # Augment system instruction
        system_instruction = guardian.augment_system_instruction(system_instruction, issue)
        # Get disclaimer
        disclaimer_text = guardian.get_disclaimer(issue)
        if disclaimer_text:
            disclaimer = f"\n\n[Ethics Notice: {disclaimer_text}]"

    response_text = ""

    if provider == "google":
        # Augment prompt for Google since we used simple generation
        augmented_prompt = f"{system_instruction}\n\nUser: {prompt}"
        response_text = handle_google_provider(api_key, model_name, augmented_prompt)

    elif provider == "openai":
        messages = create_openai_messages(chat_history, prompt, system_instruction=system_instruction)
        response_text = handle_openai_compatible_provider(api_key, model_name, messages)

    elif provider == "anthropic":
        messages = create_openai_messages(chat_history, prompt, system_instruction=system_instruction)
        response_text = handle_anthropic_provider(api_key, model_name, messages)

    else:
        return "Error: Unknown provider"

    # Append disclaimer if response is successful (not an error string)
    if response_text and not response_text.startswith("Error:") and disclaimer:
        response_text += disclaimer

    return response_text

def prepare_brain_configuration(api_keys: Dict[str, str]) -> List[Dict]:
    configs = []
    if "google" in api_keys:
        configs.append({"provider": "google", "model": "gemini-pro"})
    if "openai" in api_keys:
        configs.append({"provider": "openai", "model": "gpt-4"})
    return configs

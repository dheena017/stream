import json
import logging
import time
from typing import List, Dict, Any, Optional, Callable
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Set up logging
logger = logging.getLogger(__name__)

def retry_with_backoff(retries: int = 3, backoff_in_seconds: float = 1.0):
    """
    Decorator to retry a function with exponential backoff.
    """
    return retry(
        stop=stop_after_attempt(retries + 1), # +1 because initial call is attempt 1
        wait=wait_exponential(multiplier=backoff_in_seconds, min=backoff_in_seconds, max=10),
        reraise=True
    )

def serialize_messages(messages: List[Dict[str, Any]]) -> str:
    """
    Serializes messages to JSON, handling non-serializable objects like Images.
    """
    serializable_messages = []
    for msg in messages:
        msg_copy = msg.copy()
        if "images" in msg_copy:
            # Convert images to string descriptions
            img_descriptions = []
            for img in msg_copy["images"]:
                if hasattr(img, "format") and hasattr(img, "size"):
                    img_descriptions.append(f"Image: {img.format} {img.size}")
                else:
                    img_descriptions.append(str(img))
            msg_copy["images"] = img_descriptions
        serializable_messages.append(msg_copy)
    return json.dumps(serializable_messages)

def build_conversation_history(
    messages: List[Dict[str, Any]],
    exclude_last: bool = True,
    max_messages: int = 50, # Default from memory
    max_chars: int = 20000
) -> List[Dict[str, Any]]:
    """
    Builds conversation history with truncation and summarization support.
    """
    msgs_to_process = messages[:-1] if exclude_last and messages else messages

    # Simple truncation logic based on count
    if len(msgs_to_process) > max_messages:
        # Keep the most recent max_messages
        recent_msgs = msgs_to_process[-max_messages:]
        # Add a summary placeholder
        summary_msg = {
            "role": "system",
            "content": f"[Earlier conversation summary] (Truncated {len(msgs_to_process) - max_messages} messages)"
        }
        return [summary_msg] + recent_msgs

    return msgs_to_process

def create_openai_messages(
    history: List[Dict[str, Any]],
    prompt: str,
    system_instruction: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Creates the list of messages for OpenAI API.
    """
    msgs = []
    if system_instruction:
        msgs.append({"role": "system", "content": system_instruction})

    for h in history:
        # filter out keys not needed for openai (like 'images' if not supported in this simplistic version)
        # keeping it simple
        msgs.append({"role": h.get("role", "user"), "content": h.get("content", "")})

    msgs.append({"role": "user", "content": prompt})
    return msgs

def prepare_brain_configuration(api_keys: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Prepares configuration for available providers based on API keys.
    """
    configs = []
    if api_keys.get("google"):
        configs.append({"provider": "google", "api_key": api_keys["google"]})
    if api_keys.get("openai"):
        configs.append({"provider": "openai", "api_key": api_keys["openai"]})
    if api_keys.get("anthropic"):
        configs.append({"provider": "anthropic", "api_key": api_keys["anthropic"]})
    return configs

def augment_prompt_with_search(prompt: str, search_results: List[Dict[str, Any]]) -> str:
    """
    Augments the prompt with search results.
    """
    if not search_results:
        return prompt

    context = "\n".join([f"- {r.get('title', 'No Title')}: {r.get('body', '')}" for r in search_results])

    augmented = f"""{prompt}

[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]
The following search results may be relevant:
{context}
"""
    return augmented

def get_internet_search_engine():
    # Stub or import logic. Since ui.internet_search is empty, we return a mock or None.
    # In production, this would initialize DDGS or similar.
    # For now, we raise if called to ensure we know it's missing, but tests mock it.
    raise NotImplementedError("Search engine not initialized")

def perform_internet_search(query: str, enable_search: bool = False):
    """
    Performs internet search and returns results and context string.
    """
    if not enable_search:
        return [], ""

    try:
        engine = get_internet_search_engine()
        results = engine.search(query)
        context = "\n".join([f"{r.get('body','')}" for r in results])
        return results, context
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return [], ""

# Provider Handlers (Stubs)

def handle_google_provider(config, model_name, prompt, chat_history):
    return "Google Response (Stub)"

def handle_anthropic_provider(config, model_name, prompt, chat_history):
    return "Anthropic Response (Stub)"

def handle_openai_compatible_provider(client, model_name, messages):
    return "OpenAI Response (Stub)"

def get_openai_client(api_key):
    return None

def generate_standard_response(
    provider: str,
    model_name: str,
    api_keys: Dict[str, str],
    prompt: str,
    chat_history: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generates a response using the specified provider.
    """
    if provider not in api_keys and provider != "ollama": # Assuming ollama doesn't need key
         return "Error: Missing API Key for provider: " + provider

    try:
        if provider == "google":
            return handle_google_provider(
                {"api_key": api_keys["google"]},
                model_name,
                prompt,
                chat_history
            )
        elif provider == "anthropic":
             return handle_anthropic_provider(
                {"api_key": api_keys["anthropic"]},
                model_name,
                prompt,
                chat_history
            )
        elif provider == "openai":
            # Simplified for stub
            return handle_openai_compatible_provider(None, model_name, [])
        else:
            return f"Error: Provider {provider} not supported."

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        return f"Error: {str(e)}"

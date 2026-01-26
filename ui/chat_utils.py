
import json
import logging
from typing import List, Dict, Any, Optional, Union
from tenacity import retry, stop_after_attempt, wait_fixed
import ui.internet_search

logger = logging.getLogger(__name__)

def serialize_messages(messages: List[Dict[str, Any]]) -> str:
    """Serializes messages to JSON, handling non-serializable objects like Images."""
    serializable_messages = []
    for msg in messages:
        msg_copy = msg.copy()
        if "images" in msg_copy and msg_copy["images"]:
            # Convert images to string descriptions
            img_descs = []
            for img in msg_copy["images"]:
                if hasattr(img, "format") and hasattr(img, "size"):
                    img_descs.append(f"Image: {img.format} {img.size}")
                else:
                    img_descs.append(str(img))
            msg_copy["images"] = img_descs
        serializable_messages.append(msg_copy)
    return json.dumps(serializable_messages)

def build_conversation_history(messages: List[Dict[str, Any]], max_messages: int = None, max_chars: int = None, exclude_last: bool = True) -> List[Dict[str, Any]]:
    """Builds conversation history with truncation and summarization."""
    msgs = messages.copy()
    if exclude_last and msgs:
        msgs = msgs[:-1]

    if max_messages and len(msgs) > max_messages:
        recent = msgs[-max_messages:]
        summary_msg = {"role": "system", "content": "[Earlier conversation summary]"}
        return [summary_msg] + recent

    return msgs

def retry_with_backoff(retries: int = 3, backoff_in_seconds: float = 1.0):
    return retry(stop=stop_after_attempt(retries + 1), wait=wait_fixed(backoff_in_seconds), reraise=True)

def create_openai_messages(history: List[Dict[str, Any]], prompt: str, system_instruction: str = None) -> List[Dict[str, Any]]:
    msgs = []
    if system_instruction:
        msgs.append({"role": "system", "content": system_instruction})

    for h in history:
        msgs.append({"role": h.get("role", "user"), "content": h.get("content", "")})

    msgs.append({"role": "user", "content": prompt})
    return msgs

def augment_prompt_with_search(prompt: str, search_results: List[Dict[str, Any]]) -> str:
    if not search_results:
        return prompt

    context = ui.internet_search.create_search_context(search_results)
    if not context:
         lines = []
         for r in search_results:
             body = r.get('body', '')
             if body:
                 lines.append(body)
         context = "\n".join(lines)

    return f"{prompt}\n\n[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]\n{context}"


def prepare_brain_configuration(api_keys: Dict[str, str]) -> List[Dict[str, Any]]:
    configs = []
    if "google" in api_keys:
        configs.append({"provider": "google"})
    if "openai" in api_keys:
        configs.append({"provider": "openai"})
    return configs

def handle_google_provider(*args, **kwargs):
    return "Simulated Google Response"

def handle_openai_compatible_provider(*args, **kwargs):
    return "Simulated OpenAI Response"

def handle_anthropic_provider(*args, **kwargs):
    return "Simulated Anthropic Response"

def get_openai_client(*args, **kwargs):
    pass

def generate_standard_response(provider: str, model_name: str, api_keys: Dict[str, str], prompt: str, chat_history: List[Dict[str, Any]], config: Dict[str, Any] = None) -> str:
    if provider not in api_keys:
        return "Error: Missing API Key"

    if provider == "google":
        return handle_google_provider()
    elif provider == "openai":
        get_openai_client()
        return handle_openai_compatible_provider()
    elif provider == "anthropic":
        return handle_anthropic_provider()

    return "Error: Unknown provider"

def get_internet_search_engine():
    return None

def perform_internet_search(query: str, enable_search: bool):
    if not enable_search:
        return [], ""

    engine = get_internet_search_engine()
    if engine:
        results = engine.search(query)
        context = ""
        for r in results:
             context += r.get("body", "")
        return results, context
    return [], ""

def export_chat_to_json(messages: List[Dict[str, Any]]) -> str:
    """Exports chat history to a JSON string."""
    return serialize_messages(messages)

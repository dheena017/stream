import logging
import json
from ui.resilience import retry_with_backoff, track_failure

# Helper functions
def build_conversation_history(messages, exclude_last=True, max_messages=None, max_chars=None):
    history = list(messages)
    if exclude_last and history:
        history.pop()

    if max_messages and len(history) > max_messages:
        # Keep system message if first
        system_msg = None
        if history and history[0].get("role") == "system":
            system_msg = history.pop(0)

        # Summarize older messages (placeholder logic)
        summary = {"role": "system", "content": f"[Earlier conversation summary]"}

        # Keep last N
        history = history[-max_messages:]

        history.insert(0, summary)
        if system_msg:
             history.insert(0, system_msg)

    return history

def augment_prompt_with_search(prompt, search_results):
    if not search_results:
        return prompt

    context = "\n".join([f"- {r.get('title', 'Unknown')}: {r.get('body', '')}" for r in search_results])
    return f"{prompt}\n\n[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]\n{context}"

def perform_internet_search(query, enable_search=True):
    if not enable_search:
        return [], ""
    # Stub
    return [], ""

def create_openai_messages(history, prompt, system_instruction=None):
    msgs = []
    if system_instruction:
        msgs.append({"role": "system", "content": system_instruction})
    msgs.extend(history)
    msgs.append({"role": "user", "content": prompt})
    return msgs

def prepare_brain_configuration(api_keys):
    configs = []
    if api_keys.get("google"):
        configs.append({"provider": "google", "model": "gemini-pro"})
    if api_keys.get("openai"):
        configs.append({"provider": "openai", "model": "gpt-3.5-turbo"})
    return configs

def serialize_messages(messages):
    clean_messages = []
    for m in messages:
        cm = m.copy()
        if "images" in cm:
            cm["images"] = [f"Image: {img}" for img in cm["images"]]
        clean_messages.append(cm)
    return json.dumps(clean_messages)

# Provider Handlers

@retry_with_backoff(retries=3, backoff_in_seconds=1)
def handle_google_provider(model_name, api_key, prompt, chat_history, config):
    # Stub
    if not api_key:
        raise Exception("Invalid API Key")
    return f"Response from Google {model_name}: {prompt[::-1]}"

@retry_with_backoff(retries=3, backoff_in_seconds=1)
def handle_openai_compatible_provider(model_name, api_key, prompt, chat_history, config):
    # Stub
    if not api_key:
        raise Exception("Invalid API Key")
    return f"Response from OpenAI {model_name}: {prompt[::-1]}"

@retry_with_backoff(retries=3, backoff_in_seconds=1)
def handle_anthropic_provider(model_name, api_key, prompt, chat_history, config):
    # Stub
    if not api_key:
        raise Exception("Invalid API Key")
    return f"Response from Anthropic {model_name}: {prompt[::-1]}"

# Main generation function
def generate_standard_response(provider, model_name, api_keys, prompt, chat_history, config):
    try:
        api_key = api_keys.get(provider)
        if not api_key:
             return "Error: Missing API Key for " + provider

        if provider == "google":
            return handle_google_provider(model_name, api_key, prompt, chat_history, config)
        elif provider == "openai":
            return handle_openai_compatible_provider(model_name, api_key, prompt, chat_history, config)
        elif provider == "anthropic":
            return handle_anthropic_provider(model_name, api_key, prompt, chat_history, config)
        else:
            return f"Error: Unknown provider {provider}"

    except Exception as e:
        track_failure(provider, str(e))
        return f"Error: {str(e)}"

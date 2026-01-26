import time
import functools

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Simple pass-through for mock
            return func(*args, **kwargs)
        return wrapper
    return decorator

def build_conversation_history(messages, max_messages=10, exclude_last=True):
    # Mock implementation
    history = messages[:-1] if exclude_last and messages else messages
    if len(history) > max_messages:
        return [{"role": "system", "content": "[Earlier conversation summary]"}] + history[-max_messages:]
    return history

def generate_standard_response(prompt, chat_history, provider="openai", **kwargs):
    # Mock response with delay
    time.sleep(1.5) # Simulate network delay for spinner testing
    return f"I am a mock assistant. You said: '{prompt}'. This is a simulated response to verify the UI."

def augment_prompt_with_search(prompt, results):
    if not results:
        return prompt
    return f"{prompt}\n[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]"

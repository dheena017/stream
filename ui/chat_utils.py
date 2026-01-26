import time
import random
from tenacity import retry, stop_after_attempt, wait_exponential
import ui.analytics as analytics

# Resilience: Retry decorator
def retry_with_backoff(func):
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )(func)

@retry_with_backoff
def simulate_provider_call(provider: str, model: str, prompt: str):
    """Simulates an API call to a provider."""
    start_time = time.time()
    try:
        # Simulate network latency
        time.sleep(random.uniform(0.1, 0.5))

        # Simulate occasional failure for testing resilience
        if random.random() < 0.1:
            raise ConnectionError("Simulated connection failure")

        duration = time.time() - start_time
        analytics.log_api_call(
            provider=provider,
            model=model,
            duration=duration,
            success=True,
            input_tokens=len(prompt.split()),
            output_tokens=20 # Mock output tokens
        )
        return f"Response from {provider} using {model}: This is a simulated response to '{prompt[:20]}...'."

    except Exception as e:
        duration = time.time() - start_time
        analytics.log_api_call(
            provider=provider,
            model=model,
            duration=duration,
            success=False,
            error=str(e)
        )
        analytics.log_error(f"chat_utils.simulate_provider_call", str(e), e)
        raise e

def generate_response(provider: str, model: str, messages: list):
    """
    Generates a response from the specified provider.
    Handles errors and returns a string starting with 'Error:' on failure.
    """
    try:
        prompt = messages[-1]['content'] if messages else ""
        # In a real app, we would parse messages to string.
        # Here we just take the last message content.
        response = simulate_provider_call(provider, model, prompt)
        return response
    except Exception as e:
        # Standardizing provider errors to string returns starting with 'Error:'
        return f"Error: Failed to generate response from {provider}. {str(e)}"

def preload_blip_model_with_progress():
    """
    Simulates loading a heavy model, checking for dependencies.
    """
    try:
        import torch
        import transformers
        # Simulate loading
        time.sleep(0.5)
        analytics.log_system_event("blip_model_loaded")
        return True
    except ImportError:
        analytics.log_system_event("blip_model_load_skipped", {"reason": "dependencies_missing"})
        return False

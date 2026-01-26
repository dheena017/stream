import time
import functools
import logging
import random
import asyncio

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
                    sleep_time = (backoff_in_seconds * (2 ** x)) + random.uniform(0, 0.1)
                    logging.warning(f"Error in {func.__name__}: {e}. Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                    x += 1
        return wrapper
    return decorator

def async_retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep_time = (backoff_in_seconds * (2 ** x)) + random.uniform(0, 0.1)
                    logging.warning(f"Error in {func.__name__}: {e}. Retrying in {sleep_time:.2f}s...")
                    await asyncio.sleep(sleep_time)
                    x += 1
        return wrapper
    return decorator

def track_failure(source, error):
    try:
        import streamlit as st
        if hasattr(st, "session_state"):
            if "failure_metrics" not in st.session_state:
                st.session_state.failure_metrics = {}

            current = st.session_state.failure_metrics.get(source, 0)
            st.session_state.failure_metrics[source] = current + 1
    except ImportError:
        pass
    except Exception:
        pass

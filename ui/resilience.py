import time
import functools
import logging
import asyncio
import streamlit as st
from typing import Optional, Callable

logger = logging.getLogger(__name__)

def retry_with_backoff(retries: int = 3, backoff_in_seconds: float = 1):
    """
    Decorator to retry a function with exponential backoff.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(f"Function {func.__name__} failed after {retries} retries. Error: {e}")
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    logger.warning(f"Function {func.__name__} failed: {e}. Retrying in {sleep}s...")
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

def async_retry_with_backoff(retries: int = 3, backoff_in_seconds: float = 1):
    """
    Decorator to retry an async function with exponential backoff.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(f"Async function {func.__name__} failed after {retries} retries. Error: {e}")
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    logger.warning(f"Async function {func.__name__} failed: {e}. Retrying in {sleep}s...")
                    await asyncio.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

def track_failure(source: str, error: Exception):
    """
    Log failure and update session state metrics if available.
    """
    error_msg = str(error)
    log_msg = f"[FAILURE_METRIC] Source: {source} | Error: {error_msg}"
    logger.error(log_msg)

    # Update Streamlit session state if available
    try:
        if hasattr(st, "session_state"):
            if "failure_metrics" not in st.session_state:
                st.session_state.failure_metrics = {}

            metrics = st.session_state.failure_metrics
            current_count = metrics.get(source, 0)
            metrics[source] = current_count + 1
            st.session_state.failure_metrics = metrics
    except Exception as e:
        logger.warning(f"Failed to update session state metrics: {e}")

def log_error(context: str, error: Exception):
    """
    Standardized error logging helper.
    """
    logger.error(f"Error in {context}: {str(error)}")

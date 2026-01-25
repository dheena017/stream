import pytest
import time
import os
from pathlib import Path
from ui.analytics import init_analytics, log_api_call, log_error, get_recent_errors, get_analytics_summary, LOG_FILE

def test_analytics_logging():
    # Setup
    if LOG_FILE.exists():
        os.remove(LOG_FILE)
    init_analytics()
    print(f"DEBUG: Initialized. File: {LOG_FILE}, Abs: {LOG_FILE.absolute()}, Exists: {LOG_FILE.exists()}")

    # Test log_api_call
    log_api_call("test_provider", "test_model", 0.5, True)
    print(f"DEBUG: Logged. Exists: {LOG_FILE.exists()}")
    log_api_call("test_provider", "test_model_fail", 0.1, False, "Error message")

    # Test log_error
    try:
        raise ValueError("Test Exception")
    except Exception as e:
        log_error("test_context", e)

    # Allow some time for IO
    time.sleep(0.1)

    assert LOG_FILE.exists()

    # Test parsing
    summary = get_analytics_summary()
    assert summary["api_calls"] == 2
    assert summary["successful_calls"] == 1
    assert summary["failed_calls"] == 1

    errors = get_recent_errors(10)
    # Should have 2 errors: 1 from failed api call, 1 from log_error
    assert len(errors) == 2

    # Verify content
    # Recent errors returns reversed list
    assert errors[0]["context"] == "test_context" # The exception
    assert errors[1]["error_details"] == "Error message" or errors[1]["message"].endswith("(Failed)")

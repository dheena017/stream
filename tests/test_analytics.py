import os
import json
import pytest
import ui.chat_utils as chat_utils
import ui.analytics as analytics

LOG_FILE = "logs/app.log"

def test_analytics_logging():
    # Configure logging
    analytics.configure_logging()

    # Record initial state
    initial_lines = 0
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            initial_lines = len(f.readlines())

    from loguru import logger
    # Simulate a call
    messages = [{"role": "user", "content": "Hello test"}]
    response = chat_utils.generate_response("test_provider", "test_model", messages)

    # Wait for logs to be written
    logger.complete()

    # Verify response structure
    assert "Response from test_provider" in response or "Error:" in response

    # Check logs
    assert os.path.exists(LOG_FILE)

    found_event = False
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
        # Check new lines
        for line in lines[initial_lines:]:
            try:
                log_entry = json.loads(line)
                extra = log_entry.get("record", {}).get("extra", {})
                if extra.get("event_type") == "api_call":
                    if extra.get("provider") == "test_provider":
                        found_event = True
                        assert extra.get("model") == "test_model"
                        assert "duration" in extra
                        assert "success" in extra
                        # Check tokens
                        assert "input_tokens" in extra
                        assert "output_tokens" in extra
            except json.JSONDecodeError:
                continue

    assert found_event, "API call log entry not found in logs/app.log"

if __name__ == "__main__":
    try:
        test_analytics_logging()
        print("Test passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"Test error: {e}")
        exit(1)

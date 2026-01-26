import pytest
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import asyncio
import streamlit as st

# Ensure we can import from ui
sys.path.append(os.getcwd())

from ui.resilience import retry_with_backoff, async_retry_with_backoff, track_failure
from ui.chat_utils import generate_standard_response

# Mocking streamlit session state
if not hasattr(st, "session_state"):
    st.session_state = MagicMock()

class TestResilience(unittest.TestCase):
    # This class uses unittest style from HEAD

    @patch('ui.chat_utils.handle_openai_compatible_provider')
    def test_provider_error_handling(self, mock_handle):
        """Test that generate_standard_response returns an error string on failure."""
        mock_handle.side_effect = Exception("Critical Failure")

        api_keys = {"openai": "test-key"}
        response = generate_standard_response(
            provider="openai",
            model_name="gpt-4",
            api_keys=api_keys,
            prompt="Hello",
            chat_history=[],
            config={}
        )

        self.assertTrue(response.startswith("Error:"), f"Got: {response}")
        self.assertIn("Critical Failure", response)

# The following functions use pytest style from origin

def test_retry_with_backoff_success():
    mock_func = MagicMock(return_value="success")

    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def decorated_func():
        return mock_func()

    result = decorated_func()
    assert result == "success"
    assert mock_func.call_count == 1

def test_retry_with_backoff_fail_then_success():
    mock_func = MagicMock(side_effect=[ValueError("Fail 1"), "success"])

    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def decorated_func():
        return mock_func()

    result = decorated_func()
    assert result == "success"
    assert mock_func.call_count == 2

def test_retry_with_backoff_all_fail():
    mock_func = MagicMock(side_effect=[ValueError("Fail 1"), ValueError("Fail 2"), ValueError("Fail 3")])

    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def decorated_func():
        return mock_func()

    with pytest.raises(ValueError):
        decorated_func()

    assert mock_func.call_count == 3  # Initial + 2 retries

@pytest.mark.asyncio
async def test_async_retry_with_backoff_success():
    mock_func = MagicMock(return_value="success")

    @async_retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    async def decorated_func():
        return mock_func()

    result = await decorated_func()
    assert result == "success"
    assert mock_func.call_count == 1

@pytest.mark.asyncio
async def test_async_retry_with_backoff_fail_then_success():
    mock_func = MagicMock(side_effect=[ValueError("Fail 1"), "success"])

    @async_retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    async def decorated_func():
        return mock_func()

    result = await decorated_func()
    assert result == "success"
    assert mock_func.call_count == 2

@pytest.mark.asyncio
async def test_async_retry_with_backoff_all_fail():
    mock_func = MagicMock(side_effect=[ValueError("Fail 1"), ValueError("Fail 2"), ValueError("Fail 3")])

    @async_retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    async def decorated_func():
        return mock_func()

    with pytest.raises(ValueError):
        await decorated_func()

    assert mock_func.call_count == 3

def test_track_failure_updates_session_state():
    # Setup mock session state
    class MockSessionState(dict):
        def __getattr__(self, key):
            return self.get(key)
        def __setattr__(self, key, value):
            self[key] = value

    st.session_state = MockSessionState()

    track_failure("Test Source", ValueError("Test Error"))

    assert "failure_metrics" in st.session_state
    assert st.session_state.failure_metrics["Test Source"] == 1

    track_failure("Test Source", ValueError("Another Error"))
    assert st.session_state.failure_metrics["Test Source"] == 2

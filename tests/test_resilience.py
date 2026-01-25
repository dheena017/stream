<<<<<<< HEAD
import unittest
from unittest.mock import MagicMock, patch
import logging
import sys
import os

# Ensure we can import from ui
sys.path.append(os.getcwd())

from ui.chat_utils import retry_with_backoff, generate_standard_response

class TestResilience(unittest.TestCase):

    def test_retry_logic(self):
        """Test that retry_with_backoff retries and eventually succeeds."""
        mock_func = MagicMock()
        mock_func.side_effect = [Exception("Fail 1"), Exception("Fail 2"), "Success"]

        @retry_with_backoff(retries=3, backoff_in_seconds=0.01)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        self.assertEqual(result, "Success")
        self.assertEqual(mock_func.call_count, 3)

    def test_retry_logic_failure(self):
        """Test that retry_with_backoff raises exception after max retries."""
        mock_func = MagicMock()
        mock_func.side_effect = Exception("Persistent Fail")

        @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
        def decorated_func():
            return mock_func()

        with self.assertRaises(Exception):
            decorated_func()

        # Initial call + 2 retries = 3 calls
        self.assertEqual(mock_func.call_count, 3)

    @patch('ui.chat_utils.handle_openai_compatible_provider')
    @patch('ui.chat_utils.get_openai_client')
    def test_provider_error_handling(self, mock_get_client, mock_handle):
        """Test that generate_standard_response returns an error string on failure."""

        # Mocking so that the call inside generate_standard_response raises an exception
        # generate_standard_response calls handle_openai_compatible_provider for "openai"

        # We simulate the provider handler failing (which might happen if retries are exhausted inside it)
        # Note: In the current code, handle_openai_compatible_provider returns a string on error,
        # but generate_standard_response also has a try/except.
        # If handle_openai_compatible_provider raises an exception, generate_standard_response should catch it.
        # Wait, handle_openai_compatible_provider in current code CATCHES exceptions and returns string.
        # So generate_standard_response will receive that string.
        # But if we mock it to RAISE, we test generate_standard_response's outer try/except.

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

        # Expecting "Generation Error: Critical Failure" based on current code
        self.assertTrue(response.startswith("Generation Error:") or response.startswith("Error:"), f"Got: {response}")
        self.assertIn("Critical Failure", response)
=======
import pytest
import time
import asyncio
from unittest.mock import MagicMock, patch
import streamlit as st
from ui.resilience import retry_with_backoff, async_retry_with_backoff, track_failure

# Mocking streamlit session state
if not hasattr(st, "session_state"):
    st.session_state = MagicMock()

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
    st.session_state = MagicMock()
    # We need to simulate that 'failure_metrics' is not in session_state initially,
    # but MagicMock usually returns another MagicMock for any attribute.
    # So we'll use a real dict wrapped in a simple object or just rely on MagicMock behavior
    # simpler to just mock the dict behavior manually if we want to test logic.

    # Let's use a real dict for session_state to be safe
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
>>>>>>> origin/resilience-error-handling-7924837681139551131

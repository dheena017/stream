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

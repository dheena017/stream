import sys
import pytest
from unittest.mock import MagicMock, patch

# Custom SessionState to support attribute access
class SessionState(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'SessionState' object has no attribute '{item}'")
    def __setattr__(self, key, value):
        self[key] = value

# -------------------------------------------------------------------------
# SETUP: Mock modules BEFORE importing app.py
# -------------------------------------------------------------------------

# 1. Mock Streamlit
mock_st = MagicMock()
def mock_cache_resource(*args, **kwargs):
    if len(args) == 1 and callable(args[0]):
        return args[0]
    def decorator(func):
        return func
    return decorator
mock_st.cache_resource = mock_cache_resource
mock_st.session_state = SessionState()
sys.modules["streamlit"] = mock_st

# 2. Mock ui.database
mock_db = MagicMock()
sys.modules["ui.database"] = mock_db

# 3. Mock other UI modules
sys.modules["ui.styles"] = MagicMock()
sys.modules["ui.auth"] = MagicMock()
sys.modules["ui.profile"] = MagicMock()
sys.modules["ui.dashboard"] = MagicMock()
sys.modules["ui.sidebar"] = MagicMock()
sys.modules["ui.chat"] = MagicMock()
sys.modules["ui.prefs"] = MagicMock()
sys.modules["brain_learning"] = MagicMock()
sys.modules["multimodal_voice_integration"] = MagicMock()

import app

# -------------------------------------------------------------------------
# TESTS
# -------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_state():
    # Reset session state
    mock_st.session_state.clear()

    # Reset mocks
    mock_st.stop.reset_mock()
    app.show_login_page.reset_mock()
    app.show_dashboard.reset_mock()
    app.show_profile_page.reset_mock()
    app.show_chat_page.reset_mock()

    yield

    mock_st.session_state.clear()

def test_initialize_auth_state():
    app.initialize_auth_state()
    assert "authenticated" in mock_st.session_state
    assert mock_st.session_state.authenticated is False
    assert mock_st.session_state.username is None
    assert mock_st.session_state.current_page == "dashboard"

    # Check idempotency
    mock_st.session_state.authenticated = True
    app.initialize_auth_state()
    assert mock_st.session_state.authenticated is True

def test_initialize_chat_state():
    app.initialize_chat_state()
    assert mock_st.session_state.messages == []
    assert mock_st.session_state.voice_mode is False
    assert mock_st.session_state.enable_internet_search is False
    assert mock_st.session_state.search_result_count == 5

def test_initialize_session_tracking():
    app.initialize_session_tracking()
    assert "session_start_time" in mock_st.session_state
    assert "total_sessions" in mock_st.session_state
    assert "user_joined_date" in mock_st.session_state

def test_handle_authentication_not_authenticated():
    mock_st.session_state.authenticated = False

    app.handle_authentication()

    app.show_login_page.assert_called_once()
    mock_st.stop.assert_called_once()

def test_handle_authentication_authenticated():
    mock_st.session_state.authenticated = True
    app.handle_authentication()

    app.show_login_page.assert_not_called()
    mock_st.stop.assert_not_called()

def test_handle_page_routing_dashboard():
    mock_st.session_state.current_page = "dashboard"
    app.handle_page_routing()
    app.show_dashboard.assert_called_once()

def test_handle_page_routing_profile():
    mock_st.session_state.current_page = "profile"
    app.handle_page_routing()
    app.show_profile_page.assert_called_once()

def test_handle_page_routing_default():
    mock_st.session_state.current_page = "unknown"
    app.handle_page_routing()
    app.show_chat_page.assert_called_once()

import pytest
from unittest.mock import MagicMock, patch
import app

class SessionState(dict):
    """Mock Streamlit SessionState which supports attribute access."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

def test_initialize_auth_state():
    # Patch st in the app module
    with patch.object(app, 'st') as mock_st:
        # Setup mock session state
        mock_st.session_state = SessionState()

        # Call the function
        app.initialize_auth_state()

        # Verify state
        assert "authenticated" in mock_st.session_state
        assert mock_st.session_state.authenticated is False
        assert mock_st.session_state.username is None
        assert mock_st.session_state.current_page == "dashboard"

        # Test that it doesn't overwrite existing state
        mock_st.session_state.authenticated = True
        app.initialize_auth_state()
        assert mock_st.session_state.authenticated is True

def test_initialize_chat_state():
    # Patch st in the app module
    with patch.object(app, 'st') as mock_st:
        # Setup mock session state
        mock_st.session_state = SessionState()

        # Call the function
        app.initialize_chat_state()

        # Verify state
        assert "messages" in mock_st.session_state
        assert mock_st.session_state.messages == []
        assert mock_st.session_state.voice_mode is False
        assert mock_st.session_state.enable_internet_search is False
        assert mock_st.session_state.search_result_count == 5

        # Test persistence
        mock_st.session_state.voice_mode = True
        app.initialize_chat_state()
        assert mock_st.session_state.voice_mode is True

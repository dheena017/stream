import sys
import os
import pytest
from unittest.mock import MagicMock

# Ensure the root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_streamlit_module():
    """
    Mocks the streamlit module in sys.modules.
    This is useful for testing modules that import streamlit at the top level
    and we want to control streamlit's behavior (like session_state).
    """
    # Create the mock
    mock_st = MagicMock()
    mock_st.session_state = {}

    def noop(func=None, **kwargs):
        if func is None:
            return lambda f: f
        return func

    mock_st.cache_resource = noop
    mock_st.cache_data = noop
    mock_st.set_page_config = MagicMock()
    mock_st.markdown = MagicMock()

    # Patch
    with pytest.MonkeyPatch.context() as mp:
        mp.setitem(sys.modules, 'streamlit', mock_st)
        yield mock_st

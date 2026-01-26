
import pytest
from unittest.mock import MagicMock
import sys

# Mock streamlit before import
sys.modules["streamlit"] = MagicMock()
sys.modules["ui.chat_utils"] = MagicMock()

import ui.chat

def test_chat_interface_definition():
    assert hasattr(ui.chat, "chat_interface")
    # We can't easily run it because of the extensive st mocking needed

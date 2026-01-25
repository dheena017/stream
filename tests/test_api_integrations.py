
import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock streamlit
mock_streamlit = MagicMock()
sys.modules['streamlit'] = mock_streamlit

# Pre-mock google.generativeai
mock_genai_module = MagicMock()
sys.modules['google.generativeai'] = mock_genai_module

from ui.chat_utils import handle_google_provider, generate_standard_response

def test_handle_google_provider_configures_genai():
    # Reset mocks
    mock_genai_module.reset_mock()

    # Setup mock behaviors
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Gemini response"

    # When genai.GenerativeModel is called, return mock_model
    mock_genai_module.GenerativeModel.return_value = mock_model
    # When model.generate_content is called, return mock_response
    mock_model.generate_content.return_value = mock_response

    # Call function
    api_key = "fake_key"
    response = handle_google_provider(api_key, "gemini-1.5-flash", "Hello")

    # Assertions
    # Verify configure was called with the api_key
    mock_genai_module.configure.assert_called_with(api_key=api_key)

    # Verify model creation and generation
    mock_genai_module.GenerativeModel.assert_called()
    mock_model.generate_content.assert_called()
    assert response == "Gemini response"

@patch('ui.chat_utils.get_openai_client')
@patch('ui.chat_utils.handle_openai_compatible_provider')
def test_generate_standard_response_groq(mock_handle_provider, mock_get_client):
    # Setup
    api_keys = {"groq": "fake_groq_key"}
    chat_history = []

    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_handle_provider.return_value = "Groq Response"

    # Call
    response = generate_standard_response(
        provider="groq",
        model_name="llama-3.3-70b",
        api_keys=api_keys,
        prompt="Hi",
        chat_history=chat_history
    )

    # Assertions
    # Check if get_openai_client was called with Groq URL
    mock_get_client.assert_called_once_with("fake_groq_key", "https://api.groq.com/openai/v1")
    mock_handle_provider.assert_called_once()
    assert response == "Groq Response"

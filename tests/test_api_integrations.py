
import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock streamlit
mock_streamlit = MagicMock()
sys.modules['streamlit'] = mock_streamlit

# Pre-mock google.generativeai
# Ensure google package is also mocked to support dotted import
mock_google = MagicMock()
sys.modules['google'] = mock_google
mock_genai_module = MagicMock()
mock_google.generativeai = mock_genai_module
sys.modules['google.generativeai'] = mock_genai_module

# Mock openai
mock_openai = MagicMock()
sys.modules['openai'] = mock_openai

from ui.chat_utils import handle_google_provider, generate_standard_response, prepare_brain_configuration

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

    # Call function - Note: handle_google_provider signature might need adjustment based on implementation
    # The test in HEAD called it with (api_key, model, prompt)
    # But generate_standard_response calls it with () in my stub. I need to align them.
    # Assuming the implementation will take arguments.

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
    mock_get_client.assert_called_once_with("fake_groq_key", base_url="https://api.groq.com/openai/v1")
    mock_handle_provider.assert_called_once()
    assert response == "Groq Response"

def test_prepare_brain_configuration_with_groq():
    api_keys = {"groq": "test_key", "openai": "sk-..."}
    models = prepare_brain_configuration(api_keys)

    groq_entries = [m for m in models if m["provider"] == "groq"]
    assert len(groq_entries) == 1
    # Assuming prepare_brain_configuration returns details about models
    assert groq_entries[0]["model"] == "llama-3.3-70b-versatile"

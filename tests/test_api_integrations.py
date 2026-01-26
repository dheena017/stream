import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock streamlit if not present
sys.modules['streamlit'] = MagicMock()

# Pre-mock google.generativeai if needed, but we will patch directly in tests
# sys.modules['google.generativeai'] = MagicMock()

from ui.chat_utils import handle_google_provider, generate_standard_response, prepare_brain_configuration

@patch("ui.chat_utils.genai")
def test_handle_google_provider_configures_genai(mock_genai):
    # Setup mock behaviors
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Gemini response"

    # When genai.GenerativeModel is called, return mock_model
    mock_genai.GenerativeModel.return_value = mock_model
    # When model.generate_content is called, return mock_response
    mock_model.generate_content.return_value = mock_response

    # Call function
    api_key = "fake_key"
    response = handle_google_provider(api_key, "gemini-1.5-flash", "Hello")

    # Assertions
    # Verify configure was called with the api_key
    mock_genai.configure.assert_called_with(api_key=api_key)

    # Verify model creation and generation
    mock_genai.GenerativeModel.assert_called()
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
    # Check if handle_openai_compatible_provider was called with Groq URL
    mock_handle_provider.assert_called_once()
    args, kwargs = mock_handle_provider.call_args
    assert kwargs.get('base_url') == "https://api.groq.com/openai/v1"
    assert response == "Groq Response"

def test_prepare_brain_configuration_with_groq():
    api_keys = {"groq": "test_key", "openai": "sk-..."}
    models = prepare_brain_configuration(api_keys)

    groq_entries = [m for m in models if m["provider"] == "groq"]
    assert len(groq_entries) == 1
    assert groq_entries[0]["model"] == "llama-3.3-70b-versatile"

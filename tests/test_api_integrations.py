
import pytest
from unittest.mock import MagicMock, patch
<<<<<<< HEAD
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
=======
from ui.chat_utils import generate_standard_response, prepare_brain_configuration

@patch("ui.chat_utils.get_openai_client")
def test_groq_integration(mock_get_client):
    # Setup mock
    mock_client_instance = MagicMock()
    mock_get_client.return_value = mock_client_instance
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="Groq response"))]
    mock_client_instance.chat.completions.create.return_value = mock_completion

    api_keys = {"groq": "test_key"}
    chat_history = []

    # Test generation
    response = generate_standard_response(
        provider="groq",
        model_name="llama-3.3-70b-versatile",
        api_keys=api_keys,
        prompt="Hello",
        chat_history=chat_history,
        config={"temperature": 0.5}
    )

    # Verify response
    assert response == "Groq response"

    # Verify client was initialized with correct base_url
    mock_get_client.assert_called_with("test_key", "https://api.groq.com/openai/v1")

    # Verify completion call
    mock_client_instance.chat.completions.create.assert_called_once()
    call_kwargs = mock_client_instance.chat.completions.create.call_args[1]
    assert call_kwargs["model"] == "llama-3.3-70b-versatile"
    assert call_kwargs["temperature"] == 0.5

def test_prepare_brain_configuration_with_groq():
    api_keys = {"groq": "test_key", "openai": "sk-..."}
    models = prepare_brain_configuration(api_keys)

    groq_entries = [m for m in models if m["provider"] == "groq"]
    assert len(groq_entries) == 1
    assert groq_entries[0]["model"] == "llama-3.3-70b-versatile"
>>>>>>> origin/api-integrations-groq-12473300930587894354

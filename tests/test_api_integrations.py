from unittest.mock import MagicMock, patch


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
        config={"temperature": 0.5},
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

import pytest
from unittest.mock import MagicMock
from ui.chat_utils import (
    build_conversation_history,
    create_openai_messages,
    prepare_brain_configuration,
    generate_standard_response
)

def test_build_conversation_history_basic():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        {"role": "user", "content": "How are you?"}
    ]
    # exclude_last=True by default
    history = build_conversation_history(messages)
    assert len(history) == 2
    assert history[-1]["content"] == "Hi"

def test_build_conversation_history_limit():
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(30)]
    history = build_conversation_history(messages, exclude_last=False, max_messages=5)

    assert len(history) == 6 # 5 recent + 1 summary
    assert history[0]["role"] == "system"
    assert "[Earlier conversation summary]" in history[0]["content"]

def test_create_openai_messages():
    history = [{"role": "user", "content": "prev"}]
    prompt = "current"
    system = "sys"

    msgs = create_openai_messages(history, prompt, system)

    assert len(msgs) == 3
    assert msgs[0]["role"] == "system"
    assert msgs[0]["content"] == "sys"
    assert msgs[1]["role"] == "user"
    assert msgs[1]["content"] == "prev"
    assert msgs[2]["role"] == "user"
    assert msgs[2]["content"] == "current"

def test_prepare_brain_configuration():
    api_keys = {"google": "key1", "openai": "key2"}
    configs = prepare_brain_configuration(api_keys)

    providers = [c["provider"] for c in configs]
    assert "google" in providers
    assert "openai" in providers
    assert "anthropic" not in providers

def test_generate_standard_response_missing_key(mocker):
    # Should return error message if key is missing
    response = generate_standard_response(
        provider="google",
        model_name="gemini",
        api_keys={},
        prompt="test",
        chat_history=[]
    )
    assert "Missing API Key" in response

def test_generate_standard_response_google(mocker):
    # Mock handle_google_provider
    mock_handle = mocker.patch("ui.chat_utils.handle_google_provider", return_value="Google Response")

    response = generate_standard_response(
        provider="google",
        model_name="gemini",
        api_keys={"google": "key"},
        prompt="test",
        chat_history=[]
    )

    assert response == "Google Response"
    mock_handle.assert_called_once()

def test_generate_standard_response_openai(mocker):
    # Mock get_openai_client and handle_openai_compatible_provider
    mocker.patch("ui.chat_utils.get_openai_client")
    mock_handle = mocker.patch("ui.chat_utils.handle_openai_compatible_provider", return_value="OpenAI Response")

    response = generate_standard_response(
        provider="openai",
        model_name="gpt-4",
        api_keys={"openai": "key"},
        prompt="test",
        chat_history=[]
    )

    assert response == "OpenAI Response"
    mock_handle.assert_called_once()

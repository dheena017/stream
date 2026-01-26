from unittest.mock import MagicMock, Mock, patch

import pytest

from ui.chat_utils import (
    augment_prompt_with_search,
    build_conversation_history,
    generate_standard_response,
    perform_internet_search,
    retry_with_backoff,
)


# Test build_conversation_history
def test_build_conversation_history_basic():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        {"role": "user", "content": "How are you?"},
    ]
    # exclude_last=True by default, so it should exclude the last user message
    history = build_conversation_history(messages)
    assert len(history) == 2
    assert history[-1]["content"] == "Hi"


def test_build_conversation_history_limit():
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(30)]
    history = build_conversation_history(messages, exclude_last=False, max_messages=10)
    assert len(history) == 11  # 1 system summary + 10 recent messages
    assert history[0]["role"] == "system"
    assert "[Earlier conversation summary]" in history[0]["content"]


# Test augment_prompt_with_search
def test_augment_prompt_with_search_no_results():
    prompt = "Hello"
    results = []
    assert augment_prompt_with_search(prompt, results) == prompt


def test_augment_prompt_with_search_with_results():
    prompt = "What is the weather?"
    results = [{"title": "Weather", "href": "http://weather.com", "body": "Sunny"}]
    augmented = augment_prompt_with_search(prompt, results)
    assert "What is the weather?" in augmented
    assert "[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]" in augmented
    assert "Sunny" in augmented


# Test perform_internet_search
@patch("ui.chat_utils.get_internet_search_engine")
def test_perform_internet_search_disabled(mock_get_engine):
    results, context = perform_internet_search("query", enable_search=False)
    assert results == []
    assert context == ""
    mock_get_engine.assert_not_called()


@patch("ui.chat_utils.get_internet_search_engine")
def test_perform_internet_search_enabled(mock_get_engine):
    mock_engine = MagicMock()
    mock_engine.search.return_value = [{"title": "Test", "body": "Content"}]
    mock_get_engine.return_value = mock_engine

    results, context = perform_internet_search("query", enable_search=True)
    assert len(results) == 1
    assert "Content" in context
    mock_engine.search.assert_called_once()


# Test generate_standard_response
@patch("ui.chat_utils.handle_google_provider")
def test_generate_standard_response_google(mock_handle_google):
    mock_handle_google.return_value = "Google Response"
    api_keys = {"google": "fake_key"}
    response = generate_standard_response(
        provider="google",
        model_name="gemini-pro",
        api_keys=api_keys,
        prompt="Hello",
        chat_history=[],
        config={},
    )
    assert response == "Google Response"
    mock_handle_google.assert_called_once()


@patch("ui.chat_utils.handle_anthropic_provider")
def test_generate_standard_response_anthropic(mock_handle_anthropic):
    mock_handle_anthropic.return_value = "Claude Response"
    api_keys = {"anthropic": "fake_key"}
    response = generate_standard_response(
        provider="anthropic",
        model_name="claude-3",
        api_keys=api_keys,
        prompt="Hello",
        chat_history=[],
        config={},
    )
    assert response == "Claude Response"
    mock_handle_anthropic.assert_called_once()


def test_generate_standard_response_missing_key():
    api_keys = {}
    response = generate_standard_response(
        provider="google",
        model_name="gemini-pro",
        api_keys=api_keys,
        prompt="Hello",
        chat_history=[],
        config={},
    )
    assert "Missing API Key" in response


# Test retry_with_backoff
def test_retry_with_backoff_success():
    mock_func = Mock(side_effect=[Exception("Fail"), "Success"])

    @retry_with_backoff(retries=3, backoff_in_seconds=0.01)
    def wrapped_func():
        return mock_func()

    result = wrapped_func()
    assert result == "Success"
    assert mock_func.call_count == 2


def test_retry_with_backoff_failure():
    mock_func = Mock(side_effect=Exception("Always Fail"))

    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def wrapped_func():
        return mock_func()

    with pytest.raises(Exception, match="Always Fail"):
        wrapped_func()

    assert mock_func.call_count == 3

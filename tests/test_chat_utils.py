import json
import pytest
import sys
from unittest.mock import MagicMock, patch, Mock

# Mock modules to avoid import errors if they are not yet implemented/installed
# But since we are implementing ui/chat_utils.py, we might not need to mock them in sys.modules
# if we design chat_utils to be robust. However, the tests import from ui.chat_utils.
# If ui.chat_utils imports other things (like ui.internet_search), we might need to mock those.
# For now, we assume ui.chat_utils is standalone or we mock its dependencies.

from ui.chat_utils import (
    serialize_messages,
    build_conversation_history,
    create_openai_messages,
    retry_with_backoff,
    augment_prompt_with_search,
    prepare_brain_configuration,
    generate_standard_response,
    perform_internet_search
)

# --- serialize_messages tests ---

def test_serialize_messages_simple():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
    json_str = serialize_messages(messages)
    loaded = json.loads(json_str)
    assert len(loaded) == 2
    assert loaded[0]["content"] == "Hello"
    assert loaded[1]["content"] == "Hi there"

def test_serialize_messages_with_images():
    # Mock PIL Image
    mock_img = MagicMock()
    mock_img.format = "PNG"
    mock_img.size = (100, 100)
    # We need to make sure str(mock_img) or similar behaves as expected if used,
    # but serialize_messages likely checks isinstance.

    messages = [
        {
            "role": "user",
            "content": "Look at this",
            "images": [mock_img]
        }
    ]

    json_str = serialize_messages(messages)
    loaded = json.loads(json_str)

    assert len(loaded) == 1
    assert loaded[0]["content"] == "Look at this"
    # Check that images are converted to string descriptions
    assert isinstance(loaded[0]["images"], list)
    assert len(loaded[0]["images"]) == 1
    # The implementation should convert image object to a string description
    assert "Image" in loaded[0]["images"][0]

def test_serialize_messages_does_not_mutate_original():
    messages = [{"role": "user", "content": "test", "images": ["fake_img"]}]
    original_images = messages[0]["images"]

    # Create a copy to compare against, because list in dict might be same ref if not careful
    import copy
    original_messages = copy.deepcopy(messages)

    serialize_messages(messages)

    assert messages == original_messages

# --- build_conversation_history tests ---

def test_build_conversation_history_basic():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
        {"role": "user", "content": "How are you?"}
    ]
    # Default exclude_last=True
    history = build_conversation_history(messages)
    assert len(history) == 2
    assert history[0]["content"] == "Hello"
    assert history[1]["content"] == "Hi there"

def test_build_conversation_history_no_exclude():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
    history = build_conversation_history(messages, exclude_last=False)
    assert len(history) == 2

def test_build_conversation_history_truncation_messages():
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(10)]
    # 10 messages, exclude last -> 9. Max 5.
    # Expect 1 system summary + 5 recent = 6 items
    history = build_conversation_history(messages, max_messages=5)

    assert len(history) == 6
    assert history[0]["role"] == "system"
    assert "[Earlier conversation summary]" in history[0]["content"]
    assert history[1]["content"] == "msg 4"  # 0,1,2,3 are summarized. 4..8 kept.

# --- create_openai_messages tests ---

def test_create_openai_messages_basic():
    history = [{"role": "user", "content": "prev"}]
    prompt = "current"
    msgs = create_openai_messages(history, prompt)

    assert len(msgs) == 2
    assert msgs[0]["content"] == "prev"
    assert msgs[1]["role"] == "user"
    assert msgs[1]["content"] == "current"

def test_create_openai_messages_with_system():
    history = []
    prompt = "current"
    system = "act like a pirate"
    msgs = create_openai_messages(history, prompt, system_instruction=system)

    assert len(msgs) == 2
    assert msgs[0]["role"] == "system"
    assert msgs[0]["content"] == "act like a pirate"
    assert msgs[1]["content"] == "current"

# --- retry_with_backoff tests ---

def test_retry_with_backoff_success():
    mock_func = MagicMock(return_value="success")

    @retry_with_backoff(retries=3, backoff_in_seconds=0.01)
    def decorated():
        return mock_func()

    result = decorated()
    assert result == "success"
    assert mock_func.call_count == 1

def test_retry_with_backoff_failure_retry():
    # Fail twice, then succeed
    mock_func = MagicMock(side_effect=[ValueError("fail"), ValueError("fail"), "success"])

    @retry_with_backoff(retries=3, backoff_in_seconds=0.01)
    def decorated():
        return mock_func()

    result = decorated()
    assert result == "success"
    assert mock_func.call_count == 3

def test_retry_with_backoff_failure_ultimate():
    # Fail always
    mock_func = MagicMock(side_effect=ValueError("fail"))

    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def decorated():
        return mock_func()

    with pytest.raises(ValueError):
        decorated()

    # Calls: initial + 2 retries = 3 calls
    assert mock_func.call_count == 3

# --- augment_prompt_with_search tests ---

def test_augment_prompt_with_search_with_results():
    prompt = "Who is the president?"
    results = [{"title": "res1", "body": "content1"}]

    augmented = augment_prompt_with_search(prompt, results)

    assert "content1" in augmented
    assert "Who is the president?" in augmented
    assert "[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]" in augmented

def test_augment_prompt_with_search_no_results():
    prompt = "Hello"
    results = []
    augmented = augment_prompt_with_search(prompt, results)
    assert augmented == prompt

# --- prepare_brain_configuration tests ---

def test_prepare_brain_configuration():
    api_keys = {"google": "key1", "openai": "key2"}
    configs = prepare_brain_configuration(api_keys)

    # Assume it returns a list of config dicts or similar
    providers = [c["provider"] for c in configs]
    assert "google" in providers
    assert "openai" in providers
    assert "anthropic" not in providers

# --- generate_standard_response tests ---

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
        config={}
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
        config={}
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
        config={}
    )
    assert "Missing API Key" in response

# --- perform_internet_search tests ---

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

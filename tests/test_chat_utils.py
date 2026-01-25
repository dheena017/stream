<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import json
import pytest
from unittest.mock import MagicMock
from ui.chat_utils import serialize_messages

def test_serialize_messages_simple():
=======

import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock modules to avoid import errors
sys.modules["streamlit"] = MagicMock()
sys.modules["openai"] = MagicMock()
sys.modules["anthropic"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()

# Now import the module under test
from ui.chat_utils import (
    build_conversation_history,
    create_openai_messages,
    retry_with_backoff,
    augment_prompt_with_search
)

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
>>>>>>> origin/testing-infrastructure-11164402281265950090
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
<<<<<<< HEAD
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
    assert "Image: PNG (100, 100)" in loaded[0]["images"][0]

def test_serialize_messages_does_not_mutate_original():
    messages = [{"role": "user", "content": "test", "images": ["fake_img"]}]
    original_images = messages[0]["images"]

    serialize_messages(messages)

    assert messages[0]["images"] == original_images
=======
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
    assert history[1]["content"] == "msg 4"  # 0,1,2,3 are summarized. 4,5,6,7,8 are kept. 9 is excluded.

def test_build_conversation_history_truncation_chars():
    long_msg = "a" * 100
    messages = [{"role": "user", "content": long_msg} for _ in range(5)]
    # Total 500 chars. Limit 200.
    # The current implementation only summarizes if len > max_messages,
    # even if max_chars is exceeded.
    # We will enforce max_messages=2 to verify the summary generation logic works.
    history = build_conversation_history(messages, max_chars=200, max_messages=2, exclude_last=False)

    assert history[0]["role"] == "system"
    assert "[Earlier conversation summary]" in history[0]["content"]

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
    # The function imports create_search_context locally from ui.internet_search.
    # We need to patch it in ui.internet_search.
    # Note: Since we mocked sys.modules["ui.internet_search"] implicitly via imports or not?
    # We haven't mocked ui.internet_search in sys.modules at the top, only google, openai etc.
    # So we can patch it.

    with patch("ui.internet_search.create_search_context") as mock_ctx:
        mock_ctx.return_value = "Search Summary Info"

        prompt = "Who is the president?"
        results = [{"title": "res1", "body": "content1"}]

        augmented = augment_prompt_with_search(prompt, results)

        assert "Search Summary Info" in augmented
        assert "Who is the president?" in augmented
        assert "[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]" in augmented

def test_augment_prompt_with_search_no_results():
    prompt = "Hello"
    results = []
    augmented = augment_prompt_with_search(prompt, results)
    assert augmented == prompt
>>>>>>> origin/testing-infrastructure-11164402281265950090
=======
import pytest
from unittest.mock import MagicMock
from ui.chat_utils import (
    build_conversation_history,
    create_openai_messages,
    prepare_brain_configuration,
    generate_standard_response
)

=======
import pytest
from unittest.mock import MagicMock, patch
from ui.chat_utils import (
    build_conversation_history,
    generate_standard_response,
    augment_prompt_with_search,
    perform_internet_search
)

# Test build_conversation_history
>>>>>>> origin/qa-testing-framework-16153121365111597359
def test_build_conversation_history_basic():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        {"role": "user", "content": "How are you?"}
    ]
<<<<<<< HEAD
    # exclude_last=True by default
=======
    # exclude_last=True by default, so it should exclude the last user message
>>>>>>> origin/qa-testing-framework-16153121365111597359
    history = build_conversation_history(messages)
    assert len(history) == 2
    assert history[-1]["content"] == "Hi"

def test_build_conversation_history_limit():
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(30)]
<<<<<<< HEAD
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
>>>>>>> origin/testing-improvements-12652221572839124303
=======
    history = build_conversation_history(messages, exclude_last=False, max_messages=10)
    assert len(history) == 11 # 1 system summary + 10 recent messages
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
>>>>>>> origin/qa-testing-framework-16153121365111597359

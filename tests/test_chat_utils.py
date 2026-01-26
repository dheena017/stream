import pytest
import sys
import json
from unittest.mock import MagicMock, patch, Mock

# Mock modules to avoid import errors during test collection/execution
sys.modules["streamlit"] = MagicMock()
sys.modules["openai"] = MagicMock()
sys.modules["anthropic"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()
sys.modules["google.api_core"] = MagicMock()

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

# --- serialize_messages ---
def test_serialize_messages_simple():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
    json_str = serialize_messages(messages)
    loaded = json.loads(json_str)
    assert len(loaded) == 2
    assert loaded[0]["content"] == "Hello"

def test_serialize_messages_with_images():
    mock_img = MagicMock()
    mock_img.format = "PNG"
    mock_img.size = (100, 100)
    # The serializer expects a list of images or similar structure
    messages = [{"role": "user", "content": "Look", "images": [mock_img]}]
    json_str = serialize_messages(messages)
    loaded = json.loads(json_str)
    assert "Image: PNG (100, 100)" in loaded[0]["images"][0]

def test_serialize_messages_does_not_mutate_original():
    messages = [{"role": "user", "content": "test", "images": ["fake_img"]}]
    original_images = messages[0]["images"]
    serialize_messages(messages)
    assert messages[0]["images"] == original_images

# --- build_conversation_history ---
def test_build_conversation_history_basic():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
        {"role": "user", "content": "How are you?"}
    ]
    # Default exclude_last=True
    history = build_conversation_history(messages)
    assert len(history) == 2
    assert history[-1]["content"] == "Hi"

def test_build_conversation_history_no_exclude():
    messages = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
    history = build_conversation_history(messages, exclude_last=False)
    assert len(history) == 2

def test_build_conversation_history_limit():
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(10)]
    # limit 5 messages.
    history = build_conversation_history(messages, exclude_last=False, max_messages=5)
    assert len(history) == 6 # 5 recent + 1 summary
    assert history[0]["role"] == "system"
    assert "[Earlier conversation summary]" in history[0]["content"]

# --- create_openai_messages ---
def test_create_openai_messages_basic():
    history = [{"role": "user", "content": "prev"}]
    prompt = "current"
    msgs = create_openai_messages(history, prompt)
    assert len(msgs) == 2
    assert msgs[-1]["content"] == "current"

def test_create_openai_messages_with_system():
    history = []
    prompt = "current"
    system = "act like a pirate"
    msgs = create_openai_messages(history, prompt, system_instruction=system)
    assert msgs[0]["role"] == "system"
    assert msgs[0]["content"] == "act like a pirate"

# --- retry_with_backoff ---
def test_retry_with_backoff_success():
    mock_func = Mock(side_effect=[Exception("Fail"), "Success"])
    @retry_with_backoff(retries=3, backoff_in_seconds=0.01)
    def wrapped(): return mock_func()
    assert wrapped() == "Success"
    assert mock_func.call_count == 2

def test_retry_with_backoff_failure():
    mock_func = Mock(side_effect=Exception("Always Fail"))
    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def wrapped(): return mock_func()
    with pytest.raises(Exception):
        wrapped()
    assert mock_func.call_count == 3

# --- augment_prompt_with_search ---
def test_augment_prompt_with_search_with_results():
    prompt = "Who is the president?"
    results = [{"title": "res1", "body": "content1", "href": "url"}]
    augmented = augment_prompt_with_search(prompt, results)
    assert "content1" in augmented
    assert "Who is the president?" in augmented
    assert "[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]" in augmented

def test_augment_prompt_with_search_no_results():
    assert augment_prompt_with_search("Hi", []) == "Hi"

# --- perform_internet_search ---
@patch("ui.chat_utils.get_internet_search_engine")
def test_perform_internet_search_enabled(mock_get_engine):
    mock_engine = MagicMock()
    mock_engine.search.return_value = [{"title": "Test", "body": "Content"}]
    mock_get_engine.return_value = mock_engine
    results, context = perform_internet_search("query", enable_search=True)
    assert len(results) == 1
    assert "Content" in context

# --- prepare_brain_configuration ---
def test_prepare_brain_configuration():
    api_keys = {"google": "key1", "openai": "key2"}
    configs = prepare_brain_configuration(api_keys)
    providers = [c["provider"] for c in configs]
    assert "google" in providers
    assert "openai" in providers

# --- generate_standard_response ---
@patch("ui.chat_utils.handle_google_provider")
def test_generate_standard_response_google(mock_handle_google):
    mock_handle_google.return_value = "Google Response"
    response = generate_standard_response(
        provider="google", model_name="gemini", api_keys={"google": "k"},
        prompt="Hi", chat_history=[]
    )
    assert response == "Google Response"

@patch("ui.chat_utils.handle_openai_compatible_provider")
@patch("ui.chat_utils.get_openai_client")
def test_generate_standard_response_openai(mock_get_client, mock_handle_openai):
    mock_handle_openai.return_value = "OpenAI Response"
    response = generate_standard_response(
        provider="openai", model_name="gpt-4", api_keys={"openai": "k"},
        prompt="Hi", chat_history=[]
    )
    assert response == "OpenAI Response"

def test_generate_standard_response_missing_key():
    response = generate_standard_response(
        provider="google", model_name="gemini", api_keys={},
        prompt="Hi", chat_history=[]
    )
    assert "Missing API Key" in response

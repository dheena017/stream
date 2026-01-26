import pytest
import json
from unittest.mock import MagicMock, patch
import sys

# Mock imports
sys.modules["streamlit"] = MagicMock()
sys.modules["openai"] = MagicMock()
sys.modules["anthropic"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()

from ui.chat_utils import (
    serialize_messages,
    build_conversation_history,
    create_openai_messages,
    augment_prompt_with_search,
    retry_with_backoff,
    perform_internet_search,
    generate_standard_response,
    prepare_brain_configuration
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
    messages = [{"role": "user", "content": "Look", "images": [mock_img]}]

    json_str = serialize_messages(messages)
    loaded = json.loads(json_str)
    assert "Image: PNG (100, 100)" in loaded[0]["images"][0]

# --- build_conversation_history ---
def test_build_conversation_history_basic():
    messages = [
        {"role": "user", "content": "1"},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "3"}
    ]
    # Default exclude_last=True
    history = build_conversation_history(messages)
    assert len(history) == 2
    assert history[-1]["content"] == "2"

def test_build_conversation_history_truncation_messages():
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(10)]
    # exclude_last=False to keep all 10. Max 5. -> 1 summary + 5 recent = 6
    history = build_conversation_history(messages, max_messages=5, exclude_last=False)
    assert len(history) == 6
    assert "[Earlier conversation summary]" in history[0]["content"]

# --- create_openai_messages ---
def test_create_openai_messages_basic():
    history = [{"role": "user", "content": "prev"}]
    prompt = "current"
    msgs = create_openai_messages(history, prompt)
    assert len(msgs) == 2
    assert msgs[-1]["content"] == "current"

# --- augment_prompt_with_search ---
def test_augment_prompt_with_search_with_results():
    prompt = "Query"
    results = [{"title": "T", "body": "B"}]
    augmented = augment_prompt_with_search(prompt, results)
    assert "Query" in augmented
    assert "SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS" in augmented
    assert "Title: T" in augmented

# --- retry_with_backoff ---
def test_retry_with_backoff_success():
    mock_func = MagicMock(return_value="success")
    @retry_with_backoff(retries=3)
    def decorated(): return mock_func()
    assert decorated() == "success"

def test_retry_with_backoff_failure():
    mock_func = MagicMock(side_effect=ValueError("fail"))
    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def decorated(): return mock_func()
    with pytest.raises(ValueError):
        decorated()
    assert mock_func.call_count == 3

# --- perform_internet_search ---
@patch("ui.chat_utils.get_search_engine")
def test_perform_internet_search_enabled(mock_get_engine):
    mock_engine = MagicMock()
    mock_engine.search.return_value = [{"title": "T", "body": "B"}]
    mock_get_engine.return_value = mock_engine

    # We also need to patch create_search_context if it's imported
    with patch("ui.chat_utils.create_search_context", return_value="Context"):
        results, context = perform_internet_search("query", enable_search=True)
        assert len(results) == 1
        assert context == "Context"

# --- generate_standard_response ---
@patch("ui.chat_utils.handle_google_provider")
def test_generate_standard_response_google(mock_handle):
    mock_handle.return_value = "G"
    resp = generate_standard_response("google", "gemini", {"google": "key"}, "p", [])
    assert resp == "G"

def test_prepare_brain_configuration():
    configs = prepare_brain_configuration({"google": "k"})
    assert configs[0]["provider"] == "google"

import pytest
import sys
import os
import json
from unittest.mock import MagicMock, patch, Mock

# Ensure we can import from ui
sys.path.append(os.getcwd())

# Mock modules to avoid import errors if dependencies are missing in some envs
if "streamlit" not in sys.modules:
    sys.modules["streamlit"] = MagicMock()
if "openai" not in sys.modules:
    sys.modules["openai"] = MagicMock()
if "anthropic" not in sys.modules:
    sys.modules["anthropic"] = MagicMock()
if "google.generativeai" not in sys.modules:
    sys.modules["google.generativeai"] = MagicMock()

from ui.chat_utils import (
    build_conversation_history,
    create_openai_messages,
    prepare_brain_configuration,
    generate_standard_response,
    augment_prompt_with_search,
    perform_internet_search,
    serialize_messages
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
    assert history[1]["content"] == "msg 4"

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

def test_serialize_messages_with_images():
    messages = [
        {
            "role": "user",
            "content": "Look at this",
            "images": ["fake_img"]
        }
    ]
    json_str = serialize_messages(messages)
    loaded = json.loads(json_str)
    assert len(loaded) == 1
    assert "Image: fake_img" in loaded[0]["images"][0]

# --- create_openai_messages tests ---

def test_create_openai_messages_basic():
    history = [{"role": "user", "content": "prev"}]
    prompt = "current"
    msgs = create_openai_messages(history, prompt)

    assert len(msgs) == 2
    assert msgs[0]["content"] == "prev"
    assert msgs[1]["role"] == "user"
    assert msgs[1]["content"] == "current"

# --- augment_prompt_with_search tests ---

def test_augment_prompt_with_search_with_results():
    prompt = "Who is the president?"
    results = [{"title": "res1", "body": "content1"}]
    augmented = augment_prompt_with_search(prompt, results)
    assert "content1" in augmented
    assert "[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]" in augmented

def test_augment_prompt_with_search_no_results():
    prompt = "Hello"
    results = []
    augmented = augment_prompt_with_search(prompt, results)
    assert augmented == prompt

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

import json
import pytest
from unittest.mock import MagicMock
from ui.chat_utils import serialize_messages

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

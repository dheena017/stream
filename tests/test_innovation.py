
import json
import pytest
from unittest.mock import MagicMock
from ui.chat_utils import export_chat_to_json

def test_export_chat_to_json():
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"}
    ]

    json_str = export_chat_to_json(messages)
    data = json.loads(json_str)

    assert "timestamp" in data
    assert "messages" in data
    assert len(data["messages"]) == 2
    assert data["messages"][0]["content"] == "Hello"
    assert data["messages"][1]["content"] == "Hi"

def test_export_chat_to_json_with_images():
    # Mock PIL Image
    mock_img = MagicMock()
    mock_img.format = "PNG"
    mock_img.size = (50, 50)

    messages = [
        {"role": "user", "content": "Image msg", "images": [mock_img]}
    ]

    json_str = export_chat_to_json(messages)
    data = json.loads(json_str)

    assert "messages" in data
    assert len(data["messages"]) == 1
    # Check that image was serialized
    assert isinstance(data["messages"][0]["images"], list)
    assert "Image: PNG (50, 50)" in data["messages"][0]["images"][0]



from ui.experimental import (
    calculate_chat_stats,
    format_messages_markdown,
    serialize_messages_for_export,
)


class MockImage:
    def __init__(self, size=(100, 100)):
        self.size = size


def test_serialize_messages_for_export():
    messages = [
        {
            "role": "user",
            "content": "Hello",
            "images": [MockImage((200, 200))],
            "timestamp": "12:00:00",
        },
        {
            "role": "assistant",
            "content": "Hi there!",
            "provider": "google",
            "model": "gemini-pro",
        },
    ]

    json_output = serialize_messages_for_export(messages)

    assert "Hello" in json_output
    assert "Hi there!" in json_output
    assert "[Image: (200, 200)]" in json_output
    assert "google" in json_output


def test_format_messages_markdown():
    messages = [
        {"role": "user", "content": "Hello", "timestamp": "12:00"},
        {
            "role": "assistant",
            "content": "Hi there",
            "provider": "openai",
            "model": "gpt-4",
        },
    ]

    md = format_messages_markdown(messages)

    assert "# Chat Export" in md
    assert "### User (12:00)" in md
    assert "Hello" in md
    assert "### Assistant" in md
    assert "openai/gpt-4" in md


def test_calculate_chat_stats():
    messages = [
        {"role": "user", "content": "123"},
        {"role": "assistant", "content": "12345", "response_time": 1.5},
        {"role": "user", "content": "123"},
    ]

    stats = calculate_chat_stats(messages)

    assert stats["total_messages"] == 3
    assert stats["user_count"] == 2
    assert stats["assistant_count"] == 1
    assert stats["avg_response_time"] == 1.5
    assert stats["total_chars"] == 11


def test_calculate_chat_stats_empty():
    stats = calculate_chat_stats([])
    assert stats == {}

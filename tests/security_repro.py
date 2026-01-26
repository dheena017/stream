
from ui import chat_utils


def test_sanitize_text_exists():
    assert hasattr(
        chat_utils, "sanitize_text"
    ), "sanitize_text function is missing in chat_utils"


def test_rate_limiter_exists():
    assert hasattr(
        chat_utils, "RateLimiter"
    ), "RateLimiter class is missing in chat_utils"

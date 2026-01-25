import pytest
import time
from unittest.mock import MagicMock
import sys

# Mock streamlit before importing ui.security if not already imported
if 'streamlit' not in sys.modules:
    sys.modules['streamlit'] = MagicMock()

from ui.security import hash_password, verify_password, sanitize_html, RateLimiter
import ui.security

def test_hashing():
    password = "MySecurePassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)
    # verify_password catches exceptions and returns False
    assert not verify_password(password, "$2b$12$invalidhashstructure")

def test_sanitize_html():
    unsafe = "<script>alert(1)</script>"
    safe = sanitize_html(unsafe)
    assert "<script>" not in safe
    assert "&lt;script&gt;" in safe

    unsafe_attr = '"><img src=x onerror=alert(1)>'
    safe_attr = sanitize_html(unsafe_attr)
    # html.escape escapes " as &quot;
    assert '&quot;' in safe_attr

    assert sanitize_html(None) == ""
    assert sanitize_html(123) == "123"

def test_rate_limiter():
    # Manually patch get_rate_limit_store to return a persistent dictionary
    # because st.cache_resource doesn't work as expected in unit tests without a session
    from collections import defaultdict, deque
    store = defaultdict(lambda: deque())

    # Save original to restore later if needed (though not strictly necessary for this run)
    original_func = ui.security.get_rate_limit_store
    ui.security.get_rate_limit_store = lambda: store

    try:
        limiter = RateLimiter(max_requests=2, period=1)
        key = "test_user"

        assert limiter.is_allowed(key) == True
        assert limiter.is_allowed(key) == True
        assert limiter.is_allowed(key) == False

        time.sleep(1.1)
        assert limiter.is_allowed(key) == True
    finally:
        ui.security.get_rate_limit_store = original_func

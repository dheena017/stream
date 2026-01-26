
import streamlit as st

from ui.chat_utils import RateLimiter, sanitize_text


def test_sanitize_text():
    assert (
        sanitize_text("<script>alert(1)</script>")
        == "&lt;script&gt;alert(1)&lt;/script&gt;"
    )
    assert sanitize_text("Hello World") == "Hello World"
    assert sanitize_text("") == ""
    assert sanitize_text(None) == ""


def test_rate_limiter():
    # Mock session state
    # Streamlit session state is a bit tricky to mock directly without streamlit runtime,
    # but since RateLimiter uses st.session_state directly, we need to ensure it acts like a dict
    # or patch it.

    # We can patch st.session_state
    original_session_state = st.session_state

    class MockSessionState(dict):
        def __getattr__(self, key):
            return self.get(key)

        def __setattr__(self, key, value):
            self[key] = value

    st.session_state = MockSessionState()

    try:
        limiter = RateLimiter(max_requests=2, window_seconds=10)
        user_id = "test_user"

        assert limiter.check(user_id) is True
        assert limiter.check(user_id) is True
        assert limiter.check(user_id) is False  # 3rd request should fail
    finally:
        st.session_state = original_session_state

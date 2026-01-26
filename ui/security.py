import bcrypt
import html
import time
import streamlit as st
from collections import defaultdict, deque

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    # bcrypt.hashpw returns bytes, we decode to utf-8 string for storage
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a bcrypt hash."""
    try:
        if not hashed_password or not isinstance(hashed_password, str):
            return False
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        # Invalid salt or hash format
        return False
    except Exception:
        return False

def sanitize_html(text: str) -> str:
    """Escapes HTML characters in the text."""
    if text is None:
        return ""
    return html.escape(str(text))

@st.cache_resource
def get_rate_limit_store():
    """Returns a thread-safe store for rate limiting."""
    return defaultdict(lambda: deque())

class RateLimiter:
    def __init__(self, max_requests: int, period: float, store=None):
        self.max_requests = max_requests
        self.period = period
        # We access the store via the function to ensure it's the cached instance
        self.store = store if store is not None else get_rate_limit_store()

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        timestamps = self.store[key]

        # Remove old timestamps
        while timestamps and timestamps[0] <= now - self.period:
            timestamps.popleft()

        if len(timestamps) < self.max_requests:
            timestamps.append(now)
            return True
        return False

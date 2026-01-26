import bcrypt
import html
import time
from collections import defaultdict, deque
import streamlit as st

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # salt is saved into the hash itself
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False

def sanitize_html(input_val) -> str:
    """Sanitize input to prevent XSS."""
    if input_val is None:
        return ""
    return html.escape(str(input_val))

@st.cache_resource
def get_rate_limit_store():
    """Returns a dictionary to store rate limit data."""
    return defaultdict(lambda: deque())

class RateLimiter:
    def __init__(self, max_requests: int, period: int):
        self.max_requests = max_requests
        self.period = period
        self.store = get_rate_limit_store()

    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed for the given key."""
        now = time.time()
        timestamps = self.store[key]

        # Remove old timestamps
        while timestamps and timestamps[0] <= now - self.period:
            timestamps.popleft()

        if len(timestamps) < self.max_requests:
            timestamps.append(now)
            return True
        return False

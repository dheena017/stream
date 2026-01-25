import streamlit as st
import html
import bcrypt
import time
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

# --- Input Sanitization ---
def sanitize_html(text: str) -> str:
    """Escapes HTML characters to prevent XSS."""
    if text is None:
        return ""
    if not isinstance(text, str):
        return str(text)
    return html.escape(text)

# --- Password Hashing ---
def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    # bcrypt requires bytes
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verifies a password against a bcrypt hash."""
    try:
        pwd_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

# --- Rate Limiting ---
@st.cache_resource
def get_rate_limit_store():
    return defaultdict(lambda: deque())

class RateLimiter:
    def __init__(self, max_requests: int = 5, period: int = 60):
        self.max_requests = max_requests
        self.period = period # seconds

    def is_allowed(self, key: str) -> bool:
        store = get_rate_limit_store()
        now = time.time()
        timestamps = store[key]

        # Remove old timestamps
        while timestamps and timestamps[0] < now - self.period:
            timestamps.popleft()

        if len(timestamps) < self.max_requests:
            timestamps.append(now)
            return True
        return False

import pytest
import sys
from unittest.mock import MagicMock, patch

# Force cleanup of modules to avoid pollution from other tests
for mod in ['ui.auth', 'ui.security', 'streamlit']:
    if mod in sys.modules:
        del sys.modules[mod]

# Mock streamlit before importing ui.auth
mock_st = MagicMock()
_cache_store = {}
def mock_cache_resource(func=None, **kwargs):
    def wrapper(f):
        def cached_func(*args, **kwargs):
            if f.__name__ == 'get_rate_limiter_state' or f.__name__ == 'get_rate_limit_store':
                if 'rate_limiter' not in _cache_store:
                    _cache_store['rate_limiter'] = f(*args, **kwargs)
                return _cache_store['rate_limiter']
            return f(*args, **kwargs)
        return cached_func
    if func:
        return wrapper(func)
    return wrapper

mock_st.cache_resource = mock_cache_resource
mock_st.session_state = {}
sys.modules["streamlit"] = mock_st
sys.modules["google.oauth2"] = MagicMock()
sys.modules["google.auth.transport"] = MagicMock()

from ui import auth

# Reset global rate limiter for tests
auth.get_rate_limiter_state().clear()

def test_hash_password_format():
    """Test that password hash is valid bcrypt hash."""
    pw = "testpass"
    hashed = auth.hash_password(pw)
    # Check for bcrypt prefix
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$") or hashed.startswith("$2y$")
    assert auth.verify_password(hashed, pw)

def test_verify_password():
    """Test password verification (salted/bcrypt)"""
    pw = "securepassword"
    hashed = auth.hash_password(pw)

    assert auth.verify_password(hashed, pw) is True
    assert auth.verify_password(hashed, "wrongpassword") is False

def test_verify_legacy_password():
    """Test verification of old unsalted passwords"""
    import hashlib
    pw = "legacy"
    legacy_hash = hashlib.sha256(pw.encode()).hexdigest()

    assert auth.verify_password(legacy_hash, pw) is True
    assert auth.verify_password(legacy_hash, "wrong") is False

@patch("ui.auth.load_user_credentials")
def test_rate_limiting(mock_load):
    """Test that login is rate limited after max attempts"""
    # Mock user data
    mock_load.return_value = {
        "testuser": {
            "password": auth.hash_password("password"),
            "email": "test@example.com",
            "name": "Test User"
        }
    }

    username = "testuser"

    # Reset rate limiter
    auth.get_rate_limiter_state().clear()

    # 5 allowed attempts
    for _ in range(5):
        # We need check_login to actually consume
        # The mock returns user data if password matches.
        # But here we pass "wrongpass".
        assert auth.check_login(username, "wrongpass") is None

    # 6th attempt should be blocked
    assert auth.is_rate_limited(username) is True
    assert auth.check_login(username, "password") is None

@patch("ui.auth.save_user_credentials")
@patch("ui.auth.load_user_credentials")
def test_register_user_hashing(mock_load, mock_save):
    """Test that registration saves salted hash"""
    mock_load.return_value = {}
    mock_save.return_value = True

    username = "newuser"
    password = "newpassword"

    auth.register_user(username, "new@example.com", password)

    # Check arguments passed to save
    saved_data = mock_save.call_args[0][0]
    assert username in saved_data
    stored_pw = saved_data[username]["password"]
    assert stored_pw.startswith("$2b$") or stored_pw.startswith("$2a$")
    assert auth.verify_password(stored_pw, password)

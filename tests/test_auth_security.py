import sys
from unittest.mock import MagicMock, patch


# Mock streamlit before importing ui.auth
mock_st = MagicMock()
# Mock cache_resource to return a singleton-like behavior or just a consistent object
_cache_store = {}


def mock_cache_resource(func=None, **kwargs):
    def wrapper(f):
        def cached_func(*args, **kwargs):
            # Only cache get_rate_limiter_state for this test
            if f.__name__ == "get_rate_limiter_state":
                if "rate_limiter" not in _cache_store:
                    _cache_store["rate_limiter"] = f(*args, **kwargs)
                return _cache_store["rate_limiter"]
            return f(*args, **kwargs)

        return cached_func

    if func:
        return wrapper(func)
    return wrapper


mock_st.cache_resource = mock_cache_resource
mock_st.session_state = {}
sys.modules["streamlit"] = mock_st

# Mock google libraries to avoid import errors if not installed in test env
sys.modules["google.oauth2"] = MagicMock()
sys.modules["google.auth.transport"] = MagicMock()

# Now import the module under test
from ui import auth

# Reset global rate limiter for tests
auth.get_rate_limiter_state().clear()


def test_hash_password_format():
    """Test that password hash includes salt and follows format"""
    pw = "testpass"
    hashed = auth.hash_password(pw)
    assert "$" in hashed
    salt, hash_val = hashed.split("$")
    assert len(salt) == 32  # 16 bytes hex
    assert len(hash_val) == 64  # sha256 hex


def test_verify_password():
    """Test password verification (salted)"""
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
            "name": "Test User",
        }
    }

    username = "testuser"

    # Reset rate limiter
    auth.get_rate_limiter_state().clear()

    # 5 allowed attempts
    for _ in range(5):
        assert auth.check_login(username, "wrongpass") is None

    # 6th attempt should be blocked (and return None)
    # Ideally we'd distinguish between blocked and wrong pass, but function returns None for both.
    # We can check the rate limiter state directly.
    assert auth.is_rate_limited(username) is True

    # Even correct password should fail now if strictly enforced,
    # but the implementation checks rate limit *before* verifying password.
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
    assert "$" in stored_pw
    assert auth.verify_password(stored_pw, password)

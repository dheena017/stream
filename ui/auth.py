import json
import os
import hashlib
from ui.security import hash_password as secure_hash, verify_password as secure_verify, RateLimiter, get_rate_limit_store

USERS_FILE = "users.json"

def get_rate_limiter_state():
    """Returns the rate limiter store."""
    return get_rate_limit_store()

def load_user_credentials():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_user_credentials(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return True

def hash_password(password):
    """Wrapper for secure hashing."""
    return secure_hash(password)

def verify_password(stored_hash, password):
    """Wrapper for secure verification with legacy fallback."""
    # First try secure bcrypt verification
    if secure_verify(password, stored_hash):
        return True

    # Fallback: check for legacy SHA256 hash (64 hex chars)
    # This ensures old accounts (from the test scenario) still work
    if stored_hash and len(stored_hash) == 64:
        try:
            # Check if it is hex
            int(stored_hash, 16)
            if hashlib.sha256(password.encode('utf-8')).hexdigest() == stored_hash:
                return True
        except ValueError:
            pass

    return False

# Initialize rate limiter: 5 attempts per minute
login_rate_limiter = RateLimiter(max_requests=5, period=60)

def is_rate_limited(username):
    store = login_rate_limiter.store
    timestamps = store[username]
    import time
    now_ts = time.time()
    valid_timestamps = [t for t in timestamps if t > now_ts - login_rate_limiter.period]
    return len(valid_timestamps) >= login_rate_limiter.max_requests

def check_login(username, password):
    # Check limit before consuming?
    # Standard: check limit. If limited, reject.
    if is_rate_limited(username):
        return None

    # Consume attempt
    login_rate_limiter.is_allowed(username)

    users = load_user_credentials()
    if username not in users:
        return None

    user_data = users[username]
    stored_hash = user_data.get("password")

    if verify_password(stored_hash, password):
        return user_data
    return None

def register_user(username, email, password):
    users = load_user_credentials()
    if username in users:
        return False

    hashed = hash_password(password)
    users[username] = {
        "password": hashed,
        "email": email,
        "name": username
    }
    save_user_credentials(users)
    return True

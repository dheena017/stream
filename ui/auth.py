import json
import os
import streamlit as st
from typing import Dict, Optional

USERS_FILE = "users.json"

def load_user_credentials() -> Dict:
    """Load user credentials from disk."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_user_credentials(users: Dict) -> bool:
    """Save user credentials to disk."""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def delete_user(username: str) -> bool:
    """Delete a user from the credentials file."""
    users = load_user_credentials()
    if username in users:
        del users[username]
        return save_user_credentials(users)
    return False

def init_auth():
    """Initialize authentication state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

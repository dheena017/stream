import json
import os
from typing import Any, Dict, Optional

PREFS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_prefs.json")


def _read_prefs() -> Dict[str, Any]:
    try:
        if os.path.exists(PREFS_FILE):
            with open(PREFS_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _write_prefs(data: Dict[str, Any]) -> bool:
    try:
        with open(PREFS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


def load_prefs(username: Optional[str] = None) -> Dict[str, Any]:
    """Load preferences for a given username or global if None."""
    data = _read_prefs()
    key = username or "__global__"
    return data.get(key, {})


def save_prefs(prefs: Dict[str, Any], username: Optional[str] = None) -> bool:
    """Save preferences for a given username or global if None."""
    data = _read_prefs()
    key = username or "__global__"
    data[key] = prefs
    return _write_prefs(data)


def set_pref(key: str, value: Any, username: Optional[str] = None) -> bool:
    cur = load_prefs(username)
    cur[key] = value
    return save_prefs(cur, username)


def get_pref(key: str, username: Optional[str] = None, default: Any = None) -> Any:
    cur = load_prefs(username)
    return cur.get(key, default)


def save_dark_mode_from_session(username: Optional[str] = None) -> bool:
    """Convenience: read `st.session_state['dark_mode']` and persist it."""
    try:
        import streamlit as st

        val = bool(st.session_state.get("dark_mode", False))
        return set_pref("dark_mode", val, username)
    except Exception:
        return False

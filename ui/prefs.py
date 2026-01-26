import json
import os
from typing import Dict, Any

PREFS_FILE = "user_prefs.json"
DEFAULT_RETENTION_DAYS = 30

def _load_all_prefs() -> Dict[str, Any]:
    if not os.path.exists(PREFS_FILE):
        return {}
    try:
        with open(PREFS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_all_prefs(prefs: Dict[str, Any]):
    with open(PREFS_FILE, 'w') as f:
        json.dump(prefs, f, indent=4)

def get_user_prefs(user_id: str) -> Dict[str, Any]:
    """Get all preferences for a user."""
    all_prefs = _load_all_prefs()
    return all_prefs.get(user_id, {})

def save_user_prefs(user_id: str, prefs: Dict[str, Any]):
    """Save preferences for a user."""
    all_prefs = _load_all_prefs()
    all_prefs[user_id] = prefs
    _save_all_prefs(all_prefs)

def get_retention_days(user_id: str) -> int:
    """Get retention period in days for a user."""
    prefs = get_user_prefs(user_id)
    return prefs.get("retention_days", DEFAULT_RETENTION_DAYS)

def save_retention_days(user_id: str, days: int):
    """Save retention period in days for a user."""
    prefs = get_user_prefs(user_id)
    prefs["retention_days"] = days
    save_user_prefs(user_id, prefs)

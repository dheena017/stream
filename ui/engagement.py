import streamlit as st
from ui.database import get_total_message_count
from ui.prefs import get_pref, set_pref

# Define achievements
ACHIEVEMENTS = {
    "first_step": {
        "title": "First Step",
        "description": "Sent your first message",
        "icon": "🌱",
        "condition": lambda count, stats: count >= 1
    },
    "chatterbox": {
        "title": "Chatterbox",
        "description": "Sent 50 messages",
        "icon": "💬",
        "condition": lambda count, stats: count >= 50
    },
    "centurion": {
        "title": "Centurion",
        "description": "Sent 100 messages",
        "icon": "💯",
        "condition": lambda count, stats: count >= 100
    },
    "polymath": {
        "title": "Polymath",
        "description": "Learned 5 topics",
        "icon": "🧠",
        "condition": lambda count, stats: stats.get('total_topics', 0) >= 5
    },
    "explorer": {
        "title": "Explorer",
        "description": "Used 3 different models",
        "icon": "🧭",
        "condition": lambda count, stats: stats.get('models_tracked', 0) >= 3
    }
}

LEVELS = [
    (0, "Novice"),
    (10, "Apprentice"),
    (50, "Journeyman"),
    (100, "Expert"),
    (500, "Master"),
    (1000, "Grandmaster")
]

def calculate_level(total_messages: int):
    """
    Calculate user level based on message count.
    Returns (level_number, title, progress_percent, next_level_threshold)
    """
    current_level = 1
    current_title = "Novice"
    next_threshold = 10
    prev_threshold = 0

    for threshold, title in LEVELS:
        if total_messages >= threshold:
            current_title = title
            prev_threshold = threshold
            # Find next threshold
            try:
                # Find index of current threshold
                idx = -1
                for i, l in enumerate(LEVELS):
                    if l[0] == threshold:
                        idx = i
                        break

                if idx != -1 and idx + 1 < len(LEVELS):
                    next_threshold = LEVELS[idx + 1][0]
                    current_level = idx + 1
                else:
                    next_threshold = threshold * 2 # Cap
                    current_level = len(LEVELS)
            except ValueError:
                pass

    # Calculate progress
    if next_threshold > prev_threshold:
        progress = (total_messages - prev_threshold) / (next_threshold - prev_threshold)
    else:
        progress = 1.0

    return current_level, current_title, min(max(progress, 0.0), 1.0), next_threshold

def check_achievements(username: str, learning_stats: dict):
    """
    Check for new achievements.
    Returns a list of newly unlocked achievements (dicts).
    """
    # Get user message count
    count = get_total_message_count(username)

    # Get previously unlocked
    unlocked_ids = get_pref("achievements", username, [])
    if not isinstance(unlocked_ids, list):
        unlocked_ids = []

    new_unlocks = []

    for aid, data in ACHIEVEMENTS.items():
        if aid not in unlocked_ids:
            if data["condition"](count, learning_stats):
                unlocked_ids.append(aid)
                new_unlocks.append(data)

    # Save if any new
    if new_unlocks:
        set_pref("achievements", unlocked_ids, username)

    return new_unlocks

def get_leaderboard_data(username: str, current_count: int):
    """
    Generate leaderboard data.
    Since we don't have a centralized user DB for this demo,
    we'll generate some static comparison points and insert the current user.
    """

    data = [
        {"name": "Alice (AI)", "score": 1250, "rank": 1},
        {"name": "Bob (AI)", "score": 850, "rank": 2},
        {"name": "Charlie (AI)", "score": 420, "rank": 3},
        {"name": "Dave (AI)", "score": 150, "rank": 4},
        {"name": "Eve (AI)", "score": 45, "rank": 5},
    ]

    # Insert user
    user_entry = {"name": f"{username} (You)", "score": current_count, "rank": 0}

    # Check if user is already in (not possible with fake data, but good practice)
    data.append(user_entry)

    # Sort
    data.sort(key=lambda x: x["score"], reverse=True)

    # Re-rank
    for i, entry in enumerate(data):
        entry["rank"] = i + 1

    return data

def get_unlocked_achievements(username: str):
    """Return list of achievement objects that are unlocked"""
    unlocked_ids = get_pref("achievements", username, [])
    if not isinstance(unlocked_ids, list):
        unlocked_ids = []
    return [ACHIEVEMENTS[aid] for aid in unlocked_ids if aid in ACHIEVEMENTS], unlocked_ids


import json
import logging
from datetime import datetime, timedelta
import streamlit as st
from ui.database import get_user_stats, update_user_stats

logger = logging.getLogger(__name__)

XP_PER_MESSAGE = 10
XP_PER_STREAK_DAY = 50

# Level thresholds: Level X requires roughly 100 * X XP
# 1: 0-99
# 2: 100-299
# 3: 300-599
# ...
def calculate_level(xp: int) -> int:
    level = 1
    required_xp = 100
    while xp >= required_xp:
        xp -= required_xp
        level += 1
        required_xp = 100 * level
    return level

ACHIEVEMENTS = {
    "first_steps": {"name": "First Steps", "desc": "Send your first message", "icon": "👶"},
    "regular": {"name": "Regular", "desc": "Send 10 messages", "icon": "💬"},
    "chatterbox": {"name": "Chatterbox", "desc": "Send 50 messages", "icon": "🗣️"},
    "centurion": {"name": "Centurion", "desc": "Send 100 messages", "icon": "💯"},
    "week_streak": {"name": "On Fire", "desc": "7-day streak", "icon": "🔥"},
    "brain_user": {"name": "Brainy", "desc": "Use Brain Mode", "icon": "🧠"},
}

def check_achievements(stats: dict, activity_type: str = "message") -> list:
    unlocked = []
    current_achievements = set(stats.get("achievements", []))

    messages = stats.get("messages_sent", 0)
    streak = stats.get("streak_days", 0)

    # Message count achievements
    if messages >= 1 and "first_steps" not in current_achievements:
        unlocked.append("first_steps")
    if messages >= 10 and "regular" not in current_achievements:
        unlocked.append("regular")
    if messages >= 50 and "chatterbox" not in current_achievements:
        unlocked.append("chatterbox")
    if messages >= 100 and "centurion" not in current_achievements:
        unlocked.append("centurion")

    # Streak achievements
    if streak >= 7 and "week_streak" not in current_achievements:
        unlocked.append("week_streak")

    # Special activity achievements
    if activity_type == "brain_mode" and "brain_user" not in current_achievements:
        unlocked.append("brain_user")

    return unlocked

def update_engagement(user_id: str, activity_type: str = "message") -> dict:
    """
    Updates user stats based on activity.
    Returns a dict with changes: {'level_up': bool, 'new_level': int, 'new_achievements': list}
    """
    stats = get_user_stats(user_id)

    current_xp = stats['xp']
    current_level = stats['level']
    messages = stats['messages_sent']
    streak = stats['streak_days']
    last_active = stats['last_active_date']
    achievements = stats['achievements']

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Update Stats
    if activity_type == "message" or activity_type == "brain_mode":
        messages += 1
        current_xp += XP_PER_MESSAGE

    # Streak Logic
    if last_active != today:
        if last_active == yesterday:
            streak += 1
            current_xp += XP_PER_STREAK_DAY
        else:
            streak = 1 # Reset or start

    # Recalculate Level
    new_level = calculate_level(current_xp)
    level_up = new_level > current_level

    # Check Achievements
    temp_stats = stats.copy()
    temp_stats['messages_sent'] = messages
    temp_stats['streak_days'] = streak

    new_unlocks = check_achievements(temp_stats, activity_type)
    achievements.extend(new_unlocks)

    # Persist Changes
    update_user_stats(
        user_id,
        xp=current_xp,
        level=new_level,
        messages_sent=messages,
        streak_days=streak,
        last_active_date=today,
        achievements=achievements
    )

    return {
        "level_up": level_up,
        "new_level": new_level,
        "new_achievements": [ACHIEVEMENTS[code] for code in new_unlocks]
    }

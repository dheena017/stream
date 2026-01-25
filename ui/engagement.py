<<<<<<< HEAD

import json
import logging
from datetime import datetime, timedelta
import streamlit as st
=======
import logging
import math
from datetime import datetime
from typing import Dict, List, Tuple
>>>>>>> origin/engagement-features-3224553925721226807
from ui.database import get_user_stats, update_user_stats

logger = logging.getLogger(__name__)

<<<<<<< HEAD
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
=======
ACHIEVEMENTS = [
    {
        "id": "first_step",
        "name": "First Step",
        "description": "Send your first message",
        "icon": "🌱",
        "xp_reward": 50,
        "condition": lambda stats: stats.get("total_messages", 0) >= 1
    },
    {
        "id": "curious_mind",
        "name": "Curious Mind",
        "description": "Send 10 messages",
        "icon": "🧐",
        "xp_reward": 100,
        "condition": lambda stats: stats.get("total_messages", 0) >= 10
    },
    {
        "id": "power_user",
        "name": "Power User",
        "description": "Send 100 messages",
        "icon": "⚡",
        "xp_reward": 500,
        "condition": lambda stats: stats.get("total_messages", 0) >= 100
    },
    {
        "id": "level_5",
        "name": "Rising Star",
        "description": "Reach Level 5",
        "icon": "⭐",
        "xp_reward": 200,
        "condition": lambda stats: stats.get("level", 1) >= 5
    },
    {
        "id": "level_10",
        "name": "AI Master",
        "description": "Reach Level 10",
        "icon": "👑",
        "xp_reward": 1000,
        "condition": lambda stats: stats.get("level", 1) >= 10
    }
]

class EngagementManager:
    """Manages user engagement, gamification, and stats"""

    def __init__(self):
        self.xp_per_message = 10
        self.xp_per_level = 100

    def calculate_level(self, xp: int) -> int:
        """Calculate level based on XP"""
        # Level 1 starts at 0 XP
        # Level 2 starts at 100 XP
        return 1 + int(xp / self.xp_per_level)

    def get_next_level_progress(self, xp: int) -> float:
        """Get progress to next level (0.0 to 1.0)"""
        return (xp % self.xp_per_level) / self.xp_per_level

    def log_activity(self, user_id: str, activity_type: str) -> Dict:
        """
        Log user activity and update stats.
        Returns a dict with 'level_up' (bool), 'new_achievements' (List[Dict]), 'stats' (Dict)
        """
        stats = get_user_stats(user_id)

        previous_level = stats['level']
        new_achievements = []

        # Update stats based on activity
        if activity_type == "message_sent":
            stats['total_messages'] += 1
            stats['xp'] += self.xp_per_message

        # Check for level up
        current_level = self.calculate_level(stats['xp'])
        if current_level > previous_level:
            stats['level'] = current_level

        # Check for achievements
        current_achievement_ids = [a['id'] for a in stats['achievements']]

        for achievement in ACHIEVEMENTS:
            if achievement['id'] not in current_achievement_ids:
                if achievement['condition'](stats):
                    # Unlock achievement
                    achievement_data = {
                        "id": achievement['id'],
                        "name": achievement['name'],
                        "description": achievement['description'],
                        "icon": achievement['icon'],
                        "unlocked_at": datetime.now().isoformat()
                    }
                    stats['achievements'].append(achievement_data)
                    stats['xp'] += achievement['xp_reward']
                    new_achievements.append(achievement_data)

                    # Re-check level after achievement XP reward
                    stats['level'] = self.calculate_level(stats['xp'])

        # Save updates
        update_user_stats(user_id, stats)

        return {
            "level_up": stats['level'] > previous_level,
            "new_achievements": new_achievements,
            "stats": stats
        }

    def get_user_badges(self, user_id: str) -> List[Dict]:
        """Get list of unlocked badges for UI"""
        stats = get_user_stats(user_id)
        return stats.get('achievements', [])
>>>>>>> origin/engagement-features-3224553925721226807

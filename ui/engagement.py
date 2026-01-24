import logging
import math
from datetime import datetime
from typing import Dict, List, Tuple
from ui.database import get_user_stats, update_user_stats

logger = logging.getLogger(__name__)

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

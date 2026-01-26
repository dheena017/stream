from typing import Dict, List, Any

ACHIEVEMENTS = [
    {
        "id": "first_step",
        "title": "First Step",
        "description": "Send your first message",
        "xp_reward": 50,
        "condition": lambda stats: stats.get("total_messages", 0) >= 1
    },
    {
        "id": "curious_mind",
        "title": "Curious Mind",
        "description": "Send 10 messages",
        "xp_reward": 100,
        "condition": lambda stats: stats.get("total_messages", 0) >= 10
    }
]

# In-memory storage for user stats (simulating a DB)
_USER_DB = {}

def get_user_stats(user_id: str) -> Dict[str, Any]:
    if user_id not in _USER_DB:
        _USER_DB[user_id] = {
            "user_id": user_id,
            "xp": 0,
            "level": 1,
            "achievements": [],
            "total_messages": 0
        }
    return _USER_DB[user_id]

def update_user_stats(user_id: str, stats: Dict[str, Any]) -> None:
    _USER_DB[user_id] = stats

class EngagementManager:
    def calculate_level(self, xp: int) -> int:
        return 1 + (xp // 100)

    def get_next_level_progress(self, xp: int) -> float:
        return (xp % 100) / 100.0

    def log_activity(self, user_id: str, activity_type: str) -> Dict[str, Any]:
        stats = get_user_stats(user_id)
        level_up = False
        new_achievements = []

        previous_level = stats["level"]

        if activity_type == "message_sent":
            stats["total_messages"] += 1
            stats["xp"] += 10 # Base XP for sending a message

        # Check achievements
        current_achievement_ids = {a["id"] for a in stats["achievements"]}
        for achievement in ACHIEVEMENTS:
            if achievement["id"] not in current_achievement_ids:
                if achievement["condition"](stats):
                    stats["xp"] += achievement["xp_reward"]
                    stats["achievements"].append(achievement)
                    new_achievements.append(achievement)

        # Update level
        stats["level"] = self.calculate_level(stats["xp"])
        if stats["level"] > previous_level:
            level_up = True

        update_user_stats(user_id, stats)

        return {
            "stats": stats,
            "level_up": level_up,
            "new_achievements": new_achievements
        }

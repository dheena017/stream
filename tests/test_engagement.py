import unittest
from unittest.mock import MagicMock, patch
from ui.engagement import EngagementManager, ACHIEVEMENTS

class TestEngagementManager(unittest.TestCase):
    def setUp(self):
        self.manager = EngagementManager()

    def test_calculate_level(self):
        self.assertEqual(self.manager.calculate_level(0), 1)
        self.assertEqual(self.manager.calculate_level(99), 1)
        self.assertEqual(self.manager.calculate_level(100), 2)
        self.assertEqual(self.manager.calculate_level(150), 2)
        self.assertEqual(self.manager.calculate_level(200), 3)

    def test_get_next_level_progress(self):
        self.assertEqual(self.manager.get_next_level_progress(0), 0.0)
        self.assertEqual(self.manager.get_next_level_progress(50), 0.5)
        self.assertEqual(self.manager.get_next_level_progress(100), 0.0)
        self.assertEqual(self.manager.get_next_level_progress(125), 0.25)

    @patch('ui.engagement.get_user_stats')
    @patch('ui.engagement.update_user_stats')
    def test_log_activity_message_sent(self, mock_update, mock_get):
        # Initial state: Level 1, 0 XP, 0 messages
        mock_get.return_value = {
            'user_id': 'test_user',
            'xp': 0,
            'level': 1,
            'achievements': [],
            'total_messages': 0
        }

        result = self.manager.log_activity('test_user', 'message_sent')

        # Check stats update
        self.assertEqual(result['stats']['total_messages'], 1)
        self.assertEqual(result['stats']['xp'], 10 + 50) # 10 for msg + 50 for 'First Step' achievement

        # XP: 10 (msg) + 50 (achievement) = 60. Level 1.
        # previous_level was 1. So level_up should be False.
        self.assertFalse(result['level_up'])

        self.assertEqual(len(result['new_achievements']), 1)
        self.assertEqual(result['new_achievements'][0]['id'], 'first_step')

        mock_update.assert_called_once()

    @patch('ui.engagement.get_user_stats')
    @patch('ui.engagement.update_user_stats')
    def test_log_activity_level_up(self, mock_update, mock_get):
        # Initial state: Level 1, 90 XP, 9 messages
        # Sending 1 message -> +10 XP = 100 XP -> Level 2.
        # Also triggers "Curious Mind" (10 messages) -> +100 XP = 200 XP -> Level 3.

        mock_get.return_value = {
            'user_id': 'test_user',
            'xp': 90,
            'level': 1,
            'achievements': [{'id': 'first_step'}], # Already has first step
            'total_messages': 9
        }

        result = self.manager.log_activity('test_user', 'message_sent')

        # Total messages: 10
        self.assertEqual(result['stats']['total_messages'], 10)

        # XP: 90 + 10 (msg) = 100.
        # Achievements: "Curious Mind" (>=10 msgs) unlocked -> +100 XP.
        # Total XP: 200.
        self.assertEqual(result['stats']['xp'], 200)

        # Level: 200 XP -> Level 3 (1 + 200/100 = 3).
        self.assertEqual(result['stats']['level'], 3)

        self.assertTrue(result['level_up'])
        self.assertEqual(len(result['new_achievements']), 1)
        self.assertEqual(result['new_achievements'][0]['id'], 'curious_mind')

if __name__ == '__main__':
    unittest.main()

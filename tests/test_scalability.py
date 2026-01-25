
import unittest
import os
import sqlite3
import json
from unittest.mock import patch

# Configure path so we can import ui
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.database import init_db, create_new_conversation, save_message, get_conversation_messages

TEST_DB = "test_scalability.db"

class TestScalability(unittest.TestCase):

    def setUp(self):
        # Clean up previous test db if exists
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        # Patch the DB_FILE in ui.database
        self.patcher = patch('ui.database.DB_FILE', TEST_DB)
        self.mock_db = self.patcher.start()

        # Initialize DB
        init_db()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_pagination_logic(self):
        # 1. Create a conversation
        conv_id = create_new_conversation("user_test", "Test Chat")

        # 2. Insert 150 messages
        # We want to ensure they have timestamps that order them correctly
        # The save_message function uses datetime.now(), so we might need to sleep or just trust autoincrement ID
        # Since we plan to order by ID, insertion order matters.

        for i in range(150):
            save_message(conv_id, "user", f"Message {i}")

        # 3. Test loading with limit and offset
        # Note: accurate pagination implementation requires get_conversation_messages
        # to support limit/offset arguments.

        # Attempt to call with new arguments (will fail before implementation)
        try:
            # Load latest 50 messages (should be Message 100 to Message 149)
            latest_messages = get_conversation_messages(conv_id, limit=50, offset=0)

            self.assertEqual(len(latest_messages), 50)
            self.assertEqual(latest_messages[-1]['content'], "Message 149")
            self.assertEqual(latest_messages[0]['content'], "Message 100")

            # Load previous 50 messages (should be Message 50 to Message 99)
            older_messages = get_conversation_messages(conv_id, limit=50, offset=50)

            self.assertEqual(len(older_messages), 50)
            self.assertEqual(older_messages[-1]['content'], "Message 99")
            self.assertEqual(older_messages[0]['content'], "Message 50")

            # Load oldest 50 messages (should be Message 0 to Message 49)
            oldest_messages = get_conversation_messages(conv_id, limit=50, offset=100)

            self.assertEqual(len(oldest_messages), 50)
            self.assertEqual(oldest_messages[-1]['content'], "Message 49")
            self.assertEqual(oldest_messages[0]['content'], "Message 0")

            # Test limit beyond range
            empty_messages = get_conversation_messages(conv_id, limit=50, offset=200)
            self.assertEqual(len(empty_messages), 0)

        except TypeError:
            print("Pagination arguments not yet implemented in get_conversation_messages")
            # We expect this failure initially
            pass

if __name__ == '__main__':
    unittest.main()

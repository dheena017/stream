import pytest
import sqlite3
import os
from ui.database import init_db, create_new_conversation, save_message, delete_user_data, DB_FILE

def test_delete_user_data():
    # Setup
    test_db = "test_chat_history.db"
    # Monkeypatch DB_FILE in ui.database module for this test?
    # Since DB_FILE is imported, we can't easily patch it unless we reload or patch where it's used.
    # However, DB_FILE is a global in ui.database.
    # Let's try to patch it by modifying the module attribute.

    import ui.database
    original_db_file = ui.database.DB_FILE
    ui.database.DB_FILE = test_db

    if os.path.exists(test_db):
        os.remove(test_db)

    try:
        init_db()

        user1 = "user1"
        user2 = "user2"

        # Create data for user1
        conv1 = create_new_conversation(user1, "User1 Chat")
        save_message(conv1, "user", "Hello user1")

        # Create data for user2
        conv2 = create_new_conversation(user2, "User2 Chat")
        save_message(conv2, "user", "Hello user2")

        # Verify data exists
        conn = sqlite3.connect(test_db)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM conversations")
        assert c.fetchone()[0] == 2
        c.execute("SELECT count(*) FROM messages")
        assert c.fetchone()[0] == 2
        conn.close()

        # Delete user1 data
        delete_user_data(user1)

        # Verify user1 data is gone
        conn = sqlite3.connect(test_db)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM conversations")
        assert c.fetchone()[0] == 1 # Only user2 left
        c.execute("SELECT count(*) FROM conversations WHERE user_id = ?", (user1,))
        assert c.fetchone()[0] == 0

        c.execute("SELECT count(*) FROM messages")
        assert c.fetchone()[0] == 1 # Only user2 message left

        # Check user2 data is intact
        c.execute("SELECT count(*) FROM conversations WHERE user_id = ?", (user2,))
        assert c.fetchone()[0] == 1

        conn.close()

    finally:
        # Cleanup
        if os.path.exists(test_db):
            os.remove(test_db)
        ui.database.DB_FILE = original_db_file

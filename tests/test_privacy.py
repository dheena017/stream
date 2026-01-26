import pytest
import os
import json
import sqlite3
import tempfile
from datetime import datetime, timedelta
from ui.database import (
    EncryptionManager, save_message, get_conversation_messages,
    create_new_conversation, delete_user_data, cleanup_user_messages,
    init_db
)
from ui.auth import delete_user, save_user_credentials, load_user_credentials

# Setup mocks/fixtures
@pytest.fixture
def temp_env(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_chat.db")
        key_path = os.path.join(tmpdir, "test_secret.key")
        users_path = os.path.join(tmpdir, "test_users.json")

        monkeypatch.setattr("ui.database.DB_FILE", db_path)
        monkeypatch.setattr("ui.database.KEY_FILE", key_path)

        # Mock auth functions to use temp file
        def mock_load():
            if os.path.exists(users_path):
                with open(users_path, 'r') as f: return json.load(f)
            return {}

        def mock_save(users):
            with open(users_path, 'w') as f: json.dump(users, f)
            return True

        monkeypatch.setattr("ui.auth.load_user_credentials", mock_load)
        monkeypatch.setattr("ui.auth.save_user_credentials", mock_save)

        # Initialize
        init_db()
        # Reset cipher to ensure new key is used
        EncryptionManager._cipher = None

        yield tmpdir

def test_encryption_on_disk(temp_env):
    """Verify that data is stored encrypted in the database."""
    user_id = "testuser"
    conv_id = create_new_conversation(user_id)
    secret_msg = "This is a secret message"

    save_message(conv_id, "user", secret_msg)

    # Read raw DB
    conn = sqlite3.connect(os.path.join(temp_env, "test_chat.db"))
    c = conn.cursor()
    c.execute("SELECT content FROM messages WHERE conversation_id=?", (conv_id,))
    row = c.fetchone()
    conn.close()

    raw_content = row[0]
    assert raw_content != secret_msg
    assert "This is a secret message" not in raw_content
    assert len(raw_content) > len(secret_msg) # Encrypted is usually longer

    # Verify decryption via API
    msgs = get_conversation_messages(conv_id)
    assert msgs[0]["content"] == secret_msg

def test_user_deletion(temp_env):
    """Verify user deletion removes all data."""
    # Setup user
    users_path = os.path.join(temp_env, "test_users.json")
    users = {"del_user": {"password": "hash", "email": "a@b.com"}}
    with open(users_path, 'w') as f: json.dump(users, f)

    # Create chat data
    conv_id = create_new_conversation("del_user")
    save_message(conv_id, "user", "msg1")

    # Verify data exists
    assert len(get_conversation_messages(conv_id)) == 1

    # Delete data
    delete_user_data("del_user")

    # Verify DB empty for user (messages deleted)
    assert len(get_conversation_messages(conv_id)) == 0

    # Verify conversation record deleted
    conn = sqlite3.connect(os.path.join(temp_env, "test_chat.db"))
    c = conn.cursor()
    c.execute("SELECT count(*) FROM conversations WHERE user_id='del_user'")
    assert c.fetchone()[0] == 0
    conn.close()

    # Delete user account
    delete_user("del_user")
    with open(users_path, 'r') as f:
        data = json.load(f)
    assert "del_user" not in data

def test_retention_cleanup(temp_env):
    """Verify old messages are cleaned up for specific user."""
    # User 1
    conv_id1 = create_new_conversation("ret_user1")
    # User 2
    conv_id2 = create_new_conversation("ret_user2")

    conn = sqlite3.connect(os.path.join(temp_env, "test_chat.db"))
    c = conn.cursor()
    old_date = datetime.now() - timedelta(days=31)

    # Insert old message for User 1
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conv_id1, "user", "old_msg1", "{}", old_date))
    # Insert old message for User 2
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conv_id2, "user", "old_msg2", "{}", old_date))

    conn.commit()
    conn.close()

    # Cleanup User 1 (30 days)
    cleanup_user_messages("ret_user1", 30)

    # Verify User 1 message deleted, User 2 message remains
    conn = sqlite3.connect(os.path.join(temp_env, "test_chat.db"))
    c = conn.cursor()
    c.execute("SELECT count(*) FROM messages WHERE conversation_id=?", (conv_id1,))
    assert c.fetchone()[0] == 0

    c.execute("SELECT count(*) FROM messages WHERE conversation_id=?", (conv_id2,))
    assert c.fetchone()[0] == 1
    conn.close()

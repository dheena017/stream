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
=======
import sys
from unittest.mock import MagicMock, patch
import os
import json
import sqlite3

# Mock streamlit before importing modules that use it
sys.modules['streamlit'] = MagicMock()

from ui.privacy import PrivacyManager
from ui.database import save_message, get_conversation_messages, init_db, delete_all_user_data, get_all_user_data, create_new_conversation

@pytest.fixture
def temp_db():
    # Use a temporary DB file
    test_db = "test_chat_history.db"

    # Monkeypatch DB_FILE in ui.database
    with patch('ui.database.DB_FILE', test_db):
        # Init DB
        conn = sqlite3.connect(test_db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id TEXT PRIMARY KEY, user_id TEXT, title TEXT,
                      created_at TIMESTAMP, updated_at TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT,
                      role TEXT, content TEXT, meta_json TEXT, timestamp TIMESTAMP)''')
        conn.commit()
        conn.close()

        yield test_db

        # Cleanup
        if os.path.exists(test_db):
            os.remove(test_db)

        # Also clean up the key file created by PrivacyManager if exists in current dir
        if os.path.exists("secret.key"):
            # We don't delete it here because it might be the real one,
            # but for tests we might want to mock the key file location too.
            # For now, we assume it's fine.
            pass

@pytest.fixture
def privacy_manager():
    # Ensure fresh instance
    PrivacyManager._instance = None
    pm = PrivacyManager()
    return pm

def test_encryption_decryption(privacy_manager):
    original = "Secret Message"
    encrypted = privacy_manager.encrypt(original)
    assert encrypted != original
    decrypted = privacy_manager.decrypt(encrypted)
    assert decrypted == original

def test_database_integration(temp_db, privacy_manager):
    user_id = "test_user"
    conv_id = create_new_conversation(user_id, "Test Chat")

    content = "Confidential Data"
    save_message(conv_id, "user", content)

    # Verify raw DB has encrypted content
    conn = sqlite3.connect(temp_db)
    c = conn.cursor()
    c.execute("SELECT content FROM messages WHERE conversation_id=?", (conv_id,))
    raw_content = c.fetchone()[0]
    conn.close()

    assert raw_content != content
    assert raw_content.startswith("gAAAA") # Fernet prefix

    # Verify retrieval decrypts it
    messages = get_conversation_messages(conv_id)
    assert len(messages) == 1
    assert messages[0]['content'] == content

def test_delete_all_user_data(temp_db):
    user_id = "test_user_del"
    conv_id = create_new_conversation(user_id, "Chat to Delete")
    save_message(conv_id, "user", "msg")

    delete_all_user_data(user_id)

    conn = sqlite3.connect(temp_db)
    c = conn.cursor()
    c.execute("SELECT count(*) FROM conversations WHERE user_id=?", (user_id,))
    count_conv = c.fetchone()[0]
    c.execute("SELECT count(*) FROM messages WHERE conversation_id=?", (conv_id,))
    count_msg = c.fetchone()[0]
    conn.close()

    assert count_conv == 0
    assert count_msg == 0

def test_export_data(temp_db):
    user_id = "test_user_export"
    conv_id = create_new_conversation(user_id, "Chat Export")
    content = "Exportable Content"
    save_message(conv_id, "user", content)

    data = get_all_user_data(user_id)

    assert data['user_id'] == user_id
    assert len(data['conversations']) == 1
    assert data['conversations'][0]['messages'][0]['content'] == content
>>>>>>> origin/privacy-compliance-updates-15433171418981572602
=======
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
>>>>>>> origin/privacy-compliance-updates-6913709404570951522

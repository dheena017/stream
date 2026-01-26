import os
import sqlite3
import sys
from unittest.mock import MagicMock, patch

import pytest

# Mock streamlit before importing modules that use it
sys.modules["streamlit"] = MagicMock()

from ui.database import (
    create_new_conversation,
    delete_all_user_data,
    get_all_user_data,
    get_conversation_messages,
    save_message,
)
from ui.privacy import PrivacyManager


@pytest.fixture
def temp_db():
    # Use a temporary DB file
    test_db = "test_chat_history.db"

    # Monkeypatch DB_FILE in ui.database
    with patch("ui.database.DB_FILE", test_db):
        # Init DB
        conn = sqlite3.connect(test_db)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS conversations
                     (id TEXT PRIMARY KEY, user_id TEXT, title TEXT,
                      created_at TIMESTAMP, updated_at TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT,
                      role TEXT, content TEXT, meta_json TEXT, timestamp TIMESTAMP)""")
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
    assert raw_content.startswith("gAAAA")  # Fernet prefix

    # Verify retrieval decrypts it
    messages = get_conversation_messages(conv_id)
    assert len(messages) == 1
    assert messages[0]["content"] == content


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

    assert data["user_id"] == user_id
    assert len(data["conversations"]) == 1
    assert data["conversations"][0]["messages"][0]["content"] == content

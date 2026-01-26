import sqlite3
import os
import json
import uuid
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import logging

DB_FILE = "chat_history.db"
KEY_FILE = "secret.key"

class EncryptionManager:
    _cipher = None

    @classmethod
    def get_cipher(cls):
        if cls._cipher is None:
            env_key = os.environ.get("ENCRYPTION_KEY")
            if env_key:
                cls._cipher = Fernet(env_key.encode('utf-8'))
            elif not os.path.exists(KEY_FILE):
                key = Fernet.generate_key()
                with open(KEY_FILE, "wb") as f:
                    f.write(key)
                cls._cipher = Fernet(key)
            else:
                with open(KEY_FILE, "rb") as f:
                    key = f.read()
                cls._cipher = Fernet(key)
        return cls._cipher

    @classmethod
    def encrypt(cls, data: str) -> str:
        if not data:
            return ""
        cipher = cls.get_cipher()
        return cipher.encrypt(data.encode('utf-8')).decode('utf-8')

    @classmethod
    def decrypt(cls, token: str) -> str:
        if not token:
            return ""
        try:
            cipher = cls.get_cipher()
            return cipher.decrypt(token.encode('utf-8')).decode('utf-8')
        except Exception as e:
            logging.error(f"Decryption failed: {e}")
            return token # Return original if decryption fails (e.g. unencrypted data)

def init_db():
    """Initialize the database tables."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id TEXT PRIMARY KEY, user_id TEXT, title TEXT,
                  created_at TIMESTAMP, updated_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT,
                  role TEXT, content TEXT, meta_json TEXT, timestamp TIMESTAMP)''')
    conn.commit()
    conn.close()

def create_new_conversation(user_id: str, title: str = "New Chat") -> str:
    """Create a new conversation and return its ID."""
    conv_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (id, user_id, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
              (conv_id, user_id, title, now, now))
    conn.commit()
    conn.close()
    return conv_id

def save_message(conversation_id: str, role: str, content: str, meta_json: str = "{}"):
    """Save a message to the database with encrypted content."""
    encrypted_content = EncryptionManager.encrypt(content)
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, encrypted_content, meta_json, now))
    # Update conversation timestamp
    c.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()

def get_conversation_messages(conversation_id: str, limit: int = None, offset: int = 0):
    """Retrieve messages for a conversation, decrypting them."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id ASC"
    if limit:
        query += f" LIMIT {limit} OFFSET {offset}"

    c.execute(query, (conversation_id,))
    rows = c.fetchall()
    conn.close()

    messages = []
    for role, content, meta, timestamp in rows:
        decrypted_content = EncryptionManager.decrypt(content)
        messages.append({
            "role": role,
            "content": decrypted_content,
            "meta_json": meta,
            "timestamp": timestamp
        })
    return messages

def delete_user_data(user_id: str):
    """Delete all data associated with a user (Data Minimization)."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Get all conversation IDs for the user
    c.execute("SELECT id FROM conversations WHERE user_id = ?", (user_id,))
    conv_ids = [row[0] for row in c.fetchall()]

    if conv_ids:
        # Delete messages for these conversations
        placeholders = ','.join(['?'] * len(conv_ids))
        c.execute(f"DELETE FROM messages WHERE conversation_id IN ({placeholders})", conv_ids)

        # Delete conversations
        c.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

def cleanup_user_messages(user_id: str, retention_days: int):
    """Delete messages older than the retention period for a specific user."""
    cutoff_date = (datetime.now() - timedelta(days=retention_days)).isoformat()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Get user's conversations
    c.execute("SELECT id FROM conversations WHERE user_id = ?", (user_id,))
    conv_ids = [row[0] for row in c.fetchall()]

    if conv_ids:
        placeholders = ','.join(['?'] * len(conv_ids))
        c.execute(f"DELETE FROM messages WHERE conversation_id IN ({placeholders}) AND timestamp < ?",
                  conv_ids + [cutoff_date])

    conn.commit()
    conn.close()

def get_all_user_data(user_id: str) -> dict:
    """Export all data for a user (Data Portability)."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT id, title, created_at, updated_at FROM conversations WHERE user_id = ?", (user_id,))
    conversations = c.fetchall()

    export_data = {
        "user_id": user_id,
        "conversations": [],
        "exported_at": str(datetime.now())
    }

    for conv in conversations:
        conv_id, title, created, updated = conv
        msgs = get_conversation_messages(conv_id) # Reuse this to handle decryption
        export_data["conversations"].append({
            "id": conv_id,
            "title": title,
            "created_at": created,
            "updated_at": updated,
            "messages": msgs
        })

    conn.close()
    return export_data

import sqlite3
import json
import logging
from datetime import datetime
import uuid
from typing import List, Dict, Optional, Tuple, Any
from ui.privacy import PrivacyManager

DB_FILE = "chat_history.db"
logger = logging.getLogger(__name__)

def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # conversations: id, user_id, title, created_at, updated_at
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id TEXT PRIMARY KEY, user_id TEXT, title TEXT, 
                      created_at TIMESTAMP, updated_at TIMESTAMP)''')
        
        # messages: id, conversation_id, role, content, meta_json, timestamp
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT, 
                      role TEXT, content TEXT, meta_json TEXT, timestamp TIMESTAMP)''')
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Database init error: {e}")

def create_new_conversation(user_id: str, title: str = "New Chat") -> str:
    conversation_id = str(uuid.uuid4())
    save_conversation_metadata(conversation_id, user_id, title)
    return conversation_id

def save_conversation_metadata(conversation_id: str, user_id: str, title: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()
    # Insert or Ignore
    c.execute("INSERT OR IGNORE INTO conversations (id, user_id, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, user_id, title, now, now))
    # Update updated_at if exists
    c.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()

def save_message(conversation_id: str, role: str, content: str, meta: Dict = None):
    if meta is None: meta = {}

    # Encrypt content
    pm = PrivacyManager()
    encrypted_content = pm.encrypt(content)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()
    
    # Ensure raw content is saved, meta handles images/files references
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, encrypted_content, json.dumps(meta), now))
    
    # Update conversation timestamp
    c.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()

def get_user_conversations(user_id: str) -> List[Tuple]:
    """Returns list of (id, title, updated_at)"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, updated_at FROM conversations WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_conversation_messages(conversation_id: str) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conversation_id,))
    rows = c.fetchall()
    conn.close()
    
    pm = PrivacyManager()
    messages = []
    for r in rows:
        # Decrypt content
        decrypted_content = pm.decrypt(r[1])

        msg = {
            "role": r[0],
            "content": decrypted_content,
            "timestamp": str(r[3])
        }
        if r[2]:
            try:
                meta = json.loads(r[2])
                msg.update(meta)
            except: pass
        messages.append(msg)
    return messages

def delete_all_user_data(user_id: str):
    """Delete all conversations and messages for a user."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Get all conversation IDs for this user
    c.execute("SELECT id FROM conversations WHERE user_id = ?", (user_id,))
    conv_ids = [row[0] for row in c.fetchall()]

    if conv_ids:
        # Delete messages for these conversations
        placeholders = ','.join('?' for _ in conv_ids)
        c.execute(f"DELETE FROM messages WHERE conversation_id IN ({placeholders})", conv_ids)

        # Delete conversations
        c.execute(f"DELETE FROM conversations WHERE id IN ({placeholders})", conv_ids)

    conn.commit()
    conn.close()

def get_all_user_data(user_id: str) -> Dict[str, Any]:
    """Retrieve all data for a user (conversations and messages)."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    data = {"user_id": user_id, "conversations": []}

    # Get conversations
    c.execute("SELECT id, title, created_at, updated_at FROM conversations WHERE user_id = ? ORDER BY created_at", (user_id,))
    conversations = c.fetchall()

    pm = PrivacyManager()

    for conv in conversations:
        conv_id = conv[0]
        conv_data = {
            "id": conv_id,
            "title": conv[1],
            "created_at": str(conv[2]),
            "updated_at": str(conv[3]),
            "messages": []
        }

        # Get messages for this conversation
        c.execute("SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id", (conv_id,))
        messages = c.fetchall()

        for msg in messages:
            # Decrypt content
            decrypted_content = pm.decrypt(msg[1])

            msg_data = {
                "role": msg[0],
                "content": decrypted_content,
                "timestamp": str(msg[3])
            }
            if msg[2]:
                try:
                    msg_data["meta"] = json.loads(msg[2])
                except: pass

            conv_data["messages"].append(msg_data)

        data["conversations"].append(conv_data)

    conn.close()
    return data

def delete_conversation(conversation_id: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    c.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    conn.commit()
    conn.close()

def update_conversation_title(conversation_id: str, title: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE conversations SET title = ? WHERE id = ?", (title, conversation_id))
    conn.commit()
    conn.close()

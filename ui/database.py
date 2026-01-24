import sqlite3
import json
import logging
from datetime import datetime
import uuid
from typing import List, Dict, Optional, Tuple

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
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()
    
    # Ensure raw content is saved, meta handles images/files references
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, content, json.dumps(meta), now))
    
    # Update conversation timestamp
    c.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()

def get_user_conversations(user_id: str) -> List[Tuple[str, str, str]]:
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
    
    messages = []
    for r in rows:
        msg = {
            "role": r[0],
            "content": r[1],
            "timestamp": str(r[3])
        }
        if r[2]:
            try:
                meta = json.loads(r[2])
                msg.update(meta)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in message: {e}")
        messages.append(msg)
    return messages

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

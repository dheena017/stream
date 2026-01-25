import sqlite3
import json
import logging
from datetime import datetime, timedelta
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

        # user_stats: user_id, xp, level, messages_sent, streak_days, last_active_date, achievements_json
        c.execute('''CREATE TABLE IF NOT EXISTS user_stats
                     (user_id TEXT PRIMARY KEY, xp INTEGER, level INTEGER,
                      messages_sent INTEGER, streak_days INTEGER, last_active_date TEXT,
                      achievements_json TEXT)''')

        # feedback: id, user_id, message_id, rating, comment, timestamp
        c.execute('''CREATE TABLE IF NOT EXISTS feedback
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, message_id TEXT,
                      rating INTEGER, comment TEXT, timestamp TIMESTAMP)''')

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
            except: pass
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

# --- Engagement & Feedback Functions ---

def init_user_stats(user_id: str):
    """Initialize stats for a new user"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # xp, level, messages_sent, streak_days, last_active_date, achievements_json
    c.execute("INSERT OR IGNORE INTO user_stats VALUES (?, ?, ?, ?, ?, ?, ?)",
              (user_id, 0, 1, 0, 0, None, "[]"))
    conn.commit()
    conn.close()

def get_user_stats(user_id: str) -> Dict:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT xp, level, messages_sent, streak_days, last_active_date, achievements_json FROM user_stats WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "xp": row[0],
            "level": row[1],
            "messages_sent": row[2],
            "streak_days": row[3],
            "last_active_date": row[4],
            "achievements": json.loads(row[5]) if row[5] else []
        }
    else:
        # Auto-init if missing
        init_user_stats(user_id)
        return {
            "xp": 0, "level": 1, "messages_sent": 0,
            "streak_days": 0, "last_active_date": None, "achievements": []
        }

def update_user_stats(user_id: str, xp: int = None, level: int = None,
                      messages_sent: int = None, streak_days: int = None,
                      last_active_date: str = None, achievements: List[str] = None):
    """Update specific fields for a user"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    updates = []
    params = []

    if xp is not None:
        updates.append("xp = ?")
        params.append(xp)
    if level is not None:
        updates.append("level = ?")
        params.append(level)
    if messages_sent is not None:
        updates.append("messages_sent = ?")
        params.append(messages_sent)
    if streak_days is not None:
        updates.append("streak_days = ?")
        params.append(streak_days)
    if last_active_date is not None:
        updates.append("last_active_date = ?")
        params.append(last_active_date)
    if achievements is not None:
        updates.append("achievements_json = ?")
        params.append(json.dumps(achievements))

    if updates:
        query = f"UPDATE user_stats SET {', '.join(updates)} WHERE user_id = ?"
        params.append(user_id)
        c.execute(query, tuple(params))
        conn.commit()

    conn.close()

def get_all_user_stats() -> List[Dict]:
    """Get stats for all users (for leaderboard)"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, xp, level, messages_sent, streak_days, achievements_json FROM user_stats ORDER BY xp DESC")
    rows = c.fetchall()
    conn.close()

    stats = []
    for r in rows:
        stats.append({
            "user_id": r[0],
            "xp": r[1],
            "level": r[2],
            "messages_sent": r[3],
            "streak_days": r[4],
            "achievements": json.loads(r[5]) if r[5] else []
        })
    return stats

def save_feedback(user_id: str, rating: int, comment: str, message_id: str = None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (user_id, message_id, rating, comment, timestamp) VALUES (?, ?, ?, ?, ?)",
              (user_id, message_id, rating, comment, datetime.now()))
    conn.commit()
    conn.close()

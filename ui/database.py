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

        # user_stats: user_id, xp, level, achievements_json, total_messages, last_active
        c.execute('''CREATE TABLE IF NOT EXISTS user_stats
                     (user_id TEXT PRIMARY KEY, xp INTEGER DEFAULT 0, level INTEGER DEFAULT 1,
                      achievements_json TEXT DEFAULT '[]', total_messages INTEGER DEFAULT 0,
                      last_active TIMESTAMP)''')

        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Database init error: {e}")

def get_user_stats(user_id: str) -> Dict:
    """Get user stats, initialize if not exists"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT xp, level, achievements_json, total_messages, last_active FROM user_stats WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if not row:
        now = datetime.now()
        c.execute("INSERT INTO user_stats (user_id, xp, level, achievements_json, total_messages, last_active) VALUES (?, 0, 1, '[]', 0, ?)",
                  (user_id, now))
        conn.commit()
        stats = {
            "xp": 0, "level": 1, "achievements": [],
            "total_messages": 0, "last_active": now
        }
    else:
        stats = {
            "xp": row[0],
            "level": row[1],
            "achievements": json.loads(row[2]),
            "total_messages": row[3],
            "last_active": row[4]
        }

    conn.close()
    return stats

def update_user_stats(user_id: str, stats: Dict):
    """Update user stats"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()
    c.execute("""UPDATE user_stats
                 SET xp = ?, level = ?, achievements_json = ?, total_messages = ?, last_active = ?
                 WHERE user_id = ?""",
              (stats['xp'], stats['level'], json.dumps(stats['achievements']),
               stats['total_messages'], now, user_id))
    conn.commit()
    conn.close()

def get_leaderboard(limit: int = 5) -> List[Dict]:
    """Get top users by XP"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, xp, level, total_messages FROM user_stats ORDER BY xp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()

    leaderboard = []
    for r in rows:
        leaderboard.append({
            "user_id": r[0],
            "xp": r[1],
            "level": r[2],
            "total_messages": r[3]
        })
    return leaderboard

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

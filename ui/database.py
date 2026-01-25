<<<<<<< HEAD
<<<<<<< HEAD
import json
import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple

DB_FILE = "chat_history.db"
logger = logging.getLogger(__name__)


def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # conversations: id, user_id, title, created_at, updated_at
        c.execute(
            """CREATE TABLE IF NOT EXISTS conversations
                     (id TEXT PRIMARY KEY, user_id TEXT, title TEXT, 
                      created_at TIMESTAMP, updated_at TIMESTAMP)"""
        )

        # messages: id, conversation_id, role, content, meta_json, timestamp
        c.execute(
            """CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT, 
                      role TEXT, content TEXT, meta_json TEXT, timestamp TIMESTAMP)''')
<<<<<<< HEAD

        # Indexes for performance
        c.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_updated ON conversations(user_id, updated_at)")

=======

        # feedback: id, user_id, rating, category, comment, created_at
        c.execute('''CREATE TABLE IF NOT EXISTS feedback
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
                      rating INTEGER, category TEXT, comment TEXT, created_at TIMESTAMP)''')
>>>>>>> 89c4a85 (Feedback: [integrations])
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
    c.execute(
        "INSERT OR IGNORE INTO conversations (id, user_id, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (conversation_id, user_id, title, now, now),
    )
    # Update updated_at if exists
    c.execute(
        "UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id)
    )
    conn.commit()
    conn.close()


def save_message(conversation_id: str, role: str, content: str, meta: Dict = None):
    if meta is None:
        meta = {}
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()

    # Ensure raw content is saved, meta handles images/files references
    c.execute(
        "INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
        (conversation_id, role, content, json.dumps(meta), now),
    )

    # Update conversation timestamp
    c.execute(
        "UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id)
    )
    conn.commit()
    conn.close()


def get_user_conversations(user_id: str) -> List[Tuple]:
    """Returns list of (id, title, updated_at)"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT id, title, updated_at FROM conversations WHERE user_id = ? ORDER BY updated_at DESC",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()
    return rows


def get_conversation_messages(conversation_id: str) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id ASC",
        (conversation_id,),
    )
    rows = c.fetchall()
    conn.close()

    messages = []
    for r in rows:
        msg = {"role": r[0], "content": r[1], "timestamp": str(r[3])}
        if r[2]:
            try:
                meta = json.loads(r[2])
                msg.update(meta)
            except:
                pass
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
    c.execute(
        "UPDATE conversations SET title = ? WHERE id = ?", (title, conversation_id)
    )
    conn.commit()
    conn.close()
<<<<<<< HEAD
=======
import sqlite3
import json
import logging
import os
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Optional, Tuple
from cryptography.fernet import Fernet

DB_FILE = "chat_history.db"
KEY_FILE = "secret.key"
logger = logging.getLogger(__name__)

class EncryptionManager:
    _cipher = None

    @classmethod
    def get_cipher(cls):
        if cls._cipher is None:
            if os.path.exists(KEY_FILE):
                with open(KEY_FILE, "rb") as f:
                    key = f.read()
            else:
                key = Fernet.generate_key()
                with open(KEY_FILE, "wb") as f:
                    f.write(key)
            cls._cipher = Fernet(key)
        return cls._cipher

    @classmethod
    def encrypt(cls, data: str) -> str:
        if not data: return ""
        try:
            return cls.get_cipher().encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data

    @classmethod
    def decrypt(cls, token: str) -> str:
        if not token: return ""
        try:
            return cls.get_cipher().decrypt(token.encode()).decode()
        except Exception:
            # Fallback for unencrypted legacy data
            return token

=======
import sqlite3
import json
import logging
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Optional, Tuple

DB_FILE = "chat_history.db"
logger = logging.getLogger(__name__)

>>>>>>> origin/engagement-features-5881933724913241534
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
<<<<<<< HEAD
=======

        # user_stats: user_id, xp, level, messages_sent, streak_days, last_active_date, achievements_json
        c.execute('''CREATE TABLE IF NOT EXISTS user_stats
                     (user_id TEXT PRIMARY KEY, xp INTEGER, level INTEGER,
                      messages_sent INTEGER, streak_days INTEGER, last_active_date TEXT,
                      achievements_json TEXT)''')

        # feedback: id, user_id, message_id, rating, comment, timestamp
        c.execute('''CREATE TABLE IF NOT EXISTS feedback
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, message_id TEXT,
                      rating INTEGER, comment TEXT, timestamp TIMESTAMP)''')

>>>>>>> origin/engagement-features-5881933724913241534
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

<<<<<<< HEAD
    # Encrypt content and meta
    encrypted_content = EncryptionManager.encrypt(content)
    encrypted_meta = EncryptionManager.encrypt(json.dumps(meta))

    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, encrypted_content, encrypted_meta, now))
=======
    # Ensure raw content is saved, meta handles images/files references
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, content, json.dumps(meta), now))
>>>>>>> origin/engagement-features-5881933724913241534

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
<<<<<<< HEAD
        # Decrypt content and meta
        decrypted_content = EncryptionManager.decrypt(r[1])
        decrypted_meta_json = EncryptionManager.decrypt(r[2]) if r[2] else "{}"

        msg = {
            "role": r[0],
            "content": decrypted_content,
            "timestamp": str(r[3])
        }
        if decrypted_meta_json:
            try:
                meta = json.loads(decrypted_meta_json)
=======
        msg = {
            "role": r[0],
            "content": r[1],
            "timestamp": str(r[3])
        }
        if r[2]:
            try:
                meta = json.loads(r[2])
>>>>>>> origin/engagement-features-5881933724913241534
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

<<<<<<< HEAD
def delete_user_data(user_id: str):
    """Delete all conversations and messages for a specific user."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Get all conversation IDs for the user
    c.execute("SELECT id FROM conversations WHERE user_id = ?", (user_id,))
    conv_ids = [row[0] for row in c.fetchall()]

    if conv_ids:
        # Delete messages for these conversations
        placeholders = ', '.join(['?'] * len(conv_ids))
        c.execute(f"DELETE FROM messages WHERE conversation_id IN ({placeholders})", conv_ids)

        # Delete conversations
        c.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()
    logger.info(f"Deleted data for user: {user_id}")

def cleanup_user_messages(user_id: str, days: int):
    """Delete messages older than the specified number of days for a specific user."""
    if days <= 0: return

    cutoff_date = datetime.now() - timedelta(days=days)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        DELETE FROM messages
        WHERE timestamp < ?
        AND conversation_id IN (SELECT id FROM conversations WHERE user_id = ?)
    """, (cutoff_date, user_id))

    deleted_count = c.rowcount
    conn.commit()
    conn.close()
    logger.info(f"Cleaned up {deleted_count} old messages for user {user_id}.")
>>>>>>> 8a352f7 (Privacy: [compliance updates])
=======


def save_feedback(user_id: str, rating: int, category: str, comment: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()
    c.execute("INSERT INTO feedback (user_id, rating, category, comment, created_at) VALUES (?, ?, ?, ?, ?)",
              (user_id, rating, category, comment, now))
    conn.commit()
    conn.close()


def get_recent_feedback(limit: int = 5) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, rating, category, comment, created_at FROM feedback ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()

    feedback = []
    for r in rows:
        feedback.append({
            "user_id": r[0],
            "rating": r[1],
            "category": r[2],
            "comment": r[3],
            "created_at": r[4]
        })
    return feedback
>>>>>>> 89c4a85 (Feedback: [integrations])
=======
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
>>>>>>> origin/engagement-features-5881933724913241534

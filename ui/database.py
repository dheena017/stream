<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import json
import logging
import sqlite3
import uuid
<<<<<<< HEAD
from datetime import datetime
from typing import Dict, List, Optional, Tuple
=======
from typing import List, Dict, Optional, Tuple, Any
from ui.privacy import PrivacyManager
>>>>>>> origin/privacy-compliance-updates-15433171418981572602

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
<<<<<<< HEAD
<<<<<<< HEAD

        # Indexes for performance
        c.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_updated ON conversations(user_id, updated_at)")

=======

        # feedback: id, user_id, rating, category, comment, created_at
        c.execute('''CREATE TABLE IF NOT EXISTS feedback
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
                      rating INTEGER, category TEXT, comment TEXT, created_at TIMESTAMP)''')
>>>>>>> 89c4a85 (Feedback: [integrations])
=======

        # feedback: id, user_id, category, rating, comment, timestamp
        c.execute('''CREATE TABLE IF NOT EXISTS feedback
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
                      category TEXT, rating INTEGER, comment TEXT, timestamp TIMESTAMP)''')
>>>>>>> origin/feedback-integration-17764393616523020931
=======

        # Performance Indexes
        c.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages (conversation_id)')

>>>>>>> origin/scalability-optimizations-5191153255901361581
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
<<<<<<< HEAD
    if meta is None:
        meta = {}
=======
    if meta is None: meta = {}

    # Encrypt content
    pm = PrivacyManager()
    encrypted_content = pm.encrypt(content)

>>>>>>> origin/privacy-compliance-updates-15433171418981572602
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()

    # Ensure raw content is saved, meta handles images/files references
<<<<<<< HEAD
    c.execute(
        "INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
        (conversation_id, role, content, json.dumps(meta), now),
    )

=======
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, encrypted_content, json.dumps(meta), now))
    
>>>>>>> origin/privacy-compliance-updates-15433171418981572602
    # Update conversation timestamp
    c.execute(
        "UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id)
    )
    conn.commit()
    conn.close()

<<<<<<< HEAD

def get_user_conversations(user_id: str) -> List[Tuple]:
=======
def get_user_conversations(user_id: str) -> List[Tuple[str, str, str]]:
>>>>>>> origin/code-review-security-fixes-5343699314450815094
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

<<<<<<< HEAD

def get_conversation_messages(conversation_id: str) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id ASC",
        (conversation_id,),
    )
    rows = c.fetchall()
    conn.close()
<<<<<<< HEAD
=======
def get_conversation_messages(conversation_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Fetch in reverse order (latest first) with limit/offset
    c.execute("""
        SELECT role, content, meta_json, timestamp
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (conversation_id, limit, offset))

    rows = c.fetchall()
    conn.close()
    
    # Reverse back to chronological order
    rows.reverse()
>>>>>>> origin/scalability-optimizations-5191153255901361581

    messages = []
    for r in rows:
        msg = {"role": r[0], "content": r[1], "timestamp": str(r[3])}
=======
    
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
>>>>>>> origin/privacy-compliance-updates-15433171418981572602
        if r[2]:
            try:
                meta = json.loads(r[2])
                msg.update(meta)
<<<<<<< HEAD
            except:
                pass
=======
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error in message: {e}")
>>>>>>> origin/code-review-security-fixes-5343699314450815094
        messages.append(msg)
    return messages

<<<<<<< HEAD
=======
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
>>>>>>> origin/privacy-compliance-updates-15433171418981572602

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
=======
import json
import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Dict, List, Tuple
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
=======
>>>>>>> origin/feedback-integration-7692380356929291134
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
import sqlite3
import json
import logging
from datetime import datetime
import uuid
from typing import List, Dict, Optional, Tuple
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-7692380356929291134
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2

DB_FILE = "chat_history.db"
logger = logging.getLogger(__name__)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-7692380356929291134
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======

        # user_stats: user_id, xp, level, achievements_json, total_messages, last_active
        c.execute('''CREATE TABLE IF NOT EXISTS user_stats
                     (user_id TEXT PRIMARY KEY, xp INTEGER DEFAULT 0, level INTEGER DEFAULT 1,
                      achievements_json TEXT DEFAULT '[]', total_messages INTEGER DEFAULT 0,
                      last_active TIMESTAMP)''')

>>>>>>> origin/engagement-features-3224553925721226807
=======

        # feedback: id, user_id, category, rating, comment, timestamp
        c.execute('''CREATE TABLE IF NOT EXISTS feedback
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
                      category TEXT, rating INTEGER, comment TEXT, timestamp TIMESTAMP)''')
>>>>>>> origin/feedback-integration-7692380356929291134
=======

        # Performance index for looking up messages by conversation
        c.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages (conversation_id)')

>>>>>>> origin/jules-3174636693196525980-404a41f2
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Database init error: {e}")

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
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

>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-7692380356929291134
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
    # Ensure raw content is saved, meta handles images/files references
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, content, json.dumps(meta), now))
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    # Ensure raw content is saved, meta handles images/files references
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, content, json.dumps(meta), now))
>>>>>>> origin/engagement-features-3224553925721226807
=======
    # Ensure raw content is saved, meta handles images/files references
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, content, json.dumps(meta), now))
>>>>>>> origin/feedback-integration-7692380356929291134
=======
    # Ensure raw content is saved, meta handles images/files references
    c.execute("INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
              (conversation_id, role, content, json.dumps(meta), now))
>>>>>>> origin/jules-3174636693196525980-404a41f2

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

<<<<<<< HEAD
def get_conversation_messages(conversation_id: str) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conversation_id,))
    rows = c.fetchall()
=======
def get_conversation_messages(conversation_id: str, limit: int = None, offset: int = 0) -> List[Dict]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if limit is not None:
        # Fetch latest N messages (descending ID) to support pagination
        # We need to reverse them later to return chronological order
        query = "SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id DESC LIMIT ? OFFSET ?"
        c.execute(query, (conversation_id, limit, offset))
        rows = c.fetchall()
        # Reverse rows to restore chronological order (ASC)
        rows = rows[::-1]
    else:
        # Default behavior: fetch all, chronological
        c.execute("SELECT role, content, meta_json, timestamp FROM messages WHERE conversation_id = ? ORDER BY id ASC", (conversation_id,))
        rows = c.fetchall()

>>>>>>> origin/jules-3174636693196525980-404a41f2
    conn.close()

    messages = []
    for r in rows:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-7692380356929291134
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
        msg = {
            "role": r[0],
            "content": r[1],
            "timestamp": str(r[3])
        }
        if r[2]:
            try:
                meta = json.loads(r[2])
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-7692380356929291134
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

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
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======

def save_feedback(user_id: str, category: str, rating: int, comment: str) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        now = datetime.now()
        c.execute("INSERT INTO feedback (user_id, category, rating, comment, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (user_id, category, rating, comment, now))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error saving feedback: {e}")
        return False
>>>>>>> origin/feedback-integration-17764393616523020931
=======

def save_feedback(user_id: str, category: str, rating: int, comment: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now()
    c.execute("INSERT INTO feedback (user_id, category, rating, comment, timestamp) VALUES (?, ?, ?, ?, ?)",
              (user_id, category, rating, comment, now))
    conn.commit()
    conn.close()
>>>>>>> origin/feedback-integration-7692380356929291134
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2

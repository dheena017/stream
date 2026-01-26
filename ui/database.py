import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "chat_history.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            rating INTEGER,
            comment TEXT,
            created_at DATETIME
        )
    """)
    conn.commit()
    conn.close()

def save_feedback(user_id, rating, comment):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO feedback (user_id, rating, comment, created_at) VALUES (?, ?, ?, ?)",
              (user_id, rating, comment, datetime.now()))
    conn.commit()
    conn.close()

def get_feedback_stats():
    conn = get_connection()
    try:
        # Check if table exists first to avoid pandas error
        c = conn.cursor()
        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedback'")
        if c.fetchone()[0] == 0:
            return pd.DataFrame()

        query = "SELECT * FROM feedback ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error fetching feedback stats: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

import sqlite3
from unittest.mock import patch

import pytest

from ui.database import init_db, save_feedback


@pytest.fixture
def mock_db_file(tmp_path):
    """Fixture to mock DB_FILE to use a temporary file."""
    db_file = tmp_path / "test_chat_history.db"
    with patch("ui.database.DB_FILE", str(db_file)):
        init_db()
        yield str(db_file)


def test_init_db_creates_feedback_table(mock_db_file):
    conn = sqlite3.connect(mock_db_file)
    c = conn.cursor()

    # Check if feedback table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
    assert c.fetchone() is not None

    # Check columns
    c.execute("PRAGMA table_info(feedback)")
    columns = [info[1] for info in c.fetchall()]
    assert "user_id" in columns
    assert "category" in columns
    assert "rating" in columns
    assert "comment" in columns
    assert "timestamp" in columns
    conn.close()


def test_save_feedback(mock_db_file):
    user_id = "test_user"
    category = "Bug Report"
    rating = 4
    comment = "This is a test comment."

    save_feedback(user_id, category, rating, comment)

    conn = sqlite3.connect(mock_db_file)
    c = conn.cursor()
    c.execute("SELECT user_id, category, rating, comment FROM feedback")
    row = c.fetchone()

    assert row[0] == user_id
    assert row[1] == category
    assert row[2] == rating
    assert row[3] == comment
    conn.close()

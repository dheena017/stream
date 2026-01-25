import pytest
import sqlite3
import os
<<<<<<< HEAD
from ui.database import init_db, save_feedback, get_recent_feedback, DB_FILE

# Use a test database file
TEST_DB = "test_feedback.db"

@pytest.fixture
def mock_db(monkeypatch):
    """Use a temporary database for testing."""
    # Monkeypatch the DB_FILE in ui.database
    monkeypatch.setattr("ui.database.DB_FILE", TEST_DB)

    # Initialize the DB
    init_db()

    yield

    # Cleanup
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_save_and_get_feedback(mock_db):
    """Test saving and retrieving feedback."""
    save_feedback("test_user", 5, "General", "Great app!")
    save_feedback("test_user_2", 4, "Bug Report", "Minor glitch.")

    feedback = get_recent_feedback(limit=5)

    assert len(feedback) == 2
    assert feedback[0]["comment"] == "Minor glitch."  # Most recent first
    assert feedback[1]["comment"] == "Great app!"
    assert feedback[0]["rating"] == 4
    assert feedback[1]["rating"] == 5

def test_get_recent_limit(mock_db):
    """Test the limit parameter."""
    for i in range(10):
        save_feedback(f"user_{i}", 5, "General", f"Comment {i}")

    feedback = get_recent_feedback(limit=3)
    assert len(feedback) == 3
    assert feedback[0]["comment"] == "Comment 9"
=======
from datetime import datetime
from ui.database import init_db, save_feedback, DB_FILE

def test_save_feedback():
    # Setup
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    init_db()

    # Test saving feedback
    assert save_feedback("test_user", "Bug", 5, "This is a test comment") == True

    # Verify in DB
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    row = c.fetchone()
    conn.close()

    assert row is not None
    assert row[1] == "test_user"
    assert row[2] == "Bug"
    assert row[3] == 5
    assert row[4] == "This is a test comment"

    # Cleanup
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

if __name__ == "__main__":
    test_save_feedback()
    print("Test passed!")
>>>>>>> origin/feedback-integration-17764393616523020931

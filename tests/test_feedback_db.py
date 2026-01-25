import pytest
import sqlite3
import os
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

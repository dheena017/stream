import os
import sqlite3


from ui.database import DB_FILE, init_db, save_feedback


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

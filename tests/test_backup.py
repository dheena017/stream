import os
import shutil
import sqlite3
import sys
import time

import pytest

# Ensure scripts dir is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))

from backup_manager import BackupManager


@pytest.fixture
def backup_env():
    # Setup
    test_dir = "test_backup_env"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=True)

    db_file = os.path.join(test_dir, "test.db")
    prefs_file = os.path.join(test_dir, "test_prefs.json")
    backup_dir = os.path.join(test_dir, "backups")
    key_file = os.path.join(test_dir, "test.key")

    # Create dummy db
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("CREATE TABLE test (id INTEGER, data TEXT)")
    c.execute("INSERT INTO test VALUES (1, 'initial data')")
    conn.commit()
    conn.close()

    # Create dummy prefs
    with open(prefs_file, "w") as f:
        f.write('{"theme": "dark"}')

    yield {
        "dir": test_dir,
        "db": db_file,
        "prefs": prefs_file,
        "backup_dir": backup_dir,
        "key": key_file,
    }

    # Teardown
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def test_backup_and_restore(backup_env):
    manager = BackupManager(
        backup_dir=backup_env["backup_dir"],
        key_file=backup_env["key"],
        db_file=backup_env["db"],
        prefs_file=backup_env["prefs"],
    )

    # 1. Perform Backup
    backup_path = manager.perform_backup()
    assert os.path.exists(backup_path)
    assert backup_path.endswith(".enc")

    # 2. Modify Data (to verify restore overwrites)
    conn = sqlite3.connect(backup_env["db"])
    c = conn.cursor()
    c.execute("INSERT INTO test VALUES (2, 'new data')")
    conn.commit()
    conn.close()

    with open(backup_env["prefs"], "w") as f:
        f.write('{"theme": "light"}')

    # 3. Perform Restore
    manager.perform_restore(backup_path)

    # 4. Verify Data
    conn = sqlite3.connect(backup_env["db"])
    c = conn.cursor()
    c.execute("SELECT * FROM test")
    rows = c.fetchall()
    conn.close()

    # Should only have the initial data
    assert len(rows) == 1
    assert rows[0][1] == "initial data"

    with open(backup_env["prefs"], "r") as f:
        content = f.read()
    assert content == '{"theme": "dark"}'


def test_retention_policy(backup_env):
    manager = BackupManager(
        backup_dir=backup_env["backup_dir"],
        key_file=backup_env["key"],
        db_file=backup_env["db"],
        prefs_file=backup_env["prefs"],
        retention_days=1,
    )

    # Create an old backup manually
    os.makedirs(backup_env["backup_dir"], exist_ok=True)
    old_backup = os.path.join(backup_env["backup_dir"], "old_backup.enc")
    with open(old_backup, "wb") as f:
        f.write(b"dummy")

    # Set modification time to 2 days ago
    two_days_ago = time.time() - (2 * 86400)
    os.utime(old_backup, (two_days_ago, two_days_ago))

    # Create a new backup
    new_backup = manager.perform_backup()

    # Verify old backup is gone and new backup exists
    assert not os.path.exists(old_backup)
    assert os.path.exists(new_backup)

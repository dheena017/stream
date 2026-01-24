import pytest
import os
import sqlite3
import json
import shutil
import zipfile
import time
from pathlib import Path
from scripts import backup_manager

# Helpers
TEST_DB = "chat_history.db"
TEST_PREFS = "user_prefs.json"

@pytest.fixture
def setup_environment(monkeypatch):
    """Sets up a temporary environment for testing."""
    # Use temporary directories
    test_base_dir = Path("test_env")
    if test_base_dir.exists():
        shutil.rmtree(test_base_dir)
    test_base_dir.mkdir(parents=True)

    # Mock paths in backup_manager
    monkeypatch.setattr(backup_manager, 'BASE_DIR', test_base_dir)
    monkeypatch.setattr(backup_manager, 'DB_FILE', test_base_dir / TEST_DB)
    monkeypatch.setattr(backup_manager, 'USER_PREFS', test_base_dir / TEST_PREFS)
    monkeypatch.setattr(backup_manager, 'BACKUP_DIR', test_base_dir / "backups")
    monkeypatch.setattr(backup_manager, 'KEY_FILE', test_base_dir / "backup.key")

    # Create backup dir
    (test_base_dir / "backups").mkdir()

    # Create dummy DB
    conn = sqlite3.connect(test_base_dir / TEST_DB)
    c = conn.cursor()
    c.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
    c.execute("INSERT INTO test (value) VALUES ('initial')")
    conn.commit()
    conn.close()

    # Create dummy prefs
    with open(test_base_dir / TEST_PREFS, "w") as f:
        json.dump({"theme": "dark"}, f)

    yield test_base_dir

    # Cleanup
    if test_base_dir.exists():
        shutil.rmtree(test_base_dir)

def test_backup_creation(setup_environment):
    backup_path = backup_manager.perform_backup()
    assert backup_path is not None
    assert os.path.exists(backup_path)
    assert str(backup_path).endswith(".enc")

def test_encryption(setup_environment):
    backup_path = backup_manager.perform_backup()

    # Try to open as zip (should fail)
    with pytest.raises(zipfile.BadZipFile):
        with zipfile.ZipFile(backup_path, 'r') as zf:
            zf.testzip()

def test_restore(setup_environment):
    # 1. create backup
    backup_path = backup_manager.perform_backup()
    assert backup_path is not None

    # 2. modify data
    conn = sqlite3.connect(setup_environment / TEST_DB)
    c = conn.cursor()
    c.execute("UPDATE test SET value = 'modified' WHERE id = 1")
    conn.commit()
    conn.close()

    with open(setup_environment / TEST_PREFS, "w") as f:
        json.dump({"theme": "light"}, f)

    # 3. restore
    success = backup_manager.restore_backup(backup_path)
    assert success is True

    # 4. verify
    conn = sqlite3.connect(setup_environment / TEST_DB)
    c = conn.cursor()
    c.execute("SELECT value FROM test WHERE id = 1")
    value = c.fetchone()[0]
    conn.close()

    assert value == 'initial'

    with open(setup_environment / TEST_PREFS, "r") as f:
        prefs = json.load(f)
    assert prefs["theme"] == "dark"

def test_retention(setup_environment, monkeypatch):
    # Set retention to 2 for test
    monkeypatch.setattr(backup_manager, 'RETENTION_DAYS', 2)

    # Create 5 dummy backups with different timestamps
    backups_dir = setup_environment / "backups"

    # We can't easily fake file creation time on all OS properly without modifying the file.
    # But backup_manager sorts by getmtime.

    for i in range(5):
        fname = backups_dir / f"backup_{i}.enc"
        fname.touch()
        # Sleep to ensure different mtimes
        time.sleep(0.1)

    backup_manager.cleanup_old_backups()

    remaining = list(backups_dir.glob("*.enc"))
    assert len(remaining) == 2

import pytest
import os
import shutil
import tempfile
import sys
import time

# Add root to sys.path to allow imports from scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.backup_manager import BackupManager

@pytest.fixture
def temp_env():
    # Create a temporary directory structure simulating the app root
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create dummy files
        with open(os.path.join(temp_dir, "chat_history.db"), "w") as f:
            f.write("dummy db content")
        with open(os.path.join(temp_dir, "users.json"), "w") as f:
            f.write('{"user": "test"}')
        with open(os.path.join(temp_dir, "user_prefs.json"), "w") as f:
            f.write('{"theme": "dark"}')

        yield temp_dir

def test_backup_creation(temp_env):
    manager = BackupManager(root_dir=temp_env)
    backup_file = manager.backup()

    assert backup_file is not None
    assert os.path.exists(backup_file)
    assert backup_file.endswith(".enc")

    # Check secret.key was generated
    assert os.path.exists(os.path.join(temp_env, "secret.key"))

def test_restore(temp_env):
    manager = BackupManager(root_dir=temp_env)

    # Initial state
    db_path = os.path.join(temp_env, "chat_history.db")
    with open(db_path, "r") as f:
        original_content = f.read()

    # Create backup
    backup_file = manager.backup()
    assert backup_file is not None

    # Modify file
    with open(db_path, "w") as f:
        f.write("corrupted content")

    # Restore
    success = manager.restore(backup_file)
    assert success

    # Verify content restored
    with open(db_path, "r") as f:
        restored_content = f.read()

    assert restored_content == original_content

def test_rotation(temp_env):
    manager = BackupManager(root_dir=temp_env)
    manager.retention_count = 2

    # Create 3 backups
    b1 = manager.backup()
    time.sleep(1.1) # Ensure timestamp diff
    b2 = manager.backup()
    time.sleep(1.1)
    b3 = manager.backup()

    backups = manager.list_backups()
    assert len(backups) == 2
    assert b3 in backups
    assert b2 in backups
    # b1 should be deleted (since list_backups returns paths, checking existence is better or checking list content)
    # The list_backups returns full paths.

    assert not os.path.exists(b1)
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

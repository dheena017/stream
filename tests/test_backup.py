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

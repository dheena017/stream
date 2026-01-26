import os
import shutil
import pytest
import sys
import time

# Add scripts to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.backup_manager import BackupManager

@pytest.fixture
def backup_env(tmp_path):
    # Setup
    cwd = os.getcwd()
    os.chdir(tmp_path)

    # Create dummy data
    with open("chat_history.db", "w") as f:
        f.write("dummy db content")

    # Initialize BackupManager
    bm = BackupManager(backup_dir="backups", key_file="backup.key")

    yield bm

    # Teardown
    os.chdir(cwd)

def test_backup_create(backup_env):
    bm = backup_env
    path = bm.backup()

    assert path is not None
    assert os.path.exists(path)
    assert path.endswith(".enc")

    # Verify backup dir
    assert os.path.exists("backups")
    assert len(os.listdir("backups")) == 1

def test_restore(backup_env):
    bm = backup_env
    backup_path = bm.backup()

    # Modify original file
    with open("chat_history.db", "w") as f:
        f.write("modified content")

    # Restore
    result = bm.restore(backup_path)
    assert result is True

    # Verify content
    with open("chat_history.db", "r") as f:
        content = f.read()
    assert content == "dummy db content"

def test_rotation(backup_env):
    bm = backup_env
    # Create 8 backups
    backups = []

    # We need to simulate time passing or force filenames to be different/sorted
    # BackupManager uses datetime.now() for filenames and os.path.getmtime for sorting.
    # Sleep is slow. We can just loop.

    for i in range(8):
        path = bm.backup()
        backups.append(path)
        # Sleep slightly to ensure mtime difference and filename difference
        time.sleep(1.1)

    # Check count (should be 7)
    files = os.listdir("backups")
    assert len(files) == 7

    # The first one backups[0] should be gone
    assert not os.path.exists(backups[0])
    # The last one backups[7] should be present
    assert os.path.exists(backups[7])

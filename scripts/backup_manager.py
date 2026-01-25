import os
import shutil
<<<<<<< HEAD
<<<<<<< HEAD
import zipfile
import glob
from datetime import datetime
from cryptography.fernet import Fernet
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self, root_dir=None):
        if root_dir:
             self.root_dir = root_dir
        else:
             # Assume script is in scripts/ and project root is one level up
             self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.backup_dir = os.path.join(self.root_dir, "backups")
        self.key_file = os.path.join(self.root_dir, "secret.key")
        self.files_to_backup = [
            "chat_history.db",
            "users.json",
            "user_prefs.json"
        ]
        self.retention_count = 7

        # Ensure backup directory exists
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def _get_key(self):
        """Load or generate encryption key."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
            logger.info("Generated new encryption key.")
            return key

    def backup(self):
        """Create an encrypted backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = os.path.join(self.backup_dir, f"temp_{timestamp}")

        try:
            os.makedirs(temp_dir)

            # Copy files to temp dir
            files_copied = 0
            for filename in self.files_to_backup:
                src_path = os.path.join(self.root_dir, filename)
                if os.path.exists(src_path):
                    shutil.copy2(src_path, temp_dir)
                    files_copied += 1

            if files_copied == 0:
                logger.warning("No files found to backup.")
                shutil.rmtree(temp_dir)
                return None

            # Create ZIP
            zip_filename = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")
            shutil.make_archive(zip_filename.replace('.zip', ''), 'zip', temp_dir)

            # Encrypt ZIP
            key = self._get_key()
            fernet = Fernet(key)

            with open(zip_filename, "rb") as f:
                data = f.read()

            encrypted_data = fernet.encrypt(data)

            enc_filename = os.path.join(self.backup_dir, f"backup_{timestamp}.enc")
            with open(enc_filename, "wb") as f:
                f.write(encrypted_data)

            logger.info(f"Backup created successfully: {enc_filename}")

            # Cleanup
            os.remove(zip_filename)
            shutil.rmtree(temp_dir)

            self._rotate_backups()
            return enc_filename

        except Exception as e:
            logger.error(f"Backup failed: {e}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return None

    def _rotate_backups(self):
        """Keep only the last N backups."""
        backups = sorted(glob.glob(os.path.join(self.backup_dir, "backup_*.enc")))
        if len(backups) > self.retention_count:
            for b in backups[:-self.retention_count]:
                os.remove(b)
                logger.info(f"Deleted old backup: {b}")

    def restore(self, backup_file):
        """Restore from a backup file."""
        if not os.path.exists(backup_file):
            logger.error(f"Backup file not found: {backup_file}")
            return False

        try:
            key = self._get_key()
            fernet = Fernet(key)

            with open(backup_file, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            temp_zip = os.path.join(self.backup_dir, "restore_temp.zip")
            with open(temp_zip, "wb") as f:
                f.write(decrypted_data)

            temp_extract = os.path.join(self.backup_dir, "restore_temp")
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_extract)

            # Restore files
            for filename in os.listdir(temp_extract):
                src = os.path.join(temp_extract, filename)
                dst = os.path.join(self.root_dir, filename)
                shutil.copy2(src, dst)
                logger.info(f"Restored: {filename}")

            # Cleanup
            os.remove(temp_zip)
            shutil.rmtree(temp_extract)
            return True

        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False

    def list_backups(self):
        """List available backups."""
        return sorted(glob.glob(os.path.join(self.backup_dir, "backup_*.enc")), reverse=True)

if __name__ == "__main__":
    manager = BackupManager()
    manager.backup()
=======
import sqlite3
import zipfile
import datetime
import time
import schedule
import logging
from cryptography.fernet import Fernet
from pathlib import Path

# Configure logging
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / 'app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('backup_manager')

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "chat_history.db"
USER_PREFS = BASE_DIR / "user_prefs.json"
BACKUP_DIR = BASE_DIR / "backups"
KEY_FILE = BASE_DIR / "backup.key"
RETENTION_DAYS = 7

def load_key():
    """Loads the encryption key from file or generates a new one."""
    if not KEY_FILE.exists():
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    return open(KEY_FILE, "rb").read()

def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted_data)
    os.remove(file_path) # Remove unencrypted archive
    return file_path + ".enc"

def decrypt_file(encrypted_file_path, key):
    f = Fernet(key)
    with open(encrypted_file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    original_path = str(encrypted_file_path).replace(".enc", "")
    with open(original_path, "wb") as file:
        file.write(decrypted_data)
    return original_path

def perform_backup():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        temp_dir = BACKUP_DIR / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # 1. Backup DB (Hot Backup)
        backup_db_path = temp_dir / "chat_history.db"
        if DB_FILE.exists():
            conn = sqlite3.connect(DB_FILE)
            backup_conn = sqlite3.connect(backup_db_path)
            conn.backup(backup_conn)
            backup_conn.close()
            conn.close()

        # 2. Backup User Prefs
        if USER_PREFS.exists():
            shutil.copy(USER_PREFS, temp_dir / "user_prefs.json")

        # 3. Create Zip
        archive_path = BACKUP_DIR / f"{backup_name}.zip"
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)

        # 4. Cleanup Temp
        shutil.rmtree(temp_dir)

        # 5. Encrypt
        key = load_key()
        encrypted_path = encrypt_file(str(archive_path), key)

        logger.info(f"Backup successful: {encrypted_path}")
        print(f"Backup successful: {encrypted_path}")

        cleanup_old_backups()
        return encrypted_path

    except Exception as e:
        logger.error(f"Backup failed: {e}")
        print(f"Backup failed: {e}")
        return None

def cleanup_old_backups():
    try:
        backups = sorted(BACKUP_DIR.glob("*.enc"), key=os.path.getmtime, reverse=True)
        for backup in backups[RETENTION_DAYS:]:
            os.remove(backup)
            logger.info(f"Deleted old backup: {backup}")
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")

def restore_backup(backup_file_path):
    zip_path = None
    try:
        key = load_key()
        # Decrypt
        zip_path = decrypt_file(backup_file_path, key)

        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(BASE_DIR) # Overwrite files in root

        logger.info(f"Restore successful from {backup_file_path}")
        print(f"Restore successful from {backup_file_path}")
        return True
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        print(f"Restore failed: {e}")
        return False
    finally:
        # Cleanup decrypted zip
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)

def run_scheduler():
    schedule.every().day.at("02:00").do(perform_backup)

    logger.info("Backup scheduler started")
    print("Backup scheduler started. Press Ctrl+C to exit.")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "backup":
            perform_backup()
        elif sys.argv[1] == "restore" and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        elif sys.argv[1] == "schedule":
            run_scheduler()
        else:
            print("Usage: python backup_manager.py [backup|restore <file>|schedule]")
    else:
        perform_backup()
>>>>>>> origin/backup-automation-2982499736536864191
=======
import sqlite3
import logging
import json
import time
from datetime import datetime
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self, backup_dir="backups", key_file="backup.key", db_file="chat_history.db", prefs_file="user_prefs.json", retention_days=7):
        self.backup_dir = backup_dir
        self.key_file = key_file
        self.db_file = db_file
        self.prefs_file = prefs_file
        self.retention_days = retention_days

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)

    def _get_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            logger.info(f"Generated new encryption key at {self.key_file}")
            return key

    def cleanup_old_backups(self):
        """Delete backups older than retention_days"""
        if self.retention_days <= 0:
            return

        now = time.time()
        cutoff = now - (self.retention_days * 86400)

        count = 0
        if not os.path.exists(self.backup_dir):
            return

        for filename in os.listdir(self.backup_dir):
            if filename.endswith(".enc"):
                filepath = os.path.join(self.backup_dir, filename)
                try:
                    if os.path.getmtime(filepath) < cutoff:
                        os.remove(filepath)
                        count += 1
                        logger.info(f"Deleted old backup: {filename}")
                except Exception as e:
                    logger.error(f"Error deleting {filename}: {e}")
        if count > 0:
            logger.info(f"Cleaned up {count} old backups.")

    def _backup_db(self, target_path):
        """ safely backup sqlite db to target_path """
        if not os.path.exists(self.db_file):
            logger.warning(f"Database file {self.db_file} not found. Skipping DB backup.")
            return

        try:
            # Connect to the source database
            src = sqlite3.connect(self.db_file)
            # Connect to the destination database
            dst = sqlite3.connect(target_path)
            with dst:
                src.backup(dst)
            dst.close()
            src.close()
            logger.info("Database backup successful (sqlite3 backup API).")
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            raise

    def perform_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = f"temp_backup_{timestamp}"
        os.makedirs(temp_dir, exist_ok=True)
        zip_file = None

        try:
            # 1. Backup DB
            self._backup_db(os.path.join(temp_dir, os.path.basename(self.db_file)))

            # 2. Copy user_prefs
            if os.path.exists(self.prefs_file):
                shutil.copy2(self.prefs_file, os.path.join(temp_dir, os.path.basename(self.prefs_file)))
            else:
                logger.warning(f"{self.prefs_file} not found.")

            # 3. Zip
            archive_name = f"backup_{timestamp}"
            shutil.make_archive(archive_name, 'zip', temp_dir)
            zip_file = f"{archive_name}.zip"

            # 4. Encrypt
            with open(zip_file, "rb") as f:
                data = f.read()
            encrypted_data = self.fernet.encrypt(data)

            final_backup_path = os.path.join(self.backup_dir, f"{archive_name}.enc")
            with open(final_backup_path, "wb") as f:
                f.write(encrypted_data)

            logger.info(f"Backup created successfully: {final_backup_path}")

            self.cleanup_old_backups()

            return final_backup_path

        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            if zip_file and os.path.exists(zip_file):
                os.remove(zip_file)

    def perform_restore(self, backup_path):
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        temp_extract_dir = "temp_restore_extract"
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
        os.makedirs(temp_extract_dir)

        zip_path = "temp_restore.zip"

        try:
            # 1. Decrypt
            with open(backup_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)

            with open(zip_path, "wb") as f:
                f.write(decrypted_data)

            # 2. Unzip
            shutil.unpack_archive(zip_path, temp_extract_dir, 'zip')

            # 3. Restore files
            # Restore DB
            restored_db = os.path.join(temp_extract_dir, os.path.basename(self.db_file))
            if os.path.exists(restored_db):
                shutil.copy2(restored_db, self.db_file)
                logger.info(f"Restored {self.db_file}")

            # Restore prefs
            restored_prefs = os.path.join(temp_extract_dir, os.path.basename(self.prefs_file))
            if os.path.exists(restored_prefs):
                shutil.copy2(restored_prefs, self.prefs_file)
                logger.info(f"Restored {self.prefs_file}")

            logger.info("Restore completed successfully.")

        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise
        finally:
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)
            if os.path.exists(zip_path):
                os.remove(zip_path)
>>>>>>> origin/backup-automation-4231149804985086977

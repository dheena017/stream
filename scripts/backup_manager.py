import os
import shutil
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

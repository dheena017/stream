import os
import shutil
import zipfile
import glob
from datetime import datetime
from cryptography.fernet import Fernet
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self, backup_dir="backups", key_file="backup.key", targets=None):
        self.backup_dir = backup_dir
        self.key_file = key_file
        self.targets = targets if targets is not None else ["chat_history.db", "users.json", "secret.key"]

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        self.key = self._load_key()

    def _load_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            logger.info(f"Generated new encryption key at {self.key_file}")
            return key

    def backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_zip = f"temp_backup_{timestamp}.zip"
        final_backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}.zip.enc")

        files_found = []
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for target in self.targets:
                if os.path.exists(target):
                    zipf.write(target)
                    files_found.append(target)
                else:
                    logger.warning(f"File {target} not found, skipping.")

        if not files_found:
            logger.error("No files found to backup.")
            if os.path.exists(temp_zip):
                os.remove(temp_zip)
            return None

        # Encrypt
        f = Fernet(self.key)
        with open(temp_zip, "rb") as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)

        with open(final_backup_path, "wb") as file:
            file.write(encrypted_data)

        os.remove(temp_zip)
        logger.info(f"Backup created at {final_backup_path}")

        self.cleanup_old_backups()
        return final_backup_path

    def restore(self, backup_file):
        if not os.path.exists(backup_file):
            logger.error(f"Backup file {backup_file} does not exist.")
            return False

        try:
            f = Fernet(self.key)
            with open(backup_file, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = f.decrypt(encrypted_data)

            temp_zip = "temp_restore.zip"
            with open(temp_zip, "wb") as file:
                file.write(decrypted_data)

            with zipfile.ZipFile(temp_zip, 'r') as zipf:
                zipf.extractall(".")
                logger.info("Backup restored successfully.")

            os.remove(temp_zip)
            return True
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            if os.path.exists("temp_restore.zip"):
                os.remove("temp_restore.zip")
            return False

    def cleanup_old_backups(self, keep=7):
        backups = glob.glob(os.path.join(self.backup_dir, "*.enc"))
        backups.sort(key=os.path.getmtime)

        if len(backups) > keep:
            for backup in backups[:-keep]:
                os.remove(backup)
                logger.info(f"Removed old backup: {backup}")

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

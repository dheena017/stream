import argparse
import logging
import sys
import os

# Ensure we can import backup_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backup_manager import BackupManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def restore_backup(backup_file):
    logger.info(f"Starting restore process from {backup_file}...")
    try:
        manager = BackupManager()
        manager.perform_restore(backup_file)
        logger.info("Restore process completed.")
    except Exception as e:
        logger.error(f"Restore process failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore Utility")
    parser.add_argument("backup_file", help="Path to the backup file (.enc)")

    args = parser.parse_args()

    restore_backup(args.backup_file)

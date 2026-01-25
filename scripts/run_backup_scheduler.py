import sys
import os
import schedule
import time
import logging

# Add current directory to path so we can import backup_manager
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from backup_manager import BackupManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def job():
    logger.info("Starting scheduled backup...")
    manager = BackupManager()
    result = manager.backup()
    if result:
        logger.info(f"Scheduled backup completed: {result}")
    else:
        logger.error("Scheduled backup failed.")

def main():
    logger.info("Backup scheduler started.")
    # Schedule backup every day at 02:00 AM
    schedule.every().day.at("02:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

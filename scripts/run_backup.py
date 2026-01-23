import argparse
import time
import schedule
import logging
import sys
import os

# Ensure we can import backup_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backup_manager import BackupManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_backup():
    logger.info("Starting backup process...")
    try:
        manager = BackupManager()
        manager.perform_backup()
        logger.info("Backup process completed.")
    except Exception as e:
        logger.error(f"Backup process failed: {e}")

def run_scheduler(frequency):
    logger.info(f"Starting backup scheduler. Frequency: {frequency}")

    if frequency == "daily":
        schedule.every().day.at("02:00").do(run_backup)
        logger.info("Scheduled daily backup at 02:00")
    elif frequency == "weekly":
        schedule.every().sunday.at("02:00").do(run_backup)
        logger.info("Scheduled weekly backup on Sunday at 02:00")
    else:
        logger.error("Invalid frequency")
        return

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup Utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command: now
    parser_now = subparsers.add_parser("now", help="Run backup immediately")

    # Command: schedule
    parser_schedule = subparsers.add_parser("schedule", help="Run backup scheduler")
    parser_schedule.add_argument("--frequency", choices=["daily", "weekly"], default="daily", help="Backup frequency")

    args = parser.parse_args()

    if args.command == "now":
        run_backup()
    elif args.command == "schedule":
        run_scheduler(args.frequency)
    else:
        parser.print_help()

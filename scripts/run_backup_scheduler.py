import sys
import os
import time
import schedule

# Ensure we can import from the same directory
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from backup_manager import BackupManager

def job():
    print("Running scheduled backup...")
    bm = BackupManager()
    result = bm.backup()
    if result:
        print(f"Scheduled backup successful: {result}")
    else:
        print("Scheduled backup failed.")

def main():
    # Schedule backup every day at 03:00
    schedule.every().day.at("03:00").do(job)

    print("Backup scheduler running. Scheduled for daily run at 03:00.")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

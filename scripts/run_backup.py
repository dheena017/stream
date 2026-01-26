import sys
import os

# Ensure we can import from the same directory
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from backup_manager import BackupManager

def main():
    print("Starting backup process...")
    # Initialize with default paths (relative to CWD, which should be repo root)
    bm = BackupManager()
    result = bm.backup()
    if result:
        print(f"Backup completed successfully: {result}")
    else:
        print("Backup failed.")

if __name__ == "__main__":
    main()

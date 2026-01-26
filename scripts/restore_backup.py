import sys
import os
import argparse

# Ensure we can import from the same directory
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from backup_manager import BackupManager

def main():
    parser = argparse.ArgumentParser(description="Restore backup from file.")
    parser.add_argument("backup_file", help="Path to the encrypted backup file.")
    parser.add_argument("--force", action="store_true", help="Skip confirmation.")
    args = parser.parse_args()

    print(f"Restoring from {args.backup_file}...")

    if not args.force:
        confirm = input("This will overwrite existing data. Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            print("Restore cancelled.")
            return

    bm = BackupManager()
    if bm.restore(args.backup_file):
        print("Restore completed successfully.")
    else:
        print("Restore failed.")

if __name__ == "__main__":
    main()

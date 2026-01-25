
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime

LOG_FILE = "logs/app.log"

def parse_logs(logfile):
    stats = {
        "sessions": 0,
        "requests": 0,
        "errors": 0,
        "providers": Counter(),
        "latencies": defaultdict(list),
        "feedback": Counter(),
        "search_count": 0
    }

    try:
        with open(logfile, "r", encoding="utf-8") as f:
            for line in f:
                # Basic error counting
                if " | ERROR " in line:
                    stats["errors"] += 1

                # Session counting
                if "Auth state initialized - User:" in line:
                    stats["sessions"] += 1

                # Request counting
                # Log format example: "Generating response: provider=google model=gemini-1.5-flash"
                if "Generating response:" in line:
                    stats["requests"] += 1
                    match = re.search(r"provider=(\w+)", line)
                    if match:
                        provider = match.group(1)
                        stats["providers"][provider] += 1

                # Search counting
                if "Search completed with" in line:
                    stats["search_count"] += 1

                # Feedback counting
                if "Feedback: 👍" in line:
                    stats["feedback"]["up"] += 1
                if "Feedback: 👎" in line:
                    stats["feedback"]["down"] += 1

    except FileNotFoundError:
        print(f"Log file {logfile} not found.")
        return None

    return stats

def print_report(stats):
    if not stats:
        return

    print("="*40)
    print(f"ANALYTICS REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*40)

    print(f"\n📊 General Stats")
    print(f"Total Sessions:   {stats['sessions']}")
    print(f"Total Requests:   {stats['requests']}")
    print(f"Total Errors:     {stats['errors']}")
    print(f"Search Queries:   {stats['search_count']}")

    print(f"\n🤖 Provider Usage")
    if stats['providers']:
        for prov, count in stats['providers'].most_common():
            print(f"  - {prov}: {count}")
    else:
        print("  (No requests recorded)")

    print(f"\n👍 User Feedback")
    print(f"  - Thumbs Up:   {stats['feedback']['up']}")
    print(f"  - Thumbs Down: {stats['feedback']['down']}")

    print("\n" + "="*40)

if __name__ == "__main__":
    stats = parse_logs(LOG_FILE)
    if stats:
        print_report(stats)

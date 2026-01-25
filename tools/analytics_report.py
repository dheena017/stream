<<<<<<< HEAD

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
=======
import sys
import json
import os

LOG_FILE = "logs/usage.jsonl"

def generate_report():
    if not os.path.exists(LOG_FILE):
        print(f"Log file not found: {LOG_FILE}")
        return

    total_requests = 0
    success_count = 0
    provider_stats = {}
    latencies = []
    unique_sessions = set()

    print(f"Analyzing {LOG_FILE}...")

    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'api_request':
                    total_requests += 1
                    if data.get('success'):
                        success_count += 1
                        if data.get('latency'):
                            latencies.append(data['latency'])

                    provider = data.get('provider', 'unknown')
                    provider_stats[provider] = provider_stats.get(provider, 0) + 1

                    if data.get('session_id'):
                        unique_sessions.add(data['session_id'])
            except json.JSONDecodeError:
                continue

    if total_requests == 0:
        print("No requests found.")
        return

    success_rate = (success_count / total_requests) * 100
    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    print("-" * 30)
    print("ANALYTICS REPORT")
    print("-" * 30)
    print(f"Total Requests: {total_requests}")
    print(f"Success Rate:   {success_rate:.2f}%")
    print(f"Avg Latency:    {avg_latency:.2f}s")
    print(f"Unique Sessions:{len(unique_sessions)}")
    print("-" * 30)
    print("Requests per Provider:")
    for provider, count in provider_stats.items():
        print(f"  {provider}: {count}")
    print("-" * 30)

if __name__ == "__main__":
    generate_report()
>>>>>>> origin/analytics-monitoring-16051435839535532537

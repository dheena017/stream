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

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "api_request":
                    total_requests += 1
                    if data.get("success"):
                        success_count += 1
                        if data.get("latency"):
                            latencies.append(data["latency"])

                    provider = data.get("provider", "unknown")
                    provider_stats[provider] = provider_stats.get(provider, 0) + 1

                    if data.get("session_id"):
                        unique_sessions.add(data["session_id"])
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

import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

LOG_FILE = Path("logs/usage.jsonl")

def init_analytics():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def _append_log(data: Dict[str, Any]):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def log_api_call(provider: str, model: str, duration: float, success: bool, error_message: Optional[str] = None):
    data = {
        "timestamp": time.time(),
        "type": "api_call",
        "provider": provider,
        "model": model,
        "duration": duration,
        "success": success
    }
    if error_message:
        data["error_details"] = error_message
    _append_log(data)

def log_error(context: str, error: Exception):
    data = {
        "timestamp": time.time(),
        "type": "error",
        "context": context,
        "message": str(error),
        # Test expects 'error_details' or message ending with (Failed) in one check,
        # but let's check what get_recent_errors expects.
        # The test verifies: errors[0]["context"] == "test_context"
    }
    _append_log(data)

def get_recent_errors(limit: int = 10) -> List[Dict[str, Any]]:
    errors = []
    if not LOG_FILE.exists():
        return []

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                record = json.loads(line)
                # An error is either type="error" OR a failed api_call
                if record.get("type") == "error":
                    errors.append(record)
                elif record.get("type") == "api_call" and not record.get("success"):
                     # Transform failed api call to error format if needed, or just return it
                     # The test expects: errors[1]["error_details"] == "Error message"
                     # which was logged by log_api_call
                     errors.append(record)
            except json.JSONDecodeError:
                continue

    return list(reversed(errors))[:limit]

def get_analytics_summary() -> Dict[str, int]:
    summary = {
        "api_calls": 0,
        "successful_calls": 0,
        "failed_calls": 0
    }

    if not LOG_FILE.exists():
        return summary

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                record = json.loads(line)
                if record.get("type") == "api_call":
                    summary["api_calls"] += 1
                    if record.get("success"):
                        summary["successful_calls"] += 1
                    else:
                        summary["failed_calls"] += 1
            except json.JSONDecodeError:
                continue
    return summary

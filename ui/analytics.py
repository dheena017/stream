import sys
from loguru import logger
import pandas as pd
from datetime import datetime
import json
import os

# Configure logger
LOG_FILE = "logs/app.log"
logger.remove()  # Remove default handler
logger.add(sys.stderr, level="INFO") # Keep console output
logger.add(LOG_FILE, rotation="10 MB", level="INFO", serialize=True) # JSON logs for easier parsing

def track_request(event_type: str, duration: float, success: bool, metadata: dict = None):
    """
    Logs a request/event with its details.
    """
    if metadata is None:
        metadata = {}

    log_data = {
        "event_type": event_type,
        "duration": duration,
        "success": success,
        "timestamp": datetime.now().isoformat(),
        **metadata
    }

    # We log the JSON string so it can be reliably parsed later
    # The 'serialize=True' in logger config wraps this in a full log record JSON
    if success:
        logger.info(json.dumps(log_data))
    else:
        logger.error(json.dumps(log_data))

def get_metrics(limit: int = 100):
    """
    Parses the log file to calculate metrics.
    """
    if not os.path.exists(LOG_FILE):
        return {
            "total_requests": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "recent_events": []
        }

    data = []
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()

        for line in lines:
            try:
                # Loguru serialized format
                entry = json.loads(line)
                # The actual message we logged is in entry['record']['message']
                message_str = entry.get('record', {}).get('message', '')

                # Parse our inner JSON data
                try:
                    event_data = json.loads(message_str)
                    # Check if it has our expected fields to filter out other logs if any
                    if 'event_type' in event_data:
                        data.append(event_data)
                except json.JSONDecodeError:
                    pass
            except (json.JSONDecodeError, KeyError):
                continue

    except Exception as e:
        # Avoid infinite recursion if logging error here, so just print
        print(f"Error reading logs: {e}")
        return {}

    if not data:
        return {
            "total_requests": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "recent_events": []
        }

    df = pd.DataFrame(data)

    avg_resp_time = df['duration'].mean() if 'duration' in df.columns else 0.0

    if 'success' in df.columns:
        total = len(df)
        errors = len(df[df['success'] == False])
        error_rate = (errors / total) * 100 if total > 0 else 0.0
    else:
        error_rate = 0.0

    return {
        "total_requests": len(df),
        "avg_response_time": avg_resp_time,
        "error_rate": error_rate,
        "recent_events": data[-limit:]
    }

def check_alerts(thresholds: dict, metrics: dict = None):
    """
    Checks metrics against thresholds and returns alerts.
    """
    if metrics is None:
        metrics = get_metrics()

    alerts = []

    if metrics.get("error_rate", 0) > thresholds.get("error_rate", 5.0):
        alerts.append(f"High Error Rate: {metrics['error_rate']:.2f}% (Threshold: {thresholds['error_rate']}%)")

    if metrics.get("avg_response_time", 0) > thresholds.get("response_time", 2.0):
        alerts.append(f"High Response Time: {metrics['avg_response_time']:.2f}s (Threshold: {thresholds['response_time']}s)")

    return alerts

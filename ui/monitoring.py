import time
import json
import logging
import os
from datetime import datetime
import pandas as pd

LOG_FILE = "logs/monitor.jsonl"

logger = logging.getLogger(__name__)

def ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_metric(metric_type, data):
    """
    Log a metric to the JSONL file.

    Args:
        metric_type (str): Type of metric (e.g., 'response_time', 'error', 'usage')
        data (dict): Dictionary containing metric data
    """
    ensure_log_dir()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": metric_type,
        "data": data
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        logger.error(f"Failed to write to monitor log: {e}")

    # Alerting Logic (Simple threshold check)
    if metric_type == "response_time":
        duration = data.get("duration", 0)
        if duration > 10.0:
             logger.warning(f"ALERT: High response time: {duration:.2f}s for model {data.get('model', 'unknown')}")

    if metric_type == "error":
         logger.error(f"ALERT: Error occurred: {data.get('message')}")

def get_metrics_df():
    """
    Read the log file into a Pandas DataFrame.
    """
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame()

    data = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                try:
                    if line.strip():
                        data.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        logger.error(f"Failed to read monitor log: {e}")
        return pd.DataFrame()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)

<<<<<<< HEAD
import logging
import json
<<<<<<< HEAD
import time
import os
from pathlib import Path
from typing import List, Dict, Any

class Monitor:
    def __init__(self, log_file="logs/usage.jsonl"):
        self.log_file = log_file

        # Ensure directory exists
        log_dir = os.path.dirname(self.log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        self.logger = logging.getLogger("monitoring")
        self.logger.setLevel(logging.INFO)

        # Ensure handlers are not duplicated
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_request(self, provider: str, model: str, duration: float, success: bool, error_msg: str = None):
        """Log a request to the usage log"""
        entry = {
            "timestamp": time.time(),
            "provider": provider,
            "model": model,
            "duration": duration,
            "success": success,
            "error": error_msg
        }
        self.logger.info(json.dumps(entry))

    def get_stats(self, window_seconds=86400) -> Dict[str, Any]:
        """Calculate stats from the last `window_seconds` (default 24h)"""
        now = time.time()
        start_time = now - window_seconds

        total_requests = 0
        total_errors = 0
        total_duration = 0
        provider_stats = {}

        if not os.path.exists(self.log_file):
             return {
                "total_requests": 0,
                "error_rate": 0,
                "avg_latency": 0,
                "provider_stats": {}
            }
=======
import os
from datetime import datetime
from typing import Optional, Dict, Any

class Monitor:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Monitor, cls).__new__(cls)
            cls._instance._setup_logging()
        return cls._instance

    def _setup_logging(self):
        self.log_dir = "logs"
        self.log_file = os.path.join(self.log_dir, "usage.jsonl")

        # Ensure directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)

        self._logger = logging.getLogger("monitoring")
        self._logger.setLevel(logging.INFO)

        # Avoid adding multiple handlers if re-instantiated
        if not self._logger.handlers:
            handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def log_usage(self, user_id: str, model: str, provider: str, response_time: float, success: bool, error_message: Optional[str] = None):
        """Log usage metrics to usage.jsonl"""

        self.check_alerts(response_time)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "model": model,
            "provider": provider,
            "response_time": response_time,
            "success": success,
            "error_message": error_message
        }

        if self._logger:
            self._logger.info(json.dumps(entry))

    def check_alerts(self, response_time: float):
        """Check for performance issues and alert"""
        THRESHOLD = 10.0 # seconds
        if response_time > THRESHOLD:
            # For now, we just print/log an alert. In real app, this might send an email/slack.
            print(f"⚠️ ALERT: High response time detected: {response_time:.2f}s")

    def get_analytics(self) -> Dict[str, Any]:
        """Analyze logs to provide basic stats"""
        if not os.path.exists(self.log_file):
            return {"total_requests": 0, "avg_response_time": 0.0, "error_rate": 0.0}

        total_requests = 0
        total_time = 0.0
        errors = 0
>>>>>>> origin/monitoring-setup-3291123637376011491

        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
<<<<<<< HEAD
                        entry = json.loads(line)
                        if entry['timestamp'] >= start_time:
                            total_requests += 1
                            if not entry['success']:
                                total_errors += 1
                            else:
                                total_duration += entry['duration']

                            prov = entry.get('provider', 'unknown')
                            if prov not in provider_stats:
                                provider_stats[prov] = {"count": 0, "errors": 0, "total_duration": 0}

                            provider_stats[prov]["count"] += 1
                            if not entry['success']:
                                provider_stats[prov]["errors"] += 1
                            else:
                                provider_stats[prov]["total_duration"] += entry['duration']

                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            # Fallback if file read fails
            pass

        avg_latency = (total_duration / (total_requests - total_errors)) if (total_requests - total_errors) > 0 else 0
        error_rate = (total_errors / total_requests) if total_requests > 0 else 0

        return {
            "total_requests": total_requests,
            "error_rate": error_rate,
            "avg_latency": avg_latency,
            "provider_stats": provider_stats
        }

    def check_alerts(self) -> List[str]:
        """Check for alerts based on defined thresholds"""
        stats = self.get_stats(window_seconds=3600) # Check last hour
        alerts = []

        if stats['total_requests'] > 10: # Only alert if we have enough data
            if stats['error_rate'] > 0.10:
                alerts.append(f"High Error Rate: {stats['error_rate']*100:.1f}% in last hour")
            if stats['avg_latency'] > 5.0:
                alerts.append(f"High Latency: {stats['avg_latency']:.2f}s avg in last hour")

        return alerts

_instance = None

def get_monitor():
    global _instance
    if _instance is None:
        _instance = Monitor()
    return _instance
=======
                        data = json.loads(line)
                        total_requests += 1
                        total_time += data.get("response_time", 0)
                        if not data.get("success", True):
                            errors += 1
                    except json.JSONDecodeError:
                        continue

            avg_time = (total_time / total_requests) if total_requests > 0 else 0.0
            error_rate = (errors / total_requests) if total_requests > 0 else 0.0

            return {
                "total_requests": total_requests,
                "avg_response_time": round(avg_time, 2),
                "error_rate": round(error_rate, 4)
            }
        except Exception as e:
            print(f"Error reading analytics: {e}")
            return {"total_requests": 0, "avg_response_time": 0.0, "error_rate": 0.0}
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
import sys
import os
import json
import logging
from loguru import logger
from datetime import datetime

# Define log paths
LOG_DIR = "logs"
APP_LOG_PATH = os.path.join(LOG_DIR, "app.log")
USAGE_LOG_PATH = os.path.join(LOG_DIR, "usage.jsonl")

def init_logging():
    """Initialize the logging configuration."""
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Remove default handler
    logger.remove()

    # Add console handler (stderr)
    logger.add(sys.stderr, level="INFO")

    # Add file handler for general application logs (readable)
    logger.add(
        APP_LOG_PATH,
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    # Add file handler for usage metrics (JSONL)
    # Filter: only log records that have 'json_data' in extra
    logger.add(
        USAGE_LOG_PATH,
        rotation="10 MB",
        retention="30 days",
        filter=lambda record: "json_data" in record["extra"],
        format="{message}",
        level="INFO"
    )

    # Intercept standard logging messages
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # We replace the basicConfig if it was set, but since streamlit runs app.py multiple times,
    # we might need to be careful. However, basicConfig is idempotent if handlers are set?
    # Actually basicConfig does nothing if root logger has handlers.
    # We will clear existing handlers from root logger to be safe.
    logging.getLogger().handlers = [InterceptHandler()]
    logging.getLogger().setLevel(logging.INFO)


def track_request(provider, model, success, latency, token_usage=None, session_id=None):
    """
    Log a structured event for an API request.

    Args:
        provider (str): The AI provider (e.g., 'openai', 'google').
        model (str): The model name used.
        success (bool): Whether the request was successful.
        latency (float): Time taken in seconds.
        token_usage (dict, optional): Token usage stats.
        session_id (str, optional): User session identifier.
    """
    data = {
        "timestamp": datetime.now().isoformat(),
        "type": "api_request",
        "provider": provider,
        "model": model,
        "success": success,
        "latency": latency,
        "token_usage": token_usage,
        "session_id": session_id
    }
    # Bind json_data to extra so the filter catches it
    logger.bind(json_data=True).info(json.dumps(data))

def track_error(error_msg, context=None):
    """
    Log a structured event for an error.
    """
    data = {
        "timestamp": datetime.now().isoformat(),
        "type": "error",
        "error": str(error_msg),
        "context": context
    }
    logger.bind(json_data=True).error(json.dumps(data))

if __name__ == "__main__":
    # Test logging if run directly
    init_logging()
    logger.info("Monitoring module test started")
    track_request("test_provider", "test_model", True, 0.5)
    track_error("Test error", "Testing monitoring module")
    print(f"Logs created in {LOG_DIR}")
>>>>>>> origin/analytics-monitoring-16051435839535532537

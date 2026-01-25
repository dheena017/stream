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

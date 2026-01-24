import logging
import json
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

        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
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

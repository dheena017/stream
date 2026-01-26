import pytest
import os
import json
import time
from ui.analytics import track_request, get_metrics, check_alerts, LOG_FILE

@pytest.fixture(autouse=True)
def clean_logs():
    # Clear log file before each test
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    yield
    # Optional cleanup after test
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()

def test_track_request_and_metrics():
    # 1. Track some successful requests
    track_request("test_event", 0.5, True)
    track_request("test_event", 1.5, True)

    # 2. Track a failed request
    track_request("test_event", 1.0, False)

    # Ensure logs are flushed to disk (loguru is async or buffered sometimes?
    # default enqueue=False, so it should be sync. But OS buffering?)
    # A small sleep might be safe but usually flush happens on file close or flush.
    # loguru handles are robust.

    # 3. Get metrics
    metrics = get_metrics()

    # Total 3 requests
    assert metrics["total_requests"] == 3

    # Average duration: (0.5 + 1.5 + 1.0) / 3 = 1.0
    assert abs(metrics["avg_response_time"] - 1.0) < 0.01

    # Error rate: 1 failure out of 3 = 33.33%
    assert abs(metrics["error_rate"] - 33.33) < 0.1

def test_alerts():
    # Simulate high error rate
    # Threshold is 5% error rate

    # 1 success, 1 failure => 50% error rate
    track_request("test_event", 0.1, True)
    track_request("test_event", 0.1, False)

    thresholds = {"error_rate": 5.0, "response_time": 2.0}
    alerts = check_alerts(thresholds)

    assert any("High Error Rate" in a for a in alerts)

    # Clean logs for next part of test
    open(LOG_FILE, 'w').close()

    # Simulate high response time
    # 1 success, 5.0s duration
    track_request("test_event", 5.0, True)

    alerts = check_alerts(thresholds)
    assert any("High Response Time" in a for a in alerts)

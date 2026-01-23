import pytest
import os
import json
import time
import logging
from monitoring import Monitor, get_monitor

@pytest.fixture
def monitor_fixture(tmp_path):
    # Reset logger handlers to avoid leakage between tests
    logger = logging.getLogger("monitoring")
    logger.handlers = []

    log_file = tmp_path / "test_usage.jsonl"
    monitor = Monitor(log_file=str(log_file))
    return monitor

def test_log_request(monitor_fixture):
    monitor_fixture.log_request("test_provider", "test_model", 0.5, True)

    with open(monitor_fixture.log_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry['provider'] == "test_provider"
        assert entry['model'] == "test_model"
        assert entry['duration'] == 0.5
        assert entry['success'] is True

def test_get_stats(monitor_fixture):
    monitor_fixture.log_request("p1", "m1", 1.0, True)
    monitor_fixture.log_request("p1", "m1", 2.0, True)
    monitor_fixture.log_request("p1", "m1", 0.0, False) # Error

    stats = monitor_fixture.get_stats()

    assert stats['total_requests'] == 3
    assert stats['error_rate'] == 1/3
    # Avg latency = (1.0 + 2.0) / 2 = 1.5
    assert stats['avg_latency'] == 1.5
    assert stats['provider_stats']['p1']['count'] == 3
    assert stats['provider_stats']['p1']['errors'] == 1

def test_alerts(monitor_fixture):
    # Create high error rate scenario
    for _ in range(12):
        monitor_fixture.log_request("p1", "m1", 0.1, False)

    alerts = monitor_fixture.check_alerts()
    assert len(alerts) >= 1
    assert "High Error Rate" in alerts[0]

def test_singleton():
    m1 = get_monitor()
    m2 = get_monitor()
    assert m1 is m2

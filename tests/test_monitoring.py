<<<<<<< HEAD
import os
import json
import pandas as pd
import pytest
from ui.monitoring import log_metric, get_metrics_df, LOG_FILE

def test_monitoring_flow():
    # Clean up before test
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # 1. Test Logging
    log_metric("response_time", {"duration": 0.5, "model": "test-model"})
    log_metric("error", {"message": "test error"})

    assert os.path.exists(LOG_FILE)

    # 2. Test Reading
    df = get_metrics_df()
    assert not df.empty
    assert len(df) == 2
    assert "response_time" in df['type'].values
    assert "error" in df['type'].values

    # 3. Test Threshold Alerting (Check if it logs - captured via mocking would be better, but we check if it writes to file at least)
    log_metric("response_time", {"duration": 15.0, "model": "slow-model"})
    df = get_metrics_df()
    assert len(df) == 3

    # Check data content
    last_entry = df.iloc[-1]
    assert last_entry['type'] == 'response_time'
    assert last_entry['data']['duration'] == 15.0

    # Cleanup
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

if __name__ == "__main__":
    try:
        test_monitoring_flow()
        print("Tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
        exit(1)
=======
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
>>>>>>> origin/monitoring-setup-15681340840960488850

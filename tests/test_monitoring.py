import os
import json
import pytest
from monitoring import Monitor
import time

@pytest.fixture
def monitor():
    m = Monitor()

    # Reset handlers to allow re-setup with fresh file handle
    if m._logger:
        for handler in m._logger.handlers[:]:
            handler.close()
            m._logger.removeHandler(handler)

    # Clear log file
    if os.path.exists(m.log_file):
        os.remove(m.log_file)

    # Re-setup logging
    # We need to manually call setup because singleton __new__ won't call it again
    m._setup_logging()

    yield m

    # Cleanup after test
    if m._logger:
         for handler in m._logger.handlers[:]:
            handler.close()
            m._logger.removeHandler(handler)
    if os.path.exists(m.log_file):
        os.remove(m.log_file)

def test_log_usage(monitor):
    monitor.log_usage(
        user_id="test_user",
        model="gpt-4",
        provider="openai",
        response_time=1.5,
        success=True
    )

    # Give a tiny bit of time for file write if async (it's not, but good practice)
    # But logging.FileHandler is sync usually.

    assert os.path.exists(monitor.log_file)

    with open(monitor.log_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["user_id"] == "test_user"
        assert data["model"] == "gpt-4"
        assert data["response_time"] == 1.5

def test_analytics(monitor):
    monitor.log_usage("user1", "model1", "prov1", 1.0, True)
    monitor.log_usage("user2", "model1", "prov1", 2.0, True)
    monitor.log_usage("user3", "model1", "prov1", 3.0, False, "error")

    stats = monitor.get_analytics()
    assert stats["total_requests"] == 3
    assert stats["avg_response_time"] == 2.0 # (1+2+3)/3
    assert abs(stats["error_rate"] - 0.3333) < 0.0001

def test_alerts(monitor, capsys):
    monitor.log_usage("user1", "model1", "prov1", 11.0, True)
    captured = capsys.readouterr()
    assert "ALERT: High response time" in captured.out

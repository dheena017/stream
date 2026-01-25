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

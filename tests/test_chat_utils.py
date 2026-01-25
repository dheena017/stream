import pytest
from unittest.mock import Mock
from ui.chat_utils import augment_prompt_with_search, retry_with_backoff

def test_augment_prompt_with_search():
    prompt = "What is the capital of France?"
    search_results = [
        {"title": "Paris - Wikipedia", "href": "http://example.com", "body": "Paris is the capital of France."}
    ]
    augmented = augment_prompt_with_search(prompt, search_results)

    assert prompt in augmented
    assert "Paris is the capital of France" in augmented
    assert "[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]" in augmented

def test_retry_with_backoff_success():
    mock_func = Mock(side_effect=[Exception("Fail"), "Success"])

    @retry_with_backoff(retries=3, backoff_in_seconds=0.01)
    def wrapped_func():
        return mock_func()

    result = wrapped_func()
    assert result == "Success"
    assert mock_func.call_count == 2

def test_retry_with_backoff_failure():
    mock_func = Mock(side_effect=Exception("Always Fail"))

    @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
    def wrapped_func():
        return mock_func()

    with pytest.raises(Exception, match="Always Fail"):
        wrapped_func()

    assert mock_func.call_count == 3

import unittest
from unittest.mock import MagicMock, patch
import logging
import sys
import os

# Ensure we can import from ui
sys.path.append(os.getcwd())

from ui.chat_utils import retry_with_backoff, generate_standard_response

class TestResilience(unittest.TestCase):

    def test_retry_logic(self):
        """Test that retry_with_backoff retries and eventually succeeds."""
        mock_func = MagicMock()
        mock_func.side_effect = [Exception("Fail 1"), Exception("Fail 2"), "Success"]

        @retry_with_backoff(retries=3, backoff_in_seconds=0.01)
        def decorated_func():
            return mock_func()

        result = decorated_func()
        self.assertEqual(result, "Success")
        self.assertEqual(mock_func.call_count, 3)

    def test_retry_logic_failure(self):
        """Test that retry_with_backoff raises exception after max retries."""
        mock_func = MagicMock()
        mock_func.side_effect = Exception("Persistent Fail")

        @retry_with_backoff(retries=2, backoff_in_seconds=0.01)
        def decorated_func():
            return mock_func()

        with self.assertRaises(Exception):
            decorated_func()

        # Initial call + 2 retries = 3 calls
        self.assertEqual(mock_func.call_count, 3)

    @patch('ui.chat_utils.handle_openai_compatible_provider')
    @patch('ui.chat_utils.get_openai_client')
    def test_provider_error_handling(self, mock_get_client, mock_handle):
        """Test that generate_standard_response returns an error string on failure."""

        # Mocking so that the call inside generate_standard_response raises an exception
        # generate_standard_response calls handle_openai_compatible_provider for "openai"

        # We simulate the provider handler failing (which might happen if retries are exhausted inside it)
        # Note: In the current code, handle_openai_compatible_provider returns a string on error,
        # but generate_standard_response also has a try/except.
        # If handle_openai_compatible_provider raises an exception, generate_standard_response should catch it.
        # Wait, handle_openai_compatible_provider in current code CATCHES exceptions and returns string.
        # So generate_standard_response will receive that string.
        # But if we mock it to RAISE, we test generate_standard_response's outer try/except.

        mock_handle.side_effect = Exception("Critical Failure")

        api_keys = {"openai": "test-key"}
        response = generate_standard_response(
            provider="openai",
            model_name="gpt-4",
            api_keys=api_keys,
            prompt="Hello",
            chat_history=[],
            config={}
        )

        # Expecting "Generation Error: Critical Failure" based on current code
        self.assertTrue(response.startswith("Generation Error:") or response.startswith("Error:"), f"Got: {response}")
        self.assertIn("Critical Failure", response)

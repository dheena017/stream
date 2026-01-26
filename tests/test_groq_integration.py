import unittest
from unittest.mock import MagicMock, patch

from ui.chat_utils import generate_standard_response


class TestGroqIntegration(unittest.TestCase):
    @patch("ui.chat_utils.get_openai_client")
    @patch("ui.chat_utils.st")
    def test_groq_generation(self, mock_st, mock_get_client):
        # Setup mock client
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock successful response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Groq response"
        mock_client.chat.completions.create.return_value = mock_response

        api_keys = {"groq": "fake_key"}

        # Test parameters
        provider = "groq"
        model_name = "llama-3.1-8b-instant"
        prompt = "Hello"
        chat_history = []

        response = generate_standard_response(
            provider=provider,
            model_name=model_name,
            api_keys=api_keys,
            prompt=prompt,
            chat_history=chat_history,
        )

        # Verify get_openai_client was called with correct base_url
        mock_get_client.assert_called_with("fake_key", "https://api.groq.com/openai/v1")

        # Verify completion call
        mock_client.chat.completions.create.assert_called()
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs["model"], model_name)
        # Check that user prompt is in messages
        messages = call_args.kwargs["messages"]
        self.assertEqual(messages[-1]["role"], "user")
        self.assertEqual(messages[-1]["content"], prompt)

        # Verify response
        self.assertEqual(response, "Groq response")


if __name__ == "__main__":
    unittest.main()

import pytest
import sys
from unittest.mock import MagicMock, patch

# Ensure modules are mocked
sys.modules["streamlit"] = MagicMock()
sys.modules["openai"] = MagicMock()
sys.modules["anthropic"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()
sys.modules["google.api_core"] = MagicMock()

from ui.chat_utils import generate_standard_response

@patch("ui.chat_utils.handle_google_provider")
def test_integration_ethics_disclaimer(mock_google):
    mock_google.return_value = "AI Response"

    # Trigger a bias (e.g. "stereotype")
    prompt = "This text contains a stereotype."

    response = generate_standard_response(
        provider="google",
        model_name="gemini",
        api_keys={"google": "k"},
        prompt=prompt,
        chat_history=[]
    )

    assert "AI Response" in response
    assert "[Ethics Notice:" in response
    assert "historical biases" in response

@patch("ui.chat_utils.handle_openai_compatible_provider")
@patch("ui.chat_utils.get_openai_client")
def test_integration_ethics_system_instruction(mock_client, mock_openai):
    mock_openai.return_value = "Response"

    prompt = "This text contains a stereotype."

    with patch("ui.chat_utils.create_openai_messages") as mock_create:
        mock_create.return_value = [{"role": "user", "content": "prompt"}]

        generate_standard_response(
            provider="openai",
            model_name="gpt-4",
            api_keys={"openai": "k"},
            prompt=prompt,
            chat_history=[]
        )

        # Check if create_openai_messages was called with system_instruction containing "neutrally"
        args, kwargs = mock_create.call_args
        # kwargs might not be set if passed as positional.
        # Signature: create_openai_messages(history, prompt, system_instruction=None)
        # Call: create_openai_messages(chat_history, prompt, system_instruction=system_instruction)
        # So it is likely kwargs.

        sys_instr = kwargs.get("system_instruction")
        assert sys_instr is not None
        assert "neutrally" in sys_instr


from ui.chat_utils import preload_blip_model_with_progress


def test_preload_blip_model_graceful_failure():
    """
    Test that preload_blip_model_with_progress returns False gracefully
    when dependencies (transformers/torch) are missing.
    """
    # Since we commented out transformers/torch in requirements.txt,
    # and they are imported inside the function, this call should fail internally
    # but return False due to the try-except block.

    result = preload_blip_model_with_progress()
    assert result is False


def test_preload_blip_model_with_callback():
    """Test with a callback function."""
    msgs = []

    def callback(progress, msg):
        msgs.append((progress, msg))

    result = preload_blip_model_with_progress(progress_callback=callback)
    assert result is False
    assert len(msgs) > 0
    # Should end with 0 progress and failure message
    assert msgs[-1][0] == 0
    assert "Failed" in msgs[-1][1]

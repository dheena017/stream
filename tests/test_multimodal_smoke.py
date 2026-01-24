from PIL import Image

from ui.chat_utils import generate_image_captions, process_images_for_context


def test_process_images_for_context_basic():
    img = Image.new('RGB', (100, 200), color=(73, 109, 137))
    results = process_images_for_context([img])
    assert isinstance(results, list)
    assert results[0]['name'] == 'image_1'
    assert '100x200' in results[0]['caption']


def test_generate_image_captions_fallback():
    img = Image.new('RGB', (50, 50), color=(255, 0, 0))
    caps = generate_image_captions([img], use_blip=False, hosted_api_url=None)
    assert isinstance(caps, list)
    assert caps[0]['name'] == 'image_1'
    assert caps[0]['caption'] is not None

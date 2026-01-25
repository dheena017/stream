<<<<<<< HEAD
import os
import sys
import traceback
from io import BytesIO

# Ensure project root is on sys.path for imports
ROOT = os.getcwd()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

out = {}
try:
    from PIL import Image

    from ui.chat_utils import (
        extract_video_frame_thumbnails,
        generate_image_captions,
        perform_internet_search,
        process_images_for_context,
        transcribe_audio_file,
    )

    # Test image processing
    try:
        img = Image.new("RGB", (100, 200), color="blue")
        img_ctx = process_images_for_context([img])
        out["img_ctx"] = img_ctx
        # test BLIP wrapper (will fallback if unavailable)
        img_caps = generate_image_captions([img], use_blip=True)
        out["img_caps_with_blip"] = img_caps
    except Exception as e:
        out["img_ctx_error"] = repr(e)

    # Test audio transcription (empty buffer)
    try:
        trans = transcribe_audio_file(BytesIO(b""))
        out["transcription"] = trans
    except Exception as e:
        out["trans_error"] = repr(e)

    # Test video thumbnail extraction (empty buffer)
    try:
        thumbs = extract_video_frame_thumbnails(BytesIO(b""), max_frames=2)
        out["thumbs"] = thumbs
    except Exception as e:
        out["thumbs_error"] = repr(e)

    # Test internet search (may be empty if network/package unavailable)
    try:
        results, context = perform_internet_search(
            "latest AI", enable_search=True, max_results=2
        )
        out["search_count"] = len(results) if results else 0
        out["search_context_preview"] = (context or "")[:300]
    except Exception as e:
        out["search_error"] = repr(e)

except Exception as e:
    out["import_error"] = traceback.format_exc()

print(out)
=======
import os
import sys
import traceback
from io import BytesIO

# Ensure project root is on sys.path for imports
ROOT = os.getcwd()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

out = {}
try:
    from PIL import Image

    from ui.chat_utils import (
        extract_video_frame_thumbnails,
        generate_image_captions,
        perform_internet_search,
        process_images_for_context,
        transcribe_audio_file,
    )

    # Test image processing
    try:
        img = Image.new('RGB', (100, 200), color='blue')
        img_ctx = process_images_for_context([img])
        out['img_ctx'] = img_ctx
        # test BLIP wrapper (will fallback if unavailable)
        img_caps = generate_image_captions([img], use_blip=True)
        out['img_caps_with_blip'] = img_caps
    except Exception as e:
        out['img_ctx_error'] = repr(e)

    # Test audio transcription (empty buffer)
    try:
        trans = transcribe_audio_file(BytesIO(b''))
        out['transcription'] = trans
    except Exception as e:
        out['trans_error'] = repr(e)

    # Test video thumbnail extraction (empty buffer)
    try:
        thumbs = extract_video_frame_thumbnails(BytesIO(b''), max_frames=2)
        out['thumbs'] = thumbs
    except Exception as e:
        out['thumbs_error'] = repr(e)

    # Test internet search (may be empty if network/package unavailable)
    try:
        results, context = perform_internet_search("latest AI", enable_search=True, max_results=2)
        out['search_count'] = len(results) if results else 0
        out['search_context_preview'] = (context or '')[:300]
    except Exception as e:
        out['search_error'] = repr(e)

except Exception:
    out['import_error'] = traceback.format_exc()

print(out)
>>>>>>> origin/code-quality-refactor-17423438479402428749

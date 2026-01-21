
import streamlit as st
import logging
from typing import List, Dict, Optional, Any, Callable, Tuple

logger = logging.getLogger(__name__)

# BLIP cache holds (processor, model, device)
BLIP_CACHE: Optional[Tuple[Any, Any, Any]] = None


# --- Cached clients / resources ---
@st.cache_resource
def get_internet_search_engine():
    from ui.internet_search import InternetSearchEngine
    return InternetSearchEngine()


@st.cache_resource
def get_openai_client(api_key: str, base_url: Optional[str] = None):
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)


@st.cache_resource
def get_anthropic_client(api_key: str):
    from anthropic import Anthropic
    return Anthropic(api_key=api_key)


@st.cache_resource
def get_google_client(api_key: str):
    # Import dynamically to avoid hard dependency if not used
    import google.generativeai as genai
    return genai.Client(api_key=api_key)


# --- Conversation helpers ---
def build_conversation_history(messages: List[Dict], exclude_last: bool = True, max_messages: int = 20, max_chars: int = 50000) -> List[Dict]:
    history = messages[:-1] if exclude_last and len(messages) > 0 else messages
    if not history:
        return []
    formatted = [{"role": msg["role"], "content": msg["content"]} for msg in history if "role" in msg and "content" in msg]
    total_chars = sum(len(m.get("content", "")) for m in formatted)
    if len(formatted) > max_messages or total_chars > max_chars:
        older = formatted[:-max_messages] if len(formatted) > max_messages else []
        recent = formatted[-max_messages:]
        if older:
            older_summary_parts = []
            for msg in older[-10:]:
                content = msg.get("content", "")
                preview = content[:200] + "..." if len(content) > 200 else content
                older_summary_parts.append(f"{msg.get('role', 'unknown').upper()}: {preview}")
            summary_text = "[Earlier conversation summary]\n" + "\n".join(older_summary_parts)
            return [{"role": "system", "content": summary_text}] + recent
        else:
            return recent
    return formatted


def create_openai_messages(conversation_history: List[Dict], current_prompt: str, system_instruction: Optional[str] = None) -> List[Dict]:
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": current_prompt})
    return messages


def handle_openai_compatible_provider(
    client: Any,
    model_name: str,
    messages: List[Dict],
    temperature: float,
    max_tokens: int,
    top_p: float,
    enable_streaming: bool
) -> str:
    if enable_streaming:
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True
        )
        collected_chunks = []
        def _iter_chunks():
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                collected_chunks.append(piece)
                yield piece
        # Stream to Streamlit (best-effort)
        try:
            st.write_stream(_iter_chunks())
        except Exception:
            pass
        response_text = "".join(collected_chunks)
        return response_text if response_text else "I apologize, but I couldn't generate a response."
    else:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
        if not response_text:
            response_text = "I apologize, but I couldn't generate a response."
        try:
            st.markdown(response_text)
        except Exception:
            pass
        return response_text


# --- Internet search integration ---
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5) -> tuple[List[Dict], str]:
    if not enable_search:
        return [], ""
    try:
        search_engine = get_internet_search_engine()
        results = search_engine.search(query, max_results=max_results)
        if results:
            from ui.internet_search import create_search_context
            context = create_search_context(results, query)
            logger.info(f"Search completed with {len(results)} results")
            return results, context
        return [], ""
    except Exception as e:
        logger.error(f"Internet search failed: {str(e)}")
        return [], ""


def augment_prompt_with_search(prompt: str, search_results: List[Dict]) -> str:
    if not search_results:
        return prompt
    from ui.internet_search import create_search_context
    context = create_search_context(search_results, prompt)
    augmented = f"""{prompt}

[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]:
{context}

Please use the above search results to provide a current and accurate answer."""
    return augmented


# --- Multimodal helpers ---
def process_images_for_context(images: List) -> List[Dict]:
    results = []
    try:
        from PIL import Image
        for i, img in enumerate(images, 1):
            caption = None
            try:
                info = getattr(img, 'info', {}) or {}
                caption = info.get('description') or info.get('caption')
            except Exception:
                caption = None
            if not caption:
                try:
                    caption = f"Image {i}: {img.width}x{img.height} pixels"
                except Exception:
                    caption = f"Image {i} (unknown size)"
            results.append({"name": f"image_{i}", "caption": caption})
    except Exception as e:
        logger.error(f"process_images_for_context error: {e}")
    return results


def transcribe_audio_file(file_like) -> str:
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_like) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except Exception as e:
            logger.warning(f"Speech recognition failed: {e}")
            return "[Transcription failed or not available]"
    except Exception:
        logger.info("speech_recognition not installed; skipping transcription")
        return "[Transcription unavailable - install speech_recognition]"


def extract_video_frame_thumbnails(file_like, max_frames: int = 3) -> List[str]:
    thumbnails: List[str] = []
    try:
        import importlib
        moviepy = importlib.import_module("moviepy.editor")
        VideoFileClip = getattr(moviepy, "VideoFileClip")
        import tempfile
        from io import BytesIO
        import base64
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as tmp:
            tmp.write(file_like.read())
            tmp.flush()
            clip = VideoFileClip(tmp.name)
            duration = clip.duration or 0
            times = [(i + 1) * duration / (max_frames + 1) for i in range(max_frames)]
            for t in times:
                frame = clip.get_frame(t)
                img = Image.fromarray(frame)
                buf = BytesIO()
                img.thumbnail((320, 320))
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                thumbnails.append(f"data:image/png;base64,{b64}")
            try:
                clip.reader.close()
            except Exception:
                pass
            clip.audio = None
    except Exception as e:
        logger.info(f"moviepy not available or failed to extract frames: {e}")
    return thumbnails


def get_blip_model() -> Tuple[Any, Any, Any]:
    global BLIP_CACHE
    if BLIP_CACHE is not None:
        return BLIP_CACHE
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    BLIP_CACHE = (processor, model, device)
    return BLIP_CACHE


def generate_blip_caption(image) -> Optional[str]:
    try:
        processor, model, device = get_blip_model()
        inputs = processor(images=image, return_tensors="pt").to(device)
        import torch
        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        logger.info(f"BLIP captioning unavailable: {e}")
        return None


def call_hosted_caption_api(image, api_url: str, api_key: Optional[str] = None) -> Optional[str]:
    try:
        import requests
        from io import BytesIO
        buf = BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        files = {'image': ('image.png', buf, 'image/png')}
        headers = {}
        if api_key:
            headers['Authorization'] = f"Bearer {api_key}"
        resp = requests.post(api_url, files=files, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get('caption') or data.get('text')
    except Exception as e:
        logger.info(f"Hosted caption API call failed: {e}")
        return None


def generate_image_captions(images: List, use_blip: bool = False, hosted_api_url: Optional[str] = None, hosted_api_key: Optional[str] = None) -> List[Dict]:
    if not images:
        return []
    results = []
    for i, img in enumerate(images, 1):
        caption = None
        if hosted_api_url:
            try:
                caption = call_hosted_caption_api(img, hosted_api_url, hosted_api_key)
            except Exception as e:
                logger.info(f"Hosted caption call failed for image {i}: {e}")
        if not caption and use_blip:
            try:
                caption = generate_blip_caption(img)
            except Exception as e:
                logger.info(f"BLIP caption failed for image {i}: {e}")
        if not caption:
            fallback = process_images_for_context([img])[0]
            caption = fallback.get('caption')
        results.append({"name": f"image_{i}", "caption": caption})
    return results


def preload_blip_model(timeout: int = 120) -> bool:
    try:
        get_blip_model()
        return True
    except Exception as e:
        logger.info(f"Preload BLIP model failed: {e}")
        return False


def preload_blip_model_with_progress(progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
    global BLIP_CACHE
    try:
        if progress_callback:
            progress_callback(0, "Initializing BLIP preload...")
        if progress_callback:
            progress_callback(10, "Loading BLIP processor...")
        from transformers import BlipProcessor
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        if progress_callback:
            progress_callback(40, "Processor loaded; loading BLIP model...")
        from transformers import BlipForConditionalGeneration
        import torch
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        if progress_callback:
            progress_callback(80, "Model downloaded; moving to device...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        BLIP_CACHE = (processor, model, device)
        if progress_callback:
            progress_callback(100, "BLIP model ready")
        return True
    except Exception as e:
        logger.info(f"Preload BLIP model failed with progress: {e}")
        if progress_callback:
            try:
                progress_callback(100, f"Failed: {e}")
            except Exception:
                pass
        return False

    except Exception as e:
        logger.info(f"extract_video_frame_thumbnails error: {e}")
        return thumbnails
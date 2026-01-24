
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
    genai.configure(api_key=api_key)
    return genai

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


# --- Resilience Helpers ---
import time
import functools

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

# --- Provider Handlers ---
def handle_google_provider(
    api_key: str,
    model_name: str,
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.95,
    images: List = None,
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide a Google API Key."
        import google.generativeai as genai
        # Configure the global instance
        genai.configure(api_key=api_key)

        # Mapping config specifically for GenerativeModel
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            top_p=top_p
        )

        # Initialize model
        # system_instruction is supported in newer versions as init argument or via specific methods
        # For broader compatibility, passing via constructor if supported, else prepending to prompt might be needed
        # But latest SDK supports 'system_instruction' in GenerativeModel constructor
        try:
            model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
        except TypeError:
            # Fallback for older SDK versions that don't support system_instruction in init
            model = genai.GenerativeModel(model_name=model_name)
            if system_instruction:
                prompt = f"{system_instruction}\n\n{prompt}"

        contents = []
        if images:
            from io import BytesIO
            import base64
            for img in images:
                # Gemai SDK can take PIL images directly in 'contents'
                contents.append(img)

        contents.append(prompt)

        @retry_with_backoff(retries=2)
        def _generate():
            # For gemini, we can pass stream=True/False to generate_content
            return model.generate_content(
                contents,
                generation_config=generation_config,
                stream=enable_streaming
            )

        response = _generate()

        if enable_streaming:
            collected_text = []
            def _stream_gen():
                for chunk in response:
                    if chunk.text:
                        collected_text.append(chunk.text)
                        yield chunk.text

            try:
                st.write_stream(_stream_gen())
            except Exception as e:
                logger.warning(f"Google streaming visualization failed: {e}")

            return "".join(collected_text)
        else:
             return response.text

    except Exception as e:
        logger.error(f"Google provider error: {e}")
        return f"Error connecting to Google Gemini: {str(e)}"

def handle_anthropic_provider(
    api_key: str,
    model_name: str,
    messages: List[Dict],
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    enable_streaming: bool = False
) -> str:
    try:
        if not api_key: return "Please provide an Anthropic API Key."
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)

        kwargs = {
             "model": model_name,
             "messages": messages,
             "max_tokens": max_tokens,
             "temperature": temperature,
        }
        if system_instruction:
             kwargs["system"] = system_instruction

        @retry_with_backoff(retries=2)
        def _create_message():
            if enable_streaming:
                return client.messages.create(stream=True, **kwargs)
            else:
                return client.messages.create(stream=False, **kwargs)

        response = _create_message()

        if enable_streaming:
            collected_text = []
            def _stream_gen():
                for event in response:
                    if event.type == 'content_block_delta':
                        text = event.delta.text
                        collected_text.append(text)
                        yield text

            try:
                st.write_stream(_stream_gen())
            except Exception:
                pass
            return "".join(collected_text)
        else:
            return response.content[0].text

    except Exception as e:
         logger.error(f"Anthropic provider error: {e}")
         return f"Error connecting to Anthropic Claude: {str(e)}"

def generate_standard_response(
    provider: str,
    model_name: str,
    api_keys: Dict[str, str],
    prompt: str,
    chat_history: List[Dict],
    system_instruction: str = "",
    config: Dict[str, Any] = {},
    images: List = None
) -> str:
    """Unified dispatcher for standard mode chat generation"""
    api_key = api_keys.get(provider)
    if not api_key:
        return f"❌ Missing API Key for {provider}. Please check sidebar settings."

    try:
        temp = config.get('temperature', 0.7)
        max_tok = config.get('max_tokens', 2048)
        top_p = config.get('top_p', 0.95)
        stream = config.get('enable_streaming', False)

        if provider == "google":
            return handle_google_provider(
                api_key, model_name, prompt, system_instruction,
                temp, max_tok, top_p, images, enable_streaming=stream
            )

        elif provider in ["openai", "together", "xai", "deepseek"]:
            base_urls = {
                "together": "https://api.together.xyz/v1",
                "xai": "https://api.x.ai/v1",
                "deepseek": "https://api.deepseek.com"
            }
            client = get_openai_client(api_key, base_urls.get(provider))
            msgs = create_openai_messages(build_conversation_history(chat_history), prompt, system_instruction)
            return handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)

        elif provider == "anthropic":
            # Anthropic expects just user/assistant messages
            msgs = [{"role": "user", "content": prompt}] # Simplified for this call; ideally use full history if supported
            return handle_anthropic_provider(
                api_key, model_name, msgs, system_instruction,
                temp, max_tok, enable_streaming=stream
            )

        return "Provider not supported."

    except Exception as e:
        return f"Generation Error: {str(e)}"

def prepare_brain_configuration(api_keys: Dict[str, str], requested_models: List[str] = None) -> List[Dict[str, Any]]:
    """Helper to build the list of models for Brain Mode based on available keys"""
    models_to_query = []

    # Default strategy: Use available keys (simplified)
    # In a real app, 'requested_models' would come from user config

    if api_keys.get('google'):
        models_to_query.append({"provider": "google", "model": "gemini-1.5-flash", "api_key": api_keys['google']})

    if api_keys.get('openai'):
        models_to_query.append({"provider": "openai", "model": "gpt-4o-mini", "api_key": api_keys['openai']})

    if api_keys.get('anthropic'):
         models_to_query.append({"provider": "anthropic", "model": "claude-3-5-haiku-20241022", "api_key": api_keys['anthropic']})

    return models_to_query

def handle_openai_compatible_provider(
    client: Any,
    model_name: str,
    messages: List[Dict],
    temperature: float,
    max_tokens: int,
    top_p: float,
    enable_streaming: bool
) -> str:
    @retry_with_backoff(retries=2)
    def _create_completion(stream_mode):
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream_mode
        )

    if enable_streaming:
        try:
            stream = _create_completion(True)
        except Exception as e:
            return f"Error: {str(e)}"

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
        try:
            response = _create_completion(False)
        except Exception as e:
            return f"Error: {str(e)}"

        response_text = getattr(response.choices[0].message, 'content', None) or response.choices[0].message['content']
        if not response_text:
            response_text = "I apologize, but I couldn't generate a response."
        try:
            st.markdown(response_text)
        except Exception:
            pass
        return response_text


# --- Internet search integration ---
def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5, search_type: str = "Web", time_range: str = "Anytime", domain: str = None) -> tuple[List[Dict], str]:
    if not enable_search:
        return [], ""
    try:
        search_engine = get_internet_search_engine()

        if search_type == "News":
             # News search generally supports time range implicitly by recency,
             # but standard DDG news api might handle max_results.
             # If we want detailed time filtering for news, we'd need to extend it,
             # but for now we route to search_news.
             results = search_engine.search_news(query, max_results=max_results)
        else:
             # Standard Web Search with filters
             results = search_engine.search(query, max_results=max_results, time_range=time_range, domain=domain)

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


def generate_blip_caption(image) -> Optional[str]:
    """Generates a caption for the provided image using the BLIP model."""
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


@st.cache_resource(show_spinner=False)
def _load_blip_resources():
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch

    model_id = "Salesforce/blip-image-captioning-base"

    # helper to load with retry strategy
    def load_with_fallback(cls, model_id):
        # 1. Try local cache first
        try:
            return cls.from_pretrained(model_id, local_files_only=True)
        except Exception:
            # 2. Try download
            return cls.from_pretrained(model_id, local_files_only=False)

    processor = load_with_fallback(BlipProcessor, model_id)
    model = load_with_fallback(BlipForConditionalGeneration, model_id)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return processor, model, device

def get_blip_model():
    return _load_blip_resources()

def preload_blip_model_with_progress(progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
    """
    Simulated progress loader that actually just triggers the cached resource load.
    Since st.cache_resource handles the singleton, we just call it.
    """
    try:
        if progress_callback:
            progress_callback(10, "Checking local cache...")

        # We'll use a thread/process safe check by just calling the cached function
        # Streamlit's cache will handle the heavy lifting.

        if progress_callback:
             progress_callback(30, "Loading BLIP model items...")

        # This will block until loaded
        _load_blip_resources()

        if progress_callback:
            progress_callback(100, "BLIP model ready")
        return True
    except Exception as e:
        logger.error(f"BLIP load failed: {e}")
        if progress_callback:
             progress_callback(0, f"Failed: {str(e)}")
        return False

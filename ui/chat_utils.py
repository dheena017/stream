
import streamlit as st
import google.generativeai as genai
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

@st.cache_resource
def get_internet_search_engine():
    """Cached Internet Search Engine initialization"""
    from ui.internet_search import InternetSearchEngine
    return InternetSearchEngine()

@st.cache_resource
def get_openai_client(api_key: str, base_url: Optional[str] = None):
    """Cached OpenAI client initialization"""
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

@st.cache_resource
def get_anthropic_client(api_key: str):
    """Cached Anthropic client initialization"""
    from anthropic import Anthropic
    return Anthropic(api_key=api_key)

@st.cache_resource
def get_google_client(api_key: str):
    """Cached Google Gemini client initialization"""
    return genai.Client(api_key=api_key)

def build_conversation_history(messages: List[Dict], exclude_last: bool = True, max_messages: int = 20, max_chars: int = 50000) -> List[Dict]:
    """Build conversation history with smart summarization"""
    history = messages[:-1] if exclude_last and len(messages) > 0 else messages
    
    if not history:
        return []
    
    # Simple format conversion if needed
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
    """Create messages list for OpenAI-compatible APIs"""
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
    """Handle API calls for OpenAI-compatible providers"""
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
        st.write_stream(_iter_chunks())
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
        response_text = response.choices[0].message.content
        if not response_text:
            response_text = "I apologize, but I couldn't generate a response."
        st.markdown(response_text)
        return response_text

def perform_internet_search(query: str, enable_search: bool = True, max_results: int = 5) -> tuple[List[Dict], str]:
    """
    Perform internet search if enabled
    
    Args:
        query: Search query string
        enable_search: Whether to perform search
        max_results: Maximum number of results
    
    Returns:
        Tuple of (search_results, context_string)
    """
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
    """
    Augment user prompt with internet search results for better context
    
    Args:
        prompt: Original user prompt
        search_results: List of search results
    
    Returns:
        Augmented prompt with search context
    """
    if not search_results:
        return prompt
    
    from ui.internet_search import create_search_context
    context = create_search_context(search_results, prompt)
    
    augmented = f"""{prompt}

[SUPPLEMENTED WITH REAL-TIME WEB SEARCH RESULTS]:
{context}

Please use the above search results to provide a current and accurate answer."""
    
    return augmented


def process_images_for_context(images: List) -> List[Dict]:
    """Generate lightweight context for a list of PIL Images.

    Returns list of dicts: {name: str, caption: str}
    This function uses Pillow only and a very small heuristic captioner when
    no advanced model is available.
    """
    results = []
    try:
        from PIL import Image
        for i, img in enumerate(images, 1):
            caption = None
            # If image has info/description metadata, prefer it
            try:
                info = getattr(img, 'info', {}) or {}
                caption = info.get('description') or info.get('caption')
            except Exception:
                caption = None

            # Fallback: provide a simple size-based caption
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
    """Transcribe audio file-like object to text.

    This attempts to use `speech_recognition` if available, otherwise returns
    a short placeholder indicating transcription is not available.
    """
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        # speech_recognition accepts a path or AudioFile-like object
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
    """Extract small thumbnails (as base64 strings) from a video file-like object.

    Requires `moviepy`. Returns list of base64-encoded PNG images. If moviepy
    is not available, returns an empty list.
    """
    thumbnails = []
    try:
        from moviepy.editor import VideoFileClip
        import tempfile
        from io import BytesIO
        import base64

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as tmp:
            tmp.write(file_like.read())
            tmp.flush()
            clip = VideoFileClip(tmp.name)
            duration = clip.duration or 0
            times = [(i + 1) * duration / (max_frames + 1) for i in range(max_frames)]
            for t in times:
                frame = clip.get_frame(t)
                from PIL import Image
                img = Image.fromarray(frame)
                buf = BytesIO()
                img.thumbnail((320, 320))
                img.save(buf, format='PNG')
                b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                thumbnails.append(f"data:image/png;base64,{b64}")
            clip.reader.close()
            clip.audio = None
    except Exception as e:
        logger.info(f"moviepy not available or failed to extract frames: {e}")
    return thumbnails


def generate_blip_caption(image) -> Optional[str]:
    """Generate an image caption using BLIP model (Salesforce/blip-image-captioning-base).

    Returns caption string on success or None if BLIP is unavailable.
    """
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)

        # Prepare inputs
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            output_ids = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        logger.info(f"BLIP captioning unavailable: {e}")
        return None


def generate_image_captions(images: List, use_blip: bool = False) -> List[Dict]:
    """Generate captions for a list of PIL images.

    If `use_blip` is True, attempt BLIP captioning per image and fall back to
    `process_images_for_context` heuristics when BLIP is not available.
    Returns list of {name, caption} dictionaries.
    """
    if not images:
        return []
    results = []
    if use_blip:
        for i, img in enumerate(images, 1):
            cap = generate_blip_caption(img)
            if not cap:
                # fallback
                fallback = process_images_for_context([img])[0]
                cap = fallback.get('caption')
            results.append({"name": f"image_{i}", "caption": cap})
    else:
        results = process_images_for_context(images)
    return results
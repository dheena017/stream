
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

import streamlit as st
import google.generativeai as genai
from typing import List, Dict, Optional, Any

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

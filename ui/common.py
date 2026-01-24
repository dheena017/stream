
from typing import Any, Dict

import streamlit as st

from ui.config import MODEL_PRICING

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    if "google_oauth_token" in st.session_state:
        del st.session_state.google_oauth_token
    if "user_info" in st.session_state:
        del st.session_state.user_info
    st.rerun()

def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English"""
    if not text:
        return 0
    return len(text) // 4

def calculate_cost(model: str, input_text: str, output_text: str) -> float:
    """Calculate estimated cost for a request"""
    pricing = MODEL_PRICING.get(model, (1.0, 1.0))  # Default fallback
    input_tokens = estimate_tokens(input_text)
    output_tokens = estimate_tokens(output_text)
    
    input_cost = (input_tokens / 1_000_000) * pricing[0]
    output_cost = (output_tokens / 1_000_000) * pricing[1]
    
    return input_cost + output_cost

def get_session_cost() -> Dict[str, Any]:
    """Calculate total session cost from messages"""
    total_cost = 0.0
    cost_by_provider = {}
    
    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages):
        if msg["role"] == "assistant":
            model = msg.get("model", "unknown")
            provider = msg.get("provider", "unknown")
            
            # Get previous user message for input estimation
            input_text = messages[i-1]["content"] if i > 0 else ""
            output_text = msg["content"]
            
            cost = calculate_cost(model, input_text, output_text)
            total_cost += cost
            
            if provider not in cost_by_provider:
                cost_by_provider[provider] = 0.0
            cost_by_provider[provider] += cost
    
    return {
        "total": total_cost,
        "by_provider": cost_by_provider,
        "message_count": len([m for m in messages if m["role"] == "assistant"])
    }

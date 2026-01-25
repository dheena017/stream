<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import asyncio
import time
from datetime import datetime

import streamlit as st
from PIL import Image
=======

import asyncio
from datetime import datetime
import time

from PIL import Image
import streamlit as st
>>>>>>> origin/code-quality-refactor-17423438479402428749

from brain import AIBrain
from ui.chat_utils import (
    augment_prompt_with_search,
    extract_video_frame_thumbnails,
    generate_image_captions,
    generate_standard_response,
    perform_internet_search,
<<<<<<< HEAD
=======
    preload_blip_model_with_progress,
>>>>>>> origin/code-quality-refactor-17423438479402428749
    prepare_brain_configuration,
    transcribe_audio_file,
)
from ui.config import PROVIDER_ICONS


def show_chat_page():
<<<<<<< HEAD
    """
    Display the main chat interface of the application.

    This function handles:
    1. Rendering the chat header and status bar.
    2. Displaying the empty state/welcome screen if no history exists.
    3. Rendering the conversation history with multimodal support (images, files).
    4. Providing action buttons for messages (copy, regenerate).
    5. Configuration sections for Internet Search and File Uploads.
    6. Handling user input and dispatching it to the selected AI provider (Standard or Brain Mode).
    7. Managing database persistence for conversation history.
    """
=======

=======
>>>>>>> 673954a (Resilience: [error handling])
import streamlit as st
=======

import streamlit as st
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======

import streamlit as st
>>>>>>> performance-optimization-13534932852089819512
=======

import streamlit as st
>>>>>>> security-hardening-12270959347982184821
=======

import streamlit as st
>>>>>>> origin/engagement-features-5881933724913241534
=======

import streamlit as st
>>>>>>> origin/monitoring-setup-3187580208021102587
=======

import streamlit as st
>>>>>>> origin/ai-review-fixes-11861043321460875374
import os
import time
import base64
import asyncio
import tempfile
import json
import pandas as pd
from datetime import datetime
from io import BytesIO
from PIL import Image
import google.generativeai as genai

from ui.chat_utils import (
    get_openai_client, get_google_client, get_anthropic_client,
    build_conversation_history, create_openai_messages, handle_openai_compatible_provider,
    perform_internet_search, augment_prompt_with_search,
    process_images_for_context, transcribe_audio_file, extract_video_frame_thumbnails,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    generate_image_captions, generate_standard_response, prepare_brain_configuration
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration,
    extract_file_text
>>>>>>> performance-optimization-13534932852089819512
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> security-hardening-12270959347982184821
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/ai-review-fixes-11861043321460875374
)
from brain import AIBrain
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.config import MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======

>>>>>>> origin/ai-review-fixes-11861043321460875374

def run_async(coro):
    """Safe wrapper for asyncio.run that handles existing event loops"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    else:
        return asyncio.run(coro)

def show_chat_page():
    """Display the main chat interface"""
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
def show_chat_page():
    """Display the main chat interface"""
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
def show_chat_page():
    """Display the main chat interface"""
>>>>>>> performance-optimization-13534932852089819512
=======
from ui.security import sanitize_html

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> security-hardening-12270959347982184821
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
)
from brain import AIBrain
from brain_learning import LearningBrain
from ui.engagement import update_engagement
from ui.database import save_feedback
from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.config import MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/engagement-features-5881933724913241534
=======
from ui.monitoring import log_metric

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
    """Display the main chat interface"""
>>>>>>> origin/code-quality-refactor-17423438479402428749

    # --- 1. Header & Status Bar ---
    # Compact Header
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        st.markdown(
            """
=======
        st.markdown("""
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
        st.markdown("""
>>>>>>> 673954a (Resilience: [error handling])
=======
        st.markdown("""
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
        st.markdown("""
>>>>>>> performance-optimization-13534932852089819512
=======
        st.markdown("""
>>>>>>> security-hardening-12270959347982184821
=======
        st.markdown("""
>>>>>>> origin/engagement-features-5881933724913241534
=======
        st.markdown("""
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
        st.markdown("""
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
        st.markdown("""
>>>>>>> origin/code-quality-refactor-17423438479402428749
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">🤖</div>
            <div>
                <h2 style="margin: 0; font-weight: 700; color: white;">Multi-Provider Chat</h2>
                <div style="display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 0.25rem;">
                    <span class="subtle-text">GPT-4</span>
                    <span class="subtle-text">•</span>
                    <span class="subtle-text">Claude</span>
                    <span class="subtle-text">•</span>
                    <span class="subtle-text">Gemini</span>
                </div>
            </div>
        </div>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        """,
            unsafe_allow_html=True,
        )

    with c_head2:
        # Mini Status Details
        provider = st.session_state.get("selected_provider", "google").upper()
        brain_on = st.session_state.get("enable_brain_mode", False)
        inet_on = st.session_state.get("enable_internet_search", False)
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
        """, unsafe_allow_html=True)

    with c_head2:
        # Mini Status Details
        provider = st.session_state.get('selected_provider', 'google').upper()
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
        safe_provider = sanitize_html(provider)

        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> security-hardening-12270959347982184821
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/engagement-features-5881933724913241534
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/code-quality-refactor-17423438479402428749

        status_html = f"""
        <div style="text-align: right;">
            <div class="status-badge {'active' if brain_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px;">
                {'🧠 Brain' if brain_on else '🤖 Std'}
            </div>
             <div class="status-badge {'active' if inet_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px; margin-left:4px;">
                {'🌐 Web' if inet_on else '📱 Off'}
            </div>
            <div style="margin-top: 4px; font-weight: 600; font-size: 0.9rem; color: var(--accent-primary);">
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                 🔌 {provider}
=======
                 🔌 {safe_provider}
>>>>>>> security-hardening-12270959347982184821
=======
                 🔌 {provider}
>>>>>>> origin/engagement-features-5881933724913241534
=======
                 🔌 {provider}
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                 🔌 {provider}
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                 🔌 {provider}
>>>>>>> origin/code-quality-refactor-17423438479402428749
            </div>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)

    st.markdown("---")

    # --- 2. Input Logic Implementation Prep ---
    # We must define prompt here to capture button clicks from Empty State
    prompt = None

    # --- 3. Chat History or Welcome Screen ---
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    messages = st.session_state.get("messages", [])

    if not messages:
        # ZERO STATE: Welcome Screen
        user_name = st.session_state.get("username", "Traveler")

        st.markdown(
            f"""
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
    messages = st.session_state.get('messages', [])

    if not messages:
        # ZERO STATE: Welcome Screen
        user_name = st.session_state.get('username', 'Traveler')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

        st.markdown(f"""
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
        <div class="welcome-container">
            <div class="welcome-title">Welcome back, {user_name}! 👋</div>
=======
        safe_user_name = sanitize_html(user_name)

        st.markdown(f"""
        <div class="welcome-container">
            <div class="welcome-title">Welcome back, {safe_user_name}! 👋</div>
>>>>>>> security-hardening-12270959347982184821
=======
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

        st.markdown(f"""
        <div class="welcome-container">
            <div class="welcome-title">Welcome back, {user_name}! 👋</div>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
            <div class="welcome-subtitle">
                I'm your intelligent assistant. Select a starter or type below to begin.
            </div>
        </div>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        """,
            unsafe_allow_html=True,
        )
=======
        """, unsafe_allow_html=True)
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
        """, unsafe_allow_html=True)
>>>>>>> 673954a (Resilience: [error handling])
=======
        """, unsafe_allow_html=True)
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
        """, unsafe_allow_html=True)
>>>>>>> performance-optimization-13534932852089819512
=======
        """, unsafe_allow_html=True)
>>>>>>> security-hardening-12270959347982184821
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/engagement-features-5881933724913241534
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/code-quality-refactor-17423438479402428749

        wc1, wc2 = st.columns(2)
        with wc1:
            if st.button("🚀 Explain Quantum Computing", use_container_width=True):
                prompt = "Explain quantum computing in simple terms."
            if st.button("📝 Write a Python Script", use_container_width=True):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                prompt = "Write a python script to parse a CSV file and plot it."
        with wc2:
            if st.button("📰 Search Latest News", use_container_width=True):
                prompt = "What are the latest tech news headlines today?"
            if st.button("🎨 Analyze an Image", use_container_width=True):
                prompt = "Help me analyze an image I'm about to upload."
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                 prompt = "Write a python script to parse a CSV file and plot it."
        with wc2:
             if st.button("📰 Search Latest News", use_container_width=True):
                 prompt = "What are the latest tech news headlines today?"
             if st.button("🎨 Analyze an Image", use_container_width=True):
                 prompt = "Help me analyze an image I'm about to upload."
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)

    # 4. Filter logic (kept from original)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    chat_search = st.session_state.get("chat_search_value", "")
    messages_to_display = messages
    if chat_search:
        messages_to_display = [
            m for m in messages if chat_search.lower() in m.get("content", "").lower()
        ]
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
    chat_search = st.session_state.get('chat_search_value', '')
    messages_to_display = messages
    if chat_search:
        messages_to_display = [m for m in messages if chat_search.lower() in m.get('content', '').lower()]
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
        st.info(f"🔍 Found {len(messages_to_display)} matching messages")

    model_icons = PROVIDER_ICONS

    for idx, msg in enumerate(messages_to_display):
        with st.chat_message(msg["role"]):
            # Images
            if "images" in msg and msg["images"]:
                cols = st.columns(min(len(msg["images"]), 3))
                for i, img in enumerate(msg["images"]):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    with cols[i % 3]:
=======
                    with cols[i%3]:
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                    with cols[i%3]:
>>>>>>> 673954a (Resilience: [error handling])
=======
                    with cols[i%3]:
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                    with cols[i%3]:
>>>>>>> performance-optimization-13534932852089819512
=======
                    with cols[i%3]:
>>>>>>> security-hardening-12270959347982184821
=======
                    with cols[i%3]:
>>>>>>> origin/engagement-features-5881933724913241534
=======
                    with cols[i%3]:
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                    with cols[i%3]:
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                    with cols[i%3]:
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        st.image(img, width="stretch")

            # Files info
            if "files" in msg and msg["files"]:
                for file_info in msg["files"]:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    st.caption(f"📎 {file_info.get('name')} ({file_info.get('type')})")
=======
                     st.caption(f"📎 {file_info.get('name')} ({file_info.get('type')})")
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)

            # Content
            st.markdown(msg["content"])
=======
                     st.caption(f"📎 {file_info.get('name')} ({file_info.get('type')})")

            # Content
            if msg["content"].startswith("Error:"):
                 st.error(msg["content"])
            else:
                 st.markdown(msg["content"])
>>>>>>> 673954a (Resilience: [error handling])
=======
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                     st.caption(f"📎 {file_info.get('name')} ({file_info.get('type')})")

            # Content
            st.markdown(msg["content"])
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

            # Metadata footer
            if msg["role"] == "assistant":
                st.markdown("---")
                mc1, mc2, mc3 = st.columns([0.6, 0.2, 0.2])
                with mc1:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    prov = msg.get("provider", "")
                    mod = msg.get("model", "")
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> 673954a (Resilience: [error handling])
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> performance-optimization-13534932852089819512
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> security-hardening-12270959347982184821
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/engagement-features-5881933724913241534
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/code-quality-refactor-17423438479402428749
                    icon = model_icons.get(prov, "🤖")
                    st.caption(f"{icon} {mod} • {msg.get('timestamp','')}")

                with mc2:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    if "response_time" in msg:
                        st.caption(f"⚡ {msg['response_time']:.2f}s")
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> 673954a (Resilience: [error handling])
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> performance-optimization-13534932852089819512
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> security-hardening-12270959347982184821
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/engagement-features-5881933724913241534
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/code-quality-refactor-17423438479402428749

                with mc3:
                    # Action buttons
                    c_copy, c_regen = st.columns(2)
                    with c_copy:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                        if st.button(
                            "📋", key=f"copy_{idx}", help="View raw text to copy"
                        ):
                            st.code(msg["content"], language=None)
                    with c_regen:
                        if st.button(
                            "🔄",
                            key=f"regen_{idx}",
                            help="Regenerate (Not implemented yet)",
                        ):
                            st.toast("Regeneration coming soon!")

    # 4. Internet Search Configuration
    with st.expander(
        "🌐 Internet Search Settings",
        expanded=st.session_state.get("enable_internet_search", False),
    ):
=======
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        if st.button("📋", key=f"copy_{idx}", help="View raw text to copy"):
                            st.code(msg["content"], language=None)
                    with c_regen:
                        if st.button("🔄", key=f"regen_{idx}", help="Regenerate (Not implemented yet)"):
                             st.toast("Regeneration coming soon!")

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                        if st.button("📋", key=f"copy_{idx}", help="View raw text to copy"):
                            st.code(msg["content"], language=None)
                    with c_regen:
                        if st.button("🔄", key=f"regen_{idx}", help="Regenerate response"):
                            try:
                                real_idx = st.session_state.messages.index(msg)
                                if real_idx > 0:
                                    prev_msg = st.session_state.messages[real_idx - 1]
                                    if prev_msg["role"] == "user":
                                        st.session_state.retry_prompt = prev_msg["content"]
                                        st.session_state.messages.pop(real_idx)
                                        st.session_state.messages.pop(real_idx - 1)
                                        st.rerun()
                            except ValueError:
                                st.error("Could not locate message.")

    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
    # Suggestions
    if messages_to_display and messages_to_display[-1]["role"] == "assistant":
        st.markdown("###### 💡 Suggestions")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("Tell me more", use_container_width=True, key=f"sugg_more_{len(messages)}"):
                prompt = "Tell me more about that."
        with s_col2:
            if st.button("Summarize", use_container_width=True, key=f"sugg_sum_{len(messages)}"):
                prompt = "Can you summarize the main points?"
        with s_col3:
            if st.button("Simplify", use_container_width=True, key=f"sugg_simp_{len(messages)}"):
                prompt = "Explain that in simpler terms."

    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/engagement-features-5881933724913241534
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/code-quality-refactor-17423438479402428749

        c_search1, c_search2 = st.columns([1, 1])
        with c_search1:
            enable_internet = st.toggle(
                "Enable Real-time Search",
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                value=st.session_state.get("enable_internet_search", False),
                help="Augment answers with live web data",
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> 673954a (Resilience: [error handling])
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> performance-optimization-13534932852089819512
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> security-hardening-12270959347982184821
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/engagement-features-5881933724913241534
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/code-quality-refactor-17423438479402428749
            )
            st.session_state.enable_internet_search = enable_internet

            search_type = st.radio(
                "Search Mode",
                ["Web", "News"],
                horizontal=True,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                index=0 if st.session_state.get("search_type") != "News" else 1,
                key="search_type_selector",
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> 673954a (Resilience: [error handling])
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> performance-optimization-13534932852089819512
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> security-hardening-12270959347982184821
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/engagement-features-5881933724913241534
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/code-quality-refactor-17423438479402428749
            )
            st.session_state.search_type = search_type

        with c_search2:
            result_count = st.slider(
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                "Result Count", 1, 10, st.session_state.get("search_result_count", 5)
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> 673954a (Resilience: [error handling])
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> performance-optimization-13534932852089819512
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> security-hardening-12270959347982184821
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/engagement-features-5881933724913241534
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/code-quality-refactor-17423438479402428749
            )
            st.session_state.search_result_count = result_count

            # Future-proofing for time filtering
            time_range = st.selectbox(
                "Time Range",
                ["Anytime", "Past Day", "Past Week", "Past Month"],
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                index=0,
=======
                index=0
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                index=0
>>>>>>> 673954a (Resilience: [error handling])
=======
                index=0
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                index=0
>>>>>>> performance-optimization-13534932852089819512
=======
                index=0
>>>>>>> security-hardening-12270959347982184821
=======
                index=0
>>>>>>> origin/engagement-features-5881933724913241534
=======
                index=0
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                index=0
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                index=0
>>>>>>> origin/code-quality-refactor-17423438479402428749
            )
            st.session_state.search_time_range = time_range

        # Optional Domain Filter
        domain_filter = st.text_input(
            "Limit to Site (optional)",
            placeholder="e.g. reddit.com, stackoverflow.com",
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            help="Restrict search results to a specific domain",
=======
            help="Restrict search results to a specific domain"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
            help="Restrict search results to a specific domain"
>>>>>>> 673954a (Resilience: [error handling])
=======
            help="Restrict search results to a specific domain"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
            help="Restrict search results to a specific domain"
>>>>>>> performance-optimization-13534932852089819512
=======
            help="Restrict search results to a specific domain"
>>>>>>> security-hardening-12270959347982184821
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/engagement-features-5881933724913241534
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/code-quality-refactor-17423438479402428749
        )
        st.session_state.search_domain_filter = domain_filter

    # 5. Multimodal Uploads Area
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    multimodal_options = [
        "Images",
        "Documents (PDF/TXT)",
        "Audio Files",
        "Video Frames",
    ]
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> 673954a (Resilience: [error handling])
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> performance-optimization-13534932852089819512
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> security-hardening-12270959347982184821
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/engagement-features-5881933724913241534
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

    uploaded_images = []
    uploaded_file_info = []
    extra_context = ""
    search_results = []

    # 7. Multimodal Uploads Area
    with st.expander("📎 Upload Files & Images", expanded=False):
        uploaded_files = st.file_uploader(
            "Upload files",
            type=["jpg", "jpeg", "png", "pdf", "txt", "md", "mp3", "wav", "mp4"],
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            accept_multiple_files=True,
=======
            accept_multiple_files=True
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
            accept_multiple_files=True
>>>>>>> 673954a (Resilience: [error handling])
=======
            accept_multiple_files=True
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
            accept_multiple_files=True
>>>>>>> performance-optimization-13534932852089819512
=======
            accept_multiple_files=True
>>>>>>> security-hardening-12270959347982184821
=======
            accept_multiple_files=True
>>>>>>> origin/engagement-features-5881933724913241534
=======
            accept_multiple_files=True
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
            accept_multiple_files=True
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
            accept_multiple_files=True
>>>>>>> origin/code-quality-refactor-17423438479402428749
        )

        if uploaded_files:
            for file in uploaded_files:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                file_ext = file.name.split(".")[-1].lower()
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> 673954a (Resilience: [error handling])
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                file_ext = file.name.split('.')[-1].lower()

                # Get file content as bytes once for processing and caching
                file_bytes = file.getvalue()
>>>>>>> performance-optimization-13534932852089819512
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> security-hardening-12270959347982184821
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/engagement-features-5881933724913241534
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/code-quality-refactor-17423438479402428749

                # Images
                if file_ext in ["jpg", "jpeg", "png", "webp"]:
                    img = Image.open(file)
                    uploaded_images.append(img)
                    uploaded_file_info.append({"name": file.name, "type": "Image"})
                    st.success(f"Image: {file.name}")

                # PDF/TXT
                elif file_ext in ["pdf", "txt", "md"]:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> security-hardening-12270959347982184821
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/engagement-features-5881933724913241534
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/code-quality-refactor-17423438479402428749
                            pdf = PyPDF2.PdfReader(file)
                            text = ""
                            for page in pdf.pages[:5]:
                                text += page.extract_text() + "\n"
                            extra_context += f"\n--- PDF {file.name} ---\n{text}\n"
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                            uploaded_file_info.append(
                                {"name": file.name, "type": "PDF"}
                            )
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> 673954a (Resilience: [error handling])
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> security-hardening-12270959347982184821
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/engagement-features-5881933724913241534
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/code-quality-refactor-17423438479402428749
                            st.success(f"PDF: {file.name}")
                        except ImportError:
                            st.error("PyPDF2 not installed")
                    else:
                        text = file.read().decode("utf-8")
                        extra_context += f"\n--- {file.name} ---\n{text}\n"
                        uploaded_file_info.append({"name": file.name, "type": "Text"})
                        st.success(f"Text: {file.name}")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
                    text = extract_file_text(file_ext, file_bytes, file.name)
                    extra_context += text
                    uploaded_file_info.append({"name": file.name, "type": "Text/PDF"})
                    st.success(f"Processed: {file.name}")
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

                # Audio files
                if file_ext in ["mp3", "wav"]:
                    try:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

                        audio_buf = BytesIO(file_bytes)
                        transcription = transcribe_audio_file(audio_buf)
                        extra_context += f"\n--- Audio {file.name} (transcript) ---\n{transcription}\n"
                        uploaded_file_info.append(
                            {
                                "name": file.name,
                                "type": "Audio",
                                "transcript": transcription,
                            }
                        )
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> security-hardening-12270959347982184821
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/engagement-features-5881933724913241534
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        audio_buf = BytesIO(file_bytes)
                        transcription = transcribe_audio_file(audio_buf)
                        extra_context += f"\n--- Audio {file.name} (transcript) ---\n{transcription}\n"
                        uploaded_file_info.append({"name": file.name, "type": "Audio", "transcript": transcription})
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                        transcription = transcribe_audio_file(file_bytes)
                        extra_context += f"\n--- Audio {file.name} (transcript) ---\n{transcription}\n"
                        uploaded_file_info.append({"name": file.name, "type": "Audio", "transcript": transcription})
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        st.success(f"Audio processed: {file.name}")
                    except Exception as e:
                        st.warning(f"Audio processing failed: {e}")

                # Video files
                if file_ext in ["mp4", "mov"]:
                    try:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                        from io import BytesIO
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                        from io import BytesIO
>>>>>>> security-hardening-12270959347982184821
=======
                        from io import BytesIO
>>>>>>> origin/engagement-features-5881933724913241534
=======
                        from io import BytesIO
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                        from io import BytesIO
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                        from io import BytesIO
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        file_bytes = file.read()
                        video_buf = BytesIO(file_bytes)
                        thumbs = extract_video_frame_thumbnails(video_buf, max_frames=3)
                        if thumbs:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                            uploaded_file_info.append(
                                {
                                    "name": file.name,
                                    "type": "Video",
                                    "thumbnails": thumbs,
                                }
                            )
                            # display small gallery
                            cols = st.columns(min(len(thumbs), 3))
                            for i, b64 in enumerate(thumbs):
                                with cols[i % 3]:
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                        thumbs = extract_video_frame_thumbnails(file_bytes, max_frames=3)
                        if thumbs:
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                            uploaded_file_info.append({"name": file.name, "type": "Video", "thumbnails": thumbs})
                            # display small gallery
                            cols = st.columns(min(len(thumbs), 3))
                            for i, b64 in enumerate(thumbs):
                                with cols[i%3]:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                                    st.image(b64)
                            extra_context += f"\n--- Video {file.name} - {len(thumbs)} thumbnails extracted ---\n"
                            st.success(f"Video processed: {file.name}")
                        else:
                            st.info("No thumbnails extracted")
                    except Exception as e:
                        st.warning(f"Video processing failed: {e}")

    # Advanced captioning option (move outside upload loop)
    adv_caption = st.checkbox(
        "🖼️ Enable Advanced Image Captioning (BLIP)",
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        value=st.session_state.get("enable_advanced_captioning", False),
        help="Use BLIP model locally to generate richer image captions if installed",
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> 673954a (Resilience: [error handling])
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> performance-optimization-13534932852089819512
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> security-hardening-12270959347982184821
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/engagement-features-5881933724913241534
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/code-quality-refactor-17423438479402428749
    )
    st.session_state.enable_advanced_captioning = adv_caption

    # Hosted caption API settings (optional)
    if adv_caption:
        # Check readiness without triggering download/load
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

        # Check if the resource is already cached in Streamlit
        # We can try to peek or just rely on a session state flag that indicates explicit load success
        model_ready = st.session_state.get("blip_loaded", False)

        if not model_ready:
            st.warning("⚠️ High Performance Model Required")
            st.caption(
                "Advanced captioning requires downloading the BLIP model (~1GB). This happens only once."
            )

            if st.button("⬇️ Download & Load BLIP Model"):
                from ui.chat_utils import preload_blip_model_with_progress

=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
        from ui.chat_utils import get_blip_model
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

        # Check if the resource is already cached in Streamlit
        # We can try to peek or just rely on a session state flag that indicates explicit load success
        model_ready = st.session_state.get('blip_loaded', False)

        if not model_ready:
            st.warning("⚠️ High Performance Model Required")
            st.caption("Advanced captioning requires downloading the BLIP model (~1GB). This happens only once.")

            if st.button("⬇️ Download & Load BLIP Model"):
<<<<<<< HEAD
                from ui.chat_utils import preload_blip_model_with_progress
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                progress_bar = st.progress(0)
                status_text = st.empty()

                def _progress_callback(percent: int, message: str):
                    try:
                        progress_bar.progress(min(max(int(percent), 0), 100))
                        status_text.text(message)
                    except Exception:
                        pass

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                with st.spinner("Downloading BLIP model..."):
                    ok = preload_blip_model_with_progress(
                        progress_callback=_progress_callback
                    )
                    if ok:
                        st.session_state["blip_loaded"] = True
                        progress_bar.progress(100)
                        status_text.text("Model loaded successfully!")
                        st.success("BLIP model ready")
                        st.rerun()
                    else:
                        st.error("Failed to load BLIP model.")
        else:
            st.success("✅ BLIP Model Ready")

        # Hosted URL options
        with st.expander("Hosted Caption API (Alternative)", expanded=False):
            hosted_url = st.text_input(
                "Hosted Caption API URL",
                value=st.session_state.get("hosted_caption_url", ""),
                help="External captioning service URL",
            )
            st.session_state.hosted_caption_url = hosted_url
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                with st.spinner('Downloading BLIP model...'):
                    ok = preload_blip_model_with_progress(progress_callback=_progress_callback)
                    if ok:
                        st.session_state['blip_loaded'] = True
                        progress_bar.progress(100)
                        status_text.text('Model loaded successfully!')
                        st.success('BLIP model ready')
                        st.rerun()
                    else:
                         st.error("Failed to load BLIP model.")
        else:
             st.success("✅ BLIP Model Ready")

        # Hosted URL options
        with st.expander("Hosted Caption API (Alternative)", expanded=False):
             hosted_url = st.text_input(
                "Hosted Caption API URL",
                value=st.session_state.get('hosted_caption_url', ''),
                help="External captioning service URL"
            )
             st.session_state.hosted_caption_url = hosted_url
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
=======

    # Check for retry trigger
    if "retry_prompt" in st.session_state and st.session_state.retry_prompt:
        prompt = st.session_state.retry_prompt
        del st.session_state.retry_prompt
>>>>>>> 673954a (Resilience: [error handling])
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> performance-optimization-13534932852089819512
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> security-hardening-12270959347982184821
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/engagement-features-5881933724913241534
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/code-quality-refactor-17423438479402428749

    # We still need to render the chat input widget to allow typing
    input_prompt = st.chat_input("Ask anything...")

    if input_prompt:
        prompt = input_prompt

    # Check voice mode override if not already set
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    if not prompt and st.session_state.get("voice_mode"):
        # Simple simulation specific logic check
        # (In a real app, this would be an audio buffer handling block)
        pass
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
    if not prompt and st.session_state.get('voice_mode'):
         # Simple simulation specific logic check
         # (In a real app, this would be an audio buffer handling block)
         pass
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

    # 5. Processing
    if prompt:
        # User Message Object
        user_msg = {
            "role": "user",
            "content": prompt,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "images": uploaded_images,
            "files": uploaded_file_info,
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> 673954a (Resilience: [error handling])
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> performance-optimization-13534932852089819512
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> security-hardening-12270959347982184821
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> origin/engagement-features-5881933724913241534
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
>>>>>>> origin/code-quality-refactor-17423438479402428749
        }
        st.session_state.messages.append(user_msg)

        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

        try:
            if "conversation_id" not in st.session_state:
                user_id = st.session_state.get("username", "guest")
                # Smart title generation
                title = (prompt[:30] + "..") if len(prompt) > 30 else prompt
                st.session_state.conversation_id = create_new_conversation(
                    user_id, title
                )
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
        try:
            if 'conversation_id' not in st.session_state:
                user_id = st.session_state.get('username', 'guest')
                # Smart title generation
                title = (prompt[:30] + '..') if len(prompt) > 30 else prompt
                st.session_state.conversation_id = create_new_conversation(user_id, title)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

            # Save to DB
            save_message(
                st.session_state.conversation_id,
                "user",
                prompt,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                {
                    "images": bool(uploaded_images),
                    "files": [f["name"] for f in uploaded_file_info],
                },
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
>>>>>>> 673954a (Resilience: [error handling])
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
>>>>>>> performance-optimization-13534932852089819512
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
>>>>>>> security-hardening-12270959347982184821
            )
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )

            # --- ENGAGEMENT UPDATE ---
            eng_result = update_engagement(user_id, "brain_mode" if st.session_state.get('enable_brain_mode') else "message")
            if eng_result['level_up']:
                st.toast(f"🎉 Level Up! You are now Level {eng_result['new_level']}!", icon="🆙")
                st.balloons()
            for ach in eng_result.get('new_achievements', []):
                st.toast(f"🏆 Achievement Unlocked: {ach['name']}", icon="🏅")

>>>>>>> origin/engagement-features-5881933724913241534
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )
>>>>>>> origin/code-quality-refactor-17423438479402428749
        except Exception as e:
            # Don't block chat if DB fails
            print(f"DB Save Error: {e}")

        with st.chat_message("user"):
            if uploaded_images:
                cols = st.columns(min(len(uploaded_images), 3))
                for i, img in enumerate(uploaded_images):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    with cols[i % 3]:
=======
                    with cols[i%3]:
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                    with cols[i%3]:
>>>>>>> 673954a (Resilience: [error handling])
=======
                    with cols[i%3]:
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                    with cols[i%3]:
>>>>>>> performance-optimization-13534932852089819512
=======
                    with cols[i%3]:
>>>>>>> security-hardening-12270959347982184821
=======
                    with cols[i%3]:
>>>>>>> origin/engagement-features-5881933724913241534
=======
                    with cols[i%3]:
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                    with cols[i%3]:
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                    with cols[i%3]:
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        st.image(img, width="stretch")
            if uploaded_file_info:
                for f in uploaded_file_info:
                    st.caption(f"📎 {f['name']}")
            st.markdown(prompt)

        with st.chat_message("assistant"):
            start_time = time.time()

            final_prompt = prompt
            if extra_context:
                final_prompt += f"\n\nContext:\n{extra_context}"

            # Multimodal processing: images -> captions
            if uploaded_images:
                try:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    use_blip = st.session_state.get("enable_advanced_captioning", False)
                    img_context = generate_image_captions(
                        uploaded_images, use_blip=use_blip
                    )
                    if img_context:
                        img_texts = "\n".join(
                            [f"{it['name']}: {it['caption']}" for it in img_context]
                        )
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                    use_blip = st.session_state.get('enable_advanced_captioning', False)
                    img_context = generate_image_captions(uploaded_images, use_blip=use_blip)
                    if img_context:
                        img_texts = "\n".join([f"{it['name']}: {it['caption']}" for it in img_context])
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        final_prompt += f"\n\nImage Context:\n{img_texts}"
                except Exception as e:
                    st.warning(f"Image processing error: {e}")

            # Internet Search Integration
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            if st.session_state.get("enable_internet_search", False):
                with st.spinner("🔍 Searching the internet..."):
                    # Pass new filters to helper
                    search_type_val = st.session_state.get("search_type", "Web")
                    time_range_val = st.session_state.get(
                        "search_time_range", "Anytime"
                    )
                    domain_val = st.session_state.get("search_domain_filter", None)
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
                        final_prompt += f"\n\nImage Context:\n{img_texts}"
                except Exception as e:
                    st.warning(f"Image processing error: {e}")
                    log_metric("error", {"message": str(e), "context": "image_processing"})

            # Internet Search Integration
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
            if st.session_state.get('enable_internet_search', False):
                with st.spinner("🔍 Searching the internet..."):
                    # Pass new filters to helper
                    search_type_val = st.session_state.get('search_type', 'Web')
                    time_range_val = st.session_state.get('search_time_range', 'Anytime')
                    domain_val = st.session_state.get('search_domain_filter', None)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

                    search_results, search_context = perform_internet_search(
                        prompt,
                        enable_search=True,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                        max_results=st.session_state.get("search_result_count", 5),
                        search_type=search_type_val,
                        time_range=time_range_val,
                        domain=domain_val,
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        max_results=st.session_state.get('search_result_count', 5),
                        search_type=search_type_val,
                        time_range=time_range_val,
                        domain=domain_val
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                    )

                    if search_results:
                        st.success(f"📡 Found {len(search_results)} web results")

                        # Display search results
                        with st.expander("🌐 Search Results", expanded=False):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                            from ui.internet_search import (
                                format_search_results_for_chat,
                            )

                            search_display = format_search_results_for_chat(
                                search_results, "web"
                            )
                            st.markdown(search_display)

                        # Augment prompt with search results
                        final_prompt = augment_prompt_with_search(
                            prompt, search_results
                        )

            # Gather API keys once
            api_key_map = {
                "google": st.session_state.get("google_api_key"),
                "openai": st.session_state.get("openai_api_key"),
                "anthropic": st.session_state.get("anthropic_api_key"),
                "together": st.session_state.get("together_api_key"),
                "xai": st.session_state.get("xai_api_key"),
                "deepseek": st.session_state.get("deepseek_api_key"),
            }

            # Brain Mode Logic
            if st.session_state.get("enable_brain_mode"):
                st.info("🧠 Brain processing...")
                brain = AIBrain()
                brain.internet_enabled = st.session_state.get("enable_internet", True)
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                            from ui.internet_search import format_search_results_for_chat
                            search_display = format_search_results_for_chat(search_results, "web")
                            st.markdown(search_display)

                        # Augment prompt with search results
                        final_prompt = augment_prompt_with_search(prompt, search_results)

            # Gather API keys once
            api_key_map = {
                "google": st.session_state.get('google_api_key'),
                "openai": st.session_state.get('openai_api_key'),
                "anthropic": st.session_state.get('anthropic_api_key'),
                "together": st.session_state.get('together_api_key'),
                "xai": st.session_state.get('xai_api_key'),
                "deepseek": st.session_state.get('deepseek_api_key'),
            }

            # Brain Mode Logic
            if st.session_state.get('enable_brain_mode'):
                st.info("🧠 Brain processing...")
                brain = AIBrain()
                brain.internet_enabled = st.session_state.get('enable_internet', True)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

                models_to_query = prepare_brain_configuration(api_key_map)

                if not models_to_query:
                    response_text = "Please configure API keys (Google, OpenAI, or Claude) to use Brain Mode."
                else:
                    try:
                        config = {"temperature": 0.7, "max_output_tokens": 1024}

                        # Internet Search
                        internet_ctx = ""
                        if brain.internet_enabled:
                            with st.spinner("Searching internet..."):
                                internet_ctx = brain.gather_internet_context(prompt)
                                if internet_ctx:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                                    final_prompt += (
                                        f"\n\nInternet Info:\n{internet_ctx}"
                                    )

                        # Query Models
                        # Async execution wrapper
                        responses = asyncio.run(
                            brain.query_multiple_models(
                                final_prompt, models_to_query, config
                            )
                        )

                        # Synthesize
                        response_text = brain.synthesize_responses(
                            prompt, responses, internet_ctx
                        )
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                                    final_prompt += f"\n\nInternet Info:\n{internet_ctx}"

                        # Query Models
                        # Async execution wrapper
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
                        responses = run_async(brain.query_multiple_models(final_prompt, models_to_query, config))

                        # Synthesize
                        response_text = brain.synthesize_responses(prompt, responses, internet_ctx)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                        responses = asyncio.run(brain.query_multiple_models(final_prompt, models_to_query, config))

                        # Synthesize
                        response_text = brain.synthesize_responses(prompt, responses, internet_ctx)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

                        # Show comparison
                        with st.expander("Model Comparison"):
                            for r in responses:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                                st.markdown(
                                    f"**{r['provider'].upper()}**: {r.get('success', False)}"
                                )
                                st.text(r.get("response", "")[:200] + "...")
=======
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")
>>>>>>> 673954a (Resilience: [error handling])
=======
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")
>>>>>>> performance-optimization-13534932852089819512
=======
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")
>>>>>>> security-hardening-12270959347982184821
=======
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")
>>>>>>> origin/engagement-features-5881933724913241534

                    except Exception as e:
                        response_text = f"Brain Error: {e}"
=======
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")

                    except Exception as e:
                        response_text = f"Brain Error: {e}"
<<<<<<< HEAD
<<<<<<< HEAD
                        log_metric("error", {"message": str(e), "context": "brain_mode"})
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

                provider = "brain-mode"
                model_name = "ensemble"

            else:
                # Standard Mode
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                provider = st.session_state.get("selected_provider", "google")
                model_name = st.session_state.get(
                    "selected_model_name", "gemini-1.5-flash"
                )

                config = {
                    "temperature": st.session_state.get("temperature", 1.0),
                    "max_tokens": st.session_state.get("max_tokens", 2048),
                    "top_p": st.session_state.get("top_p", 0.95),
                    "enable_streaming": st.session_state.get("enable_streaming", True),
                }

                sys_prompt = st.session_state.get("system_instruction", "")
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                provider = st.session_state.get('selected_provider', 'google')
                model_name = st.session_state.get('selected_model_name', 'gemini-1.5-flash')

                config = {
                    "temperature": st.session_state.get('temperature', 1.0),
                    "max_tokens": st.session_state.get('max_tokens', 2048),
                    "top_p": st.session_state.get('top_p', 0.95),
                    "enable_streaming": st.session_state.get('enable_streaming', True)
                }

                sys_prompt = st.session_state.get('system_instruction', "")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749

                response_text = generate_standard_response(
                    provider=provider,
                    model_name=model_name,
                    api_keys=api_key_map,
                    prompt=final_prompt,
                    chat_history=st.session_state.messages,
                    system_instruction=sys_prompt,
                    config=config,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    images=uploaded_images,
                )

            end_time = time.time()
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "response_time": end_time - start_time,
                    "provider": provider,
                    "model": model_name,
                }
            )

            # --- DB SAVE: ASSISTANT ---
            try:
                if "conversation_id" in st.session_state:
                    save_message(
                        st.session_state.conversation_id,
                        "assistant",
                        response_text,
                        {
                            "provider": provider,
                            "model": model_name,
                            "response_time": end_time - start_time,
                        },
                    )
            except Exception as e:
                print(f"DB Save Assistant Error: {e}")

            if st.session_state.get("voice_mode") and st.session_state.get(
                "auto_speak"
            ):
=======
=======
>>>>>>> 673954a (Resilience: [error handling])
=======
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
>>>>>>> performance-optimization-13534932852089819512
=======
>>>>>>> security-hardening-12270959347982184821
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
                    images=uploaded_images
                )

            end_time = time.time()
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
            duration = end_time - start_time

            # Monitoring Log
            log_metric("response_time", {
                "duration": duration,
                "provider": provider,
                "model": model_name,
                "brain_mode": st.session_state.get('enable_brain_mode', False)
            })
            log_metric("usage", {
                "provider": provider,
                "model": model_name,
                "timestamp": datetime.now().isoformat()
            })

>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().strftime('%H:%M:%S'),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                "response_time": end_time - start_time,
=======
                "response_time": duration,
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                "response_time": end_time - start_time,
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                "response_time": end_time - start_time,
>>>>>>> origin/code-quality-refactor-17423438479402428749
                "provider": provider,
                "model": model_name
            })

            # --- DB SAVE: ASSISTANT ---
            try:
                if 'conversation_id' in st.session_state:
                     save_message(st.session_state.conversation_id, "assistant", response_text, {
                        "provider": provider, "model": model_name, "response_time": end_time - start_time
                     })
            except Exception as e:
                 print(f"DB Save Assistant Error: {e}")

            if st.session_state.get('voice_mode') and st.session_state.get('auto_speak'):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
                pass

            st.rerun()
=======

import streamlit as st
import os
import time
from loguru import logger
import base64
import asyncio
import tempfile
import json
import pandas as pd
from datetime import datetime
from io import BytesIO
from PIL import Image
import google.generativeai as genai

from ui.chat_utils import (
    get_openai_client, get_google_client, get_anthropic_client,
    build_conversation_history, create_openai_messages, handle_openai_compatible_provider,
    perform_internet_search, augment_prompt_with_search,
    process_images_for_context, transcribe_audio_file, extract_video_frame_thumbnails, 
    generate_image_captions, generate_standard_response, prepare_brain_configuration
)
from brain import AIBrain
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.config import MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS

def show_chat_page():
    """Display the main chat interface"""
    
    # --- 1. Header & Status Bar ---
    # Compact Header
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown("""
<<<<<<< HEAD
<<<<<<< HEAD
        <div class="chat-header-container">
            <div class="header-icon">🤖</div>
=======
        <div role="region" aria-label="Chat Header" style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;" aria-hidden="true">🤖</div>
>>>>>>> origin/accessibility-improvements-8538246568398497801
            <div>
                <h2 class="chat-title">Multi-Provider Chat</h2>
                <div class="chat-subtitle">
=======
        <div class="chat-header-container" style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;" role="img" aria-label="Robot Icon">🤖</div>
            <div>
                <h2 class="header-title" style="margin: 0; font-weight: 700; color: white;">Multi-Provider Chat</h2>
                <div style="display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 0.25rem;">
>>>>>>> origin/ui-ux-improvements-15420733255677191781
                    <span class="subtle-text">GPT-4</span>
                    <span class="subtle-text">•</span>
                    <span class="subtle-text">Claude</span>
                    <span class="subtle-text">•</span>
                    <span class="subtle-text">Gemini</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c_head2:
        # Mini Status Details
        provider = st.session_state.get('selected_provider', 'google').upper()
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
        
        status_html = f"""
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        <div class="chat-status-container">
            <div class="status-badge {'active' if brain_on else ''} chat-status-badge">
=======
        <div class="header-status-container" style="text-align: right;">
            <div class="status-badge {'active' if brain_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px;">
>>>>>>> origin/mobile-optimizations-15403240101322836592
                {'🧠 Brain' if brain_on else '🤖 Std'}
            </div>
             <div class="status-badge {'active' if inet_on else ''} chat-status-badge chat-status-badge-ml">
                {'🌐 Web' if inet_on else '📱 Off'}
=======
        <div role="status" aria-label="System Status" style="text-align: right;">
            <div class="status-badge {'active' if brain_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px;" aria-label="Brain Mode {'Active' if brain_on else 'Standard'}">
                <span aria-hidden="true">{'🧠 Brain' if brain_on else '🤖 Std'}</span>
            </div>
             <div class="status-badge {'active' if inet_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px; margin-left:4px;" aria-label="Internet Search {'Enabled' if inet_on else 'Disabled'}">
                <span aria-hidden="true">{'🌐 Web' if inet_on else '📱 Off'}</span>
>>>>>>> origin/accessibility-improvements-8538246568398497801
            </div>
            <div class="chat-provider-status">
=======
        <div class="status-container" style="text-align: right;">
            <div class="status-badge {'active' if brain_on else ''}" title="{'Brain Mode Active' if brain_on else 'Standard Mode'}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px;">
                {'🧠 Brain' if brain_on else '🤖 Std'}
            </div>
             <div class="status-badge {'active' if inet_on else ''}" title="{'Internet Search Enabled' if inet_on else 'Internet Search Disabled'}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px; margin-left:4px;">
                {'🌐 Web' if inet_on else '📱 Off'}
            </div>
            <div style="margin-top: 4px; font-weight: 600; font-size: 0.9rem; color: var(--accent-primary);" title="Selected Provider: {provider}">
>>>>>>> origin/ui-ux-improvements-15420733255677191781
                 🔌 {provider}
            </div>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)

    st.markdown("---")

    # --- 2. Input Logic Implementation Prep ---
    # We must define prompt here to capture button clicks from Empty State
    prompt = None

    # --- 3. Chat History or Welcome Screen ---
    messages = st.session_state.get('messages', [])
    
    if not messages:
        # ZERO STATE: Welcome Screen
        user_name = st.session_state.get('username', 'Traveler')
        
        st.markdown(f"""
        <div class="welcome-container" role="main" aria-labelledby="welcome-title">
            <h1 id="welcome-title" class="welcome-title">Welcome back, {user_name}! <span aria-hidden="true">👋</span></h1>
            <p class="welcome-subtitle">
                I'm your intelligent assistant. Select a starter or type below to begin.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        wc1, wc2 = st.columns(2)
        with wc1:
            if st.button("🚀 Explain Quantum Computing", use_container_width=True):
                prompt = "Explain quantum computing in simple terms."
            if st.button("📝 Write a Python Script", use_container_width=True):
                 prompt = "Write a python script to parse a CSV file and plot it."
        with wc2:
             if st.button("📰 Search Latest News", use_container_width=True):
                 prompt = "What are the latest tech news headlines today?"
             if st.button("🎨 Analyze an Image", use_container_width=True):
                 prompt = "Help me analyze an image I'm about to upload."
                 
        st.markdown("<div class='spacer-2rem'></div>", unsafe_allow_html=True)
    
    # 4. Filter logic (kept from original)
    chat_search = st.session_state.get('chat_search_value', '')
    messages_to_display = messages
    if chat_search:
        messages_to_display = [m for m in messages if chat_search.lower() in m.get('content', '').lower()]
        st.info(f"🔍 Found {len(messages_to_display)} matching messages")

    model_icons = PROVIDER_ICONS

    for idx, msg in enumerate(messages_to_display):
        with st.chat_message(msg["role"]):
            # Images
            if "images" in msg and msg["images"]:
                cols = st.columns(min(len(msg["images"]), 3))
                for i, img in enumerate(msg["images"]):
                    with cols[i%3]:
                        st.image(img, width="stretch", caption=f"Uploaded Image {i+1}")
            
            # Files info
            if "files" in msg and msg["files"]:
                for file_info in msg["files"]:
                     st.caption(f"📎 {file_info.get('name')} ({file_info.get('type')})")

            # Content
            st.markdown(msg["content"])
            
            # Metadata footer
            if msg["role"] == "assistant":
                st.markdown("---")
                mc1, mc2, mc3 = st.columns([0.5, 0.2, 0.3])
                with mc1:
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
                    icon = model_icons.get(prov, "🤖")
                    st.caption(f"{icon} {mod} • {msg.get('timestamp','')}")
                
                with mc2:
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
                
                with mc3:
                    # Action buttons
                    c_copy, c_regen, c_up, c_down = st.columns(4)
                    with c_copy:
                        if st.button("📋", key=f"copy_{idx}", help="View raw text to copy"):
                            st.code(msg["content"], language=None)
                    with c_regen:
                        if st.button("🔄", key=f"regen_{idx}", help="Regenerate (Not implemented yet)"):
                             st.toast("Regeneration coming soon!")
                    with c_up:
                        if st.button("👍", key=f"up_{idx}"):
                             st.session_state.learning_brain.register_feedback(msg.get('provider', 'unknown'), True)
                             logger.info(f"Feedback: 👍 for provider={msg.get('provider')}")
                             st.toast("Thanks!")
                    with c_down:
                        if st.button("👎", key=f"down_{idx}"):
                             st.session_state.learning_brain.register_feedback(msg.get('provider', 'unknown'), False)
                             logger.info(f"Feedback: 👎 for provider={msg.get('provider')}")
                             st.toast("Thanks!")
    
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
        
        c_search1, c_search2 = st.columns([1, 1])
        with c_search1:
            enable_internet = st.toggle(
                "Enable Real-time Search",
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
            )
            st.session_state.enable_internet_search = enable_internet
            
            search_type = st.radio(
                "Search Mode", 
                ["Web", "News"], 
                horizontal=True,
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
            )
            st.session_state.search_type = search_type

        with c_search2:
            result_count = st.slider(
                "Result Count", 
                1, 10, 
                st.session_state.get('search_result_count', 5)
            )
            st.session_state.search_result_count = result_count
            
            # Future-proofing for time filtering
            time_range = st.selectbox(
                "Time Range", 
                ["Anytime", "Past Day", "Past Week", "Past Month"], 
                index=0
            )
            st.session_state.search_time_range = time_range

        # Optional Domain Filter
        domain_filter = st.text_input(
            "Limit to Site (optional)", 
            placeholder="e.g. reddit.com, stackoverflow.com",
            help="Restrict search results to a specific domain"
        )
        st.session_state.search_domain_filter = domain_filter
    
    # 5. Multimodal Uploads Area
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
    
    uploaded_images = []
    uploaded_file_info = []
    extra_context = ""
    search_results = []
    
    # 7. Multimodal Uploads Area
    with st.expander("📎 Upload Files & Images", expanded=False):
        uploaded_files = st.file_uploader(
            "Upload files",
            type=["jpg", "jpeg", "png", "pdf", "txt", "md", "mp3", "wav", "mp4"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for file in uploaded_files:
                file_ext = file.name.split('.')[-1].lower()
                
                # Images
                if file_ext in ["jpg", "jpeg", "png", "webp"]:
                    img = Image.open(file)
                    uploaded_images.append(img)
                    uploaded_file_info.append({"name": file.name, "type": "Image"})
                    st.success(f"Image: {file.name}")
                    
                # PDF/TXT
                elif file_ext in ["pdf", "txt", "md"]:
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
                            pdf = PyPDF2.PdfReader(file)
                            text = ""
                            for page in pdf.pages[:5]:
                                text += page.extract_text() + "\n"
                            extra_context += f"\n--- PDF {file.name} ---\n{text}\n"
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
                            st.success(f"PDF: {file.name}")
                        except ImportError:
                            st.error("PyPDF2 not installed")
                    else:
                        text = file.read().decode("utf-8")
                        extra_context += f"\n--- {file.name} ---\n{text}\n"
                        uploaded_file_info.append({"name": file.name, "type": "Text"})
                        st.success(f"Text: {file.name}")

                # Audio files
                if file_ext in ["mp3", "wav"]:
                    try:
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
                        audio_buf = BytesIO(file_bytes)
                        transcription = transcribe_audio_file(audio_buf)
                        extra_context += f"\n--- Audio {file.name} (transcript) ---\n{transcription}\n"
                        uploaded_file_info.append({"name": file.name, "type": "Audio", "transcript": transcription})
                        st.success(f"Audio processed: {file.name}")
                    except Exception as e:
                        st.warning(f"Audio processing failed: {e}")

                # Video files
                if file_ext in ["mp4", "mov"]:
                    try:
                        from io import BytesIO
                        file_bytes = file.read()
                        video_buf = BytesIO(file_bytes)
                        thumbs = extract_video_frame_thumbnails(video_buf, max_frames=3)
                        if thumbs:
                            uploaded_file_info.append({"name": file.name, "type": "Video", "thumbnails": thumbs})
                            # display small gallery
                            cols = st.columns(min(len(thumbs), 3))
                            for i, b64 in enumerate(thumbs):
                                with cols[i%3]:
                                    st.image(b64)
                            extra_context += f"\n--- Video {file.name} - {len(thumbs)} thumbnails extracted ---\n"
                            st.success(f"Video processed: {file.name}")
                        else:
                            st.info("No thumbnails extracted")
                    except Exception as e:
                        st.warning(f"Video processing failed: {e}")

    # Advanced captioning option (move outside upload loop)
    adv_caption = st.checkbox(
        "🖼️ Enable Advanced Image Captioning (BLIP)",
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
    )
    st.session_state.enable_advanced_captioning = adv_caption

    # Hosted caption API settings (optional)
    if adv_caption:
        # Check readiness without triggering download/load
        from ui.chat_utils import get_blip_model
        
        # Check if the resource is already cached in Streamlit
        # We can try to peek or just rely on a session state flag that indicates explicit load success 
        model_ready = st.session_state.get('blip_loaded', False)
        
        if not model_ready:
            st.warning("⚠️ High Performance Model Required")
            st.caption("Advanced captioning requires downloading the BLIP model (~1GB). This happens only once.")
            
            if st.button("⬇️ Download & Load BLIP Model"):
                from ui.chat_utils import preload_blip_model_with_progress
                progress_bar = st.progress(0)
                status_text = st.empty()

                def _progress_callback(percent: int, message: str):
                    try:
                        progress_bar.progress(min(max(int(percent), 0), 100))
                        status_text.text(message)
                    except Exception:
                        pass

                with st.spinner('Downloading BLIP model...'):
                    ok = preload_blip_model_with_progress(progress_callback=_progress_callback)
                    if ok:
                        st.session_state['blip_loaded'] = True
                        progress_bar.progress(100)
                        status_text.text('Model loaded successfully!')
                        st.success('BLIP model ready')
                        st.rerun()
                    else:
                         st.error("Failed to load BLIP model.")
        else:
             st.success("✅ BLIP Model Ready")
             
        # Hosted URL options
        with st.expander("Hosted Caption API (Alternative)", expanded=False):
             hosted_url = st.text_input(
                "Hosted Caption API URL",
                value=st.session_state.get('hosted_caption_url', ''),
                help="External captioning service URL"
            )
             st.session_state.hosted_caption_url = hosted_url
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
    
    # We still need to render the chat input widget to allow typing
    input_prompt = st.chat_input("Ask anything...")
    
    if input_prompt:
        prompt = input_prompt
    
    # Check voice mode override if not already set
    if not prompt and st.session_state.get('voice_mode'):
         # Simple simulation specific logic check
         # (In a real app, this would be an audio buffer handling block)
         pass

    # 5. Processing
    if prompt:
        # User Message Object
        user_msg = {
            "role": "user", 
            "content": prompt, 
            "timestamp": datetime.now().strftime('%H:%M:%S'), 
            "images": uploaded_images, 
            "files": uploaded_file_info
        }
        st.session_state.messages.append(user_msg)
        
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
        try:
            if 'conversation_id' not in st.session_state:
                user_id = st.session_state.get('username', 'guest')
                # Smart title generation
                title = (prompt[:30] + '..') if len(prompt) > 30 else prompt
                st.session_state.conversation_id = create_new_conversation(user_id, title)
            
            # Save to DB
            save_message(
                st.session_state.conversation_id, 
                "user", 
                prompt, 
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )
        except Exception as e:
            # Don't block chat if DB fails
            st.toast(f"Database error: {e}", icon="⚠️")

        with st.chat_message("user"):
            if uploaded_images:
                cols = st.columns(min(len(uploaded_images), 3))
                for i, img in enumerate(uploaded_images):
                    with cols[i%3]:
                        st.image(img, width="stretch")
            if uploaded_file_info:
                for f in uploaded_file_info:
                    st.caption(f"📎 {f['name']}")
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            start_time = time.time()
            
            final_prompt = prompt
            if extra_context:
                final_prompt += f"\n\nContext:\n{extra_context}"

            # Multimodal processing: images -> captions
            if uploaded_images:
                try:
                    use_blip = st.session_state.get('enable_advanced_captioning', False)
                    img_context = generate_image_captions(uploaded_images, use_blip=use_blip)
                    if img_context:
                        img_texts = "\n".join([f"{it['name']}: {it['caption']}" for it in img_context])
                        final_prompt += f"\n\nImage Context:\n{img_texts}"
                except Exception as e:
                    st.warning(f"Image processing error: {e}")
            
            # Internet Search Integration
            if st.session_state.get('enable_internet_search', False):
                with st.spinner("🔍 Searching the internet..."):
                    # Pass new filters to helper
                    search_type_val = st.session_state.get('search_type', 'Web')
                    time_range_val = st.session_state.get('search_time_range', 'Anytime')
                    domain_val = st.session_state.get('search_domain_filter', None)
                    
                    search_results, search_context = perform_internet_search(
                        prompt,
                        enable_search=True,
                        max_results=st.session_state.get('search_result_count', 5),
                        search_type=search_type_val,
                        time_range=time_range_val,
                        domain=domain_val
                    )
                    
                    if search_results:
                        st.success(f"📡 Found {len(search_results)} web results")
                        
                        # Display search results
                        with st.expander("🌐 Search Results", expanded=False):
                            from ui.internet_search import format_search_results_for_chat
                            search_display = format_search_results_for_chat(search_results, "web")
                            st.markdown(search_display)
                        
                        # Augment prompt with search results
                        final_prompt = augment_prompt_with_search(prompt, search_results)
            
            # Gather API keys once
            api_key_map = {
                "google": st.session_state.get('google_api_key'),
                "openai": st.session_state.get('openai_api_key'),
                "anthropic": st.session_state.get('anthropic_api_key'),
                "together": st.session_state.get('together_api_key'),
                "xai": st.session_state.get('xai_api_key'),
                "deepseek": st.session_state.get('deepseek_api_key'),
            }

            # Brain Mode Logic
            if st.session_state.get('enable_brain_mode'):
                st.info("🧠 Brain processing...")
                brain = AIBrain()
                brain.internet_enabled = st.session_state.get('enable_internet', True)
                
                models_to_query = prepare_brain_configuration(api_key_map)
                
                if not models_to_query:
                    response_text = "Please configure API keys (Google, OpenAI, or Claude) to use Brain Mode."
                else:
                    try:
                        config = {"temperature": 0.7, "max_output_tokens": 1024}
                        
                        # Internet Search
                        internet_ctx = ""
                        if brain.internet_enabled:
                            with st.spinner("Searching internet..."):
                                internet_ctx = brain.gather_internet_context(prompt)
                                if internet_ctx:
                                    final_prompt += f"\n\nInternet Info:\n{internet_ctx}"
                        
                        # Query Models
                        # Async execution wrapper
                        responses = asyncio.run(brain.query_multiple_models(final_prompt, models_to_query, config))
                        
                        # Synthesize
                        response_text = brain.synthesize_responses(prompt, responses, internet_ctx)
                        
                        # Show comparison
                        with st.expander("Model Comparison"):
                            for r in responses:
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")
                                
                    except Exception as e:
                        response_text = f"Brain Error: {e}"
                
                provider = "brain-mode"
                model_name = "ensemble"
                
            else:
                # Standard Mode
                provider = st.session_state.get('selected_provider', 'google')
                model_name = st.session_state.get('selected_model_name', 'gemini-1.5-flash')
                
                config = {
                    "temperature": st.session_state.get('temperature', 1.0),
                    "max_tokens": st.session_state.get('max_tokens', 2048),
                    "top_p": st.session_state.get('top_p', 0.95),
                    "enable_streaming": st.session_state.get('enable_streaming', True)
                }
                
                sys_prompt = st.session_state.get('system_instruction', "")
                
                with st.spinner("Generating response..."):
                    response_text = generate_standard_response(
                        provider=provider,
                        model_name=model_name,
                        api_keys=api_key_map,
                        prompt=final_prompt,
                        chat_history=st.session_state.messages,
                        system_instruction=sys_prompt,
                        config=config,
                        images=uploaded_images
                    )
            
            end_time = time.time()
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text, 
                "timestamp": datetime.now().strftime('%H:%M:%S'),
                "response_time": end_time - start_time,
                "provider": provider,
                "model": model_name
            })
            
            # --- DB SAVE: ASSISTANT ---
            try:
                if 'conversation_id' in st.session_state:
                     save_message(st.session_state.conversation_id, "assistant", response_text, {
                        "provider": provider, "model": model_name, "response_time": end_time - start_time
                     })
            except Exception as e:
                 st.toast(f"Database error: {e}", icon="⚠️")
            
            if st.session_state.get('voice_mode') and st.session_state.get('auto_speak'):
                pass
            
            st.rerun()

>>>>>>> d4117c9 (Review: Fix syntax error and refactor inline styles)
=======
                pass

            st.rerun()
>>>>>>> 673954a (Resilience: [error handling])
=======
                pass

            st.rerun()
>>>>>>> 3e83144 (AI Review: Fix ui/chat_utils.py syntax and asyncio crash in ui/chat.py)
=======
                pass

            st.rerun()
>>>>>>> performance-optimization-13534932852089819512
=======
                pass

            st.rerun()
>>>>>>> security-hardening-12270959347982184821
=======
                pass

            st.rerun()
>>>>>>> origin/engagement-features-5881933724913241534
=======
                pass

            st.rerun()
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
                pass

            st.rerun()
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
                pass

            st.rerun()
>>>>>>> origin/code-quality-refactor-17423438479402428749

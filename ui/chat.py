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
=======

import streamlit as st
>>>>>>> origin/engagement-features-3224553925721226807
=======

import streamlit as st
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======

import streamlit as st
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======

import streamlit as st
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======

import streamlit as st
>>>>>>> origin/monitoring-setup-3291123637376011491
=======

import streamlit as st
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

import streamlit as st
>>>>>>> origin/security-fixes-5054230979788780781
=======

import streamlit as st
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======

import streamlit as st
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======

import streamlit as st
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======

import streamlit as st
>>>>>>> origin/engagement-features-7857729897611492638
import os
import time
import base64
import asyncio
import tempfile
import json
import pandas as pd
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
import html
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/engagement-features-7857729897611492638
from datetime import datetime
from io import BytesIO
from PIL import Image
import google.generativeai as genai

<<<<<<< HEAD
=======
from datetime import datetime
from io import BytesIO
from PIL import Image

from ui.database import get_conversation_messages
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/engagement-features-3224553925721226807
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration,
    run_async_safely
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/security-fixes-5054230979788780781
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
    generate_image_captions, generate_standard_response, prepare_brain_configuration
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
from ui.engagement import EngagementManager

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/engagement-features-3224553925721226807
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/monitoring-setup-3291123637376011491
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/security-fixes-5054230979788780781
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
from ui.database import get_conversation_messages

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
from ui.engagement import check_achievements

def show_chat_page():
    """Display the main chat interface"""
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
        st.markdown("""
>>>>>>> origin/engagement-features-3224553925721226807
=======
        st.markdown("""
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        st.markdown("""
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
        st.markdown("""
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
        st.markdown("""
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        st.markdown("""
>>>>>>> origin/security-fixes-5054230979788780781
=======
        st.markdown("""
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        st.markdown("""
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
        st.markdown("""
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
        st.markdown("""
>>>>>>> origin/engagement-features-7857729897611492638
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">🤖</div>
            <div>
                <h2 style="margin: 0; font-weight: 700; color: white;">Multi-Provider Chat</h2>
                <div style="display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 0.25rem;">
                    <span class="subtle-text">GPT-4</span>
                    <span class="subtle-text">•</span>
                    <span class="subtle-text">Claude</span>
                    <span class="subtle-text">•</span>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
        st.markdown("""
        <div role="banner" style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;" aria-hidden="true">🤖</div>
            <div>
                <h2 style="margin: 0; font-weight: 700; color: white;">Multi-Provider Chat</h2>
                <div style="display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 0.25rem;" aria-label="Supported providers">
                    <span class="subtle-text">GPT-4</span>
                    <span class="subtle-text" aria-hidden="true">•</span>
                    <span class="subtle-text">Claude</span>
                    <span class="subtle-text" aria-hidden="true">•</span>
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
        """, unsafe_allow_html=True)

    with c_head2:
        # Mini Status Details
        provider = st.session_state.get('selected_provider', 'google').upper()
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
<<<<<<< HEAD
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
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/engagement-features-3224553925721226807
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/security-fixes-5054230979788780781
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
                 🔌 {provider}
>>>>>>> origin/engagement-features-3224553925721226807
=======
                 🔌 {provider}
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)

        status_html = f"""
        <div role="status" aria-live="polite" style="text-align: right;">
            <div class="status-badge {'active' if brain_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px;" aria-label="Brain mode {'on' if brain_on else 'off'}">
                {'🧠 Brain' if brain_on else '🤖 Std'}
            </div>
             <div class="status-badge {'active' if inet_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px; margin-left:4px;" aria-label="Internet search {'on' if inet_on else 'off'}">
                {'🌐 Web' if inet_on else '📱 Off'}
            </div>
            <div style="margin-top: 4px; font-weight: 600; font-size: 0.9rem; color: var(--accent-primary);">
                 🔌 {provider}
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                 🔌 {provider}
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                 🔌 {provider}
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                 🔌 {provider}
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                 🔌 {provider}
>>>>>>> origin/security-fixes-5054230979788780781
=======
                 🔌 {provider}
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                 🔌 {provider}
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                 🔌 {provider}
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                 🔌 {provider}
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/engagement-features-7857729897611492638
    messages = st.session_state.get('messages', [])

    if not messages:
        # ZERO STATE: Welcome Screen
        user_name = st.session_state.get('username', 'Traveler')
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
=======
        safe_user_name = html.escape(user_name)
>>>>>>> origin/security-fixes-5054230979788780781

        st.markdown(f"""
        <div class="welcome-container">
            <div class="welcome-title">Welcome back, {safe_user_name}! 👋</div>
<<<<<<< HEAD
>>>>>>> security-hardening-12270959347982184821
=======
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
    messages = st.session_state.get('messages', [])

    # Load More Button
    if messages and 'conversation_id' in st.session_state:
        if st.button("⬆️ Load Older Messages", key="load_more_btn", use_container_width=True):
             cid = st.session_state.conversation_id
             current_count = len(messages)
             more_msgs = get_conversation_messages(cid, limit=20, offset=current_count)
             if more_msgs:
                 st.session_state.messages = more_msgs + messages
                 st.rerun()
             else:
                 st.toast("No older messages found.")

    if not messages:
        # ZERO STATE: Welcome Screen
        user_name = st.session_state.get('username', 'Traveler')
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

        st.markdown(f"""
        <div class="welcome-container">
            <div class="welcome-title">Welcome back, {user_name}! 👋</div>
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
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/engagement-features-3224553925721226807
=======

        st.markdown(f"""
        <div class="welcome-container" style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
            <div class="welcome-title" style="margin-bottom: 0.5rem;">Welcome back, {user_name}! 👋</div>
            <div class="welcome-subtitle" style="max-width: 600px; line-height: 1.6;">
                I'm your intelligent assistant. Select a starter or type below to begin.
            </div>
        </div>
        """, unsafe_allow_html=True)
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/security-fixes-5054230979788780781
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
        """, unsafe_allow_html=True)
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        """, unsafe_allow_html=True)

        wc1, wc2 = st.columns(2)
        with wc1:
            if st.button("🚀 Explain Quantum Computing", use_container_width=True, help="Ask about quantum computing basics"):
                prompt = "Explain quantum computing in simple terms."
            if st.button("📝 Write a Python Script", use_container_width=True, help="Ask to generate a Python script for CSV parsing"):
                 prompt = "Write a python script to parse a CSV file and plot it."
        with wc2:
             if st.button("📰 Search Latest News", use_container_width=True, help="Search for today's tech news"):
                 prompt = "What are the latest tech news headlines today?"
             if st.button("🎨 Analyze an Image", use_container_width=True, help="Start image analysis workflow"):
                 prompt = "Help me analyze an image I'm about to upload."
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    chat_search = st.session_state.get('chat_search_value', '')
    messages_to_display = messages

    # Pagination Control
    if 'conversation_id' in st.session_state and not chat_search and messages:
        # Only show pagination if we are in a saved conversation and not searching
        if st.button("⬆️ Load Previous Messages", key="load_more_msgs", type="secondary", use_container_width=True):
            # Use current message count as offset to skip already loaded messages
            current_offset = len(st.session_state.messages)
            c_id = st.session_state.conversation_id

            # Fetch next batch
            older_msgs = get_conversation_messages(c_id, limit=50, offset=current_offset)

            if older_msgs:
                st.session_state.messages = older_msgs + st.session_state.messages
                st.rerun()
            else:
                st.info("No older messages found.")

    if chat_search:
        messages_to_display = [m for m in messages if chat_search.lower() in m.get('content', '').lower()]
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                    with cols[i%3]:
>>>>>>> origin/engagement-features-3224553925721226807
=======
                    with cols[i%3]:
>>>>>>> origin/ui-ux-improvements-11896252316584290961
                        st.image(img, width="stretch")
=======
                    with cols[i%3]:
                        st.image(img, width="stretch", caption=f"Uploaded Image {i+1}")
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/security-fixes-5054230979788780781
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
                     st.caption(f"📎 {file_info.get('name')} ({file_info.get('type')})")

            # Content
            st.markdown(msg["content"])
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
<<<<<<< HEAD
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/engagement-features-3224553925721226807
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/security-fixes-5054230979788780781
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/engagement-features-3224553925721226807
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/security-fixes-5054230979788780781
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
                        if st.button("📋", key=f"copy_{idx}", help="View raw text to copy"):
                            st.code(msg["content"], language=None)
                    with c_regen:
                        if st.button("🔄", key=f"regen_{idx}", help="Regenerate (Not implemented yet)"):
                             st.toast("Regeneration coming soon!")

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
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/engagement-features-3224553925721226807
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                        if st.button("📋", key=f"copy_{idx}", help="View raw text to copy"):
                            st.code(msg["content"], language=None)
                    with c_regen:
                        # Only allow regeneration if search is not active to avoid index confusion
                        if not chat_search and st.button("🔄", key=f"regen_{idx}", help="Regenerate Response"):
                            if idx > 0 and messages[idx-1].get("role") == "user":
                                user_msg = messages[idx-1]
                                st.session_state.regen_prompt = user_msg["content"]
                                st.session_state.regen_images = user_msg.get("images", [])

                                # Truncate history from the user message onwards
                                if "messages" in st.session_state:
                                    st.session_state.messages[:] = st.session_state.messages[:idx-1]

                                st.rerun()
                            else:
                                st.error("Cannot regenerate: previous message not found.")

    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/security-fixes-5054230979788780781
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
    # 4. Internet Search Configuration
    with st.expander("🌐 Internet Search Settings", expanded=st.session_state.get('enable_internet_search', False)):
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/engagement-features-3224553925721226807
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/security-fixes-5054230979788780781
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                value=st.session_state.get('enable_internet_search', False),
                help="Augment answers with live web data"
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/engagement-features-3224553925721226807
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/security-fixes-5054230979788780781
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                index=0 if st.session_state.get('search_type') != "News" else 1,
                key="search_type_selector"
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/engagement-features-3224553925721226807
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/security-fixes-5054230979788780781
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                "Result Count",
                1, 10,
                st.session_state.get('search_result_count', 5)
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                index=0
>>>>>>> origin/engagement-features-3224553925721226807
=======
                index=0
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                index=0
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                index=0
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                index=0
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                index=0
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                index=0
>>>>>>> origin/security-fixes-5054230979788780781
=======
                index=0
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                index=0
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                index=0
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                index=0
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/engagement-features-3224553925721226807
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/security-fixes-5054230979788780781
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
            help="Restrict search results to a specific domain"
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/engagement-features-3224553925721226807
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/security-fixes-5054230979788780781
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
            accept_multiple_files=True
>>>>>>> origin/engagement-features-3224553925721226807
=======
            accept_multiple_files=True
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
            accept_multiple_files=True
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
            accept_multiple_files=True
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
            accept_multiple_files=True
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
            accept_multiple_files=True
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
            accept_multiple_files=True
>>>>>>> origin/security-fixes-5054230979788780781
=======
            accept_multiple_files=True
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            accept_multiple_files=True
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
            accept_multiple_files=True
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
            accept_multiple_files=True
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/engagement-features-3224553925721226807
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/security-fixes-5054230979788780781
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                file_ext = file.name.split('.')[-1].lower()
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/engagement-features-3224553925721226807
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/security-fixes-5054230979788780781
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                    if file_ext == "pdf":
                        try:
                            import PyPDF2
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/engagement-features-3224553925721226807
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/security-fixes-5054230979788780781
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                            uploaded_file_info.append({"name": file.name, "type": "PDF"})
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

                # Audio files
                if file_ext in ["mp3", "wav"]:
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
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/engagement-features-3224553925721226807
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/security-fixes-5054230979788780781
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                        # Keep a buffer copy for transcription helper
                        file_bytes = file.read()
                        from io import BytesIO
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
                        from io import BytesIO
>>>>>>> origin/engagement-features-3224553925721226807
=======
                        from io import BytesIO
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                        from io import BytesIO
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                        from io import BytesIO
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                        from io import BytesIO
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                        from io import BytesIO
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                        from io import BytesIO
>>>>>>> origin/security-fixes-5054230979788780781
=======
                        from io import BytesIO
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                        from io import BytesIO
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                        from io import BytesIO
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                        from io import BytesIO
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/engagement-features-3224553925721226807
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/security-fixes-5054230979788780781
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
        value=st.session_state.get('enable_advanced_captioning', False),
        help="Use BLIP model locally to generate richer image captions if installed"
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/engagement-features-3224553925721226807
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/security-fixes-5054230979788780781
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
        from ui.chat_utils import get_blip_model
>>>>>>> origin/engagement-features-7857729897611492638

        # Check if the resource is already cached in Streamlit
        # We can try to peek or just rely on a session state flag that indicates explicit load success
        model_ready = st.session_state.get('blip_loaded', False)

        if not model_ready:
            st.warning("⚠️ High Performance Model Required")
            st.caption("Advanced captioning requires downloading the BLIP model (~1GB). This happens only once.")

            if st.button("⬇️ Download & Load BLIP Model"):
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
<<<<<<< HEAD
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
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/engagement-features-3224553925721226807
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/security-fixes-5054230979788780781
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                from ui.chat_utils import preload_blip_model_with_progress
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/engagement-features-3224553925721226807
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/security-fixes-5054230979788780781
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
    # 'prompt' might already be set by Welcome Screen buttons or Voice mode simulation
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======

    # Check for regeneration trigger
    if not prompt and "regen_prompt" in st.session_state:
        prompt = st.session_state.pop("regen_prompt")
        saved_imgs = st.session_state.pop("regen_images", [])
        if saved_imgs:
            uploaded_images = saved_imgs
        st.toast("Regenerating response...")
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "images": uploaded_images,
            "files": uploaded_file_info
        }
        st.session_state.messages.append(user_msg)

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
        # --- GAMIFICATION LOGGING ---
        try:
            user_id = st.session_state.get('username', 'guest')
            if user_id:
                engagement = EngagementManager()
                result = engagement.log_activity(user_id, "message_sent")

                if result['level_up']:
                    st.toast(f"🎉 Level Up! You are now Level {result['stats']['level']}!", icon="🆙")

                if result['new_achievements']:
                    for achievement in result['new_achievements']:
                        st.toast(f"🏆 Achievement Unlocked: {achievement['name']}", icon=achievement['icon'])
        except Exception as e:
            print(f"Engagement Error: {e}")

        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/engagement-features-3224553925721226807
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/security-fixes-5054230979788780781
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
        # --- DB SAVE: USER ---
        from ui.database import create_new_conversation, save_message
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )
>>>>>>> origin/engagement-features-3224553925721226807
        except Exception as e:
            # Don't block chat if DB fails
            print(f"DB Save Error: {e}")
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )
        except Exception as e:
            # Don't block chat if DB fails
            st.toast(f"Database Error: {e}", icon="⚠️")
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )
        except Exception as e:
            # Don't block chat if DB fails
            print(f"DB Save Error: {e}")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                {"images": bool(uploaded_images), "files": [f['name'] for f in uploaded_file_info]}
            )

            # --- CHECK ACHIEVEMENTS ---
            learning_brain = st.session_state.get('learning_brain')
            stats = learning_brain.get_learning_stats() if learning_brain else {}
            new_achievements = check_achievements(st.session_state.username, stats)
            for ach in new_achievements:
                st.toast(f"🏆 Achievement Unlocked: {ach['title']}!", icon=ach['icon'])

        except Exception as e:
            # Don't block chat if DB fails
            print(f"DB Save Error: {e}")
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
                    with cols[i%3]:
>>>>>>> origin/engagement-features-3224553925721226807
=======
                    with cols[i%3]:
>>>>>>> origin/ui-ux-improvements-11896252316584290961
                        st.image(img, width="stretch")
=======
                    with cols[i%3]:
                        st.image(img, width="stretch", caption=f"User Image {i+1}")
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/security-fixes-5054230979788780781
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                    with cols[i%3]:
                        st.image(img, width="stretch")
>>>>>>> origin/engagement-features-7857729897611492638
            if uploaded_file_info:
                for f in uploaded_file_info:
                    st.caption(f"📎 {f['name']}")
            st.markdown(prompt)

        with st.chat_message("assistant"):
            start_time = time.time()

            final_prompt = prompt
            if extra_context:
                final_prompt += f"\n\nContext:\n{extra_context}"

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
            # Ethics Check
            from ui.ethics import EthicsEngine
            ethics_engine = EthicsEngine()
            bias_type = ethics_engine.detect_bias(prompt)
            import logging
            logging.getLogger(__name__).info(f"DEBUG: Prompt='{prompt}', Bias='{bias_type}'")
            ethics_disclaimer = ""
            if bias_type:
                ethics_disclaimer = ethics_engine.get_disclaimer()
                st.warning(ethics_disclaimer)
                final_prompt = f"{ethics_engine.get_ethical_guidelines()}\n\n{final_prompt}"

            # Multimodal processing: images -> captions
            if uploaded_images:
                try:
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
            # Multimodal processing: images -> captions
            if uploaded_images:
                try:
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
            # Multimodal processing: images -> captions
            if uploaded_images:
                try:
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
            # Multimodal processing: images -> captions
            if uploaded_images:
                try:
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
                        responses = asyncio.run(brain.query_multiple_models(final_prompt, models_to_query, config))

                        # Synthesize
                        response_text = brain.synthesize_responses(prompt, responses, internet_ctx)
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                        responses = run_async_safely(brain.query_multiple_models(final_prompt, models_to_query, config))

                        # Synthesize
                        response_text = brain.synthesize_responses(prompt, responses, internet_ctx)
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
                                st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                st.text(r.get('response', '')[:200] + "...")

                    except Exception as e:
                        response_text = f"Brain Error: {e}"
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                        log_metric("error", {"message": str(e), "context": "brain_mode"})
>>>>>>> origin/monitoring-setup-3187580208021102587
=======
>>>>>>> origin/ai-review-fixes-11861043321460875374
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638

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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
                    images=uploaded_images
                )

            end_time = time.time()
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
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======

                with st.spinner("✨ Generating response..."):
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
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
                    images=uploaded_images
                )

            if ethics_disclaimer:
                response_text = f"{ethics_disclaimer}\n\n{response_text}"

            end_time = time.time()
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().strftime('%H:%M:%S'),
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
<<<<<<< HEAD
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
=======
                "response_time": end_time - start_time,
>>>>>>> origin/engagement-features-3224553925721226807
=======
                "response_time": end_time - start_time,
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
                "response_time": end_time - start_time,
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
                "response_time": end_time - start_time,
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
                "response_time": end_time - start_time,
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
                "response_time": end_time - start_time,
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
                "response_time": end_time - start_time,
>>>>>>> origin/security-fixes-5054230979788780781
=======
                "response_time": end_time - start_time,
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
                "response_time": end_time - start_time,
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
                "response_time": end_time - start_time,
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
                "response_time": end_time - start_time,
>>>>>>> origin/engagement-features-7857729897611492638
                "provider": provider,
                "model": model_name
            })

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
            # --- MONITORING ---
            try:
                from monitoring import Monitor
                success_status = True
                if response_text and response_text.startswith("Brain Error:"):
                    success_status = False

                Monitor().log_usage(
                    user_id=st.session_state.get('username', 'anonymous'),
                    model=model_name,
                    provider=provider,
                    response_time=end_time - start_time,
                    success=success_status
                )
            except Exception as e:
                print(f"Monitoring Log Error: {e}")

>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
            # --- DB SAVE: ASSISTANT ---
            try:
                if 'conversation_id' in st.session_state:
                     save_message(st.session_state.conversation_id, "assistant", response_text, {
                        "provider": provider, "model": model_name, "response_time": end_time - start_time
                     })
            except Exception as e:
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

from ui.database import get_conversation_messages
from ui.chat_utils import (
    get_openai_client, get_google_client, get_anthropic_client,
    build_conversation_history, create_openai_messages, handle_openai_compatible_provider,
    perform_internet_search, augment_prompt_with_search,
    process_images_for_context, transcribe_audio_file, extract_video_frame_thumbnails, 
    generate_image_captions, generate_standard_response, prepare_brain_configuration,
<<<<<<< HEAD
    safe_run_async
=======
    sanitize_text, RateLimiter
>>>>>>> origin/security-hardening-9145044555925710481
)
from brain import AIBrain
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.config import MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS

def show_chat_page():
    """Display the main chat interface"""
    
    # --- 1. Header & Status Bar ---
    # Compact Header
    c_head1, c_head2 = st.columns([0.7, 0.3])
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
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
                <h2 style="margin: 0; font-weight: 700; color: white; font-size: 1.5rem;">Antigravity AI</h2>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.25rem; font-size: 0.8rem;">
                    <span class="subtle-text">GPT-4 • Claude • Gemini</span>
>>>>>>> origin/ui-ux-improvements-3860328367442600035
                </div>
=======
                <h2 style="margin: 0; font-weight: 700; color: white;">Multi-Provider Chat</h2>
                <ul style="display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 0.25rem; list-style: none; padding: 0;">
                    <li class="subtle-text">GPT-4</li>
                    <li class="subtle-text" aria-hidden="true">•</li>
                    <li class="subtle-text">Claude</li>
                    <li class="subtle-text" aria-hidden="true">•</li>
                    <li class="subtle-text">Gemini</li>
                </ul>
>>>>>>> origin/accessibility-improvements-11788990073009031255
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        <div class="chat-status-container">
            <div class="status-badge {'active' if brain_on else ''} chat-status-badge">
=======
        <div class="header-status-container" style="text-align: right;">
=======
        <div class="header-status-container">
>>>>>>> origin/mobile-optimizations-6398649563128325227
=======
        <style>
        .chat-status-container {{ text-align: right; }}
        @media (max-width: 768px) {{ .chat-status-container {{ text-align: left; margin-top: 0.5rem; }} }}
        </style>
        <div class="chat-status-container">
>>>>>>> origin/mobile-optimization-12966885757340563810
=======
        <div style="text-align: right;" role="status" aria-live="polite">
>>>>>>> origin/accessibility-improvements-11788990073009031255
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
    
    # Load Older Messages Button
    if messages and 'conversation_id' in st.session_state:
        if st.button("⬆️ Load Older Messages", type="secondary", use_container_width=True):
             cid = st.session_state.conversation_id
             current_len = len(messages)
             older_msgs = get_conversation_messages(cid, limit=50, offset=current_len)
             if older_msgs:
                 st.session_state.messages = older_msgs + messages
                 st.rerun()
             else:
                 st.toast("No older messages found.")

    if not messages:
        # ZERO STATE: Welcome Screen
        user_name = st.session_state.get('username', 'Traveler')
        
        st.markdown(f"""
<<<<<<< HEAD
        <div class="welcome-container" role="main" aria-labelledby="welcome-title">
            <h1 id="welcome-title" class="welcome-title">Welcome back, {user_name}! <span aria-hidden="true">👋</span></h1>
            <p class="welcome-subtitle">
=======
        <div class="welcome-container">
            <div class="welcome-title">Welcome back, {sanitize_text(user_name)}! 👋</div>
            <div class="welcome-subtitle">
>>>>>>> origin/security-hardening-9145044555925710481
                I'm your intelligent assistant. Select a starter or type below to begin.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        wc1, wc2 = st.columns(2)
        with wc1:
            if st.button("🚀 Quantum Computing", use_container_width=True, help="Explain quantum computing in simple terms"):
                prompt = "Explain quantum computing in simple terms."
            if st.button("📝 Python Script", use_container_width=True, help="Write a python script to parse a CSV file and plot it"):
                 prompt = "Write a python script to parse a CSV file and plot it."
        with wc2:
             if st.button("📰 Latest News", use_container_width=True, help="What are the latest tech news headlines today?"):
                 prompt = "What are the latest tech news headlines today?"
             if st.button("🎨 Analyze Image", use_container_width=True, help="Help me analyze an image I'm about to upload"):
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
    

    # Experimental: Chat Export
    with st.expander("🧪 Experimental: Chat Export", expanded=False):
        st.caption("Download your conversation history.")

        # Prepare data
        chat_data = st.session_state.get('messages', [])

        # JSON
        try:
            json_str = json.dumps(chat_data, indent=2, default=str)
            st.download_button(
                label="📄 Download as JSON",
                data=json_str,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error preparing JSON export: {e}")

        # Markdown
        try:
            md_lines = ["# Chat Export\n"]
            for msg in chat_data:
                role = msg.get('role', 'unknown').capitalize()
                timestamp = msg.get('timestamp', '')
                content = msg.get('content', '')
                md_lines.append(f"### {role} ({timestamp})")
                md_lines.append(f"{content}\n")
                if msg.get('images'):
                    md_lines.append(f"*(Included {len(msg['images'])} images)*\n")

            md_str = "\n".join(md_lines)
            st.download_button(
                label="📝 Download as Markdown",
                data=md_str,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error preparing Markdown export: {e}")

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
        # Check rate limit
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        user_id = st.session_state.get('username', 'guest')
        if not limiter.check(user_id):
            st.error("⚠️ Rate limit exceeded. Please wait a moment.")
            return

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
                        responses = safe_run_async(brain.query_multiple_models(final_prompt, models_to_query, config))
                        
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
=======
                pass

            st.rerun()
>>>>>>> origin/engagement-features-3224553925721226807
=======
                 st.toast(f"Database Error: {e}", icon="⚠️")

            if st.session_state.get('voice_mode') and st.session_state.get('auto_speak'):
                pass

            st.rerun()
>>>>>>> origin/ui-ux-improvements-11896252316584290961
=======
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638
                 print(f"DB Save Assistant Error: {e}")

            if st.session_state.get('voice_mode') and st.session_state.get('auto_speak'):
                pass

            st.rerun()
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/accessibility-improvements-6998911318674562570
=======
>>>>>>> origin/feature-chat-export-regen-2510491870086228569
=======
>>>>>>> origin/monitoring-setup-3291123637376011491
=======
>>>>>>> origin/code-quality-refactor-brain-and-async-11409629077043540949
=======
>>>>>>> origin/security-fixes-5054230979788780781
=======
>>>>>>> origin/ethics-bias-fixes-10212520104040218540
=======
>>>>>>> origin/jules-3174636693196525980-404a41f2
=======
>>>>>>> origin/scalability-optimizations-11923254205763930774
=======
>>>>>>> origin/engagement-features-7857729897611492638


import streamlit as st
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
    generate_image_captions, generate_standard_response, prepare_brain_configuration
)
from brain import AIBrain
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.config import MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS
from ui.engagement import check_achievements

def show_chat_page():
    """Display the main chat interface"""

    # --- 1. Header & Status Bar ---
    # Compact Header
    c_head1, c_head2 = st.columns([3, 1])
    with c_head1:
        st.markdown("""
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
        """, unsafe_allow_html=True)

    with c_head2:
        # Mini Status Details
        provider = st.session_state.get('selected_provider', 'google').upper()
        brain_on = st.session_state.get('enable_brain_mode', False)
        inet_on = st.session_state.get('enable_internet_search', False)

        status_html = f"""
        <div style="text-align: right;">
            <div class="status-badge {'active' if brain_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px;">
                {'🧠 Brain' if brain_on else '🤖 Std'}
            </div>
             <div class="status-badge {'active' if inet_on else ''}" style="display:inline-flex; width:auto; font-size:0.8rem; padding: 2px 8px; margin-left:4px;">
                {'🌐 Web' if inet_on else '📱 Off'}
            </div>
            <div style="margin-top: 4px; font-weight: 600; font-size: 0.9rem; color: var(--accent-primary);">
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
        <div class="welcome-container">
            <div class="welcome-title">Welcome back, {user_name}! 👋</div>
            <div class="welcome-subtitle">
                I'm your intelligent assistant. Select a starter or type below to begin.
            </div>
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

        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)

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
                        st.image(img, width="stretch")

            # Files info
            if "files" in msg and msg["files"]:
                for file_info in msg["files"]:
                     st.caption(f"📎 {file_info.get('name')} ({file_info.get('type')})")

            # Content
            st.markdown(msg["content"])

            # Metadata footer
            if msg["role"] == "assistant":
                st.markdown("---")
                mc1, mc2, mc3 = st.columns([0.6, 0.2, 0.2])
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
                    c_copy, c_regen = st.columns(2)
                    with c_copy:
                        if st.button("📋", key=f"copy_{idx}", help="View raw text to copy"):
                            st.code(msg["content"], language=None)
                    with c_regen:
                        if st.button("🔄", key=f"regen_{idx}", help="Regenerate (Not implemented yet)"):
                             st.toast("Regeneration coming soon!")

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

            # --- CHECK ACHIEVEMENTS ---
            learning_brain = st.session_state.get('learning_brain')
            stats = learning_brain.get_learning_stats() if learning_brain else {}
            new_achievements = check_achievements(st.session_state.username, stats)
            for ach in new_achievements:
                st.toast(f"🏆 Achievement Unlocked: {ach['title']}!", icon=ach['icon'])

        except Exception as e:
            # Don't block chat if DB fails
            print(f"DB Save Error: {e}")

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
                 print(f"DB Save Assistant Error: {e}")

            if st.session_state.get('voice_mode') and st.session_state.get('auto_speak'):
                pass

            st.rerun()

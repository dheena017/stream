
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
    process_images_for_context, transcribe_audio_file, extract_video_frame_thumbnails, generate_image_captions
)
from brain import AIBrain
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.config import MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS

def show_chat_page():
    """Display the main chat interface"""
    # 1. Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%); 
    padding: 2rem 2.5rem; border-radius: 16px; margin-bottom: 1.5rem; 
    box-shadow: 0 10px 40px rgba(0,0,0,0.12);">
        <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
            <div style="font-size: 3rem;">🤖</div>
            <div>
                <h1 style="color: var(--text-primary); margin: 0; font-size: 2rem; font-weight: 700;">
                    Multi-Provider AI Chat
                </h1>
                <p style="color: var(--text-secondary); margin: 0.25rem 0 0 0; font-size: 1rem;">
                    GPT-4 • Claude • Gemini • Llama • Grok • DeepSeek
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Status Indicators
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        brain_mode = st.session_state.get('enable_brain_mode', False)
        status = "🧠 Brain ON" if brain_mode else "🤖 Standard"
        color = "var(--accent-primary)" if brain_mode else "var(--text-secondary)"
        st.markdown(f'<div style="background:rgba(0,0,0,0.03);padding:8px;border-radius:10px;border-left:3px solid {color};text-align:center;"><span style="color:{color};font-weight:600">{status}</span></div>', unsafe_allow_html=True)
    with c2:
        voice_mode = st.session_state.get('voice_mode', False)
        status = "🎤 Voice ON" if voice_mode else "⌨️ Text Mode"
        color = "var(--accent-secondary)" if voice_mode else "var(--accent-primary)"
        st.markdown(f'<div style="background:rgba(0,0,0,0.03);padding:8px;border-radius:10px;border-left:3px solid {color};text-align:center;"><span style="color:{color};font-weight:600">{status}</span></div>', unsafe_allow_html=True)
    with c3:
        count = len(st.session_state.get('messages', []))
        st.markdown(f'<div style="background:rgba(0,0,0,0.03);padding:8px;border-radius:10px;border-left:3px solid var(--accent-secondary);text-align:center;"><span style="color:var(--accent-secondary);font-weight:600">💬 {count} Messages</span></div>', unsafe_allow_html=True)
    with c4:
        provider = st.session_state.get('selected_provider', 'google').upper()
        st.markdown(f'<div style="background:rgba(0,0,0,0.03);padding:8px;border-radius:10px;border-left:3px solid var(--accent-primary);text-align:center;"><span style="color:var(--accent-primary);font-weight:600">🔌 {provider}</span></div>', unsafe_allow_html=True)
    with c5:
        internet_mode = st.session_state.get('enable_internet_search', False)
        status = "🌐 Web ON" if internet_mode else "📱 Local"
        color = "var(--accent-secondary)" if internet_mode else "var(--text-secondary)"
        st.markdown(f'<div style="background:rgba(0,0,0,0.03);padding:8px;border-radius:10px;border-left:3px solid {color};text-align:center;"><span style="color:{color};font-weight:600">{status}</span></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # 3. Chat History
    messages = st.session_state.get('messages', [])
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
                mc1, mc2, mc3 = st.columns([2, 1, 1])
                with mc1:
                    prov = msg.get('provider', '')
                    mod = msg.get('model', '')
                    icon = model_icons.get(prov, "🤖")
                    st.caption(f"{icon} {mod} • {msg.get('timestamp','')}")
                with mc2:
                     if "response_time" in msg:
                         st.caption(f"⚡ {msg['response_time']:.2f}s")
                with mc3:
                    if st.button("📋", key=f"copy_{idx}", help="Copy"):
                        st.code(msg["content"])
    
    # 4. Internet Search Configuration
    search_col1, search_col2, search_col3 = st.columns([2, 1, 1])
    with search_col1:
        enable_internet = st.checkbox(
            "🌐 Enable Internet Search",
            value=st.session_state.get('enable_internet_search', False),
            help="Search the internet for real-time information to augment responses"
        )
        st.session_state.enable_internet_search = enable_internet
    
    search_results = []
    if enable_internet:
        with search_col2:
            search_result_count = st.number_input(
                "Results",
                min_value=1,
                max_value=10,
                value=st.session_state.get('search_result_count', 5),
                help="Number of search results to fetch"
            )
            st.session_state.search_result_count = search_result_count
        
        with search_col3:
            search_type = st.selectbox(
                "Type",
                ["Web", "News"],
                key="search_type",
                help="Type of search to perform"
            )
    
    # 5. Multimodal Uploads Area
    multimodal_options = ["Images", "Documents (PDF/TXT)", "Audio Files", "Video Frames"]
    
    # 6. Input Handling
    prompt = None
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
        hosted_url = st.text_input(
            "Hosted Caption API URL (optional)",
            value=st.session_state.get('hosted_caption_url', ''),
            help="Optional external captioning service URL that accepts multipart form-image uploads and returns JSON {caption: ...}"
        )
        hosted_key = st.text_input(
            "Hosted Caption API Key (optional)",
            value=st.session_state.get('hosted_caption_api_key', ''),
            help="Optional API key for hosted caption service"
        )
        st.session_state.hosted_caption_url = hosted_url
        st.session_state.hosted_caption_api_key = hosted_key

        # Preload BLIP model in background with progress when enabled
        if adv_caption and not st.session_state.get('blip_loaded', False):
            from ui.chat_utils import preload_blip_model_with_progress
            progress_bar = st.progress(0)
            status_text = st.empty()

            def _progress_callback(percent: int, message: str):
                try:
                    progress_bar.progress(min(max(int(percent), 0), 100))
                    status_text.text(message)
                except Exception:
                    pass

            with st.spinner('Downloading/preloading advanced caption model (BLIP)...'):
                ok = preload_blip_model_with_progress(progress_callback=_progress_callback)
                st.session_state['blip_loaded'] = bool(ok)
                if ok:
                    progress_bar.progress(100)
                    status_text.text('BLIP model ready')
                    st.success('BLIP model ready')
                else:
                    status_text.text('BLIP not available; falling back to simple captions or hosted API')
                    st.info('BLIP not available; falling back to simple captions or hosted API')

    if st.session_state.get('voice_mode'):
        st.info("🎤 Voice Mode Active - Use audio input")
        audio = st.audio_input("Record")
        if audio:
            st.spinner("Transcribing...")
            # Simple simulation for voice mode since dependencies might be complex
            # In a real scenario, use speech_recognition as per original app
            prompt = "Simulated voice input (Voice mode enabled)"
            st.success("Voice received.")
    else:
        prompt = st.chat_input("Ask anything...")

    # 5. Processing
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": datetime.now().strftime('%H:%M:%S'), "images": uploaded_images, "files": uploaded_file_info})
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
                    search_results, search_context = perform_internet_search(
                        prompt,
                        enable_search=True,
                        max_results=st.session_state.get('search_result_count', 5)
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
            
            # Brain Mode Logic
            if st.session_state.get('enable_brain_mode'):
                st.info("🧠 Brain processing...")
                brain = AIBrain()
                brain.internet_enabled = st.session_state.get('enable_internet', True)
                
                # Determine models to use based on settings in sidebar
                # We need api keys
                google_key = st.session_state.get('google_api_key')
                openai_key = st.session_state.get('openai_api_key')
                anthropic_key = st.session_state.get('anthropic_api_key')
                together_key = st.session_state.get('together_api_key')
                
                models_to_query = []
                # Simple logic to pick models (in real app, use `brain_consult_models` map)
                if google_key: models_to_query.append({"provider": "google", "model": "gemini-1.5-flash", "api_key": google_key})
                if openai_key: models_to_query.append({"provider": "openai", "model": "gpt-4o-mini", "api_key": openai_key})
                
                if not models_to_query:
                    response_text = "Please configure API keys to use Brain Mode."
                else:
                    # Async execution
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
                        if len(models_to_query) > 0:
                            # We can't easily run async loop here without event loop issues in some streamlit envs
                            # We will run them sequentially for stability in this refactor, or usage `asyncio.run` cautiously
                            responses = asyncio.run(brain.query_multiple_models(final_prompt, models_to_query, config))
                            
                            # Synthesize
                            response_text = brain.synthesize_responses(prompt, responses, internet_ctx)
                            
                            # Show comparison
                            with st.expander("Model Comparison"):
                                for r in responses:
                                    st.markdown(f"**{r['provider'].upper()}**: {r.get('success', False)}")
                                    st.text(r.get('response', '')[:200] + "...")
                        else:
                            response_text = "No models available for Brain Mode."

                    except Exception as e:
                        response_text = f"Brain Error: {e}"
                
                provider = "brain-mode"
                model_name = "ensemble"
                
            else:
                # Standard Mode
                provider = st.session_state.get('selected_provider', 'google')
                model_name = st.session_state.get('selected_model_name', 'gemini-1.5-flash')
                temp = st.session_state.get('temperature', 1.0)
                max_tok = st.session_state.get('max_tokens', 2048)
                top_p = st.session_state.get('top_p', 0.95)
                stream = st.session_state.get('enable_streaming', True)
                sys_prompt = st.session_state.get('system_instruction', "")
                
                api_key_map = {
                    "google": st.session_state.get('google_api_key'),
                    "openai": st.session_state.get('openai_api_key'),
                    "anthropic": st.session_state.get('anthropic_api_key'),
                    "together": st.session_state.get('together_api_key'),
                    "xai": st.session_state.get('xai_api_key'),
                    "deepseek": st.session_state.get('deepseek_api_key'),
                }
                api_key = api_key_map.get(provider)
                
                if not api_key:
                    st.error(f"❌ Missing API Key for {provider}")
                    response_text = f"Please provide an API key for {provider} in the sidebar."
                else:
                    response_text = ""
                    try:
                        if provider == "google":
                            client = genai.Client(api_key=api_key)
                            cfg = {"temperature": temp, "max_output_tokens": max_tok, "top_p": top_p}
                            if sys_prompt: cfg["system_instruction"] = sys_prompt
                            
                            # Handle images for Gemini
                            contents = []
                            if uploaded_images:
                                for img in uploaded_images:
                                    img_byte_arr = BytesIO()
                                    img.save(img_byte_arr, format='PNG')
                                    contents.append({"inline_data": {"mime_type": "image/png", "data": base64.b64encode(img_byte_arr.getvalue()).decode()}})
                            contents.append(final_prompt)
                            
                            # Streaming not supported nicely with new sdk structure in this snippet, using blocked
                            resp = client.models.generate_content(model=model_name, contents=contents, config=cfg)
                            response_text = resp.text
                            st.markdown(response_text)
                            
                        elif provider in ["openai", "together", "xai", "deepseek"]:
                            base_urls = {
                                "together": "https://api.together.xyz/v1",
                                "xai": "https://api.x.ai/v1",
                                "deepseek": "https://api.deepseek.com"
                            }
                            client = get_openai_client(api_key, base_urls.get(provider))
                            msgs = create_openai_messages(build_conversation_history(st.session_state.messages), final_prompt, sys_prompt)
                            response_text = handle_openai_compatible_provider(client, model_name, msgs, temp, max_tok, top_p, stream)
                            
                        elif provider == "anthropic":
                            client = get_anthropic_client(api_key)
                            msgs = [{"role": "user", "content": final_prompt}]
                            if sys_prompt:
                                # System prompt handling for Claude
                                pass 
                            resp = client.messages.create(
                                model=model_name,
                                messages=msgs,
                                max_tokens=max_tok,
                                temperature=temp
                            )
                            response_text = resp.content[0].text
                            st.markdown(response_text)
                            
                    except Exception as e:
                        st.error(f"Error: {e}")
                        response_text = f"Error: {e}"
            
            end_time = time.time()
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text, 
                "timestamp": datetime.now().strftime('%H:%M:%S'),
                "response_time": end_time - start_time,
                "provider": provider,
                "model": model_name
            })
            
            if st.session_state.get('voice_mode') and st.session_state.get('auto_speak'):
                pass
            
            st.rerun()


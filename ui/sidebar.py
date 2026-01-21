
import streamlit as st
import os
import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any

from ui.common import logout, get_session_cost
from ui.auth import load_user_credentials, save_user_credentials, hash_password
from ui.config import MODEL_OPTIONS, MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS, PROVIDER_LABELS
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator

def render_sidebar():
    """Render the application sidebar and handle settings"""
    with st.sidebar:
        # 1. Header & Theme
        st.markdown("""
        <div class="sidebar-header">
            <h1 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 800; letter-spacing: 0.5px;">⚙️ Control Panel</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### 📍 Navigation")
        col_nav1, col_nav2, col_nav3 = st.columns(3)
        with col_nav1:
            if st.button("📊 Dash", width="stretch", type="primary" if st.session_state.current_page == "dashboard" else "secondary", help="Go to Dashboard"):
                st.session_state.current_page = "dashboard"
                st.rerun()
        with col_nav2:
            if st.button("💬 Chat", width="stretch", type="primary" if st.session_state.current_page == "chat" else "secondary", help="Go to Chat"):
                st.session_state.current_page = "chat"
                st.rerun()
        with col_nav3:
            if st.button("👤 Profile", width="stretch", type="primary" if st.session_state.current_page == "profile" else "secondary", help="Go to Profile"):
                st.session_state.current_page = "profile"
                st.rerun()
        
        st.divider()

        # 2. User Info (Compact)
        user_info = st.session_state.get('user_info', {})
        username = st.session_state.get('username', 'Guest')
        auth_type = '🔐 Google' if 'google_oauth_token' in st.session_state else '🔐 Login'
        
        st.markdown(f"""
        <div class="sidebar-user-card">
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                <span style="font-weight: 600; color: var(--text-primary);">👤 {username}</span>
                <span style="font-size: 0.8rem; background: var(--bg-tertiary); padding: 2px 6px; border-radius: 4px; color: var(--text-secondary);">{auth_type}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Sign Out", key="sidebar_logout_btn", width="stretch"):
            logout()
            
        st.divider()

        # 3. Model Selection
        st.markdown("### 🤖 Model Selection")
        
        # Provider Filter
        provider_filter = st.selectbox(
            "Filter by Provider",
            ["All", "Google", "OpenAI", "Anthropic", "Together AI", "xAI", "DeepSeek"],
            index=0
        )
        
        filtered_models = MODEL_OPTIONS
        if provider_filter != "All":
            provider_map = {
                "Google": "google",
                "OpenAI": "openai",
                "Anthropic": "anthropic",
                "Together AI": "together",
                "xAI": "xai",
                "DeepSeek": "deepseek"
            }
            filtered_models = [m for m in MODEL_OPTIONS if m[2] == provider_map.get(provider_filter)]

        # Model Select Box
        # Build display labels with icons
        display_labels = [f"{PROVIDER_ICONS.get(m[2], '⚪')} {m[0]}" for m in filtered_models]
        model_choice_idx = st.selectbox(
            "Select Model",
            range(len(filtered_models)),
            format_func=lambda i: display_labels[i],
            index=0
        )
        
        selected_model_tuple = filtered_models[model_choice_idx]
        st.session_state.selected_model_label = selected_model_tuple[0]
        st.session_state.selected_model_name = selected_model_tuple[1]
        st.session_state.selected_provider = selected_model_tuple[2]
        
        # Show capabilities
        model_name = selected_model_tuple[1]
        caps = MODEL_CAPABILITIES.get(model_name, [])
        if caps:
            st.caption(" ".join(caps))

        st.divider()

        # 4. API Keys (Collapsible)
        # Initialize API keys if needed (This logic should ideally be in main setup, but safe here)
        if "api_keys_initialized" not in st.session_state:
            st.session_state.google_api_key = os.getenv("GEMINI_API_KEY", "")
            st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
            st.session_state.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
            st.session_state.together_api_key = os.getenv("TOGETHER_API_KEY", "")
            st.session_state.xai_api_key = os.getenv("XAI_API_KEY", "")
            st.session_state.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
            st.session_state.api_keys_initialized = True

        configured_keys = sum([
            bool(st.session_state.google_api_key),
            bool(st.session_state.openai_api_key),
            bool(st.session_state.anthropic_api_key),
            bool(st.session_state.together_api_key),
            bool(st.session_state.xai_api_key),
            bool(st.session_state.deepseek_api_key)
        ])
        
        with st.expander(f"🔑 API Keys ({configured_keys}/6)", expanded=False):
            show_keys = st.checkbox("Show Keys", value=False)
            key_type = "default" if show_keys else "password"
            
            st.session_state.google_api_key = st.text_input("Google API Key", value=st.session_state.google_api_key, type=key_type)
            st.session_state.openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type=key_type)
            st.session_state.anthropic_api_key = st.text_input("Anthropic API Key", value=st.session_state.anthropic_api_key, type=key_type)
            st.session_state.together_api_key = st.text_input("Together AI Key", value=st.session_state.together_api_key, type=key_type)
            st.session_state.xai_api_key = st.text_input("xAI API Key", value=st.session_state.xai_api_key, type=key_type)
            st.session_state.deepseek_api_key = st.text_input("DeepSeek API Key", value=st.session_state.deepseek_api_key, type=key_type)

        st.divider()

        # 5. Generation Settings
        with st.expander("⚙️ Parameters", expanded=False):
            st.session_state.temperature = st.slider("Temperature", 0.0, 2.0, st.session_state.get('temperature', 1.0), 0.1)
            st.session_state.top_p = st.slider("Top P", 0.0, 1.0, st.session_state.get('top_p', 0.95), 0.05)
            st.session_state.max_tokens = st.slider("Max Tokens", 100, 8192, st.session_state.get('max_tokens', 2048), 100)
            st.session_state.enable_streaming = st.checkbox("Enable Streaming", value=st.session_state.get('enable_streaming', True))
            st.session_state.system_instruction = st.text_area("System Prompt", value=st.session_state.get('system_instruction', ""), placeholder="You are a helpful assistant...", height=100)

        st.divider()

        # 6. Brain Mode
        with st.expander("🧠 Brain Mode", expanded=False):
            enable_brain = st.checkbox("Enable AI Brain", value=st.session_state.get('enable_brain_mode', False))
            st.session_state.enable_brain_mode = enable_brain
            
            if enable_brain:
                st.info("🧠 Brain Active")
                st.session_state.enable_internet = st.checkbox("Internet Search", value=st.session_state.get('enable_internet', True))
                st.session_state.brain_auto_select = st.checkbox("Auto-Select Models", value=st.session_state.get('brain_auto_select', True))
                
                st.caption("Consulted Models:")
                c1, c2 = st.columns(2)
                with c1:
                    google = st.checkbox("Google", value=True, disabled=not bool(st.session_state.google_api_key))
                    openai = st.checkbox("OpenAI", value=False, disabled=not bool(st.session_state.openai_api_key))
                with c2:
                    anthropic = st.checkbox("Claude", value=False, disabled=not bool(st.session_state.anthropic_api_key))
                    together = st.checkbox("Llama", value=False, disabled=not bool(st.session_state.together_api_key))
                
                # Logic to store which models to consult (could be stored in session state)
                st.session_state.brain_consult_models = {
                    "google": google, "openai": openai, "anthropic": anthropic, "together": together
                }

        st.divider()

        # 7. Multimodal
        with st.expander("📎 Multimodal", expanded=False):
            if "multimodal_voice_integrator" not in st.session_state:
                st.session_state.multimodal_voice_integrator = MultimodalVoiceIntegrator()
            
            integrator = st.session_state.multimodal_voice_integrator
            integrator.create_multimodal_uploader()
            
            st.markdown("#### Voice")
            st.session_state.voice_mode = st.toggle("Voice Mode", value=st.session_state.get('voice_mode', False))
            st.session_state.auto_speak = st.checkbox("Auto-Speak", value=st.session_state.get('auto_speak', True))
            
        st.divider()
        
        # 8. Stats & Learning
        with st.expander("📊 Learning Brain Stats", expanded=False):
            learning_brain = st.session_state.get('learning_brain')
            if learning_brain:
                stats = learning_brain.get_learning_stats()
                st.metric("Topics", stats.get('total_topics', 0))
                st.metric("Conversations", stats.get('total_conversations', 0))
                
                if st.button("Download Report"):
                     report = learning_brain.format_learning_report()
                     st.download_button("Get Report", report, "report.md")

        # 9. Cost
        with st.expander("💰 Cost Tracking", expanded=False):
            cost_data = get_session_cost()
            st.metric("Total Cost", f"${cost_data['total']:.4f}")
            st.caption(f"Msg Count: {cost_data['message_count']}")
            if cost_data['by_provider']:
                 st.write(cost_data['by_provider'])

        st.divider()
        
        # Chat Controls
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ Clear", width="stretch"):
                st.session_state.messages = []
                st.rerun()
        with c2:
            if st.button("💾 Save", width="stretch"):
                # Simple export
                msgs = st.session_state.get('messages', [])
                text = "\n".join([f"{m['role']}: {m['content']}" for m in msgs])
                st.download_button("TxT", text, "chat.txt")


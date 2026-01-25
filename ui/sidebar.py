<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import json
import os
from datetime import datetime
from typing import Any, Dict

import pandas as pd
import streamlit as st

<<<<<<< HEAD
=======
from ui.common import logout, get_session_cost
from ui.auth import load_user_credentials, save_user_credentials, hash_password
from ui.config import MODEL_OPTIONS, MODEL_PRICING, MODEL_CAPABILITIES, PROVIDER_ICONS, PROVIDER_LABELS
from ui.chat_utils import serialize_messages
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.chat_utils import serialize_messages

def render_sidebar():
    """Render the application sidebar and handle settings"""
    with st.sidebar:
        # 1. Header & Theme
<<<<<<< HEAD
        st.markdown(
            """
        <div class="sidebar-header">
            <h1 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 800; letter-spacing: 0.5px;">⚙️ Control Panel</h1>
=======
        st.markdown("""
        <div class="sidebar-header" role="banner" aria-label="Sidebar Header">
            <h2 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 800; letter-spacing: 0.5px;">
                <span aria-hidden="true">⚙️</span> Control Panel
            </h2>
>>>>>>> origin/accessibility-improvements-8538246568398497801
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown("### 📍 Navigation")
<<<<<<< HEAD
<<<<<<< HEAD
        col_nav1, col_nav2 = st.columns(2)

=======
        col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
>>>>>>> origin/privacy-compliance-updates-15433171418981572602
        with col_nav1:
<<<<<<< HEAD
            if st.button(
                "📊 Dash",
                width="stretch",
                type=(
                    "primary"
                    if st.session_state.current_page == "dashboard"
                    else "secondary"
                ),
                help="Go to Dashboard",
            ):
=======
            if st.button("📊 Dash", key="nav_dash", use_container_width=True, type="primary" if st.session_state.current_page == "dashboard" else "secondary", help="Go to Dashboard"):
>>>>>>> 89c4a85 (Feedback: [integrations])
=======
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1.2])
        with col_nav1:
            if st.button("📊 Dash", use_container_width=True, type="primary" if st.session_state.current_page == "dashboard" else "secondary", help="Go to Dashboard"):
>>>>>>> origin/ui-ux-improvements-3860328367442600035
                st.session_state.current_page = "dashboard"
                st.rerun()
            if st.button("👤 Profile", key="nav_profile", use_container_width=True, type="primary" if st.session_state.current_page == "profile" else "secondary", help="Go to Profile"):
                st.session_state.current_page = "profile"
                st.rerun()

        with col_nav2:
<<<<<<< HEAD
<<<<<<< HEAD
            if st.button(
                "💬 Chat",
                width="stretch",
                type=(
                    "primary"
                    if st.session_state.current_page == "chat"
                    else "secondary"
                ),
                help="Go to Chat",
            ):
                st.session_state.current_page = "chat"
                st.rerun()
        with col_nav3:
            if st.button(
                "👤 Profile",
                width="stretch",
                type=(
                    "primary"
                    if st.session_state.current_page == "profile"
                    else "secondary"
                ),
                help="Go to Profile",
            ):
=======
            if st.button("💬 Chat", use_container_width=True, type="primary" if st.session_state.current_page == "chat" else "secondary", help="Go to Chat"):
                st.session_state.current_page = "chat"
                st.rerun()
        with col_nav3:
            if st.button("👤 Profile", use_container_width=True, type="primary" if st.session_state.current_page == "profile" else "secondary", help="Go to Profile"):
>>>>>>> origin/ui-ux-improvements-3860328367442600035
                st.session_state.current_page = "profile"
=======
            if st.button("💬 Chat", key="nav_chat", use_container_width=True, type="primary" if st.session_state.current_page == "chat" else "secondary", help="Go to Chat"):
                st.session_state.current_page = "chat"
                st.rerun()
<<<<<<< HEAD
            if st.button("📣 Feedback", key="nav_feedback", use_container_width=True, type="primary" if st.session_state.current_page == "feedback" else "secondary", help="Give Feedback"):
                st.session_state.current_page = "feedback"
>>>>>>> 89c4a85 (Feedback: [integrations])
                st.rerun()


=======
        with col_nav4:
            if st.button("🔒 Privacy", width="stretch", type="primary" if st.session_state.current_page == "privacy" else "secondary", help="Privacy & Security"):
                st.session_state.current_page = "privacy"
                st.rerun()
        
>>>>>>> origin/privacy-compliance-updates-15433171418981572602
        st.divider()

        # 2. User Info (Compact)
        user_info = st.session_state.get('user_info', {})
        username = st.session_state.get('username', 'Guest')
        auth_type = '🔐 Google' if 'google_oauth_token' in st.session_state else '🔐 Login'

        st.markdown(f"""
        <div class="sidebar-user-card" role="region" aria-label="User Information">
            <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                <span style="font-weight: 600; color: var(--text-primary);" aria-label="User: {username}">👤 {username}</span>
                <span style="font-size: 0.8rem; background: var(--bg-tertiary); padding: 2px 6px; border-radius: 4px; color: var(--text-secondary);" aria-label="Authentication Type: {auth_type}">{auth_type}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
<<<<<<< HEAD

        if st.button("🚪 Sign Out", key="sidebar_logout_btn", width="stretch"):
=======
        
        if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
>>>>>>> origin/ui-ux-improvements-3860328367442600035
            logout()


        st.divider()

        # --- CHAT HISTORY ---
        try:
            from ui.database import get_user_conversations, create_new_conversation, get_conversation_messages

            c_hist1, c_hist2 = st.columns([0.2, 0.8])
            with c_hist1:
                st.markdown("### 🕒")
            with c_hist2:
                if st.button("➕ New Chat", use_container_width=True, type="primary"):
                     st.session_state.messages = []
                     # Create immediately or wait for first message?
                     # Better to wait for first message to avoid empty entries,
                     # BUT to support "switching", we just clear the ID so a new one is made on first send.
                     if 'conversation_id' in st.session_state:
                        del st.session_state['conversation_id']
                     st.rerun()

            conversations = get_user_conversations(username)
            if conversations:
                # Show most recent first
                for c_id, c_title, c_date in conversations[:5]:
                    # Highlight active
                    type_ = (
                        "primary"
                        if st.session_state.get("conversation_id") == c_id
                        else "secondary"
                    )
                    if st.button(
                        f"{c_title}",
                        key=f"hist_{c_id}",
                        use_container_width=True,
                        type=type_,
                    ):
                        st.session_state.conversation_id = c_id
                        st.session_state.messages = get_conversation_messages(c_id)
                        st.rerun()


                if len(conversations) > 5:
                    with st.expander("Older Chats"):
                        for c_id, c_title, c_date in conversations[5:15]:
                            if st.button(
                                f"{c_title}",
                                key=f"hist_old_{c_id}",
                                use_container_width=True,
                            ):
                                st.session_state.conversation_id = c_id
                                st.session_state.messages = get_conversation_messages(
                                    c_id
                                )
                                st.rerun()


        except Exception as e:
            st.error(f"History error: {e}")

        st.divider()

        # 3. Model Selection
        st.markdown("### 🤖 Model Selection")


        # Provider Filter (Horizontal Radio for cleaner look)
        providers = [
            "All",
            "Google",
            "OpenAI",
            "Anthropic",
            "Together",
            "xAI",
            "DeepSeek",
        ]
        selected_provider_filter = st.radio(
            "Provider Filter",
            providers,
            horizontal=True,
            label_visibility="collapsed",
            help="Filter specific model providers",
        )


        # Filter Models based on selection
        # Using the new MODEL_DETAILS structure
        from ui.config import MODEL_DETAILS


        provider_map = {
            "Google": "google",
            "OpenAI": "openai",
            "Anthropic": "anthropic",
            "Together": "together",
            "xAI": "xai",
            "DeepSeek": "deepseek",
        }


        filter_key = provider_map.get(selected_provider_filter)


        if filter_key:
            filtered_models_list = [
                (v['label'], k, v['provider'])
                for k, v in MODEL_DETAILS.items()
                if v['provider'] == filter_key
            ]
        else:
            # show all
            filtered_models_list = [
               (v['label'], k, v['provider'])
               for k, v in MODEL_DETAILS.items()
            ]

        # Model Select Box
        if not filtered_models_list:
            st.warning(f"No models found for {selected_provider_filter}")
            filtered_models_list = [
                (v["label"], k, v["provider"]) for k, v in MODEL_DETAILS.items()
            ]

        # Build display labels with icons
        display_labels = [f"{PROVIDER_ICONS.get(m[2], '⚪')} {m[0]}" for m in filtered_models_list]

        # Persist selection if possible, otherwise default
        current_selection = st.session_state.get("selected_model_name")
        default_index = 0
        if current_selection:
            # try to find index
            for i, m in enumerate(filtered_models_list):
                if m[1] == current_selection:
                    default_index = i
                    break


        model_choice_idx = st.selectbox(
            "Select Model",
            range(len(filtered_models_list)),
            format_func=lambda i: display_labels[i],
            index=default_index,
            label_visibility="collapsed",
        )


        selected_model_tuple = filtered_models_list[model_choice_idx]
        st.session_state.selected_model_label = selected_model_tuple[0]
        st.session_state.selected_model_name = selected_model_tuple[1]
        st.session_state.selected_provider = selected_model_tuple[2]


        # --- Enhanced Model Info Card ---
        model_id = selected_model_tuple[1]
        model_info = MODEL_DETAILS.get(model_id, {})
        pricing = MODEL_PRICING.get(model_id, (0, 0))


        with st.container():
            # Description
            st.caption(model_info.get('description', 'No description available.'))

            # Badges (Capabilities)
            caps = model_info.get("capabilities", [])
            if caps:
                badges_html = "".join(f"<span style='background:#334155; color:#e2e8f0; padding:2px 6px; border-radius:4px; font-size:0.75rem; margin-right:4px;'>{c}</span>" for c in caps)
                st.markdown(f"<div style='margin-bottom:8px;'>{badges_html}</div>", unsafe_allow_html=True)

            # Stats Grid
            c_info1, c_info2 = st.columns(2)
            with c_info1:
                st.markdown(f"**Context:** `{model_info.get('context', 'Unknown')}`")
            with c_info2:
                 st.markdown(f"**Cost:** `${pricing[0]} / ${pricing[1]}`")

            st.caption(f"*Cost per 1M tokens (In/Out)*")

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
            st.session_state.temperature = st.slider(
                "Temperature", 0.0, 2.0, st.session_state.get("temperature", 1.0), 0.1
            )
            st.session_state.top_p = st.slider(
                "Top P", 0.0, 1.0, st.session_state.get("top_p", 0.95), 0.05
            )
            st.session_state.max_tokens = st.slider(
                "Max Tokens", 100, 8192, st.session_state.get("max_tokens", 2048), 100
            )
            st.session_state.enable_streaming = st.checkbox(
                "Enable Streaming", value=st.session_state.get("enable_streaming", True)
            )
            st.session_state.system_instruction = st.text_area(
                "System Prompt",
                value=st.session_state.get("system_instruction", ""),
                placeholder="You are a helpful assistant...",
                height=100,
            )

        st.divider()

        # 6. Brain Mode
        with st.expander("🧠 Brain Mode", expanded=False):
            enable_brain = st.checkbox(
                "Enable AI Brain",
                value=st.session_state.get("enable_brain_mode", False),
            )
            st.session_state.enable_brain_mode = enable_brain


            if enable_brain:
                st.info("🧠 Brain Active")
                st.session_state.enable_internet = st.checkbox("Internet Search", value=st.session_state.get('enable_internet', True))
                st.session_state.brain_auto_select = st.checkbox("Auto-Select Models", value=st.session_state.get('brain_auto_select', True))

                st.caption("Consulted Models:")
                c1, c2 = st.columns(2)
                with c1:
                    google = st.checkbox(
                        "Google",
                        value=True,
                        disabled=not bool(st.session_state.google_api_key),
                    )
                    openai = st.checkbox(
                        "OpenAI",
                        value=False,
                        disabled=not bool(st.session_state.openai_api_key),
                    )
                with c2:
                    anthropic = st.checkbox("Claude", value=False, disabled=not bool(st.session_state.anthropic_api_key))
                    together = st.checkbox("Llama", value=False, disabled=not bool(st.session_state.together_api_key))

                # Logic to store which models to consult (could be stored in session state)
                st.session_state.brain_consult_models = {
                    "google": google,
                    "openai": openai,
                    "anthropic": anthropic,
                    "together": together,
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
            learning_brain = st.session_state.get("learning_brain")
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
            if cost_data["by_provider"]:
                st.write(cost_data["by_provider"])

        st.divider()


        # Chat Controls
        st.markdown("### 💬 Chat Controls")
        c1, c2 = st.columns(2)
        with c1:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            if st.button("🗑️ Clear", width="stretch", help="Clear current conversation"):
                st.session_state.messages = []
                st.rerun()
        with c2:
            with st.popover("💾 Export", use_container_width=True):
                st.caption("Download Conversation")
=======
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with c2:
            # Use popover for export options
            with st.popover("💾 Export", use_container_width=True):
                msgs = st.session_state.get('messages', [])

                # TXT Export
                txt_data = "\n\n".join([f"[{m.get('timestamp', '')}] {m['role'].upper()}: {m['content']}" for m in msgs])
                st.download_button(
                    "📄 Download as .txt",
                    data=txt_data,
                    file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
=======
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with c2:
            # Use popover for export options
            with st.popover("💾 Export", use_container_width=True):
                st.markdown("### Export Chat")
                msgs = st.session_state.get('messages', [])

                # Text format
                text_content = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in msgs])
                st.download_button(
                    "📄 Download as Text",
                    text_content,
                    "chat_history.txt",
>>>>>>> origin/feature/json-chat-export-3053385537761538795
                    mime="text/plain",
                    use_container_width=True
                )

<<<<<<< HEAD
                # JSON Export
                try:
                    json_data = serialize_messages(msgs)
                    st.download_button(
                        "﹛﹜ Download as .json",
                        data=json_data,
                        file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
=======
                # JSON format
                try:
                    from ui.chat_utils import serialize_messages
                    import json
                    json_data = json.dumps(serialize_messages(msgs), indent=2)
                    st.download_button(
                        "📦 Download as JSON",
                        json_data,
                        "chat_history.json",
>>>>>>> origin/feature/json-chat-export-3053385537761538795
                        mime="application/json",
                        use_container_width=True
                    )
                except Exception as e:
<<<<<<< HEAD
                    st.error(f"JSON export failed: {e}")
>>>>>>> d35a0fe (Innovation: Add chat export functionality (TXT/JSON))
=======
                    st.error(f"JSON Export error: {e}")
>>>>>>> origin/feature/json-chat-export-3053385537761538795

                # Prepare data
                msgs = st.session_state.get('messages', [])

                # TXT
                text_data = "\n\n".join([f"[{m['role'].upper()}] ({m.get('timestamp','')}): {m.get('content','')}" for m in msgs])
                st.download_button("📄 Text (.txt)", text_data, f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", use_container_width=True)

                # JSON
                json_data = serialize_messages(msgs)
                st.download_button("📦 JSON (.json)", json.dumps(json_data, indent=2), f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", use_container_width=True)
=======
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961

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
<<<<<<< HEAD
<<<<<<< HEAD
=======

import os

import streamlit as st

from multimodal_voice_integration import MultimodalVoiceIntegrator
from ui.common import get_session_cost, logout
from ui.config import MODEL_DETAILS, MODEL_PRICING, PROVIDER_ICONS

>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961

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

<<<<<<< HEAD
<<<<<<< HEAD
        st.divider()

        # 2. User Info (Compact)
<<<<<<< HEAD
        user_info = st.session_state.get('user_info', {})
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        if st.button("📝 Feedback", width="stretch", type="primary" if st.session_state.current_page == "feedback" else "secondary", help="Provide Feedback"):
            st.session_state.current_page = "feedback"
            st.rerun()

=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
        st.divider()

        # 2. User Info (Compact)
        user_info = st.session_state.get('user_info', {})
<<<<<<< HEAD
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
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

        # --- CHAT HISTORY ---
        try:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            from ui.database import get_user_conversations, create_new_conversation, get_conversation_messages
=======
            from ui.database import get_conversation_messages, get_user_conversations
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            from ui.database import get_user_conversations, create_new_conversation, get_conversation_messages
>>>>>>> origin/feedback-integration-17764393616523020931
=======
            from ui.database import get_user_conversations, create_new_conversation, get_conversation_messages
>>>>>>> origin/ui-ux-improvements-11896252316584290961

            c_hist1, c_hist2 = st.columns([0.2, 0.8])
            with c_hist1:
                 st.markdown("### 🕒")
            with c_hist2:
                if st.button("➕ New Chat", use_container_width=True, type="primary"):
                     st.session_state.messages = []
                     # Create immediately or wait for first message?
                     # Better to wait for first message to avoid empty entries,
                     # BUT to support "switching", we just clear the ID so a new one is made on first send.
                     if 'conversation_id' in st.session_state:
                        del st.session_state['conversation_id']
                     st.rerun()

            conversations = get_user_conversations(username)
            if conversations:
                # Show most recent first
                for c_id, c_title, c_date in conversations[:5]:
                    # Highlight active
                    type_ = "primary" if st.session_state.get("conversation_id") == c_id else "secondary"
                    if st.button(f"{c_title}", key=f"hist_{c_id}", use_container_width=True, type=type_):
                        st.session_state.conversation_id = c_id
                        st.session_state.messages = get_conversation_messages(c_id)
                        st.rerun()

                if len(conversations) > 5:
                    with st.expander("Older Chats"):
                         for c_id, c_title, c_date in conversations[5:15]:
                            if st.button(f"{c_title}", key=f"hist_old_{c_id}", use_container_width=True):
                                st.session_state.conversation_id = c_id
                                st.session_state.messages = get_conversation_messages(c_id)
                                st.rerun()

        except Exception as e:
            st.error(f"History error: {e}")

        st.divider()

        # 3. Model Selection
        st.markdown("### 🤖 Model Selection")

<<<<<<< HEAD
        # Provider Filter (Horizontal Radio for cleaner look)
<<<<<<< HEAD
<<<<<<< HEAD
        providers = ["All", "Google", "OpenAI", "Anthropic", "Together", "xAI", "DeepSeek", "Groq"]
=======
        providers = ["All", "Google", "OpenAI", "Anthropic", "Together", "xAI", "DeepSeek"]
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        providers = ["All", "Google", "OpenAI", "Anthropic", "Together", "xAI", "DeepSeek"]
>>>>>>> origin/feedback-integration-17764393616523020931
        selected_provider_filter = st.radio(
            "Provider Filter",
            providers,
            horizontal=True,
            label_visibility="collapsed",
            help="Filter specific model providers"
        )

        # Filter Models based on selection
        # Using the new MODEL_DETAILS structure
<<<<<<< HEAD
<<<<<<< HEAD
        from ui.config import MODEL_DETAILS
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
        from ui.config import MODEL_DETAILS
>>>>>>> origin/feedback-integration-17764393616523020931

        provider_map = {
            "Google": "google",
            "OpenAI": "openai",
            "Anthropic": "anthropic",
            "Together": "together",
            "xAI": "xai",
<<<<<<< HEAD
<<<<<<< HEAD
            "DeepSeek": "deepseek",
            "Groq": "groq"
=======
            "DeepSeek": "deepseek"
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
            "DeepSeek": "deepseek"
>>>>>>> origin/feedback-integration-17764393616523020931
        }

        filter_key = provider_map.get(selected_provider_filter)

        if filter_key:
            filtered_models_list = [
                (v['label'], k, v['provider'])
                for k, v in MODEL_DETAILS.items()
                if v['provider'] == filter_key
            ]
        else:
            # show all
            filtered_models_list = [
               (v['label'], k, v['provider'])
               for k, v in MODEL_DETAILS.items()
            ]

        # Model Select Box
        if not filtered_models_list:
            st.warning(f"No models found for {selected_provider_filter}")
            filtered_models_list = [(v['label'], k, v['provider']) for k, v in MODEL_DETAILS.items()]

        # Build display labels with icons
        display_labels = [f"{PROVIDER_ICONS.get(m[2], '⚪')} {m[0]}" for m in filtered_models_list]

        # Persist selection if possible, otherwise default
        current_selection = st.session_state.get('selected_model_name')
        default_index = 0
        if current_selection:
            # try to find index
            for i, m in enumerate(filtered_models_list):
                if m[1] == current_selection:
                    default_index = i
                    break

        model_choice_idx = st.selectbox(
            "Select Model",
            range(len(filtered_models_list)),
            format_func=lambda i: display_labels[i],
            index=default_index,
            label_visibility="collapsed"
        )

        selected_model_tuple = filtered_models_list[model_choice_idx]
        st.session_state.selected_model_label = selected_model_tuple[0]
        st.session_state.selected_model_name = selected_model_tuple[1]
        st.session_state.selected_provider = selected_model_tuple[2]

        # --- Enhanced Model Info Card ---
        model_id = selected_model_tuple[1]
        model_info = MODEL_DETAILS.get(model_id, {})
        pricing = MODEL_PRICING.get(model_id, (0, 0))

        with st.container():
=======
        with st.container(border=True):
            # Provider Filter (Horizontal Radio for cleaner look)
            providers = ["All", "Google", "OpenAI", "Anthropic", "Together", "xAI", "DeepSeek"]
            selected_provider_filter = st.radio(
                "Provider Filter",
                providers,
                horizontal=True,
                label_visibility="collapsed",
                help="Filter specific model providers"
            )

            # Filter Models based on selection
            # Using the new MODEL_DETAILS structure
            from ui.config import MODEL_DETAILS

            provider_map = {
                "Google": "google",
                "OpenAI": "openai",
                "Anthropic": "anthropic",
                "Together": "together",
                "xAI": "xai",
                "DeepSeek": "deepseek"
            }

            filter_key = provider_map.get(selected_provider_filter)

            if filter_key:
                filtered_models_list = [
                    (v['label'], k, v['provider'])
                    for k, v in MODEL_DETAILS.items()
                    if v['provider'] == filter_key
                ]
            else:
                # show all
                filtered_models_list = [
                (v['label'], k, v['provider'])
                for k, v in MODEL_DETAILS.items()
                ]

            # Model Select Box
            if not filtered_models_list:
                st.warning(f"No models found for {selected_provider_filter}")
                filtered_models_list = [(v['label'], k, v['provider']) for k, v in MODEL_DETAILS.items()]

            # Build display labels with icons
            display_labels = [f"{PROVIDER_ICONS.get(m[2], '⚪')} {m[0]}" for m in filtered_models_list]

            # Persist selection if possible, otherwise default
            current_selection = st.session_state.get('selected_model_name')
            default_index = 0
            if current_selection:
                # try to find index
                for i, m in enumerate(filtered_models_list):
                    if m[1] == current_selection:
                        default_index = i
                        break

            model_choice_idx = st.selectbox(
                "Select Model",
                range(len(filtered_models_list)),
                format_func=lambda i: display_labels[i],
                index=default_index,
                label_visibility="collapsed"
            )

            selected_model_tuple = filtered_models_list[model_choice_idx]
            st.session_state.selected_model_label = selected_model_tuple[0]
            st.session_state.selected_model_name = selected_model_tuple[1]
            st.session_state.selected_provider = selected_model_tuple[2]

            # --- Enhanced Model Info Card ---
            model_id = selected_model_tuple[1]
            model_info = MODEL_DETAILS.get(model_id, {})
            pricing = MODEL_PRICING.get(model_id, (0, 0))

            # Nested container inside border container is fine, but maybe redundant.
            # Removing inner container call, just using markdown inside the border container.

>>>>>>> origin/ui-ux-improvements-11896252316584290961
            # Description
            st.caption(model_info.get('description', 'No description available.'))

            # Badges (Capabilities)
            caps = model_info.get('capabilities', [])
            if caps:
                badges_html = "".join(f"<span style='background:#334155; color:#e2e8f0; padding:2px 6px; border-radius:4px; font-size:0.75rem; margin-right:4px;'>{c}</span>" for c in caps)
                st.markdown(f"<div style='margin-bottom:8px;'>{badges_html}</div>", unsafe_allow_html=True)

            # Stats Grid
            c_info1, c_info2 = st.columns(2)
            with c_info1:
                st.markdown(f"**Context:** `{model_info.get('context', 'Unknown')}`")
            with c_info2:
<<<<<<< HEAD
                 st.markdown(f"**Cost:** `${pricing[0]} / ${pricing[1]}`")
=======
                    st.markdown(f"**Cost:** `${pricing[0]} / ${pricing[1]}`")
>>>>>>> origin/ui-ux-improvements-11896252316584290961

            st.caption(f"*Cost per 1M tokens (In/Out)*")

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
            st.session_state.api_keys_initialized = True

        configured_keys = sum([
            bool(st.session_state.google_api_key),
            bool(st.session_state.openai_api_key),
            bool(st.session_state.anthropic_api_key),
            bool(st.session_state.together_api_key),
            bool(st.session_state.xai_api_key),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            bool(st.session_state.deepseek_api_key),
            bool(st.session_state.groq_api_key)
        ])

        with st.expander(f"🔑 API Keys ({configured_keys}/7)", expanded=False):
=======
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
            bool(st.session_state.deepseek_api_key)
        ])

        with st.expander(f"🔑 API Keys ({configured_keys}/6)", expanded=False):
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
            show_keys = st.checkbox("Show Keys", value=False)
            key_type = "default" if show_keys else "password"

            st.session_state.google_api_key = st.text_input("Google API Key", value=st.session_state.google_api_key, type=key_type)
            st.session_state.openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type=key_type)
            st.session_state.anthropic_api_key = st.text_input("Anthropic API Key", value=st.session_state.anthropic_api_key, type=key_type)
            st.session_state.together_api_key = st.text_input("Together AI Key", value=st.session_state.together_api_key, type=key_type)
            st.session_state.xai_api_key = st.text_input("xAI API Key", value=st.session_state.xai_api_key, type=key_type)
            st.session_state.deepseek_api_key = st.text_input("DeepSeek API Key", value=st.session_state.deepseek_api_key, type=key_type)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            st.session_state.groq_api_key = st.text_input("Groq API Key", value=st.session_state.groq_api_key, type=key_type)
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                    groq = st.checkbox("Groq", value=False, disabled=not bool(st.session_state.groq_api_key))
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961
                with c2:
                    anthropic = st.checkbox("Claude", value=False, disabled=not bool(st.session_state.anthropic_api_key))
                    together = st.checkbox("Llama", value=False, disabled=not bool(st.session_state.together_api_key))

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
                groq = st.checkbox("Groq", value=False, disabled=not bool(st.session_state.groq_api_key))

>>>>>>> api-integrations-groq-3434217061461873316
                # Logic to store which models to consult (could be stored in session state)
                st.session_state.brain_consult_models = {
                    "google": google, "openai": openai, "anthropic": anthropic, "together": together, "groq": groq
=======
                # Logic to store which models to consult (could be stored in session state)
                st.session_state.brain_consult_models = {
                    "google": google, "openai": openai, "anthropic": anthropic, "together": together
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
                # Logic to store which models to consult (could be stored in session state)
                st.session_state.brain_consult_models = {
                    "google": google, "openai": openai, "anthropic": anthropic, "together": together
>>>>>>> origin/feedback-integration-17764393616523020931
=======
                # Logic to store which models to consult (could be stored in session state)
                st.session_state.brain_consult_models = {
                    "google": google, "openai": openai, "anthropic": anthropic, "together": together
>>>>>>> origin/ui-ux-improvements-11896252316584290961
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> api-groq-integration-6554511320622598819
=======
>>>>>>> api-integrations-groq-3434217061461873316
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        with c2:
            if st.button("💾 Save", use_container_width=True):
                # Simple export
                msgs = st.session_state.get('messages', [])
                text = "\n".join([f"{m['role']}: {m['content']}" for m in msgs])
                st.download_button("TxT", text, "chat.txt")
>>>>>>> origin/ui-ux-improvements-3860328367442600035
=======
>>>>>>> origin/ui-ux-improvements-11896252316584290961

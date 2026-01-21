
import streamlit as st
import os
import time
from datetime import datetime

# Import UI Modules
import ui.styles
from ui.auth import show_login_page
from ui.profile import show_profile_page
from ui.dashboard import show_dashboard
from ui.sidebar import render_sidebar
from ui.chat import show_chat_page

# Import Brain
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(page_title="Antigravity AI", page_icon="🤖", layout="wide")

# Initialize theme state early
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Apply theme CSS
st.markdown(ui.styles.load_css(), unsafe_allow_html=True)

# Force native DNS to avoid SRV lookups that can time out in some networks
os.environ.setdefault("GRPC_DNS_RESOLVER", "native")

# --- INITIALIZATION ---

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

# Initialize session tracking
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = time.time()
if "total_sessions" not in st.session_state:
    st.session_state.total_sessions = 1
if "user_joined_date" not in st.session_state:
    st.session_state.user_joined_date = datetime.now().strftime('%Y-%m-%d')

# Initialize Brain components
if "learning_brain" not in st.session_state:
    st.session_state.learning_brain = LearningBrain()
if "multimodal_voice_integrator" not in st.session_state:
    st.session_state.multimodal_voice_integrator = MultimodalVoiceIntegrator()

# Initialize Chat State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False

# --- ROUTING ---

# Show login page if not authenticated
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# Render Sidebar (Always visible for authenticated users)
render_sidebar()

# Page Routing
if st.session_state.current_page == "dashboard":
    show_dashboard()
elif st.session_state.current_page == "profile":
    # Ensure profile page can navigate back
    show_profile_page()
elif st.session_state.current_page == "chat":
    show_chat_page()
else:
    # Default to chat if unknown page
    st.session_state.current_page = "chat"
    show_chat_page()
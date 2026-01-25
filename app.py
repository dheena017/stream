"""
Antigravity AI - Multi-Provider Intelligent Chat Application
A sophisticated Streamlit-based AI chat interface with learning capabilities,
voice integration, and multi-modal support.
"""

import logging
import os
import time
from datetime import datetime

import streamlit as st

# Import UI Modules
import ui.styles
from ui.auth import show_login_page
from ui.chat import show_chat_page
from ui.dashboard import show_dashboard
from ui.database import init_db
from ui.profile import show_profile_page
from ui.sidebar import render_sidebar

# Initialize DB on startup
init_db()

# Import Brain
from brain_learning import LearningBrain
from multimodal_voice_integration import MultimodalVoiceIntegrator

# --- LOGGER SETUP ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def initialize_page_config():
    """Configure Streamlit page settings and metadata."""
    st.set_page_config(
        page_title="Antigravity AI",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "Antigravity AI - Multi-Provider Intelligence Platform v1.0"
        },
    )
    logger.info("Page configuration initialized")


def initialize_theme():
    """Initialize and apply theme settings."""
    # Load persisted preference (global or per-user) before setting defaults
    try:
        from ui.prefs import get_pref

        username = st.session_state.get("username")
        pref_dark = get_pref("dark_mode", username, None)
        if pref_dark is not None and "dark_mode" not in st.session_state:
            st.session_state["dark_mode"] = bool(pref_dark)
        if "dark_mode" not in st.session_state:
            st.session_state["dark_mode"] = False
    except Exception:
        if "dark_mode" not in st.session_state:
            st.session_state["dark_mode"] = False

    # Apply theme CSS (uses st.session_state['dark_mode'])
    st.markdown(ui.styles.load_css(), unsafe_allow_html=True)
    logger.debug("Theme applied")


def configure_environment():
    """Configure environment variables for optimal performance."""
    os.environ.setdefault("GRPC_DNS_RESOLVER", "native")
    logger.debug("Environment configured")


def initialize_auth_state():
    """Initialize authentication and user session state."""
    defaults = {"authenticated": False, "username": None, "current_page": "dashboard"}

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    logger.info(f"Auth state initialized - User: {st.session_state.username}")


def initialize_session_tracking():
    """Initialize session and user tracking metrics."""
    tracking_defaults = {
        "session_start_time": time.time(),
        "total_sessions": 1,
        "user_joined_date": datetime.now().strftime("%Y-%m-%d"),
    }

    for key, value in tracking_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    logger.debug("Session tracking initialized")


@st.cache_resource
def initialize_brain_components():
    """Initialize AI brain components (cached to prevent reinitalization)."""
    learning_brain = LearningBrain()
    multimodal_voice_integrator = MultimodalVoiceIntegrator()
    logger.info("Brain components initialized and cached")
    return learning_brain, multimodal_voice_integrator


def initialize_brain_state():
    """Initialize brain and multimodal components in session state."""
    if "learning_brain" not in st.session_state:
        learning_brain, multimodal_voice = initialize_brain_components()
        st.session_state.learning_brain = learning_brain
        st.session_state.multimodal_voice_integrator = multimodal_voice

    logger.debug("Brain state initialized")


def initialize_chat_state():
    """Initialize chat-related session state."""
    chat_defaults = {
        "messages": [],
        "voice_mode": False,
        "enable_internet_search": False,
        "search_result_count": 5,
        "enable_advanced_captioning": False,
    }

    for key, value in chat_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    logger.debug("Chat state initialized")


def initialize_all_states():
    """Master initialization function for all application states."""
    initialize_auth_state()
    initialize_session_tracking()
    initialize_brain_state()
    initialize_chat_state()
    logger.info("All application states initialized")


def handle_authentication():
    """Handle user authentication flow."""
    if not st.session_state.authenticated:
        show_login_page()
        st.stop()


def handle_page_routing():
    """Route to appropriate page based on current_page state."""
    page_router = {
        "dashboard": show_dashboard,
        "profile": show_profile_page,
        "chat": show_chat_page,
    }

    current_page = st.session_state.current_page
    page_handler = page_router.get(current_page, show_chat_page)

    logger.info(f"Routing to page: {current_page}")
    page_handler()


def main():
    """Main application entry point."""
    # Setup
    initialize_page_config()
    initialize_theme()
    configure_environment()

    # Initialize all states
    initialize_all_states()

    # Authentication check
    handle_authentication()

    # Render sidebar for authenticated users
    render_sidebar()

    # Route to appropriate page
    handle_page_routing()

    logger.info("Application render completed")


if __name__ == "__main__":
    main()

import streamlit as st
import time
import ui.dashboard
import ui.chat
import ui.auth
import ui.sidebar
import ui.profile
from ui.analytics import init_analytics

def initialize_auth_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

def initialize_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "voice_mode" not in st.session_state:
        st.session_state.voice_mode = False
    if "enable_internet_search" not in st.session_state:
        st.session_state.enable_internet_search = False
    if "search_result_count" not in st.session_state:
        st.session_state.search_result_count = 5

def initialize_session_tracking():
    if "session_start_time" not in st.session_state:
        st.session_state.session_start_time = time.time()
    if "total_sessions" not in st.session_state:
        st.session_state.total_sessions = 1
    if "user_joined_date" not in st.session_state:
        st.session_state.user_joined_date = time.time()

def show_login_page():
    ui.auth.show_login_form()

def show_dashboard():
    ui.dashboard.render_dashboard()

def show_chat_page():
    ui.chat.render_chat()

def show_profile_page():
    ui.profile.render_profile()

def handle_authentication():
    if not st.session_state.authenticated:
        show_login_page()
        st.stop()

def handle_page_routing():
    if st.session_state.current_page == "dashboard":
        show_dashboard()
    elif st.session_state.current_page == "profile":
        show_profile_page()
    else:
        show_chat_page()

def main():
    st.set_page_config(page_title="Streamlit AI Chat", layout="wide")

    init_analytics()

    initialize_auth_state()
    initialize_chat_state()
    initialize_session_tracking()

    ui.sidebar.render_sidebar()

    handle_authentication()
    handle_page_routing()

if __name__ == "__main__":
    main()

import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("Navigation")
        if st.button("Chat"):
            st.session_state.current_page = "chat"
            st.rerun()
        if st.button("Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        if st.button("Profile"):
            st.session_state.current_page = "profile"
            st.rerun()

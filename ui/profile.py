import streamlit as st

def render_profile():
    st.title("User Profile")
    st.write("This is the profile page.")
    st.write(f"Username: {st.session_state.get('username', 'Unknown')}")

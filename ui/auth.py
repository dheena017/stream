def show_login_form():
    import streamlit as st
    st.header("Login")
    if st.button("Login as Guest"):
        st.session_state.authenticated = True
        st.session_state.username = "guest"
        st.rerun()

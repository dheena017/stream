import streamlit as st
from ui import styles
import time
from brain import get_brain

def render():
    styles.load_css()

    st.header("Chat Interface")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            # Use cached brain
            brain = get_brain()
            response = brain.process(prompt)
            st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

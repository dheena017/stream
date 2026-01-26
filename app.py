import streamlit as st
from ui import chat, sidebar

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

sidebar.render()
chat.render()

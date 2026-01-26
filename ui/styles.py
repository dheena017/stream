import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* Mobile Optimizations */
        @media (max-width: 768px) {
            /* Increase touch targets */
            .stButton > button {
                min-height: 48px;
                width: 100%;
                margin-top: 10px;
            }

            /* Chat input full width and accessible */
            .stChatInputContainer {
                padding-bottom: 20px;
            }

            /* Adjust padding for main container */
            .block-container {
                padding-top: 2rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            /* Typography adjustments */
            h1 {
                font-size: 1.8rem !important;
            }

            .stMarkdown p {
                font-size: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from ui.database import get_feedback_stats

def render_dashboard():
    st.header("Dashboard")
    st.write("Overview of application metrics.")

    st.subheader("Feedback Analysis")
    df = get_feedback_stats()

    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Feedback", len(df))
        with col2:
            st.metric("Average Rating", f"{df['rating'].mean():.2f}")

        st.write("Recent Feedback:")
        st.dataframe(df[['created_at', 'rating', 'comment', 'user_id']])
    else:
        st.info("No feedback collected yet.")

import streamlit as st
from ui.database import save_feedback

def show_feedback_page():
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 3rem;">📝</div>
        <div>
            <h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">
                Feedback
            </h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0.25rem 0 0 0; font-size: 1rem;">
                Help us improve Antigravity AI
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.write("We value your input! Please let us know what you think.")

        with st.form("feedback_form"):
            category = st.selectbox(
                "Category",
                ["Bug Report", "Feature Request", "General Feedback", "Other"]
            )

            rating = st.slider("Rating", 1, 5, 5, help="1 = Poor, 5 = Excellent")

            comment = st.text_area("Comments", height=150, placeholder="Tell us more...")

            submitted = st.form_submit_button("Submit Feedback", type="primary")

            if submitted:
                if not comment:
                    st.warning("Please enter a comment.")
                else:
                    # Enforce anonymity
                    username = "Anonymous"
                    if save_feedback(username, category, rating, comment):
                        st.success("Thank you for your feedback! We appreciate it.")
                    else:
                        st.error("Failed to save feedback. Please try again later.")

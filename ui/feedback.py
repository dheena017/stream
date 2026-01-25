import streamlit as st
from ui.database import save_feedback, get_recent_feedback

def show_feedback_page():
    """Display the feedback page."""

    # Header
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 3rem;">📣</div>
        <div>
            <h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">
                Feedback Center
            </h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0.25rem 0 0 0; font-size: 1rem;">
                Help us improve your experience
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📝 Submit Feedback")
        st.markdown("We value your input! Please let us know if you found a bug, have a feature request, or just want to share your thoughts.")

        with st.form("feedback_form"):
            category = st.selectbox("Category", ["General", "Bug Report", "Feature Request", "Model Performance", "UI/UX"])

            st.write("How would you rate your experience?")
            rating = st.slider("Rating", 1, 5, 5, format="%d ⭐")

            comment = st.text_area("Details", placeholder="Tell us more about your experience...")

            submitted = st.form_submit_button("Submit Feedback", type="primary", use_container_width=True)

            if submitted:
                if not comment:
                    st.error("Please provide some details.")
                else:
                    user_id = st.session_state.get('username', 'Anonymous')
                    try:
                        save_feedback(user_id, rating, category, comment)
                        st.success("✅ Thank you! Your feedback has been recorded.")
                    except Exception as e:
                        st.error(f"Error saving feedback: {e}")

    with col2:
        st.markdown("### 🕒 Recent Feedback")
        try:
            recent = get_recent_feedback(5)
            if recent:
                for item in recent:
                    with st.container(border=True):
                        st.caption(f"{item['created_at'][:16]} • {item['user_id']}")
                        st.markdown(f"**{item['category']}** ({item['rating']} ⭐)")
                        st.markdown(item['comment'])
            else:
                st.info("No feedback yet. Be the first!")
        except Exception as e:
            st.error(f"Could not load recent feedback: {e}")

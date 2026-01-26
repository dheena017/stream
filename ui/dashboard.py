import streamlit as st
from ui.engagement import EngagementManager

def render_dashboard():
    st.title("User Engagement Dashboard")

    # Simple User ID retrieval (fallback to 'test_user')
    user_id = st.session_state.get("username", "test_user")
    if not user_id:
        user_id = "test_user"

    manager = EngagementManager()
    from ui.engagement import get_user_stats
    stats = get_user_stats(user_id)

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Level", stats["level"])
    with col2:
        st.metric("XP", stats["xp"])
    with col3:
        st.metric("Messages", stats["total_messages"])

    # Progress Bar
    progress = manager.get_next_level_progress(stats["xp"])
    st.write(f"Progress to Level {stats['level'] + 1}")
    st.progress(progress)

    # Achievements
    st.subheader("Achievements")

    # We need to know ALL achievements to show locked ones too.
    from ui.engagement import ACHIEVEMENTS

    unlocked_ids = {a["id"] for a in stats["achievements"]}

    for achievement in ACHIEVEMENTS:
        is_unlocked = achievement["id"] in unlocked_ids
        if is_unlocked:
            st.success(f"🏆 **{achievement['title']}**: {achievement['description']} (+{achievement['xp_reward']} XP)")
        else:
            st.info(f"🔒 **{achievement['title']}**: {achievement['description']} ({achievement['xp_reward']} XP)")

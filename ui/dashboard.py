<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import json
import platform
import sys
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from ui.common import logout


def show_dashboard():
    """Display user dashboard with stats and activity"""

    # Modern gradient header for dashboard
    # Modern gradient header for dashboard
    st.markdown(
        """
    <div class="main-header">
        <div style="font-size: 3rem;">📊</div>
        <div>
            <h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">
                Dashboard
            </h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0.25rem 0 0 0; font-size: 1rem;">
                Your AI activity at a glance
            </p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # User info
    user_info = st.session_state.get("user_info", {})
    user_name = user_info.get("name", st.session_state.username)
    user_email = user_info.get("email", "")

    # Welcome card
    # Welcome card
    st.markdown(
        f"""
    <div class="glass-panel" style="margin-bottom: 2rem;">
        <h3 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">Welcome back, {user_name}! 👋</h3>
        {"<p style='color: var(--text-secondary); margin: 0;'>📧 " + user_email + "</p>" if user_email else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Activity metrics with modern cards
    col1, col2, col3, col4 = st.columns(4)

    total_messages = len(st.session_state.get("messages", []))
    learning_brain = st.session_state.get("learning_brain")
    stats = learning_brain.get_learning_stats() if learning_brain else {}

    with col1:
        st.markdown(
            f"""
        <div class="dashboard-card">
            <div class="metric-value">{total_messages}</div>
            <div class="metric-label">💬 Messages</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        topics = stats.get("total_topics", 0)
        st.markdown(
            f"""
        <div class="dashboard-card">
            <div class="metric-value">{topics}</div>
            <div class="metric-label">🧠 Topics</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col3:
        models = stats.get("models_tracked", 0)
        st.markdown(
            f"""
        <div class="dashboard-card">
            <div class="metric-value">{models}</div>
            <div class="metric-label">🤖 Models</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col4:
        convos = stats.get("total_conversations", 0)
        st.markdown(
            f"""
        <div class="dashboard-card">
            <div class="metric-value">{convos}</div>
            <div class="metric-label">📚 Convos</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Enhanced Quick actions with descriptions
    st.markdown(
        """
    <h3 style="display: flex; align-items: center; gap: 0.5rem;">
        <span>🚀</span> Quick Actions
    </h3>
    """,
        unsafe_allow_html=True,
    )

    # Create action cards with descriptions
    action_col1, action_col2 = st.columns(2)

    with action_col1:
        st.markdown(
            f"""
        <div class="action-card">
            <div class="action-title">💬 Start Chatting</div>
            <div class="action-desc">Begin a new conversation with your selected AI model or enable AI Brain for multi-model responses</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "▶️ Open Chat", width="stretch", type="primary", key="quick_chat_btn"
        ):
            st.session_state.current_page = "chat"
            st.rerun()

    with action_col2:
        st.markdown(
            """
        <div class="action-card">
            <div class="action-title">👤 View Profile</div>
            <div class="action-desc">Manage your account settings, preferences, and view your usage statistics</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("▶️ Go to Profile", width="stretch", key="quick_profile_btn"):
            st.session_state.current_page = "profile"
            st.rerun()

    action_col3, action_col4 = st.columns(2)

    with action_col3:
        st.markdown(
            """
        <div class="action-card">
            <div class="action-title">🧠 View Brain Stats</div>
            <div class="action-desc">See what your AI brain has learned: topics, model performance, and insights</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("▶️ Show Stats", width="stretch", key="quick_brain_btn"):
            st.session_state.show_brain_stats = not st.session_state.get(
                "show_brain_stats", False
            )
            st.rerun()

    with action_col4:
        st.markdown(
            """
        <div class="action-card">
            <div class="action-title">📥 Export Chat</div>
            <div class="action-desc">Download your chat history as JSON for backup, analysis, or sharing</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button("▶️ Download", width="stretch", key="quick_export_btn"):
            if st.session_state.messages:
                chat_export = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    "📥 Download Chat History",
                    chat_export,
                    file_name="chat_history.json",
                    mime="application/json",
                    width="stretch",
                    key="download_chat_btn",
                )
            else:
                st.warning("No chat history to export. Start a conversation first!")

    # Additional quick action shortcuts (enhanced)
    st.markdown("---")
    st.markdown("### ⚡ Additional Actions")

    # Custom CSS for action cards
    st.markdown(
        """
    <style>
    .action-card {
        background: linear-gradient(135deg, var(--accent-primary)10 0%, var(--accent-secondary)10 100%);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.06);
        transition: transform 0.2s;
        color: var(--text-primary);
    }
    .action-card:hover { transform: translateY(-2px); }
    .action-icon { font-size: 1.5rem; }
    .action-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Row 1: Primary actions
    st.markdown("#### Primary")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

    with quick_col1:
        if st.button("🔄 Clear Chat", width="stretch", key="clear_chat_quick"):
            st.session_state.messages = []
            st.success("✅ Chat cleared!")
            st.rerun()
        st.caption("Reset conversation")

    with quick_col2:
        if st.button("🧠 Reset Brain", width="stretch", key="reset_brain_quick"):
            learning_brain = st.session_state.learning_brain
            learning_brain.reset_learning()
            st.success("✅ Brain reset!")
            st.rerun()
        st.caption("Clear learning data")

    with quick_col3:
        if st.button("💾 Save Brain", width="stretch", key="save_brain_quick"):
            learning_brain = st.session_state.learning_brain
            path = st.session_state.get("brain_state_path", "learning_brain_state.json")
            if learning_brain.save_to_file(path):
                st.success("✅ Brain saved!")
            else:
                st.error("❌ Save failed")
        st.caption("Persist to disk")

    with quick_col4:
        if st.button("📂 Load Brain", width="stretch", key="load_brain_quick"):
            learning_brain = st.session_state.learning_brain
            path = st.session_state.get("brain_state_path", "learning_brain_state.json")
            if learning_brain.load_from_file(path):
                st.success("✅ Brain loaded!")
                st.rerun()
            else:
                st.warning("⚠️ File not found")
        st.caption("Restore from disk")

    # Row 2: Secondary actions
    st.markdown("#### Secondary")
    sec_col1, sec_col2, sec_col3, sec_col4 = st.columns(4)

    with sec_col1:
        if st.button("📣 Feedback", width="stretch", key="give_feedback_quick"):
            st.session_state.current_page = "feedback"
            st.rerun()
        st.caption("Share thoughts")

    with sec_col2:
        if st.button("📥 Export Chat", width="stretch", key="export_chat_quick"):
            messages = st.session_state.get("messages", [])
            if messages:
                chat_blob = "\n\n".join(
                    [f"{m['role'].upper()}: {m['content']}" for m in messages]
                )
                st.download_button(
                    "Download",
                    chat_blob,
                    "chat_export.txt",
                    "text/plain",
                    key="dl_chat_quick",
                )
            else:
                st.info("No messages to export")
        st.caption("Save conversation")

    with sec_col3:
        if st.button("📄 Download Report", width="stretch", key="dl_report_quick"):
            learning_brain = st.session_state.learning_brain
            report = learning_brain.format_learning_report()
            st.download_button(
                "Download",
                report,
                "learning_report.md",
                "text/markdown",
                key="dl_rpt_quick2",
            )
        st.caption("Brain insights")

    with sec_col4:
        if st.button("🔗 Copy Session ID", width="stretch", key="copy_session_quick"):
            session_id = st.session_state.get("session_id", "N/A")
            st.code(session_id)
        st.caption("For debugging")

    # Row 3: Toggles & info
    st.markdown("#### Toggles")
    tog_col1, tog_col2, tog_col3, tog_col4 = st.columns(4)

    with tog_col1:
        show_brain_stats = st.checkbox(
            "📈 Show Brain Stats",
            value=st.session_state.get("show_brain_stats", False),
            key="toggle_brain_stats",
        )
        st.session_state.show_brain_stats = show_brain_stats

    with tog_col2:
        dark_mode = st.checkbox(
            "🌙 Dark Hints",
            value=st.session_state.get("dark_hints", False),
            key="toggle_dark_hints",
        )
        st.session_state.dark_hints = dark_mode

    with tog_col3:
        auto_save = st.checkbox(
            "💾 Auto-save Brain",
            value=st.session_state.get("auto_save_brain", False),
            key="toggle_auto_save",
        )
        st.session_state.auto_save_brain = auto_save

    with tog_col4:
        compact_ui = st.checkbox(
            "📐 Compact UI",
            value=st.session_state.get("compact_ui", False),
            key="toggle_compact_ui",
        )
        st.session_state.compact_ui = compact_ui

    # Brain stats display
    if st.session_state.get("show_brain_stats", False):
        st.divider()
        st.markdown("### 🧠 AI Brain Learning Stats")

        if stats.get("model_strengths"):
            st.markdown("#### Model Performance")
            for model_stat in stats["model_strengths"][:5]:
                col_model, col_rate, col_total = st.columns([2, 1, 1])
                with col_model:
                    st.markdown(f"**{model_stat['model']}**")
                with col_rate:
                    st.metric("Success Rate", f"{model_stat['success_rate']}%")
                with col_total:
                    st.metric(
                        "Queries", f"{model_stat['success']}/{model_stat['total']}"
                    )

        if stats.get("top_topics"):
            st.markdown("#### Top Knowledge Topics")
            cols = st.columns(min(len(stats["top_topics"]), 5))
            for i, topic_info in enumerate(stats["top_topics"][:5]):
                with cols[i]:
<<<<<<< HEAD
                    st.metric(topic_info["topic"], topic_info["count"])

=======
                    st.metric(topic_info['topic'], topic_info['count'])
    
    # System Monitoring
    st.divider()
    with st.expander("📉 System Monitoring", expanded=False):
        st.markdown("### 🔍 Real-time Metrics")
        from ui.monitoring import get_metrics_df
        df_metrics = get_metrics_df()

        if not df_metrics.empty:
            # Parse timestamps
            df_metrics['timestamp'] = pd.to_datetime(df_metrics['timestamp'])

            # Response Times
            resp_df = df_metrics[df_metrics['type'] == 'response_time'].copy()
            if not resp_df.empty:
                resp_df['duration'] = resp_df['data'].apply(lambda x: x.get('duration', 0))
                resp_df['model'] = resp_df['data'].apply(lambda x: x.get('model', 'unknown'))

                avg_time = resp_df['duration'].mean()
                st.metric("Average Response Time", f"{avg_time:.2f}s")

                st.line_chart(resp_df.set_index('timestamp')['duration'])

            # Usage
            usage_df = df_metrics[df_metrics['type'] == 'usage'].copy()
            if not usage_df.empty:
                usage_df['model'] = usage_df['data'].apply(lambda x: x.get('model', 'unknown'))
                st.markdown("#### Model Usage")
                st.bar_chart(usage_df['model'].value_counts())

            # Errors
            err_df = df_metrics[df_metrics['type'] == 'error'].copy()
            if not err_df.empty:
                st.error(f"Total Errors: {len(err_df)}")
                st.dataframe(err_df[['timestamp', 'data']])
        else:
            st.info("No monitoring data available yet.")

>>>>>>> origin/monitoring-setup-3187580208021102587
    # Recent activity
    st.divider()
    st.markdown("### 📝 Recent Activity")

    recent_messages = st.session_state.get("messages", [])[-5:]
    if recent_messages:
        for msg in recent_messages:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            with st.expander(
                f"{role_icon} {msg['role'].title()} - {msg['content'][:50]}..."
            ):
                st.markdown(msg["content"])
    else:
        st.info("No recent activity. Start a conversation to see your history here!")

    st.divider()

    # Enhanced system info
    with st.expander("ℹ️ System Information", expanded=False):
        st.markdown("### 📊 Session Information")

        # Session details
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Session Start", datetime.now().strftime("%H:%M:%S"))
            st.metric("Session Date", datetime.now().strftime("%Y-%m-%d"))
        with col_info2:
            uptime_seconds = time.time() - st.session_state.get(
                "session_start_time", time.time()
            )
            st.metric("Session Duration", f"{int(uptime_seconds // 60)} min")
            st.metric("Current Time", datetime.now().strftime("%I:%M %p"))

        st.markdown("---")
        st.markdown("### 👤 User Information")

        user_info = st.session_state.get("user_info", {})
        col_user1, col_user2 = st.columns(2)

        with col_user1:
            st.text_input("Username", value=st.session_state.username, disabled=True)
            st.text_input(
                "Display Name",
                value=user_info.get("name", st.session_state.username),
                disabled=True,
            )
        with col_user2:
            auth_method = (
                "🔐 Google OAuth"
                if "google_oauth_token" in st.session_state
                else "🔐 Traditional Login"
            )
            st.text_input("Authentication", value=auth_method, disabled=True)
            st.text_input(
                "Email", value=user_info.get("email", "Not set"), disabled=True
            )

        st.markdown("---")
        st.markdown("### 💻 System Details")

        col_sys1, col_sys2, col_sys3 = st.columns(3)

        with col_sys1:
            st.metric("Platform", platform.system())
            st.metric("Python", platform.python_version())

        with col_sys2:
            st.metric("Streamlit", st.__version__)
            st.metric("Browser", "Chrome/Safari/Firefox")

        with col_sys3:
            total_messages = len(st.session_state.get("messages", []))
            st.metric("Messages", total_messages)
            st.metric("Files Uploaded", len(st.session_state.get("uploaded_files", [])))

        st.markdown("---")
        st.markdown("### 🤖 AI Information")

        learning_brain = st.session_state.get("learning_brain")
        stats = learning_brain.get_learning_stats() if learning_brain else {}

        col_ai1, col_ai2, col_ai3 = st.columns(3)

        with col_ai1:
            st.metric("Topics Learned", stats.get("total_topics", 0))
            st.metric("Conversations", stats.get("total_conversations", 0))

        with col_ai2:
            st.metric("Models Tracked", stats.get("models_tracked", 0))
            model_perf = stats.get("model_performance", {})
            st.metric(
                "Total Model Calls", sum(m.get("total", 0) for m in model_perf.values())
            )

        with col_ai3:
            if stats.get("model_strengths"):
                best_model = stats["model_strengths"][0]
                st.metric("Best Model", best_model["model"][:15] + "...")
                st.metric("Best Success Rate", f"{best_model['success_rate']}%")

        st.markdown("---")
        st.markdown("### 🎛️ Configuration")

        col_config1, col_config2 = st.columns(2)

        with col_config1:
            prefs = st.session_state.get("profile_preferences", {})
            st.text_input("Theme", value=prefs.get("theme", "Auto"), disabled=True)
            st.text_input(
                "Language", value=prefs.get("language", "English"), disabled=True
            )

        with col_config2:
            st.text_input("Timezone", value=prefs.get("timezone", "UTC"), disabled=True)
            notifications_status = (
                "✅ Enabled" if prefs.get("notifications", True) else "❌ Disabled"
            )
            st.text_input("Notifications", value=notifications_status, disabled=True)

        st.markdown("---")
        st.markdown("### 🔧 Feature Status")

        col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)

        with col_feat1:
            voice_status = "🔊 On" if st.session_state.voice_mode else "🔇 Off"
            st.metric("Voice Mode", voice_status)

        with col_feat2:
            multimodal_count = len(st.session_state.get("multimodal_options", []))
            st.metric("Multimodal", f"{multimodal_count} types")

        with col_feat3:
            streaming_status = (
                "✅ On" if st.session_state.get("enable_streaming", True) else "❌ Off"
            )
            st.metric("Streaming", streaming_status)

        with col_feat4:
            brain_status = (
                "🧠 On"
                if st.session_state.get("enable_brain_mode", False)
                else "⚪ Off"
            )
            st.metric("Brain Mode", brain_status)

        st.markdown("---")
        st.markdown("### 📝 Quick Debug Info")

        with st.expander("🔍 Developer Info", expanded=False):
            col_debug1, col_debug2 = st.columns(2)

            with col_debug1:
                st.write("**Session State Keys:**")
                st.code(", ".join(list(st.session_state.keys())[:10]))

            with col_debug2:
                st.write("**Memory Usage:**")
                messages_size = sys.getsizeof(st.session_state.messages)
                st.caption(f"📦 Messages: ~{messages_size / 1024:.1f} KB")

        st.markdown("---")

        # Copy session info button
        session_info = f"""
Session Information - {datetime.now().isoformat()}
User: {st.session_state.username}
Auth: {'Google OAuth' if 'google_oauth_token' in st.session_state else 'Traditional'}
Messages: {total_messages}
Platform: {platform.system()}
Python: {platform.python_version()}
"""

        if st.button("📋 Copy Session Info", width="stretch"):
            st.success("✅ Session info copied to clipboard!")
            st.code(session_info)
=======
=======

>>>>>>> origin/engagement-features-5881933724913241534
=======

>>>>>>> origin/engagement-features-3224553925721226807
=======

>>>>>>> origin/feedback-integration-17764393616523020931
=======

>>>>>>> origin/feedback-integration-7692380356929291134
import streamlit as st
import time
import json
import sys
import platform
from datetime import datetime
import pandas as pd
from ui.common import logout
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from ui.analytics import get_recent_errors, get_analytics_summary
=======
from ui.database import get_user_stats, get_all_user_stats
from ui.engagement import ACHIEVEMENTS
>>>>>>> origin/engagement-features-5881933724913241534
=======

import json
import platform
import sys
import time
from datetime import datetime

import streamlit as st
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
from ui.engagement import EngagementManager
from ui.database import get_user_stats, get_leaderboard
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/feedback-integration-7692380356929291134

def show_dashboard():
    """Display user dashboard with stats and activity"""

    # Modern gradient header for dashboard
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    # Modern gradient header for dashboard
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
    # Modern gradient header for dashboard
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
    # Modern gradient header for dashboard
>>>>>>> origin/feedback-integration-17764393616523020931
=======
    # Modern gradient header for dashboard
>>>>>>> origin/feedback-integration-7692380356929291134
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 3rem;">📊</div>
        <div>
            <h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">
                Dashboard
            </h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0.25rem 0 0 0; font-size: 1rem;">
                Your AI activity at a glance
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # User info
    user_info = st.session_state.get('user_info', {})
    user_name = user_info.get('name', st.session_state.username)
    user_email = user_info.get('email', '')

    # Welcome card
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    # Welcome card
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
    # Welcome card
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
    # Welcome card
>>>>>>> origin/feedback-integration-17764393616523020931
=======
    # Welcome card
>>>>>>> origin/feedback-integration-7692380356929291134
    st.markdown(f"""
    <div class="glass-panel" style="margin-bottom: 2rem;">
        <h3 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">Welcome back, {user_name}! 👋</h3>
        {"<p style='color: var(--text-secondary); margin: 0;'>📧 " + user_email + "</p>" if user_email else ""}
    </div>
    """, unsafe_allow_html=True)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    # --- GAMIFICATION SECTION ---
    user_id = st.session_state.get('username', 'guest')
    user_stats = get_user_stats(user_id)

    st.markdown("### 🏆 Your Progress")

    # Level & XP
    level = user_stats.get('level', 1)
    xp = user_stats.get('xp', 0)
    # Calculate progress to next level
    next_level_xp = sum([100 * i for i in range(1, level + 1)]) # Simplified for display logic if needed
    current_level_base = sum([100 * i for i in range(1, level)])
    xp_in_level = xp - current_level_base
    req_xp = 100 * level

    # Simple progress bar logic
    if req_xp > 0:
        progress = min(max(xp_in_level / req_xp, 0.0), 1.0)
    else:
        progress = 0.0

    cols_prog = st.columns([1, 3, 1])
    with cols_prog[0]:
        st.markdown(f"""
        <div style="text-align:center; padding: 1rem; background: var(--card-bg); border-radius: 10px; border: 1px solid var(--border-color);">
            <div style="font-size: 2rem;">Lvl {level}</div>
            <div style="color: var(--text-secondary); font-size: 0.8rem;">Current Level</div>
        </div>
        """, unsafe_allow_html=True)

    with cols_prog[1]:
        st.write(f"**XP Progress** ({xp_in_level}/{req_xp})")
        st.progress(progress)
        st.caption("Keep chatting to earn XP and level up!")

    with cols_prog[2]:
        st.markdown(f"""
        <div style="text-align:center; padding: 1rem; background: var(--card-bg); border-radius: 10px; border: 1px solid var(--border-color);">
            <div style="font-size: 2rem;">🔥 {user_stats.get('streak_days', 0)}</div>
            <div style="color: var(--text-secondary); font-size: 0.8rem;">Day Streak</div>
        </div>
        """, unsafe_allow_html=True)

    # Achievements
    st.markdown("#### 🏅 Achievements")
    unlocked = set(user_stats.get('achievements', []))

    ach_cols = st.columns(6)
    for idx, (code, data) in enumerate(ACHIEVEMENTS.items()):
        is_unlocked = code in unlocked
        opacity = "1" if is_unlocked else "0.3"
        filter_style = "grayscale(0%)" if is_unlocked else "grayscale(100%)"

        with ach_cols[idx % 6]:
            st.markdown(f"""
            <div style="text-align: center; opacity: {opacity}; filter: {filter_style};" title="{data['desc']}">
                <div style="font-size: 2rem;">{data['icon']}</div>
                <div style="font-size: 0.7rem; font-weight: bold;">{data['name']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- END GAMIFICATION ---

>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
    # Gamification Section
    engagement = EngagementManager()
    user_stats = get_user_stats(st.session_state.username)

    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
            <span>🏆</span> My Progress
        </h3>
    </div>
    """, unsafe_allow_html=True)

    g_col1, g_col2 = st.columns([2, 1])

    with g_col1:
        # Level and XP
        level = user_stats.get('level', 1)
        xp = user_stats.get('xp', 0)
        progress = engagement.get_next_level_progress(xp)

        st.markdown(f"**Level {level}** • {xp} XP")
        st.progress(progress)

        # Badges
        badges = engagement.get_user_badges(st.session_state.username)
        if badges:
            st.markdown("**Earned Badges:**")
            # Use a container for badges
            badge_html = "<div style='display: flex; gap: 10px; flex-wrap: wrap;'>"
            for badge in badges:
                badge_html += f"<div title='{badge['name']}: {badge['description']}' style='font-size: 2rem; cursor: help;'>{badge['icon']}</div>"
            badge_html += "</div>"
            st.markdown(badge_html, unsafe_allow_html=True)
        else:
            st.caption("Start chatting to earn badges!")

    with g_col2:
        # Mini Leaderboard
        st.markdown("**🏆 Top Users**")
        leaderboard = get_leaderboard(5)
        if leaderboard:
            for i, user in enumerate(leaderboard):
                is_me = user['user_id'] == st.session_state.username
                style = "font-weight: bold; color: var(--accent-primary);" if is_me else ""
                display_name = user['user_id'].split('@')[0] # Simple display name
                st.markdown(f"<div style='{style}'>{i+1}. {display_name} (Lvl {user['level']})</div>", unsafe_allow_html=True)
        else:
            st.caption("No data yet.")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/feedback-integration-7692380356929291134
    # Activity metrics with modern cards
    col1, col2, col3, col4 = st.columns(4)

    total_messages = len(st.session_state.get('messages', []))
    learning_brain = st.session_state.get('learning_brain')
    stats = learning_brain.get_learning_stats() if learning_brain else {}

    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-value">{total_messages}</div>
            <div class="metric-label">💬 Messages</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        topics = stats.get('total_topics', 0)
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-value">{topics}</div>
            <div class="metric-label">🧠 Topics</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        models = stats.get('models_tracked', 0)
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-value">{models}</div>
            <div class="metric-label">🤖 Models</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        convos = stats.get('total_conversations', 0)
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="metric-value">{convos}</div>
            <div class="metric-label">📚 Convos</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    # Leaderboard Section
    with st.expander("🏆 Leaderboard", expanded=False):
        all_stats = get_all_user_stats()
        # Create a DataFrame for nice display
        lb_data = []
        for i, s in enumerate(all_stats[:10]): # Top 10
            lb_data.append({
                "Rank": i + 1,
                "User": s['user_id'],
                "Level": s['level'],
                "XP": s['xp'],
                "Streak": s['streak_days']
            })

        if lb_data:
            st.table(pd.DataFrame(lb_data).set_index("Rank"))
        else:
            st.info("No data yet.")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/feedback-integration-7692380356929291134
    # Enhanced Quick actions with descriptions
    st.markdown("""
    <h3 style="display: flex; align-items: center; gap: 0.5rem;">
        <span>🚀</span> Quick Actions
    </h3>
    """, unsafe_allow_html=True)

    # Create action cards with descriptions
    action_col1, action_col2 = st.columns(2)

    with action_col1:
        st.markdown(f"""
        <div class="action-card">
            <div class="action-title">💬 Start Chatting</div>
            <div class="action-desc">Begin a new conversation with your selected AI model or enable AI Brain for multi-model responses</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Open Chat", width="stretch", type="primary", key="quick_chat_btn"):
            st.session_state.current_page = "chat"
            st.rerun()

    with action_col2:
        st.markdown("""
        <div class="action-card">
            <div class="action-title">👤 View Profile</div>
            <div class="action-desc">Manage your account settings, preferences, and view your usage statistics</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Go to Profile", width="stretch", key="quick_profile_btn"):
            st.session_state.current_page = "profile"
            st.rerun()

    action_col3, action_col4 = st.columns(2)

    with action_col3:
        st.markdown("""
        <div class="action-card">
            <div class="action-title">🧠 View Brain Stats</div>
            <div class="action-desc">See what your AI brain has learned: topics, model performance, and insights</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Show Stats", width="stretch", key="quick_brain_btn"):
            st.session_state.show_brain_stats = not st.session_state.get('show_brain_stats', False)
            st.rerun()

    with action_col4:
        st.markdown("""
        <div class="action-card">
            <div class="action-title">📥 Export Chat</div>
            <div class="action-desc">Download your chat history as JSON for backup, analysis, or sharing</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Download", width="stretch", key="quick_export_btn"):
            if st.session_state.messages:
                chat_export = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    "📥 Download Chat History",
                    chat_export,
                    file_name="chat_history.json",
                    mime="application/json",
                    width="stretch",
                    key="download_chat_btn"
                )
            else:
                st.warning("No chat history to export. Start a conversation first!")

<<<<<<< HEAD
<<<<<<< HEAD
=======

    action_col5, action_col6 = st.columns(2)

    with action_col5:
        st.markdown("""
        <div class="action-card">
            <div class="action-title">📝 Provide Feedback</div>
            <div class="action-desc">Help us improve by sharing your thoughts, reporting bugs, or suggesting features</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Give Feedback", width="stretch", key="quick_feedback_btn"):
            st.session_state.current_page = "feedback"
            st.rerun()

>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/feedback-integration-7692380356929291134
    # Additional quick action shortcuts (enhanced)
    st.markdown("---")
    st.markdown("### ⚡ Additional Actions")

    # Custom CSS for action cards
    st.markdown("""
    <style>
    .action-card {
        background: linear-gradient(135deg, var(--accent-primary)10 0%, var(--accent-secondary)10 100%);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.06);
        transition: transform 0.2s;
        color: var(--text-primary);
    }
    .action-card:hover { transform: translateY(-2px); }
    .action-icon { font-size: 1.5rem; }
    .action-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

    # Row 1: Primary actions
    st.markdown("#### Primary")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

    with quick_col1:
        if st.button("🔄 Clear Chat", width="stretch", key="clear_chat_quick"):
            st.session_state.messages = []
            st.success("✅ Chat cleared!")
            st.rerun()
        st.caption("Reset conversation")

    with quick_col2:
        if st.button("🧠 Reset Brain", width="stretch", key="reset_brain_quick"):
            learning_brain = st.session_state.learning_brain
            learning_brain.reset_learning()
            st.success("✅ Brain reset!")
            st.rerun()
        st.caption("Clear learning data")

    with quick_col3:
        if st.button("💾 Save Brain", width="stretch", key="save_brain_quick"):
            learning_brain = st.session_state.learning_brain
            path = st.session_state.get("brain_state_path", "learning_brain_state.json")
            if learning_brain.save_to_file(path):
                st.success("✅ Brain saved!")
            else:
                st.error("❌ Save failed")
        st.caption("Persist to disk")

    with quick_col4:
        if st.button("📂 Load Brain", width="stretch", key="load_brain_quick"):
            learning_brain = st.session_state.learning_brain
            path = st.session_state.get("brain_state_path", "learning_brain_state.json")
            if learning_brain.load_from_file(path):
                st.success("✅ Brain loaded!")
                st.rerun()
            else:
                st.warning("⚠️ File not found")
        st.caption("Restore from disk")

    # Row 2: Secondary actions
    st.markdown("#### Secondary")
    sec_col1, sec_col2, sec_col3, sec_col4 = st.columns(4)

    with sec_col1:
        if st.button("📊 Refresh Stats", width="stretch", key="refresh_stats_quick"):
            st.rerun()
        st.caption("Update UI")

    with sec_col2:
        if st.button("📥 Export Chat", width="stretch", key="export_chat_quick"):
            messages = st.session_state.get("messages", [])
            if messages:
                chat_blob = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
                st.download_button("Download", chat_blob, "chat_export.txt", "text/plain", key="dl_chat_quick")
            else:
                st.info("No messages to export")
        st.caption("Save conversation")

    with sec_col3:
        if st.button("📄 Download Report", width="stretch", key="dl_report_quick"):
            learning_brain = st.session_state.learning_brain
            report = learning_brain.format_learning_report()
            st.download_button("Download", report, "learning_report.md", "text/markdown", key="dl_rpt_quick2")
        st.caption("Brain insights")

    with sec_col4:
        if st.button("🔗 Copy Session ID", width="stretch", key="copy_session_quick"):
            session_id = st.session_state.get("session_id", "N/A")
            st.code(session_id)
        st.caption("For debugging")

    # Row 3: Toggles & info
    st.markdown("#### Toggles")
    tog_col1, tog_col2, tog_col3, tog_col4 = st.columns(4)

    with tog_col1:
        show_brain_stats = st.checkbox("📈 Show Brain Stats", value=st.session_state.get('show_brain_stats', False), key="toggle_brain_stats")
        st.session_state.show_brain_stats = show_brain_stats

    with tog_col2:
        dark_mode = st.checkbox("🌙 Dark Hints", value=st.session_state.get('dark_hints', False), key="toggle_dark_hints")
        st.session_state.dark_hints = dark_mode

    with tog_col3:
        auto_save = st.checkbox("💾 Auto-save Brain", value=st.session_state.get('auto_save_brain', False), key="toggle_auto_save")
        st.session_state.auto_save_brain = auto_save

    with tog_col4:
        compact_ui = st.checkbox("📐 Compact UI", value=st.session_state.get('compact_ui', False), key="toggle_compact_ui")
        st.session_state.compact_ui = compact_ui

<<<<<<< HEAD
=======
    st.markdown("#### Support")
    from ui.feedback import render_feedback_form
    with st.expander("🗣️ Give Feedback", expanded=False):
        render_feedback_form(key_suffix="dashboard")

>>>>>>> origin/feedback-integration-7692380356929291134
    # Brain stats display
    if st.session_state.get('show_brain_stats', False):
        st.divider()
        st.markdown("### 🧠 AI Brain Learning Stats")

        if stats.get('model_strengths'):
            st.markdown("#### Model Performance")
            for model_stat in stats['model_strengths'][:5]:
                col_model, col_rate, col_total = st.columns([2, 1, 1])
                with col_model:
                    st.markdown(f"**{model_stat['model']}**")
                with col_rate:
                    st.metric("Success Rate", f"{model_stat['success_rate']}%")
                with col_total:
                    st.metric("Queries", f"{model_stat['success']}/{model_stat['total']}")

        if stats.get('top_topics'):
            st.markdown("#### Top Knowledge Topics")
            cols = st.columns(min(len(stats['top_topics']), 5))
            for i, topic_info in enumerate(stats['top_topics'][:5]):
                with cols[i]:
                    st.metric(topic_info['topic'], topic_info['count'])

    # Recent activity
    st.divider()
    st.markdown("### 📝 Recent Activity")

    recent_messages = st.session_state.get('messages', [])[-5:]
    if recent_messages:
        for msg in recent_messages:
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            with st.expander(f"{role_icon} {msg['role'].title()} - {msg['content'][:50]}..."):
                st.markdown(msg['content'])
    else:
        st.info("No recent activity. Start a conversation to see your history here!")

    st.divider()

    # Enhanced system info
    with st.expander("ℹ️ System Information", expanded=False):
        st.markdown("### 📊 Session Information")

        # Session details
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Session Start", datetime.now().strftime('%H:%M:%S'))
            st.metric("Session Date", datetime.now().strftime('%Y-%m-%d'))
        with col_info2:
            uptime_seconds = time.time() - st.session_state.get('session_start_time', time.time())
            st.metric("Session Duration", f"{int(uptime_seconds // 60)} min")
            st.metric("Current Time", datetime.now().strftime('%I:%M %p'))

        st.markdown("---")
        st.markdown("### 👤 User Information")

        user_info = st.session_state.get('user_info', {})
        col_user1, col_user2 = st.columns(2)

        with col_user1:
            st.text_input("Username", value=st.session_state.username, disabled=True)
            st.text_input("Display Name", value=user_info.get('name', st.session_state.username), disabled=True)
        with col_user2:
            auth_method = "🔐 Google OAuth" if 'google_oauth_token' in st.session_state else "🔐 Traditional Login"
            st.text_input("Authentication", value=auth_method, disabled=True)
            st.text_input("Email", value=user_info.get('email', 'Not set'), disabled=True)

        st.markdown("---")
        st.markdown("### 💻 System Details")

        col_sys1, col_sys2, col_sys3 = st.columns(3)

        with col_sys1:
            st.metric("Platform", platform.system())
            st.metric("Python", platform.python_version())

        with col_sys2:
            st.metric("Streamlit", st.__version__)
            st.metric("Browser", "Chrome/Safari/Firefox")

        with col_sys3:
            total_messages = len(st.session_state.get('messages', []))
            st.metric("Messages", total_messages)
            st.metric("Files Uploaded", len(st.session_state.get('uploaded_files', [])))

        st.markdown("---")
        st.markdown("### 🤖 AI Information")

        learning_brain = st.session_state.get('learning_brain')
        stats = learning_brain.get_learning_stats() if learning_brain else {}

        col_ai1, col_ai2, col_ai3 = st.columns(3)

        with col_ai1:
            st.metric("Topics Learned", stats.get('total_topics', 0))
            st.metric("Conversations", stats.get('total_conversations', 0))

        with col_ai2:
            st.metric("Models Tracked", stats.get('models_tracked', 0))
            model_perf = stats.get('model_performance', {})
            st.metric("Total Model Calls", sum(m.get('total', 0) for m in model_perf.values()))

        with col_ai3:
            if stats.get('model_strengths'):
                best_model = stats['model_strengths'][0]
                st.metric("Best Model", best_model['model'][:15] + "...")
                st.metric("Best Success Rate", f"{best_model['success_rate']}%")

        st.markdown("---")
        st.markdown("### 🎛️ Configuration")

        col_config1, col_config2 = st.columns(2)

        with col_config1:
            prefs = st.session_state.get('profile_preferences', {})
            st.text_input("Theme", value=prefs.get('theme', 'Auto'), disabled=True)
            st.text_input("Language", value=prefs.get('language', 'English'), disabled=True)

        with col_config2:
            st.text_input("Timezone", value=prefs.get('timezone', 'UTC'), disabled=True)
            notifications_status = "✅ Enabled" if prefs.get('notifications', True) else "❌ Disabled"
            st.text_input("Notifications", value=notifications_status, disabled=True)

        st.markdown("---")
        st.markdown("### 🔧 Feature Status")

        col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)

        with col_feat1:
            voice_status = "🔊 On" if st.session_state.voice_mode else "🔇 Off"
            st.metric("Voice Mode", voice_status)

        with col_feat2:
            multimodal_count = len(st.session_state.get('multimodal_options', []))
            st.metric("Multimodal", f"{multimodal_count} types")

        with col_feat3:
            streaming_status = "✅ On" if st.session_state.get('enable_streaming', True) else "❌ Off"
            st.metric("Streaming", streaming_status)

        with col_feat4:
            brain_status = "🧠 On" if st.session_state.get('enable_brain_mode', False) else "⚪ Off"
            st.metric("Brain Mode", brain_status)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        # --- Analytics / System Health ---
        st.markdown("---")
        st.markdown("### 🩺 System Health")

        analytics_summary = get_analytics_summary()
        col_health1, col_health2, col_health3 = st.columns(3)
        with col_health1:
            st.metric("API Calls", analytics_summary.get('api_calls', 0))
        with col_health2:
            st.metric("Errors (24h)", analytics_summary.get('total_errors', 0))
        with col_health3:
            success_rate = 0
            total = analytics_summary.get('api_calls', 0)
            if total > 0:
                success_rate = (analytics_summary.get('successful_calls', 0) / total) * 100
            st.metric("API Success Rate", f"{success_rate:.1f}%")

        recent_errors = get_recent_errors(5)
        if recent_errors:
            st.markdown("#### 🚨 Recent Errors")
            for err in recent_errors:
                with st.expander(f"{err['time']} - {str(err['message'])[:50]}..."):
                    st.write(f"**Context:** {err.get('context')}")
                    st.code(err.get('message'))
                    if err.get('exception'):
                        st.write("**Exception:**")
                        st.code(str(err.get('exception')))
        else:
             st.success("✅ No recent errors detected.")

=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/feedback-integration-7692380356929291134
        st.markdown("---")
        st.markdown("### 📝 Quick Debug Info")

        with st.expander("🔍 Developer Info", expanded=False):
            col_debug1, col_debug2 = st.columns(2)

            with col_debug1:
                st.write("**Session State Keys:**")
                st.code(', '.join(list(st.session_state.keys())[:10]))

            with col_debug2:
                st.write("**Memory Usage:**")
                messages_size = sys.getsizeof(st.session_state.messages)
                st.caption(f"📦 Messages: ~{messages_size / 1024:.1f} KB")

        st.markdown("---")

        # Copy session info button
        session_info = f"""
Session Information - {datetime.now().isoformat()}
User: {st.session_state.username}
Auth: {'Google OAuth' if 'google_oauth_token' in st.session_state else 'Traditional'}
Messages: {total_messages}
Platform: {platform.system()}
Python: {platform.python_version()}
"""

        if st.button("📋 Copy Session Info", width="stretch"):
            st.success("✅ Session info copied to clipboard!")
            st.code(session_info)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> origin/analytics-monitoring-17353357073288903889
=======
>>>>>>> origin/engagement-features-5881933724913241534
=======
>>>>>>> origin/code-quality-refactor-17423438479402428749
=======
>>>>>>> origin/engagement-features-3224553925721226807
=======
>>>>>>> origin/feedback-integration-17764393616523020931
=======
>>>>>>> origin/feedback-integration-7692380356929291134

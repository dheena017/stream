import streamlit as st
import json
from typing import List, Dict, Any
from datetime import datetime

def serialize_messages_for_export(messages: List[Dict[str, Any]]) -> str:
    """
    Serialize messages to JSON string, handling non-serializable objects like PIL Images.
    """
    export_data = []
    for msg in messages:
        # Create a copy to avoid modifying the session state
        msg_copy = msg.copy()

        # Handle images
        if 'images' in msg_copy:
            # Replace PIL images with placeholder
            msg_copy['images'] = [f"[Image: {img.size}]" for img in msg_copy['images'] if hasattr(img, 'size')]

        # Handle files info which might contain non-serializable stuff (though usually just dicts)
        # Ensure 'files' is serializable

        export_data.append(msg_copy)

    return json.dumps(export_data, indent=2, default=str)

def format_messages_markdown(messages: List[Dict[str, Any]]) -> str:
    """
    Format messages as a Markdown conversation string.
    """
    md_output = [f"# Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

    for msg in messages:
        role = msg.get('role', 'unknown').capitalize()
        timestamp = msg.get('timestamp', '')
        content = msg.get('content', '')
        provider = msg.get('provider', '')
        model = msg.get('model', '')

        header = f"### {role}"
        if timestamp:
            header += f" ({timestamp})"
        if provider and model:
            header += f" - {provider}/{model}"

        md_output.append(header)
        md_output.append(f"\n{content}\n")

        if msg.get('images'):
            md_output.append(f"*[Attached {len(msg['images'])} image(s)]*\n")

        md_output.append("---\n")

    return "\n".join(md_output)

def calculate_chat_stats(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate basic statistics for the current conversation.
    """
    if not messages:
        return {}

    stats = {
        "total_messages": len(messages),
        "user_count": sum(1 for m in messages if m.get('role') == 'user'),
        "assistant_count": sum(1 for m in messages if m.get('role') == 'assistant'),
        "avg_response_time": 0.0,
        "total_chars": sum(len(m.get('content', '')) for m in messages)
    }

    # Calculate average response time
    response_times = [m.get('response_time', 0) for m in messages if m.get('role') == 'assistant' and 'response_time' in m]
    if response_times:
        stats['avg_response_time'] = sum(response_times) / len(response_times)

    return stats

def render_experimental_section():
    """
    Render the experimental features section in the sidebar.
    """
    st.markdown("### 📊 Conversation Analysis")

    messages = st.session_state.get('messages', [])

    if not messages:
        st.info("Start a conversation to see analytics and export options.")
        return

    stats = calculate_chat_stats(messages)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", stats['total_messages'])
        st.metric("Avg Speed", f"{stats['avg_response_time']:.2f}s")
    with col2:
        st.metric("User/AI", f"{stats['user_count']}/{stats['assistant_count']}")
        st.metric("Chars", stats['total_chars'])

    st.markdown("### 📤 Export Data")

    col_json, col_md = st.columns(2)

    with col_json:
        json_data = serialize_messages_for_export(messages)
        st.download_button(
            label="JSON",
            data=json_data,
            file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True,
            help="Export full conversation data (excluding images)"
        )

    with col_md:
        md_data = format_messages_markdown(messages)
        st.download_button(
            label="Markdown",
            data=md_data,
            file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
            help="Export readable conversation transcript"
        )

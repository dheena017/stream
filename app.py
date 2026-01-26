import streamlit as st
import time
import random
from ui.analytics import track_request, get_metrics, check_alerts

st.set_page_config(page_title="Streamlit AI Chat", layout="wide")

st.title("Streamlit AI Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Monitoring Dashboard in Sidebar
with st.sidebar:
    st.header("Monitoring Dashboard")

    # Refresh button
    if st.button("Refresh Metrics"):
        st.rerun()

    metrics = get_metrics()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Requests", metrics.get("total_requests", 0))
    with col2:
        st.metric("Error Rate", f"{metrics.get('error_rate', 0):.1f}%")

    st.metric("Avg Response Time", f"{metrics.get('avg_response_time', 0):.2f}s")

    st.subheader("Alerts")
    # Configurable thresholds for demo
    thresholds = {"error_rate": 10.0, "response_time": 1.0}
    alerts = check_alerts(thresholds, metrics)
    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("System Healthy")

    st.divider()
    st.caption("Recent Events")
    if metrics.get("recent_events"):
        for event in reversed(metrics["recent_events"][-5:]):
            icon = "✅" if event.get("success") else "❌"
            st.text(f"{icon} {event.get('event_type')} ({event.get('duration'):.2f}s)")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Simulate AI processing
        start_time = time.time()

        # Simulate processing delay and potential errors
        try:
            # Random delay between 0.1 and 1.5 seconds
            delay = random.uniform(0.1, 1.5)

            # 20% chance of "error" (simulated by throwing exception)
            if random.random() < 0.2:
                time.sleep(delay)
                raise Exception("Simulated provider failure")

            # Simulate streaming response
            response_text = f"Echo: {prompt} (Processed in {delay:.2f}s)"

            # Simulate streaming visual effect
            time.sleep(delay)
            full_response = response_text
            message_placeholder.markdown(full_response)

            duration = time.time() - start_time
            track_request("chat_response", duration, True, {"model": "simulated-gpt"})

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            duration = time.time() - start_time
            track_request("chat_response", duration, False, {"error": str(e)})
            st.error(f"Error generating response: {e}")

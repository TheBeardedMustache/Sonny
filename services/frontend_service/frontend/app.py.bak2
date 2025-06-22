"""app.py: Sonny Unified Chat-Only Frontend (Streamlit)."""
import os
import sys
import streamlit as st
from datetime import datetime

# Ensure the logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
log_path = os.path.abspath(os.path.join(log_dir, "chat_interactions.log"))
try:
    os.makedirs(log_dir, exist_ok=True)
except Exception:
    pass


# Chat state is kept in Streamlit session
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.set_page_config(page_title="Sonny Unified Chatbot", layout="centered")
st.title("💬 Sonny: Unified Autonomous Chat Interface")
st.caption("This interface is limited to chat interactions with Sonny AI.")

# --- Chat message rendering and input ---
chat_container = st.container()
for role, msg in st.session_state["chat_history"]:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Sonny:** {msg}")

def log_chat(role, message):
    """Append chat interaction to the unified log location."""
    dt_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{dt_str}] {role}: {message}\n"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass

user_input = st.text_input("Type your message and press Enter", "", key="user_input")
if st.button("Send", key="send_button") and user_input.strip():
    user_msg = user_input.strip()
    st.session_state["chat_history"].append(("user", user_msg))
    log_chat("USER", user_msg)

    # --- Communicate with backend for Sonny's reply ---
    with st.spinner("Sonny is thinking..."):
        try:
            # Try to use backend if available
            from backend.core.core_agent import process_chat
        except ImportError:
            def process_chat(prompt):
                return "[Sonny backend unavailable in dev mode - echoing] " + prompt
        try:
            sonny_reply = process_chat(user_msg)
        except Exception as ex:
            sonny_reply = f"[Error from Sonny backend: {ex}]"

    st.session_state["chat_history"].append(("sonny", sonny_reply))
    log_chat("SONNY", sonny_reply)
    if hasattr(st, "rerun"):
        st.rerun()
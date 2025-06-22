import streamlit as st
import os
from datetime import datetime
from pathlib import Path

# Set up logging path(s)
frontend_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs", "chat_interactions.log"))
backend_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend_core_service", "logs", "autonomy_log.log"))
symbolic_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "symbolic_ai_service", "logs", "symbolic_reasoning.log"))
try:
    os.makedirs(os.path.dirname(frontend_log_path), exist_ok=True)
except Exception:
    pass

# --------------- LOGGING UTILS ---------------
def log_frontend(role, message):
    dt_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{dt_str}] [FRONTEND|{role.upper()}] {message}\n"
    try:
        with open(frontend_log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass

def read_tail(filepath, n=40):
    """Read the last n lines from a log file."""
    try:
        lines = Path(filepath).read_text(encoding="utf-8").splitlines()
        return lines[-n:]
    except Exception:
        return ["[Log not available or not found]"]

# --------------- PAGE CONFIG ---------------
st.set_page_config(page_title="Sonny: Unified Chatbot", layout="wide")

# --------------- CHAT INTERFACE ---------------
st.title("💬 Sonny: Unified Autonomous Chatbot")
st.caption("Unified text-based chat interface with real-time backend & symbolic reasoning logs.")

# Store message history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# CHAT DISPLAY
for role, msg in st.session_state["messages"]:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(msg)

# CHAT INPUT
user_text = st.chat_input("Type your message and press Enter")
if user_text and user_text.strip():
    # Register and log user message
    st.session_state["messages"].append(("user", user_text))
    log_frontend("USER", user_text)

    # Get Sonny's backend response
    with st.chat_message("assistant"):
        with st.spinner("Sonny is thinking..."):
            try:
                from backend.core.core_agent import process_chat
            except ImportError:
                def process_chat(prompt):
                    return "[Sonny backend unavailable in dev mode - echoing] " + prompt
            try:
                sonny_text = process_chat(user_text)
            except Exception as ex:
                sonny_text = f"[Error from Sonny backend: {ex}]"
            st.markdown(sonny_text)
            st.session_state["messages"].append(("assistant", sonny_text))
            log_frontend("SONNY", sonny_text)

# --------------- REAL-TIME LOGS ---------------
st.divider()
st.subheader("📋 Real-Time Logs (Frontend, Backend, Symbolic AI)")
log_col1, log_col2, log_col3 = st.columns(3)
with log_col1:
    st.markdown("**Frontend (chat) log**")
    log_lines = read_tail(frontend_log_path)
    st.code("\n".join(log_lines), language="none")
with log_col2:
    st.markdown("**Backend Autonomy log**")
    backend_lines = read_tail(backend_log_path)
    st.code("\n".join(backend_lines), language="none")
with log_col3:
    st.markdown("**Symbolic AI log**")
    symbolic_lines = read_tail(symbolic_log_path)
    st.code("\n".join(symbolic_lines), language="none")

# --------------- DOCS ---------------
st.caption(
    "All chat and agent interactions are logged for transparency. "
    "See 'Unified_Sonny_Chatbot_Page.md' for merge notes and live logging design."
)

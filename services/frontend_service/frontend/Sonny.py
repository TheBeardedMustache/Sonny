# --- Sonny Unified Royal Diadem: Explicit Amalgamation of All Service Frontends ---
import streamlit as st
import os
from datetime import datetime
from pathlib import Path

# --------------- LOGGING UTILS ---------------
frontend_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs", "chat_interactions.log"))
backend_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend_core_service", "logs", "autonomy_log.log"))
symbolic_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "symbolic_ai_service", "logs", "symbolic_reasoning.log"))

def log_frontend(role, message):
    dt_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{dt_str}] [FRONTEND|{role.upper()}] {message}\n"
    try:
        with open(frontend_log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass

def read_tail(filepath, n=40):
    try:
        lines = Path(filepath).read_text(encoding="utf-8").splitlines()
        # Also log all realtime accesses to combined UI log
        ui_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs", "real_time_logs.log"))
        if not os.path.abspath(filepath).endswith("real_time_logs.log"):
            dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(ui_log_path, "a", encoding='utf-8') as f:
                    f.write(f"[{dt}] [read_tail] {filepath}: tail read ({n} lines) via Streamlit UI\n")
            except Exception:
                pass
        return lines[-n:]
    except Exception as ex:
        return [f"[Log not available or not found: {ex}]"]

st.set_page_config(page_title="Sonny: Royal Diadem (Unified)", layout="wide")
st.title("👑 Sonny: The Royal Diadem - Unified Agent & Chat Portal")

tabs = st.tabs([
    "Unified Chat", "Silver (Desktop Automation)", "Gold (Autonomous Coding)",
    "Cinnabar (NLU)", "Combined (Full Workflow)"
])

with tabs[0]:
    st.header(":speech_balloon: Unified Chat with Sonny")
    st.caption("Interact with Sonny using natural language. All messages & agent replies are logged.")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for role, msg in st.session_state["messages"]:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(msg)
    user_text = st.chat_input("Type your message and press Enter")
    if user_text and user_text.strip():
        st.session_state["messages"].append(("user", user_text))
        log_frontend("USER", user_text)
        with st.chat_message("assistant"):
            with st.spinner("Sonny is thinking..."):
                try:
                    from backend.core.autonomous_agent import AutonomousAgent
                    agent = AutonomousAgent(system_prompt="You are Sonny, backend autonomy agent for unified chat. Log and explain each step.")
                    sonny_text = agent.process_chat(user_text)
                except Exception as ex:
                    sonny_text = f"[Error from Sonny backend: {ex}]"
                st.markdown(sonny_text)
                st.session_state["messages"].append(("assistant", sonny_text))
                log_frontend("SONNY", sonny_text)

    st.divider()
    st.subheader(":satellite: Real-Time Observability — Backend, Sophic Mercury Symbolic AI, Error, Chat, and Deep Reasoning Logs")
    # Real-time observable logs (columns): Chat, Backend, Symbolic, Error, Sophic Symbolic, Sophic Backend
    log_col1, log_col2, log_col3, log_col4, log_col5, log_col6 = st.columns([1,1,1,1,2,2])
    with log_col1:
        st.markdown("**Frontend (chat) log**")
        st.code("\n".join(read_tail(frontend_log_path)), language="none")
    with log_col2:
        st.markdown("**Backend Autonomy log**")
        st.code("\n".join(read_tail(backend_log_path)), language="none")
    with log_col3:
        st.markdown("**Symbolic AI log**")
        st.code("\n".join(read_tail(symbolic_log_path)), language="none")
    with log_col4:
        error_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend_core_service", "logs", "error_handling.log"))
        st.markdown("**Backend Errors** ")
        st.code("\n".join(read_tail(error_log_path)), language="none")
    with log_col5:
        sophic_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "symbolic_ai_service", "logs", "sophic_mercury_integration.log"))
        st.markdown("**Sophic Mercury Symbolic Reasoning (Live)**")
        st.code("\n".join(read_tail(sophic_log_path)), language="none")
    with log_col6:
        autoenh_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend_core_service", "logs", "autonomy_enhancements.log"))
        st.markdown("**Sophic Mercury Autonomy/Backend Enhancements**")
        st.code("\n".join(read_tail(autoenh_path)), language="none")
    st.button("🔄 Refresh All Logs", on_click=lambda: None)

# ... [unchanged: Silver, Gold, Cinnabar, Combined paths] ...

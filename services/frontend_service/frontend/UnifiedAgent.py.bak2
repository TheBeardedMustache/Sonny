import streamlit as st
import time
import os
import sys

# --- Websocket Live Heartbeat Indicator ---
heartbeat = st.empty()
if "heartbeat_counter" not in st.session_state:
    st.session_state["heartbeat_counter"] = 0
with heartbeat:
    st.write(f"UI Heartbeat: {st.session_state['heartbeat_counter']}")
    st.session_state["heartbeat_counter"] += 1
    time.sleep(2)
    # Remove or handle st.experimental_rerun for Streamlit version mismatch
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.warning("Streamlit experimental_rerun() not present (old version?), live updates disabled.")

# Ensure parent dir is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from components.silver import silver_ui
    from components.gold import gold_ui
    from components.cinnabar import cinnabar_ui
    from components.combined import combined_ui
    from components.home import home_page
    from components.autonomous_testing import autonomous_testing_ui
except ImportError:
    from frontend.components.silver import silver_ui
    from frontend.components.gold import gold_ui
    from frontend.components.cinnabar import cinnabar_ui
    from frontend.components.combined import combined_ui
    from frontend.components.home import home_page
    from frontend.components.autonomous_testing import autonomous_testing_ui

# Chat message state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.set_page_config(page_title="Sonny Unified Agent", layout="wide")
st.title("Sonny: Unified Autonomous Agent")
# Tabs for each path
tabs = st.tabs(["Home", "Silver", "Gold", "Cinnabar", "Combined", "Autonomous Testing", "Talk to Sonny"])

with tabs[0]:
    home_page()
with tabs[1]:
    silver_ui()
with tabs[2]:
    gold_ui()
with tabs[3]:
    cinnabar_ui()
with tabs[4]:
    combined_ui()
with tabs[5]:
    autonomous_testing_ui()

# --- Chat Tab ---
with tabs[6]:
    st.header("Talk to Sonny")
    chat_box = st.container()
    for entry in st.session_state["chat_history"]:
        role, msg = entry
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Sonny:** {msg}")
    user_msg = st.text_input("Type your message and press Enter", "", key="user_prompt")
    if st.button("Send", key="chat_send_button") and user_msg.strip():
        # Add user message
        st.session_state["chat_history"].append(("user", user_msg.strip()))
        # Backend interaction: Try direct import, else dummy
        try:
            from backend.core.core_agent import process_chat
        except ImportError:
            def process_chat(prompt):
                return "[Sonny backend unavailable in dev mode - echoing] " + prompt
        with st.spinner("Sonny is thinking..."):
            try:
                sonny_reply = process_chat(user_msg.strip())
            except Exception as ex:
                sonny_reply = f"[Error from Sonny backend: {ex}]"
        st.session_state["chat_history"].append(("sonny", sonny_reply))
        st.rerun()  # Refresh chat
# --- Websocket Live Heartbeat Indicator ---
import time
heartbeat = st.empty()
if "heartbeat_counter" not in st.session_state:
    st.session_state["heartbeat_counter"] = 0
with heartbeat:
    st.write(f"UI Heartbeat: {st.session_state['heartbeat_counter']}")
    st.session_state["heartbeat_counter"] += 1
    time.sleep(2)
    st.experimental_rerun()


import streamlit as st
import time
import os
import sys

# --- Websocket Live Heartbeat Indicator ---
def add_heartbeat():
    heartbeat = st.empty()
    if "heartbeat_counter" not in st.session_state:
        st.session_state["heartbeat_counter"] = 0
    with heartbeat:
        st.write(f"UI Heartbeat: {st.session_state['heartbeat_counter']}")
        st.session_state["heartbeat_counter"] += 1

add_heartbeat()

# Ensure parent dir is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from components.silver import silver_ui
    from components.gold import gold_ui
    from components.cinnabar import cinnabar_ui
    from components.combined import combined_ui
    from components.home import home_page
    from components.autonomous_testing import autonomous_testing_ui
except ImportError:
    from frontend.components.silver import silver_ui
    from frontend.components.gold import gold_ui
    from frontend.components.cinnabar import cinnabar_ui
    from frontend.components.combined import combined_ui
    from frontend.components.home import home_page
    from frontend.components.autonomous_testing import autonomous_testing_ui

# Chat message state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.set_page_config(page_title="Sonny Unified Agent", layout="wide")
st.title("Sonny: Unified Autonomous Agent")
# Tabs for each path
tabs = st.tabs(["Home", "Silver", "Gold", "Cinnabar", "Combined", "Autonomous Testing", "Talk to Sonny"])

with tabs[0]:
    home_page()
with tabs[1]:
    silver_ui()
with tabs[2]:
    gold_ui()
with tabs[3]:
    cinnabar_ui()
with tabs[4]:
    combined_ui()
with tabs[5]:
    autonomous_testing_ui()

# --- Chat Tab ---
with tabs[6]:
    st.header("Talk to Sonny")
    chat_box = st.container()
    for entry in st.session_state["chat_history"]:
        role, msg = entry
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Sonny:** {msg}")
    user_msg = st.text_input("Type your message and press Enter", "", key="user_prompt")
    if st.button("Send", key="chat_send_button") and user_msg.strip():
        # Add user message
        st.session_state["chat_history"].append(("user", user_msg.strip()))
        # Backend interaction: Try direct import, else dummy
        try:
            from backend.core.core_agent import process_chat
        except ImportError:
            def process_chat(prompt):
                return "[Sonny backend unavailable in dev mode - echoing] " + prompt
        with st.spinner("Sonny is thinking..."):
            try:
                sonny_reply = process_chat(user_msg.strip())
            except Exception as ex:
                sonny_reply = f"[Error from Sonny backend: {ex}]"
        st.session_state["chat_history"].append(("sonny", sonny_reply))
        st.rerun()  # Refresh chat
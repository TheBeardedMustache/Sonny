# app.py: Entry point for the Sonny frontend application using Streamlit.

import streamlit as st
from frontend.Home_Page import main as home_page
from backend.core.core_agent import SilverAutomation, GoldAutomation, process_request, symbolic_state
from backend.core.core_agent import SilverAutomation, GoldAutomation, process_request

def silver_ui():
    st.header("Silver Path: Desktop Automation")
    sa = SilverAutomation()
    x = st.number_input("X-coordinate", value=0)
    y = st.number_input("Y-coordinate", value=0)
    duration = st.number_input("Duration (seconds)", value=0.0)
    if st.button("Move Mouse"):
        try:
            sa.move_mouse(x, y, duration)
            st.success(f"Moved mouse to ({x}, {y})")
        except Exception as e:
            st.exception(e)
    if st.button("Click Mouse"):
        try:
            sa.click(x, y)
            st.success(f"Clicked at ({x}, {y})")
        except Exception as e:
            st.exception(e)
    # Display symbolic state for real-time feedback
    st.markdown("**Symbolic State:**")
    st.json(symbolic_state.get_state())

def gold_ui():
    st.header("Gold Path: Autonomous Coding")
    ga = GoldAutomation()
    prompt = st.text_area("Prompt", "")
    model = st.text_input("Model", "gpt-4")
    max_tokens = st.number_input("Max Tokens", value=1024)
    if st.button("Generate Script"):
        try:
            code = ga.generate_script(prompt, model=model, max_tokens=int(max_tokens))
            st.code(code, language="python")
        except Exception as e:
            st.exception(e)
    # Display symbolic state
    st.markdown("**Symbolic State:**")
    st.json(symbolic_state.get_state())

def cinnabar_ui():
    st.header("Cinnabar Path: Natural Language Understanding")
    text = st.text_area("Input Text", "")
    if st.button("Interpret Input"):
        try:
            response = process_request(text)
            st.write(response)
        except Exception as e:
            st.exception(e)
    # Display symbolic state
    st.markdown("**Symbolic State:**")
    st.json(symbolic_state.get_state())

def combined_ui():
    st.header("Combined Path: Full Workflow")
    st.write("Generate and execute tasks in a unified workflow.")
    # Display symbolic state for combined insights
    st.markdown("**Symbolic State:**")
    st.json(symbolic_state.get_state())

def main():
    st.sidebar.title("Sonny Navigation")
    choice = st.sidebar.radio(
        "Choose Path",
        ["Home", "Silver", "Gold", "Cinnabar", "Combined"],
    )
    if choice == "Home":
        home_page()
    elif choice == "Silver":
        silver_ui()
    elif choice == "Gold":
        gold_ui()
    elif choice == "Cinnabar":
        cinnabar_ui()
    elif choice == "Combined":
        combined_ui()

if __name__ == "__main__":
    main()
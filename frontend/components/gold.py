"""
gold.py: Streamlit UI for Gold Path (Autonomous Coding).
"""
import streamlit as st


def gold_ui():
    """Render the Gold Path UI for autonomous code generation."""
    st.header("Gold Path: Autonomous Coding")
    # Dynamic import to respect frontend.app overrides in tests
    try:
        from frontend.app import GoldAutomation, symbolic_state
    except ImportError:
        from backend.core.core_agent import GoldAutomation, symbolic_state
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
    st.subheader("Symbolic State")
    st.json(symbolic_state.get_state())
"""
cinnabar.py: Streamlit UI for Cinnabar Path (Natural Language Understanding).
"""
import streamlit as st
from backend.core.core_agent import process_request, symbolic_state

def cinnabar_ui():
    """Render the Cinnabar Path UI for NLU interactions."""
    st.header("Cinnabar Path: Natural Language Understanding")
    text = st.text_area("Input Text", "")
    if st.button("Interpret Input"):
        try:
            response = process_request(text)
            st.write(response)
        except Exception as e:
            st.exception(e)
    with st.expander("Symbolic State (click to view)"):
        st.json(symbolic_state.get_state())
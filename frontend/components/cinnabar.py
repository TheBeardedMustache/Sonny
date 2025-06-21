"""
cinnabar.py: Streamlit UI for Cinnabar Path (Natural Language Understanding).
"""
import streamlit as st

def cinnabar_ui():
    """Render the Cinnabar Path UI for NLU interactions."""
    st.header("Cinnabar Path: Natural Language Understanding")
    text = st.text_area("Input Text", "")
    if st.button("Interpret Input"):
        with st.spinner("Interpreting input..."):
            try:
                # Dynamic import to allow test overrides
                try:
                    from frontend.app import process_request
                except ImportError:
                    from backend.core.core_agent import process_request
                response = process_request(text)
                st.write(response)
            except Exception as e:
                st.exception(e)
    # Dynamic import for symbolic_state
    try:
        from frontend.app import symbolic_state
    except ImportError:
        from backend.core.core_agent import symbolic_state
    st.subheader("Symbolic State")
    st.json(symbolic_state.get_state())
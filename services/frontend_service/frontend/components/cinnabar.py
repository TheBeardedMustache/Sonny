"""
cinnabar.py: Streamlit UI for Cinnabar Path (Natural Language Understanding).
"""
import streamlit as st

def cinnabar_ui():
    """Render the Cinnabar Path UI for NLU interactions."""
    st.header("Cinnabar Path: Natural Language Understanding")
    text = st.text_area("Input Text", "")
    @st.cache_data(ttl=300)
    def interpret_cached(text: str):
        try:
            from frontend.app import process_request
        except ImportError:
            from backend.core.core_agent import process_request
        return process_request(text)

    if st.button("Interpret Input"):
        with st.spinner("Interpreting input..."):
            try:
                response = interpret_cached(text)
                st.write(response)
            except Exception as e:
                st.exception(e)
    # Dynamic import for symbolic_state
    try:
        from frontend.app import symbolic_state
    except ImportError:
        from backend.core.core_agent import symbolic_state
    @st.cache_data(ttl=10)
    def get_state_cached():
        return symbolic_state.get_state()

    st.subheader("Symbolic State")
    st.json(get_state_cached())